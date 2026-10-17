# Roadmap Penerjemahan The Rust Programming Language ke Bahasa Indonesia

Sumber kebenaran status file: `python3 cek_terjemahan.py --progres`.
File ini memuat urutan kerja, log istilah, dan masalah terbuka.
Diperbarui di akhir setiap sesi.

## Status terkini

- Bab terakhir selesai: Bab 12 (proyek I/O, 7 file) — Tahap 2 berjalan.
- File berikutnya yang dikerjakan: `ch13-00-functional-features.md`
  (Bab 13, 5 file; mulai dari `ch13-00`).
  `foreword.md` masih di kelompok Pendahuluan (dikerjakan belakangan).
- `mdbook test` terakhir lulus: setelah Bab 11 (exit 0); dijadwalkan lagi
  setelah Bab 14.
- Terakhir diperbarui: 2026-10-17

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
| TOTAL       |      53 |     0 |    59 |   112 |

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

## Konvensi yang dipakai di Bab 4 (usulan, mohon konfirmasi)

- Heading: istilah teknis ditulis tanpa miring dan tanpa padanan
  (mis. `## Tipe Slice`, `### Mutable References`); padanan hanya pada
  kemunculan pertama di prosa per bab.
- Judul bab (`ch04-00`) memuat padanan: `Memahami Ownership (Kepemilikan)`.
- Alt teks gambar dan caption Listing/Gambar ikut diterjemahkan.
- Kutipan di prosa memakai tanda kutip tipografis “ ” dan apostrof ’
  mengikuti teks asli (diperbaiki menyusul di bab 01: "Hello, world!" → “Hello, world!”).

## Konvensi yang dipakai di Bab 3 (usulan, mohon konfirmasi)

- Heading yang anchor-nya menjadi target tautan dari bab lain dipertahankan
  bahasa Inggrisnya: `### Shadowing` tetap "Shadowing" karena ch02 menaut ke
  `ch03-01-variables-and-mutability.html#shadowing`. Heading lain
  diterjemahkan, tanpa miring dan tanpa padanan (mis. `## Tipe Data`).
- Caption Tabel (`<span class="caption">`) dan caption komponen
  `<Listing ...>` ikut diterjemahkan; header tabel diterjemahkan.
- Judul karya (“The Twelve Days of Christmas”) tetap Inggris.

## Masalah terbuka

- Teks tautan yang diterjemahkan di bab terdahulu harus cocok dengan heading
  final file tujuan (diperiksa saat file itu dikerjakan):
  ch15-02 “Menggunakan Deref Coercions di dalam Fungsi dan Metode”;
  appendix-03 “Trait yang Dapat Diturunkan”;
  ch14-02 “Menerbitkan Crate ke Crates.io”.
  (ch05-03 “Metode” sudah beres: heading ch05-03 kini `## Metode`; anchor
  `#methods` → `#metode` masuk pemeriksaan Tahap 5.)
- Teks tautan baru yang diterjemahkan di sesi ini, harus cocok dengan
  heading final file tujuan (diperiksa saat file itu dikerjakan):
  ch14-02 seksi “Mengekspor API Publik yang Mudah Dipakai” (dari ch07-04);
  ch14-02 seksi “Komentar Dokumentasi sebagai Pengujian” (dari ch11-01);
  ch15-02 “Mengikuti Reference Menuju Nilai” (dari ch08-01);
  ch18-02 “Memakai Trait Object untuk Mengabstraksi Perilaku Bersama”
  (dari ch09-02);
  ch18-03 “Menyandikan State dan Perilaku sebagai Tipe” (dari ch09-03).
  (ch11-01 “Cara Menulis Pengujian” dari ch07-04 sudah beres: heading
  ch11-01 kini `## Cara Menulis Pengujian`.)
- Teks tautan di bab yang belum diterjemahkan, menuju heading final bab 10
  (dicatat di sini supaya cocok saat bab itu dikerjakan):
  ch13-03 & ch17-01 → ch10-02 “Memakai Trait sebagai Parameter”;
  ch15-02 & ch20-02 → ch10-02 “Mengimplementasikan Trait pada Suatu Tipe”.
  (ch12-04 → ch10-03 “Memvalidasi Reference dengan Lifetime” sudah beres:
  teks tautan ch12-04 kini persis sama dengan heading final ch10-03.)
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
