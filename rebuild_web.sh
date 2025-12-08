#!/usr/bin/env bash
set -euo pipefail

# remove previous web build and cache
rm -rf build/web build/web-cache

# ensure build folders exist so pygbag can cache template/icon and write cartofia-game.html
mkdir -p build/web build/web-cache

# pre-seed cache from local archives if available to avoid CDN flakiness
if [ -f build/web/archives/0.9/default.tmpl ]; then
  cp build/web/archives/0.9/default.tmpl build/web-cache/489f66f53e526d7110d2d34527229eca.tmpl || true
fi
if [ -f build/web/archives/0.9/favicon.png ]; then
  cp build/web/archives/0.9/favicon.png build/web-cache/38e02d124325c756243ee99a92e528ed.png || true
fi

# rebuild
PYTHON_BIN="${PYTHON:-python}"
$PYTHON_BIN -m pygbag --build --html --title Cartofia main.py

echo "Fresh build ready in build/web/"
