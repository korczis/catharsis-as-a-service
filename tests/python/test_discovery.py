"""Search index, theory export and per-page social previews."""

import json
import shutil

from conftest import ROOT, run, write

PY = "python3"


def test_search_index_covers_pages_and_glossary_terms(tmp_path):
    assert run([PY, "scripts/export-api.py", "--out", str(tmp_path)]).returncode == 0
    api = tmp_path / "api" / "v1"
    index = json.loads((api / "index.json").read_text(encoding="utf-8"))
    for language, filename in index["search"].items():
        entries = json.loads((api / filename).read_text(encoding="utf-8"))
        urls = [entry["url"] for entry in entries]
        assert len(urls) == len(set(urls)), f"duplicate search entries in {language}"
        sections = {entry["section"] for entry in entries}
        assert {"research", "advice", "glossary", "pages"} <= sections
        assert all(entry["url"].startswith(index["site"] + "/") for entry in entries)
        assert not any(entry["url"].rstrip("/").endswith(("/search", "/hledat")) for entry in entries)
        glossary = [entry for entry in entries if entry["section"] == "glossary" and "#" in entry["url"]]
        assert glossary, f"no glossary terms in {language}"
    cs = json.loads((api / index["search"]["cs"]).read_text(encoding="utf-8"))
    assert any("/cs/slovnik/#catharsis" in entry["url"] for entry in cs)
    assert any(entry["url"].endswith("/cs/research/venting-hypothesis/") for entry in cs)


def test_social_check_passes_on_repository():
    result = run([PY, "scripts/render-social.py", "--check"])
    assert result.returncode == 0, result.stdout


def test_social_check_reports_a_missing_preview(tmp_path):
    shutil.copy(ROOT / "zola.toml", tmp_path / "zola.toml")
    write(tmp_path / "artwork/og.html", (ROOT / "artwork/og.html").read_text(encoding="utf-8"))
    write(tmp_path / "content/about/index.md", '+++\ntitle = "About"\n+++\n')
    result = run([PY, str(ROOT / "scripts/render-social.py"), "--check", "--root", str(tmp_path)])
    assert result.returncode == 1
    assert "content/about/index.md: social preview static/og/about/index.jpg is missing" in result.stdout


def test_social_check_reports_a_stale_preview(tmp_path):
    shutil.copy(ROOT / "zola.toml", tmp_path / "zola.toml")
    write(tmp_path / "artwork/og.html", (ROOT / "artwork/og.html").read_text(encoding="utf-8"))
    write(tmp_path / "content/about/index.md", '+++\ntitle = "About"\n+++\n')
    write(tmp_path / "static/og/about/index.jpg", "not really a jpeg")
    write(tmp_path / "static/og/manifest.json", json.dumps({"about/index.jpg": "0" * 64}))
    result = run([PY, str(ROOT / "scripts/render-social.py"), "--check", "--root", str(tmp_path)])
    assert result.returncode == 1
    assert "is stale" in result.stdout
