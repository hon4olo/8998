#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Non-root Debian user-space installation; no credentials are read or stored.
command -v node; command -v python3; command -v ffmpeg; command -v curl; command -v unzip
npm ci
python3 -m pip install -r requirements.txt
npx playwright install chromium
bash scripts/install-tesseract.sh
bash scripts/startup-checks.sh
