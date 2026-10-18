# Pipeline Cetak (Tahap 6)

Membangun PDF cetak B5 (176 × 250 mm) dari `src/` lewat output mdBook.

Keputusan (2026-10-17, lihat `ROADMAP.md`):
- Ukuran B5 (bukan A5) agar baris kode muat; font isi 10 pt IBM Plex
  Serif, kode 8,5 pt IBM Plex Mono.
- Tata letak per 2026-10-18 (umpan balik pemeriksaan visual pengguna):
  margin buku dengan sisi dalam lebih lebar untuk ruang jilid
  (dalam 22 mm, luar 15 mm, atas 18 mm, bawah 20 mm); judul bab
  (heading level 1) rata tengah dan selalu memulai halaman baru.
- Mesin: Pandoc (konversi) + Typst (tata letak); XeLaTeX cadangan.
- Dua jilid: Jilid 1 = Kata Pengantar, Pendahuluan, Bab 1-12;
  Jilid 2 = Bab 13-21 + Lampiran. Titik potong di `BATAS_JILID`
  (`cetak/ekstrak-print.py`), disesuaikan bila ketebalan jilid timpang.
- Daftar isi otomatis oleh Typst (`outline`) dengan nomor halaman.

Susunan buku cetak (poin 3, 2026-10-18):
sampul → halaman judul → hak cipta/atribusi/lisensi → kata pengantar
penerjemah → kata pengantar penulis asli (foreword) → panduan membaca →
daftar isi → pendahuluan → bab-bab → lampiran → glosarium Inggris–Indonesia
→ referensi dan sumber daring → indeks istilah → profil penerjemah →
informasi edisi & kanal koreksi. Materi baru ini HANYA ada di buku cetak
(ditulis di `cetak/materi/*.md`); situs mdBook tidak berubah.
**Kedua jilid dibuat lengkap** (keputusan 2026-10-18): bagian awal dan
belakang diulang di jilid 1 dan 2, sehingga tiap jilid berdiri sendiri.

## Alur

```
mdbook build ──► book/print.html ──► ekstrak-print.py ──► 5 fragmen HTML
  ──► pandoc (+ hilangkan-tautan.lua) ──► file .typ + materi/*.md ──►
  lepas-figure.py ──► template.typ ──► typst compile pass 1 ──►
  typst eval (peta heading→halaman) ──► buat-materi.py indeks ──►
  typst compile pass 2 ──► keluaran/*.pdf
```

- `ekstrak-print.py` memotong `<main>` print.html per `<h1>` (judul bab
  sintetis mdBook, urut sesuai `src/SUMMARY.md`), membuang `title-page`,
  membuang h1 duplikat sub-bab, dan membersihkan markup tautan.
  Keluaran: `foreword`, `pendahuluan`, `jilid-1`, `jilid-2`, `lampiran`.
- `hilangkan-tautan.lua` mengubah tautan internal (`#anchor`) jadi teks
  polos — label antar-jilid tidak ada di dokumen yang sama.
- `lepas-figure.py` membuka pembungkus `#figure` pandoc (lihat seksi
  "Blok kode dan tabel").
- Font `cetak/fonts/` (Liberation Serif, lisensi SIL OFL): dipakai untuk
  teks di dalam diagram SVG (aslinya `Times,serif` yang tidak terpasang;
  Liberation Serif metriknya identik dengan Times New Roman sehingga label
  di dalam kotak diagram tidak meluber). `konversi.sh` menyalin media lewat
  pandoc lalu mengganti `font-family="Times,serif"` pada SVG hasil ekstrak;
  Typst dijalankan dengan `--font-path cetak/fonts`.
- `buat-materi.py`:
  - `glosarium` merangkai glosarium dari tabel glosarium `CLAUDE.md` +
    log istilah `ROADMAP.md` + pemetaan `revert_istilah.py`.
  - `indeks-scan` memindai fragmen .typ untuk kemunculan istilah glosarium
    (di luar blok kode dan heading), mencatat heading terdekat.
  - `indeks-rakit` menggabungkannya dengan peta heading→halaman dari
    `typst eval` menjadi `indeks.typ` (maks. 15 rujukan per istilah).
- Kompilasi dua pass: pass 1 memakai stub `= Indeks Istilah` supaya daftar
  isi pass 1 == pass 2; halaman sebelum indeks tidak bergeser karena indeks
  ditempel paling belakang jilid 2.
- `template.typ` — `gaya()` berisi semua aturan tampilan; `dokumen()`
  menyusun satu jilid lengkap; `pratinjau()` untuk mode dev.
- Blok kode ditangani paket **codly** (`@preview/codly:2.0.0`): baris
  panjang dilipat dengan penanda `↪` tanpa mengubah teks sumber; zebra,
  nomor baris, dan badge bahasa dimatikan; `leading: 1.5pt` merapatkan
  jarak antar-baris (bawaan codly 0.32em per sisi).

## Blok kode dan tabel (lepas-figure.py)

Pandoc membungkus listing (blok kode + caption) dengan `#figure(...)` dan
tabel dengan `#figure(align(center)[#table(...)], kind: table)`. Figure
Typst tidak bisa pecah lintas halaman, sehingga listing/tabel yang lebih
tinggi dari sisa halaman dipaksa muat satu halaman: bagian bawah terpotong
dan caption menimpa nomor halaman. `lepas-figure.py` (dipanggil setelah
pandoc) mengubahnya:

- Figure listing → `#block(breakable: true)[...]` dengan caption
  `#caption[...] <cap-listing-N-M>` di dalam blok yang sama, sehingga blok
  tinggi pecah lintas halaman dan caption mengikuti potongan terakhir.
- Figure tabel → `#table(...)` polos; tabel Typst 0.13+ pecah lintas
  halaman dan `table.header` berulang otomatis di tiap sambungan.
- Figure gambar (`#figure(image(...), caption: [...])`, mis. bab 17) →
  gambar + paragraf `#caption[...] <cap-gambar-N-M>`.
- Paragraf caption Gambar/Tabel → `#caption[...] <cap-tabel-N-M>` (gaya:
  rata tengah, 9 pt).
- Gambar SVG tanpa ukuran bawaan dirender Typst selebar viewBox (jauh
  melebihi kolom teks). Lebar diatur lewat peta `LEBAR_GAMBAR` (lebar kolom
  394 pt; ikon Ferris 70 pt; assert menolak gambar baru yang belum dipetakan).

Label `cap-*` dipakai `periksa.py` untuk memeriksa halaman caption secara
terprogram.

## Pemakaian

```bash
./cetak/konversi.sh                          # build penuh dua jilid
./cetak/dev-bab.sh ch04-01-what-is-ownership # pratinjau satu bab (~10 dtk)
```

Hasil di `cetak/keluaran/`; `cetak/build/` dan `cetak/keluaran/` tidak
di-commit (`.gitignore`).

## Pemeriksaan terprogram

- Halaman bab: `typst eval 'query(heading.where(level: 1)).map(h =>
  (h.body, h.location().page()))' --in cetak/jilid-1.typ` (peta bab).
- `python3 cetak/periksa.py` — per jilid: jumlah halaman, ukuran & halaman
  tiap gambar (tidak boleh melebihi kolom teks), tinggi & halaman tiap blok
  kode (yang > 1 halaman harus pecah, bukan terpotong), tabel yang pecah,
  dan halaman tiap label caption.
- `grep -ao "/Count [0-9]*"` pada PDF memberi jumlah halaman (tanpa poppler).
- Peringatan kompilasi Typst muncul di stderr `konversi.sh`.
