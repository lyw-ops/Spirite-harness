"""Agent-friendly command-line interface and JSON protocol."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from . import __version__
from .build import (
    build_to_animation_spec,
    create_build,
    is_build_dir,
    load_build,
    validate_build,
)
from .contact_sheet import create_contact_sheet
from .exit_codes import (
    MALFORMED_SPECIFICATION,
    MISSING_INPUT,
    PROCESSING_FAILURE,
    SUCCESS,
    VALIDATION_FAILURE,
)
from .normalize import NormalizationError, normalize_animation
from .plan import load_plan
from .processing import ProcessingError
from .preview import create_preview
from .qa import build_qa_report, qa_report_path, write_json_artifact
from .report import build_report, human_report
from .spec import SpecLoadError, load_spec
from .validator import validate_animation


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sprite-harness",
        description="Validate and prepare provider-agnostic sprite animations.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser(
        "plan", help="Normalize and expand an Animation Plan into a build directory."
    )
    plan.add_argument("--spec", type=Path, required=True, help="Animation Plan JSON/YAML file.")
    plan.add_argument(
        "--source", type=Path, help="Source sprite PNG; overrides the plan's source.image."
    )
    plan.add_argument(
        "--output",
        type=Path,
        help="Build directory (default: 'build' beside the spec file).",
    )
    plan.add_argument("--json", action="store_true", dest="as_json")

    validate = subparsers.add_parser(
        "validate", help="Validate an animation directory or a plan build directory."
    )
    _common(validate)
    validate.add_argument(
        "--write-qa",
        action="store_true",
        help="For build directories: also write qa/frames.qa.json.",
    )

    normalize = subparsers.add_parser(
        "normalize", help="Write normalized frames to a derived-artwork directory."
    )
    _common(normalize)
    normalize.add_argument("--output", type=Path, help="Derived output directory.")
    normalize.add_argument(
        "--scale",
        choices=("none", "fit"),
        default="none",
        help="Uniform scaling policy; scaling is never implicit.",
    )

    preview = subparsers.add_parser("preview", help="Generate an animated GIF preview.")
    _common(preview)
    preview.add_argument("--output", type=Path, help="Preview GIF path.")

    sheet = subparsers.add_parser(
        "contact-sheet", help="Generate a deterministic labeled contact sheet."
    )
    _common(sheet)
    sheet.add_argument("--output", type=Path, help="Contact-sheet PNG path.")
    sheet.add_argument("--thumb-size", type=int, default=192, metavar="PX")

    report = subparsers.add_parser("report", help="Report metadata and artifact status.")
    _common(report)
    return parser


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("animation", help="Animation directory, spec path, or build directory.")
    parser.add_argument("--json", action="store_true", dest="as_json")


def _emit(payload: dict[str, Any], as_json: bool, human: str | None = None) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    elif human is not None:
        print(human)
    elif payload.get("success", payload.get("valid", False)):
        output = payload.get("output") or payload.get("output_dir")
        print(f"OK{': ' + str(output) if output else ''}")
    else:
        for error in payload.get("errors", []):
            print(f"[{error.get('code', 'ERROR')}] {error.get('message', '')}", file=sys.stderr)


def _spec_error_payload(command: str, exc: SpecLoadError, as_json: bool) -> int:
    payload = {"command": command, "valid": False, "errors": [exc.as_error()]}
    _emit(payload, as_json)
    if exc.code in {"INPUT_NOT_FOUND", "SPEC_NOT_FOUND"}:
        return MISSING_INPUT
    return MALFORMED_SPECIFICATION


def _load_or_error(args: argparse.Namespace) -> tuple[Any | None, int | None]:
    try:
        return load_spec(args.animation), None
    except SpecLoadError as exc:
        return None, _spec_error_payload(args.command, exc, args.as_json)


def _run_plan(args: argparse.Namespace) -> int:
    try:
        plan = load_plan(args.spec)
    except SpecLoadError as exc:
        return _spec_error_payload(args.command, exc, args.as_json)
    output = args.output if args.output is not None else plan.spec_dir / "build"
    payload = create_build(plan, output, source_override=args.source)
    payload = {"command": args.command, "spec": str(plan.spec_path), **payload}
    _emit(payload, args.as_json)
    return SUCCESS if payload["success"] else VALIDATION_FAILURE


def _run_build_command(args: argparse.Namespace) -> int:
    try:
        build = load_build(args.animation)
    except SpecLoadError as exc:
        return _spec_error_payload(args.command, exc, args.as_json)

    result, checks = validate_build(build)
    if args.command == "validate":
        payload = {
            "command": args.command,
            "build": str(build.build_dir),
            "animation_id": build.animation_id,
            "checks": checks,
            **result.as_dict(),
        }
        if args.write_qa:
            stage = "frames" if build.frames_dir.is_dir() else "build"
            qa_path = qa_report_path(build.build_dir, stage)
            write_json_artifact(
                qa_path,
                build_qa_report(
                    stage=stage,
                    animation_id=build.animation_id,
                    result=result,
                    checks=checks,
                ),
            )
            payload["qa_report"] = str(qa_path)
        human = "Validation passed." if result.valid else None
        _emit(payload, args.as_json, human=human)
        return SUCCESS if result.valid else VALIDATION_FAILURE

    if args.command == "report":
        artifacts = {
            "frames": build.frames_dir,
            "preview": build.build_dir / "preview.gif",
            "contact_sheet": build.build_dir / "contact-sheet.png",
            "plan_qa": qa_report_path(build.build_dir, "plan"),
        }
        payload = {
            "command": args.command,
            "build": str(build.build_dir),
            "animation_id": build.animation_id,
            "playback": build.frame_plan.get("playback"),
            "canvas": build.frame_plan.get("canvas"),
            "anchor": build.frame_plan.get("anchor"),
            "frame_count": len(build.frame_plan.get("frames", [])),
            "validation": result.as_dict(),
            "artifacts": {
                name: {"path": str(path), "exists": path.exists()}
                for name, path in artifacts.items()
            },
        }
        human_lines = [
            f"Animation: {build.animation_id}",
            f"Build: {build.build_dir}",
            f"Frames planned: {payload['frame_count']}",
            f"Validation: {'valid' if result.valid else 'invalid'}",
        ]
        for name, artifact in payload["artifacts"].items():
            state = "present" if artifact["exists"] else "not generated"
            human_lines.append(f"  {name}: {artifact['path']} ({state})")
        _emit(payload, args.as_json, human="\n".join(human_lines))
        return SUCCESS if result.valid else VALIDATION_FAILURE

    # preview / contact-sheet require validated, rendered frames.
    if not result.valid:
        _emit({"command": args.command, **result.as_dict()}, args.as_json)
        return VALIDATION_FAILURE
    spec = build_to_animation_spec(build)
    if args.command == "preview":
        output = args.output if args.output is not None else build.build_dir / "preview.gif"
        payload = create_preview(spec, output)
    else:
        if args.thumb_size < 32:
            _emit(
                {
                    "command": args.command,
                    "success": False,
                    "errors": [
                        {
                            "code": "INVALID_THUMB_SIZE",
                            "message": "Thumbnail size must be at least 32 pixels.",
                            "actual": args.thumb_size,
                        }
                    ],
                },
                args.as_json,
            )
            return PROCESSING_FAILURE
        output = (
            args.output if args.output is not None else build.build_dir / "contact-sheet.png"
        )
        payload = create_contact_sheet(spec, output, thumb_size=args.thumb_size)
    _emit({"command": args.command, **payload}, args.as_json)
    return SUCCESS


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "plan":
            return _run_plan(args)

        if args.command != "normalize" and is_build_dir(Path(args.animation).expanduser()):
            return _run_build_command(args)

        spec, code = _load_or_error(args)
        if code is not None:
            return code

        if args.command == "validate":
            result = validate_animation(spec)
            payload = {
                "command": args.command,
                "animation": str(spec.animation_dir),
                "spec": str(spec.spec_path),
                **result.as_dict(),
            }
            human = "Validation passed." if result.valid else None
            _emit(payload, args.as_json, human=human)
            return SUCCESS if result.valid else VALIDATION_FAILURE

        if args.command == "normalize":
            try:
                result = normalize_animation(
                    spec, output_dir=args.output, scale_mode=args.scale
                )
            except NormalizationError as exc:
                payload = {
                    "command": args.command,
                    "success": False,
                    "errors": [exc.as_error()],
                }
                _emit(payload, args.as_json)
                if exc.code == "NORMALIZATION_INPUT_INVALID":
                    return VALIDATION_FAILURE
                return PROCESSING_FAILURE
            _emit({"command": args.command, **result}, args.as_json)
            return SUCCESS

        validation = validate_animation(spec)
        if args.command == "report":
            report = build_report(spec, validation)
            _emit(
                {"command": args.command, **report},
                args.as_json,
                human=human_report(report),
            )
            return SUCCESS if validation.valid else VALIDATION_FAILURE

        if not validation.valid:
            _emit(
                {"command": args.command, **validation.as_dict()}, args.as_json
            )
            return VALIDATION_FAILURE

        if args.command == "preview":
            result = create_preview(spec, args.output)
        elif args.command == "contact-sheet":
            if args.thumb_size < 32:
                _emit(
                    {
                        "command": args.command,
                        "success": False,
                        "errors": [
                            {
                                "code": "INVALID_THUMB_SIZE",
                                "message": "Thumbnail size must be at least 32 pixels.",
                                "actual": args.thumb_size,
                            }
                        ],
                    },
                    args.as_json,
                )
                return PROCESSING_FAILURE
            result = create_contact_sheet(spec, args.output, thumb_size=args.thumb_size)
        else:  # argparse guarantees this is unreachable.
            raise RuntimeError(f"Unhandled command: {args.command}")

        _emit({"command": args.command, **result}, args.as_json)
        return SUCCESS
    except ProcessingError as exc:
        payload = {
            "command": args.command,
            "success": False,
            "errors": [exc.as_error()],
        }
        _emit(payload, args.as_json)
        return PROCESSING_FAILURE
    except Exception as exc:
        payload = {
            "command": args.command,
            "success": False,
            "errors": [
                {
                    "code": "PROCESSING_ERROR",
                    "message": str(exc) or "Unexpected processing failure.",
                    "type": type(exc).__name__,
                }
            ],
        }
        _emit(payload, args.as_json)
        return PROCESSING_FAILURE


if __name__ == "__main__":
    raise SystemExit(main())
