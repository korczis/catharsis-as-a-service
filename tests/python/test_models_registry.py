"""The model registry validator must pass on the repository and fail on every gap it exists to catch."""

import shutil

from conftest import ROOT, run, write

PY = "python3"
SCRIPT = str(ROOT / "scripts/validate-models.py")

MODEL = """[meta]
version = 1

[[models]]
id = "relief-loop"
kind = "simulation"
title = { en = "The relief loop", cs = "Smyčka úlevy" }
question = { en = "What happens to the urge?", cs = "Co se děje s nutkáním?" }
aria = { en = "A line chart over episodes.", cs = "Spojnicový graf přes epizody." }
prediction = false
claims = ["relief-negative-reinforcement"]
sources = ["rescorla-wagner-1972"]
assumptions = [
  { en = "Distress returns to the same level.", cs = "Tíseň se vrací na stejnou úroveň." },
  { en = "Relief is the same size every time.", cs = "Úleva je pokaždé stejně velká." },
]
limits = [
  { en = "The rule comes from conditioning research.", cs = "Pravidlo pochází z výzkumu podmiňování." },
  { en = "Causes rarely change by chance.", cs = "Příčiny se málokdy mění náhodou." },
]

[models.implementation]
module = "scripts/validate-models.py"
entry = "check_model"
tests = ["tests/python/test_models_registry.py"]

[models.epistemics]
inputs = "assumed"
mechanism = "derived"
parameters = "assumed"
output = "illustrative"

[models.explanations.essential]
en = "Relief teaches the behaviour that produced it."
cs = "Úleva učí chování, které ji přineslo."

[[models.rules]]
id = "urge-update"
statement = { en = "The urge grows with relief.", cs = "Nutkání roste s úlevou." }
formula = "urge += 0.15 * (1 - urge) * relief / 100"
claim = "relief-negative-reinforcement"

[[models.url_state]]
name = "relief"
min = 0
max = 60
step = 5
default = 20
"""


def fixture(tmp_path, registry=MODEL):
    shutil.copytree(ROOT / "data", tmp_path / "data", dirs_exist_ok=True)
    (tmp_path / "data" / "audiences.toml").unlink(missing_ok=True)
    write(tmp_path / "data/models.toml", registry)
    for rel in ("scripts/validate-models.py", "tests/python/test_models_registry.py"):
        write(tmp_path / rel, "placeholder check_model")
    return tmp_path


def check(root):
    return run([PY, SCRIPT, "--root", str(root)])


def test_registry_passes_on_the_repository():
    result = run([PY, SCRIPT])
    assert result.returncode == 0, result.stdout


def test_a_complete_model_passes(tmp_path):
    result = check(fixture(tmp_path))
    assert result.returncode == 0, result.stdout


def test_missing_registry_is_not_an_error(tmp_path):
    shutil.copytree(ROOT / "data", tmp_path / "data")
    (tmp_path / "data" / "models.toml").unlink(missing_ok=True)
    result = check(tmp_path)
    assert result.returncode == 0
    assert "absent" in result.stdout


def test_rejects_a_model_without_claims(tmp_path):
    result = check(fixture(tmp_path, MODEL.replace('claims = ["relief-negative-reinforcement"]', "claims = []")))
    assert result.returncode == 1
    assert "names no claims" in result.stdout


def test_rejects_an_unknown_claim(tmp_path):
    result = check(fixture(tmp_path, MODEL.replace("relief-negative-reinforcement", "no-such-claim")))
    assert result.returncode == 1
    assert "not in the ledger" in result.stdout


def test_rejects_a_field_in_one_language_only(tmp_path):
    result = check(fixture(tmp_path, MODEL.replace('cs = "Smyčka úlevy" }', 'cs = "" }')))
    assert result.returncode == 1
    assert "missing its cs text" in result.stdout


def test_rejects_too_few_limits(tmp_path):
    trimmed = MODEL.replace(
        '  { en = "Causes rarely change by chance.", cs = "Příčiny se málokdy mění náhodou." },\n', ""
    )
    result = check(fixture(tmp_path, trimmed))
    assert result.returncode == 1
    assert "at least 2 limits" in result.stdout


def test_rejects_a_missing_epistemic_class(tmp_path):
    result = check(fixture(tmp_path, MODEL.replace('mechanism = "derived"\n', "")))
    assert result.returncode == 1
    assert "epistemics.mechanism is missing" in result.stdout


def test_rejects_an_unknown_epistemic_class(tmp_path):
    result = check(fixture(tmp_path, MODEL.replace('output = "illustrative"', 'output = "measured"')))
    assert result.returncode == 1
    assert "not one of" in result.stdout


def test_rejects_a_prediction(tmp_path):
    result = check(fixture(tmp_path, MODEL.replace("prediction = false", "prediction = true")))
    assert result.returncode == 1
    assert "models arguments, not people" in result.stdout


def test_rejects_a_missing_implementation(tmp_path):
    result = check(fixture(tmp_path, MODEL.replace('module = "scripts/validate-models.py"', 'module = "static/js/models/nope.js"')))
    assert result.returncode == 1
    assert "implementation.module does not exist" in result.stdout


def test_rejects_a_model_without_a_test(tmp_path):
    result = check(fixture(tmp_path, MODEL.replace('tests = ["tests/python/test_models_registry.py"]', "tests = []")))
    assert result.returncode == 1
    assert "names no test" in result.stdout


def test_rejects_a_model_without_the_first_explanation(tmp_path):
    result = check(fixture(tmp_path, MODEL.replace("[models.explanations.essential]", "[models.explanations.technical]")))
    assert result.returncode == 1
    assert "explanations.essential" in result.stdout


def test_rejects_url_state_whose_default_is_out_of_range(tmp_path):
    result = check(fixture(tmp_path, MODEL.replace("default = 20", "default = 90")))
    assert result.returncode == 1
    assert "default lies outside" in result.stdout


def test_audience_ids_are_checked_once_the_file_exists(tmp_path):
    root = fixture(tmp_path, MODEL.replace("prediction = false", 'audiences = ["no-such-audience"]\nprediction = false'))
    result = check(root)
    assert result.returncode == 0, "without data/audiences.toml the audience list cannot be checked yet"

    kinds = "".join(f'[[epistemic_kinds]]\nid = "{k}"\n\n' for k in ("observed", "derived", "inferred", "assumed", "illustrative", "unknown"))
    write(
        root / "data/audiences.toml",
        '[[lenses]]\nid = "essential"\n\n[[audiences]]\nid = "general-reader"\nlens = "essential"\n\n' + kinds,
    )
    result = check(root)
    assert result.returncode == 1
    assert "not in data/audiences.toml" in result.stdout


def test_epistemic_kinds_come_from_the_audiences_file_without_fallback(tmp_path):
    root = fixture(tmp_path)
    write(root / "data/audiences.toml", '[[lenses]]\nid = "essential"\n\n[[audiences]]\nid = "general-reader"\nlens = "essential"\n')
    result = check(root)
    assert result.returncode == 1
    assert "declares no [[epistemic_kinds]]" in result.stdout

    write(root / "data/audiences.toml", '[[lenses]]\nid = "essential"\n\n[[epistemic_kinds]]\nid = "assumed"\n\n[[epistemic_kinds]]\nid = "derived"\n')
    result = check(root)
    assert result.returncode == 1
    assert "epistemics.output is 'illustrative', not one of" in result.stdout
