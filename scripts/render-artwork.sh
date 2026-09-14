#!/usr/bin/env bash
# Re-renders the committed artwork from artwork/ sources: poster master (4800×7200 @ 300 DPI),
# one social preview per locale (1200×630) and the icon set (favicon.ico, 192, 512, apple-touch).
# Needs Google Chrome and ImageMagick; run it by hand when artwork/ changes and commit the outputs.
set -euo pipefail
cd "$(dirname "$0")/.."

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
LOCALES="$(python3 -c 'import tomllib; print(" ".join(tomllib.load(open("zola.toml", "rb"))["extra"]["locales"]))')"
DEFAULT_LOCALE="$(python3 -c 'import tomllib; print(tomllib.load(open("zola.toml", "rb"))["default_language"])')"

render() {
  local source="$1" size="$2" scale="$3" output="$4"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size="$size" \
    --force-device-scale-factor="$scale" --virtual-time-budget=12000 \
    --screenshot="$PWD/$output" "file://$PWD/$source" >/dev/null 2>&1
}

render "artwork/poster.html?print" 1200,1800 4 static/assets/catharsis-as-a-service.png
magick static/assets/catharsis-as-a-service.png -strip -units PixelsPerInch -density 300 \
  static/assets/catharsis-as-a-service.png

for code in $LOCALES; do
  if [[ "$code" == "$DEFAULT_LOCALE" ]]; then
    output=static/assets/social-preview.png
  else
    output="static/assets/social-preview.$code.png"
  fi
  render "artwork/social.html?lang=$code" 1200,630 1 "$output"
  magick "$output" -strip "$output"
done

SVG=static/assets/favicon.svg
magick -background none -density 384 "$SVG" -define icon:auto-resize=48,32,16 static/favicon.ico
magick -background none -density 384 "$SVG" -resize 180x180 -strip static/assets/apple-touch-icon.png
magick -background none -density 384 "$SVG" -resize 192x192 -strip static/assets/icon-192.png
magick -background none -density 768 "$SVG" -resize 512x512 -strip static/assets/icon-512.png

magick identify -format '%f %wx%h %B bytes\n' static/assets/*.png static/favicon.ico
