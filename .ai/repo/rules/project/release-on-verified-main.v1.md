---
id: project.release-on-verified-main
version: 1
kind: rule
title: Every verified push to main is released
description: Conventional Commits are mandatory because they compute the version of the release cut after each verified deployment.
statement: Every commit subject follows Conventional Commits, and every push to main that passes validate, deploy and verify produces a GitHub Release whose version is derived from those commits.
status: active
class: blocking
depends_on: []
tags: [release, git]
---

# Rationale

Releasing often is only safe when it is automatic and gated; the commit history is the changelog and the
version input, so its format is part of the build.

# Required behaviour

- Commit subjects match `type(scope): description` (`scripts/lint-commits.sh`); the `commit-msg` hook and CI both run it.
- Versions come from `scripts/release.sh`: breaking → major (minor while 0.x), `feat` → minor, otherwise patch.
- Tags `v*` are created by the pipeline only and never moved or deleted.
- Never force-push `main`; the repository ruleset blocks it.

# Failure behaviour

A non-conventional subject fails the `Conventional commits` job and nothing deploys. A failed verify job means no release.

# Verification

`scripts/lint-commits.sh <range>`; the `Release` job of the `Pages` workflow.
