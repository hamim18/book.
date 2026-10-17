## Lampiran E: Edisi

Di Bab 1, Anda melihat bahwa `cargo new` menambahkan sedikit metadata ke file
_Cargo.toml_ Anda tentang edisi. Lampiran ini membahas apa artinya itu!

Bahasa dan kompilator Rust memiliki siklus rilis enam minggu, artinya pengguna
mendapatkan aliran fitur baru yang terus-menerus. Bahasa pemrograman lain
merilis perubahan yang lebih besar dengan frekuensi yang lebih jarang; Rust
merilis pembaruan yang lebih kecil dengan frekuensi yang lebih sering. Setelah
beberapa saat, semua perubahan kecil ini bertumpuk. Namun, dari rilis ke rilis,
sulit untuk menoleh ke belakang dan berkata, “Wah, antara Rust 1.10 dan Rust
1.31, Rust telah banyak berubah!”

Kira-kira setiap tiga tahun, tim Rust menghasilkan _edisi_ Rust yang baru.
Setiap edisi menyatukan fitur-fitur yang telah hadir ke dalam paket yang jelas
dengan dokumentasi dan perangkat yang sepenuhnya diperbarui. Edisi baru dirilis
sebagai bagian dari proses rilis enam minggu yang biasa.

Edisi memiliki tujuan yang berbeda bagi orang yang berbeda:

- Bagi pengguna aktif Rust, edisi baru menyatukan perubahan-perubahan bertahap
  ke dalam paket yang mudah dipahami.
- Bagi yang bukan pengguna, edisi baru menandakan bahwa beberapa kemajuan besar
  telah hadir, yang mungkin membuat Rust layak dilihat sekali lagi.
- Bagi mereka yang mengembangkan Rust, edisi baru menjadi titik berkumpul bagi
  proyek secara keseluruhan.

Saat buku ini ditulis, tersedia empat edisi Rust: Rust 2015, Rust 2018, Rust
2021, dan Rust 2024. Buku ini ditulis memakai idiom edisi Rust 2024.

Kunci `edition` di _Cargo.toml_ menunjukkan edisi mana yang harus dipakai
kompilator untuk kode Anda. Jika kunci itu tidak ada, Rust memakai `2015`
sebagai nilai edisi demi alasan kompatibilitas mundur.

Setiap proyek dapat memilih memakai edisi selain edisi bawaan 2015. Edisi dapat
memuat perubahan yang tidak kompatibel, seperti menyertakan kata kunci baru yang
bertentangan dengan identifier dalam kode. Namun, kecuali Anda memilih untuk
memakai perubahan itu, kode Anda akan tetap terkompilasi meskipun Anda
meningkatkan versi kompilator Rust yang Anda pakai.

Semua versi kompilator Rust mendukung edisi mana pun yang sudah ada sebelum
rilis kompilator tersebut, dan mereka dapat menautkan *crate* dari edisi mana pun
yang didukung secara bersamaan. Perubahan edisi hanya memengaruhi cara
kompilator melakukan parsing awal terhadap kode. Karena itu, jika Anda memakai
Rust 2015 dan salah satu dependensi Anda memakai Rust 2018, proyek Anda akan
terkompilasi dan dapat memakai dependensi itu. Situasi sebaliknya, saat proyek
Anda memakai Rust 2018 dan sebuah dependensi memakai Rust 2015, juga berjalan
dengan baik.

Agar jelas: sebagian besar fitur akan tersedia di semua edisi. Pengembang yang
memakai edisi Rust mana pun akan terus melihat peningkatan seiring dibuatnya
rilis stabil baru. Namun, dalam beberapa kasus, terutama ketika kata kunci baru
ditambahkan, beberapa fitur baru mungkin hanya tersedia di edisi yang lebih
baru. Anda perlu berpindah edisi jika ingin memanfaatkan fitur semacam itu.

Untuk detail lebih lanjut, lihat [_The Rust Edition
Guide_][edition-guide]. Ini adalah buku lengkap yang menyebutkan satu per satu
perbedaan antaredisi dan menjelaskan cara meningkatkan kode Anda ke edisi baru
secara otomatis melalui `cargo fix`.

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide
