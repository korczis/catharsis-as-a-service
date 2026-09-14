#!/usr/bin/env python3
"""Curated, deterministic snapshot of how this repository was delivered: data/case_study.json.

Export (local only; needs the checkout's Majordomus state, Git and an authenticated gh):
  - the Majordomus ledger (`majordomus history --all --json`, falling back to
    .ai/local/state/ledger.jsonl), task titles, decisions, handovers and checkpoints
  - the Git history, GitHub releases and runs of the Pages workflow with their jobs

Only curated, sanitized facts leave .ai/local: no absolute local paths, no raw checkpoint bodies,
no prompts. Findings are declared in this file and are published only when the records confirm
them. The output has sorted keys and no generation timestamp, so the same records give the same
bytes. See docs/CASE-STUDY.md.

--check validates an existing snapshot against the schema (and the case-study front matter
against the snapshot and the command registry). It needs neither .ai/local nor the network.

usage: export-case-study.py [--check] [--offline] [--root <repo>] [--out <file>]
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

REPOSITORY = "korczis/catharsis-as-a-service"
REPO_URL = f"https://github.com/{REPOSITORY}"
SITE_URL = "https://korczis.github.io/catharsis-as-a-service/"
BLOB = f"{REPO_URL}/blob/main/"
SNAPSHOT = Path("data/case_study.json")
SCHEMA = "case-study/v1"

KINDS = ("task", "checkpoint", "finish", "decision", "handover", "finding", "commit", "pipeline", "release")
OUTCOMES = {"completed", "partial", "blocked", "no_match", "failed", "active"}
CONTRACT_RESULTS = {"pass", "skipped", "fail", "warn"}
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
EVENT_ID = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
TASK_ID = re.compile(r"^t-\d{14}-[0-9a-f]{4}$")
SHA = re.compile(r"^[0-9a-f]{40}$")
# Anything that looks like a path on the machine that produced the records.
LOCAL_PATH = re.compile(r"(?:/Users/|/home/|/private/|/var/folders/|/tmp/|[A-Za-z]:\\\\)")
PRIVATE_KEYS = {"repository_id", "worktree", "checkpoint_path", "handover_path", "policy_sha256"}
REPO_TOKEN = re.compile(r"[\w./-]+\.(?:py|js|html|xml|yml|yaml|toml|md|sh|json)|\.github/[\w./-]+")


# ── helpers ───────────────────────────────────────────────────────────────────────────────────


def utc(value):
    """Any ISO 8601 timestamp to YYYY-MM-DDTHH:MM:SSZ."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def seconds_between(start, end):
    return int((datetime.fromisoformat(end.replace("Z", "+00:00")) - datetime.fromisoformat(start.replace("Z", "+00:00"))).total_seconds())


def duration_en(seconds):
    minutes, rest = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    parts = ([f"{hours} h"] if hours else []) + ([f"{minutes} min"] if minutes else []) + [f"{rest} s"]
    return " ".join(parts)


def sanitize(text):
    text = re.sub(r"(?:/Users|/home|/private|/var/folders|/tmp)/\S*", "<local path>", text or "")
    return re.sub(r"\s+", " ", text).strip()


def short(sha):
    return sha[:7]


def commit_link(sha):
    return {"label": f"commit {short(sha)}", "url": f"{REPO_URL}/commit/{sha}"}


def run_link(run_id, label=None):
    return {"label": label or f"run {run_id}", "url": f"{REPO_URL}/actions/runs/{run_id}"}


def file_link(root, token):
    token = token.strip("'\"`,.;:")
    if token and (root / token).is_file():
        return {"label": token, "url": BLOB + token}
    return None


def command(args, root):
    if not shutil.which(args[0]):
        return None
    result = subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=300)
    return result.stdout if result.returncode == 0 else None


