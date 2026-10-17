#!/usr/bin/env bash
# Pipeline cetak: mdbook build -> ekstrak print.html -> pandoc -> typst -> PDF.
# Dipanggil dari akar repo: ./cetak/konversi.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== mdbook build"
mdbook build >/dev/null

echo "== ekstrak print.html"
python3 cetak/ekstrak-print.py

echo "== pandoc html -> typst"
# Dijalankan dari cetak/build supaya referensi media di .typ relatif
# terhadap lokasi file output (media/...), bukan terhadap akar repo.
(
  cd cetak/build
  for nama in depan jilid-1 jilid-2 lampiran; do
    pandoc -f html -t typst --wrap=none --resource-path=../../book \
      --extract-media=media \
      --lua-filter=../hilangkan-tautan.lua \
      "$nama.html" -o "$nama.typ"
  done
)

echo "== typst compile"
mkdir -p cetak/keluaran
typst compile --root cetak cetak/jilid-1.typ cetak/keluaran/rust-book-id-jilid-1.pdf
typst compile --root cetak cetak/jilid-2.typ cetak/keluaran/rust-book-id-jilid-2.pdf

echo "Selesai:"
ls -la cetak/keluaran/
