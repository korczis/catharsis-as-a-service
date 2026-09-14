#!/usr/bin/env bash
# Tailwind in watch mode next to `zola serve`; both stop together.
set -euo pipefail
cd "$(dirname "$0")/.."

npm run --silent vendor
python3 scripts/generate-study-pages.py > /dev/null
python3 scripts/generate-term-pages.py > /dev/null
npx tailwindcss --input styles/app.css --output static/css/app.css --watch=always &
CSS_PID=$!
trap 'kill "$CSS_PID" 2>/dev/null || true' EXIT

until [[ -s static/css/app.css ]]; do
  sleep 0.2
done
zola serve "$@"
