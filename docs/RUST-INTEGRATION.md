# Rust integration

The site exports its library as a versioned JSON API. Other applications read that API instead of parsing
Markdown or templates. `crates/caas-content` is the Rust side of the contract and `crates/caas-cli` (binary
`caas`) is a command-line client built on it.

## The API

Produced by [`python3 scripts/export-api.py`](https://korczis.github.io/catharsis-as-a-service/commands/#export-api)
into `public/api/v1/` on every build and published with the site at
<https://korczis.github.io/catharsis-as-a-service/api/v1/index.json>. Output is deterministic: no timestamps,
stable ordering.

| File | Content |
|---|---|
| `index.json` | `api_version`, `site`, `default_language`, `languages`, file names of everything below, `endpoint` |
| `research.<lang>.json` | Research notes: slug, url, title, description, date, kicker, summary, key points, tags, references |
| `advice.<lang>.json` | Advice: evidence grade and label, recommendation, practice, limits, related notes, tags, references |
| `references.json` | The bibliography, keyed by id |
| `claims.json` | The evidence ledger: localized statement, scope and caveat; type, level, confidence, sources, pages, dates |
| `sources.json` | Appraisal of every reference: design, level, population, appraisal, dates |
| `glossary.json` | Glossary terms: localized term and definition, kind, see also, links, references |
| `evidence_changelog.json` | Ledger changes, newest first |
| `commands.json` | The command registry |

Dates are ISO 8601 strings. Localized fields are objects keyed by language code (`en`, `cs`).

### Versioning

`api_version` changes only for breaking changes (a removed or retyped field). Adding a file or a field is not
breaking: `caas-content` ignores unknown fields, so older clients keep working.

## The crate

```rust
use caas_content::{ClaimType, Library};

let library = Library::load("public/api/v1")?;
assert!(library.problems().is_empty());

for claim in library.claims_due_by("2027-03-31") {
    println!("{} {} {}", claim.id, claim.claim_type, claim.review_due);
}
let clinical = library
    .claims
    .iter()
    .filter(|claim| claim.claim_type == ClaimType::ClinicalBoundary)
    .count();
```

`Library::problems()` returns the integrity problems an application should refuse to run with: missing
translations of notes or advice, unknown references, advice without practice steps, a changed endpoint contract,
unappraised references, claims graded above their best source, and dangling glossary cross references.

The contract tests (`crates/caas-content/tests/contract.rs`) run against a fresh export, or against
`CAAS_API_DIR` when it is set; CI sets it to the export of the commit being tested.

## The CLI

```sh
cargo run -p caas-cli -- claims list --due-by 2027-03-31
cargo test --workspace
```

- [`cargo run -p caas-cli`](https://korczis.github.io/catharsis-as-a-service/commands/#caas-cli) with
  `advice list`, `advice show <slug>`, `research list`, `claims list [--due-by <date>]`, `claims show <id>`,
  `glossary show <id>`, `check` and `endpoint`. `--lang cs` selects the language, `--api <dir>` the export.
- [`cargo test --workspace`](https://korczis.github.io/catharsis-as-a-service/commands/#cargo-test),
  [`cargo clippy`](https://korczis.github.io/catharsis-as-a-service/commands/#cargo-clippy) and
  [`cargo fmt`](https://korczis.github.io/catharsis-as-a-service/commands/#cargo-fmt) run in the CI job `Rust`.

The endpoint stays what the artwork says it is: `POST /v1/catharsis` returns 200 with `problem_solved: false`.
