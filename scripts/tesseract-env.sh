#!/usr/bin/env bash
ZNAYA_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export TSRCT="${XDG_DATA_HOME:-$HOME/.local/share}/Tesseract/bin/tsrct"
if [[ -f "$ZNAYA_ROOT/.runtime/mesa/usr/share/vulkan/icd.d/lvp_icd.json" ]]; then
 export VK_ICD_FILENAMES="$ZNAYA_ROOT/.runtime/mesa/usr/share/vulkan/icd.d/lvp_icd.json"
 export LD_LIBRARY_PATH="$ZNAYA_ROOT/.runtime/mesa/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-$ZNAYA_ROOT/.runtime/xdg}"
mkdir -p "$XDG_RUNTIME_DIR"; chmod 700 "$XDG_RUNTIME_DIR"
