+++
title = "Guides"
description = "How to read the artifact, share it, publish new work, add a language, verify a deployment and work under Majordomus, with the reasoning behind each step."
+++

Practical guides for readers, for people sharing the work, and for whoever publishes the next artifact. Each guide says what to do and why it is done that way.

## Reading the artifact

Start with the poster, not the text. The first reading is the campaign; let it land before looking for the diagnosis.

1. The **Experience** view shows the state transition as a sequence: input, process, output.
2. The **Diagnostic** view shows the status matrix. The HTTP status and the problem status disagree on purpose.
3. The **Raw** view states the same claim as an API response, for people who trust JSON more than posters.

The observability table uses artistic values. The bars show intensity, not measurement, and the red rows are the ones that did not change.

**Why it is built this way:** the gap between `200 OK` and `problem_solved: false` is the work. Every view restates that gap in a different register instead of explaining it away.

## Sharing and link previews

Every page carries Open Graph and Twitter Card metadata, so messengers and social networks show a proper preview card instead of a bare URL.

- English pages use the English preview card; Czech pages use a Czech card with a translated subtitle.
- Each language edition points to the other through `hreflang` and `og:locale:alternate`, so a shared Czech link stays Czech.
- Search engines receive structured data (WebSite, VisualArtwork, BreadcrumbList) and are allowed to show a large image preview.

To share a specific language, link to it directly: `/` for English, `/cs/` for Czech. The English home page moves a first-time visitor with a Czech browser to the Czech edition, but a direct link always wins.

**Why:** a link preview is often the only part of the work someone sees. It should carry the same first-glance, second-glance tension as the poster, in the reader's language.

## Publishing a new artifact

1. Create `content/artifacts/<slug>/index.md` by copying the existing artifact and keeping the same front-matter structure.
2. Create `content/artifacts/<slug>/index.cs.md` with the translated copy. The structure must match; only the values change.
3. Put the poster master under `static/assets/` and point `extra.poster` at it. Responsive WebP versions are generated at build time.
4. Preview with [`npm run dev`](../commands/#npm-run-dev), then run [`npm run validate`](../commands/#npm-run-validate) and [`npm test`](../commands/#npm-test).
5. Commit with a conventional message such as `feat(content): add <slug>` and push to `main`.

**Why:** the listing, sitemap, feeds, language links, previews and structured data all derive from those two files. There is nothing else to update, so there is nothing to forget.

## Adding a language

1. Add `[languages.<code>]` to `zola.toml` with a title, a description and a complete `translations` table.
2. Add the code to `extra.locales`.
3. Add a `*.<code>.md` file next to every content file.
4. Run [`npm run validate`](../commands/#npm-run-validate); the i18n check lists every missing file or string.

No template, script or workflow has to change. That is a design constraint, not an accident: templates never branch on language, so a new language cannot need template work.

## Verifying a deployment

A green build is not a deployment. The pipeline treats the live URL as the only evidence:

1. **validate** builds the site and checks translations, links, anchors, metadata, structured data and accessibility basics.
2. **e2e** runs the browser suite against a local copy served under the same subpath as GitHub Pages, so base-path mistakes fail before they ship.
3. **deploy** refuses to publish if Pages reports a different base URL than the site was built for.
4. **verify** waits until production serves the new commit, then runs the smoke test and the full browser suite against the live site.
5. **release** tags a version only after verify has passed.

To check by hand:

```sh
npm run smoke            # every page and asset of the live site
npm run test:production  # the browser suite against the live URL
gh run list --workflow pages.yml --limit 5
```

**Why:** most real failures of static sites (a wrong subpath, a stale CDN, a missing asset) are invisible in the build and obvious on the live URL.

## Working under Majordomus

This repository is supervised by Majordomus. The workflow for a change:

```sh
majordomus start "<task>" --scope content,templates
majordomus check                      # before claiming progress
majordomus checkpoint < note.md       # progress worth keeping
majordomus finish --outcome completed --verify-command "npm run smoke"
```

What it adds, and why it matters here:

- **Scope** keeps a content change from quietly touching the pipeline, and makes accidental edits visible before a push.
- **Checkpoints and handovers** let anyone, human or agent, resume from recorded facts.
- **The finish contract** means "done" requires a passing verification command, which for this site is the live smoke test.
- **Hooks** run [`majordomus doctor`](../commands/#majordomus-doctor) before every commit and [`majordomus finish --check`](../commands/#majordomus-finish) before every push. When a hook refuses, read the finding: it names the file and the rule.

## Releases

Releases are automatic. Every verified push to `main` produces a GitHub Release. The version comes from the commits since the previous tag: a breaking change bumps the major version (the minor while the project is at 0.x), `feat` bumps the minor, everything else the patch.

**Why:** releasing often is only safe when it is gated and mechanical. Commit messages are the version input, which is why they are checked at commit time and again in CI.
