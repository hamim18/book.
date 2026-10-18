# Roadmap Penerjemahan The Rust Programming Language ke Bahasa Indonesia

Sumber kebenaran status file: `python3 cek_terjemahan.py --progres`.
File ini memuat urutan kerja, log istilah, dan masalah terbuka.
Diperbarui di akhir setiap sesi.

## Status terkini

- Tahap 4 selesai — Pendahuluan (`title-page.md`, `foreword.md`, `SUMMARY.md`)
  diterjemahkan dan lulus `cek_terjemahan.py`. **Semua 112 file selesai,
  0 galat.** `mdbook test` lulus (exit 0).
- Tahap 5 (pemeriksaan menyeluruh) **selesai** (menunggu dua keputusan istilah,
  lihat Masalah terbuka):
  - **Anchor internal**: 70 tag `<a id>` kompatibilitas ditambahkan di 41
    file tujuan; pemindaian ~290 tautan internal ber-anchor kini 0 rusak.
    Dua tautan stale (ch17-05 → ch17-03#working-with-any-number-of-futures
    dan ch17-06 → ch17-04#composing-streams) dibiarkan: keduanya definisi
    tautan mati yang tidak pernah dipakai di prosa. Commit `0324fd6`.
  - **Review kedua** (seluruh buku, 17 agen pembanding `asli/` ↔ `src/`
    dalam 2 gelombang): tidak ada pergeseran makna berarti; ±50 catatan
    kecil diperbaiki; kerusakan markup warisan sesi penerjemahan (asterisk
    di dalam span/blok kode, label tautan `[*X*]`, asterisk di tengah kata)
    dibersihkan. Commit `24bd8b8` dan `30de8a7`.
  - **Konsistensi istilah**: "command line" → "baris perintah" (ch11-02);
    "di Appendix C" → "di Lampiran C" (ch04-01); "kami" → "kita" (52
    kemunculan); header tabel appendix-02 Symbol/Context → Simbol/Konteks;
    "nilai hardcoded" → "nilai yang ditulis langsung (hardcoded)";
    "resource" → "sumber daya".
  - **Konvensi miring**: atas keputusan pengguna, istilah teknis Inggris
    dimiringkan pada SETIAP kemunculan di prosa (≈4.400 kemunculan, 97
    file), termasuk istilah berkapital di awal kalimat; heading, kode,
    tautan, komentar HTML, dan judul karya dikecualikan.
  - `cek_terjemahan.py` 97 file OK; `mdbook build` tanpa tautan rusak;
    `mdbook test` exit 0.
- Tahap 6 (cetak) dimulai 2026-10-17:
  - **Keputusan**: B5 ISO 176 × 250 mm, bukan A5 (di A5 satu baris hanya
    muat ±55 karakter kode, sementara 353 baris listing lebih dari 76
    karakter); mesin Pandoc + Typst (XeLaTeX cadangan); font IBM Plex
    (isi Serif 10 pt, kode Mono 8,5 pt).
  - **Pipeline** di `cetak/` (folder baru; tidak menyentuh folder
    terlarang): `mdbook build` → `ekstrak-print.py` memotong
    `book/print.html` per bab (buang h1 duplikat sub-bab, buang
    title-page, bersihkan tautan) → pandoc HTML→Typst
    (`hilangkan-tautan.lua`: tautan internal jadi teks polos; kotak
    catatan jadi `#catatan[...]`) → `template.typ`.
  - **Fitur**: daftar isi otomatis dengan nomor halaman; nomor "Bab N" /
    "N.M" otomatis (offset 12 di jilid 2); kotak catatan; blok kode paket
    codly — baris panjang dilipat bertanda ↪ tanpa mengubah teks sumber,
    tanpa nomor baris/badge bahasa.
  - **Hasil build**: jilid 1 (kata pengantar + pendahuluan + bab 1-12)
    429 halaman; jilid 2 (bab 13-21 + lampiran) 445 halaman.
  - **Mode dev**: `./cetak/dev-bab.sh ch04-01-...` mengompilasi satu bab
    ±10 detik untuk iterasi gaya.
  - Menunggu pemeriksaan visual pengguna; pratinjau PNG halaman terpilih
    di `cetak/keluaran/`.
- **Selesai 2026-10-18 — poin 1 (tata letak cetak, umpan balik pemeriksaan
  visual pengguna)**: margin buku B5 dengan sisi dalam 22 mm untuk ruang
  jilid (luar 15, atas 18, bawah 20); judul bab (h1) rata tengah; jarak
  antar-baris kode dirapatkan (codly `leading: 1.5pt`, bawaan 0.32em/sisi);
  kalimat "tidak diperjualbelikan" dihapus dari kata pengantar penerjemah
  dan info edisi. Pembungkus `#figure` pandoc dibuka oleh
  `cetak/lepas-figure.py` (listing → blok breakable dengan caption di
  dalamnya; tabel → tabel polos yang bisa pecah lintas halaman; gambar
  diberi lebar kolom 394 pt, ikon Ferris 70 pt). Font Liberation Serif
  ditambahkan di `cetak/fonts/` dan dipakai untuk teks diagram SVG
  (aslinya `Times,serif` yang tidak terpasang sehingga label meluber keluar
  kotak). Verifikasi terprogram `cetak/periksa.py`: 0 gambar melebihi
  kolom; 0 caption menembus batas bawah area teks; blok kode > 1 halaman
  (8 di j1, 27 di j2) pecah lintas halaman; Tabel B-1 pecah 2 halaman.
  Hasil: jilid 1 = 442 hal., jilid 2 = 436 hal. Pratinjau PNG halaman yang
  diperbaiki di `cetak/keluaran/pratinjau-j{1,2}-*.png`.
- **Selesai 2026-10-18 — persetujuan pemeriksaan visual putaran kedua
  pengguna ("sudah sangat bagus, siap cetak")**: titik potong jilid final
  dikunci — **Jilid 1 = 442 hal., Jilid 2 = 436 hal.** PDF final dibangun
  ulang (`./cetak/konversi.sh`; PDF lama di `cetak/keluaran/` ternyata
  belum memuat perbaikan poin 1) lalu diverifikasi penuh dengan
  `cetak/periksa.py`: 22 gambar, 0 melebihi kolom teks; 978 blok kode,
  35 pecah lintas halaman (bukan terpotong); 26 tabel, 4 pecah; 431 label
  caption. **Tahap 6 selesai.** Opsi .docx tetap terbuka bila diminta.
- **Sampul pengguna diintegrasikan (2026-10-18)**: desain sampul depan dan
  belakang dibuat pengguna di luar Claude Code (PNG B5 300 DPI 2079×2953
  full-bleed + SVG sumber, keduanya di `cetak/desain-sampul/`; desain
  kustom — Jilid 1 teal gelap #1E4D4A, Jilid 2 merah-karat #6E2A1D,
  ilustrasi kepiting khas). **PNG dipakai di build** (persis seperti yang
  diverifikasi pengguna; SVG hanya beda 0,55% piksel tepi saat dirender
  Typst, disimpan sebagai sumber edit). `template.typ` kini menerima
  `sampul-depan`/`sampul-belakang` (gambar full-bleed, halaman pertama dan
  terakhir; sampul teks lama dipertahankan sebagai cadangan bila parameter
  kosong); `periksa.py` mengecualikan gambar sampul dari batas kolom;
  atribusi maskot (Dave Gandy, CC BY 4.0) ditambahkan ke `hak-cipta.md`.
  Jumlah halaman berubah: **Jilid 1 = 443 hal., Jilid 2 = 437 hal.**
  (menggantikan 442/436). `periksa.py` lulus: 0 gambar melebihi kolom,
  semua blok kode pecah lintas halaman. Masih terbuka: lembar sampul
  menyebar (belakang–punggung–depan) dengan bleed 3 mm untuk percetakan.
- **Versi e-book + perbaikan teks sampul (2026-10-18)**: (1) teks
  "pengumpul sampah" di sinopsis sampul belakang diganti "garbage
  collector" — file PNG/SVG sampul diperbarui langsung oleh pengguna di
  `cetak/desain-sampul/` (pendekatan tempelan teks Typst dicoba lalu
  dibatalkan karena hanya menyembunyikan teks lama); (2) versi e-book
  ditambahkan: `cetak/ebook-1.typ` dan `ebook-2.typ` dengan margin
  kiri-kanan sama (`x: 18,5 mm`) dan lebar area teks sama dengan cetak
  (139 mm) sehingga paginasi — dan nomor halaman indeks istilah — tidak
  berubah; `template.typ` kini menerima parameter `margin`; `konversi.sh`
  membangun 4 PDF (jilid-1, jilid-2, ebook-1, ebook-2), semuanya
  443/437 hal.
- **Poin 3 (susunan buku lengkap) dimulai 2026-10-18**: materi baru HANYA di
  buku cetak (`cetak/materi/*.md` + `cetak/buat-materi.py`); situs mdBook
  tidak berubah. Urutan per jilid: sampul → halaman judul → hak
  cipta/atribusi/lisensi → kata pengantar penerjemah → kata pengantar
  penulis asli → panduan membaca → daftar isi → pendahuluan → bab →
  lampiran → glosarium Inggris–Indonesia (±650 entri, dibangkitkan dari
  tabel glosarium CLAUDE.md + log istilah ROADMAP + pemetaan
  `revert_istilah.py`) → referensi dan sumber daring → indeks istilah
  (seksi + halaman, dibangkitkan dua-pass lewat `typst eval`; maks. 15
  rujukan per istilah) → profil penerjemah → informasi edisi & kanal
  koreksi. **Kedua jilid dibuat lengkap** (keputusan 2026-10-18): bagian
  awal dan belakang diulang di jilid 1 dan 2 agar tiap jilid berdiri
  sendiri. Nama penerjemah: "AI" (keputusan pengguna 2026-10-18);
  profil/kata pengantar/info edisi diisi asisten. `ekstrak-print.py` kini
  memisahkan `foreword` dan `pendahuluan`; daftar isi otomatis tetap ada
  di tiap jilid.
- **Kebijakan istilah 2026-10-17 (disetujui pengguna, dikerjakan tuntas)**: semua
  istilah teknis glosarium kembali ditulis dalam bahasa Inggris di prosa
  (±4.500 pergantian di seluruh `src/`, 8 commit: `0b3de5d` s/d `93d07ae`).
  Kata pinjaman umum polos (error, variable, method, type, loop, test, ...),
  istilah yang sudah miring tetap miring (*compiler*, *ownership*, ...).
  "galat" diganti "error" polos; "penanganan galat" → "penanganan error";
  padanan dalam kurung yang sudah ada dipertahankan; padanan lengkap akan
  disusun sebagai glosarium Inggris–Indonesia di akhir buku (poin 3).
  `cek_terjemahan.py` 112/112 OK, `mdbook build` tanpa peringatan,
  `mdbook test` exit 0. Detail per istilah: lihat Log keputusan istilah.
- Terakhir diperbarui: 2026-10-18

## Urutan kerja

- [x] Tahap 0 — Snapshot `asli/` + commit baseline (`siapkan asli/ dan perangkat terjemahan`)
- [x] Tahap 1 — Bab 4 sebagai uji coba gaya & istilah: `ch04-00` … `ch04-03`
- [x] Tahap 2 — Urut dari awal buku: `ch00` → `ch01` → … → `ch21`.
      Per bab: terjemah semua file → `cek_terjemahan.py` per file → commit per bab
      (`terjemah: bab NN <judul>`). Jalankan `mdbook test` (lihat Catatan teknis)
      setiap beberapa bab. (`foreword.md` dipindah ke Tahap 4, bersama kelompok
      Pendahuluan.)
- [x] Tahap 3 — `appendix-00` s/d `appendix-07`
- [x] Tahap 4 — `title-page.md` + `foreword.md` + `SUMMARY.md` (judul bab
      diterjemahkan, path tetap; label SUMMARY mengikuti heading final tiap bab).
- [x] Tahap 5 — Pemeriksaan menyeluruh: review kedua (banding `asli/` ↔ `src/`),
      `mdbook test` (lihat Catatan teknis), `mdbook build` (tautan anchor rusak
      karena heading diterjemahkan), konsistensi istilah antar-bab. Selesai
      2026-10-17; dua keputusan istilah menunggu konfirmasi (lihat Masalah
      terbuka).
- [x] Tahap 6 — Cetak B5 ISO 176 × 250 mm, mesin Pandoc + Typst (keputusan
      2026-10-17: A5 diganti B5 agar baris kode muat tanpa terpotong; Typst
      dipilih karena cepat, ringan, dan Unicode-native, XeLaTeX cadangan;
      lihat Tahap 8 `PANDUAN_PROMPT.md`). Selesai 2026-10-18: dua jilid
      final dikunci (J1 442 hal. / J2 436 hal.) dan disetujui pengguna.

## Ukuran kerja per kelompok (kata, dari `asli/`)

File tunggal terbesar (>3.500 kata, butuh beberapa sesi): `ch02-00` (6.028),
`ch21-02` (5.136), `ch10-03` (4.633), `ch17-05` (4.366), `ch19-03` (4.366),
`ch20-01` (4.348), `ch18-03` (4.320), `ch04-01` (4.160), `ch09-02` (4.103).

| Kelompok | File | Kata |
|---|---:|---:|
| Pendahuluan (title-page, foreword, SUMMARY) | 3 | 1.199 |
| Bab 00 | 1 | 1.601 |
| Bab 01 | 4 | 4.039 |
| Bab 02 | 1 | 6.028 |
| Bab 03 | 6 | 8.322 |
| Bab 04 | 4 | 7.749 |
| Bab 05 | 4 | 5.687 |
| Bab 06 | 4 | 5.560 |
| Bab 07 | 6 | 7.348 |
| Bab 08 | 4 | 6.608 |
| Bab 09 | 4 | 7.781 |
| Bab 10 | 4 | 10.498 |
| Bab 11 | 4 | 7.036 |
| Bab 12 | 7 | 8.943 |
| Bab 13 | 5 | 6.557 |
| Bab 14 | 6 | 6.139 |
| Bab 15 | 7 | 12.641 |
| Bab 16 | 5 | 6.947 |
| Bab 17 | 7 | 15.407 |
| Bab 18 | 4 | 7.699 |
| Bab 19 | 4 | 6.937 |
| Bab 20 | 6 | 14.604 |
| Bab 21 | 4 | 10.497 |
| Appendix | 8 | 7.001 |
| **TOTAL** | **112** | **±183.000** |

## Catatan teknis

- `mdbook test` butuh crate `trpl` (dipakai contoh-contoh bab 17) yang dibangun
  dulu, lalu path-nya diteruskan:
  ```bash
  cargo build --locked --manifest-path packages/trpl/Cargo.toml
  mdbook test --library-path packages/trpl/target/debug/deps
  ```
  Tanpa ini, semua contoh bab 17 gagal dengan `can't find crate for trpl`.
- Batas edit sesuai `CLAUDE.md`: hanya `src/` yang diterjemahkan;
  `listings/`, `packages/`, `book.toml`, dll. tidak disentuh. Diperkuat
  deny rules di `.claude/settings.json` (Read/Edit/Write pada folder
  terlarang; `asli/` tetap boleh dibaca untuk review kedua).
- Titik buta `cek_terjemahan.py` (diketahui di Tahap 5; belum diperbaiki
  karena skrip berada di luar `src/`): (1) blok kode yang fence-nya
  berawalan `> ` (di dalam blockquote) tidak terdeteksi sebagai blok kode
  sehingga isinya tidak dibandingkan dengan asli; (2) inline code span
  (backtick, termasuk yang lintas-baris) tidak dibandingkan dengan asli,
  sehingga markup miring yang terselip di dalamnya tidak tertangkap. Kedua
  hal ini pernah rusak (warisan sesi penerjemahan) dan sudah dibersihkan
  manual di Tahap 5; jika skrip diperbaiki nanti, tambahkan dua pemeriksaan
  tersebut.

## Tabel progres

<!-- Refresh tiap sesi: tempel output `python3 cek_terjemahan.py --progres`
     (bagian tabel ringkasnya) di bawah baris ini. -->

| Kelompok    | Selesai | Galat | Belum | Total |
|-------------|--------:|------:|------:|------:|
| Pendahuluan |       3 |     0 |     0 |     3 |
| Bab 00      |       1 |     0 |     0 |     1 |
| Bab 01      |       4 |     0 |     0 |     4 |
| Bab 02      |       1 |     0 |     0 |     1 |
| Bab 03      |       6 |     0 |     0 |     6 |
| Bab 04      |       4 |     0 |     0 |     4 |
| Bab 05      |       4 |     0 |     0 |     4 |
| Bab 06      |       4 |     0 |     0 |     4 |
| Bab 07      |       6 |     0 |     0 |     6 |
| Bab 08      |       4 |     0 |     0 |     4 |
| Bab 09      |       4 |     0 |     0 |     4 |
| Bab 10      |       4 |     0 |     0 |     4 |
| Bab 11      |       4 |     0 |     0 |     4 |
| Bab 12      |       7 |     0 |     0 |     7 |
| Bab 13      |       5 |     0 |     0 |     5 |
| Bab 14      |       6 |     0 |     0 |     6 |
| Bab 15      |       7 |     0 |     0 |     7 |
| Bab 16      |       5 |     0 |     0 |     5 |
| Bab 17      |       7 |     0 |     0 |     7 |
| Bab 18      |       4 |     0 |     0 |     4 |
| Bab 19      |       4 |     0 |     0 |     4 |
| Bab 20      |       6 |     0 |     0 |     6 |
| Bab 21      |       4 |     0 |     0 |     4 |
| Appendix    |       8 |     0 |     0 |     8 |
| TOTAL       |     112 |     0 |     0 |   112 |

## Log keputusan istilah

Istilah baru di luar tabel glosarium `CLAUDE.md`. Setelah disetujui pengguna,
masukkan juga ke tabel glosarium di `CLAUDE.md`.

| Istilah | Padanan | Bab |
|---|---|---|
| pointer | penunjuk | 04 |
| memory allocator / allocator | pengalokasi memori (tetap miring) | 04 |
| allocation / allocating on the heap | alokasi / mengalokasikan di heap | 04 |
| garbage collector (GC) / garbage collection | pengumpul sampah / pengumpulan sampah | 04 |
| owner | pemilik | 04 |
| string literal | (tetap) | 04 |
| runtime | (tetap) | 04 |
| shallow copy / deep copy | salinan dangkal / salinan dalam | 04 |
| double free | (tetap) | 04 |
| namespace | ruang nama | 04 |
| standard library | pustaka standar | 04 |
| signature (fungsi) | tanda tangan | 04 |
| floating point | titik mengambang | 04 |
| tuple | (tetap, miring) | 04 |
| assignment / assign | penetapan / menetapkan | 04 |
| method | metode (tanpa miring) | 04 |
| collection | koleksi (tanpa miring) | 04 |
| pattern | pola (tanpa miring) | 04 |
| loop | perulangan (tanpa miring) | 04 |
| vector | vektor (tanpa miring) | 04 |
| dereferencing | dereferensi | 04 |
| deref coercion | (tetap) | 04 |
| data race / race condition | (tetap) | 04 |
| dangling pointer / dangling reference | pointer menggantung / reference menggantung | 04 |
| undefined behavior | perilaku tak terdefinisi | 04 |
| error (error message, error-handling) | galat (pesan galat, penanganan galat) | 00 |
| bug | (tetap, tanpa miring) | 00 |
| dependency / dependency manager | dependensi / pengelola dependensi (tanpa miring) | 00 |
| tool / tooling | alat / perangkat (tanpa miring) | 00 |
| build (build tool) | (tetap, tanpa miring; "alat build") | 00 |
| open source | (tetap, tanpa miring) | 00 |
| panic | (tetap, tanpa miring) | 00 |
| refactoring | (tetap, tanpa miring) | 00 |
| zero-cost abstraction | *zero-cost abstraction* (abstraksi tanpa biaya) | 00 |
| thread | (tetap, tanpa miring) | 00 |
| async / await | (tetap, tanpa miring) | 00 |
| task / future / stream | (tetap, miring) | 00 |
| concurrency / concurrent | konkurensi / konkuren (tanpa miring) | 00 |
| control flow | alur kontrol (tanpa miring) | 00 |
| hash map | (tetap, tanpa miring) | 00 |
| programmer | pemrogram | 00 |
| web browser / web server | peramban web / server web | 00 |
| machine learning | pembelajaran mesin | 00 |
| linker | (tetap, miring) | 01 |
| script | skrip | 01 |
| shell | (tetap, tanpa miring) | 01 |
| native | (tetap, tanpa miring) | 01 |
| cache | (tetap, tanpa miring) | 01 |
| flag | (tetap, tanpa miring) | 01 |
| installer | (tetap, tanpa miring) | 01 |
| optimization | optimasi | 01 |
| benchmarking | benchmark (tetap, tanpa miring) | 01 |
| version control system | sistem kontrol versi | 01 |
| build (verba) | membangun | 01 |
| "Filename:" (label <span>) | "Nama File:" | 01 |
| offline | luring | 01 |
| source file | file sumber | 01 |
| variable | variabel (tanpa miring) | 02 |
| associated function | *associated function* (fungsi asosiasi) | 02 |
| enumeration | *enumeration* (enumerasi) | 02 |
| variant | *variant* (varian) | 02 |
| arm (match arm) | *arm* (lengan) | 02 |
| prelude | (tetap, miring) | 02 |
| instance | (tetap, tanpa miring) | 02 |
| handle | (tetap, tanpa miring) | 02 |
| placeholder | (tetap, tanpa miring) | 02 |
| crash | (tetap, tanpa miring) | 02 |
| registry | *registry* (registri) | 02 |
| range | (tetap, tanpa miring) | 02 |
| seed (seeded) | di-seed | 02 |
| source control | kontrol sumber | 02 |
| input/output | masukan/keluaran | 02 |
| random number generator | pembangkit angka acak | 02 |
| type inference | inferensi tipe | 02 |
| unsigned | tak bertanda | 02 |
| whitespace | spasi | 02 |
| newline | (tetap, tanpa miring) | 02 |
| shadowing | (tetap, miring) | 02 |
| guess / secret number | tebakan / angka rahasia | 02 |
| integer | (tetap, tanpa miring) | 02 |
| infinite loop | perulangan tak berujung | 02 |
| keyword | *keyword* (kata kunci) | 03 |
| data type | tipe data (tanpa miring) | 03 |
| statically typed | *statically typed* (bertipe statis) | 03 |
| scalar | skalar (tanpa miring) | 03 |
| signed | bertanda | 03 |
| literal (integer/number literal) | literal (tanpa miring) | 03 |
| integer overflow | (tetap, tanpa miring) | 03 |
| two's complement | komplemen dua | 03 |
| wrapping (two's complement wrapping) | pembungkusan | 03 |
| saturate | menjenuhkan | 03 |
| conditionals | kondisional | 03 |
| Unicode scalar value | nilai skalar Unicode | 03 |
| zero-width space | spasi lebar nol | 03 |
| compound type | tipe majemuk (tanpa miring) | 03 |
| destructuring | *destructuring* (destrukturisasi) | 03 |
| unit (unit type) | (tetap, miring) | 03 |
| array | (tetap, tanpa miring) | 03 |
| indexing | pengindeksan | 03 |
| memory safety | keamanan memori | 03 |
| low-level language | bahasa tingkat rendah | 03 |
| constant | konstanta (tanpa miring) | 03 |
| compile time / compile-time | waktu kompilasi | 03 |
| type annotation | anotasi tipe | 03 |
| hardcoded value | nilai yang ditulis langsung (hardcoded) | 03 |
| snake case | (tetap, miring) | 03 |
| entry point | titik masuk | 03 |
| parameter | parameter (tanpa miring) | 03 |
| argument | argumen (tanpa miring) | 03 |
| statement | pernyataan (tanpa miring) | 03 |
| expression | ekspresi (tanpa miring) | 03 |
| return value / return type | nilai kembalian / tipe kembalian | 03 |
| binary project | proyek binary | 03 |
| loop label | label perulangan | 03 |
| iteration | iterasi (tanpa miring) | 03 |
| machine code | kode mesin | 03 |
| error-prone | rawan galat | 03 |
| countdown | hitung mundur | 03 |
| keyboard shortcut | pintasan keyboard | 03 |
| interrupt signal | sinyal interupsi | 03 |
| format string | string format | 03 |
| mutability / immutability | (tetap, tanpa miring) | 03 |
| field | *field* (medan) | 05 |
| field init shorthand | (tetap, nama fitur) | 05 |
| struct update syntax | sintaks update struct | 05 |
| tuple struct | *tuple struct* (struct tuple) | 05 |
| unit-like struct | *unit-like struct* (struct mirip unit) | 05 |
| dot notation | notasi titik | 05 |
| template | templat | 05 |
| derive / derived traits | menurunkan / trait yang diturunkan | 05 |
| attribute | atribut (tanpa miring) | 05 |
| debug (verba) | men-debug | 05 |
| primitive type | tipe primitif | 05 |
| end user | pengguna akhir | 05 |
| specifier | penanda | 05 |
| standard error / standard output | (tetap, aliran konsol) | 05 |
| getter | (tetap, tanpa miring) | 05 |
| trait object | *trait object* (objek trait) | 05 |
| constructor | konstruktor | 05 |
| receiver | *receiver* (penerima) | 05 |
| automatic referencing and dereferencing | (tetap, miring; referensi dan dereferensi otomatis) | 05 |
| alias | alias | 05 |
| ergonomic | ergonomis | 05 |
| rectangle | persegi panjang | 05 |
| width / height | lebar / tinggi | 05 |
| null | (tetap, miring pada kemunculan pertama) | 06 |
| wildcard | (tetap) | 06 |
| catch-all | (tetap) | 06 |
| exhaustive / exhaustiveness | *exhaustive* (ekshaustif) / ekshaustivitas | 06 |
| quarter (koin) | (tetap, koin 25 sen) | 06 |
| syntax sugar | gula sintaks | 06 |
| boilerplate | (tetap) | 06 |
| happy path | (tetap, “happy path”) | 06 |
| enumerate (verba) | menyebutkan satu per satu | 06 |
| workspace | (tetap, tanpa miring) | 07 |
| crate root | *crate root* (akar crate) | 07 |
| crate binary / crate library | crate binary / crate library | 07 |
| module system | *module system* (sistem modul) | 07 |
| module tree | *module tree* (pohon modul) | 07 |
| sibling | *sibling* (saudara) | 07 |
| child / parent (module) | *child* (anak) / *parent* (induk) | 07 |
| front of house / back of house | *front of house* (area depan) / *back of house* (area belakang) | 07 |
| privacy | *privacy* (privasi) | 07 |
| path | (tetap, miring) | 07 |
| identifier | *identifier* (pengidentifikasi) | 07 |
| absolute path / relative path | *absolute path* (path absolut) / *relative path* (path relatif) | 07 |
| glob operator | operator *glob* | 07 |
| nested path | *nested path* (path bersarang) | 07 |
| re-exporting | *re-exporting* (mengekspor ulang) | 07 |
| idiomatic | idiomatis (tanpa miring) | 07 |
| symbolic link | tautan simbolik | 07 |
| submodule | (tetap, tanpa miring) | 07 |
| encapsulation | enkapsulasi | 07 |
| publik / privat | (tanpa miring) | 07 |
| map | *map* (tetap, miring) | 08 |
| key | kunci | 08 |
| dereference operator | operator dereferensi | 08 |
| drop (verba) / dropped | membebaskan / dibebaskan | 08 |
| spreadsheet | (tetap, tanpa miring) | 08 |
| hashing function | *hashing function* (fungsi hashing) | 08 |
| hash table | tabel hash | 08 |
| hasher | (tetap, miring) | 08 |
| concatenate / concatenation | menggabungkan / penggabungan | 08 |
| wrapper | *wrapper* (pembungkus) | 08 |
| coerce | mengoersi | 08 |
| grapheme cluster | *grapheme cluster* (klaster grafem) | 08 |
| diacritics | diakritik | 08 |
| Devanagari script | aksara Devanagari | 08 |
| denial-of-service (DoS) | (tetap) | 08 |
| homogeneous | homogen | 08 |
| median / mode | median / modus | 08 |
| consonant / vowel | konsonan / vokal | 08 |
| recoverable / unrecoverable error | galat yang dapat dipulihkan / tidak dapat dipulihkan | 09 |
| exception | (tetap, miring) | 09 |
| file not found | *file not found* (file tidak ditemukan) | 09 |
| unwinding | (tetap, miring) | 09 |
| aborting | *aborting* (pembatalan) | 09 |
| backtrace | (tetap, miring) | 09 |
| buffer overread | *buffer overread* (pembacaan buffer berlebih) | 09 |
| propagate (galat) | *propagating* (meneruskan) | 09 |
| question mark operator | operator tanda tanya | 09 |
| early return | return dini | 09 |
| bad state | *bad state* (keadaan yang buruk) | 09 |
| contract (fungsi) | kontrak | 09 |
| invariant | invarian | 09 |
| parser | (tetap, tanpa miring) | 09 |
| malformed | cacat | 09 |
| rate limit | batas laju (rate limit) | 09 |
| out-of-bounds | di luar batas | 09 |
| monomorphization | *monomorphization* (monomorfisasi) | 10 |
| trait bound | *trait bound* (batasan trait) | 10 |
| interface | *interface* (antarmuka) | 10 |
| coherence | *coherence* (koherensi) | 10 |
| orphan rule | *orphan rule* (aturan anak yatim) | 10 |
| blanket implementation | *blanket implementation* (implementasi menyeluruh) | 10 |
| lifetime elision rules | *lifetime elision rules* (aturan elision lifetime) | 10 |
| input lifetime / output lifetime | *input lifetime* (lifetime masukan) / *output lifetime* (lifetime keluaran) | 10 |
| dynamically typed | *dynamically typed* (bertipe dinamis) | 10 |
| default implementation | implementasi bawaan | 10 |
| Appendix (merujuk lampiran buku) | Lampiran | 10 |
| test / testing | pengujian (kemunculan pertama: *test* (pengujian)) | 11 |
| assert (verba) / assertion | menegaskan / asersi | 11 |
| unit tests / integration tests | pengujian unit / pengujian integrasi | 11 |
| documentation test | *documentation test* (test dokumentasi) | 11 |
| test runner / test harness / test suite | (tetap, tanpa miring) | 11 |
| filtering | *filtering* (penyaringan) | 11 |
| helper function | fungsi pembantu | 11 |
| environment variable | variabel lingkungan | 11 |
| coverage | cakupan | 11 |
| ancestor (modul) | leluhur | 11 |
| artifact (hasil kompilasi) | artefak | 11 |
| command line | baris perintah (catatan: ch11-02 masih memakai "command line", lihat Masalah terbuka) | 12 |
| query | kueri | 12 |
| case-insensitive / case-sensitive | (tetap, tanpa miring; kemunculan pertama: *case-insensitive* (tanpa membedakan huruf besar-kecil)) | 12 |
| parse / parsing / parser | (tetap, tanpa miring; verba di prosa: "melakukan parsing") | 12 |
| separation of concerns | pemisahan tanggung jawab | 12 |
| configuration variable | variabel konfigurasi | 12 |
| exit status / exit status code | status keluar / kode status keluar | 12 |
| user-friendly | ramah pengguna | 12 |
| anonymous function | fungsi anonim | 12 |
| vertical pipes | garis vertikal | 12 |
| side effects | efek samping | 12 |
| maintainer | pengelola | 12 |
| test-driven development (TDD) | *test-driven development* (TDD, pengembangan yang digerakkan oleh pengujian) | 12 |
| skeleton implementation | implementasi kerangka | 12 |
| casing (huruf besar-kecil) | kapitalisasi | 12 |
| lowercase (verba) / uppercase | mengubah menjadi huruf kecil / huruf kapital | 12 |
| take precedence | didahulukan | 12 |
| ampersand | ampersand (tetap) | 12 |
| Boolean | (tetap) | 12 |
| cmdlet | (tetap) | 12 |
| functional programming | pemrograman fungsional | 13 |
| capture (closure) / capturing | menangkap / penangkapan | 13 |
| environment (closure) | lingkungan | 13 |
| mailing list | milis | 13 |
| inventory | persediaan | 13 |
| T-shirt | kaos | 13 |
| lazy (iterator) | _lazy_ (malas) | 13 |
| consuming adapter | _consuming adapter_ (adapter yang mengonsumsi) | 13 |
| iterator adapter | _iterator adapter_ (tetap) | 13 |
| associated type | *associated type* (tipe asosiasi) | 13 |
| implementor | pengimplementasi | 13 |
| internal state | keadaan internal | 13 |
| behind the scenes / under the hood | di belakang layar / di balik layar | 13 |
| running total | total berjalan | 13 |
| chain (verba) | merantaikan | 13 |
| intermediate (vektor) | perantara | 13 |
| mutable state | keadaan mutable | 13 |
| in parallel | secara paralel | 13 |
| concurrent access | akses konkuren | 13 |
| spawn (thread) | membuat (thread baru) | 13 |
| zero-overhead | (tetap) | 13 |
| loop unrolling | (tetap, tanpa miring) | 13 |
| bounds checking | pemeriksaan batas | 13 |
| performance penalty | denda performa | 13 |
| expressiveness | ekspresivitas | 13 |
| shoe size | ukuran sepatu | 13 |
| release profile | *release profile* (profil rilis) | 14 |
| binary target | *binary target* (target binary) | 14 |
| members (workspace) | anggota | 14 |
| yank / yanking | menarik / penarikan | 14 |
| documentation comment / doc comment | *documentation comment* (komentar dokumentasi) / komentar dok | 14 |
| license identifier | *license identifier* (pengidentifikasi lisensi) | 14 |
| library (berdiri sendiri) | (tetap, tanpa miring; selaras "crate library" bab 07) | 14 |
| box | (tetap, miring; tanpa padanan) | 15 |
| recursive type | *recursive type* (tipe rekursif) | 15 |
| cons list | (tetap, miring) | 15 |
| linked list | *linked list* (senarai berantai) | 15 |
| reference counting | *reference counting* (penghitungan referensi) | 15 |
| reference cycle | reference cycle (siklus referensi) | 15 |
| interior mutability | *interior mutability* (mutabilitas internal) | 15 |
| indirection | *indirection* (indireksi) | 15 |
| dereference (verba) | melakukan dereferensi | 15 |
| memory leak | *memory leak* (kebocoran memori) | 15 |
| strong reference / weak reference | *strong reference* (reference kuat) / *weak reference* (reference lemah) | 15 |
| tree | *tree* (pohon) | 15 |
| node (graf/tree) | *node* (simpul) | 15 |
| graph / edge (graf) | graf / sisi | 15 |
| test double | *test double* (pengganti dalam pengujian) | 15 |
| mock object | *mock object* (objek tiruan) | 15 |
| destructor | *destructor* (destruktor) | 15 |
| socket | soket | 15 |
| single-threaded / multithreaded | (tetap) | 15 |
| clone (verba) | mengklon | 15 |
| stack overflow | luapan stack | 15 |
| thread-safe | (tetap) | 15 |
| concurrent programming / parallel programming | *concurrent programming* (pemrograman konkuren) / *parallel programming* (pemrograman paralel) | 16 |
| fearless concurrency | *fearless concurrency* (konkurensi tanpa takut) | 16 |
| process | *process* (proses) | 16 |
| deadlock | *deadlock* (kebuntuan) | 16 |
| blocking (thread) | *blocking* (pemblokiran) | 16 |
| channel | *channel* (saluran) | 16 |
| transmitter / receiver | *transmitter* (pengirim) / *receiver* (penerima) | 16 |
| message passing | *message passing* (pengiriman pesan) | 16 |
| shared-state / shared memory | *shared-state* (state bersama) / memori bersama | 16 |
| producer / consumer | produsen / konsumen | 16 |
| mutex / mutual exclusion | mutex (tetap) / *mutual exclusion* (eksklusi mutual) | 16 |
| lock (nomina/verba) | lock (kunci) / mengunci | 16 |
| unlock | membuka kunci | 16 |
| guard (mutex, verba) | menjaga | 16 |
| concurrency primitive | primitif konkurensi | 16 |
| counter | pencacah | 16 |
| atomic / atomics | *atomic* (atomik) / atomik | 16 |
| marker trait | *marker trait* (trait penanda) | 16 |
| raw pointer | *raw pointer* (pointer mentah) | 16 |
| thread safety | (tetap) | 16 |
| upstream / downstream | hulu / hilir | 16 |
| actor | aktor | 16 |
| asynchronous / asynchronous programming | asinkron / pemrograman asinkron (tanpa miring) | 17 |
| parallelism | paralelisme (tanpa miring) | 17 |
| CPU-bound / compute-bound / I/O-bound | _CPU-bound_ (terikat CPU) / _compute-bound_ (terikat komputasi) / _I/O-bound_ (terikat I/O) | 17 |
| non-blocking | _non_-blocking (tidak memblokir) | 17 |
| multitask (verba) | melakukan banyak tugas sekaligus | 17 |
| serial | serial (tanpa miring) | 17 |
| invisibly (interupsi OS) | secara tak terlihat | 17 |
| lock up (UI) | membuat macet | 17 |
| join handle | (tetap, tanpa miring) | 17 |
| fair / fairness | _fair_ (adil) / fairness | 17 |
| unbounded (channel) | tanpa batas | 17 |
| starvation / starving | kelaparan / membuat kelaparan | 17 |
| yield / yielding | menyerahkan kontrol | 17 |
| cooperative multitasking | _cooperative multitasking_ (multitasking kooperatif) | 17 |
| timer | _timer_ (pewaktu) | 17 |
| elapse (timeout) | habis (batas waktu habis) | 17 |
| interleaved / interleave | saling menyelang | 17 |
| handoff / hand off control | penyerahan / menyerahkan kontrol | 17 |
| building block | batu penyusun | 17 |
| compose (future) | menyusun | 17 |
| retries | percobaan ulang | 17 |
| bottleneck | hambatan | 17 |
| embedded (sistem operasi) | tertanam | 17 |
| batch up (events) | mengelompokkan | 17 |
| event | (tetap, tanpa miring) | 17 |
| throttle | membatasi laju | 17 |
| chunks (data) | potongan-potongan | 17 |
| extension (trait Ext) | _extension_ (ekstensi) | 17 |
| utility methods | metode utilitas | 17 |
| self-referential | mengacu ke diri sendiri | 17 |
| pin (verba) / pinning | mem-pin / pinning | 17 |
| web of references | jaringan reference | 17 |
| work stealing | _work stealing_ (pencurian pekerjaan) | 17 |
| fire and forget | “fire and forget” (dilepas dan dibiarkan) | 17 |
| rules of thumb | aturan praktis | 17 |
| parallelizable | dapat diparalelkan | 17 |
| granular | halus (satuan paling halus) | 17 |
| video encoding | pengodean video | 17 |
| OOP / object-oriented programming | pemrograman berorientasi objek (OOP) | 18 |
| coin (verba) | mencetuskan (istilah) | 18 |
| The Gang of Four | _The Gang of Four_ (Geng Empat) | 18 |
| inheritance | _inheritance_ (pewarisan) | 18 |
| parent class / child class | kelas induk / kelas anak | 18 |
| subclass | (tetap, tanpa miring) | 18 |
| polymorphism | _polymorphism_ (polimorfisme) | 18 |
| bounded parametric polymorphism | _bounded parametric polymorphism_ (polimorfisme parametrik terbatas) | 18 |
| single inheritance | _single inheritance_ (pewarisan tunggal) | 18 |
| reuse of code | pemakaian ulang kode | 18 |
| out of sync | tidak sinkron | 18 |
| on demand | setiap kali dibutuhkan | 18 |
| graphical user interface (GUI) | antarmuka pengguna grafis (GUI) | 18 |
| framework | (tetap, tanpa miring) | 18 |
| duck typing | _duck typing_ (pengetikan bebek) | 18 |
| quack | berkuek | 18 |
| static dispatch / dynamic dispatch | _static dispatch_ (dispatch statis) / _dynamic dispatch_ (dispatch dinamis) | 18 |
| dyn compatibility | _dyn compatibility_ (kompatibilitas dyn) | 18 |
| inline (verba) | meng-inline | 18 |
| stand-in | pengganti | 18 |
| fill in for | mengisi peran | 18 |
| workaround | jalan keluar | 18 |
| state pattern | _state pattern_ (pola state) | 18 |
| state object | _state object_ (objek state) | 18 |
| blog post | post blog | 18 |
| workflow | alur kerja | 18 |
| business requirements | persyaratan bisnis | 18 |
| coupled | saling terkait | 18 |
| lingering | tersisa | 18 |
| get around (batasan) | mengakali | 18 |
| in exchange for | dengan imbalan | 18 |
| maintainability | kemudahan pemeliharaan | 18 |
| blurring the lines | mengaburkan batas | 18 |
| refutability | refutabilitas | 19 |
| irrefutable / refutable | _irrefutable_ (tidak dapat dibantah) / _refutable_ (dapat dibantah) | 19 |
| bind (pola) | mengikat | 19 |
| match guard | _match guard_ (pengawal match) | 19 |
| inclusive range | rentang inklusif | 19 |
| shorthand (pola struct) | bentuk singkat | 19 |
| axis | sumbu | 19 |
| by virtue of | karena | 19 |
| prototype (verba) | membuat prototipe | 19 |
| unset (pengaturan) | menghapus nilai | 19 |
| customization | kustomisasi | 19 |
| setting | pengaturan | 19 |
| three-dimensional space | ruang tiga dimensi | 19 |
| unambiguous | tidak ambigu | 19 |
| precedence | prioritas | 19 |
| penultimate | kedua terakhir | 19 |
| remainder | sisa pembagian | 19 |
| hypothetical | hipotetis | 19 |
| one level deep | sedalam satu tingkat | 19 |
| superpowers (unsafe superpowers) | kekuatan super (unsafe) | 20 |
| opt out (verba) | memilih untuk tidak memakai | 20 |
| alter ego | alter ego (tetap) | 20 |
| static analysis | analisis statis | 20 |
| low-level systems programming | pemrograman sistem tingkat rendah | 20 |
| raw borrow operator | operator borrow mentah | 20 |
| cast (verba) | melakukan cast | 20 |
| segmentation fault | (tetap) | 20 |
| use case | kasus pemakaian | 20 |
| cleanup | pembersihan | 20 |
| union | *union* (tetap) | 20 |
| lint | lint (tanpa miring) | 20 |
| unsound | tidak sound (tetap) | 20 |
| mangling / name mangling | melakukan mangling / name mangling (tetap) | 20 |
| name collision | bentrokan nama | 20 |
| shared library | library bersama | 20 |
| Foreign Function Interface (FFI) | *Foreign Function Interface* (FFI, Antarmuka Fungsi Asing) | 20 |
| application binary interface (ABI) | *application binary interface* (ABI, antarmuka biner aplikasi) | 20 |
| assembly level | tingkat assembly | 20 |
| dynamic analysis | analisis dinamis | 20 |
| operator overloading | *operator overloading* (overload operator) | 20 |
| overload (verba) | meng-overload | 20 |
| default type parameter | *default type parameter* (parameter tipe bawaan) | 20 |
| fully qualified syntax | sintaks fully qualified (miring) | 20 |
| supertrait | supertrait (tetap, miring) | 20 |
| newtype pattern | *newtype pattern* (pola newtype) | 20 |
| disambiguate | mendisambiguasi | 20 |
| angle brackets | kurung sudut | 20 |
| right-hand side | sisi kanan | 20 |
| puppy | puppy (tetap) | 20 |
| animal shelter | penampungan hewan | 20 |
| delegate (verba) | mendelegasikan | 20 |
| elide (tipe wrapper) | menghilangkan (pada waktu kompilasi) | 20 |
| type synonym | sinonim tipe | 20 |
| type alias | *type alias* (alias tipe) | 20 |
| thunk | thunk (tetap, miring) | 20 |
| never type | *never type* (tipe never) | 20 |
| empty type | *empty type* (tipe kosong) | 20 |
| diverging function | *diverging function* (fungsi divergen) | 20 |
| type theory | teori tipe | 20 |
| dynamically sized type (DST) | *dynamically sized type* (tipe berukuran dinamis); DST (tetap) | 20 |
| unsized type | *unsized type* (tipe yang tidak berukuran) | 20 |
| metadata | metadata (tetap) | 20 |
| golden rule | aturan emas | 20 |
| initializer function | fungsi penginisialisasi | 20 |
| opaque type | *opaque type* (tipe opak) | 20 |
| metaprogramming | *metaprogramming* (metapemrograman) | 20 |
| expand (macro) | diekspansi | 20 |
| declarative macro | *declarative macro* (macro deklaratif) | 20 |
| procedural macro | *procedural macro* (macro prosedural) | 20 |
| attribute-like macro | macro mirip atribut | 20 |
| function-like macro | macro mirip fungsi | 20 |
| token / TokenStream | token (tetap); TokenStream (tetap) | 20 |
| reflection | refleksi | 20 |
| syntax tree | pohon sintaks | 20 |
| intermediate representation | representasi perantara | 20 |
| templating | templating (tetap) | 20 |
| production code | kode produksi | 20 |
| toolbox | kotak perkakas | 20 |
| emitted (kode) | dihasilkan | 20 |
| pre-allocate (up front) | mengalokasikan di muka | 20 |
| syntactically correct | benar secara sintaksis | 20 |
| thread pool | thread pool (tetap) | 21 |
| throughput | throughput (tetap) | 21 |
| request (HTTP) | permintaan | 21 |
| response (HTTP) | respons | 21 |
| client | *client* (klien) | 21 |
| server | *server* (tetap, miring pada kemunculan pertama) | 21 |
| protocol | protokol | 21 |
| Hypertext Transfer Protocol (HTTP) / Transmission Control Protocol (TCP) | (tetap, nama resmi) | 21 |
| request-response | (tetap, miring) | 21 |
| connection / connection attempt | koneksi / percobaan koneksi | 21 |
| bind / binding | mengikat ke port / pengikatan | 21 |
| port | port (tetap) | 21 |
| buffering | buffering (tetap) | 21 |
| request line / status line | baris permintaan / baris status | 21 |
| uniform resource identifier (URI) | *uniform resource identifier* (pengidentifikasi sumber seragam) | 21 |
| uniform resource locator (URL) | *uniform resource locator* (penunjuk lokasi sumber) | 21 |
| CRLF / carriage return / line feed | (tetap) | 21 |
| status code | kode status | 21 |
| reason phrase | frasa alasan | 21 |
| header (HTTP) | header (tetap) | 21 |
| body (HTTP) | isi (respons) | 21 |
| well-formed | well-formed (tetap, miring) | 21 |
| handcoded | menulis dengan tangan | 21 |
| filesystem | filesystem (tetap) | 21 |
| DoS attack | serangan DoS | 21 |
| back up (permintaan) | menumpuk (di antrean) | 21 |
| long-running | berjalan lama | 21 |
| idle thread | thread yang menganggur | 21 |
| fork/join model | model fork/join | 21 |
| compiler-driven development | *compiler-driven development* (pengembangan yang digerakkan oleh kompilator) | 21 |
| configurable | dapat dikonfigurasi | 21 |
| queue | antrean | 21 |
| job (channel) | pekerjaan | 21 |
| worker (pooling) | *Worker* (tetap, nama struct) | 21 |
| pooling | pooling (tetap) | 21 |
| logging | logging (tetap) | 21 |
| capacity (vektor) | kapasitas | 21 |
| sender | pengirim | 21 |
| poisoned (mutex) | *poisoned* (teracuni) | 21 |
| double panic | panic ganda | 21 |
| graceful shutdown | *graceful shutdown* (penghentian yang rapi) | 21 |
| disconnect (channel) | terputus | 21 |
| signaling (verba) | memberi sinyal | 21 |
| robustness | ketangguhan | 21 |
| enhance | menyempurnakan | 21 |
| Rustaceans | Rustacean (tetap) | 21 |
| raw identifier | *raw identifier* (identifier mentah) | App A |
| module path | (tetap, urutan Inggris) | App A |
| glossary | glosarium (tanpa miring) | App B |
| bitwise | bitwise (tetap) | App B |
| left-shift / right-shift | pergeseran kiri / pergeseran kanan | App B |
| short-circuit (evaluasi) | evaluasi hubung singkat | App B |
| bottom type | tipe bottom (tetap, miring) | App B |
| metavariable | metavariabel | App B |
| turbofish | _turbofish_ (tetap) | App B |
| linter | linter (tetap) | App D |
| autocompletion | pelengkapan otomatis | App D |
| inline (galat) | inline (tetap) | App D |
| language server | language server (tetap) | App D |
| edition | edisi (tanpa miring; sudah dipakai ch00/ch01) | App E |
| release channel | *release channel* (saluran rilis) | App G |
| train model / train schedule | model kereta / jadwal kereta | App G |
| branch (git) | branch (tetap) | App G |
| regression | regresi | App G |
| backport | backport (tetap) | App G |
| feature flag / feature gate | (tetap) | App G |
| toolchain | *toolchain* (rantai alat) | App G |
| end of life (EOL) | akhir masa pakai | App G |
| RFC (Request For Comments) | (tetap, nama resmi) | App G |
| opt in (verba) | ikut serta / memilih untuk memakai | App G |
| rock-solid | kokoh | App G |
| bleeding edge | garis terdepan | App G |
| empowerment / empowering | pemberdayaan / memberdayakan | Kata Pengantar |
| enthusiasts | para penggemar | Kata Pengantar |
| advocates (verba) | mengadvokasi | Kata Pengantar |

## Kebijakan istilah 2026-10-17 — pengembalian ke bahasa Inggris

Keputusan pengguna (sesi 2026-10-17): kata Inggris yang umum di dunia
pemrograman tidak diterjemahkan; padanan Indonesia disusun sebagai glosarium
di akhir buku (dikerjakan di poin 3). Aturan hasil keputusan:
- Istilah yang **sebelumnya ditulis penuh Indonesia** kini memakai bahasa
  Inggris: **polos** untuk kata pinjaman umum; **miring** untuk istilah yang
  di bagian lain buku memang sudah miring.
- Padanan dalam kurung yang sudah ada di prosa (`*ownership* (kepemilikan)`)
  **dipertahankan**.
- Heading ikut berubah; anchor terjaga lewat tag `<a id>` Tahap 5; label
  SUMMARY disinkronkan dengan heading final.
- Verba turunan tetap Indonesia (meminjam, mengalokasikan, menetapkan,
  menangkap, menyalin, memproses); kata di luar glosarium tetap Indonesia
  (fungsi, nilai, angka, perangkat lunak, pekerjaan, aturan praktis, dll.).

**Polos** (penggantian per kelompok; alat: `revert_istilah.py` di akar repo):
| Kelompok | Istilah |
|---|---|
| error | galat→error; pesan/penanganan/rawan galat→pesan/penanganan/rawan error; galat kompilator→error *compiler* |
| tipe | tipe→type; tipe data→data type; tipe majemuk→compound type; tipe primitif→primitive type; tipe kembalian→return type; anotasi tipe→type annotation; inferensi tipe→type inference; alias/sinonim/parameter tipe→type alias/synonym/parameter; teori tipe→type theory; bertipe→typed; statis/dinamis→statically/dynamically typed; sistem tipe→type system; tipe asosiasi→associated type; tipe generik→generic type; tipe kustom→custom type; tipe angka→numeric type; tipe berukuran dinamis→dynamically sized type; tipe yang (tidak) berukuran→(un)sized type; pengetikan bebek→duck typing |
| dasar | variabel→variable (lingkungan/konfigurasi→environment/configuration variable); konstanta→constant; pernyataan→statement; ekspresi→expression; nilai kembalian→return value; perulangan→loop (tak berujung→infinite loop; label→loop label); alur kontrol→control flow; bahasa tingkat rendah→low-level language; titik mengambang→floating point; masukan/keluaran→input/output (standar→standard input/output; pengguna→user input); pembangkit angka acak→random number generator; spasi lebar nol→zero-width space; whitespace (ch02, konteks trim) |
| OOP | metode→method; koleksi→collection; pola→pattern (newtype/state→newtype/state pattern); vektor→vector |
| lain | pemrogram→programmer; pustaka standar→standard library; dependensi→dependency (+manager); baris perintah→command line; file sumber→source file; alat→tool; sistem kontrol versi→version control system; keamanan memori→memory safety; ruang nama→namespace; konkurensi/konkuren→concurrency/concurrent; pengiriman pesan→message passing; asinkron→asynchronous; pemrograman fungsional/konkuren/paralel/asinkron→functional/concurrent/parallel/asynchronous programming; pemrograman berorientasi objek→object-oriented programming; pemrograman sistem tingkat rendah→low-level systems programming; pengembangan yang digerakkan oleh pengujian/kompilator→test-driven/compiler-driven development; pemrosesan→processing; penyaringan→filtering; pengguna akhir→end user; luring→offline; peramban web→web browser; server web→web server; pembelajaran mesin→machine learning; denda performa→performance penalty; pengujian→test (unit/integrasi→unit/integration test); pemisahan tanggung jawab→separation of concerns; alur kerja→workflow; keadaan internal→internal state; keadaan yang buruk→bad state; state bersama→shared state; akhir masa pakai→end of life |
| bab 16–21 & lampiran | kueri→query; antrean→queue; permintaan→request (baris→request line); respons→response; protokol→protocol; koneksi→connection (percobaan→connection attempt); baris status→status line; kode status→status code; frasa alasan→reason phrase; kapasitas→capacity; kelaparan→starvation; hambatan performa→performance bottleneck; percobaan ulang→retries; batu penyusun→building block; ekspresivitas→expressiveness; pemeriksaan batas→bounds checking; pencacah→counter; glosarium→glossary; pelengkapan otomatis→autocompletion; edisi→edition; regresi→regression; prioritas→precedence; sisa pembagian→remainder; evaluasi hubung singkat→short-circuit evaluation; model/jadwal kereta→train model/schedule; pengirim/penerima→sender/receiver (bab 16: *transmitter*/*receiver*); handoff (ch17); saluran stable→stable channel |

**Miring** (mengikuti gaya istilah yang sudah miring di bagian lain buku):
kompilator→*compiler*; kepemilikan→*ownership*; pemilik→*owner*;
peminjaman→*borrowing*; referensi→*reference*; masa hidup→*lifetime*;
cakupan→*scope* (bab 11: coverage polos); pemindahan→*move*;
dapat/tidak dapat diubah→*mutable*/*immutable*; tanda tangan→*signature*;
penunjuk→*pointer*; alokasi/pengalokasi→*allocation*/*allocator*
(pengalokasi memori→*memory allocator*); tumpukan→*stack*; timbunan→*heap*;
menggantung→*dangling*; perilaku tak terdefinisi→*undefined behavior*;
salinan dangkal/dalam→*shallow copy*/*deep copy*; kebocoran memori→*memory leak*;
memori bersama→*shared memory*; kata kunci→*keyword*; saluran→*channel*;
mutabilitas→mutability (polos).

**Tetap Indonesia** (di luar glosarium atau kata biasa): fungsi, nilai, angka,
memori (kata tunggal), perangkat lunak/keras, pekerjaan, pengiriman,
penyerahan tanggung jawab (ch12), aturan praktis, kaos, ukuran sepatu,
persediaan, milis, penampungan hewan, kokoh, dan verba turunan (meminjam,
mengalokasikan, menetapkan, menangkap, menyalin, memproses, menyaring).

## Konvensi yang dipakai di Bab 4 (usulan, mohon konfirmasi)

- Heading: istilah teknis ditulis tanpa miring dan tanpa padanan
  (mis. `## Tipe Slice`, `### Mutable References`); padanan hanya pada
  kemunculan pertama di prosa per bab.
- Judul bab (`ch04-00`) memuat padanan: `Memahami Ownership (Kepemilikan)`.
- Alt teks gambar dan caption Listing/Gambar ikut diterjemahkan.
- Kutipan di prosa memakai tanda kutip tipografis “ ” dan apostrof ’
  mengikuti teks asli (diperbaiki menyusul di bab 01: "Hello, world!" → “Hello, world!”).

## Konvensi baru Tahap 5 (disetujui pengguna 2026-10-17)

- Istilah teknis Inggris dari glosarium dicetak miring pada **setiap**
  kemunculan di prosa, bukan hanya kemunculan pertama (selaras gaya Bab 4).
  Kemunculan pertama per bab tetap diberi padanan dalam kurung.
- Istilah berkapital di awal kalimat ikut dimiringkan (“*Compiler*
  biasanya…”).
- Yang dikecualikan dari pemiringan: heading, blok kode dan komentar di
  dalamnya, inline code (backtick), tautan dan label tautan, komentar HTML,
  judul karya/kutipan Inggris yang memang dipertahankan, serta istilah yang
  glosariumnya bertanda "tanpa miring"/"tetap" polos (mis. thread, panic,
  hash map, linter, workspace).

## Konvensi yang dipakai di Bab 3 (usulan, mohon konfirmasi)

- Heading yang anchor-nya menjadi target tautan dari bab lain dipertahankan
  bahasa Inggrisnya: `### Shadowing` tetap "Shadowing" karena ch02 menaut ke
  `ch03-01-variables-and-mutability.html#shadowing`. Heading lain
  diterjemahkan, tanpa miring dan tanpa padanan (mis. `## Tipe Data`).
- Caption Tabel (`<span class="caption">`) dan caption komponen
  `<Listing ...>` ikut diterjemahkan; header tabel diterjemahkan.
- Judul karya (“The Twelve Days of Christmas”) tetap Inggris.

## Masalah terbuka

- **SELESAI (2026-10-18)**: pemeriksaan visual putaran kedua disetujui
  pengguna ("sudah sangat bagus, siap cetak"). Titik potong jilid final
  dikunci: J1 442 hal. / J2 436 hal.; PDF final dibangun ulang dan lulus
  `cetak/periksa.py` (rincian di Status terkini). **Catatan: setelah sampul
  pengguna diintegrasikan (2026-10-18), jumlah halaman menjadi J1 443 /
  J2 437** (sampul belakang menambah 1 halaman per jilid). Titik yang belum
  otomatis terverifikasi dan kini dianggap beres oleh pengguna: (a) judul
  bab rata tengah; (b) label diagram SVG memakai Liberation Serif, tidak
  lagi meluber; (c) caption sendirian di puncak halaman (14 di j1, 4 di
  j2) dianggap wajar; (d) tabel B-1 pecah dua halaman dengan header
  berulang.
- **SELESAI (2026-10-18)**: semua temuan visual pengguna 2026-10-18
  (gambar 4-1..4-7, 15-1, 15-2 terlalu besar; Tabel B-1 berdempetan; blok
  kode terpotong dengan caption menimpa nomor halaman di ±30 listing;
  "tidak diperjualbelikan"; judul bab rata tengah; jarak baris kode).
  Detail perbaikan di Status terkini dan `cetak/README.md`. Opsi .docx
  belum dikerjakan (tetap terbuka bila diminta).
- **SELESAI (Tahap 5)**: semua masalah anchor di bawah ini (heading
  diterjemahkan → tautan `file.html#anchor` rusak) ditangani dengan
  menambahkan tag `<a id="...">` pada heading tujuan di `src/`; pemindaian
  291 tautan internal ber-anchor kini 0 rusak (commit `0324fd6`). Daftar lama
  tetap di bawah sebagai jejak.
- **SELESAI (Tahap 5)**: "command line" di ch11-02 kini "baris perintah";
  "di Appendix C" di ch04-01 kini "di Lampiran C" (commit `24bd8b8`).
- **SELESAI (Tahap 5)**: heading ch17-06 dikonfirmasi setia pada asli
  ("Putting It All Together: Futures, Tasks, and Threads" →
  "Merangkai Semuanya: Futures, Tasks, dan Threads").
- **KEPUTUSAN (Tahap 5)**: konvensi miring — istilah teknis Inggris
  dimiringkan pada SETIAP kemunculan di prosa (bukan hanya kemunculan
  pertama), sesuai pilihan pengguna; istilah berkapital di awal kalimat ikut
  dirapikan. Dicatat juga di seksi Konvensi.
- **SELESAI (kebijakan 2026-10-17)**: "performance penalty" kini ditulis
  dalam bahasa Inggris (denda performa → performance penalty).
- **SELESAI (kebijakan 2026-10-17)**: ch02 memakai *whitespace* di konteks
  `trim`/pemisah masukan (dulu "spasi"); "spasi" untuk karakter spasi tetap.
- **SELESAI (kebijakan 2026-10-17)**: glosarium CLAUDE.md disinkronkan —
  "error | error (polos)", "error handling | penanganan error".

- Keputusan Tahap 4 (Pendahuluan), mohon konfirmasi:
  - Judul buku di `title-page.md` dipertahankan “The Rust Programming
    Language” (nama resmi; prosa bab lain juga mempertahankannya dalam
    miring). Bila ingin diterjemahkan, ubah sekaligus SUMMARY baris pertama.
  - Label SUMMARY untuk Lampiran memakai pola asli “A - Keywords”, “B -
    Operator dan Simbol”, dst. (bukan “Lampiran A: …”), dengan induk
    “[Lampiran]”.
  - `ch17-03-more-futures.md` tidak punya heading H2 (sama dengan aslinya),
    jadi label SUMMARY dipilih bebas: “Bekerja dengan Futures dalam Jumlah
    Berapa Pun” (asli: “Working With Any Number of Futures”).
  - Heading `ch17-06` kini “Merangkai Semuanya: Futures, Tasks, dan Threads”;
    label SUMMARY mengikutinya. Perlu dicek di Tahap 5 apakah aslinya memang
    memuat “Tying It All Together” (belum bisa dibandingkan karena `asli/`
    tidak dibuka di sesi ini).

- Teks tautan yang diterjemahkan di bab terdahulu harus cocok dengan heading
  final file tujuan (diperiksa saat file itu dikerjakan):
  appendix-03 “Trait yang Dapat Diturunkan”.
  Sudah beres: ch14-02 “Menerbitkan Crate ke Crates.io”, ch14-02 seksi
  “Mengekspor API Publik yang Mudah Dipakai” (dari ch07-04), ch14-02 seksi
  “Komentar Dokumentasi sebagai Pengujian” (dari ch11-01), ch15-02
  “Menggunakan Deref Coercions di dalam Fungsi dan Metode”, ch15-02
  “Mengikuti Reference Menuju Nilai” (dari ch08-01).
  Sudah beres setelah Appendix: heading final appendix-03 kini
  `## Lampiran C: Trait yang Dapat Diturunkan` (cocok dengan teks tautan
  ch04-01/ch10-02); heading final appendix-07 kini `## Lampiran G: Bagaimana
  Rust Dibuat dan “Nightly Rust”` (cocok dengan teks tautan ch20-01).
  Catatan: prosa ch04-01 masih menulis “di Appendix C” (bahasa Inggris),
  tidak konsisten dengan “Lampiran C” di bab lain — ditangani di Tahap 5.
- Teks tautan baru yang diterjemahkan di sesi ini, harus cocok dengan
  heading final file tujuan (diperiksa saat file itu dikerjakan):
  ch18-02 “Memakai Trait Object untuk Mengabstraksi Perilaku Bersama”
  (dari ch09-02 dan ch15-01) dan ch18-03 “Menyandikan State dan Perilaku
  sebagai Tipe” (dari ch09-03) sudah beres: heading finalnya kini persis
  sama dengan teks tautan itu.
  Sudah beres setelah Bab 20 dikerjakan: ch18-02 → ch20-03 (heading kini
  “Tipe Berukuran Dinamis dan Trait `Sized`”) dan ch18-03 → ch20-05
  (heading kini “Macro”).
- Teks tautan ch07-00 “[“Cargo Workspaces”]” diubah menjadi “[“Workspace
  Cargo”]” agar cocok dengan heading final ch14-03 (`## Workspace Cargo`),
  satu commit dengan bab 14.
- Teks tautan di bab yang belum diterjemahkan, menuju heading final bab 10
  (dicatat di sini supaya cocok saat bab itu dikerjakan):
  ch15-02 & ch20-02 → ch10-02 “Mengimplementasikan Trait pada Suatu Tipe”.
  (ch12-04 → ch10-03 “Memvalidasi Reference dengan Lifetime”,
  ch13-03 → ch10-02 “Memakai Trait sebagai Parameter”, dan
  ch17-01 → ch10-02 “Memakai Trait sebagai Parameter” sudah beres: teks
  tautannya kini persis sama dengan heading final file tujuan.)
- Teks tautan ch05-02 “Mengalihkan Galat ke Standard Error” dan heading
  ch12-06 sudah beres: heading ch12-06 kini `## Mengalihkan Galat ke Standard
  Error`, persis sama dengan teks tautan ch05-02.
- Anchor heading diterjemahkan → tautan antar-bagian dicek di Tahap 5
  (sesuai Catatan teknis di CLAUDE.md). Termasuk anchor intra-bab ch02
  (`#handling-potential-failure-with-result`,
  `#comparing-the-guess-to-the-secret-number`), anchor ch04-03 → ch06-02
  (`#patterns-that-bind-to-values`, heading kini “Pola yang Mengikat
  Nilai”), ch04-01 → ch05-03 (`#methods`, heading kini “Metode”),
  ch05-03 → ch07-03 (`#exposing-paths-with-the-pub-keyword`, heading kini
  “Mengekspos Path dengan Kata Kunci `pub`”), intra-bab ch08-03
  (`#accessing-values-in-a-hash-map`, heading kini “Mengakses Nilai di
  dalam Hash Map”), ch08-03 & ch12-04 → ch10-03
  (`#validating-references-with-lifetimes`, heading kini “Memvalidasi
  Reference dengan Lifetime”), ch15-02 & ch20-02 → ch10-02
  (`#implementing-a-trait-on-a-type`, heading kini “Mengimplementasikan
  Trait pada Suatu Tipe”; anchor ini otomatis dari heading, tidak ada
  tag `<a id>` lama), ch11-01 → ch11-02 (`#controlling-how-tests-are-run`
  kini “Mengontrol Cara Pengujian Dijalankan”,
  `#running-a-subset-of-tests-by-name` kini “Menjalankan Sebagian
  Pengujian Berdasarkan Nama”, `#ignoring-tests-unless-specifically-requested`
  kini “Mengabaikan Pengujian Kecuali Diminta Secara Spesifik”; ketiganya
  otomatis dari heading, sementara `<a id>` lama
  `ignoring-some-tests-unless-specifically-requested` tetap ada), dan
  ch12-01 → ch07-04
  (`#creating-idiomatic-use-paths`, heading kini “Membuat Path `use` yang
  Idiomatis”; ch12-01 sudah diterjemahkan dengan target tautan dipertahankan;
  di ch07-04 tidak ada tag `<a id>` untuk seksi itu sehingga anchor-nya
  otomatis dari heading terjemahan — solusinya diputuskan di Tahap 5).
  Heading `### Shadowing` (ch03-01) sengaja dipertahankan karena ch02
  menaut ke `#shadowing`.
- Baris glosarium CLAUDE.md "error handling | penanganan *error*" tidak cocok
  dengan pemakaian Bab 4/00 ("galat"). Mohon konfirmasi pemakaian mana yang
  dianggap resmi, lalu sinkronkan tabel glosarium dengan log di atas.
- Kejanggalan teks asli ch00: kalimat "In most situations, we'll lead you to
  the correct version of any code that doesn't compile." muncul dua kali
  (sebelum dan sesudah tabel Ferris). Diterjemahkan apa adanya, tidak diperbaiki.
- Kejanggalan teks asli ch11-03: tautan [alt-paths] menuju
  `ch07-05-...#alternate-file-paths`, tetapi anchor itu tidak ada di ch07-05
  bahkan di teks asli (bagian "Alternate File Paths" sudah dihapus dari
  edisi ini). Target tautan dipertahankan apa adanya.
- Inkonsistensi "command line": ch11-02 menulis "command line", sedangkan
  ch01/ch07/bab 12 menulis "baris perintah". Arahkan ke "baris perintah";
  perbaiki ch11-02 saat ada kesempatan (atau di Tahap 5).
- Anchor otomatis dari heading bab 13 yang menjadi target tautan bab lain
  (tidak ada tag `<a id>` di teks asli; heading kini diterjemahkan):
  ch17-02 → ch13-01 `#capturing-references-or-moving-ownership` (heading kini
  “Menangkap Reference atau Memindahkan Ownership”);
  ch17-04 → ch13-02 `#the-iterator-trait-and-the-next-method` (heading kini
  “Trait `Iterator` dan Metode `next`”). Solusi (tambahkan tag `<a id>`)
  diputuskan di Tahap 5.
- Anchor otomatis dari heading bab 15 yang menjadi target tautan
  (heading kini diterjemahkan; tidak ada tag `<a id>` di teks asli):
  ch15-01 intra-file `#enabling-recursive-types-with-boxes` (heading kini
  “Mengaktifkan Tipe Rekursif dengan Boxes”). Solusi diputuskan di Tahap 5.
- Anchor otomatis dari heading bab 16 yang menjadi target tautan
  (heading kini diterjemahkan; tag `<a id>` yang ada tidak cocok dengan
  target tautan, yang di teks asli mengandalkan anchor otomatis):
  ch16-04 → ch16-03 `#shared-access-to-mutext` (heading kini “Akses Bersama ke
  `Mutex<T>`”);
  ch17-01 → ch16-01 `#creating-a-new-thread-with-spawn` (heading kini
  “Membuat Thread Baru dengan `spawn`”);
  ch17-02 → ch16-01 `#waiting-for-all-threads-to-finish` (heading kini
  “Menunggu Semua Thread Selesai”; di teks asli pun target ini tidak cocok
  dengan tag `<a id>` maupun heading versi asli);
  ch17-02 → ch16-01 `#using-move-closures-with-threads` (heading kini
  “Memakai Closure `move` dengan Thread”). Solusi diputuskan di Tahap 5.
- Anchor otomatis dari heading bab 19 yang menjadi target tautan (heading
  kini diterjemahkan; tidak ada tag `<a id>` yang cocok di teks asli):
  ch19-01 → ch19-03 `#ignoring-values-in-a-pattern` (heading kini
  “Mengabaikan Nilai dalam Pola”);
  ch19-03 intra-file `#adding-conditionals-with-match-guards` (heading kini
  “Menambahkan Kondisional dengan Match Guard”; tag
  `<a id="extra-conditionals-with-match-guards">` tetap ada tetapi target
  tautan memakai anchor otomatis). Solusi diputuskan di Tahap 5.
- Anchor otomatis dari heading bab 20 yang menjadi target tautan (heading
  kini diterjemahkan; tag `<a id>` yang ada tidak cocok dengan target
  tautan, yang di teks asli mengandalkan anchor otomatis):
  ch20-04 → ch20-02 `#advanced-traits` (heading kini “Trait Lanjutan”);
  ch20-02 dan ch20-03 → ch20-02 `#implementing-external-traits-with-the-newtype-pattern`
  (heading kini “Mengimplementasikan Trait Eksternal dengan Pola Newtype”).
  Tag `<a id>` yang dipertahankan di ch20 (unsafe-superpowers,
  when-to-use-unsafe-code, associated-types, default-generic-type-parameters-…,
  disambiguating-between-methods-with-the-same-name, using-supertraits-…,
  using-the-newtype-pattern-…, declarative-macros-with-macro_rules-…,
  how-to-write-a-custom-derive-macro) tetap cocok dengan target tautan
  aslinya. Solusi diputuskan di Tahap 5.
- Teks tautan ch20-01 → appendix-07 “Lampiran G: Bagaimana Rust Dibuat dan
  “Nightly Rust”” harus cocok dengan heading final appendix-07
  (diperiksa saat Tahap 3 mengerjakan file itu). Sudah beres: heading
  finalnya persis sama dengan teks tautan itu.
- Anchor otomatis dari heading bab 21 yang menjadi target tautan (heading
  kini diterjemahkan; tag `<a id>` yang ada tidak cocok dengan target
  tautan, yang di teks asli mengandalkan anchor otomatis):
  ch21-02 intra-file `#creating-a-finite-number-of-threads` (heading kini
  “Membuat Thread dalam Jumlah Terbatas”);
  ch21-02 → ch20-03 `#type-synonyms-and-type-aliases` (heading kini
  “Sinonim Tipe dan Alias Tipe”; di ch20-03 hanya ada
  `<a id="creating-type-synonyms-with-type-aliases">`). Solusi diputuskan
  di Tahap 5.
- Anchor otomatis yang menjadi target tautan appendix-03 (heading kini
  diterjemahkan; di teks asli anchor-nya otomatis dari heading, dan tag
  `<a id>` yang ada memakai id lama yang tidak cocok):
  appendix-03 → ch04-01 `#variables-and-data-interacting-with-clone`
  (heading kini “Variabel dan Data yang Berinteraksi dengan Clone”;
  `<a id="ways-variables-and-data-interact-clone">` tidak cocok),
  appendix-03 → ch04-01 `#stack-only-data-copy` (heading kini “Data yang
  Hanya Ada di Stack: Copy”; tidak ada tag `<a id>`),
  appendix-03 → ch20-05 `#custom-derive-macros` (heading kini “Macro
  `derive` Kustom”; `<a id="how-to-write-a-custom-derive-macro">` tidak
  cocok). Solusi diputuskan di Tahap 5.
- Heading yang sengaja dipertahankan bahasa Inggris karena menjadi target
  anchor intra-file: `### Raw Identifiers` (appendix-01,
  `#raw-identifiers`) dan `### Unstable Features` (appendix-07,
  `#unstable-features`).
- Kejanggalan teks asli ch20-05: kalimat “Let’s walk through what the
  pattern pieces in Listing 20-29 mean” merujuk Listing 20-29, padahal
  konteksnya adalah definisi `vec!` di Listing 20-35. Diterjemahkan apa
  adanya, tidak diperbaiki.
- Kejanggalan teks asli ch20-04: tautan [future-types] menunjuk
  `ch17-03-more-futures.html`, tetapi seksi “The `Pin` Type and the `Unpin`
  Trait” berada di ch17-05. Target tautan dipertahankan apa adanya.

## Cara memulai sesi baru

1. `git status` — pastikan bersih; commit sisa pekerjaan sesi sebelumnya.
2. Jalankan `python3 cek_terjemahan.py --progres`; tempel tabel ringkasnya ke
   bagian "Tabel progres" di atas.
3. Baca "Status terkini" dan "Masalah terbuka".
4. Kerjakan file berikutnya sesuai urutan kerja dan alur di `CLAUDE.md`.
   Satu sesi = satu bab. Jangan mulai bab berikutnya tanpa diminta.

## Cara mengakhiri sesi

1. Perbarui "Status terkini" (bab selesai, file berikutnya, tanggal).
2. Refresh "Tabel progres"; tambahkan istilah baru dan masalah baru bila ada.
3. Commit per bab: `git add -A && git commit -m "terjemah: bab NN <judul>"`.
