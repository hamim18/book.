# Proyek: Terjemahan The Rust Programming Language ke Bahasa Indonesia

Repositori ini adalah fork dari `rust-lang/book`. Tugasmu adalah menerjemahkan
buku ini ke bahasa Indonesia yang natural dan akademis, untuk dicetak sebagai
buku A5 pembelajaran pribadi.

## Struktur dan batas edit

- `src/`      : file Markdown buku. **Inilah satu-satunya tempat yang kamu edit.**
- `asli/`     : salinan `src/` versi bahasa Inggris, hanya untuk dibandingkan. **Jangan diedit.**
- `listings/` : contoh kode yang dipanggil dari `src/`. **Jangan diubah.**
- `packages/`, `tools/`, `theme/`, `ci/`, `.github/` : **jangan disentuh.**
- `book.toml`  : hanya boleh diubah atas permintaan eksplisit (judul, `language = "id"`).

Nama file dan path di `src/` tidak boleh diganti.
Di `src/SUMMARY.md`, judul bab boleh diterjemahkan, tetapi path tautan harus tetap.

## Gaya bahasa

- Bahasa Indonesia baku, natural, dan akademis, namun tidak kaku.
- Kata ganti untuk pembaca: **"Anda"** (ubah di sini jika ingin "kamu").
- Gunakan kalimat aktif bila memungkinkan. Pecah kalimat Inggris yang panjang
  menjadi dua kalimat Indonesia bila perlu, tetapi jangan mengubah maknanya.
- Pertahankan nada ramah dan humor ringan dari teks asli.
- Terjemahkan makna, bukan kata per kata. Hindari kalimat yang terasa seperti hasil mesin.

## Aturan ketat (tidak boleh dilanggar)

1. **Jangan meringkas, menambah, atau menghilangkan** isi. Setiap paragraf,
   daftar, catatan, dan peringatan di teks asli harus ada di terjemahan.
