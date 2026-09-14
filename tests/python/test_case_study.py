"""The case-study snapshot (data/case_study.json) is exported from local records; CI can only check it.

`export-case-study.py --check` must pass on the committed snapshot without .ai/local, Git, gh or the
network, and must fail on the defects a hand edit or a bad export would introduce.
"""

import json
import shutil
import sys

import pytest

from conftest import ROOT, require_tool, run, write

SCRIPT = str(ROOT / "scripts/export-case-study.py")


def _snapshot():
    return json.loads((ROOT / "data/case_study.json").read_text(encoding="utf-8"))


def _fixture(tmp_path, snapshot, front_matter=None):
    write(tmp_path / "data/case_study.json", json.dumps(snapshot))
    shutil.copy(ROOT / "data/commands.toml", tmp_path / "data/commands.toml")
    if front_matter is not None:
        write(tmp_path / "content/case-study/index.md", front_matter)
    return tmp_path


def _check(root):
    # An empty PATH proves the check needs no majordomus, git or gh.
    return run([sys.executable, SCRIPT, "--check", "--root", str(root)], env={"PATH": ""})


def test_case_study_check_passes_on_repository():
    result = run([sys.executable, SCRIPT, "--check"])
    assert result.returncode == 0, result.stdout
    assert "PASS" in result.stdout


def test_case_study_check_needs_no_local_state_or_tools(tmp_path):
    root = _fixture(tmp_path, _snapshot())
    assert not (root / ".ai").exists()
    result = _check(root)
    assert result.returncode == 0, result.stdout


def test_case_study_snapshot_is_curated():
    snapshot = _snapshot()
    text = json.dumps(snapshot)
    for private in ("/Users/", "/home/", "repository_id", "worktree", "checkpoint_path", "handover_path"):
        assert private not in text
    counts = snapshot["generated_from"]
    for key in ("tasks", "checkpoints", "decisions", "findings", "commits", "pipeline_runs", "releases"):
        assert counts[key] > 0, key
    assert snapshot["milestones"]["first_commit_to_first_release_seconds"] > 0
    completed = [task for task in snapshot["tasks"] if task["outcome"] == "completed"]
    assert completed and all(task["verify"]["exit"] == 0 for task in completed)


def _unknown_kind(s):
    s["events"][0]["kind"] = "rumour"


def _unsorted(s):
    s["events"][0]["ts"], s["events"][-1]["ts"] = s["events"][-1]["ts"], s["events"][0]["ts"]


def _dangling_evidence(s):
    s["findings"][0]["evidence"] = ["event-that-never-happened"]


def _count_mismatch(s):
    s["generated_from"]["commits"] += 1


def _local_path(s):
    s["events"][0]["detail_en"] = "written in /Users/someone/checkout"


def _completed_without_verification(s):
    task = next(task for task in s["tasks"] if task["outcome"] == "completed")
    task["verify"] = None


def _bad_timestamp(s):
    s["commits"][0]["ts"] = "yesterday"


def _duplicate_id(s):
    s["events"][1]["id"] = s["events"][0]["id"]


def _insecure_link(s):
    s["events"][0]["links"] = [{"label": "record", "url": "http://example.test/"}]


def _missing_section(s):
    del s["pipelines"]


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (_unknown_kind, "kind must be one of"),
        (_unsorted, "not sorted by time"),
        (_dangling_evidence, "is not an event"),
        (_count_mismatch, "generated_from.commits"),
        (_local_path, "local path"),
        (_completed_without_verification, "completed task needs a verification command"),
        (_bad_timestamp, "timestamp must be"),
        (_duplicate_id, "duplicate event id"),
        (_insecure_link, "https url"),
        (_missing_section, "'pipelines' must be a list"),
    ],
)
def test_case_study_check_rejects_malformed_snapshot(tmp_path, mutate, message):
    snapshot = _snapshot()
    mutate(snapshot)
    result = _check(_fixture(tmp_path, snapshot))
    assert result.returncode == 1, result.stdout
    assert message in result.stdout, result.stdout


def test_case_study_check_rejects_invalid_json(tmp_path):
    write(tmp_path / "data/case_study.json", "{ not json")
    result = _check(tmp_path)
    assert result.returncode == 1
    assert "cannot read" in result.stdout


def test_case_study_check_rejects_front_matter_pointing_nowhere(tmp_path):
    front_matter = (
        '+++\ntitle = "Case study"\n[extra]\nlifecycle = [\n'
        '  { id = "start", name = "Start", command_id = "majordomus-launch", what = "", why = "", example_event = "no-such-event" },\n'
        "]\n+++\n"
    )
    result = _check(_fixture(tmp_path, _snapshot(), front_matter))
    assert result.returncode == 1
    assert "unregistered command 'majordomus-launch'" in result.stdout
    assert "unknown event 'no-such-event'" in result.stdout


def test_case_study_export_is_deterministic(tmp_path):
    if not (ROOT / ".ai/local/state/ledger.jsonl").exists():
        pytest.skip("the export reads this checkout's Majordomus state, which CI does not have")
    require_tool("git")
    first, second = tmp_path / "first.json", tmp_path / "second.json"
    for out in (first, second):
        result = run([sys.executable, SCRIPT, "--offline", "--out", str(out)])
        assert result.returncode == 0, result.stdout
    assert first.read_bytes() == second.read_bytes()


def test_majordomus_read_only_commands_used_by_the_case_study():
    require_tool("majordomus")
    rules = run(["majordomus", "rules", "list"], timeout=120)
    assert rules.returncode == 0, rules.stdout + rules.stderr
    assert "project.verified-deployment" in rules.stdout
    adrs = run(["majordomus", "adr", "list"], timeout=120)
    assert adrs.returncode == 0, adrs.stdout + adrs.stderr
    assert "adr-0001" in adrs.stdout
