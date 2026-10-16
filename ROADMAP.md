# Roadmap Penerjemahan The Rust Programming Language ke Bahasa Indonesia

Sumber kebenaran status file: `python3 cek_terjemahan.py --progres`.
File ini memuat urutan kerja, log istilah, dan masalah terbuka.
Diperbarui di akhir setiap sesi.

## Status terkini

- Bab terakhir selesai: — (belum ada)
- File berikutnya yang dikerjakan: `ch04-00-understanding-ownership.md` (Tahap 1)
- Terakhir diperbarui: 2026-10-16 (infrastruktur siap; belum ada yang diterjemahkan)

## Urutan kerja

- [x] Tahap 0 — Snapshot `asli/` + commit baseline (`siapkan asli/ dan perangkat terjemahan`)
- [ ] Tahap 1 — Bab 4 sebagai uji coba gaya & istilah: `ch04-00` … `ch04-03`
- [ ] Tahap 2 — Urut dari awal buku: `foreword` → `ch00` → `ch01` → … → `ch21`.
      Per bab: terjemah semua file → `cek_terjemahan.py` per file → commit per bab
      (`terjemah: bab NN <judul>`). Jalankan `mdbook test` setiap beberapa bab.
- [ ] Tahap 3 — `appendix-00` s/d `appendix-07`
- [ ] Tahap 4 — `title-page.md` + `SUMMARY.md` (judul bab diterjemahkan, path tetap).
      Paling akhir, supaya judul SUMMARY pasti cocok dengan heading final tiap bab.
- [ ] Tahap 5 — Pemeriksaan menyeluruh: review kedua (banding `asli/` ↔ `src/`),
      `mdbook test`, `mdbook build` (tautan anchor rusak karena heading
      diterjemahkan), konsistensi istilah antar-bab.
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

## Tabel progres

<!-- Refresh tiap sesi: tempel output `python3 cek_terjemahan.py --progres`
     (bagian tabel ringkasnya) di bawah baris ini. -->

| Kelompok    | Selesai | Galat | Belum | Total |
|-------------|--------:|------:|------:|------:|
| Pendahuluan |       0 |     0 |     3 |     3 |
| Bab 00      |       0 |     0 |     1 |     1 |
| Bab 01      |       0 |     0 |     4 |     4 |
| Bab 02      |       0 |     0 |     1 |     1 |
| Bab 03      |       0 |     0 |     6 |     6 |
| Bab 04      |       0 |     0 |     4 |     4 |
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
| TOTAL       |       0 |     0 |   112 |   112 |

## Log keputusan istilah

Istilah baru di luar tabel glosarium `CLAUDE.md`. Setelah disetujui pengguna,
masukkan juga ke tabel glosarium di `CLAUDE.md`.

| Istilah | Padanan | Bab |
|---|---|---|
| (kosong) | | |

## Masalah terbuka

- (kosong)

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
