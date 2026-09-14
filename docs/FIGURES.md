# Figures

The site's charts and diagrams share one visual language: dark ground, bone strokes, one blood-red
accent, condensed uppercase labels, mono uppercase metadata, square boxes, dashed guides. This document
specifies that language and the data format that reproduces it. A figure is **data in front matter**; the
geometry lives only in `templates/components/illustrations.html`, so two figures of the same kind are always
drawn the same way, in both languages, on screen and in print.

## Where figures come from

| Place | How |
|-------|-----|
| Research notes and theory essays | `[[extra.figures]]` tables in the page's front matter, rendered by `library.figures` above the prose. |
| Any other template | Call the component directly: `{{ <illustration.curves id="fig-x" labels={map} /> }}`. |

The EN and CS files carry the same figure with the same `id`, `kind`, values and structure; only the
strings differ (the i18n step of
[`npm run validate`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-validate) checks the shape).

## Visual tokens

Colours come from CSS tokens (`styles/app.css`, section *Illustrations*); a figure never sets a colour.

| Role | Class | Token | Use |
|------|-------|-------|-----|
| Primary series, node strokes, arrows | `bone` | `--color-bone` | The reading the text supports. |
| Accent | `alert` | `--color-blood` | Exactly one thing per figure: the misleading path, the loop, the problem node. |
| Reference | `muted` | `--color-muted`, dashed | A comparison or control condition. |
| Axes | `.ill-axis` | `--color-muted` | Always present on `curves`. |
| Guides | `.ill-grid` | `--color-line`, dashed | Baseline and event lines. |
| Label | `.ill-label` | condensed, 18px (15px at five nodes), uppercase | Series names, node titles. |
| Metadata | `.ill-meta` | mono, 11px, tracked uppercase | Axis titles, indices, events, machine-style notes (`decision: null`). |

In print every stroke and text is forced to black on white (`@media print`).

## Narrow screens

A `curves` or `pipeline` figure keeps a minimum drawing width (34rem, or 44rem for a row of more than three
nodes) and scrolls sideways inside its own focusable region below it, rather than shrinking its labels until
they cannot be read; at those widths the mono metadata is set larger, because the drawing is scaled down. The page body itself never scrolls sideways, and in print the region expands and the
whole figure is drawn. Because a `curves` figure carries its series labels at the right edge of the drawing,
where a narrow screen scrolls them out of view, the same labels are repeated as a key below the figure and
CSS shows that key only at those widths. The fixed kinds used on the landing page are unaffected.

## Kinds

| Kind | For | Data |
|------|-----|------|
| `curves` | A quantity over time or condition, two or three trajectories compared. | See below. |
| `pipeline` | A sequence of stages, optionally with one return loop. | See below. |
| `timeline` | Dated milestones. | `items = [{ year, label }]` |
| `relief_loop`, `relief_curve`, `synchrony` | Fixed figures of the catharsis argument; labels only. | See `content/research/relief-is-not-resolution`. |
| `screens`, `posters` | Image galleries. | See `templates/components/library.html`. |

Prefer `curves` and `pipeline` for new figures; add a fixed kind only when the drawing cannot be expressed
as data, and document it here.

### `curves`

Plot area x 70–690, y 30–330 in a 720×400 viewBox. Values are on a 0–100 scale; value `v` is drawn at
`y = 330 − 3v`, and points are spaced evenly. The line is a Catmull–Rom spline through every point, drawn as
cubic Béziers (control points at one third of a step, slope from the neighbouring points, end points clamped),
so it passes exactly through each value without steps at the points. Keep values between 5 and 95 when a
neighbour changes sharply, so the curve does not bend past the axes.

```toml
[[extra.figures]]
kind = "curves"
id = "fig-venting-arousal"          # unique on the page; same in EN and CS
title = "…"                          # SVG <title>
description = "…"                    # SVG <desc>: what the lines do, in words
caption = "Figure 1. … Conceptual illustration, not measured data."
axis_x = "time"
axis_y = "anger"
baseline = "baseline"                # optional dashed horizontal guide …
baseline_value = 20                  # … at this value (required with baseline)
events = [{ at = 1, label = "provocation" }]   # optional vertical guides at point indexes
series = [
  { label = "venting", style = "alert", values = [20, 62, 70, 74, 71, 69, 67] },
  { label = "lowering arousal", style = "bone", values = [20, 62, 52, 43, 36, 31, 28] },
]
```

Series fields: `label`, `values` (3–12 numbers, 0–100, the same count in every series), `style`
(`bone` default, `alert`, `muted`), optional `marker` (index of a dot), `label_at` (index where the label
sits; default the last point, right-aligned) and `label_dy` (vertical label offset; default −14). At most
three series.

### `pipeline`

Two to five nodes in one row between x 20 and 700 of a 720×320 viewBox, 28 units apart. A label breaks
onto two lines at `|`.

```toml
[[extra.figures]]
kind = "pipeline"
id = "fig-rumination-loop"
title = "…"
description = "…"
caption = "Figure 1. …"
axis = "the emotion unfolds in time"     # optional arrow above the nodes
nodes = [
  { label = "Unresolved|problem", meta = "input" },
  { label = "Why does|this happen?", meta = "abstract", mark = "feels like processing", alert = true },
  { label = "Replaying", meta = "01" },
  { label = "Lower mood", meta = "02" },
]
loop = { from = 3, to = 1, label = "no new information", meta = "decision: null" }   # optional
```

Node fields: `label`, `meta` (index or short type, shown small below), optional `mark` (text above the
node) and `alert` (red outline and label). `loop` draws one dashed red return arrow below the row.

## Content rules

These follow `project.no-neuro-overreach` and `project.medical-claims`:

- A figure illustrates a finding the page text states and cites; the caption names the source.
- Anything drawn like data (`curves`, `relief_curve`) that is not measured says so in the caption:
  *Conceptual illustration, not measured data.* / *Koncepční ilustrace, nikoli naměřená data.*
  Values encode direction and shape, never an effect size.
- An interpretation that belongs to this site, not the source, is labelled as such in the caption.
- One red element per figure. Red marks the path the text argues against or the point of failure.
- `title` and `description` make the figure an accessible image; the description says in words what the
  drawing shows.

## Validation

[`python3 scripts/validate-content.py`](https://korczis.github.io/catharsis-as-a-service/commands/#validate-content)
checks every figure on every page: a known `kind`, an `id` unique on the page,
and for `curves` and `pipeline` the required fields, value ranges, index bounds, series lengths, node count,
two-line labels and the loop target; for data-like kinds it requires the conceptual label in the caption.
Tests: `tests/python/test_validators.py`.

## Adding a figure

1. Pick the kind from the table above and write the data in the EN page.
2. Copy the table to the CS page; translate the strings only.
3. Run [`python3 scripts/validate-content.py`](https://korczis.github.io/catharsis-as-a-service/commands/#validate-content)
   and [`npm run validate`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-validate), then
   look at the page in [`npm run dev`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-dev) on
   a narrow and a wide screen.
