"""The JSON API export is the integration contract for other applications (docs/RUST-INTEGRATION.md)."""

import json

from conftest import run


def test_export_api_writes_the_contract(tmp_path):
    result = run(["python3", "scripts/export-api.py", "--out", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    api = tmp_path / "api" / "v1"

    index = json.loads((api / "index.json").read_text(encoding="utf-8"))
    assert index["api_version"] == 1
    assert index["endpoint"] == {"method": "POST", "path": "/v1/catharsis", "status": 200, "problem_solved": False}
    assert index["default_language"] in index["languages"]

    references = json.loads((api / index["references"]).read_text(encoding="utf-8"))
    commands = json.loads((api / index["commands"]).read_text(encoding="utf-8"))
    assert references and commands

    for collection in ("research", "advice"):
        slug_sets = []
        for language in index["languages"]:
            items = json.loads((api / index["collections"][collection][language]).read_text(encoding="utf-8"))
            assert items, f"{collection}.{language} is empty"
            slug_sets.append(sorted(item["slug"] for item in items))
            for item in items:
                assert item["url"].startswith(index["site"] + "/")
                assert item["references"], f"{collection}/{language}/{item['slug']} cites nothing"
                for reference in item["references"]:
                    assert reference in references
        assert all(slugs == slug_sets[0] for slugs in slug_sets), f"{collection} differs between languages"


def test_export_api_is_deterministic(tmp_path):
    first, second = tmp_path / "a", tmp_path / "b"
    for out in (first, second):
        assert run(["python3", "scripts/export-api.py", "--out", str(out)]).returncode == 0
    for path in sorted((first / "api/v1").glob("*.json")):
        assert path.read_bytes() == (second / "api/v1" / path.name).read_bytes(), path.name
