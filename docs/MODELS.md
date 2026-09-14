# Interactive models

An interactive model on this site is an argument you can run: it takes values you set, computes a result in
your browser from rules that are written down, and shows what the result does and does not mean. It is never
a measurement, never a prediction about a person, and never an assessment of anyone.

`data/models.toml` is the registry: one entry per model, shared by every language and every surface that
renders it. Prose stays in `content/models/`; the maths stays in `static/js/models/`; the registry is what
binds them to the evidence and what the build enforces.

## Why a registry

A model that draws a curve is making a claim about the world by other means. Three things must therefore be
inspectable for every model, in both languages, or the build fails:

1. **What it rests on** — the claims from `data/claims.toml` and the works from `data/references.toml`.
2. **What was invented** — which of its inputs, mechanism, parameters and output are observed, derived,
   inferred, assumed, illustrative or unknown.
3. **Where it breaks** — its assumptions and its limits, stated by the author, not implied by a caption.

## Schema

```toml
[meta]
version = 1

[[models]]
id = "relief-loop"                  # stable, kebab-case, unique; the anchor and the URL-state namespace
kind = "simulation"                 # simulation | comparison | sandbox
title = { en = "…", cs = "…" }
question = { en = "…", cs = "…" }   # the question the model exists to answer
prediction = false                  # must be false: nothing here predicts a person
claims = ["relief-negative-reinforcement"]        # ids in data/claims.toml
sources = ["rescorla-wagner-1972", "hayes-1996"]  # ids in data/references.toml
audiences = ["general-reader", "researcher"]      # ids in data/audiences.toml
aria = { en = "…", cs = "…" }       # what the chart shows, for a reader who cannot see it

assumptions = [
  { en = "…", cs = "…" },           # at least two: what the model takes for granted
]
limits = [
  { en = "…", cs = "…" },           # at least two: where it stops being a good analogy
]

[models.implementation]
module = "static/js/models/relief-loop.js"   # pure functions, no DOM
entry = "simulateReliefLoop"                 # the function the UI calls
tests = ["tests/js/relief-loop.test.mjs"]    # at least one; must exist

[models.epistemics]
inputs = "assumed"                  # observed | derived | inferred | assumed | illustrative | unknown
mechanism = "derived"
parameters = "assumed"
output = "illustrative"

[models.explanations.essential]     # per lens (data/audiences.toml); essential is required
en = "…"
cs = "…"

[[models.rules]]
id = "urge-update"
statement = { en = "…", cs = "…" }  # the rule in words
formula = "urge += 0.15 * (1 - urge) * relief / 100"
claim = "relief-negative-reinforcement"      # the claim this rule implements, or ""

[[models.url_state]]
name = "relief"                     # query parameter; the model's state must survive a reload
min = 0
max = 60
step = 5
default = 20
```

### Field rules

| Field | Rule |
|-------|------|
| `id` | Unique across the registry, stable once published: it is an anchor, a URL-state namespace and a test name. |
| `kind` | `simulation` computes a trajectory, `comparison` contrasts conditions, `sandbox` explores inference. |
| Localized fields | Every one is `{ en = …, cs = … }`, both non-empty. There is no fallback to English. |
| `claims`, `sources` | Must resolve in `data/claims.toml` and `data/references.toml`. A model with no claims is a drawing, not an argument, and is rejected. |
| `audiences` | Must resolve in `data/audiences.toml`; each audience declares the lens it is shown under. Checked only once that file exists. |
| `assumptions`, `limits` | At least two of each. "The model is simplified" is not a limit; name what it gets wrong. |
| `implementation` | The module must exist and hold pure functions; `entry` must appear in it; every test path must exist. |
| `epistemics` | All four of `inputs`, `mechanism`, `parameters`, `output`, each an id from `[[epistemic_kinds]]` in `data/audiences.toml`. Once that file exists its vocabulary is the only one accepted; there is no fallback to a built-in list. |
| `explanations` | Keyed by lens id; `essential` is required, the rest are optional and fall back to a shallower lens. |
| `rules` | At least one. Each names the claim it implements, or `""` when it is a drawing convention rather than a finding. |
| `url_state` | Every input the reader can change appears here, with its range and default, so a shared link reproduces the state. |
| `prediction` | Must be `false`. The registry has no place for a model that predicts a person. |

## What the build enforces

[`python3 scripts/validate-models.py`](https://korczis.github.io/catharsis-as-a-service/commands/#validate-models)
runs in [`npm run validate`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-validate) and fails the build when any rule above is broken: a missing or one-language
field, an unknown claim, source, audience or epistemic class, fewer than two assumptions or limits, no rule,
no test, a missing module or test file, a model that names no claims, or `prediction = true`.

It does not judge whether a model is any good. That is what the assumptions, the limits and the provenance
chain are for: every model renders the same `evidence.provenance` chain as a figure, from what you are
looking at, to the claim, to the studies, to the DOI.

## Content rules

These follow `project.no-neuro-overreach` and `project.medical-claims`:

- A model never describes, measures or assesses the person using it. Inputs are scenario values, not symptoms.
- Every surface carries the illustrative label: the numbers are computed from the reader's own inputs, and
  they come from no person, device or dataset.
- Where a model follows a published finding, it follows its **direction**, not its effect size or its timing,
  and says so in its limits.
- A lens changes what is shown, never what is claimed.
