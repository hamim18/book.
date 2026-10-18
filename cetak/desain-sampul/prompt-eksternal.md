# Prompt Eksternal — Sampul Buku Cetak

Disusun 2026-10-18 untuk dipakai di luar Claude Code (pembuat gambar/desain
lainnya). Simpan PNG hasilnya ke `cetak/desain-sampul/` (atau `cetak/img/`)
dengan nama yang tercantum di bawah, lalu beri tahu asisten untuk
mengintegrasikannya ke `template.typ`.

---

Tugas: buat desain sampul depan dan belakang untuk buku cetak dua jilid
berikut ini.

**Konteks**
- Buku: *The Rust Programming Language* — terjemahan bahasa Indonesia,
  edisi cetak pribadi (bukan komersial).
- Dua jilid: Jilid 1 = Kata Pengantar, Pendahuluan, Bab 1–12;
  Jilid 2 = Bab 13–21, Lampiran A–G.
- Ukuran sampul: B5 ISO 176 × 250 mm, 300 DPI (2079 × 2953 px), desain
  full-bleed (warna latar sampai ke tepi halaman), semua teks minimal
  12 mm dari tepi.

**Keluaran yang diminta**
4 berkas PNG:
1. `sampul-depan-jilid1.png`
2. `sampul-belakang-jilid1.png`
3. `sampul-depan-jilid2.png`
4. `sampul-belakang-jilid2.png`

**Teks wajib (harus persis seperti tertulis, tanpa salah eja)**

Depan (semua jilid):
- Judul: The Rust Programming Language
- Subjudul: Terjemahan Bahasa Indonesia
- Penulis: Steve Klabnik · Carol Nichols · Chris Krycho
- Penerjemah: diterjemahkan oleh AI
- Jilid 1: "JILID 1" dan "Kata Pengantar · Pendahuluan · Bab 1–12"
- Jilid 2: "JILID 2" dan "Bab 13–21 · Lampiran A–G"
- Catatan edisi: edisi 2024 · Rust 1.98

Belakang (semua jilid):
- Judul kecil: The Rust Programming Language
- Sinopsis: "Rust adalah bahasa pemrograman sistem yang cepat, andal, dan
  aman — tanpa pengumpul sampah. Buku resmi ini memandu Anda dari dasar:
  variable, function, ownership, hingga fitur paling canggih seperti
  generics, async, unsafe, dan macro. Ditutup dengan proyek akhir:
  membangun server web multithread dari nol."
- Daftar isi buku:
  - 21 bab + 7 lampiran — terjemahan lengkap
  - Glosarium Inggris–Indonesia (±650 istilah)
  - Indeks istilah dengan nomor halaman
  - Kanal koreksi terbuka
- Edisi: Edisi cetak pribadi · Oktober 2026

**Arah desain — pilih salah satu, atau buat ketiganya untuk dibandingkan**

A. Klasik Oranye — latar putih; ikon kepiting kecil oranye (#F74C00) di
   bagian atas; judul serif tebal hitam di tengah; garis oranye tipis di
   bawah judul; pita oranye solid (#F74C00) selebar halaman di bagian bawah
   berisi teks jilid berwarna putih; belakang oranye penuh dengan teks
   putih.

B. Ferris Raksasa — latar krem (#FBF6EE); siluet kepiting (maskot Rust,
   garis tunggal, merah #E33B26) besar, sekitar separuh lebar halaman, di
   tengah sebagai tokoh visual; judul merah marun (#7A1B18) tebal di atas;
   pita marun solid di bawah berisi teks jilid putih; belakang marun penuh
   dengan teks krem muda.

C. Gelap Modern — latar arang (#23272E); judul putih tebal rata kiri dengan
   aksen garis oranye (#F74C00); panel kode gelap berisi kode
   `fn main() {` / `    println!("Hello, world!");` / `}` dalam font
   monospace; badge oranye membulat berisi teks jilid; belakang arang penuh
   dengan teks abu terang.

**Aturan kualitas**
- Semua teks terbaca jelas, ejaan persis seperti di atas, tidak ada teks
  terpotong atau tertutup elemen lain.
- Tipografi: serif tebal untuk judul (mis. IBM Plex Serif), monospace untuk
  kode (mis. IBM Plex Mono).
- Kontras teks terhadap latar harus tinggi.
- Jika memakai gambar kepiting: siluet sederhana satu warna, bukan foto
  realistik. Atribusi (CC BY 4.0) dicantumkan di halaman hak cipta buku,
  tidak perlu muncul di sampul.
- Jilid 1 dan jilid 2 harus konsisten: desain sama persis, hanya badge
  jilid yang berbeda.
