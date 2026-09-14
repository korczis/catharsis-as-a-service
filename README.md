# CATHARSIS AS A SERVICE™

> Emotional State Transition Endpoint

[![Pages](https://github.com/korczis/catharsis-as-a-service/actions/workflows/pages.yml/badge.svg)](https://github.com/korczis/catharsis-as-a-service/actions/workflows/pages.yml)

**Live:** https://korczis.github.io/catharsis-as-a-service/ ([čeština](https://korczis.github.io/catharsis-as-a-service/cs/)) ·
**Repository:** https://github.com/korczis/catharsis-as-a-service ·
**Releases:** https://github.com/korczis/catharsis-as-a-service/releases

![Catharsis as a Service, desktop](docs/screenshot-desktop.png)

A digital artifact combining industrial rave imagery, human-systems telemetry and API semantics.

```text
INPUT    unresolved emotional state
PROCESS  repetition → synchronization → discharge
OUTPUT   temporary relief

problem_solved: false
```

## Concept

A festival campaign that sells catharsis at first glance and reveals, at second, that it is
instrumenting it. The endpoint returns `200 OK`. The underlying condition is unchanged.

The poster is the anchor: a monumental red-lit stage, a dense crowd and one anonymous figure
beneath a diagnostic overlay. The page around it exposes that overlay as a state transition, a
crowd model, conceptual telemetry (artistic values, never measurements) and the raw API response.

## Technology

| Layer | Choice | Version |
|---|---|---|
| Site generator | [Zola](https://www.getzola.org/) (Tera templates, Markdown content, native i18n) | 0.23.6 (`.zola-version`) |
| CSS | Tailwind CSS, CSS-first `@theme` tokens | 4.3.3 |
| Interaction primitives | Flowbite (modal, drawer, tooltip) | 4.0.2 |
| Client state | Alpine.js (header, view switch, copy feedback) | 3.17.2 |
| Tests | Playwright (Chromium) | 1.63.0 |
| Hosting | GitHub Pages via GitHub Actions | — |
| Supervision | [Majordomus](https://majordomus.dev) | 0.6.0 |

No framework runtime, no CDN, no analytics. Fonts (Anton, JetBrains Mono, Barlow Condensed) and
scripts are self-hosted.

## Architecture

| Concern | Lives in |
|---|---|
| Content | `content/` Markdown + front matter, one file per locale (`index.md`, `index.cs.md`) |
| UI strings | `zola.toml` `[translations]` and `[languages.cs.translations]`, read with `trans()` |
| Presentation | `templates/` (base, partials, `macros/artifact.html`), `styles/app.css` |
| Interaction | `static/js/app.js` (Alpine components, Flowbite instances), `static/js/locale.js` |
| Validation | `scripts/validate.sh` and the checks it runs, `tests/site.spec.js` |
| Deployment | `.github/workflows/pages.yml` (calls `ci.yml`), `scripts/release.sh` |
| Artwork sources | `artwork/` (poster and social preview sources, original concept image) |

Every artifact section (hero, diagnostic views, crowd, observability, poster, endpoint) is a macro
that reads only the page's front matter. A new artifact is a Markdown file pair; listing, sitemap,
language links and metadata follow from it.

Ownership never overlaps: Alpine owns the header state, the view switch and copy feedback; Flowbite
owns the artwork viewer, the mobile drawer and the tooltip; `locale.js` owns locale negotiation.

## Repository structure

```text
.ai/                    Majordomus layer (policy, rules, workflows); .ai/local/ is never committed
.github/workflows/      ci.yml (validate + e2e + supervision), pages.yml (deploy → verify → release)
.githooks/              commit-msg (Conventional Commits), pre-commit / pre-push (Majordomus)
artwork/                poster.html, social.html, bg.jpg, source/concept-1024x1536.png
content/                _index, artifacts/, about/ — each in en and cs
scripts/                validate.sh, validate-i18n.py, validate-html.py, smoke-production.sh,
                        preview.sh, dev.sh, lint-commits.sh, release.sh, render-artwork.sh, vendor.mjs
static/                 assets/ (poster master, social preview, icons), fonts/, js/, site.webmanifest
styles/app.css          Tailwind entry and design tokens
templates/              base.html, index.html, artifact.html, section.html, page.html, 404.html,
                        partials/, macros/
tests/site.spec.js      Playwright contract, local or production
zola.toml               site config, locales, UI dictionaries
```

## Local development

Requirements: Node.js 22+, Python 3.11+, [Zola 0.23.6](https://github.com/getzola/zola/releases/tag/v0.23.6),
and [Majordomus](https://majordomus.dev) for the commit hooks.

```sh
npm ci                  # installs pinned dependencies and wires .githooks
npm run dev             # Tailwind watch + zola serve on http://127.0.0.1:1111
```

Production-like preview under the same `/catharsis-as-a-service/` subpath GitHub Pages uses:

```sh
npm run preview         # http://127.0.0.1:4173/catharsis-as-a-service/
```

## Build and validation

```sh
npm run build           # vendor bundles + Tailwind + zola build → public/
npm run validate        # toolchain, assets, JS syntax, i18n parity, zola check, build, HTML/links
npm test                # Playwright against the local subpath preview
npm run test:production # the same suite against the live site
npm run smoke           # HTTP smoke test of the live site
```

`validate` fails on a missing translation, a UI string missing in any locale, a changed front-matter
shape between locales, a broken internal reference or anchor, a duplicate id, a missing alt text or a
heading jump.

## Deployment, verification and releases

Every push to `main` runs `.github/workflows/pages.yml`:

1. **validate**: `ci.yml` (Conventional Commit lint, Majordomus supervision check, `scripts/validate.sh`,
   Playwright against the subpath preview). The validated `public/` is the artifact that ships.
2. **deploy**: `actions/configure-pages` must report the same base URL as `zola.toml`, then the artifact is
   deployed with `actions/deploy-pages`.
3. **verify**: `scripts/smoke-production.sh` and the full Playwright suite run against the live URL.
4. **release**: `scripts/release.sh` tags `vX.Y.Z` from the commits since the last tag (breaking → major,
   `feat` → minor, anything else → patch) and publishes a GitHub Release with the poster attached.

Enforcement:

- local hooks: `commit-msg` rejects non-conventional subjects, `pre-commit` runs `majordomus doctor`,
  `pre-push` runs `majordomus finish --check`
- CI re-checks commit subjects and the Majordomus layer on every push and pull request
- a repository ruleset on `main` blocks force pushes and deletion; `v*` tags are protected

Pull requests run `ci.yml` only. Nothing deploys or releases without passing every stage before it.

## Adding content

1. Create `content/artifacts/<slug>/index.md` with the same front-matter shape as the existing artifact.
2. Create `content/artifacts/<slug>/index.cs.md` with the translated copy.
3. `npm run dev`, then `npm run validate && npm test`.
4. Commit (`feat(content): …`) and push. The pipeline deploys, verifies and releases.

## Adding a language

1. Add `[languages.<code>]` with `title`, `description` and a complete `translations` table to `zola.toml`.
2. Add `<code>` to `extra.locales`.
3. Add `*.<code>.md` for every content file. `validate-i18n.py` lists anything missing.

No template, script or workflow changes are needed.

## Supervision

This repository is supervised by Majordomus. Agents start at [`AGENTS.md`](AGENTS.md) (Claude Code:
[`CLAUDE.md`](CLAUDE.md)); both are generated from `.ai/repo/policy.yaml`. Project rules live in
`.ai/repo/rules/project/`.

## License status

© 2026 Sig Nihl. All rights reserved: no open license is granted for the artwork, text or code.
The bundled fonts are under the SIL Open Font License 1.1 (`static/fonts/LICENSES/`); Alpine.js and
Flowbite are MIT-licensed and vendored at build time from `node_modules`.

```text
POST /v1/catharsis → 200 OK
```
