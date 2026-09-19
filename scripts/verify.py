#!/usr/bin/env python3
"""Run local Sprite Harness acceptance gates and bind them to one source snapshot."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def source_files() -> list[str]:
    output = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
    )
    names = [part.decode("utf-8") for part in output.split(b"\0") if part]
    return sorted(name for name in names if not name.startswith("build/"))


def source_snapshot() -> dict:
    files = {}
    digest = hashlib.sha256()
    for name in source_files():
        path = ROOT / name
        if not path.is_file():
            value = None
        else:
            value = hashlib.sha256(path.read_bytes()).hexdigest()
        files[name] = value
        digest.update(name.encode("utf-8") + b"\0")
        digest.update((value or "MISSING").encode("ascii") + b"\0")
    return {"sha256": digest.hexdigest(), "files": files}


def run_verification(root: Path) -> int:
    if root != ROOT:
        raise ValueError(f"verification root must be {ROOT}")
    started = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    artifact = Path("build/verification") / started
    output = root / artifact
    output.mkdir(parents=True, exist_ok=False)
    before = source_snapshot()
    report = {
        "version": 1,
        "started_utc": started,
        "artifact": str(artifact / "report.json"),
        "git": {
            "head": git_output("rev-parse", "HEAD"),
            "branch": git_output("branch", "--show-current"),
            "dirty": bool(git_output("status", "--porcelain")),
        },
        "snapshot": before,
        "status": "failed",
        "gates": [],
        "errors": [],
        "trust_scope": (
            "Local workflow metadata, source byte-compilation, pytest, and one layered source-tree CLI smoke path. "
            "No network, dependency installation, live provider, manual visual approval, consumer-native verification, "
            "installation, code signing, remote CI, commit, push, tag, or package publication."
        ),
    }
    environment = dict(os.environ)
    python_path = str(root / "src")
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = python_path if not existing else python_path + os.pathsep + existing

    def save() -> None:
        serialized = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        (output / "report.json").write_text(serialized, encoding="utf-8")
        latest = root / "build/verification/latest.json"
        latest.parent.mkdir(parents=True, exist_ok=True)
        pending = latest.with_suffix(".tmp")
        pending.write_text(serialized, encoding="utf-8")
        pending.replace(latest)

    def run(name: str, command: list[str], *, env: dict | None = None) -> None:
        print(f"Checking {name}...", flush=True)
        start = time.monotonic()
        process = subprocess.run(
            command,
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )
        log = output / f"{name}.log"
        log.write_text(process.stdout + process.stderr, encoding="utf-8")
        report["gates"].append(
            {
                "name": name,
                "command": command,
                "exit_code": process.returncode,
                "seconds": round(time.monotonic() - start, 3),
                "log": str(artifact / log.name),
            }
        )
        save()
        if process.returncode:
            raise RuntimeError(f"{name} failed; see {artifact / log.name}")

    smoke = output / "smoke"
    try:
        run("workflow", [sys.executable, "workflow/update.py", "--check"])
        run("diff-check", ["git", "diff", "--check", "HEAD", "--"])
        run(
            "compileall",
            [sys.executable, "-m", "compileall", "-q", "src", "adapters/openai/src", "scripts", "tests", "workflow"],
        )
        run("pytest", [sys.executable, "-m", "pytest"])
        run("smoke-fixture", [sys.executable, "scripts/create_layered_placeholder.py", str(smoke)], env=environment)
        build = smoke / "build"
        run(
            "smoke-plan",
            [sys.executable, "-m", "sprite_harness", "plan", "--spec", str(smoke / "animation.json"), "--output", str(build), "--json"],
            env=environment,
        )
        run("smoke-render", [sys.executable, "-m", "sprite_harness", "render", str(build), "--json"], env=environment)
        run(
            "smoke-validate",
            [sys.executable, "-m", "sprite_harness", "validate", str(build), "--write-qa", "--json"],
            env=environment,
        )
        run("smoke-report", [sys.executable, "-m", "sprite_harness", "report", str(build), "--json"], env=environment)
        report["status"] = "passed"
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        report["errors"].append(str(exc))
    after = source_snapshot()
    if after["sha256"] != before["sha256"]:
        report["status"] = "failed"
        report["errors"].append("Sources changed during verification; rerun on a coherent snapshot.")
        report["after_snapshot"] = after
    report["finished_utc"] = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    save()
    print(f"Verification {report['status']}: {artifact / 'report.json'}", flush=True)
    for error in report["errors"]:
        print(error, file=sys.stderr)
    return 0 if report["status"] == "passed" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        return run_verification(args.root.resolve())
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
