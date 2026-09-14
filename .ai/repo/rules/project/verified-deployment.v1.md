---
id: project.verified-deployment
version: 1
kind: rule
title: Deployment is claimed only after live verification
description: Nothing is reported as deployed, working or released until the live GitHub Pages URL has been checked.
statement: A deployment is complete only when the Pages workflow's verify job has passed against the live URL returned by GitHub, and a release is cut only after that job.
status: active
class: blocking
depends_on: []
tags: [deployment, verification]
---

# Rationale

A green build says the source compiles. It says nothing about the repository subpath, the CDN, the
Pages configuration or the browser. Only the live URL answers those.

# Required behaviour

- The production URL is read from GitHub (`gh api repos/<owner>/<repo>/pages --jq .html_url`), never guessed.
- `zola.toml` `base_url` equals that URL; the deploy job asserts it before deploying.
- `scripts/smoke-production.sh` and `tests/site.spec.js` pass against the live URL before a release exists.
- Validation is never bypassed to make CI pass: no `|| true` around a mandatory check, no `--no-verify`.

# Failure behaviour

A failing verify job means the change is not deployed in any sense a report may claim. Diagnose, fix,
push, and let the pipeline run again.

# Verification

Reviewer-owned. Evidence is the `Pages` workflow run: `deploy`, `verify` and `release` all green for the commit.
