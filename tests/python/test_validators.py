"""Validators must pass on the repository and fail on the defects they exist to catch."""

import shutil

from conftest import ROOT, run, write

PY = "python3"


def test_i18n_passes_on_repository():
    result = run([PY, "scripts/validate-i18n.py"])
    assert result.returncode == 0, result.stdout
    assert "missing: 0" in result.stdout


def test_i18n_reports_missing_translation(tmp_path):
    shutil.copy(ROOT / "zola.toml", tmp_path / "zola.toml")
    shutil.copytree(ROOT / "templates", tmp_path / "templates")
    write(tmp_path / "content/_index.md", '+++\ntitle = "Home"\n+++\n')
    write(tmp_path / "content/_index.cs.md", '+++\ntitle = "Domů"\n+++\n')
    write(tmp_path / "content/only-english/index.md", '+++\ntitle = "Only English"\n+++\n')
    result = run([PY, str(ROOT / "scripts/validate-i18n.py")], env={"CAAS_ROOT": str(tmp_path)})
    assert result.returncode == 1
    assert "missing cs translation for content/only-english/index.md" in result.stdout


def test_i18n_reports_front_matter_shape_mismatch(tmp_path):
    shutil.copy(ROOT / "zola.toml", tmp_path / "zola.toml")
    shutil.copytree(ROOT / "templates", tmp_path / "templates")
    write(tmp_path / "content/_index.md", '+++\ntitle = "Home"\n[extra]\nitems = ["a", "b"]\n+++\n')
    write(tmp_path / "content/_index.cs.md", '+++\ntitle = "Domů"\n[extra]\nitems = ["a"]\n+++\n')
    result = run([PY, str(ROOT / "scripts/validate-i18n.py")], env={"CAAS_ROOT": str(tmp_path)})
    assert result.returncode == 1
    assert "[extra] structure differs" in result.stdout


def test_content_passes_on_repository():
    result = run([PY, "scripts/validate-content.py"])
    assert result.returncode == 0, result.stdout


def _content_fixture(tmp_path, body):
    shutil.copytree(ROOT / "data", tmp_path / "data")
    write(tmp_path / "README.md", "# Fixture\n")
    write(
        tmp_path / "content/guides/index.md",
        '+++\ntitle = "Guides"\ndescription = "A description that is long enough to satisfy the SEO length rule."\n+++\n' + body,
    )
    return tmp_path


def test_content_rejects_unlinked_command(tmp_path):
    root = _content_fixture(tmp_path, "Run `npm run validate` before committing.\n")
    result = run([PY, str(ROOT / "scripts/validate-content.py"), "--root", str(root)])
    assert result.returncode == 1
    assert "mentioned without a link" in result.stdout


def test_content_rejects_unregistered_command_in_code_block(tmp_path):
    root = _content_fixture(tmp_path, "```sh\nnpm run does-not-exist\n```\n")
    result = run([PY, str(ROOT / "scripts/validate-content.py"), "--root", str(root)])
    assert result.returncode == 1
    assert "not registered: npm run does-not-exist" in result.stdout


def test_content_rejects_wrong_registry_anchor(tmp_path):
    root = _content_fixture(tmp_path, "Run [`npm run validate`](../commands/#npm-test).\n")
    result = run([PY, str(ROOT / "scripts/validate-content.py"), "--root", str(root)])
    assert result.returncode == 1
    assert "must link to the registry anchor #npm-run-validate" in result.stdout


def test_content_accepts_linked_command(tmp_path):
    root = _content_fixture(tmp_path, "Run [`npm run validate`](../commands/#npm-run-validate).\n")
    result = run([PY, str(ROOT / "scripts/validate-content.py"), "--root", str(root)])
    assert result.returncode == 0, result.stdout


def test_content_rejects_banned_promotional_phrasing(tmp_path):
    root = _content_fixture(tmp_path, "This festival poster sells a night out.\n")
    result = run([PY, str(ROOT / "scripts/validate-content.py"), "--root", str(root)])
    assert result.returncode == 1
    assert "banned promotional phrasing" in result.stdout


def test_references_pass_offline_on_repository():
    result = run([PY, "scripts/check-references.py"])
    assert result.returncode == 0, result.stdout


def test_references_reject_unknown_citation(tmp_path):
    shutil.copytree(ROOT / "data", tmp_path / "data")
    write(
        tmp_path / "content/research/note/index.md",
        '+++\ntitle = "Note"\n[extra]\nreferences = ["no-such-reference"]\n+++\n',
    )
    result = run([PY, str(ROOT / "scripts/check-references.py"), "--root", str(tmp_path)])
    assert result.returncode == 1
    assert "cites unknown reference 'no-such-reference'" in result.stdout


def test_references_reject_article_without_doi(tmp_path):
    write(
        tmp_path / "data/references.toml",
        '[references.x]\nkind = "journal-article"\nauthors = "A"\nyear = "2020"\ntitle = "T"\ncontainer = "J"\n'
        'volume = ""\nissue = ""\npages = ""\npublisher = ""\ndoi = ""\nurl = ""\n',
    )
    (tmp_path / "content").mkdir()
    result = run([PY, str(ROOT / "scripts/check-references.py"), "--root", str(tmp_path)])
    assert result.returncode == 1
    assert "needs a DOI" in result.stdout


def _html_site(tmp_path, page):
    base = "https://example.test/site"
    write(tmp_path / "index.html", page)
    write(tmp_path / "sitemap.xml", f"<urlset><url><loc>{base}/</loc></url></urlset>")
    write(tmp_path / "robots.txt", f"Sitemap: {base}/sitemap.xml\n")
    return base


GOOD_HEAD = (
    '<html lang="en"><head><title>T</title><meta name="description" content="d">'
    '<link rel="canonical" href="https://example.test/site/">'
    '<meta property="og:title" content="t"><meta property="og:description" content="d">'
    '<meta property="og:url" content="https://example.test/site/"><meta property="og:image" content="https://example.test/site/index.html">'
    '<meta property="og:image:alt" content="a"><meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary">'
    '<script type="application/ld+json">{"@context": "https://schema.org", "@graph": [{"@type": "WebSite"}]}</script>'
    "</head><body>"
)


def test_html_passes_on_valid_fixture(tmp_path):
    base = _html_site(tmp_path, GOOD_HEAD + '<h1 id="a">Title</h1><h2>Sub</h2><img src="index.html" alt="x"></body></html>')
    result = run([PY, str(ROOT / "scripts/validate-html.py"), str(tmp_path), base])
    assert result.returncode == 0, result.stdout


def test_html_reports_duplicate_ids_missing_alt_and_heading_jump(tmp_path):
    body = '<h1 id="a">T</h1><h3 id="a">Jump</h3><img src="index.html"><a href="missing.html">x</a></body></html>'
    base = _html_site(tmp_path, GOOD_HEAD + body)
    result = run([PY, str(ROOT / "scripts/validate-html.py"), str(tmp_path), base])
    assert result.returncode == 1
    for fragment in ("duplicate ids", "has no alt attribute", "heading level jumps", "broken reference"):
        assert fragment in result.stdout


def test_html_reports_invalid_structured_data(tmp_path):
    head = GOOD_HEAD.replace('{"@context": "https://schema.org", "@graph": [{"@type": "WebSite"}]}', "{not json")
    base = _html_site(tmp_path, head + "<h1>T</h1></body></html>")
    result = run([PY, str(ROOT / "scripts/validate-html.py"), str(tmp_path), base])
    assert result.returncode == 1
    assert "JSON-LD does not parse" in result.stdout
