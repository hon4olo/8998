#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[[ "$(uname -s)-$(uname -m)" == Linux-x86_64 ]] || { echo 'Unsupported host (requires Linux x86_64)'; exit 1; }
python3 - <<'PY'
import platform
assert tuple(map(int,platform.libc_ver()[1].split('.'))) >= (2,35),'glibc 2.35+ required'
PY
version="$(tr -d '\r\n' < skills/tesseract-video/references/cli-version.txt)"
[[ "$version" == "0.3.1" ]] || { echo 'Skill pin changed: review and update installation explicitly'; exit 1; }
mkdir -p .runtime/downloads .runtime/mesa
archive="tesseract-$version-linux-x86_64.zip"
base="https://github.com/mirage-hq/tesseract/releases/download/v$version"
if [[ ! -f .runtime/downloads/$archive ]]; then curl -fL "$base/$archive" -o ".runtime/downloads/$archive"; fi
curl -fL "$base/$archive.sha256" -o ".runtime/downloads/$archive.sha256"
(cd .runtime/downloads && sha256sum -c "$archive.sha256" && sha256sum -c ../../scripts/tesseract.sha256)
unzip -qo ".runtime/downloads/$archive" -d .runtime/downloads
bash ".runtime/downloads/tesseract-$version-linux-x86_64/install.sh" > .runtime/tesseract-install.log
# Debian 13 Mesa 25.0.7, llvm19 dependency: extract locally when root package install is unavailable.
mesa=mesa-vulkan-drivers_25.0.7-2+deb13u1_amd64.deb
curl -fL "https://deb.debian.org/debian/pool/main/m/mesa/$mesa" -o ".runtime/downloads/$mesa"
# SHA is frozen from the tested official Debian binary, checked before extraction.
(cd .runtime/downloads && sha256sum -c ../../scripts/mesa.sha256)
dpkg-deb -x ".runtime/downloads/$mesa" .runtime/mesa
if ldd .runtime/mesa/usr/lib/x86_64-linux-gnu/libvulkan_lvp.so | grep -q 'not found'; then
 ldd .runtime/mesa/usr/lib/x86_64-linux-gnu/libvulkan_lvp.so
 echo 'Missing Mesa dependencies: on Debian 13 install libllvm19, libdrm2, libzstd1, libvulkan1, libasound2t64, zlib1g, libstdc++6'; exit 1
fi
source scripts/tesseract-env.sh
"$TSRCT" --version | tee .runtime/tesseract-version.txt
rg -q 'tsrct 0.3.1' .runtime/tesseract-version.txt
