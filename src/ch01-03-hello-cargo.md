## Hello, Cargo!

Cargo adalah sistem build dan pengelola *package* (paket) milik Rust.
Sebagian besar Rustaceans memakai alat ini untuk mengelola proyek Rust
mereka karena Cargo menangani banyak tugas untuk Anda, seperti membangun
kode Anda, mengunduh pustaka-pustaka yang dibutuhkan kode Anda, dan
membangun pustaka-pustaka itu. (Kita menyebut pustaka yang dibutuhkan kode
Anda sebagai _dependensi_.)

Program Rust yang paling sederhana, seperti yang telah kita tulis sejauh
ini, tidak memiliki dependensi. Jika kita membangun proyek “Hello, world!”
dengan Cargo, proyek itu hanya akan memakai bagian Cargo yang menangani
pembangunan kode Anda. Seiring Anda menulis program Rust yang lebih
kompleks, Anda akan menambahkan dependensi, dan jika Anda memulai proyek
menggunakan Cargo, menambahkan dependensi akan jauh lebih mudah.

Karena sebagian besar proyek Rust memakai Cargo, sisa buku ini mengasumsikan
bahwa Anda juga memakai Cargo. Cargo ikut terpasang bersama Rust jika Anda
memakai installer resmi yang dibahas di bagian
[“Instalasi”][installation]<!-- ignore -->. Jika Anda memasang Rust melalui
cara lain, periksa apakah Cargo sudah terpasang dengan memasukkan perintah
berikut di terminal Anda:

```console
$ cargo --version
```

Jika Anda melihat nomor versi, berarti Cargo sudah terpasang! Jika Anda
melihat error, seperti `command not found`, lihat dokumentasi metode
instalasi Anda untuk menentukan cara memasang Cargo secara terpisah.

### Membuat Proyek dengan Cargo

Mari kita membuat proyek baru menggunakan Cargo dan melihat perbedaannya
dengan proyek “Hello, world!” awal kita. Arahkan kembali ke direktori
_projects_ Anda (atau ke mana pun Anda memutuskan untuk menyimpan kode).
Lalu, di sistem operasi apa pun, jalankan perintah berikut:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

Perintah pertama membuat direktori dan proyek baru bernama _hello_cargo_.
Kita menamai proyek kita _hello_cargo_, dan Cargo membuat file-file
proyeknya di direktori dengan nama yang sama.

Masuklah ke direktori _hello_cargo_ dan lihat daftar file-nya. Anda akan
melihat bahwa Cargo telah menghasilkan dua file dan satu direktori untuk
kita: file _Cargo.toml_ dan direktori _src_ yang berisi file _main.rs_ di
dalamnya.

Cargo juga telah menginisialisasi repositori Git baru beserta file
_.gitignore_. File-file Git tidak akan dibuat jika Anda menjalankan
`cargo new` di dalam repositori Git yang sudah ada; Anda dapat
mengesampingkan perilaku ini dengan memakai `cargo new --vcs=git`.

> Catatan: Git adalah sistem kontrol versi yang umum. Anda dapat mengubah
> `cargo new` agar memakai sistem kontrol versi yang berbeda atau tidak
> memakai sistem kontrol versi sama sekali dengan menggunakan flag `--vcs`.
> Jalankan `cargo new --help` untuk melihat opsi-opsi yang tersedia.

Buka _Cargo.toml_ di editor teks pilihan Anda. Isinya seharusnya mirip
dengan kode di Listing 1-2.

<Listing number="1-2" file-name="Cargo.toml" caption="Isi *Cargo.toml* yang dihasilkan oleh `cargo new`">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

File ini berformat [_TOML_][toml]<!-- ignore --> (_Tom’s Obvious, Minimal
Language_), yang merupakan format konfigurasi Cargo.

Baris pertama, `[package]`, adalah judul bagian yang menandakan bahwa
statement-statement berikutnya sedang mengonfigurasi sebuah *package*.
Saat kita menambahkan lebih banyak informasi ke file ini, kita akan
menambahkan bagian-bagian lain.

Tiga baris berikutnya menetapkan informasi konfigurasi yang dibutuhkan
Cargo untuk mengompilasi program Anda: nama, versi, dan edisi Rust yang
akan dipakai. Kita akan membahas kunci `edition` di
[Lampiran E][appendix-e]<!-- ignore -->.

