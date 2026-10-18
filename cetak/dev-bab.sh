#!/usr/bin/env bash
# Pratinjau cepat satu bab untuk iterasi gaya:
#   ./cetak/dev-bab.sh ch04-01-what-is-ownership
set -euo pipefail
cd "$(dirname "$0")/.."
id="${1:?beri id file bab, mis. ch04-01-what-is-ownership}"

mdbook build >/dev/null
python3 cetak/ekstrak-print.py --satu "$id"
(
  cd cetak/build
  pandoc -f html -t typst --wrap=none --resource-path=../../book \
    --extract-media=media --lua-filter=../hilangkan-tautan.lua \
    bab-dev.html -o bab-dev.typ
)
python3 cetak/lepas-figure.py bab-dev
sed -i 's/font-family="Times,serif"/font-family="Liberation Serif"/g' \
  cetak/build/media/img/*.svg
mkdir -p cetak/keluaran
typst compile --root cetak --font-path cetak/fonts cetak/pratinjau-bab.typ "cetak/keluaran/bab-dev-$id.pdf"
echo "Selesai: cetak/keluaran/bab-dev-$id.pdf"
