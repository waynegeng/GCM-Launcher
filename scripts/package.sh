#!/usr/bin/env bash
# Build frontend and produce a Decky plugin zip at gcm-launcher/out/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -d dist ]; then
  echo "dist/ missing; run 'pnpm run build' first" >&2
  exit 1
fi

mkdir -p out
rm -rf out/package
mkdir -p out/package
PLUGIN_FOLDER=out/package/GCM-Launcher
mkdir -p "$PLUGIN_FOLDER"
cp -r dist main.py plugin.json package.json "$PLUGIN_FOLDER/"
cp -r py_modules "$PLUGIN_FOLDER/"
find out/package -type d -name __pycache__ -prune -exec rm -rf {} +
rm -f out/gcm-launcher.zip
(
  cd out/package
  zip -qr ../gcm-launcher.zip GCM-Launcher
)
echo "plugin zip: $ROOT/out/gcm-launcher.zip"
