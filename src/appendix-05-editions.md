## Lampiran E: Edition

Di Bab 1, Anda melihat bahwa `cargo new` menambahkan sedikit metadata ke file
_Cargo.toml_ Anda tentang edition. Lampiran ini membahas apa artinya itu!

Bahasa dan *compiler* Rust memiliki siklus rilis enam minggu, artinya pengguna
mendapatkan aliran fitur baru yang terus-menerus. Bahasa pemrograman lain
merilis perubahan yang lebih besar dengan frekuensi yang lebih jarang; Rust
merilis pembaruan yang lebih kecil dengan frekuensi yang lebih sering. Setelah
beberapa saat, semua perubahan kecil ini bertumpuk. Namun, dari rilis ke rilis,
sulit untuk menoleh ke belakang dan berkata, “Wah, antara Rust 1.10 dan Rust
1.31, Rust telah banyak berubah!”

Kira-kira setiap tiga tahun, tim Rust menghasilkan _edisi_ Rust yang baru.
Setiap edition menyatukan fitur-fitur yang telah hadir ke dalam paket yang jelas
dengan dokumentasi dan perangkat yang sepenuhnya diperbarui. Edition baru dirilis
sebagai bagian dari proses rilis enam minggu yang biasa.

Edition memiliki tujuan yang berbeda bagi orang yang berbeda:

- Bagi pengguna aktif Rust, edition baru menyatukan perubahan-perubahan bertahap
  ke dalam paket yang mudah dipahami.
- Bagi yang bukan pengguna, edition baru menandakan bahwa beberapa kemajuan besar
  telah hadir, yang mungkin membuat Rust layak dilihat sekali lagi.
- Bagi mereka yang mengembangkan Rust, edition baru menjadi titik berkumpul bagi
  proyek secara keseluruhan.

Saat buku ini ditulis, tersedia empat edition Rust: Rust 2015, Rust 2018, Rust
2021, dan Rust 2024. Buku ini ditulis memakai idiom edition Rust 2024.

Kunci `edition` di _Cargo.toml_ menunjukkan edition mana yang harus dipakai
*compiler* untuk kode Anda. Jika kunci itu tidak ada, Rust memakai `2015`
sebagai nilai edition demi alasan kompatibilitas mundur.

Setiap proyek dapat memilih memakai edition selain edition bawaan 2015. Edition dapat
memuat perubahan yang tidak kompatibel, seperti menyertakan *keyword* baru yang
bertentangan dengan identifier dalam kode. Namun, kecuali Anda memilih untuk
memakai perubahan itu, kode Anda akan tetap terkompilasi meskipun Anda
meningkatkan versi *compiler* Rust yang Anda pakai.

Semua versi *compiler* Rust mendukung edition mana pun yang sudah ada sebelum
rilis *compiler* tersebut, dan mereka dapat menautkan *crate* dari edition mana pun
yang didukung secara bersamaan. Perubahan edition hanya memengaruhi cara
*compiler* melakukan parsing awal terhadap kode. Karena itu, jika Anda memakai
Rust 2015 dan salah satu dependency Anda memakai Rust 2018, proyek Anda akan
terkompilasi dan dapat memakai dependency itu. Situasi sebaliknya, saat proyek
Anda memakai Rust 2018 dan sebuah dependency memakai Rust 2015, juga berjalan
dengan baik.

Agar jelas: sebagian besar fitur akan tersedia di semua edition. Pengembang yang
memakai edition Rust mana pun akan terus melihat peningkatan seiring dibuatnya
rilis stabil baru. Namun, dalam beberapa kasus, terutama ketika *keyword* baru
ditambahkan, beberapa fitur baru mungkin hanya tersedia di edition yang lebih
baru. Anda perlu berpindah edition jika ingin memanfaatkan fitur semacam itu.

Untuk detail lebih lanjut, lihat [_The Rust Edition
Guide_][edition-guide]. Ini adalah buku lengkap yang menyebutkan satu per satu
perbedaan antaredisi dan menjelaskan cara meningkatkan kode Anda ke edition baru
secara otomatis melalui `cargo fix`.

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide
