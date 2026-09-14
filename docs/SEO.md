# Search, previews and structured data

Every generated page carries complete metadata. The templates produce it from front matter and UI strings;
validators and browser tests fail the build when any of it is missing.

## Per page

| Metadata | Source | Enforced by |
|---|---|---|
| `<title>` (unique per language) | page or section title | [scripts/validate-html.py](../scripts/validate-html.py) |
| `<meta name="description">`, 50–320 characters | `description` front matter | `validate-content.py`, `validate-html.py` |
| `<link rel="canonical">` | page permalink | `validate-html.py`, Playwright |
| `hreflang` alternates for `en`, `cs`, `x-default` | Zola translations | `validate-html.py`, Playwright |
| Open Graph: title, description, url, image (1200×630, localized), image alt, locale and alternate locale | `templates/partials/head.html` | `validate-html.py`, Playwright |
| Twitter card `summary_large_image` | same | same |
| `article:published_time` on dated pages | `date` front matter | Playwright |
| JSON-LD graph | `templates/partials/structured-data.html` | `validate-html.py`, Playwright |
| One `<h1>`, ordered headings, alt text, resolvable links and anchors | templates and content | `validate-html.py` |

## Structured data

Every page has a single JSON-LD graph with `WebSite` and `Person`, plus:

- `VisualArtwork` for the artwork (home and artifact page),
- `Article` for research notes, advice entries, methods, evidence, glossary and about, with `citation` DOIs,
- `DefinedTermSet` with a `DefinedTerm` per entry on the glossary,
- `CollectionPage` for listings,
- `BreadcrumbList` for every page below the home page.

`MedicalWebPage` and other medical types are forbidden: the site is educational (`project.medical-claims`).

## Site-wide

- `sitemap.xml` lists every page with alternates. Pages whose slug differs by language (glossary `/glossary/` and
  `/cs/slovnik/`) are declared in `zola.toml` under `[[extra.localized_paths]]`, which the sitemap template reads.
- Atom feeds per language and per tag, `robots.txt` pointing at the sitemap, a web manifest and the HTML5
  Boilerplate icon set.
- No analytics, trackers or cookies.

## Checking

- [`npm run validate`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-validate) runs every static check.
- [`npm test`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-test) checks metadata, previews and
  structured data in a browser; [`npm run test:production`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-test-production)
  repeats it against the live site after each deployment.
