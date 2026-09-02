"""QA report assembly and serialization.

QA reports are deterministic JSON documents (no wall-clock timestamps) so that
re-running the same stage over the same inputs yields byte-identical output.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import __version__
from .validator import ValidationResult


QA_VERSION = 1
QA_DIRNAME = "qa"


def build_qa_report(
    *,
    stage: str,
    animation_id: str,
    result: ValidationResult,
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "qa_version": QA_VERSION,
        "stage": stage,
        "animation_id": animation_id,
        "generated_by": f"sprite-harness {__version__}",
        "valid": result.valid,
        "errors": [error.as_dict() for error in result.errors],
        "warnings": [warning.as_dict() for warning in result.warnings],
        "checks": checks,
    }


def write_json_artifact(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def qa_report_path(build_dir: Path, stage: str) -> Path:
    return build_dir / QA_DIRNAME / f"{stage}.qa.json"
