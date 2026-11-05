#!/usr/bin/env bash
set -euo pipefail
VER="${1:-0.1.0}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${2:-$ROOT/..}/NEVEXONA-2.1-GAMING-DEV-$VER.zip"
cd "$ROOT"
rm -f "$OUT"
zip -r "$OUT" . -x ".git/*" "build/*" "*.iso" "*.zip" "*.log" ".env" "*.key" "*.pem" "__pycache__/*" >/dev/null
unzip -tq "$OUT"
echo "$OUT"
