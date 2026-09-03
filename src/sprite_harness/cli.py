"""Agent-friendly command-line interface and JSON protocol."""

from __future__ import annotations

import argparse
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
from .contracts import ContractViolation
from .exit_codes import (
    MALFORMED_SPECIFICATION,
    MISSING_INPUT,
    PROCESSING_FAILURE,
    SUCCESS,
    VALIDATION_FAILURE,
)
from .jsonio import dumps_strict
from .normalize import NormalizationError, normalize_animation
from .plan import load_plan
from .processing import ProcessingError, ensure_safe_build_output
from .preview import create_preview
from .qa import build_qa_report, qa_report_path, write_json_artifact
from .render import render_build
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
        "--source", type=Path, help="Single source PNG; overrides source.image, conflicts with source.layers."
    )
    plan.add_argument(
        "--output",
        type=Path,
        help="Build directory (default: 'build' beside the spec file).",
    )
    plan.add_argument("--json", action="store_true", dest="as_json")

    render = subparsers.add_parser(
        "render",
        help="Render build/frames/ from a bound single sprite or explicit PNG layers.",
    )
    render.add_argument("build", type=Path, help="Build directory produced by 'plan'.")
    render.add_argument(
        "--reduced-motion",
        action="store_true",
        help="Render the reduced-motion variant the plan declares "
        "(reduced_motion.mode) instead of full motion.",
    )
    render.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace previously rendered declared frame files and render.json.",
    )
    render.add_argument("--generated-input", action="store_true", help="Use accepted source replacements; never calls an adapter.")
    render.add_argument("--json", action="store_true", dest="as_json")

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
    generation = subparsers.add_parser('generate', help='Explicitly run an external adapter and freeze checked source replacements.')
    generation.add_argument('build', type=Path)
    generation.add_argument('--spec', type=Path, required=True)
    generation.add_argument('--adapter-argv', required=True, help='JSON array of explicit executable and arguments; no shell.')
    generation.add_argument('--timeout', type=float, default=120)
    generation.add_argument('--overwrite', action='store_true')
    generation.add_argument('--json', action='store_true', dest='as_json')
    exporter = subparsers.add_parser('export', help='Pack validated builds into one deterministic grid atlas.')
    exporter.add_argument('--spec', type=Path, required=True)
    exporter.add_argument('--output', type=Path, required=True)
    exporter.add_argument('--overwrite', action='store_true')
    exporter.add_argument('--json', action='store_true', dest='as_json')
    export_validator = subparsers.add_parser('validate-export', help='Revalidate inputs and every atlas pixel offline.')
    export_validator.add_argument('output', type=Path)
    export_validator.add_argument('--json', action='store_true', dest='as_json')
    return parser


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("animation", help="Animation directory, spec path, or build directory.")
    parser.add_argument("--json", action="store_true", dest="as_json")


def _emit(payload: dict[str, Any], as_json: bool, human: str | None = None) -> None:
    if as_json:
        print(dumps_strict(payload, indent=2, sort_keys=True, ensure_ascii=False))
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
        output = args.output if args.output is not None else plan.spec_dir / "build"
        payload = create_build(plan, output, source_override=args.source)
    except SpecLoadError as exc:
        return _spec_error_payload(args.command, exc, args.as_json)
    payload = {"command": args.command, "spec": str(plan.spec_path), **payload}
    _emit(payload, args.as_json)
    return SUCCESS if payload["success"] else VALIDATION_FAILURE


def _run_render(args: argparse.Namespace) -> int:
    try:
        build = load_build(args.build)
    except SpecLoadError as exc:
        return _spec_error_payload(args.command, exc, args.as_json)
    payload = render_build(
        build, reduced_motion=args.reduced_motion, overwrite=args.overwrite, generated_input=args.generated_input
    )
    payload = {"command": args.command, **payload}
    human: str | None = None
    if payload["success"]:
        lines = [
            f"Rendered {payload['frame_count']} frames "
            f"(mode: {payload['mode']}) -> {payload['frames_dir']}"
        ]
        for warning in payload.get("warnings", []):
            if warning.get("code") == "TARGET_TRACKS_SKIPPED":
                skipped = ", ".join(
                    f"{track['track_id']} ({track['target']})"
                    for track in warning.get("tracks", [])
                )
                lines.append(
                    "Skipped target-local tracks (not rendered, whole-sprite "
                    f"transforms only): {skipped}"
                )
        human = "\n".join(lines)
    _emit(payload, args.as_json, human=human)
    return SUCCESS if payload["success"] else VALIDATION_FAILURE


