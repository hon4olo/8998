#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
node --version; python3 --version; ffmpeg -version | head -1
ffmpeg -hide_banner -encoders 2>/dev/null | rg 'libx264| AAC | aac '
npx tsc
npx tsx --test tests/startup.test.ts
source scripts/tesseract-env.sh
"$TSRCT" --version | rg 'tsrct 0.3.1'
# CLI version is not proof of renderer support. Verify actual Vulkan image rendering.
mkdir -p .runtime
ZNAYA_CHECK_DIR="$(mktemp -d "$PWD/.runtime/check-XXXXXX")"
trap 'rm -rf "$ZNAYA_CHECK_DIR"' EXIT
"$TSRCT" project create --project "$ZNAYA_CHECK_DIR/startup.tsrct"
"$TSRCT" preview --project "$ZNAYA_CHECK_DIR/startup.tsrct" --time 0 --output .runtime/startup.png
python3 - <<'PY'
from PIL import Image
im=Image.open('.runtime/startup.png');assert im.size==(1080,1920);print('Native Vulkan render passed',im.size)
PY
