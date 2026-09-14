#!/usr/bin/env bash
# Production smoke test: every entry point and first-party asset of the live site answers as expected.
# usage: scripts/smoke-production.sh <live-base-url>
set -euo pipefail

BASE="${1:?usage: smoke-production.sh <live-base-url>}"
BASE="${BASE%/}/"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
FAILED=0

row() {
  printf '%s %s %s\n' "$1" "$(printf '%*s' $((26 - ${#1})) '' | tr ' ' '.')" "$2"
}

fetch() {
  curl -sS -o "$2" -w '%{http_code}' --retry 4 --retry-delay 5 --retry-connrefused "$1" || echo 000
}

check() {
  local label="$1" url="$2" expect="${3:-200}" code
  code="$(fetch "$url" "$TMP/body")"
  row "$label" "$code"
  if [[ "$code" != "$expect" ]]; then
    echo "  expected $expect: $url" >&2
    FAILED=1
  fi
}

expect_lang() {
  if ! grep -Eq "<html[^>]*lang=\"?$2([\" >])" "$1"; then
    echo "  $3 is not lang=$2" >&2
    FAILED=1
  fi
}

echo "PRODUCTION SMOKE TEST  $BASE"
echo "────────────────────────────"

code="$(fetch "$BASE" "$TMP/home.html")"
row "/" "$code"
[[ "$code" == 200 ]] || FAILED=1
expect_lang "$TMP/home.html" en /

check "/cs/" "${BASE}cs/"
expect_lang "$TMP/body" cs /cs/
check "/about/" "${BASE}about/"
check "/cs/about/" "${BASE}cs/about/"
check "/guides/" "${BASE}guides/"
check "/cs/guides/" "${BASE}cs/guides/"
check "/artifacts/" "${BASE}artifacts/"
check "/artifacts/…/" "${BASE}artifacts/catharsis-as-a-service/"
check "poster master" "${BASE}assets/catharsis-as-a-service.png"
check "social preview en" "${BASE}assets/social-preview.png"
check "social preview cs" "${BASE}assets/social-preview.cs.png"
check "favicon.ico" "${BASE}favicon.ico"
check "favicon.svg" "${BASE}assets/favicon.svg"
check "icon 192" "${BASE}assets/icon-192.png"
check "atom feed en" "${BASE}atom.xml"
check "atom feed cs" "${BASE}cs/atom.xml"
check "/research/" "${BASE}research/"
check "/advice/" "${BASE}advice/"
check "/commands/" "${BASE}commands/"
check "/tags/" "${BASE}tags/"
check "/methods/" "${BASE}methods/"
check "/cs/methods/" "${BASE}cs/methods/"
check "/evidence/" "${BASE}evidence/"
check "/cs/evidence/" "${BASE}cs/evidence/"
check "/glossary/" "${BASE}glossary/"
check "/cs/slovnik/" "${BASE}cs/slovnik/"
check "/status/" "${BASE}status/"
check "/research/music-…/" "${BASE}research/music-and-emotion-regulation/"
check "api index" "${BASE}api/v1/index.json"
check "api advice cs" "${BASE}api/v1/advice.cs.json"
check "manifest" "${BASE}site.webmanifest"
check "fonts" "${BASE}fonts/fonts.css"
check "robots" "${BASE}robots.txt"
check "sitemap" "${BASE}sitemap.xml"

# Cache-busted and processed assets, discovered from the live home page itself.
while IFS=$'\t' read -r label url; do
  check "$label" "$url"
done < <(python3 - "$BASE" "$TMP/home.html" <<'PY'
import re
import sys

base, path = sys.argv[1], sys.argv[2]
html = open(path, encoding="utf-8").read()
refs = re.findall(r"""(?:href|src)=["']?([^"' >]+)""", html)
for srcset in re.findall(r"""srcset=["']([^"']+)["']""", html):
    refs.extend(part.strip().split(" ")[0] for part in srcset.split(","))
wanted = {
    "css/app.css": "css",
    "js/locale.js": "js locale",
    "js/app.js": "js app",
    "js/vendor/alpine.min.js": "js alpine",
    "js/vendor/flowbite.min.js": "js flowbite",
    "processed_images/": "poster webp",
}
seen, found = set(), set()
for ref in refs:
    if not ref.startswith(base):
        continue
    clean = ref[len(base):].split("?")[0].split("#")[0]
    for prefix, label in wanted.items():
        if clean.startswith(prefix) and clean not in seen:
            seen.add(clean)
            found.add(label)
            print(f"{label}\t{ref}")
for label in sorted(set(wanted.values()) - found):
    print(f"{label}\tmissing-from-home-page")
PY
)

code="$(fetch "${BASE}__state-transition-failed__/" "$TMP/404.html")"
row "404 route" "$code"
if [[ "$code" != 404 ]] || ! grep -qi 'state transition failed' "$TMP/404.html"; then
  echo "  unknown routes must return 404 with the bespoke page" >&2
  FAILED=1
fi

echo
if [[ "$FAILED" == 0 ]]; then
  echo PASS
else
  echo FAIL
  exit 1
fi