Baris terakhir, `[dependencies]`, adalah awal dari bagian untuk
mendaftarkan dependensi-dependensi proyek Anda. Di Rust, paket-paket
kode disebut sebagai *crate*. Kita tidak membutuhkan crate lain untuk
proyek ini, tetapi kita akan membutuhkannya pada proyek pertama di Bab 2,
jadi kita akan memakai bagian dependensi ini nanti.

Sekarang buka _src/main.rs_ dan lihatlah:

<span class="filename">Nama File: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo telah membuatkan program “Hello, world!” untuk Anda, sama seperti
yang kita tulis di Listing 1-1! Sejauh ini, perbedaan antara proyek kita
dan proyek buatan Cargo adalah bahwa Cargo menempatkan kodenya di direktori
_src_, dan kita memiliki file konfigurasi _Cargo.toml_ di direktori
teratas.

Cargo mengharapkan file-file sumber Anda berada di dalam direktori _src_.
Direktori proyek tingkat atas hanya untuk file README, informasi lisensi,
file konfigurasi, dan hal-hal lain yang tidak terkait dengan kode Anda.
Memakai Cargo membantu Anda mengorganisasi proyek. Setiap hal punya
tempatnya, dan semuanya berada di tempatnya.

Jika Anda memulai proyek yang tidak memakai Cargo, seperti yang kita
lakukan dengan proyek “Hello, world!”, Anda dapat mengubahnya menjadi
proyek yang memakai Cargo. Pindahkan kode proyek ke direktori _src_ dan
buat file _Cargo.toml_ yang sesuai. Salah satu cara mudah untuk
mendapatkan file _Cargo.toml_ itu adalah menjalankan `cargo init`, yang
akan membuatkannya untuk Anda secara otomatis.

### Membangun dan Menjalankan Proyek Cargo

Sekarang mari kita lihat apa yang berbeda ketika kita membangun dan
menjalankan program “Hello, world!” dengan Cargo! Dari direktori
_hello_cargo_ Anda, bangun proyek Anda dengan memasukkan perintah berikut:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

Perintah ini membuat file eksekutabel di _target/debug/hello_cargo_ (atau
_target\debug\hello_cargo.exe_ di Windows), bukan di direktori Anda saat
ini. Karena build bawaannya adalah build debug, Cargo menempatkan file
binernya di direktori bernama _debug_. Anda dapat menjalankan file
eksekutabelnya dengan perintah ini:

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

Jika semuanya berjalan lancar, `Hello, world!` seharusnya tercetak ke
terminal. Menjalankan `cargo build` untuk pertama kalinya juga membuat
Cargo menciptakan file baru di tingkat teratas: _Cargo.lock_. File ini
melacak versi-versi pasti dari dependensi dalam proyek Anda. Proyek ini
tidak memiliki dependensi, jadi isi file-nya agak sepi. Anda tidak akan
pernah perlu mengubah file ini secara manual; Cargo mengelola isinya untuk
Anda.

Kita baru saja membangun proyek dengan `cargo build` dan menjalankannya
dengan `./target/debug/hello_cargo`, tetapi kita juga dapat memakai
`cargo run` untuk mengompilasi kode lalu menjalankan file eksekutabel
hasilnya dalam satu perintah sekaligus:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Memakai `cargo run` lebih praktis daripada harus ingat untuk menjalankan
`cargo build` lalu memakai seluruh *path* menuju file binernya, jadi
kebanyakan pengembang memakai `cargo run`.

Perhatikan bahwa kali ini kita tidak melihat output yang menandakan
bahwa Cargo sedang mengompilasi `hello_cargo`. Cargo tahu bahwa
file-file-nya belum berubah, jadi Cargo tidak membangun ulang, melainkan
langsung menjalankan file binernya. Jika Anda mengubah kode sumber Anda,
Cargo akan membangun ulang proyeknya sebelum menjalankannya, dan Anda akan
melihat output ini:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo juga menyediakan perintah bernama `cargo check`. Perintah ini
memeriksa kode Anda dengan cepat untuk memastikan kode itu terkompilasi,
tetapi tidak menghasilkan file eksekutabel:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Mengapa Anda tidak menginginkan file eksekutabel? Sering kali, `cargo
check` jauh lebih cepat daripada `cargo build` karena perintah ini
melewati langkah pembuatan file eksekutabel. Jika Anda terus-menerus
memeriksa pekerjaan Anda selagi menulis kode, memakai `cargo check` akan
mempercepat proses untuk memberi tahu Anda apakah proyek Anda masih
terkompilasi! Karena itu, banyak Rustaceans menjalankan `cargo check`
secara berkala selagi menulis program untuk memastikan programnya
terkompilasi. Lalu, mereka menjalankan `cargo build` ketika sudah siap
memakai file eksekutabelnya.

