# Architecture

A static publication: Markdown and TOML in, validated HTML and JSON out, deployed only after it is verified
against the live URL.

## Flow

```text
content/*.md ─┐
data/*.toml ──┼─► Zola 0.23.6 (Tera v2 templates) ─► public/ ─► validators ─► GitHub Pages ─► live verification ─► release
zola.toml ────┘                     │                               ▲
styles/app.css ─► Tailwind CSS 4 ───┘   scripts/export-api.py ─► public/api/v1 ─► caas-content (Rust)
```

## Layers

| Layer | Lives in | Notes |
|---|---|---|
| Content | `content/` (one file per language) | research, advice, methods, evidence, glossary, status, about, guides, commands, artifacts |
| Data | `data/` | references, sources, claims, evidence changelog, glossary, command registry |
| UI strings | `zola.toml` `[translations]` | parity enforced by [scripts/validate-i18n.py](../scripts/validate-i18n.py) |
| Templates | `templates/` | page templates plus components: `artifact`, `landing`, `library`, `evidence`, `illustration` |
| Styles | `styles/app.css` | design tokens and components on Tailwind CSS 4 with the Flowbite plugin |
| Behaviour | `static/js/app.js`, `static/js/locale.js` | Alpine: header, view switch, copy, claim panels, detection simulation. Flowbite: modal, drawer, tooltip, accordion. Content is complete without JavaScript |
| API | [scripts/export-api.py](../scripts/export-api.py) → `api/v1` | contract in [RUST-INTEGRATION.md](RUST-INTEGRATION.md) |
| Rust | `crates/caas-content`, `crates/caas-cli` | typed client, integrity checks, CLI |
| Supervision | `.ai/`, `.githooks/` | Majordomus policy, project rules, ADRs; hooks run the health check and the finish contract |
| Delivery | `.github/workflows/` | `ci.yml` (gate), `pages.yml` (deploy, verify, release), `evidence-freshness.yml` (weekly) |

## Routes

| Route | Template | Data |
|---|---|---|
| `/`, `/cs/` | `index.html` | `content/_index*.md` landing blocks, featured artifact |
| `/research/<slug>/` | `essay.html` | front matter, references, ledger claims (`used_in`) |
| `/advice/<slug>/` | `advice.html` | front matter, references, ledger claims |
| `/methods/` | `methods.html` | structured blocks in front matter, simulation, ledger claims |
| `/evidence/` | `evidence.html` | claims, sources, references, changelog |
| `/glossary/`, `/cs/slovnik/` | `glossary.html` | `data/glossary.toml` |
| `/status/` | `status.html` | ledger statistics, build metadata from `CAAS_VERSION`, `CAAS_COMMITTED`, `GITHUB_SHA` |
| `/commands/` | `commands.html` | `data/commands.toml` |
| `/tags/…` | taxonomy templates | tags from front matter |

## Validation stages

[`npm run validate`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-validate) runs, in order:
toolchain, assets, JavaScript syntax, translations, content standards, references, evidence ledger, Zola check,
Zola build, API export and HTML. [`npm run test:python`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-test-python)
tests the validators and registered commands, and [`npm test`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-test)
runs the browser suite.

## Decisions

Architecture decisions are recorded in `.ai/repo/adrs/`. See also [EVIDENCE.md](EVIDENCE.md),
[CONTENT-STANDARDS.md](CONTENT-STANDARDS.md) and [SEO.md](SEO.md).
