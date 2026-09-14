#!/usr/bin/env bash
# Cuts a GitHub Release for every verified deployment of main.
# Version bump from Conventional Commits since the last tag:
#   breaking (type! or BREAKING CHANGE) -> major (minor while 0.x) · feat -> minor · anything else -> patch
# usage: GH_TOKEN=... scripts/release.sh [--dry-run]
set -euo pipefail
cd "$(dirname "$0")/.."

DRY_RUN="${1:-}"
PAGE_URL="${PAGE_URL:-$(gh api "repos/${GITHUB_REPOSITORY:-korczis/catharsis-as-a-service}/pages" --jq .html_url 2>/dev/null || true)}"

git fetch --tags --force --quiet
last="$(git describe --tags --abbrev=0 --match 'v[0-9]*.[0-9]*.[0-9]*' 2>/dev/null || true)"
range="${last:+$last..}HEAD"

if [[ -z "$(git log --format=%H "$range")" ]]; then
  echo "release: no commits since $last, nothing to release"
  exit 0
fi

subjects="$(git log --format=%s "$range")"
bump=patch
if git log --format=%B "$range" | grep -qE '^BREAKING[ -]CHANGE:' || grep -qE '^[a-z]+(\([^)]+\))?!:' <<<"$subjects"; then
  bump=major
elif grep -qE '^feat(\([^)]+\))?:' <<<"$subjects"; then
  bump=minor
fi

current="${last#v}"
IFS=. read -r major minor patch <<<"${current:-0.0.0}"
case "$bump" in
  major)
    if [[ "$major" == 0 ]]; then
      minor=$((minor + 1)); patch=0
    else
      major=$((major + 1)); minor=0; patch=0
    fi
    ;;
  minor) minor=$((minor + 1)); patch=0 ;;
  patch) patch=$((patch + 1)) ;;
esac
next="v$major.$minor.$patch"

notes="$(mktemp)"
trap 'rm -f "$notes"' EXIT
{
  echo "Deployed and verified: ${PAGE_URL:-GitHub Pages}"
  if [[ -n "${GITHUB_RUN_ID:-}" ]]; then
    echo "Pipeline: ${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"
  fi
  echo
  echo "## Changes (${last:-initial}..$(git rev-parse --short HEAD), $bump)"
  echo
  git log --format='- %s (%h)' "$range"
} > "$notes"

echo "release: ${last:-none} -> $next ($bump)"
if [[ "$DRY_RUN" == "--dry-run" ]]; then
  cat "$notes"
  exit 0
fi

gh release create "$next" \
  --target "$(git rev-parse HEAD)" \
  --title "$next" \
  --notes-file "$notes" \
  static/assets/catharsis-as-a-service.png \
  static/assets/social-preview.png