Mari kita rekap apa yang telah kita pelajari sejauh ini tentang Cargo:

- Kita dapat membuat proyek menggunakan `cargo new`.
- Kita dapat membangun proyek menggunakan `cargo build`.
- Kita dapat membangun dan menjalankan proyek dalam satu langkah
  menggunakan `cargo run`.
- Kita dapat membangun proyek tanpa menghasilkan file biner untuk
  memeriksa error menggunakan `cargo check`.
- Alih-alih menyimpan hasil build di direktori yang sama dengan kode
  kita, Cargo menyimpannya di direktori _target/debug_.

Keuntungan tambahan memakai Cargo adalah perintah-perintahnya sama apa pun
sistem operasi yang Anda pakai. Jadi, mulai saat ini, kita tidak akan lagi
memberikan petunjuk khusus untuk Linux dan macOS versus Windows.

### Membangun untuk Rilis

Ketika proyek Anda akhirnya siap untuk dirilis, Anda dapat memakai
`cargo build --release` untuk mengompilasinya dengan optimasi. Perintah
ini akan membuat file eksekutabel di _target/release_ alih-alih
_target/debug_. Optimasi membuat kode Rust Anda berjalan lebih cepat,
tetapi mengaktifkannya memperpanjang waktu yang dibutuhkan untuk
mengompilasi program Anda. Inilah alasan adanya dua profil yang berbeda:
satu untuk pengembangan, saat Anda ingin membangun ulang dengan cepat dan
sering, dan satu lagi untuk membangun program akhir yang akan Anda berikan
kepada pengguna, yang tidak akan dibangun ulang berulang kali dan akan
berjalan secepat mungkin. Jika Anda melakukan benchmark terhadap waktu
berjalan kode Anda, pastikan untuk menjalankan `cargo build --release` dan
melakukan benchmark dengan file eksekutabel di _target/release_.

<!-- Old headings. Do not remove or links may break. -->
<a id="cargo-as-convention"></a>

### Memanfaatkan Konvensi Cargo

Pada proyek-proyek sederhana, Cargo tidak memberikan banyak nilai
dibandingkan sekadar memakai `rustc`, tetapi nilainya akan terbukti saat
program Anda semakin rumit. Begitu program tumbuh menjadi banyak file atau
membutuhkan dependensi, jauh lebih mudah membiarkan Cargo mengoordinasikan
build-nya.

Meskipun proyek `hello_cargo` sederhana, proyek ini kini memakai banyak
perangkat nyata yang akan Anda pakai selama sisa karier Rust Anda. Bahkan,
untuk mengerjakan proyek mana pun yang sudah ada, Anda dapat memakai
perintah-perintah berikut untuk mengambil kode menggunakan Git, berpindah
ke direktori proyek itu, lalu membangunnya:

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

Untuk informasi lebih lanjut tentang Cargo, lihat [dokumentasinya][cargo].

## Ringkasan

Anda sudah memulai perjalanan Rust Anda dengan sangat baik! Di bab ini,
Anda telah belajar cara:

- Memasang versi stabil terbaru Rust menggunakan `rustup`.
- Memperbarui ke versi Rust yang lebih baru.
- Membuka dokumentasi yang terpasang secara lokal.
- Menulis dan menjalankan program “Hello, world!” menggunakan `rustc`
  secara langsung.
- Membuat dan menjalankan proyek baru menggunakan konvensi Cargo.

Ini saat yang tepat untuk membangun program yang lebih substansial agar
terbiasa membaca dan menulis kode Rust. Jadi, di Bab 2, kita akan
membangun program permainan tebak angka. Jika Anda lebih suka memulai
dengan mempelajari cara kerja konsep-konsep pemrograman yang umum di Rust,
lihat Bab 3, lalu kembali lagi ke Bab 2.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/
