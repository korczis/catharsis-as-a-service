"""The audience taxonomy must pass on the repository and fail on the defects it exists to catch."""

import re

from conftest import ROOT, run, write

PY = "python3"
VALIDATOR = str(ROOT / "scripts/validate-audiences.py")
SOURCE = (ROOT / "data/audiences.toml").read_text(encoding="utf-8")


def _fixture(tmp_path, text=SOURCE):
    """A repository holding only the taxonomy and a stub page for every starting point it names."""
    write(tmp_path / "data/audiences.toml", text)
    for entry in set(re.findall(r'^entry = "([^"]+)"', text, re.M)):
        write(tmp_path / "content" / entry, "+++\ntitle = \"stub\"\n+++\n")
    return tmp_path


def _validate(tmp_path):
    return run([PY, VALIDATOR], env={"CAAS_ROOT": str(tmp_path)})


def test_audiences_pass_on_repository():
    result = run([PY, "scripts/validate-audiences.py"])
    assert result.returncode == 0, result.stdout
    assert "lenses ............ 6" in result.stdout
    assert "epistemic kinds ... 6" in result.stdout


def test_audiences_pass_on_an_unchanged_copy(tmp_path):
    result = _validate(_fixture(tmp_path))
    assert result.returncode == 0, result.stdout


def test_audiences_report_a_missing_translation(tmp_path):
    broken = SOURCE.replace('label = { en = "Essential", cs = "Základní" }', 'label = { en = "Essential", cs = "" }', 1)
    assert broken != SOURCE
    result = _validate(_fixture(tmp_path, broken))
    assert result.returncode == 1
    assert "lens essential: 'label.cs' is empty" in result.stdout


def test_audiences_report_an_audience_mapped_to_no_lens(tmp_path):
    broken = SOURCE.replace('id = "general-reader"\nlens = "essential"', 'id = "general-reader"\nlens = "casual"', 1)
    assert broken != SOURCE
    result = _validate(_fixture(tmp_path, broken))
    assert result.returncode == 1
    assert "audience general-reader: lens 'casual' is not one of" in result.stdout


def test_audiences_report_a_starting_point_that_does_not_exist(tmp_path):
    fixture = _fixture(tmp_path)
    (fixture / "content/evidence/index.md").unlink()
    result = _validate(fixture)
    assert result.returncode == 1
    assert "entry content/evidence/index.md does not exist" in result.stdout


def test_audiences_report_a_disclosure_slot_no_component_renders(tmp_path):
    broken = SOURCE.replace('reveals = ["question", "demonstration", "plain_language", "key_limitation"]',
                            'reveals = ["question", "vibes"]', 1)
    assert broken != SOURCE
    result = _validate(_fixture(tmp_path, broken))
    assert result.returncode == 1
    assert "reveals 'vibes', which no component renders" in result.stdout


def test_audiences_report_an_epistemic_vocabulary_that_is_not_the_six_words(tmp_path):
    broken = SOURCE.replace('id = "illustrative"', 'id = "plausible"', 1)
    assert broken != SOURCE
    result = _validate(_fixture(tmp_path, broken))
    assert result.returncode == 1
    assert "the epistemic vocabulary must define exactly" in result.stdout


def test_audiences_report_a_lens_no_audience_reaches(tmp_path):
    broken = SOURCE.replace('id = "epistemic-researcher"\nlens = "epistemic"', 'id = "epistemic-researcher"\nlens = "research"', 1)
    assert broken != SOURCE
    result = _validate(_fixture(tmp_path, broken))
    assert result.returncode == 1
    assert "lens epistemic: no audience maps to it" in result.stdout


def test_audiences_report_a_default_lens_that_does_not_exist(tmp_path):
    broken = SOURCE.replace('default_lens = "essential"', 'default_lens = "everything"', 1)
    assert broken != SOURCE
    result = _validate(_fixture(tmp_path, broken))
    assert result.returncode == 1
    assert "default_lens 'everything' is not one of the lenses" in result.stdout
