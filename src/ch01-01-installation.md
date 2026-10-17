<a id="installation"></a>
## Instalasi

Langkah pertama adalah memasang Rust. Kita akan mengunduh Rust melalui
`rustup`, alat baris perintah untuk mengelola versi Rust dan alat-alat
terkaitnya. Anda memerlukan koneksi internet untuk pengunduhan ini.

> Catatan: Jika karena suatu alasan Anda memilih untuk tidak memakai
> `rustup`, silakan lihat [halaman Method Instalasi Rust Lainnya][otherinstall]
> untuk opsi lebih lanjut.

Langkah-langkah berikut memasang versi stabil terbaru dari *compiler*
(kompilator) Rust. Jaminan stabilitas Rust memastikan bahwa semua contoh
dalam buku ini yang terkompilasi akan tetap terkompilasi dengan versi Rust
yang lebih baru. Keluarannya mungkin sedikit berbeda antarversi karena Rust
sering meningkatkan pesan error dan peringatannya. Dengan kata lain, versi
stabil Rust yang lebih baru mana pun yang Anda pasang menggunakan
langkah-langkah ini seharusnya bekerja sesuai harapan dengan isi buku ini.

> ### Notasi Baris Perintah
>
> Di bab ini dan di seluruh buku, kita akan menampilkan beberapa perintah
> yang dipakai di terminal. Baris yang harus Anda ketik di terminal semuanya
> diawali dengan `$`. Anda tidak perlu mengetik karakter `$`; itu adalah
> prompt baris perintah yang ditampilkan untuk menandai awal setiap perintah.
> Baris yang tidak diawali `$` biasanya menampilkan output dari perintah
> sebelumnya. Selain itu, contoh khusus PowerShell akan memakai `>` alih-alih
> `$`.

### Memasang `rustup` di Linux atau macOS

Jika Anda memakai Linux atau macOS, buka terminal dan masukkan perintah
berikut:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

Perintah ini mengunduh sebuah skrip dan memulai instalasi alat `rustup`,
yang memasang versi stabil terbaru dari Rust. Anda mungkin akan diminta
memasukkan kata sandi. Jika instalasi berhasil, baris berikut akan muncul:

```text
Rust is installed now. Great!
```

Anda juga memerlukan _linker_, yaitu program yang dipakai Rust untuk
menggabungkan output hasil kompilasinya menjadi satu file. Kemungkinan
besar Anda sudah memilikinya. Jika Anda mendapat error linker, Anda harus
memasang *compiler* C, yang biasanya menyertakan linker. *Compiler* C juga
berguna karena beberapa *package* (paket) Rust yang umum bergantung pada
kode C dan akan membutuhkan *compiler* C.

Di macOS, Anda bisa mendapatkan *compiler* C dengan menjalankan:

```console
$ xcode-select --install
```

Pengguna Linux umumnya perlu memasang GCC atau Clang, sesuai dokumentasi
distribusi mereka. Misalnya, jika Anda memakai Ubuntu, Anda dapat memasang
*package* `build-essential`.

### Memasang `rustup` di Windows

Di Windows, kunjungi [https://www.rust-lang.org/tools/install][install]<!-- ignore
--> dan ikuti petunjuk untuk memasang Rust. Pada suatu titik dalam proses
instalasi, Anda akan diminta untuk memasang Visual Studio. Ini menyediakan
linker dan pustaka native yang diperlukan untuk mengompilasi program. Jika
Anda memerlukan bantuan lebih lanjut untuk langkah ini, lihat
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!--
ignore -->.

Sisa buku ini memakai perintah yang bekerja di _cmd.exe_ maupun PowerShell.
Jika ada perbedaan tertentu, kita akan menjelaskan mana yang harus dipakai.

<a id="troubleshooting"></a>
### Pemecahan Masalah

Untuk memeriksa apakah Rust telah terpasang dengan benar, buka shell dan
masukkan baris ini:

```console
$ rustc --version
```

Anda seharusnya melihat nomor versi, hash commit, dan tanggal commit untuk
versi stabil terbaru yang telah dirilis, dalam format berikut:

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

Jika Anda melihat informasi ini, Anda telah berhasil memasang Rust! Jika
tidak, periksa apakah Rust ada di variable sistem `%PATH%` Anda seperti
berikut.

Di Windows CMD, gunakan:

```console
> echo %PATH%
```

Di PowerShell, gunakan:

```powershell
> echo $env:Path
```

Di Linux dan macOS, gunakan:

```console
$ echo $PATH
```

Jika semua itu sudah benar tetapi Rust tetap tidak berfungsi, ada sejumlah
tempat untuk meminta bantuan. Cari tahu cara berhubungan dengan sesama
Rustaceans (julukan konyol untuk menyebut diri kita sendiri) di [halaman
komunitas][community].

### Memperbarui dan Menghapus Instalasi

Setelah Rust terpasang melalui `rustup`, memperbarui ke versi yang baru
dirilis menjadi mudah. Dari shell Anda, jalankan skrip pembaruan berikut:

```console
$ rustup update
```

Untuk menghapus instalasi Rust dan `rustup`, jalankan skrip penghapusan
berikut dari shell Anda:

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->
<a id="local-documentation"></a>

### Membaca Dokumentasi Lokal

Instalasi Rust juga menyertakan salinan lokal dokumentasinya sehingga Anda
dapat membacanya secara luring. Jalankan `rustup doc` untuk membuka
dokumentasi lokal di peramban Anda.

Kapan pun sebuah type atau fungsi disediakan oleh pustaka standar dan Anda
tidak yakin apa fungsinya atau bagaimana cara memakainya, gunakan
dokumentasi antarmuka pemrograman aplikasi (API) untuk mengetahuinya!

<!-- Old headings. Do not remove or links may break. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Menggunakan Editor Teks dan IDE

Buku ini tidak membuat asumsi tentang alat yang Anda pakai untuk menulis
kode Rust. Hampir semua editor teks bisa menyelesaikan pekerjaan ini!
Namun, banyak editor teks dan lingkungan pengembangan terpadu (IDE)
memiliki dukungan bawaan untuk Rust. Anda selalu dapat menemukan daftar
yang cukup mutakhir dari banyak editor dan IDE di [halaman alat][tools] di
situs web Rust.

### Bekerja Luring dengan Buku Ini

Dalam beberapa contoh, kita akan memakai *package* Rust di luar pustaka
standar. Untuk mengerjakan contoh-contoh tersebut, Anda memerlukan koneksi
internet atau harus mengunduh dependensi-dependensi itu lebih dulu. Untuk
mengunduh dependensinya lebih dulu, Anda dapat menjalankan perintah-perintah
berikut. (Nanti kita akan menjelaskan secara detail apa itu `cargo` dan apa
fungsi setiap perintah ini.)

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

Ini akan menyimpan cache unduhan untuk *package*-*package* ini sehingga
Anda tidak perlu mengunduhnya lagi nanti. Setelah Anda menjalankan perintah
ini, Anda tidak perlu menyimpan folder `get-dependencies`. Jika Anda telah
menjalankan perintah ini, Anda dapat memakai flag `--offline` pada semua
perintah `cargo` di sisa buku ini untuk memakai versi-versi yang tersimpan
di cache alih-alih mencoba menggunakan jaringan.

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools
