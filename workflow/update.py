#!/usr/bin/env python3
"""Validate the canonical task ledger and generate deterministic progress views."""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = "workflow/tasks.json"
README_PATH = "workflow/README.md"
STATUS_PATH = "workflow/STATUS.md"
TREE_PATH = "workflow/TREE.mmd"
GATES = (
    "specification",
    "implementation",
    "technical",
    "visual",
    "consumer",
    "publication",
)
ALLOWED = {
    "specification": {"pending", "ready", "blocked"},
    "implementation": {"pending", "in_progress", "ready", "blocked"},
    "technical": {"pending", "running", "passed", "failed", "blocked"},
    "visual": {"not_required", "pending", "in_review", "approved", "rejected", "blocked"},
    "consumer": {"not_required", "pending", "in_progress", "verified", "failed", "blocked"},
    "publication": {"not_required", "unpublished", "pending", "published", "failed", "blocked"},
}
SUCCESS = {
    "specification": {"ready"},
    "implementation": {"ready"},
    "technical": {"passed"},
    "visual": {"approved", "not_required"},
    "consumer": {"verified", "not_required"},
    "publication": {"published", "not_required"},
}
BLOCKING = {"blocked", "failed", "rejected"}
STAGE_FOR_GATE = {
    "specification": "specification",
    "implementation": "implementation",
    "technical": "technical validation",
    "visual": "visual review",
    "consumer": "consumer integration",
    "publication": "publication",
}


def read_source(path: str, *, index: bool) -> str:
    if index:
        try:
            return subprocess.check_output(
                ["git", "show", ":" + path], cwd=ROOT, text=True, stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as exc:
            raise ValueError(f"{path} is absent from the Git index") from exc
    return (ROOT / path).read_text(encoding="utf-8")


def local_evidence_exists(path: str, *, index: bool) -> bool:
    if path.startswith(("https://", "http://")):
        return True
    candidate = PurePosixPath(path)
    if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
        return False
    if index:
        result = subprocess.run(
            ["git", "cat-file", "-e", ":" + path],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    return (ROOT / candidate).is_file()


def validate(data: dict, *, index: bool = False) -> list[str]:
    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("workflow/tasks.json: version must be 1")
    if not isinstance(data.get("updated"), str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data.get("updated", "")):
        errors.append("workflow/tasks.json: updated must be YYYY-MM-DD")
    policy = data.get("policy")
    if not isinstance(policy, dict) or policy.get("gate_order") != list(GATES):
        errors.append("workflow/tasks.json: policy.gate_order must match the canonical gate order")
    tasks = data.get("tasks")
    if not isinstance(tasks, dict) or not tasks:
        return errors + ["workflow/tasks.json: tasks must be a nonempty object"]

    for task_id, task in sorted(tasks.items()):
        prefix = f"task {task_id}"
        if not re.fullmatch(r"[A-Z][A-Z0-9-]{2,63}", task_id):
            errors.append(f"{prefix}: invalid task id")
        if not isinstance(task, dict):
            errors.append(f"{prefix}: task must be an object")
            continue
        if not isinstance(task.get("title"), str) or not task["title"].strip():
            errors.append(f"{prefix}: title must be nonempty")
        if not isinstance(task.get("kind"), str) or not task["kind"].strip():
            errors.append(f"{prefix}: kind must be nonempty")
        dependencies = task.get("depends_on")
        if not isinstance(dependencies, list) or any(not isinstance(item, str) for item in dependencies):
            errors.append(f"{prefix}: depends_on must be a list of task ids")
            dependencies = []
        elif len(set(dependencies)) != len(dependencies):
            errors.append(f"{prefix}: dependencies must be unique")
        required = task.get("required_gates")
        if not isinstance(required, list) or any(item not in GATES for item in required):
            errors.append(f"{prefix}: required_gates must use canonical gate names")
            required = []
        elif len(set(required)) != len(required):
            errors.append(f"{prefix}: required_gates must be unique")
        gates = task.get("gates")
        if not isinstance(gates, dict) or set(gates) != set(GATES):
            errors.append(f"{prefix}: gates must declare exactly {', '.join(GATES)}")
            continue
        for gate_name in GATES:
            gate = gates[gate_name]
            gate_prefix = f"{prefix} gate {gate_name}"
            if not isinstance(gate, dict):
                errors.append(f"{gate_prefix}: gate must be an object")
                continue
            status = gate.get("status")
            if status not in ALLOWED[gate_name]:
                errors.append(f"{gate_prefix}: invalid status {status!r}")
            evidence = gate.get("evidence")
            if not isinstance(evidence, list) or any(not isinstance(item, str) or not item for item in evidence):
                errors.append(f"{gate_prefix}: evidence must be a list of nonempty strings")
                evidence = []
            if status in SUCCESS[gate_name] - {"not_required"} and not evidence:
                errors.append(f"{gate_prefix}: successful status requires evidence")
            for item in evidence:
                if not local_evidence_exists(item, index=index):
                    errors.append(f"{gate_prefix}: missing or unsafe evidence {item!r}")
            if not isinstance(gate.get("note"), str) or not gate["note"].strip():
                errors.append(f"{gate_prefix}: note must be nonempty")

    for task_id, task in sorted(tasks.items()):
        if not isinstance(task, dict) or not isinstance(task.get("depends_on"), list):
            continue
        for dependency in task["depends_on"]:
            if dependency not in tasks:
                errors.append(f"task {task_id}: unknown dependency {dependency}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visiting:
            errors.append(f"workflow/tasks.json: dependency cycle reaches {task_id}")
            return
        if task_id in visited:
            return
        visiting.add(task_id)
        task = tasks.get(task_id, {})
        for dependency in task.get("depends_on", []) if isinstance(task, dict) else []:
            if dependency in tasks:
                visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in sorted(tasks):
        visit(task_id)
    return errors


def overall(task: dict) -> str:
    required = task["required_gates"]
    for gate_name in required:
        if task["gates"][gate_name]["status"] in BLOCKING:
            return "blocked"
    for gate_name in GATES:
        if gate_name in required and task["gates"][gate_name]["status"] not in SUCCESS[gate_name]:
            return STAGE_FOR_GATE[gate_name]
    return "complete"


def cell(value: object) -> str:
    return str(value).replace("|", "&#124;").replace("\n", " ").strip()


def evidence_cell(items: list[str]) -> str:
    links = []
    for item in items:
        if item.startswith(("https://", "http://")):
            links.append(f"[remote]({item})")
        else:
            links.append(f"[{Path(item).name}](../{item})")
    return ", ".join(links) if links else "—"


def render_status(data: dict) -> str:
    out = [
        "# Sprite Harness task status",
        "",
        "> Generated from `workflow/tasks.json`; do not edit by hand.",
        "",
        f"Ledger date: **{data['updated']}**.",
        "",
        "A gate records one claim only. In particular, `technical: passed` never supplies visual, consumer, installation, or publication evidence.",
        "",
        "| Task | Kind | Derived stage | Required gates | Dependencies |",
        "| --- | --- | --- | --- | --- |",
    ]
    for task_id, task in sorted(data["tasks"].items()):
        deps = ", ".join(f"`{item}`" for item in task["depends_on"]) or "—"
        required = ", ".join(task["required_gates"])
        out.append(f"| `{task_id}` · {cell(task['title'])} | {cell(task['kind'])} | **{overall(task)}** | {cell(required)} | {deps} |")
    for task_id, task in sorted(data["tasks"].items()):
        anchor = task_id.lower()
        out += ["", f'<a id="{anchor}"></a>', f"## `{task_id}` · {task['title']}", "", f"Derived stage: **{overall(task)}**.", "", "| Gate | Required | Status | Evidence | Boundary note |", "| --- | --- | --- | --- | --- |"]
        for gate_name in GATES:
            gate = task["gates"][gate_name]
            out.append(
                f"| {gate_name} | {'yes' if gate_name in task['required_gates'] else 'no'} | `{gate['status']}` | {evidence_cell(gate['evidence'])} | {cell(gate['note'])} |"
            )
    return "\n".join(out) + "\n"


def render_tree(data: dict) -> str:
    symbols = {"complete": "✓", "blocked": "!"}
    out = ["flowchart LR"]
    for task_id, task in sorted(data["tasks"].items()):
        stage = overall(task)
        symbol = symbols.get(stage, "◐")
        node = "N_" + re.sub(r"[^A-Za-z0-9_]", "_", task_id)
        label = cell(task["title"]).replace('"', "'")
        out.append(f'    {node}["{symbol} {task_id}<br/>{label}<br/>stage: {stage}"]')
    for task_id, task in sorted(data["tasks"].items()):
        target = "N_" + re.sub(r"[^A-Za-z0-9_]", "_", task_id)
        for dependency in task["depends_on"]:
            source = "N_" + re.sub(r"[^A-Za-z0-9_]", "_", dependency)
            out.append(f"    {source} --> {target}")
    out += [
        "    classDef complete fill:#dbeafe,stroke:#1d4ed8,color:#172554;",
        "    classDef active fill:#ffedd5,stroke:#c2410c,color:#431407;",
        "    classDef blocked fill:#fee2e2,stroke:#b91c1c,color:#450a0a;",
    ]
    classes: dict[str, list[str]] = {"complete": [], "active": [], "blocked": []}
    for task_id, task in sorted(data["tasks"].items()):
        stage = overall(task)
        key = stage if stage in {"complete", "blocked"} else "active"
        classes[key].append("N_" + re.sub(r"[^A-Za-z0-9_]", "_", task_id))
    for key in ("complete", "active", "blocked"):
        if classes[key]:
            out.append(f"    class {','.join(classes[key])} {key};")
    return "\n".join(out) + "\n"


def replace_block(text: str, name: str, body: str) -> str:
    pattern = re.compile(
        rf"<!-- BEGIN GENERATED {re.escape(name)} -->.*?<!-- END GENERATED {re.escape(name)} -->",
        re.DOTALL,
    )
    replacement = f"<!-- BEGIN GENERATED {name} -->\n{body.rstrip()}\n<!-- END GENERATED {name} -->"
    updated, count = pattern.subn(replacement, text)
    if count != 1:
        raise ValueError(f"workflow/README.md must contain exactly one generated {name} block")
    return updated


def render(data: dict, *, index: bool = False) -> dict[str, str]:
    status = render_status(data)
    tree = render_tree(data)
    counts: dict[str, int] = {}
    for task in data["tasks"].values():
        counts[overall(task)] = counts.get(overall(task), 0) + 1
    summary = " · ".join(f"**{count} {stage}**" for stage, count in sorted(counts.items()))
    rows = ["| Task | Derived stage | Next unsatisfied required gate |", "| --- | --- | --- |"]
    for task_id, task in sorted(data["tasks"].items()):
        stage = overall(task)
        rows.append(f"| [`{task_id}`](STATUS.md#{task_id.lower()}) | **{stage}** | {stage if stage != 'complete' else '—'} |")
    readme = read_source(README_PATH, index=index)
    readme = replace_block(readme, "SUMMARY", summary)
    readme = replace_block(readme, "TASKS", "\n".join(rows))
    readme = replace_block(readme, "TREE", f"```mermaid\n{tree.rstrip()}\n```")
    return {README_PATH: readme, STATUS_PATH: status, TREE_PATH: tree}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated views differ from the ledger")
    parser.add_argument("--index", action="store_true", help="read canonical inputs from the Git index")
    args = parser.parse_args()
    try:
        data = json.loads(read_source(TASKS_PATH, index=args.index))
        errors = validate(data, index=args.index)
        if errors:
            raise ValueError("\n".join(errors))
        outputs = render(data, index=args.index)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1
    stale = []
    for name, expected in outputs.items():
        path = ROOT / name
        actual = path.read_text(encoding="utf-8") if path.is_file() else None
        if actual != expected:
            stale.append(name)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected, encoding="utf-8")
    if args.check and stale:
        print("stale generated workflow views: " + ", ".join(stale), file=sys.stderr)
        return 1
    print(("checked" if args.check else "updated") + f" {len(outputs)} workflow views from {TASKS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
