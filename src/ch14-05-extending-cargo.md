## Memperluas Cargo dengan Perintah Buatan Sendiri

Cargo dirancang sedemikian rupa sehingga Anda dapat memperluasnya dengan
subperintah baru tanpa harus mengubahnya. Jika sebuah binary di `$PATH` Anda
bernama `cargo-something`, Anda dapat menjalankannya seolah-olah binary itu
adalah subperintah Cargo dengan menjalankan `cargo something`. Perintah
buatan sendiri seperti ini juga terdaftar ketika Anda menjalankan
`cargo --list`. Bisa memakai `cargo install` untuk memasang ekstensi lalu
menjalankannya persis seperti alat bawaan Cargo merupakan keuntungan desain
Cargo yang sangat praktis!

## Ringkasan

Berbagi kode dengan Cargo dan [crates.io](https://crates.io/)<!-- ignore -->
adalah bagian dari hal yang membuat ekosistem Rust berguna untuk banyak tugas
yang berbeda. Pustaka standar Rust memang kecil dan stabil, tetapi crate
mudah dibagikan, dipakai, dan ditingkatkan dengan jadwal yang berbeda dari
jadwal bahasa itu sendiri. Jangan ragu membagikan kode yang berguna bagi Anda
di [crates.io](https://crates.io/)<!-- ignore -->; kemungkinan besar kode itu
akan berguna juga bagi orang lain!
