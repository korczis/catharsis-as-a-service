#!/usr/bin/env bash
# Re-renders the committed artwork from artwork/ sources: poster master (4800×7200 @ 300 DPI),
# social preview (1200×630) and PNG icons. Needs Google Chrome and ImageMagick; run it by hand
# when artwork/ changes and commit the outputs.
set -euo pipefail
cd "$(dirname "$0")/.."

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"

render() {
  local source="$1" size="$2" scale="$3" output="$4"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size="$size" \
    --force-device-scale-factor="$scale" --virtual-time-budget=12000 \
    --screenshot="$PWD/$output" "file://$PWD/$source" >/dev/null 2>&1
}

render "artwork/poster.html?print" 1200,1800 4 static/assets/catharsis-as-a-service.png
magick static/assets/catharsis-as-a-service.png -strip -units PixelsPerInch -density 300 \
  static/assets/catharsis-as-a-service.png

render "artwork/social.html" 1200,630 1 static/assets/social-preview.png
magick static/assets/social-preview.png -strip static/assets/social-preview.png

magick -background none -density 768 static/assets/favicon.svg -resize 512x512 -strip static/assets/icon-512.png
magick -background none -density 384 static/assets/favicon.svg -resize 180x180 -strip static/assets/apple-touch-icon.png

magick identify -format '%f %wx%h %B bytes\n' static/assets/catharsis-as-a-service.png \
  static/assets/social-preview.png static/assets/icon-512.png static/assets/apple-touch-icon.png
