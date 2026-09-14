#!/usr/bin/env bash
# Serves a production build under the same repository subpath GitHub Pages uses,
# so base-path mistakes fail locally instead of in production.
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-4173}"
SUBPATH="${SUBPATH:-catharsis-as-a-service}"
OUT=".preview"

rm -rf "$OUT"
mkdir -p "$OUT"
npm run --silent assets
python3 scripts/generate-study-pages.py > /dev/null
zola build --base-url "http://127.0.0.1:$PORT/$SUBPATH" --output-dir "$OUT/$SUBPATH" --force
python3 scripts/export-api.py --out "$OUT/$SUBPATH" --base-url "http://127.0.0.1:$PORT/$SUBPATH"
echo "preview: http://127.0.0.1:$PORT/$SUBPATH/"
exec python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$OUT"