def front_matter(path):
    """YAML-like front matter between --- lines: flat `key: value` pairs only."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n?(.*)\Z", text, re.S)
    if not match:
        return {}, text
    fields = {}
    for line in match.group(1).splitlines():
        pair = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if pair:
            fields[pair.group(1)] = pair.group(2).strip().strip('"')
    return fields, match.group(2)


def sections(body):
    found = {}
    for block in re.split(r"^# ", body, flags=re.M)[1:]:
        heading, _, text = block.partition("\n")
        found[heading.strip()] = sanitize(text)
    return found


# ── sources ───────────────────────────────────────────────────────────────────────────────────


def load_ledger(root):
    output = command(["majordomus", "history", "--all", "--json"], root)
    if output is None:
        path = root / ".ai/local/state/ledger.jsonl"
        if not path.exists():
            raise SystemExit("export needs the Majordomus ledger (.ai/local/state) of this checkout; use --check in CI")
        output = path.read_text(encoding="utf-8")
    return [json.loads(line) for line in output.splitlines() if line.strip()]


def load_task_titles(root):
    titles = {}
    state = root / ".ai/local/state"
    for path in [*sorted((state / "archive").glob("*.yaml")), state / "current.yaml"]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        ident = re.search(r"^id:\s*(\S+)", text, re.M)
        task = re.search(r'^task:\s*"?(.*?)"?\s*$', text, re.M)
        if ident and task:
            titles[ident.group(1)] = sanitize(task.group(1))
    return titles


def load_decisions(root):
    path = root / ".ai/local/state/decisions.md"
    if not path.exists():
        return []
    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    decisions = []
    for match in re.finditer(r"^## (\d{4}-\d{2}-\d{2}) — (.+?)\n(.*?)(?=^## |\Z)", text, re.S | re.M):
        fields = dict(re.findall(r"^([A-Z][a-z]+):\s*(.+)$", match.group(3), re.M))
        decisions.append({"title": sanitize(match.group(2)), **{key.lower(): sanitize(value) for key, value in fields.items()}})
    return decisions


def load_records(root, folder):
    records = []
    for path in sorted((root / ".ai/local/state" / folder).glob("*.md")):
        fields, body = front_matter(path)
        if "created_at" in fields:
            records.append({"ts": utc(fields["created_at"]), "task_id": fields.get("task_id", ""), "head": fields.get("head", ""),
                            "sections": sections(body), "body": body})
    return records


def load_policy_targets(root):
    path = root / ".ai/repo/policy.yaml"
    return re.findall(r"^\s+target:\s*(\S+)", path.read_text(encoding="utf-8"), re.M) if path.exists() else []


def load_commits(root):
    output = command(["git", "log", "--reverse", "--format=%H|%cI|%s"], root) or ""
    commits = []
    for line in output.splitlines():
        sha, ts, subject = line.split("|", 2)
        commits.append({"sha": sha, "ts": utc(ts), "subject": subject, "url": f"{REPO_URL}/commit/{sha}"})
    return commits


def load_github(root, previous, offline):
    if offline:
        return previous.get("pipelines", []), previous.get("releases", [])
    raw_releases = command(["gh", "release", "list", "--repo", REPOSITORY, "-L", "100", "--json", "tagName,publishedAt"], root)
    raw_runs = command(["gh", "run", "list", "--repo", REPOSITORY, "-w", "pages.yml", "-L", "50", "--json",
                        "databaseId,headSha,conclusion,createdAt,updatedAt,status,displayTitle"], root)
    if raw_releases is None or raw_runs is None:
        raise SystemExit("export needs an authenticated gh; use --offline to keep the snapshot's GitHub records")
    releases = sorted(({"tag": r["tagName"], "published": utc(r["publishedAt"]),
                        "url": f"{REPO_URL}/releases/tag/{r['tagName']}"} for r in json.loads(raw_releases) if r["publishedAt"]),
                      key=lambda r: r["published"])
    pipelines = []
    for run in json.loads(raw_runs):
        if run["status"] != "completed":
            continue
        view = command(["gh", "run", "view", str(run["databaseId"]), "--repo", REPOSITORY, "--json", "jobs"], root)
        jobs = []
        for job in json.loads(view or '{"jobs": []}')["jobs"]:
            started, completed = utc(job["startedAt"]), utc(job["completedAt"])
            jobs.append({"name": job["name"], "conclusion": job["conclusion"] or "unknown", "started": started,
                         "completed": completed, "seconds": max(0, seconds_between(started, completed))})
        created, updated = utc(run["createdAt"]), utc(run["updatedAt"])
        pipelines.append({"id": run["databaseId"], "sha": run["headSha"], "title": run["displayTitle"],
                          "conclusion": run["conclusion"], "created": created, "updated": updated,
                          "seconds": seconds_between(created, updated), "url": f"{REPO_URL}/actions/runs/{run['databaseId']}",
                          "jobs": sorted(jobs, key=lambda j: j["name"])})
    return sorted(pipelines, key=lambda p: p["created"]), releases


# ── snapshot ──────────────────────────────────────────────────────────────────────────────────


def contract_summary(contract):
    counts = {}
    for result in contract.values():
        counts[result] = counts.get(result, 0) + 1
    return ", ".join(f"{counts[key]} {key}" for key in sorted(counts))


def build(root, offline):
    previous = json.loads((root / SNAPSHOT).read_text(encoding="utf-8")) if (root / SNAPSHOT).exists() else {}
    ledger = load_ledger(root)
    titles = load_task_titles(root)
    decisions = load_decisions(root)
    handovers = load_records(root, "handovers")
    checkpoints = load_records(root, "checkpoints")
    commits = load_commits(root)
    pipelines, releases = load_github(root, previous, offline)
    targets = load_policy_targets(root)

    events, tasks = [], {}
    version = next((e["by"].split("/", 1)[1] for e in ledger if e.get("by", "").startswith("majordomus/")), "unknown")
    decision_index = 0

    def add(order, **event):
        event.setdefault("links", [])
        events.append({"_order": order, **event})

    for order, entry in enumerate(ledger):
        ts, kind, head = utc(entry["ts"]), entry["event"], entry.get("head", "")
        head_links = [commit_link(head)] if SHA.match(head or "") else []
        task_id = entry.get("task_id", "")
        title = titles.get(task_id, task_id)
        if kind == "projections.updated":
            add(order, id="majordomus-init", ts=ts, kind="task",
                title_en="Majordomus layer initialised; provider instruction files generated",
                title_cs="Inicializována vrstva Majordomus; vygenerovány instrukční soubory pro poskytovatele",
                detail_en=f"The policy was projected into {entry.get('targets', len(targets))} instruction files ({', '.join(targets)}) that point every agent at .ai/README.md.",
                detail_cs=f"Politika se promítla do {entry.get('targets', len(targets))} instrukčních souborů ({', '.join(targets)}), které každého agenta odkazují na .ai/README.md.",
                links=[*head_links, {"label": ".ai/repo/policy.yaml", "url": BLOB + ".ai/repo/policy.yaml"}])
        elif kind == "task.started":
            scope = entry.get("scope", "").split()
            tasks[task_id] = {"id": task_id, "title_en": title, "started": ts, "finished": None, "outcome": "active",
                              "profile": entry.get("profile", ""), "scope_paths_count": len(scope), "checkpoints": 0,
                              "handovers": 0, "decisions": 0, "verify": None, "contract": {}, "duration_seconds": None}
            literal = f' declared as "{scope[0]}"' if len(scope) == 1 else ""
            add(order, id=f"{task_id}-start", ts=ts, kind="task", task=task_id,
                title_en=f"Task started: {title}", title_cs=f"Start úlohy: {title}",
                detail_en=f"Profile {entry.get('profile')}; scope of {len(scope)} path{'s' if len(scope) != 1 else ''}{literal}.",
                detail_cs=f"Profil {entry.get('profile')}; rozsah {len(scope)} {'cesta' if len(scope) == 1 else 'cest'}{literal.replace('declared as', 'zadaný jako')}.",
                links=head_links)
        elif kind == "task.checkpoint":
            # The note file is named when it is written; the ledger line can follow a second later.
            record = next((c for c in checkpoints if c["task_id"] == task_id and abs(seconds_between(c["ts"], ts)) <= 5), None)
            if task_id in tasks:
                tasks[task_id]["checkpoints"] += 1
            if record and "Derived, not authored" in record["body"]:
                changed = re.search(r"(\d+) file\(s\) changed", record["body"])
                number = changed.group(1) if changed else "?"
                detail_en = f"Derived from Git, not authored: {number} files changed since the task started."
                detail_cs = f"Odvozeno z Gitu, ne napsáno: od začátku úlohy se změnilo {number} souborů."
            elif record:
                detail_en = "Authored progress note (at most 40 lines by policy); the body stays in the checkout's local state."
                detail_cs = "Ručně psaná poznámka o průběhu (podle politiky nejvýš 40 řádků); text zůstává v lokálním stavu checkoutu."
            else:
                detail_en = "Checkpoint of the task recorded in the ledger; no note file is retained for it."
                detail_cs = "Checkpoint úlohy zaznamenaný v ledgeru; soubor s poznámkou k němu uchován není."
            ident = f"checkpoint-{ts.replace('-', '').replace(':', '').lower()}"
            if record:
                record["event_id"] = ident
            add(order, id=ident, ts=ts, kind="checkpoint", task=task_id,
                title_en=f"Checkpoint: {title}", title_cs=f"Checkpoint: {title}", detail_en=detail_en, detail_cs=detail_cs,
                links=[commit_link(record["head"])] if record and SHA.match(record["head"]) else head_links)
        elif kind == "task.handed_over":
            record = next((h for h in handovers if h["task_id"] == task_id and abs(seconds_between(h["ts"], ts)) <= 5), None)
            if task_id in tasks:
                tasks[task_id]["handovers"] += 1
            state = record["sections"] if record else {}
            ident = f"handover-{ts.replace('-', '').replace(':', '').lower()}"
            if record:
                record["event_id"] = ident
            add(order, id=ident, ts=ts, kind="handover", task=task_id,
                title_en="Handover written: current state and next action",
                title_cs="Zapsán handover: aktuální stav a další krok",
                detail_en=" ".join(filter(None, [f"Current state: {state['Current State']}" if state.get("Current State") else "",
                                                 f"Next action: {state['Next Action']}" if state.get("Next Action") else ""])),
                links=[commit_link(record["head"])] if record and SHA.match(record["head"]) else head_links)
        elif kind == "task.finished":
            verify = entry.get("verify")
            contract = entry.get("contract") or {}
            if task_id in tasks:
                tasks[task_id].update(finished=ts, outcome=entry["outcome"], contract=dict(sorted(contract.items())),
                                      verify={"command": sanitize(verify["command"]), "exit": verify["exit"], "seconds": verify["seconds"]} if verify else None,
                                      checkpoints=entry.get("checkpoints", tasks[task_id]["checkpoints"]),
                                      duration_seconds=seconds_between(tasks[task_id]["started"], ts))
            if verify:
                check_en = f"verification command {sanitize(verify['command'])} exited {verify['exit']} in {verify['seconds']} s"
                check_cs = f"ověřovací příkaz {sanitize(verify['command'])} skončil kódem {verify['exit']} za {verify['seconds']} s"
            else:
                check_en, check_cs = "no verification command recorded", "bez zaznamenaného ověřovacího příkazu"
            links = list(head_links)
            if verify and SITE_URL.rstrip("/") in verify["command"]:
                links.append({"label": "live site", "url": SITE_URL})
            add(order, id=f"{task_id}-finish", ts=ts, kind="finish", task=task_id,
                title_en=f"Task finished as {entry['outcome']}: {title}", title_cs=f"Úloha ukončena jako {entry['outcome']}: {title}",
                detail_en=f"Finish contract: {contract_summary(contract)}; {check_en}.",
                detail_cs=f"Smlouva o dokončení: {contract_summary(contract)}; {check_cs}.", links=links)
        elif kind == "decision.recorded":
            decision_index += 1
            text = sanitize(entry.get("decision", ""))
            record = next((d for d in decisions if d["title"] == text), {})
            if task_id in tasks:
                tasks[task_id]["decisions"] += 1
            links = [link for link in (file_link(root, token) for token in REPO_TOKEN.findall(record.get("evidence", ""))) if link]
            add(order, id=f"decision-{decision_index}", ts=ts, kind="decision", task=task_id, title_en=text,
                detail_en=" ".join(filter(None, [f"Why: {record['why']}." if record.get("why") else "",
                                                 f"Rejected: {record['rejected']}." if record.get("rejected") else "",
                                                 f"Evidence: {record['evidence']}." if record.get("evidence") else ""])),
                links=[*head_links, *links])
        elif kind == "adr.proposed":
            ident = entry.get("adr", "adr")
            files = sorted((root / ".ai/repo/adrs").glob(f"{ident.split('-')[-1]}-*.md"))
            add(order, id=f"{ident}-proposed", ts=ts, kind="decision",
                title_en=f"{ident.upper()} proposed: {entry.get('title', '')}", title_cs=f"{ident.upper()} navrženo: {entry.get('title', '')}",
                detail_en="Recorded as proposed. Accepting an architecture decision is left to a person.",
                detail_cs="Zaznamenáno jako návrh. Přijetí architektonického rozhodnutí je ponecháno na člověku.",
                links=[{"label": files[0].relative_to(root).as_posix(), "url": BLOB + files[0].relative_to(root).as_posix()}] if files else [])

    runs_by_sha = {}
    for pipeline in pipelines:
        runs_by_sha.setdefault(pipeline["sha"], []).append(pipeline)

    for commit in commits:
        runs = runs_by_sha.get(commit["sha"], [])
        add(10_000, id=f"commit-{short(commit['sha'])}", ts=commit["ts"], kind="commit", title_en=commit["subject"],
            detail_en=(f"Pages pipeline: {', '.join(f'run {r['id']} {r['conclusion']}' for r in runs)}." if runs
                       else "No Pages pipeline run for this commit (it predates the workflow)."),
            detail_cs=(f"Pipeline Pages: {', '.join(f'běh {r['id']} {r['conclusion']}' for r in runs)}." if runs
                       else "Pro tento commit neběžela pipeline Pages (workflow ještě neexistoval)."),
            links=[commit_link(commit["sha"]), *(run_link(r["id"]) for r in runs)])

    for index, pipeline in enumerate(pipelines):
        failed = [job["name"] for job in pipeline["jobs"] if job["conclusion"] == "failure"]
        skipped = [job["name"] for job in pipeline["jobs"] if job["conclusion"] == "skipped"]
        passed = sum(1 for job in pipeline["jobs"] if job["conclusion"] == "success")
        links = [run_link(pipeline["id"]), commit_link(pipeline["sha"])]
        detail_en = f"{len(pipeline['jobs'])} jobs in {duration_en(pipeline['seconds'])}: {passed} passed"
        detail_cs = f"{len(pipeline['jobs'])} jobů za {duration_en(pipeline['seconds'])}: {passed} prošlo"
        if failed:
            detail_en += f", failed: {', '.join(failed)}"
            detail_cs += f", selhalo: {', '.join(failed)}"
        if skipped:
            detail_en += f", skipped: {', '.join(skipped)}"
            detail_cs += f", přeskočeno: {', '.join(skipped)}"
        detail_en += "."
        detail_cs += "."
        if pipeline["conclusion"] != "success":
            later = next((p for p in pipelines[index + 1:] if p["conclusion"] == "success"), None)
            if later:
                links.append(run_link(later["id"], f"next green run {later['id']}"))
                detail_en += f" The next green run was {later['id']} for commit {short(later['sha'])}."
                detail_cs += f" Další zelený běh byl {later['id']} pro commit {short(later['sha'])}."
            else:
                detail_en += " No later run is in this snapshot."
                detail_cs += " V tomto snímku není žádný pozdější běh."
        verb_en = {"success": "passed", "failure": "failed"}.get(pipeline["conclusion"], pipeline["conclusion"])
        verb_cs = {"success": "prošla", "failure": "selhala"}.get(pipeline["conclusion"], pipeline["conclusion"])
        add(20_000, id=f"pipeline-{pipeline['id']}", ts=pipeline["created"], kind="pipeline",
            title_en=f"Pages pipeline {verb_en}: {pipeline['title']}",
            title_cs=f"Pipeline Pages {verb_cs}: {pipeline['title']}", detail_en=detail_en, detail_cs=detail_cs, links=links)

    for release in releases:
        run = next((p for p in pipelines for job in p["jobs"] if job["name"] == "Release" and job["conclusion"] == "success"
                    and job["started"] <= release["published"] <= job["completed"]), None)
        release["run"] = run["id"] if run else None
        release["sha"] = run["sha"] if run else None
        add(30_000, id=f"release-{release['tag'].replace('.', '-')}", ts=release["published"], kind="release",
            title_en=f"Release {release['tag']} published", title_cs=f"Publikováno vydání {release['tag']}",
            detail_en=(f"Cut by the Release job of run {run['id']} after Deploy and Verify production passed for commit {short(run['sha'])}."
                       if run else "Published release."),
            detail_cs=(f"Vytvořeno jobem Release v běhu {run['id']} poté, co pro commit {short(run['sha'])} prošly Deploy a Verify production."
                       if run else "Publikované vydání."),
            links=[{"label": release["tag"], "url": release["url"]}, *([run_link(run["id"]), commit_link(run["sha"])] if run else [])])

    sources = {"events": events, "tasks": tasks, "handovers": handovers, "checkpoints": checkpoints, "pipelines": pipelines,
               "commits": commits, "releases": releases}
    findings = [finding for finding in (rule(sources) for rule in FINDINGS) if finding]
    for finding in findings:
        add(40_000, id=f"finding-{finding['id']}", ts=finding["ts"], kind="finding", title_en=finding["title_en"],
            title_cs=finding["title_cs"], detail_en=finding["detail_en"], detail_cs=finding["detail_cs"], links=finding["links"])

    events.sort(key=lambda e: (e["ts"], e["_order"], e["id"]))
    for event in events:
        del event["_order"]

    first_commit = commits[0]["ts"] if commits else None
    first_release = releases[0]["published"] if releases else None
    init = next((e["ts"] for e in events if e["id"] == "majordomus-init"), None)
    milestones = {
        "first_commit": first_commit,
        "majordomus_initialised": init,
        "first_verified_release": first_release,
        "first_commit_to_first_release_seconds": seconds_between(first_commit, first_release) if first_commit and first_release else None,
        "majordomus_to_first_release_seconds": seconds_between(init, first_release) if init and first_release else None,
    }
    task_list = sorted(tasks.values(), key=lambda t: t["started"])
    return {
        "schema": SCHEMA,
        "repository": REPO_URL,
        "site": SITE_URL,
        "majordomus_version": version,
        "generated_from": {
            "ledger_events": len(ledger),
            "tasks": len(task_list),
            "checkpoints": sum(1 for e in ledger if e["event"] == "task.checkpoint"),
            "handovers": sum(1 for e in ledger if e["event"] == "task.handed_over"),
            "decisions": sum(1 for e in ledger if e["event"] == "decision.recorded"),
            "adrs_proposed": sum(1 for e in ledger if e["event"] == "adr.proposed"),
            "findings": len(findings),
            "commits": len(commits),
            "pipeline_runs": len(pipelines),
            "releases": len(releases),
            "events": len(events),
            "through": events[-1]["ts"] if events else None,
        },
        "milestones": milestones,
        "tasks": task_list,
        "events": events,
        "findings": findings,
        "commits": commits,
        "pipelines": pipelines,
        "releases": releases,
    }


# ── findings: declared here, published only when the records confirm them ─────────────────────


def _event(sources, predicate):
    return next((e for e in sources["events"] if predicate(e)), None)


def _finding(ident, ts, caught_by, evidence, links, title_en, title_cs, detail_en, detail_cs):
    return {"id": ident, "ts": ts, "caught_by": caught_by, "evidence": [e for e in evidence if e], "links": links,
            "title_en": title_en, "title_cs": title_cs, "detail_en": detail_en, "detail_cs": detail_cs}


def _next_start(sources, after):
    return _event(sources, lambda e: e["kind"] == "task" and e["id"].endswith("-start") and e["ts"] >= after)


def _first_push(sources):
    return sources["pipelines"][0]["created"] if sources["pipelines"] else "9999"


def finding_scope_drift(sources):
    handover = next((h for h in sources["handovers"] if "scope drift" in h["sections"].get("Current State", "")), None)
    if not handover:
        return None
    task = sources["tasks"].get(handover["task_id"])
    start = _next_start(sources, handover["ts"])
    handover_id = handover.get("event_id")
    stage_en = "before the first push" if handover["ts"] < _first_push(sources) else "during the work"
    stage_cs = "před prvním pushem" if handover["ts"] < _first_push(sources) else "během práce"
    return _finding(
        "scope-drift", handover["ts"], "majordomus-watch", [handover_id, f"{handover['task_id']}-finish", start and start["id"]],
        [{"label": "task lifecycle", "url": BLOB + ".ai/repo/workflows/task-lifecycle.md"}],
        "Scope drift after files were moved; task restarted",
        "Odchylka od rozsahu po přesunu souborů; úloha restartována",
        f"The first task claimed {task['scope_paths_count'] if task else '?'} paths but not the root files that were moved into artwork/ and static/. "
        f"The handover records that majordomus watch reported the drift; the task was finished as partial and restarted {stage_en}.",
        f"První úloha si nárokovala {task['scope_paths_count'] if task else '?'} cest, ale ne kořenové soubory přesunuté do artwork/ a static/. "
        f"Handover zaznamenává, že majordomus watch nahlásil odchylku; úloha byla ukončena jako partial a restartována {stage_cs}.",
    )


def finding_malformed_scope(sources):
    handover = next((h for h in sources["handovers"] if "not interpreted as the whole repository" in h["sections"].get("Current State", "")), None)
    task = sources["tasks"].get(handover["task_id"]) if handover else None
    if not handover or not task or task["scope_paths_count"] != 1:
        return None
    start = _next_start(sources, handover["ts"])
    return _finding(
        "malformed-scope", handover["ts"], "majordomus-check",
        [f"{task['id']}-start", handover.get("event_id"), f"{task['id']}-finish", start and start["id"]],
        [{"label": "scope-integrity rule", "url": BLOB + ".ai/repo/rules/vendor/majordomus/rules/scope-integrity.v1.md"}],
        "A scope of \".\" was caught before the first push",
        "Rozsah \".\" zachycen před prvním pushem",
        "The restarted task declared its scope as \".\", which Majordomus does not read as the whole repository, so majordomus check "
        "reported every changed file as out of scope. The task was restarted with explicit top-level paths"
        + (" before the first push." if handover["ts"] < _first_push(sources) else "."),
        "Restartovaná úloha zadala rozsah jako \".\", což Majordomus nečte jako celý repozitář, a majordomus check proto nahlásil "
        "každý změněný soubor jako mimo rozsah. Úloha byla restartována s výslovně vyjmenovanými cestami"
        + (" ještě před prvním pushem." if handover["ts"] < _first_push(sources) else "."),
    )


def finding_scope_outgrown(sources):
    handover = next((h for h in sources["handovers"] if "outside this task scope" in h["sections"].get("Current State", "")), None)
    if not handover:
        return None
    start = _next_start(sources, handover["ts"])
    new_task = sources["tasks"].get(start["task"]) if start and start.get("task") else None
    return _finding(
        "scope-outgrown", handover["ts"], None,
        [handover.get("event_id"), f"{handover['task_id']}-finish", start and start["id"]],
        [],
        "The brief outgrew the claimed scope; a new task claimed it",
        "Zadání přerostlo nárokovaný rozsah; nová úloha si ho nárokovala",
        "When the brief grew to a Rust workspace, data files and Python tooling, the handover recorded that the new top-level paths fell "
        f"outside the task's scope. The task was finished as partial and a new one claimed {new_task['scope_paths_count'] if new_task else '?'} paths.",
        "Když se zadání rozrostlo o workspace v Rustu, datové soubory a nástroje pro Python, handover zaznamenal, že nové cesty nejvyšší úrovně "
        f"leží mimo rozsah úlohy. Úloha skončila jako partial a nová si nárokovala {new_task['scope_paths_count'] if new_task else '?'} cest.",
    )


def finding_live_verified_completion(sources):
    completed = [t for t in sources["tasks"].values() if t["outcome"] == "completed"]
    if not completed or not all(t["verify"] and t["verify"]["exit"] == 0 and "smoke-production" in t["verify"]["command"] for t in completed):
        return None
    partial = [t for t in sources["tasks"].values() if t["outcome"] == "partial"]
    seconds = sorted({t["verify"]["seconds"] for t in completed})
    return _finding(
        "live-verified-completion", completed[0]["finished"], "majordomus-finish", [f"{t['id']}-finish" for t in completed],
        [{"label": "verification-integrity rule", "url": BLOB + ".ai/repo/rules/vendor/majordomus/rules/verification-integrity.v1.md"},
         {"label": "scripts/smoke-production.sh", "url": BLOB + "scripts/smoke-production.sh"}],
        "\"Completed\" was recorded only with a passing check of the live site",
        "„Dokončeno“ se zaznamenalo jen s úspěšnou kontrolou živého webu",
        f"{'Both' if len(completed) == 2 else f'All {len(completed)}'} tasks closed as completed ran the production smoke test against the live URL "
        f"as their verification command (exit 0, {' and '.join(f'{s} s' for s in seconds)}). The {len(partial)} tasks closed as partial recorded "
        "no verification command and claimed no completion.",
        f"{'Obě' if len(completed) == 2 else f'Všech {len(completed)}'} úlohy uzavřené jako dokončené spustily jako ověřovací příkaz smoke test "
        f"proti živé URL (exit 0, {' a '.join(f'{s} s' for s in seconds)}). Úlohy uzavřené jako partial ({len(partial)}) žádný ověřovací příkaz "
        "nezaznamenaly a dokončení netvrdily.",
    )


def finding_ruleset_bypass(sources):
    record = next((c for c in sources["checkpoints"] if "bypass recorded" in c["body"]), None)
    if not record:
        return None
    return _finding(
        "ruleset-bypass", record["ts"], None, [record.get("event_id")],
        [{"label": ".github/workflows/pages.yml", "url": BLOB + ".github/workflows/pages.yml"}],
        "The first push to main went through the ruleset's admin bypass",
        "První push do main prošel přes výjimku pravidel pro administrátora",
        "The checkpoint written after the first push records that the push used the admin bypass of the repository ruleset that requires CI. "
        "Deployment was still gated: in the Pages workflow the deploy job needs the CI jobs, and the release job needs production verification.",
        "Checkpoint zapsaný po prvním pushi zaznamenává, že push využil výjimku pro administrátora v pravidlech repozitáře, která vyžadují CI. "
        "Nasazení přesto zůstalo podmíněné: ve workflow Pages job deploy závisí na jobech CI a job release na ověření produkce.",
    )


def finding_adr_left_to_person(sources):
    adr = _event(sources, lambda e: e["id"].endswith("-proposed"))
    handover = next((h for h in sources["handovers"] if "awaits a person" in h["sections"].get("Current State", "")), None)
    if not adr or not handover:
        return None
    return _finding(
        "adr-left-to-person", adr["ts"], None, [adr["id"], handover.get("event_id")],
        adr["links"],
        "ADR-0001 stayed proposed; acceptance was left to a person",
        "ADR-0001 zůstalo návrhem; přijetí zůstalo na člověku",
        "The agent recorded the evidence-ledger decision as a proposed ADR and did not accept it. The final handover lists accepting or amending it as the next action for a person.",
        "Agent zaznamenal rozhodnutí o ledgeru důkazů jako navržené ADR a sám ho nepřijal. Poslední handover uvádí jeho přijetí nebo úpravu jako další krok pro člověka.",
    )


def _failed_pipeline_finding(sources, job_name, ident, title_en, title_cs):
    pipelines = sources["pipelines"]
    for index, pipeline in enumerate(pipelines):
        if not any(j["name"].endswith(job_name) and j["conclusion"] == "failure" for j in pipeline["jobs"]):
            continue
        skipped = [j["name"] for j in pipeline["jobs"] if j["conclusion"] == "skipped"]
        later = next((p for p in pipelines[index + 1:] if p["conclusion"] == "success"), None)
        fix = next((c for c in sources["commits"] if later and c["sha"] == later["sha"]), None)
        release = next((r for r in sources["releases"] if later and r.get("run") == later["id"]), None)
        evidence = [f"pipeline-{pipeline['id']}", fix and f"commit-{short(fix['sha'])}", later and f"pipeline-{later['id']}",
                    release and f"release-{release['tag'].replace('.', '-')}"]
        links = [run_link(pipeline["id"], f"failed run {pipeline['id']}")]
        if later:
            links += [commit_link(later["sha"]), run_link(later["id"], f"green run {later['id']}")]
            subject = f" ({fix['subject']})" if fix else ""
            outcome_en = (f" The next green run was {later['id']} for commit {short(later['sha'])}{subject}"
                          + (f", which published {release['tag']}." if release else "."))
            outcome_cs = (f" Další zelený běh byl {later['id']} pro commit {short(later['sha'])}{subject}"
                          + (f", který publikoval {release['tag']}." if release else "."))
        else:
            outcome_en = " No later run is in this snapshot, so no release exists for this commit yet."
            outcome_cs = " V tomto snímku není žádný pozdější běh, takže pro tento commit zatím žádné vydání neexistuje."
        return _finding(
            ident, pipeline["created"], f"ci:{job_name}", evidence, links, title_en, title_cs,
            f"Run {pipeline['id']} failed in {job_name}; {', '.join(skipped) or 'no job'} {'was' if len(skipped) == 1 else 'were'} skipped.{outcome_en}",
            f"Běh {pipeline['id']} selhal v jobu {job_name}; přeskočeno: {', '.join(skipped) or 'nic'}.{outcome_cs}",
        )
    return None


def finding_references_failure(sources):
    return _failed_pipeline_finding(sources, "References (Crossref)", "references-failure",
                                    "A Crossref title mismatch stopped a deployment", "Neshoda názvu v Crossrefu zastavila nasazení")


def finding_production_failure(sources):
    return _failed_pipeline_finding(sources, "Verify production", "production-verification-failure",
                                    "Production verification failed, so no release was cut", "Ověření produkce selhalo, a proto nevzniklo vydání")


FINDINGS = (
    finding_scope_drift,
    finding_malformed_scope,
    finding_scope_outgrown,
    finding_ruleset_bypass,
    finding_live_verified_completion,
    finding_references_failure,
    finding_adr_left_to_person,
    finding_production_failure,
)


# ── schema check ──────────────────────────────────────────────────────────────────────────────


def _links(where, links, errors):
    if not isinstance(links, list):
        errors.append(f"{where}: links must be a list")
        return
    for link in links:
        if not (isinstance(link, dict) and isinstance(link.get("label"), str) and link["label"]
                and isinstance(link.get("url"), str) and link["url"].startswith("https://")):
            errors.append(f"{where}: link needs a label and an https url: {link!r}")


def _ts(where, value, errors, nullable=False):
    if value is None and nullable:
        return
    if not (isinstance(value, str) and TS.match(value)):
        errors.append(f"{where}: timestamp must be YYYY-MM-DDTHH:MM:SSZ, found {value!r}")


def validate(snapshot, root=None):
    errors = []
    if not isinstance(snapshot, dict):
        return ["snapshot must be a JSON object"]
    expected = {"schema": str, "repository": str, "site": str, "majordomus_version": str, "generated_from": dict,
                "milestones": dict, "tasks": list, "events": list, "findings": list, "commits": list, "pipelines": list, "releases": list}
    for key, kind in expected.items():
        if not isinstance(snapshot.get(key), kind):
            errors.append(f"'{key}' must be a {kind.__name__}")
    if errors:
        return errors
    if snapshot["schema"] != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")

    serialized = json.dumps(snapshot, ensure_ascii=False)
    if LOCAL_PATH.search(serialized):
        errors.append(f"snapshot contains a local path: {LOCAL_PATH.search(serialized).group(0)!r}")
    for key in PRIVATE_KEYS:
        if f'"{key}"' in serialized:
            errors.append(f"snapshot contains the private field '{key}'")

    ids = [event.get("id") for event in snapshot["events"]]
    for ident in sorted({i for i in ids if ids.count(i) > 1 and i}):
        errors.append(f"duplicate event id '{ident}'")
    previous = ""
    for position, event in enumerate(snapshot["events"]):
        where = f"events[{position}]"
        if not isinstance(event, dict):
            errors.append(f"{where}: must be an object")
            continue
        if not (isinstance(event.get("id"), str) and EVENT_ID.match(event["id"])):
            errors.append(f"{where}: id must match {EVENT_ID.pattern}")
        _ts(where, event.get("ts"), errors)
        if event.get("kind") not in KINDS:
            errors.append(f"{where}: kind must be one of {KINDS}")
        if not (isinstance(event.get("title_en"), str) and event["title_en"].strip()):
            errors.append(f"{where}: title_en is required")
        for optional in ("title_cs", "detail_en", "detail_cs", "task"):
            if optional in event and not isinstance(event[optional], str):
                errors.append(f"{where}: {optional} must be a string")
        _links(where, event.get("links"), errors)
        if isinstance(event.get("ts"), str):
            if event["ts"] < previous:
                errors.append(f"{where}: events are not sorted by time")
            previous = event["ts"]
    known = set(ids)

    for position, task in enumerate(snapshot["tasks"]):
        where = f"tasks[{position}]"
        if not (isinstance(task.get("id"), str) and TASK_ID.match(task["id"])):
            errors.append(f"{where}: id must match {TASK_ID.pattern}")
        _ts(where, task.get("started"), errors)
        _ts(where, task.get("finished"), errors, nullable=True)
        if task.get("outcome") not in OUTCOMES:
            errors.append(f"{where}: outcome must be one of {sorted(OUTCOMES)}")
        if task.get("outcome") == "active" and task.get("finished") is not None:
            errors.append(f"{where}: an active task has no finish time")
        if not (isinstance(task.get("scope_paths_count"), int) and task["scope_paths_count"] > 0):
            errors.append(f"{where}: scope_paths_count must be a positive integer")
        if not (isinstance(task.get("checkpoints"), int) and task["checkpoints"] >= 0):
            errors.append(f"{where}: checkpoints must be a non-negative integer")
        verify = task.get("verify")
        if verify is not None and not (isinstance(verify, dict) and isinstance(verify.get("command"), str)
                                       and isinstance(verify.get("exit"), int) and isinstance(verify.get("seconds"), (int, float))):
            errors.append(f"{where}: verify must be null or {{command, exit, seconds}}")
        if task.get("outcome") == "completed" and not (isinstance(verify, dict) and verify.get("exit") == 0):
            errors.append(f"{where}: a completed task needs a verification command that exited 0")
        contract = task.get("contract")
        if not isinstance(contract, dict) or any(value not in CONTRACT_RESULTS for value in contract.values()):
            errors.append(f"{where}: contract must map rule ids to {sorted(CONTRACT_RESULTS)}")

    for position, finding in enumerate(snapshot["findings"]):
        where = f"findings[{position}]"
        for key in ("id", "title_en", "title_cs", "detail_en", "detail_cs"):
            if not (isinstance(finding.get(key), str) and finding[key].strip()):
                errors.append(f"{where}: {key} is required")
        _ts(where, finding.get("ts"), errors)
        if finding.get("caught_by") is not None and not isinstance(finding["caught_by"], str):
            errors.append(f"{where}: caught_by must be a string or null")
        evidence = finding.get("evidence")
        if not (isinstance(evidence, list) and evidence):
            errors.append(f"{where}: evidence must list at least one event id")
        else:
            for ident in evidence:
                if ident not in known:
                    errors.append(f"{where}: evidence '{ident}' is not an event")
        if f"finding-{finding.get('id')}" not in known:
            errors.append(f"{where}: finding has no timeline event")
        _links(where, finding.get("links"), errors)

    for position, commit in enumerate(snapshot["commits"]):
        where = f"commits[{position}]"
        if not (isinstance(commit.get("sha"), str) and SHA.match(commit["sha"])):
            errors.append(f"{where}: sha must be 40 hex characters")
        _ts(where, commit.get("ts"), errors)
        if not isinstance(commit.get("subject"), str) or not str(commit.get("url", "")).startswith(REPO_URL + "/commit/"):
            errors.append(f"{where}: subject and a commit url are required")
    for position, pipeline in enumerate(snapshot["pipelines"]):
        where = f"pipelines[{position}]"
        if not isinstance(pipeline.get("id"), int) or not (isinstance(pipeline.get("sha"), str) and SHA.match(pipeline["sha"])):
            errors.append(f"{where}: id (integer) and sha are required")
        _ts(where, pipeline.get("created"), errors)
        _ts(where, pipeline.get("updated"), errors)
        if not isinstance(pipeline.get("conclusion"), str) or not isinstance(pipeline.get("jobs"), list):
            errors.append(f"{where}: conclusion and jobs are required")
        if not str(pipeline.get("url", "")).startswith(REPO_URL + "/actions/runs/"):
            errors.append(f"{where}: url must be a run of {REPOSITORY}")
    for position, release in enumerate(snapshot["releases"]):
        where = f"releases[{position}]"
        if not re.match(r"^v\d+\.\d+\.\d+$", str(release.get("tag"))):
            errors.append(f"{where}: tag must be vX.Y.Z")
        _ts(where, release.get("published"), errors)
        if not str(release.get("url", "")).startswith(REPO_URL + "/releases/tag/"):
            errors.append(f"{where}: url must be a release of {REPOSITORY}")

    counts = snapshot["generated_from"]
    for key, collection in (("tasks", "tasks"), ("findings", "findings"), ("commits", "commits"),
                            ("pipeline_runs", "pipelines"), ("releases", "releases"), ("events", "events")):
        if counts.get(key) != len(snapshot[collection]):
            errors.append(f"generated_from.{key} is {counts.get(key)!r}, but {collection} has {len(snapshot[collection])}")
    for key in ("checkpoints", "handovers", "decisions"):
        if not isinstance(counts.get(key), int):
            errors.append(f"generated_from.{key} must be an integer")
    for key, value in snapshot["milestones"].items():
        if key.endswith("_seconds"):
            if value is not None and not (isinstance(value, int) and value > 0):
                errors.append(f"milestones.{key} must be a positive integer")
        else:
            _ts(f"milestones.{key}", value, errors, nullable=True)

    if root is not None:
        errors.extend(validate_front_matter(root, known))
    return errors


def validate_front_matter(root, known):
    """The case-study pages point into the snapshot and the command registry; both references must resolve."""
    errors = []
    registry_path = root / "data/commands.toml"
    registry = {entry["id"] for entry in tomllib.loads(registry_path.read_text(encoding="utf-8")).get("commands", [])} if registry_path.exists() else set()
    for path in sorted((root / "content/case-study").glob("index*.md")):
        match = re.match(r"\A\+\+\+\s*\n(.*?)\n\+\+\+", path.read_text(encoding="utf-8"), re.S)
        if not match:
            errors.append(f"{path.relative_to(root)}: missing TOML front matter")
            continue
        extra = tomllib.loads(match.group(1)).get("extra", {})
        for step in extra.get("lifecycle", []):
            if step.get("command_id") and step["command_id"] not in registry:
                errors.append(f"{path.relative_to(root)}: lifecycle step '{step.get('id')}' names unregistered command '{step['command_id']}'")
            if step.get("example_event") and step["example_event"] not in known:
                errors.append(f"{path.relative_to(root)}: lifecycle step '{step.get('id')}' names unknown event '{step['example_event']}'")
        for row in extra.get("wiring", []):
            if row.get("command_id") and row["command_id"] not in registry:
                errors.append(f"{path.relative_to(root)}: wiring row '{row.get('where')}' names unregistered command '{row['command_id']}'")
    return errors


# ── entry point ───────────────────────────────────────────────────────────────────────────────


def dump(snapshot):
    return json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--out", type=Path, help="snapshot path (default: data/case_study.json under --root)")
    parser.add_argument("--check", action="store_true", help="validate the existing snapshot; no .ai/local, no network")
    parser.add_argument("--offline", action="store_true", help="export without gh, keeping the snapshot's GitHub records")
    args = parser.parse_args()
    root = args.root.resolve()
    out = (args.out or root / SNAPSHOT).resolve()

    if args.check:
        try:
            snapshot = json.loads(out.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            print(f"CASE STUDY\n────────────────────\nerror: cannot read {out.name}: {error}\n\nFAIL")
            return 1
        errors = validate(snapshot, root)
    else:
        snapshot = build(root, args.offline)
        errors = validate(snapshot, root)
        if not errors:
            out.write_text(dump(snapshot), encoding="utf-8")

    counts = snapshot.get("generated_from", {}) if isinstance(snapshot, dict) else {}
    print("CASE STUDY")
    print("────────────────────")
    for key in ("events", "tasks", "checkpoints", "handovers", "decisions", "findings", "commits", "pipeline_runs", "releases"):
        print(f"{key.replace('_', ' ')} {'.' * (18 - len(key))} {counts.get(key, '?')}")
    for error in errors:
        print(f"error: {error}")
    print()
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
