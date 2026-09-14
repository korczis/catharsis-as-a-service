+++
title = "Status"
description = "Build revision, content version and the state of the evidence ledger: claims by level, confidence and type, the next reviews due, and the checks that run on every change."
template = "status.html"

[extra]
kicker = "Status"
intro = "This page is generated on every build from the repository itself: the commit it was built from, the evidence ledger and the review schedule. If a claim passes its review date, the build fails before this page can be published."
checks = [
  { name = "Content standards", text = "Required front matter, description length, links from every mentioned command to its registry entry, and a linter for prohibited phrasing such as claims that a sensor can tell what someone feels." },
  { name = "Evidence ledger", text = "Every reference is appraised, every claim is graded no higher than its best source, every research note and advice entry is covered, and no review date has passed." },
  { name = "References", text = "Registry fields and citations offline; DOIs, titles and years against Crossref in continuous integration and weekly." },
  { name = "Translations", text = "English and Czech have the same pages, the same front-matter structure and the same interface strings." },
  { name = "Generated site", text = "One h1 per page, heading order, alt text, canonical and hreflang links, link previews, JSON-LD, internal links, anchors and the sitemap." },
  { name = "Content API", text = "Deterministic JSON export, read by Rust contract tests and the command-line client." },
  { name = "Browser tests", text = "Playwright on four viewports and both languages, locally before merge and against the live site after every deployment." },
  { name = "Supervision", text = "Majordomus health check on every commit and the finish contract on every push; a task closes only when its verification command passes." },
  { name = "Evidence freshness", text = "A scheduled weekly run repeats the ledger and Crossref checks and opens an evidence-update issue when anything has expired." },
]
+++
