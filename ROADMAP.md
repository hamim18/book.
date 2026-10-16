# Roadmap Penerjemahan The Rust Programming Language ke Bahasa Indonesia

Sumber kebenaran status file: `python3 cek_terjemahan.py --progres`.
File ini memuat urutan kerja, log istilah, dan masalah terbuka.
Diperbarui di akhir setiap sesi.

## Status terkini

- Bab terakhir selesai: Bab 02 (permainan tebak angka) — Tahap 2 berjalan.
- File berikutnya yang dikerjakan: `ch03-00-common-programming-concepts.md`
  (Bab 03, 6 file; mulai dari `ch03-00`).
  `foreword.md` masih di kelompok Pendahuluan (dikerjakan belakangan).
- Terakhir diperbarui: 2026-10-16

## Urutan kerja

- [x] Tahap 0 — Snapshot `asli/` + commit baseline (`siapkan asli/ dan perangkat terjemahan`)
- [x] Tahap 1 — Bab 4 sebagai uji coba gaya & istilah: `ch04-00` … `ch04-03`
- [ ] Tahap 2 — Urut dari awal buku: `foreword` → `ch00` → `ch01` → … → `ch21`.
      Per bab: terjemah semua file → `cek_terjemahan.py` per file → commit per bab
      (`terjemah: bab NN <judul>`). Jalankan `mdbook test` (lihat Catatan teknis)
      setiap beberapa bab.
- [ ] Tahap 3 — `appendix-00` s/d `appendix-07`
- [ ] Tahap 4 — `title-page.md` + `SUMMARY.md` (judul bab diterjemahkan, path tetap).
      Paling akhir, supaya judul SUMMARY pasti cocok dengan heading final tiap bab.
- [ ] Tahap 5 — Pemeriksaan menyeluruh: review kedua (banding `asli/` ↔ `src/`),
      `mdbook test` (lihat Catatan teknis), `mdbook build` (tautan anchor rusak
      karena heading diterjemahkan), konsistensi istilah antar-bab.
- [ ] Tahap 6 — Cetak A5 (lihat Tahap 8 `PANDUAN_PROMPT.md`).

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

## Tabel progres

<!-- Refresh tiap sesi: tempel output `python3 cek_terjemahan.py --progres`
     (bagian tabel ringkasnya) di bawah baris ini. -->

| Kelompok    | Selesai | Galat | Belum | Total |
|-------------|--------:|------:|------:|------:|
| Pendahuluan |       0 |     0 |     3 |     3 |
| Bab 00      |       1 |     0 |     0 |     1 |
| Bab 01      |       4 |     0 |     0 |     4 |
| Bab 02      |       1 |     0 |     0 |     1 |
| Bab 03      |       0 |     0 |     6 |     6 |
| Bab 04      |       4 |     0 |     0 |     4 |
| Bab 05      |       0 |     0 |     4 |     4 |
| Bab 06      |       0 |     0 |     4 |     4 |
| Bab 07      |       0 |     0 |     6 |     6 |
| Bab 08      |       0 |     0 |     4 |     4 |
| Bab 09      |       0 |     0 |     4 |     4 |
| Bab 10      |       0 |     0 |     4 |     4 |
| Bab 11      |       0 |     0 |     4 |     4 |
| Bab 12      |       0 |     0 |     7 |     7 |
| Bab 13      |       0 |     0 |     5 |     5 |
| Bab 14      |       0 |     0 |     6 |     6 |
| Bab 15      |       0 |     0 |     7 |     7 |
| Bab 16      |       0 |     0 |     5 |     5 |
| Bab 17      |       0 |     0 |     7 |     7 |
| Bab 18      |       0 |     0 |     4 |     4 |
| Bab 19      |       0 |     0 |     4 |     4 |
| Bab 20      |       0 |     0 |     6 |     6 |
| Bab 21      |       0 |     0 |     4 |     4 |
| Appendix    |       0 |     0 |     8 |     8 |
| TOTAL       |      10 |     0 |   102 |   112 |

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

## Konvensi yang dipakai di Bab 4 (usulan, mohon konfirmasi)

- Heading: istilah teknis ditulis tanpa miring dan tanpa padanan
  (mis. `## Tipe Slice`, `### Mutable References`); padanan hanya pada
  kemunculan pertama di prosa per bab.
- Judul bab (`ch04-00`) memuat padanan: `Memahami Ownership (Kepemilikan)`.
- Alt teks gambar dan caption Listing/Gambar ikut diterjemahkan.
- Kutipan di prosa memakai tanda kutip tipografis “ ” dan apostrof ’
  mengikuti teks asli (diperbaiki menyusul di bab 01: "Hello, world!" → “Hello, world!”).

## Masalah terbuka

- Teks tautan yang diterjemahkan di Bab 4 harus cocok dengan heading final
  file tujuan (diperiksa saat file itu dikerjakan):
  ch05-03 "Metode"; ch07-03 "Path untuk Merujuk Item di dalam Pohon Modul";
  ch08-02 "Menyimpan Teks Terenkode UTF-8 dengan String";
  ch15-02 "Menggunakan Deref Coercions di dalam Fungsi dan Metode";
  ch03-02 "Tipe Data"; appendix-03 "Trait yang Dapat Diturunkan".
- Anchor heading diterjemahkan → tautan antar-bagian dicek di Tahap 5
  (sesuai Catatan teknis di CLAUDE.md).
- Baris glosarium CLAUDE.md "error handling | penanganan *error*" tidak cocok
  dengan pemakaian Bab 4/00 ("galat"). Mohon konfirmasi pemakaian mana yang
  dianggap resmi, lalu sinkronkan tabel glosarium dengan log di atas.
- Kejanggalan teks asli ch00: kalimat "In most situations, we'll lead you to
  the correct version of any code that doesn't compile." muncul dua kali
  (sebelum dan sesudah tabel Ferris). Diterjemahkan apa adanya, tidak diperbaiki.
- Teks tautan yang diterjemahkan di Bab 02 harus cocok dengan heading final
  file tujuan (diperiksa saat file itu dikerjakan): ch03-01 "Variabel dan
  Mutabilitas". Anchor intra-bab ch02 (`#handling-potential-failure-with-result`,
  `#comparing-the-guess-to-the-secret-number`) ikut dicek di Tahap 5.
- `mdbook test` dijadwalkan berjalan setelah Bab 02 (bab ke-4 yang selesai).

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
