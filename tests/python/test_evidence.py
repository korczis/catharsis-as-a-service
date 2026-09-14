"""The evidence ledger validator and the prohibited-phrase linter catch the defects they exist for."""

from conftest import run, write

PY = "python3"

REFERENCES = """
[references.study]
kind = "journal-article"
authors = "Doe, J."
year = "2020"
title = "A study"
container = "Journal"
volume = "1"
issue = ""
pages = "1"
publisher = ""
doi = "10.1000/example"
url = ""
"""

SOURCES = """
[sources.study]
design = "experiment"
level = "C"
population = { en = "Students.", cs = "Studenti." }
appraisal = { en = "Supports the claim.", cs = "Podporuje tvrzení." }
last_reviewed = 2026-09-14
review_due = 2027-09-14
"""


def claim(level="C", claim_type="empirical", due="2027-09-14", used_in='["research/note/index.md"]'):
    return f"""
[[claims]]
id = "a-claim"
statement = {{ en = "Something is associated with something.", cs = "Něco souvisí s něčím." }}
claim_type = "{claim_type}"
evidence_level = "{level}"
confidence = "MODERATE"
sources = ["study"]
scope = {{ en = "Students.", cs = "Studenti." }}
caveat = {{ en = "One study.", cs = "Jedna studie." }}
used_in = {used_in}
last_reviewed = 2026-09-14
review_due = {due}
"""


def ledger(tmp_path, claims_text):
    write(tmp_path / "data/references.toml", REFERENCES)
    write(tmp_path / "data/sources.toml", SOURCES)
    write(tmp_path / "data/claims.toml", claims_text)
    write(tmp_path / "data/evidence_changelog.toml", "entries = []\n")
    write(tmp_path / "data/glossary.toml", "terms = []\n")
    write(tmp_path / "content/research/note/index.md", "+++\ntitle = \"Note\"\n+++\n")
    write(tmp_path / "content/advice/.keep", "")
    return tmp_path


def validate(root, today="2026-09-15"):
    return run([PY, "scripts/validate-claims.py", "--root", str(root), "--today", today])


def test_ledger_passes_on_repository():
    result = run([PY, "scripts/validate-claims.py"])
    assert result.returncode == 0, result.stdout
    assert "claims ............" in result.stdout


def test_minimal_ledger_passes(tmp_path):
    result = validate(ledger(tmp_path, claim()))
    assert result.returncode == 0, result.stdout


def test_stale_review_date_fails(tmp_path):
    result = validate(ledger(tmp_path, claim()), today="2028-01-01")
    assert result.returncode == 1
    assert "(stale)" in result.stdout


def test_repository_ledger_expires_without_review():
    result = run([PY, "scripts/validate-claims.py", "--today", "2031-01-01"])
    assert result.returncode == 1
    assert "(stale)" in result.stdout


def test_claim_stronger_than_its_sources_fails(tmp_path):
    result = validate(ledger(tmp_path, claim(level="A")))
    assert result.returncode == 1
    assert "stronger than its best source (C)" in result.stdout


def test_clinical_boundary_interval_is_capped(tmp_path):
    result = validate(ledger(tmp_path, claim(claim_type="clinical-boundary")))
    assert result.returncode == 1
    assert "the maximum is 180" in result.stdout


def test_uncovered_research_note_fails(tmp_path):
    root = ledger(tmp_path, claim())
    write(root / "content/research/other/index.md", "+++\ntitle = \"Other\"\n+++\n")
    result = validate(root)
    assert result.returncode == 1
    assert "content/research/other/index.md makes claims but no ledger entry" in result.stdout


def test_dangling_used_in_fails(tmp_path):
    result = validate(ledger(tmp_path, claim(used_in='["research/note/index.md", "missing/index.md"]')))
    assert result.returncode == 1
    assert "content/missing/index.md does not exist" in result.stdout


def content_root(tmp_path, body):
    write(tmp_path / "data/commands.toml", "commands = []\n")
    description = "A page used by the test suite to check the prohibited phrase linter works."
    write(tmp_path / "content/page/index.md", f'+++\ntitle = "Page"\ndescription = "{description}"\n+++\n\n{body}\n')
    return tmp_path


def test_prohibited_phrases_fail(tmp_path):
    root = content_root(tmp_path, "This wristband detects emotions and the brain decides what you feel.")
    result = run([PY, "scripts/validate-content.py", "--root", str(root)])
    assert result.returncode == 1
    assert "prohibited phrasing 'detects emotion'" in result.stdout
    assert "prohibited phrasing 'the brain does X'" in result.stdout


def test_prohibited_czech_phrases_fail(tmp_path):
    root = content_root(tmp_path, "Náramek čte emoce a výsledky garantujeme.")
    result = run([PY, "scripts/validate-content.py", "--root", str(root)])
    assert result.returncode == 1
    assert "'čte emoce'" in result.stdout
    assert "'garantuje'" in result.stdout


def test_clinical_wording_is_allowed(tmp_path):
    root = content_root(tmp_path, "People diagnosed with PTSD were studied; a diagnosis requires a clinician.")
    result = run([PY, "scripts/validate-content.py", "--root", str(root)])
    assert result.returncode == 0, result.stdout
