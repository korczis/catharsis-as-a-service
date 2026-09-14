+++
title = "Interactive models and search in a static site"
description = "How a site with no server runs simulations and search in the reader's browser: Alpine.js models drawn as SVG, including the Kuramoto model of synchrony, diacritic-insensitive search over an exported index, and per-page social previews rendered once and checked by hash without a browser."
date = 2026-09-14
weight = 6

[taxonomies]
tags = ["engineering", "simulation", "search", "alpine"]

[extra]
kicker = "Engineering 06"
kind = "technical"
summary = "Three features look as if they need a server and do not. Five interactive models run as small Alpine.js components that recompute SVG paths from sliders, with a fixed random seed so every reader sees the same run. Search loads a per-language JSON index once and ranks results in the browser, ignoring case and diacritics and matching Czech word forms by a crude stem. Social previews are rendered locally with headless Chrome, and CI verifies them from a hash manifest without launching a browser. This article explains each design and its limits."
key_points = [
  "The models are deterministic: a seeded mulberry32 generator and fixed time steps mean the same inputs always draw the same curves, which keeps the models testable and their outputs reproducible for every reader.",
  "Search normalizes text with Unicode decomposition, strips combining marks and compares truncated stems, so a query typed without Czech diacritics or in another case still matches.",
  "Preview images are an expensive build product, so the pipeline checks a manifest of input hashes instead of re-rendering; a page with a missing or stale image fails validation."
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## Constraints

Everything on this site is static files on GitHub Pages. There is no server to run code, no database to query and, by design, no third-party service: the site makes no requests to other hosts, sets no cookies and loads no analytics. Content must also stay readable without JavaScript. That rules out the usual answers for three features the library needed:

- interactive models that let a reader change an assumption and watch the consequence;
- search across both language editions and the glossary;
- a distinct link preview image for every page in every language.

Each was built so that the expensive or dynamic part happens either in the reader's browser or once on a developer machine, and so that the build can check the result without repeating the work.

## Five models as Alpine components

The [interactive models page](@/models/index.md) runs five simulations: the relief loop, venting and arousal over time, peak–end memory, synchrony in coupled oscillators, and allostatic load. Each is an Alpine.js component defined in [static/js/models.js](https://github.com/korczis/catharsis-as-a-service/blob/main/static/js/models.js), a 344-line script loaded only on that page and registered before Alpine starts.

The division of responsibility is the same as elsewhere on the site ([How the site was built](@/engineering/how-the-site-was-built/index.md)): **content lives in Markdown, behaviour in JavaScript.** Each model's question, explanation, how to read the chart, assumptions, limits, references and every UI label are front-matter fields in `content/models/index.md` and its Czech edition. The template passes the labels to the component as JSON:

{% raw -%}
```html
<div class="model" data-requires-js data-model="synchrony" x-data="synchrony"
     data-labels="{{ l | json_encode }}">
```
{%- endraw %}

so the script contains no language-specific text, and a reader without JavaScript still gets the full explanation, the assumptions and the limits, plus a note that the interactive part needs scripts.

Charts are plain SVG. The component exposes computed getters, and Alpine binds them to path and circle attributes:

```js
const line = (values, max) =>
  values.map((value, index) => `${index ? 'L' : 'M'}${x(index, values.length).toFixed(1)},${y(value, max).toFixed(1)}`).join(' ');
```

There is no chart library. A 600 × 240 viewBox, three helper functions and a handful of CSS classes cover every chart on the page, so the visual language matches the rest of the site and the whole feature adds no dependency.

### Determinism

Two of the models involve chance: whether the cause of distress changes in an episode, and the natural tempos of the oscillators. `Math.random()` would make every page load different, which is bad for readers comparing notes and worse for tests. The script uses a small seeded generator instead:

```js
// mulberry32: a small deterministic generator so every reader sees the same run for the same inputs.
const random = (seed) => {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};
```

With a fixed seed and fixed time steps, the same slider positions always produce the same curves. The browser test "interactive models respond to their inputs and stay labelled as illustrative" can therefore change an input, assert that the output changes, and confirm that the models stay labelled; the page banner reads "Illustrative models · not predictions about any person".

## The Kuramoto model in a browser

The synchrony model is the most computational of the five. The Kuramoto model describes a population of oscillators, each with its own natural frequency, each pulled towards the phases of the others. Below a critical coupling strength the phases drift; above it, part of the population locks into a common rhythm. The site uses it as an analogy for collective rhythm, and says so in the ledger and on the page: "It is a mathematical model of synchronization in general, not a model of dancers, crowds or bonding."

The implementation uses the mean-field form, which avoids comparing every pair of oscillators. First the component measures the order parameter, the length *r* and angle ψ of the average of all phases taken as unit vectors:

```js
measure() {
  const n = this.phases.length;
  const re = this.phases.reduce((sum, phase) => sum + Math.cos(phase), 0) / n;
  const im = this.phases.reduce((sum, phase) => sum + Math.sin(phase), 0) / n;
  this.order = Math.hypot(re, im);
  this.angle = Math.atan2(im, re);
},
```

Then every oscillator advances by one Euler step of dθᵢ/dt = ωᵢ + K·r·sin(ψ − θᵢ):

```js
this.phases = this.phases.map((phase, index) =>
  phase + DT * (this.tempos[index] + k * this.order * Math.sin(this.angle - phase)));
```

With at most 40 oscillators, a time step of 0.05 and two steps per animation frame, one frame costs a few hundred trigonometric calls, well within budget on a phone. The animation runs through `requestAnimationFrame` and stops when paused, and a "Step" button advances 40 steps at once without animating. The circle of dots and the arrow for *r* are SVG elements bound to the phases; a second SVG draws the recent history of *r*.

Small populations do not behave like the theory, and the page says so instead of hiding it: "With 4 to 40 oscillators, r fluctuates and rarely falls to 0 even without coupling; the sharp threshold of the mathematical theory holds for very large populations." A simulation that looked cleaner than the mathematics allows would contradict the site's own standard for data-like output. The model's claims, including the coupling threshold and its use only as an analogy, are entries in the evidence ledger with Kuramoto (1984) and Strogatz (2000) as sources.

## Search without a search server

The [search page](@/search/index.md) searches every page in the current language, including this one, and every glossary term. The index is produced at build time by [`python3 scripts/export-api.py`](../../commands/#export-api), which writes `api/v1/search.en.json` and `search.cs.json`. Each entry has a URL, title, description, section, kicker, tags and up to 1,500 characters of body text with Markdown syntax, links and code blocks stripped. Glossary terms become entries whose URL points at the term's anchor on the glossary page.

[static/js/search.js](https://github.com/korczis/catharsis-as-a-service/blob/main/static/js/search.js) fetches the index once, pre-normalizes every field and ranks entries as the reader types. The normalization carries most of the weight:

```js
const normalize = (value) =>
  String(value ?? '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase();

const stem = (term) => (term.length >= STEM_FROM ? term.slice(0, Math.max(STEM_MIN, term.length - STEM_TRIM)) : term);
```

`NFD` splits "č" into "c" and a combining caron, and the regular expression removes the combining marks, so "přehodnocení" and "prehodnoceni" compare equal. Czech inflects heavily, and a query for "katarzi" should find pages that say "katarze". A full stemmer for Czech would be a large dependency, so the script truncates: terms of six or more characters lose their last two, but never shrink below five. "Katarze" and "katarzi" both become "katar". The browser test types exactly those two cases on the Czech search page.

Ranking is weighted substring matching. Every query term must match somewhere, or the entry scores zero; a match adds 10 points in the title, 5 in the kicker or tags, 3 in the description and 1 in the body text. Results are sorted by score, then by title, and capped at 50. The query is mirrored into `?q=` with `history.replaceState`, so a search can be linked and the back button is not flooded.

The trade-offs are deliberate and visible. Truncation over-matches short common stems. Only the first 1,500 characters of a page's body are searchable, which keeps the index small but misses late sections of long essays. There is no typo tolerance. In exchange, search adds no dependency and no service, the query never leaves the browser, and the whole index is an inspectable file in the public API.

## Social previews rendered once, checked forever

A link shared in a chat or a social network shows a preview image. A single image for the whole site makes every shared page look the same, so each content page in each language gets its own 1200 × 630 card with its title, section and kicker.

Rendering those cards takes a real browser, since the design uses the site's web fonts and Czech text. [`python3 scripts/render-social.py`](../../commands/#render-social) opens [artwork/og.html](https://github.com/korczis/catharsis-as-a-service/blob/main/artwork/og.html) in headless Chrome with the page's fields as query parameters, takes a screenshot and converts it to a progressive JPEG with ImageMagick, rendering several pages in parallel. The output path mirrors the content path: `content/research/x/index.cs.md` becomes `static/og/research/x/index.cs.jpg`.

CI cannot sensibly do this on every push, and it does not need to. The script writes a manifest recording, for each image, a SHA-256 digest of everything that determines its pixels:

```python
digest = hashlib.sha256(json.dumps({**fields, "template": template_hash}, sort_keys=True).encode()).hexdigest()
```

where `fields` are the title, section label, kicker, the red footer line and the language, and `template_hash` is the digest of `og.html` itself. With `--check` the script needs no browser at all. It recomputes the digests from the content files and fails when a page has no image, when an image's recorded digest differs (a title was edited, or the template changed), or when an image belongs to no page. That check is the `social` stage of [`npm run validate`](../../commands/#npm-run-validate). The Python tests give it a missing and a stale preview and assert both messages, and a browser test confirms that sampled pages in both languages serve distinct `og:image` URLs with `image/jpeg` responses.

One detail from the template shows why rendering was not left to a generic tool. The display font is a condensed face whose capitals sit tight against the line above, and Czech capitals carry accents above the cap height:

```css
/* Czech capitals carry accents above the cap height; Anton needs extra leading so they clear the line above. */
:lang(cs) h1 { line-height: 1.24; padding-top: 0.08em; }
```

A similar adjustment appears on the site itself: a checkpoint from the first release records that the Czech display leading was raised to 1.2 "after measuring diacritic collisions".

The hash scheme has limits, and they are worth stating. The digest covers the page fields and the template file, but not the font files the template loads or the Chrome version that renders it. Changing a font would leave every image marked current, and a re-render with `--force` is the remedy. Rendering is also tied to a developer machine with Chrome and ImageMagick installed; the pipeline verifies images, it does not produce them.

## A common pattern

All three features follow the same pattern. Put the expensive or dynamic work where it is cheapest: in the reader's browser for models and search, once on a workstation for images. Export what the work needs as plain, inspectable data: front matter, a JSON index, a hash manifest. Then make the build verify the result rather than trust it. The models are deterministic enough to test, the search index is part of a versioned API with its own tests, and a preview image cannot drift out of date without failing validation.
