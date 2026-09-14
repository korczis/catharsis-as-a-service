#!/usr/bin/env bash
# Single validation entry point for local runs and CI. Every step must pass; the first failure stops the run.
set -euo pipefail
cd "$(dirname "$0")/.."

BASE_URL="${BASE_URL:-$(python3 -c 'import tomllib; print(tomllib.load(open("zola.toml", "rb"))["base_url"])')}"
REQUIRED_ZOLA="$(tr -d '[:space:]' < .zola-version)"
# Build metadata for the footer and /status/. Derived from the commit, so a rebuild is reproducible.
export CAAS_VERSION="${CAAS_VERSION:-$(git describe --tags --always 2>/dev/null || echo unreleased)}"
export CAAS_COMMITTED="${CAAS_COMMITTED:-$(git log -1 --format=%cs 2>/dev/null || echo local)}"
RESULTS=()

dots() {
  printf '%*s' $((20 - ${#1})) '' | tr ' ' '.'
}

report() {
  printf '\nVALIDATION\n────────────────────\n'
  local entry
  for entry in "${RESULTS[@]}"; do
    printf '%s %s %s\n' "${entry%%|*}" "$(dots "${entry%%|*}")" "${entry##*|}"
  done
}

step() {
  local name="$1"
  shift
  printf '\n── %s: %s\n' "$name" "$*"
  if "$@"; then
    RESULTS+=("$name|PASS")
  else
    RESULTS+=("$name|FAIL")
    report
    printf '\nRESULT %s FAIL\n' "$(dots RESULT)"
    exit 1
  fi
}

zola_version() {
  local actual
  actual="$(zola --version | awk '{print $2}')"
  if [[ "$actual" != "$REQUIRED_ZOLA" ]]; then
    echo "zola $REQUIRED_ZOLA is required (.zola-version), found $actual" >&2
    return 1
  fi
  echo "zola $actual"
}

js_syntax() {
  local file
  for file in static/js/app.js static/js/locale.js static/js/url-state.js static/js/models.js static/js/search.js static/js/case-study.js; do
    node --check "$file" || return 1
  done
}

step toolchain zola_version
step assets npm run --silent assets
step studies python3 scripts/generate-study-pages.py
step javascript js_syntax
step i18n python3 scripts/validate-i18n.py
step content python3 scripts/validate-content.py
step references python3 scripts/check-references.py
step claims python3 scripts/validate-claims.py
step case-study python3 scripts/export-case-study.py --check
step social python3 scripts/render-social.py --check
step zola-check zola check --skip-external-links
step zola-build zola build --base-url "$BASE_URL"
step api python3 scripts/export-api.py --out public --base-url "$BASE_URL"
step html python3 scripts/validate-html.py public "$BASE_URL"

report
printf '\nRESULT %s PASS\n' "$(dots RESULT)"
