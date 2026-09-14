#!/usr/bin/env bash
# Re-renders the committed artwork from artwork/ sources: poster master (4800×7200 @ 300 DPI),
# one social preview per locale (1200×630) and the icon set (favicon.ico, 192, 512, apple-touch).
# Needs Google Chrome and ImageMagick; run it by hand when artwork/ changes and commit the outputs.
set -euo pipefail
cd "$(dirname "$0")/.."

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
LOCALES="$(python3 -c 'import tomllib; print(" ".join(tomllib.load(open("zola.toml", "rb"))["extra"]["locales"]))')"
DEFAULT_LOCALE="$(python3 -c 'import tomllib; print(tomllib.load(open("zola.toml", "rb"))["default_language"])')"

preview_for() {
  if [[ "$1" == "$DEFAULT_LOCALE" ]]; then
    echo static/assets/social-preview.png
  else
    echo "static/assets/social-preview.$1.png"
  fi
}

# --check: verify sources and committed outputs without rendering anything.
if [[ "${1:-}" == "--check" ]]; then
  missing=0
  expected=(artwork/poster.html artwork/social.html static/assets/favicon.svg static/assets/catharsis-as-a-service.png
    artwork/closure/poster.html static/assets/closure-as-a-service.png static/favicon.ico static/assets/apple-touch-icon.png static/assets/icon-192.png static/assets/icon-512.png)
  for code in $LOCALES; do
    expected+=("$(preview_for "$code")")
  done
  for file in "${expected[@]}"; do
    if [[ -s "$file" ]]; then
      echo "ok      $file"
    else
      echo "missing $file"
      missing=1
    fi
  done
  exit "$missing"
fi

render() {
  local source="$1" size="$2" scale="$3" output="$4"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size="$size" \
    --force-device-scale-factor="$scale" --virtual-time-budget=12000 \
    --screenshot="$PWD/$output" "file://$PWD/$source" >/dev/null 2>&1
}

render "artwork/poster.html?print" 1200,1800 4 static/assets/catharsis-as-a-service.png
magick static/assets/catharsis-as-a-service.png -strip -units PixelsPerInch -density 300 \
  -define png:include-chunk=pHYs static/assets/catharsis-as-a-service.png

render "artwork/closure/poster.html?print" 1200,1800 4 static/assets/closure-as-a-service.png
# ImageMagick 7.1.2 drops pHYs after -strip unless the chunk is requested explicitly.
magick static/assets/closure-as-a-service.png -strip -units PixelsPerInch -density 300 \
  -define png:include-chunk=pHYs static/assets/closure-as-a-service.png

for code in $LOCALES; do
  output="$(preview_for "$code")"
  render "artwork/social.html?lang=$code" 1200,630 1 "$output"
  magick "$output" -strip "$output"
done

SVG=static/assets/favicon.svg
magick -background none -density 384 "$SVG" -define icon:auto-resize=48,32,16 static/favicon.ico
magick -background none -density 384 "$SVG" -resize 180x180 -strip static/assets/apple-touch-icon.png
magick -background none -density 384 "$SVG" -resize 192x192 -strip static/assets/icon-192.png
magick -background none -density 768 "$SVG" -resize 512x512 -strip static/assets/icon-512.png

magick identify -format '%f %wx%h %B bytes\n' static/assets/*.png static/favicon.ico