2. **Blok kode harus identik** dengan aslinya, termasuk spasi, penanda info
   (misalnya ```` ```rust,ignore,does_not_compile ````), dan baris tersembunyi
   yang diawali `#`.
3. **Komentar di dalam kode tetap bahasa Inggris** kecuali diminta lain.
4. **Output terminal dan pesan error kompilator tetap bahasa Inggris**,
   supaya cocok dengan yang muncul di layar pembaca.
5. **Sintaks `{{#include ...}}`, `{{#rustdoc_include ...}}`, dan `{{#...}}`
   lainnya tidak boleh diubah sedikit pun.**
6. **URL dan target tautan tidak boleh diubah.** Teks tautan boleh diterjemahkan.
7. Pertahankan struktur Markdown: tingkat heading, urutan, daftar bernomor,
   tabel, dan jumlah heading harus sama dengan aslinya.
8. Nama di dalam backtick (`` `String` ``, `` `Vec<T>` ``, `` `cargo build` ``)
   tidak diterjemahkan.
9. Jangan memperbaiki "kesalahan" yang kamu kira ada di teks asli. Jika menemukan
   sesuatu yang janggal, terjemahkan apa adanya lalu laporkan di akhir.

## Aturan istilah

Istilah teknis dipertahankan dalam bahasa Inggris dan dicetak *miring*.
**Saat pertama kali muncul di setiap bab**, beri padanan Indonesia dalam kurung,
misalnya *ownership* (kepemilikan). Pemunculan berikutnya cukup *ownership*.
Istilah bertanda "tetap" tidak diberi padanan.

| Inggris | Penulisan |
|---|---|
| ownership | *ownership* (kepemilikan) |
| borrowing | *borrowing* (peminjaman) |
| borrow checker | *borrow checker* (tetap) |
| reference | *reference* (referensi) |
| lifetime | *lifetime* (masa hidup) |
| scope | *scope* (cakupan) |
| move | *move* (pemindahan) |
| mutable / immutable | *mutable* (dapat diubah) / *immutable* (tidak dapat diubah) |
| stack / heap | *stack* (tumpukan) / *heap* (timbunan) |
| trait | *trait* (tetap) |
| crate | *crate* (tetap) |
| package | *package* (paket) |
| module | *module* (modul) |
| struct | *struct* (tetap) |
| enum | *enum* (tetap) |
| slice | *slice* (tetap) |
| closure | *closure* (tetap) |
| iterator | *iterator* (tetap) |
| generics | *generics* (tipe generik) |
| smart pointer | *smart pointer* (penunjuk pintar) |
| pattern matching | *pattern matching* (pencocokan pola) |
| compiler | *compiler* (kompilator) |
| error handling | penanganan galat |
| unsafe | *unsafe* (tetap) |
| macro | *macro* (makro) |

Istilah yang belum ada di tabel: tanyakan padaku atau tambahkan ke tabel ini
lebih dulu, lalu gunakan secara konsisten di seluruh buku.

## Alur kerja per file

1. Baca `ROADMAP.md` di awal sesi untuk tahu posisi terakhir dan masalah
   terbuka. Perbarui file itu di akhir sesi (status terkini, tabel progres,
   log istilah, masalah terbuka).
2. Baca file yang sedang dikerjakan di `src/`. **Jangan membuka `asli/`**;
   folder itu hanya dipakai oleh `cek_terjemahan.py`.
3. Terjemahkan **satu file per kali**. Untuk file yang panjang, kerjakan per bagian heading.
4. Tulis hasilnya ke file yang sama di `src/`.
5. Jalankan pengecekan:
   `python3 cek_terjemahan.py nama-file.md`
   Jika ada galat, perbaiki sampai bersih.
6. Setelah beberapa file selesai, jalankan `mdbook test` untuk memastikan semua
   kode masih terkompilasi. Bangun dulu crate `trpl` lalu sertakan path-nya,
   jika tidak semua contoh bab 17 gagal:
   `cargo build --locked --manifest-path packages/trpl/Cargo.toml`
   `mdbook test --library-path packages/trpl/target/debug/deps`
7. Lakukan review kedua: bandingkan teks asli dan terjemahan, lalu tandai
   bagian yang maknanya bergeser atau terlewat. Perbaiki.
8. Commit per bab dengan pesan seperti `terjemah: bab 04 ownership`.
9. Di akhir setiap file, laporkan singkat: istilah baru yang kamu putuskan,
   dan bagian yang kamu ragukan.

## Hemat konteks

- Jangan membaca seluruh repositori atau menelusuri folder besar. Buka hanya
  file yang sedang dikerjakan dan `src/SUMMARY.md` bila perlu melihat struktur.
- Jangan membuka `listings/`, `packages/`, `tools/`, atau `asli/`.
- Satu sesi mengerjakan satu bab. Jangan mulai bab berikutnya tanpa diminta.
- Saat memperbaiki galat dari skrip pengecek, edit hanya bagian yang bermasalah,
  jangan menulis ulang seluruh file.

## Format laporan di akhir tiap file

Tulis ringkas, maksimal 10 baris:
1. Status skrip pengecek (OK atau daftar galat yang tersisa).
2. Istilah baru yang kamu putuskan sendiri (jika ada), beserta usulan padanannya.
3. Bagian yang kamu ragukan, lengkap dengan nama heading-nya.
4. Hal janggal di teks asli yang kamu temukan (jika ada).

## Jika ragu

- Ragu soal istilah: pakai aturan istilah di atas, atau tanyakan sebelum menulis.
- Ragu apakah sesuatu kode atau prosa: perlakukan sebagai kode dan jangan ubah.
- Jangan pernah mengarang isi. Jika kalimat asli ambigu, terjemahkan seambigu
  aslinya dan laporkan.

## Catatan teknis

- Heading di mdBook menghasilkan anchor otomatis dari teksnya. Menerjemahkan heading
  dapat membuat tautan antar-bagian seperti `file.html#nama-anchor` tidak lagi
  menemukan sasarannya. Jangan ubah tautan itu; kita periksa dan tangani
  masalah anchor secara terpisah setelah build.
- Urutan bab pertama yang dikerjakan: Bab 4 (ownership) sebagai uji coba gaya dan istilah.
