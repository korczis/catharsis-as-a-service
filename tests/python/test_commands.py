"""Every registered command is backed by a real test or CI job, and each command actually runs."""

import json
import os
import re
import signal
import subprocess
import time
import tomllib
import urllib.request

import pytest

from conftest import ROOT, require_tool, run, write

REGISTRY = tomllib.loads((ROOT / "data/commands.toml").read_text(encoding="utf-8"))
REPOSITORY = "korczis/catharsis-as-a-service"


def ci_job_names():
    names = set()
    for workflow in (ROOT / ".github/workflows").glob("*.yml"):
        text = workflow.read_text(encoding="utf-8")
        jobs = text.split("\njobs:", 1)[-1]
        names.update(re.findall(r"^    name: (.+)$", jobs, re.M))
    return names


def pytest_function_names():
    names = set()
    for module in (ROOT / "tests/python").glob("test_*.py"):
        names.update(re.findall(r"^def (test_\w+)\(", module.read_text(encoding="utf-8"), re.M))
    return names


def test_registry_entries_name_existing_verifications():
    jobs, tests = ci_job_names(), pytest_function_names()
    problems = []
    for entry in REGISTRY["commands"]:
        assert entry["verified_by"], f"{entry['id']} has no verification"
        for reference in entry["verified_by"]:
            kind, _, name = reference.partition(":")
            if kind == "ci" and name not in jobs:
                problems.append(f"{entry['id']}: CI job '{name}' does not exist (known: {sorted(jobs)})")
            elif kind == "pytest" and name not in tests:
                problems.append(f"{entry['id']}: pytest '{name}' does not exist")
            elif kind not in {"ci", "pytest"}:
                problems.append(f"{entry['id']}: unknown verification kind '{kind}'")
    assert not problems, "\n".join(problems)


def test_registry_sources_exist():
    missing = [entry["source"] for entry in REGISTRY["commands"] if not (ROOT / entry["source"]).exists()]
    assert not missing, missing


def test_registry_groups_are_declared():
    groups = {group["id"] for group in REGISTRY["groups"]}
    undeclared = {entry["group"] for entry in REGISTRY["commands"]} - groups
    assert not undeclared, undeclared


def test_package_scripts_named_by_the_registry_exist():
    scripts = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["scripts"]
    for entry in REGISTRY["commands"]:
        match = re.match(r"npm run ([\w:-]+)", entry["command"])
        if match:
            assert match.group(1) in scripts, f"{entry['command']} has no package.json script"


def test_lint_commits_accepts_and_rejects(tmp_path):
    good = write(tmp_path / "good", "feat(content): add a research note\n")
    bad = write(tmp_path / "bad", "added some stuff\n")
    assert run(["scripts/lint-commits.sh", "--file", str(good)]).returncode == 0
    rejected = run(["scripts/lint-commits.sh", "--file", str(bad)])
    assert rejected.returncode == 1
    assert "not a conventional commit" in rejected.stderr
    history = run(["scripts/lint-commits.sh", "HEAD~1..HEAD"])
    assert history.returncode == 0, history.stderr


def test_release_dry_run_computes_a_version():
    result = run(["scripts/release.sh", "--dry-run"], env={"PAGE_URL": "https://example.test/"}, timeout=120)
    assert result.returncode == 0, result.stderr
    assert re.search(r"release: (v\d+\.\d+\.\d+|none) -> v\d+\.\d+\.\d+ \((major|minor|patch)\)", result.stdout) or (
        "nothing to release" in result.stdout
    ), result.stdout


def test_render_artwork_check_mode():
    result = run(["scripts/render-artwork.sh", "--check"])
    assert result.returncode == 0, result.stdout
    assert "missing" not in result.stdout


def test_majordomus_commands_are_available():
    require_tool("majordomus")
    for subcommand in ("start", "check", "checkpoint", "finish", "watch", "doctor", "history", "handover", "decision"):
        result = run(["majordomus", subcommand, "--help"], timeout=60)
        output = result.stdout + result.stderr
        assert result.returncode == 0, f"majordomus {subcommand} --help exited {result.returncode}: {output}"
        assert "usage" in output.lower(), f"majordomus {subcommand} --help printed no usage"


def test_gh_run_list_reads_the_pipeline():
    require_tool("gh", probe=["gh", "auth", "status"])
    result = run(
        ["gh", "run", "list", "--repo", REPOSITORY, "--workflow", "pages.yml", "--limit", "5", "--json", "status,conclusion"],
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    runs = json.loads(result.stdout)
    assert isinstance(runs, list) and runs, "the Pages workflow has no runs"


@pytest.mark.slow
def test_build_produces_the_site():
    require_tool("zola")
    require_tool("npm")
    result = run(["npm", "run", "build"], timeout=900)
    assert result.returncode == 0, result.stdout + result.stderr
    for relative in ("index.html", "cs/index.html", "research/index.html", "advice/index.html", "commands/index.html", "sitemap.xml"):
        assert (ROOT / "public" / relative).exists(), relative


@pytest.mark.slow
def test_dev_server_serves_the_site():
    require_tool("zola")
    require_tool("npm")
    port = "11711"
    process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", port, "--interface", "127.0.0.1"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    try:
        deadline = time.time() + 180
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5) as response:
                    body = response.read().decode("utf-8")
                    assert response.status == 200
                    assert "Catharsis as a Service" in body
                    return
            except OSError:
                time.sleep(1)
        pytest.fail("zola serve did not answer within 180 seconds")
    finally:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=30)
