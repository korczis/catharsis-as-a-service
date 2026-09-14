"""The generated study pages must be a faithful, reproducible projection of the evidence ledger."""

import re
import tomllib

from conftest import ROOT, run

PY = "python3"
FRONT_MATTER = re.compile(r"\A\+\+\+\s*\n(.*?)\n\+\+\+\s*\n", re.S)
STUDIES = ROOT / "content" / "studies"


def front_matter(path):
    return tomllib.loads(FRONT_MATTER.match(path.read_text(encoding="utf-8")).group(1))


def data(name):
    return tomllib.loads((ROOT / "data" / f"{name}.toml").read_text(encoding="utf-8"))


def test_generation_is_reproducible():
    """Regenerating without a data change must leave the tree untouched: the build depends on it."""
    assert run([PY, "scripts/generate-study-pages.py"]).returncode == 0
    result = run([PY, "scripts/generate-study-pages.py", "--check"])
    assert result.returncode == 0, result.stdout
    assert "out of date ....... 0" in result.stdout


def test_every_reference_has_a_page_in_both_locales():
    run([PY, "scripts/generate-study-pages.py"])
    references = data("references")["references"]
    for ident in references:
        for name in ("index.md", "index.cs.md"):
            assert (STUDIES / ident / name).exists(), f"{ident}/{name} is missing"


def test_pages_carry_the_appraisal_and_the_claims_that_rest_on_the_work():
    run([PY, "scripts/generate-study-pages.py"])
    sources = data("sources")["sources"]
    claims = data("claims")["claims"]
    expected = {}
    for claim in claims:
        for ident in claim.get("sources", []):
            expected.setdefault(ident, set()).add(claim["id"])

    for path in sorted(STUDIES.glob("*/index.md")):
        meta = front_matter(path)
        extra = meta["extra"]
        ident = extra["reference"]
        assert extra["level"] == sources[ident]["level"]
        assert extra["design"] == sources[ident]["design"]
        assert set(extra["claims"]) == expected.get(ident, set())
        assert meta["template"] == "study.html"


def test_cited_by_names_pages_that_exist_and_actually_cite_the_work():
    run([PY, "scripts/generate-study-pages.py"])
    run([PY, "scripts/generate-term-pages.py"])
    for path in sorted(STUDIES.glob("*/index.md")):
        extra = front_matter(path)["extra"]
        for rel in extra["cited_by"]:
            cited = ROOT / "content" / rel
            assert cited.exists(), f"{path.parent.name} names a missing page: {rel}"
            assert extra["reference"] in front_matter(cited)["extra"]["references"]


def test_a_work_cited_only_by_a_glossary_term_is_not_reported_as_uncited():
    """A term page cites its sources too; a study page must not claim that nothing cites it."""
    run([PY, "scripts/generate-study-pages.py"])
    glossary = tomllib.loads((ROOT / "data" / "glossary.toml").read_text(encoding="utf-8"))["terms"]
    from_terms = {ident for term in glossary for ident in term.get("references", [])}
    assert from_terms, "the glossary cites no sources; this test would prove nothing"
    for ident in sorted(from_terms):
        page = STUDIES / ident / "index.md"
        if not page.exists():
            continue
        cited_by = front_matter(page)["extra"]["cited_by"]
        assert cited_by, f"{ident} is cited by a glossary term but its page reports no citing page"


def test_check_mode_reports_drift():
    run([PY, "scripts/generate-study-pages.py"])
    victim = sorted(STUDIES.glob("*/index.md"))[0]
    original = victim.read_text(encoding="utf-8")
    try:
        victim.write_text(original.replace('level = "', 'level = "X'), encoding="utf-8")
        result = run([PY, "scripts/generate-study-pages.py", "--check"])
        assert result.returncode == 1
        assert "is out of date" in result.stdout
    finally:
        victim.write_text(original, encoding="utf-8")
