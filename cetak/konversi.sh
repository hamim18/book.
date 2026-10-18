#!/usr/bin/env bash
# Pipeline cetak: mdbook build -> ekstrak print.html -> pandoc -> typst -> PDF.
# Dipanggil dari akar repo: ./cetak/konversi.sh
# Dua pass kompilasi: pass 1 untuk peta heading->halaman, lalu indeks
# istilah dibangkitkan, lalu pass 2 (halaman sebelum indeks tidak bergeser
# karena indeks ditempel paling belakang; heading stub-nya sudah ada di
# pass 1 sehingga daftar isi pun tidak berubah).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== mdbook build"
mdbook build >/dev/null

echo "== ekstrak print.html"
python3 cetak/ekstrak-print.py

echo "== materi (glosarium, langsung .typ)"
python3 cetak/buat-materi.py glosarium

echo "== pandoc html/markdown -> typst"
# Dijalankan dari cetak/build supaya referensi media di .typ relatif
# terhadap lokasi file output (media/...), bukan terhadap akar repo.
(
  cd cetak/build
  for nama in foreword pendahuluan jilid-1 jilid-2 lampiran; do
    pandoc -f html -t typst --wrap=none --resource-path=../../book \
      --extract-media=media \
      --lua-filter=../hilangkan-tautan.lua \
      "$nama.html" -o "$nama.typ"
  done
  # indeks: stub heading dulu supaya daftar isi pass 1 == pass 2
  printf '= Indeks Istilah\n' > indeks.typ
  for nama in hak-cipta kata-pengantar-penerjemah panduan-membaca referensi profil info-edisi; do
    pandoc -f markdown -t typst --wrap=none \
      --lua-filter=../hilangkan-tautan.lua \
      "../materi/$nama.md" -o "$nama.typ"
  done
  # glosarium.typ ditulis langsung oleh buat-materi.py (tabel panjang
  # tidak boleh dibungkus #figure oleh pandoc).
)

echo "== lepas pembungkus figure (listing & tabel)"
python3 cetak/lepas-figure.py
# Diagram SVG meminta font Times yang tidak terpasang; ganti ke Liberation
# Serif (metrik identik dengan Times New Roman, dipasok di cetak/fonts/)
# supaya label di dalam kotak diagram tidak meluber.
sed -i 's/font-family="Times,serif"/font-family="Liberation Serif"/g' \
  cetak/build/media/img/*.svg

echo "== typst compile pass 1"
mkdir -p cetak/keluaran
for nama in jilid-1 jilid-2 ebook-1 ebook-2; do
  typst compile --root cetak --font-path cetak/fonts \
    "cetak/$nama.typ" "cetak/keluaran/rust-book-id-$nama.pdf"
done

echo "== peta heading -> halaman"
typst eval 'query(heading).map(h => (h.level, h.body, h.location().page()))' \
  --in cetak/jilid-1.typ --font-path cetak/fonts > cetak/build/halaman-1.json
typst eval 'query(heading).map(h => (h.level, h.body, h.location().page()))' \
  --in cetak/jilid-2.typ --font-path cetak/fonts > cetak/build/halaman-2.json

echo "== indeks istilah"
python3 cetak/buat-materi.py indeks-scan
python3 cetak/buat-materi.py indeks-rakit

echo "== typst compile pass 2"
# E-book: paginasi identik dengan cetak (lebar area teks sama), jadi
# indeks istilah dari pass cetak tetap sah untuk kedua versi.
for nama in jilid-1 jilid-2 ebook-1 ebook-2; do
  typst compile --root cetak --font-path cetak/fonts \
    "cetak/$nama.typ" "cetak/keluaran/rust-book-id-$nama.pdf"
done

echo "== sampul sablon (percetakan, bleed 3 mm)"
for j in 1 2; do
  typst compile --root cetak --font-path cetak/fonts \
    "cetak/sablon-jilid-$j.typ" "cetak/keluaran/sampul-sablon-jilid-$j.pdf"
done

echo "Selesai:"
ls -la cetak/keluaran/
