from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from workflow import update


ROOT = Path(__file__).resolve().parents[1]


def load_tasks():
    return json.loads((ROOT / "workflow/tasks.json").read_text(encoding="utf-8"))


def test_checked_in_ledger_is_valid():
    assert update.validate(load_tasks()) == []


def test_generated_views_are_current():
    expected = update.render(load_tasks())
    for name, content in expected.items():
        assert (ROOT / name).read_text(encoding="utf-8") == content


def test_first_unsatisfied_required_gate_drives_stage():
    task = deepcopy(load_tasks()["tasks"]["HARNESS-WORKFLOW-001"])
    task["gates"]["publication"] = {
        "status": "unpublished", "evidence": [], "note": "unpublished"
    }
    assert update.overall(task) == "publication"
    task["gates"]["technical"] = {"status": "pending", "evidence": [], "note": "pending"}
    assert update.overall(task) == "technical validation"
    task["gates"]["technical"] = {"status": "passed", "evidence": ["receipt"], "note": "pass"}
    assert update.overall(task) == "publication"
    task["gates"]["publication"] = {"status": "published", "evidence": ["remote"], "note": "published"}
    assert update.overall(task) == "complete"


def test_blocking_gate_dominates_later_progress():
    task = deepcopy(load_tasks()["tasks"]["HARNESS-KEYFRAMES-001"])
    task["required_gates"] = list(update.GATES)  # the sample task itself does not require a visual gate
    task["gates"]["visual"]["status"] = "rejected"
    assert update.overall(task) == "blocked"


def test_dependency_cycle_is_rejected():
    data = load_tasks()
    data["tasks"]["HARNESS-WORKFLOW-001"]["depends_on"] = ["HARNESS-KEYFRAMES-001"]
    data["tasks"]["HARNESS-KEYFRAMES-001"]["depends_on"] = ["HARNESS-WORKFLOW-001"]
    assert any("dependency cycle" in error for error in update.validate(data))
