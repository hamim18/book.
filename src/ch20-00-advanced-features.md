# Fitur Lanjutan

Sampai di sini, Anda sudah mempelajari bagian-bagian bahasa pemrograman Rust
yang paling sering dipakai. Sebelum kita mengerjakan satu proyek lagi di
Bab 21, kita akan menengok beberapa aspek bahasa yang mungkin sesekali Anda
temui, tetapi mungkin tidak Anda pakai setiap hari. Anda bisa memakai bab ini
sebagai rujukan saat menemukan hal-hal yang belum Anda kenal. Fitur-fitur
yang dibahas di sini berguna dalam situasi yang sangat spesifik. Meskipun
mungkin tidak sering Anda pakai, kami ingin memastikan Anda memahami semua
fitur yang ditawarkan Rust.

Di bab ini, kita akan membahas:

- *Unsafe* Rust: Cara memilih untuk tidak memakai sebagian jaminan Rust dan
  mengambil tanggung jawab untuk menegakkan jaminan itu secara manual
- *Trait* lanjutan: Tipe asosiasi, parameter tipe bawaan, sintaks fully
  qualified, *supertrait*, dan pola newtype dalam kaitannya dengan *trait*
- Tipe lanjutan: Lebih jauh tentang pola newtype, alias tipe, tipe never,
  dan tipe berukuran dinamis
- Fungsi dan *closure* lanjutan: *Pointer* fungsi dan mengembalikan *closure*
- *Macro*: Cara mendefinisikan kode yang mendefinisikan lebih banyak kode pada
  waktu kompilasi

Semuanya ini adalah kumpulan lengkap fitur Rust dengan sesuatu untuk semua
orang! Mari kita mulai!
