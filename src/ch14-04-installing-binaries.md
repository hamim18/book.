<!-- Old headings. Do not remove or links may break. -->

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>

## Memasang Binary dengan `cargo install`

Perintah `cargo install` memungkinkan Anda memasang dan memakai *crate* binary
secara lokal. Ini tidak dimaksudkan untuk menggantikan *package* sistem; ini
dimaksudkan sebagai cara yang nyaman bagi pengembang Rust untuk memasang alat
yang telah dibagikan orang lain di
[crates.io](https://crates.io/)<!-- ignore -->. Perhatikan bahwa Anda hanya
dapat memasang *package* yang memiliki target binary. Sebuah _binary target_
adalah program yang dapat dijalankan yang dibuat jika *crate* itu memiliki file
_src/main.rs_ atau file lain yang disebutkan sebagai binary, berbeda dengan
target library yang tidak dapat dijalankan sendiri tetapi cocok untuk
disertakan di dalam program lain. Biasanya, *crate* memiliki informasi di file
README tentang apakah *crate* itu merupakan library, memiliki target binary,
atau keduanya.

Semua binary yang dipasang dengan `cargo install` disimpan di folder _bin_
pada akar instalasi. Jika Anda memasang Rust menggunakan _rustup.rs_ dan tidak
memiliki konfigurasi khusus, direktori ini adalah *$HOME/.cargo/bin*. Pastikan
direktori ini ada di `$PATH` Anda supaya Anda dapat menjalankan program yang
telah Anda pasang dengan `cargo install`.

Sebagai contoh, di Bab 12 kita menyebutkan bahwa ada implementasi Rust dari
alat `grep` bernama `ripgrep` untuk mencari file. Untuk memasang `ripgrep`,
kita dapat menjalankan perintah berikut:

<!-- manual-regeneration
cargo install something you don't have, copy relevant output below
-->

```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

Baris kedua dari terakhir pada keluaran itu menunjukkan lokasi dan nama binary
yang dipasang, yang dalam kasus `ripgrep` adalah `rg`. Selama direktori
instalasi itu ada di `$PATH` Anda, seperti disebutkan sebelumnya, Anda dapat
menjalankan `rg --help` dan mulai memakai alat pencari file yang lebih cepat
dan lebih Rust-y!
