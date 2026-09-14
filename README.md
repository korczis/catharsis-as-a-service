# CATHARSIS AS A SERVICE™

Festival poster that sells euphoria at first glance and diagnoses it at second.
PRISMATIC × SIG NIHL.

- Live: https://korczis.github.io/catharsis-as-a-service/
- Print file: `catharsis-as-a-service.png` (4800×7200 px, 300 DPI → 16×24 in)

## Structure

- `index.html` — the poster as inline SVG: typography, telemetry overlay and waveforms are vector.
- `bg.jpg` — stage/crowd photo layer, upscaled 4× and posterized.
- `?print` query hides page chrome for rendering.

## Render

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
  --window-size=1200,1800 --force-device-scale-factor=4 --virtual-time-budget=10000 \
  --screenshot="$PWD/catharsis-as-a-service.png" "file://$PWD/index.html?print"
magick catharsis-as-a-service.png -density 300 -units PixelsPerInch catharsis-as-a-service.png
```
