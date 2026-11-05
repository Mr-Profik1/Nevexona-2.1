#!/usr/bin/env bash
# Сборка NEVEXONA CORE ISO. Запускать от root в Debian trixie (или контейнере).
# ВНИМАНИЕ: параметры lb config ещё не проверены реальной сборкой.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${WORK:-$ROOT/build}"
mkdir -p "$WORK" && cd "$WORK"
lb clean --purge || true
lb config \
  --distribution trixie \
  --architectures amd64 \
  --archive-areas "main contrib non-free non-free-firmware" \
  --binary-image iso-hybrid \
  --bootloaders "grub-pc,grub-efi" \
  --debian-installer none \
  --iso-application "NEVEXONA" \
  --iso-volume "NEVEXONA_CORE" \
  --linux-flavours amd64 \
  --bootappend-live "boot=live components quiet splash"
mkdir -p config/package-lists
cp "$ROOT"/config/package-lists/*.list.chroot config/package-lists/
lb build 2>&1 | tee "$WORK/build.log"
ls -lh ./*.iso
(sha256sum ./*.iso > SHA256SUMS) && cat SHA256SUMS
