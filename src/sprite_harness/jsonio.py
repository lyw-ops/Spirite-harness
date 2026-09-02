"""Strict JSON serialization shared by every JSON boundary.

Standard JSON has no NaN or Infinity tokens. Every artifact and every ``--json``
payload the harness emits must parse under a strict JSON parser, so
serialization always runs with ``allow_nan=False`` and non-finite numbers in
diagnostic contexts are first converted to the deterministic strings ``"NaN"``,
``"Infinity"``, and ``"-Infinity"``.
"""

from __future__ import annotations

import json
import math
from typing import Any


def json_safe(value: Any) -> Any:
    """Recursively replace non-finite numbers with deterministic strings."""

    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if value == math.inf:
            return "Infinity"
        if value == -math.inf:
            return "-Infinity"
        return value
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def dumps_strict(value: Any, **kwargs: Any) -> str:
    """``json.dumps`` that never emits NaN/Infinity tokens."""

    return json.dumps(json_safe(value), allow_nan=False, **kwargs)


def json_compat_problems(value: Any, path: str = "metadata") -> list[dict[str, str]]:
    """Why ``value`` is not representable as standard JSON, if at all.

    Accepts null, booleans, integers, finite floats, strings, arrays, and
    objects with string keys — the exact JSON data model. YAML-only values
    (dates, sets, binary, custom objects) and non-finite numbers are reported
    with their path.
    """

    if value is None or isinstance(value, (bool, int, str)):
        return []
    if isinstance(value, float):
        if not math.isfinite(value):
            return [{"path": path, "reason": "non-finite number"}]
        return []
    if isinstance(value, list):
        problems: list[dict[str, str]] = []
        for index, item in enumerate(value):
            problems.extend(json_compat_problems(item, f"{path}[{index}]"))
        return problems
    if isinstance(value, dict):
        problems = []
        for key, item in value.items():
            if not isinstance(key, str):
                problems.append(
                    {
                        "path": f"{path}.{key!r}",
                        "reason": f"object keys must be strings, got {type(key).__name__}",
                    }
                )
            else:
                problems.extend(json_compat_problems(item, f"{path}.{key}"))
        return problems
    return [{"path": path, "reason": f"unsupported type {type(value).__name__}"}]