def _run_build_command(args: argparse.Namespace) -> int:
    try:
        build = load_build(args.animation)
    except SpecLoadError as exc:
        return _spec_error_payload(args.command, exc, args.as_json)

    result, checks = validate_build(build)
    from .contracts import read_json
    state = {'backend': 'external', 'mode': 'full'}
    if result.valid and (build.build_dir / 'render.json').is_file():
        manifest = read_json(build.build_dir / 'render.json')
        state = {'backend': manifest.get('backend', 'deterministic'), 'mode': manifest['mode']}
    elif not result.valid:
        state = {'backend': 'unverified', 'mode': 'unverified'}
    if args.command == "validate":
        payload = {
            "command": args.command,
            "build": str(build.build_dir),
            "animation_id": build.animation_id,
            "checks": checks,
            **state,
            **result.as_dict(),
        }
        if args.write_qa and not any(e.code.endswith('TRANSACTION_INCOMPLETE') for e in result.errors):
            stage = "frames" if build.frames_dir.is_dir() else "build"
            qa_path = qa_report_path(build.build_dir, stage)
            ensure_safe_build_output((*build.protected_paths, build.build_dir / 'render.json', *(build.build_dir / f'frames/frame_{i:03d}.png' for i in range(build.plan.frame_count))), qa_path, build.build_dir)
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
        human = f"Validation passed ({state['backend']}, {state['mode']})." if result.valid else None
        _emit(payload, args.as_json, human=human)
        return SUCCESS if result.valid else VALIDATION_FAILURE

    if args.command == "report":
        artifacts = {
            "frames": build.frames_dir,
            "render_manifest": build.build_dir / "render.json",
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
            "source_mode": "layered" if build.plan.layered else "single",
            **state,
            "checks": checks,
            "layer_targets": [layer.target for layer in build.plan.layers or ()],
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
            f"Backend: {state['backend']}; motion: {state['mode']}",
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
        ensure_safe_build_output((*build.protected_paths, build.build_dir / 'render.json', *(build.build_dir / f'frames/frame_{i:03d}.png' for i in range(build.plan.frame_count))), output, build.build_dir)
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
        ensure_safe_build_output((*build.protected_paths, build.build_dir / 'render.json', *(build.build_dir / f'frames/frame_{i:03d}.png' for i in range(build.plan.frame_count))), output, build.build_dir)
        payload = create_contact_sheet(spec, output, thumb_size=args.thumb_size)
    _emit({"command": args.command, **payload}, args.as_json)
    return SUCCESS


def _atlas_human(payload):
    return '\n'.join([f"Atlas validated: {payload['frame_count']} frames, {payload['clip_count']} clips.",
                       *(f"  {clip['id']}: {clip['backend']}, {clip['mode']}" for clip in payload['clips'])])


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if '--json' in arguments:
        import contextlib
        import io
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                args = _parser().parse_args(arguments)
        except SystemExit as exc:
            if exc.code != 2:
                raise
            _emit({'command': arguments[0] if arguments else '', 'valid': False,
                   'errors': [{'code': 'MALFORMED_COMMAND', 'message': 'Invalid command arguments; use --help for the command contract.'}]}, True)
            return MALFORMED_SPECIFICATION
    else:
        args = _parser().parse_args(arguments)
    try:
        if args.command in ('generate', 'export', 'validate-export'):
            from .atlas import export_atlas, validate_export
            from .generation import generate_build
            from .contracts import parse_json
            if args.command == 'generate':
                try:
                    argv = parse_json(args.adapter_argv)
                except ValueError as exc:
                    raise SpecLoadError('MALFORMED_SPEC', '--adapter-argv must be a JSON array.') from exc
                payload = generate_build(load_build(args.build), args.spec, argv, timeout=args.timeout, overwrite=args.overwrite)
            elif args.command == 'export':
                payload = export_atlas(args.spec, args.output, overwrite=args.overwrite)
            else:
                payload = validate_export(args.output)
            human = None
            if args.command == 'validate-export':
                human = _atlas_human(payload)
            elif args.command == 'generate':
                human = f"Accepted {payload['accepted_count']} source replacements -> {payload['output']} (frames require render and validate)."
            _emit({'command': args.command, **payload}, args.as_json, human=human)
            return SUCCESS
        if args.command == 'report':
            from .atlas import export_marker, validate_export
            candidate = Path(args.animation).expanduser().absolute()
            if (candidate / 'export-config.json').exists() or export_marker(candidate).exists():
                payload = validate_export(candidate)
                _emit({'command': 'report', **payload}, args.as_json, human=_atlas_human(payload))
                return SUCCESS
        if args.command == "plan":
            return _run_plan(args)

        if args.command == "render":
            return _run_render(args)

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
    except SpecLoadError as exc:
        return _spec_error_payload(args.command, exc, args.as_json)
    except ContractViolation as exc:
        _emit({'command': args.command, 'valid': False, 'success': False, 'errors': [exc.as_error()]}, args.as_json)
        return VALIDATION_FAILURE
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
