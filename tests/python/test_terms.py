"""The generated term pages must be a faithful, reproducible projection of the glossary."""

import re
import tomllib

from conftest import ROOT, run

PY = "python3"
FRONT_MATTER = re.compile(r"\A\+\+\+\s*\n(.*?)\n\+\+\+\s*\n", re.S)
TERMS = ROOT / "content" / "terms"


def front_matter(path):
    return tomllib.loads(FRONT_MATTER.match(path.read_text(encoding="utf-8")).group(1))


def glossary():
    return tomllib.loads((ROOT / "data" / "glossary.toml").read_text(encoding="utf-8"))["terms"]


def test_generation_is_reproducible():
    assert run([PY, "scripts/generate-term-pages.py"]).returncode == 0
    result = run([PY, "scripts/generate-term-pages.py", "--check"])
    assert result.returncode == 0, result.stdout
    assert "out of date ....... 0" in result.stdout


def test_every_term_has_a_page_in_both_locales():
    run([PY, "scripts/generate-term-pages.py"])
    for term in glossary():
        for name in ("index.md", "index.cs.md"):
            assert (TERMS / term["id"] / name).exists(), f"{term['id']}/{name} is missing"


def test_pages_carry_the_definition_and_its_relations():
    run([PY, "scripts/generate-term-pages.py"])
    for term in glossary():
        for lang, name in (("en", "index.md"), ("cs", "index.cs.md")):
            meta = front_matter(TERMS / term["id"] / name)
            assert meta["title"] == term["term"][lang]
            assert meta["extra"]["definition"] == term["definition"][lang]
            assert meta["extra"]["kind"] == term["kind"]
            assert meta["extra"]["see_also"] == term.get("see_also", [])
            assert meta["extra"]["references"] == term.get("references", [])


def test_related_terms_and_uses_resolve():
    """A term page links to other term pages and to the pages that use it; both must exist."""
    run([PY, "scripts/generate-term-pages.py"])
    ids = {term["id"] for term in glossary()}
    for path in sorted(TERMS.glob("*/index.md")):
        extra = front_matter(path)["extra"]
        for other in extra["see_also"]:
            assert other in ids, f"{path.parent.name} points at unknown term {other}"
        for rel in extra["used_by"]:
            assert (ROOT / "content" / rel).exists(), f"{path.parent.name} names a missing page: {rel}"


def test_descriptions_stay_within_the_content_rule():
    run([PY, "scripts/generate-term-pages.py"])
    for path in sorted(TERMS.glob("*/index*.md")):
        description = front_matter(path)["description"]
        assert 50 <= len(description) <= 320, f"{path}: description has {len(description)} characters"


def test_check_mode_reports_drift():
    run([PY, "scripts/generate-term-pages.py"])
    victim = sorted(TERMS.glob("*/index.md"))[0]
    original = victim.read_text(encoding="utf-8")
    try:
        victim.write_text(original.replace('kind = "', 'kind = "x'), encoding="utf-8")
        result = run([PY, "scripts/generate-term-pages.py", "--check"])
        assert result.returncode == 1
        assert "is out of date" in result.stdout
    finally:
        victim.write_text(original, encoding="utf-8")
