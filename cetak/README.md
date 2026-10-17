# Pipeline Cetak (Tahap 6)

Membangun PDF cetak B5 (176 × 250 mm) dari `src/` lewat output mdBook.

Keputusan (2026-10-17, lihat `ROADMAP.md`):
- Ukuran B5 (bukan A5) agar baris kode muat; margin 18/20 mm, font isi
  10 pt IBM Plex Serif, kode 8,5 pt IBM Plex Mono.
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

## Alur

```
mdbook build ──► book/print.html ──► ekstrak-print.py ──► 5 fragmen HTML
  ──► pandoc (+ hilangkan-tautan.lua) ──► file .typ + materi/*.md ──►
  template.typ ──► typst compile pass 1 ──► typst eval (peta heading→halaman)
  ──► buat-materi.py indeks ──► typst compile pass 2 ──► keluaran/*.pdf
```

- `ekstrak-print.py` memotong `<main>` print.html per `<h1>` (judul bab
  sintetis mdBook, urut sesuai `src/SUMMARY.md`), membuang `title-page`,
  membuang h1 duplikat sub-bab, dan membersihkan markup tautan.
  Keluaran: `foreword`, `pendahuluan`, `jilid-1`, `jilid-2`, `lampiran`.
- `hilangkan-tautan.lua` mengubah tautan internal (`#anchor`) jadi teks
  polos — label antar-jilid tidak ada di dokumen yang sama.
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
  nomor baris, dan badge bahasa dimatikan.

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
- `grep -ao "/Count [0-9]*"` pada PDF memberi jumlah halaman (tanpa poppler).
- Peringatan kompilasi Typst muncul di stderr `konversi.sh`.
