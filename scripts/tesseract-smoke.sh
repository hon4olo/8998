#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/tesseract-env.sh
mkdir -p out reviews
# Fresh document at each run, current outputs are technical test artifacts.
if [[ -f out/native-smoke.tsrct ]]; then mv -f out/native-smoke.tsrct out/native-previous.tsrct; fi
"$TSRCT" project create --project out/native-smoke.tsrct
"$TSRCT" project checkout --project out/native-smoke.tsrct --output out/native-editable.json
python3 - <<'PY'
import json
p=json.load(open('out/native-editable.json'));p['dimensions']={'width':640,'height':360};p['duration']=2;p['backgroundColor']=[.03,.06,.1,1];json.dump(p,open('out/native-editable.json','w'),indent=2)
PY
"$TSRCT" project commit --project out/native-smoke.tsrct --file out/native-editable.json
"$TSRCT" project import-font --project out/native-smoke.tsrct --file assets/fonts/DejaVuSans.ttf
python3 scripts/native-project.py
"$TSRCT" project apply --project out/native-smoke.tsrct --actions out/native-actions.json
"$TSRCT" preview --project out/native-smoke.tsrct --time 1 --output out/native-preview.png
"$TSRCT" filmstrip --project out/native-smoke.tsrct --start-ms 0 --duration-ms 2000 --interval-ms 250 --output reviews/native-filmstrip.png
python3 scripts/benchmark.py --out reviews/native-benchmark.json -- "$TSRCT" export --project out/native-smoke.tsrct --resolution 720p --fps 30 --encoder-backend external-ffmpeg-command --ffmpeg-path "$(command -v ffmpeg)" --output out/native-smoke.mp4
"$TSRCT" project checkout --project out/native-smoke.tsrct --output out/native-editable.json
ffprobe -v error -show_streams -show_format -of json out/native-smoke.mp4 > reviews/native-ffprobe.json
