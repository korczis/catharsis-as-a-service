# Audiences and lenses

The site serves a casual reader, a therapist, a researcher, an artist, a product designer, an
engineer and an epistemics researcher from one body of material. It does that without forking
the content: an audience is a **lens**, and a lens changes how much of the apparatus around a
statement is unfolded, never what the statement says.

The rule the whole architecture exists to keep:

> Do not create different truths for different audiences. Create different paths into the
> same truth.

A statement that is true under one lens is true under all of them. A lens that hid a
limitation would be a different truth for a different reader, which is the thing this project
is about not doing.

## The canonical file

[`data/audiences.toml`](../data/audiences.toml) is the only place the taxonomy exists. It
declares three things:

| Block | What it holds | Used by |
|---|---|---|
| `[[lenses]]` | six lenses, each with a bilingual label, summary and question, the disclosure slots it unfolds (`reveals`), and a starting point (`entry`) | the selector, `?view=`, `data-lens-for` |
| `[[audiences]]` | ten arrivals, each mapped to exactly one lens, with the questions they come with and a `never` clause | the landing entry points, `data/models.toml` `audiences = [...]` |
| `[[epistemic_kinds]]` | the six words every model and figure classifies its parts with | the epistemic key, the detection sandbox, model metadata |

Nothing else defines a lens id, an audience id or an epistemic class. `?view=` takes lens ids,
[`python3 scripts/validate-models.py`](https://korczis.github.io/catharsis-as-a-service/commands/#validate-models) rejects a model that names an audience or an epistemic class this file does not
define, and [`python3 scripts/export-api.py --out public`](https://korczis.github.io/catharsis-as-a-service/commands/#export-api) publishes the whole taxonomy at
`/api/v1/audiences.json` so a client reads it rather than copying it.

## The lenses

| Lens | `?view=` | Who arrives here | What it unfolds |
|---|---|---|---|
| Essential | `essential` (default) | general reader, educator | the question, something to try, plain language, the one limit that matters most |
| Practice | `practice` | helping professional | population, evidence level, limits, review date, gaps, the clinical disclaimer |
| Research | `research` | researcher, investigative reader | the mechanism, assumptions, parameters and where each came from, citations |
| Design | `design` | artist, product designer | the mechanism as something to design for, and what the effect is not |
| Technical | `technical` | engineer, evaluator | model id, schema, implementation, tests, seed, JSON, provenance |
| Epistemic | `epistemic` | AI and epistemic systems researcher | observed, derived, inferred, assumed, illustrative, unknown, alternatives |

Ten audiences, six lenses. A selector with one entry per audience would be a persona menu; the
six are the distinct depths the material actually has, and the audience→lens mapping in the
file is what lets a therapist and an epistemics researcher be served without writing anything
twice.

## How a lens reaches the page

1. `templates/base.html` reads the file, puts `data-lens`, `data-lens-default` and
   `data-lenses` on `<html>`, and renders the default lens.
2. Any block declares the lenses it belongs to: `<div data-lens-for="research technical">`.
   Multiple lenses are space-separated.
3. `styles/app.css` hides `[data-lens-for]` and shows the blocks whose list contains the
   lens named by `html[data-lens]`.
4. [`static/js/lens.js`](../static/js/lens.js) reads `?view=` on load, applies it, and turns
   the selector's links into an instant switch that pushes history, so Back moves between
   lenses.

Three consequences worth stating, because they are the reason it is built this way:

- **Every lens's markup is in every page.** Nothing is fetched or generated when a lens
  changes. A crawler, a printed page and a reader without JavaScript receive the whole
  document; `@media print` unfolds every lens, because paper has no switch.
- **The page is correct before the script runs.** The server renders the default lens and the
  links are real links (`?view=research`), so the switch works without JavaScript by
  navigating.
- **Nothing is stored.** The lens lives in the URL. It can be sent to somebody and bookmarked,
  and it leaves nothing on the reader's machine. See [PRIVACY](#privacy) below.

## Adding a lens-aware block to a page

```html
<div data-lens-for="research" class="mt-12">
  <h2 class="condensed section-title">{{ x.lenses.research.heading }}</h2>
  <p class="mt-3 max-w-3xl">{{ x.lenses.research.body }}</p>
</div>
```

The prose lives in the page's own front matter, bilingually, under `[extra.lenses.<lens>]`.
The lens layer holds no prose of its own: it decides what is unfolded, and each page says what
each lens unfolds about it. `content/detection-sandbox/index.md` is the worked example, with
all five of its lenses filled in.

Do not write a second copy of a statement for a second lens. If a sentence would have to
change between lenses to stay true, the sentence is wrong, not the lens.

## The epistemic vocabulary

Six words, defined once in `data/audiences.toml` and rendered by
`audience.epistemic_key`:

| Word | What it marks |
|---|---|
| observed | recorded by an instrument or reported by a person; on this site, the values a reader typed |
| derived | computed from observed values by a stated rule; adds no knowledge |
| inferred | a conclusion that goes beyond the values and could be wrong; always shown with its alternatives |
| assumed | taken as given so a model can run; changing it changes the output |
| illustrative | invented to make a relationship visible; carries direction, never magnitude |
| unknown | not available from anything the model has, and named rather than omitted |

[`/detection-sandbox/`](../content/detection-sandbox/index.md) is the demonstration: five
synthetic signals, four derived features, five competing readings with the arithmetic that
ranked them, and a list of what no signal settles. Change the setting and the signals do not
move while the leading reading does.

## Enforcement

| Check | What it refuses | Where |
|---|---|---|
| [`python3 scripts/validate-audiences.py`](https://korczis.github.io/catharsis-as-a-service/commands/#validate-audiences) | a missing translation, a non-kebab id, a duplicate id, a lens no audience maps to, a `reveals` slot no component renders, a `default_lens` that is not a lens, an `entry` whose page does not exist, an epistemic vocabulary that is not exactly the six words in order | `validate.sh`, step `audiences` |
| [`python3 scripts/validate-models.py`](https://korczis.github.io/catharsis-as-a-service/commands/#validate-models) | a model with no audience classification, no assumptions, no limits, no epistemic classification, or one that names an audience, a lens explanation or an epistemic class `data/audiences.toml` does not define; once this file exists there is no built-in fallback vocabulary | `validate.sh`, step `models` |
| [`python3 scripts/validate-content.py`](https://korczis.github.io/catharsis-as-a-service/commands/#validate-content) | prohibited phrasing anywhere, including this taxonomy — the audience file is content and is linted like content | `validate.sh`, step `content` |
| translation parity (step `i18n`) | a page whose `[extra]` shape differs between languages, which covers `[extra.lenses.*]` | `validate.sh`, step `i18n` |
| `tests/lens.spec.js` | a lens that does not switch, does not survive Back, does not fall back from an unknown value, or hides content from a reader without JavaScript | [`npm test`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-test) |
| `tests/sandbox.spec.js` | a sandbox whose rendered numbers disagree with its own pure functions, that returns one reading instead of the competing set, or whose URL state does not round-trip | [`npm test`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-test) |

## Privacy

The lens and every model run entirely in the browser. Nothing a reader sets is transmitted,
and nothing is written to storage: state lives in the URL, which is the only place it persists
and the only way it is shared. The site has no analytics, no trackers and no cookies, which is
a claim in the evidence ledger (`no-analytics-trackers-cookies`) and readable in the source.

## Related

- [`docs/CONTENT-STANDARDS.md`](CONTENT-STANDARDS.md) — the vocabulary content must use
- [`content/evidence/index.md`](../content/evidence/index.md) — how claims are graded
- [`docs/MODELS.md`](MODELS.md) — the interactive model registry schema that names these
  audiences, lenses and epistemic classes
