# Memprogram Permainan Tebak Angka

Mari kita langsung menyelami Rust dengan mengerjakan sebuah proyek praktik
bersama-sama! Bab ini memperkenalkan Anda pada beberapa konsep Rust yang umum
dengan menunjukkan cara memakainya di program sungguhan. Anda akan belajar
tentang `let`, `match`, method, *associated function* (fungsi asosiasi),
*crate* eksternal, dan lainnya! Di bab-bab berikutnya, kita akan
mengeksplorasi gagasan-gagasan ini lebih detail. Di bab ini, Anda hanya akan
berlatih dasarnya.

Kita akan mengimplementasikan masalah pemrograman klasik untuk pemula:
permainan tebak angka. Begini cara kerjanya: Program akan menghasilkan
integer acak antara 1 dan 100. Lalu, program akan meminta pemain untuk
memasukkan tebakan. Setelah tebakan dimasukkan, program akan menunjukkan
apakah tebakan itu terlalu rendah atau terlalu tinggi. Jika tebakan benar,
permainan akan mencetak pesan ucapan selamat dan berhenti.

## Menyiapkan Proyek Baru

Untuk menyiapkan proyek baru, buka direktori _projects_ yang Anda buat di
Bab 1 dan buat proyek baru menggunakan Cargo, seperti ini:

```console
$ cargo new guessing_game
$ cd guessing_game
```

Perintah pertama, `cargo new`, menerima nama proyek (`guessing_game`)
sebagai argumen pertamanya. Perintah kedua berpindah ke direktori proyek
baru tersebut.

Lihatlah file _Cargo.toml_ yang dihasilkan:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">Nama File: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

Seperti yang Anda lihat di Bab 1, `cargo new` menghasilkan program
“Hello, world!” untuk Anda. Periksa file _src/main.rs_-nya:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

Sekarang mari kita kompilasi program “Hello, world!” ini dan jalankan
dalam satu langkah menggunakan perintah `cargo run`:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

Perintah `run` sangat berguna ketika Anda perlu melakukan iterasi pada
proyek secara cepat, seperti yang akan kita lakukan pada permainan ini,
dengan cepat menguji tiap iterasi sebelum melanjutkan ke yang berikutnya.

Buka lagi file _src/main.rs_. Anda akan menulis semua kode di file ini.

## Memproses Tebakan

Bagian pertama dari program permainan tebak angka akan meminta input dari
pengguna, memproses input tersebut, dan memeriksa bahwa inputnya sesuai
dengan bentuk yang diharapkan. Untuk memulainya, kita akan mengizinkan
pemain memasukkan sebuah tebakan. Masukkan kode di Listing 2-1 ke
_src/main.rs_.

<Listing number="2-1" file-name="src/main.rs" caption="Kode yang mengambil tebakan dari pengguna dan mencetaknya">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

Kode ini memuat banyak informasi, jadi mari kita bahas baris per baris.
Untuk mendapatkan user input lalu mencetak hasilnya sebagai output,
kita perlu membawa pustaka input/output `io` ke dalam *scope*
(cakupan). Pustaka `io` berasal dari standard library, yang dikenal sebagai
`std`:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

Secara bawaan, Rust memiliki sekumpulan item yang didefinisikan di pustaka
standar dan dibawa ke dalam *scope* setiap program. Kumpulan ini disebut
*prelude*, dan Anda dapat melihat semuanya [di dokumentasi pustaka
standar][prelude].

Jika type yang ingin Anda pakai tidak ada di dalam *prelude*, Anda harus
membawa type itu ke dalam *scope* secara eksplisit dengan statement `use`.
Memakai pustaka `std::io` memberi Anda sejumlah fitur berguna, termasuk
kemampuan untuk menerima user input.

Seperti yang Anda lihat di Bab 1, fungsi `main` adalah titik masuk ke
dalam program:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

Sintaks `fn` mendeklarasikan fungsi baru; tanda kurung, `()`, menandakan
tidak ada parameter; dan kurung kurawal, `{`, mengawali badan fungsi.

Seperti yang juga Anda pelajari di Bab 1, `println!` adalah makro yang
mencetak string ke layar:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

Kode ini mencetak prompt yang menyatakan apa permainan ini dan meminta
input dari pengguna.

<a id="storing-values-with-variables"></a>
### Menyimpan Nilai dengan Variable

Berikutnya, kita akan membuat variable untuk menyimpan user input,
seperti ini:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

Sekarang programnya mulai menarik! Banyak hal yang terjadi pada baris
kecil ini. Kita memakai statement `let` untuk membuat variablenya. Berikut
contoh lainnya:

```rust,ignore
let apples = 5;
```

Baris ini membuat variable baru bernama `apples` dan mengikatnya ke nilai
`5`. Di Rust, variable bersifat *immutable* (tidak dapat diubah) secara
bawaan, artinya begitu kita memberikan nilai ke variable, nilainya tidak
akan berubah. Kita akan membahas konsep ini secara detail di bagian
[“Variable dan Mutability”][variables-and-mutability]<!-- ignore -->
pada Bab 3. Untuk membuat variable menjadi *mutable* (dapat diubah), kita
menambahkan `mut` sebelum nama variablenya:

```rust,ignore
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> Catatan: Sintaks `//` mengawali komentar yang berlanjut sampai akhir
> baris. Rust mengabaikan semua yang ada di dalam komentar. Kita akan
> membahas komentar lebih detail di [Bab 3][comments]<!-- ignore -->.

Kembali ke program permainan tebak angka, sekarang Anda tahu bahwa
`let mut guess` akan memperkenalkan variable *mutable* bernama `guess`.
Tanda sama dengan (`=`) memberi tahu Rust bahwa kita ingin mengikat sesuatu
ke variable itu sekarang. Di sebelah kanan tanda sama dengan terdapat nilai
yang diikat ke `guess`, yaitu hasil dari memanggil `String::new`, fungsi
yang mengembalikan instance baru dari `String`. [`String`][string]<!--
ignore --> adalah type string yang disediakan standard library berupa teks
yang dapat bertambah dan terenkode UTF-8.

Sintaks `::` pada baris `::new` menandakan bahwa `new` adalah *associated
function* dari type `String`. *Associated function* adalah fungsi yang
diimplementasikan pada sebuah type, dalam hal ini `String`. Fungsi `new`
ini membuat string baru yang kosong. Anda akan menemukan fungsi `new` pada
banyak type karena itu adalah nama yang umum untuk fungsi yang membuat
nilai baru dari jenis tertentu.

Secara lengkap, baris `let mut guess = String::new();` telah membuat
variable *mutable* yang saat ini terikat pada instance baru `String` yang
kosong. Fiuh!

### Menerima Input Pengguna

Ingat bahwa kita menyertakan fungsionalitas input/output dari pustaka
standar dengan `use std::io;` pada baris pertama program. Sekarang kita
akan memanggil fungsi `stdin` dari *module* (modul) `io`, yang akan
memungkinkan kita menangani user input:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

Jika kita tidak mengimpor *module* `io` dengan `use std::io;` di awal
program, kita tetap bisa memakai fungsi itu dengan menulis pemanggilannya
sebagai `std::io::stdin`. Fungsi `stdin` mengembalikan instance
[`std::io::Stdin`][iostdin]<!-- ignore -->, yaitu type yang
merepresentasikan handle ke standard input untuk terminal Anda.

Berikutnya, baris `.read_line(&mut guess)` memanggil method
[`read_line`][read_line]<!-- ignore --> pada handle standard input untuk
mendapatkan input dari pengguna. Kita juga meneruskan `&mut guess`
sebagai argumen ke `read_line` untuk memberi tahu string mana yang akan
dipakai untuk menyimpan user input. Tugas penuh `read_line` adalah
mengambil apa pun yang diketik pengguna ke standard input dan
menambahkannya ke sebuah string (tanpa menimpa isinya), jadi karena itulah
kita meneruskan string tersebut sebagai argumen. Argumen string itu harus
*mutable* agar methodnya dapat mengubah isi string tersebut.

Tanda `&` menandakan bahwa argumen ini adalah sebuah *reference*
(referensi), yang memberi Anda cara untuk memungkinkan banyak bagian kode
mengakses satu data tanpa perlu menyalin data itu ke memori berkali-kali.
*Reference* adalah fitur yang kompleks, dan salah satu keunggulan utama Rust
adalah betapa aman dan mudahnya memakai *reference*. Anda tidak perlu tahu
banyak detail itu untuk menyelesaikan program ini. Untuk saat ini, yang
perlu Anda ketahui hanyalah bahwa, seperti variable, *reference* bersifat
*immutable* secara bawaan. Karena itu, Anda perlu menulis `&mut guess`
alih-alih `&guess` untuk membuatnya *mutable*. (Bab 4 akan menjelaskan
*reference* lebih tuntas.)

<!-- Old headings. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>

<a id="handling-potential-failure-with-result"></a>
### Menangani Kemungkinan Kegagalan dengan `Result`

Kita masih mengerjakan baris kode ini. Sekarang kita membahas baris teks
ketiga, tetapi perhatikan bahwa baris itu masih bagian dari satu baris
kode logis yang sama. Bagian berikutnya adalah method ini:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```

Kita sebenarnya bisa menulis kode ini sebagai:

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

Namun, satu baris panjang sulit dibaca, jadi sebaiknya dibagi. Sering kali
bijak untuk menyisipkan baris baru dan whitespace lain untuk membantu memecah
baris-baris panjang ketika Anda memanggil method dengan sintaks
`.method_name()`. Sekarang mari kita bahas apa yang dilakukan baris ini.

Seperti yang disebutkan sebelumnya, `read_line` memasukkan apa pun yang
diketik pengguna ke string yang kita berikan, tetapi ia juga mengembalikan
nilai `Result`. [`Result`][result]<!-- ignore --> adalah
[_enumeration_][enums]<!-- ignore --> (enumerasi), yang sering disebut
*enum*, yaitu type yang dapat berada pada salah satu dari beberapa keadaan
yang mungkin. Setiap keadaan yang mungkin itu kita sebut *variant*
(varian).

[Bab 6][enums]<!-- ignore --> akan membahas *enum* lebih detail. Tujuan
type-type `Result` ini adalah untuk mengodekan informasi penanganan error.

*Variant* `Result` adalah `Ok` dan `Err`. *Variant* `Ok` menandakan
operasinya berhasil, dan ia memuat nilai yang berhasil dihasilkan.
*Variant* `Err` berarti operasinya gagal, dan ia memuat informasi tentang
bagaimana atau mengapa operasi itu gagal.

Nilai typed `Result`, seperti nilai dari type mana pun, memiliki method
yang didefinisikan padanya. Sebuah instance `Result` memiliki [method
`expect`][expect]<!-- ignore --> yang dapat Anda panggil. Jika instance
`Result` ini bernilai `Err`, `expect` akan membuat program crash dan
menampilkan pesan yang Anda berikan sebagai argumen ke `expect`. Jika
method `read_line` mengembalikan `Err`, kemungkinan besar itu akibat error
yang berasal dari sistem operasi yang mendasarinya. Jika instance `Result`
ini bernilai `Ok`, `expect` akan mengambil nilai balik yang dipegang `Ok`
dan mengembalikan nilai itu saja kepada Anda sehingga Anda dapat
memakainya. Dalam kasus ini, nilai itu adalah jumlah byte dalam input
pengguna.

Jika Anda tidak memanggil `expect`, program akan terkompilasi, tetapi Anda
akan mendapat peringatan:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

Rust memperingatkan bahwa Anda belum memakai nilai `Result` yang
dikembalikan `read_line`, menandakan bahwa program belum menangani error
yang mungkin terjadi.

Cara yang benar untuk meredam peringatan itu adalah menulis kode
penanganan error yang sesungguhnya, tetapi dalam kasus kita, kita hanya
ingin membuat program ini crash saat terjadi masalah, jadi kita dapat
memakai `expect`. Anda akan belajar tentang pemulihan dari error di
[Bab 9][recover]<!-- ignore -->.

### Mencetak Nilai dengan Placeholder `println!`

Selain kurung kurawal penutup, hanya ada satu baris lagi yang perlu
dibahas dari kode sejauh ini:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

Baris ini mencetak string yang kini berisi user input. Kumpulan
kurung kurawal `{}` adalah placeholder: Bayangkan `{}` sebagai capit
kepiting kecil yang menahan nilai di tempatnya. Saat mencetak nilai sebuah
variable, nama variablenya dapat dimasukkan ke dalam kurung kurawal. Saat
mencetak hasil evaluasi sebuah expression, letakkan kurung kurawal kosong
pada string format, lalu ikuti string format itu dengan daftar expression
yang dipisahkan koma untuk dicetak ke setiap placeholder kurung kurawal
kosong dengan urutan yang sama. Mencetak sebuah variable dan hasil sebuah
expression dalam satu pemanggilan `println!` akan tampak seperti ini:

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

Kode ini akan mencetak `x = 5 and y + 2 = 12`.

### Menguji Bagian Pertama

Mari kita uji bagian pertama dari permainan tebak angka. Jalankan dengan
`cargo run`:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

Pada titik ini, bagian pertama permainan sudah selesai: Kita mendapatkan
input dari keyboard lalu mencetaknya.

## Menghasilkan Angka Rahasia

Berikutnya, kita perlu menghasilkan angka rahasia yang akan coba ditebak
pengguna. Angka rahasia harus berbeda setiap kali supaya permainannya seru
dimainkan lebih dari sekali. Kita akan memakai angka acak antara 1 dan 100
supaya permainannya tidak terlalu sulit. Rust belum menyertakan
fungsionalitas angka acak di standard librarynya. Namun, tim Rust
menyediakan [crate `rand`][randcrate]<!-- ignore --> dengan fungsionalitas
tersebut.

<!-- Old headings. Do not remove or links may break. -->
<a id="using-a-crate-to-get-more-functionality"></a>

### Menambah Fungsionalitas dengan Crate

Ingat bahwa *crate* adalah kumpulan file kode sumber Rust. Proyek yang
sedang kita bangun adalah *crate* biner, yaitu sebuah file yang dapat
dieksekusi. *Crate* `rand` adalah *crate* pustaka, yang berisi kode yang
dimaksudkan untuk dipakai di program lain dan tidak dapat dieksekusi
sendiri.

Koordinasi *crate* eksternal adalah tempat Cargo benar-benar bersinar.
Sebelum kita bisa menulis kode yang memakai `rand`, kita perlu mengubah
file _Cargo.toml_ untuk menyertakan *crate* `rand` sebagai dependency. Buka
file itu sekarang dan tambahkan baris berikut ke bagian bawah, di bawah
judul seksi `[dependencies]` yang dibuat Cargo untuk Anda. Pastikan untuk
menuliskan `rand` persis seperti di sini, dengan nomor versi ini, atau
contoh kode dalam tutorial ini mungkin tidak akan bekerja:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

<span class="filename">Nama File: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

Di file _Cargo.toml_, semua yang mengikuti sebuah judul adalah bagian dari
seksi itu, yang berlanjut sampai seksi lain dimulai. Di `[dependencies]`,
Anda memberi tahu Cargo *crate* eksternal mana yang menjadi dependency proyek
Anda dan versi *crate* mana yang Anda butuhkan. Dalam kasus ini, kita
menentukan *crate* `rand` dengan spesifikasi versi semantik `0.10.1`. Cargo
memahami [Semantic Versioning][semver]<!-- ignore --> (kadang disebut
_SemVer_), yaitu standar untuk menulis nomor versi. Spesifikasi `0.10.1`
sebenarnya adalah singkatan dari `^0.10.1`, yang berarti versi apa pun yang
sekurang-kurangnya 0.10.1 tetapi di bawah 0.11.0.

Cargo menganggap versi-versi ini memiliki API publik yang kompatibel dengan
versi 0.10.1, dan spesifikasi ini menjamin bahwa Anda akan mendapat rilis
patch terbaru yang tetap terkompilasi dengan kode di bab ini. Versi 0.11.0
atau yang lebih tinggi tidak dijamin memiliki API yang sama dengan yang
dipakai contoh-contoh berikut.

Sekarang, tanpa mengubah kode apa pun, mari kita membangun proyeknya, seperti
yang ditunjukkan pada Listing 2-2.

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
rm Cargo.lock
cargo clean
cargo build -->

<Listing number="2-2" caption="Output dari menjalankan `cargo build` setelah menambahkan crate `rand` sebagai dependency">

```console
$ cargo build
    Updating crates.io index
     Locking 8 packages to latest Rust 1.96.0 compatible versions
  Downloaded rand_core v0.10.1
  Downloaded chacha20 v0.10.1
  Downloaded rand v0.10.1
  Downloaded 3 crates (162.9KiB) in 0.59s
   Compiling libc v0.2.186
   Compiling rand_core v0.10.1
   Compiling getrandom v0.4.3
   Compiling cfg-if v1.0.4
   Compiling chacha20 v0.10.1
   Compiling rand v0.10.1
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.03s
```

</Listing>

Anda mungkin melihat nomor versi yang berbeda (tetapi semuanya akan
kompatibel dengan kodenya, berkat SemVer!) dan baris-baris yang berbeda
(tergantung sistem operasi), dan baris-barisnya mungkin dalam urutan yang
berbeda.

Ketika kita menyertakan dependency eksternal, Cargo mengambil versi
terbaru dari semua yang dibutuhkan dependency itu dari *registry*
(registri), yang merupakan copy data dari [*Crates*.io][cratesio].
*Crates*.io adalah tempat orang-orang di ekosistem Rust memublikasikan proyek
Rust open source mereka untuk dipakai orang lain.

Setelah memperbarui *registry*, Cargo memeriksa seksi `[dependencies]` dan
mengunduh *crate* apa pun yang terdaftar dan belum diunduh. Dalam kasus ini,
meskipun kita hanya mendaftarkan `rand` sebagai dependency, Cargo juga
mengambil *crate* lain yang dibutuhkan `rand` agar bisa bekerja. Setelah
mengunduh *crate*-crate tersebut, Rust mengompilasinya, lalu mengompilasi
proyek dengan dependency yang tersedia.

Jika Anda langsung menjalankan `cargo build` lagi tanpa mengubah apa pun,
Anda tidak akan mendapat output apa pun selain baris `Finished`. Cargo
tahu bahwa ia telah mengunduh dan mengompilasi dependencynya, dan Anda
belum mengubah apa pun tentang dependency itu di file _Cargo.toml_ Anda.
Cargo juga tahu bahwa Anda belum mengubah apa pun pada kode Anda, jadi ia
tidak mengompilasi ulang kode itu juga. Karena tidak ada yang perlu
dikerjakan, ia langsung berhenti.

Jika Anda membuka file _src/main.rs_, membuat perubahan sepele, lalu
menyimpannya dan menjalankan build lagi, Anda hanya akan melihat dua baris
output:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
touch src/main.rs
cargo build -->

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

Baris-baris ini menunjukkan bahwa Cargo hanya memperbarui build dengan
perubahan kecil Anda pada file _src/main.rs_. Dependency Anda belum
berubah, jadi Cargo tahu bahwa ia dapat memakai ulang apa yang telah
diunduh dan dikompilasi untuk dependency itu.

<!-- Old headings. Do not remove or links may break. -->
<a id="ensuring-reproducible-builds-with-the-cargo-lock-file"></a>

#### Menjamin Build yang Dapat Direproduksi

Cargo memiliki mekanisme yang menjamin bahwa Anda dapat membangun ulang
artefak yang sama setiap kali Anda atau siapa pun membangun kode Anda:
Cargo hanya akan memakai versi dependency yang Anda tentukan sampai Anda
menyatakan sebaliknya. Misalnya, katakanlah minggu depan versi 0.10.2 dari
*crate* `rand` dirilis, dan versi itu memuat perbaikan bug yang penting,
tetapi juga memuat regression yang akan merusak kode Anda. Untuk menangani
ini, Rust membuat file _Cargo.lock_ saat pertama kali Anda menjalankan
`cargo build`, jadi sekarang kita punya file ini di direktori
_guessing_game_.

Ketika Anda membangun proyek untuk pertama kalinya, Cargo mencari tahu
semua versi dependency yang memenuhi kriteria lalu menuliskannya ke file
_Cargo.lock_. Ketika Anda membangun proyek di masa depan, Cargo akan
melihat bahwa file _Cargo.lock_ sudah ada dan akan memakai versi-versi
yang ditentukan di sana alih-alih melakukan semua pekerjaan mencari tahu
versi lagi. Ini memungkinkan Anda mendapatkan build yang dapat
direproduksi secara otomatis. Dengan kata lain, proyek Anda akan tetap
berada di 0.10.1 sampai Anda menaikkannya secara eksplisit, berkat file
_Cargo.lock_. Karena file _Cargo.lock_ penting untuk build yang dapat
direproduksi, file ini sering ikut dimasukkan ke kontrol sumber bersama
kode lain di proyek Anda.

#### Memperbarui Crate untuk Mendapat Versi Baru

Ketika Anda _memang_ ingin memperbarui crate, Cargo menyediakan perintah
`update`, yang akan mengabaikan file _Cargo.lock_ dan mencari tahu semua
versi terbaru yang sesuai dengan spesifikasi Anda di _Cargo.toml_. Cargo
kemudian akan menulis versi-versi itu ke file _Cargo.lock_. Jika tidak
demikian, secara bawaan, Cargo hanya akan mencari versi yang lebih besar dari 0.10.1
dan kurang dari 0.11.0. Jika crate `rand` telah merilis dua versi baru
0.10.2 dan 0.999.0, Anda akan melihat yang berikut jika menjalankan
`cargo update`:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.96.0 compatible version
    Updating rand v0.10.1 -> v0.10.2 (available: v0.999.0)
```

Cargo mengabaikan rilis 0.999.0. Pada titik ini, Anda juga akan melihat
perubahan pada file _Cargo.lock_ Anda yang mencatat bahwa versi crate
`rand` yang sekarang Anda pakai adalah 0.10.2. Untuk memakai `rand` versi
0.999.0 atau versi mana pun dalam seri 0.999._x_, Anda harus mengubah file
_Cargo.toml_ agar tampak seperti ini (jangan benar-benar melakukan
perubahan ini karena contoh-contoh berikutnya mengasumsikan Anda memakai
`rand` 0.10):

```toml
[dependencies]
rand = "0.999.0"
```

Saat berikutnya Anda menjalankan `cargo build`, Cargo akan memperbarui
*registry* crate yang tersedia dan mengevaluasi ulang kebutuhan `rand`
Anda sesuai versi baru yang Anda tentukan.

Masih banyak yang bisa dibahas tentang [Cargo][doccargo]<!-- ignore --> dan
[ekosistemnya][doccratesio]<!-- ignore -->, yang akan kita bahas di Bab 14,
tetapi untuk sekarang, itu saja yang perlu Anda ketahui. Cargo membuat
pemakaian ulang pustaka menjadi sangat mudah, sehingga para Rustaceans
mampu menulis proyek-proyek yang lebih kecil yang dirangkai dari sejumlah
*package* (paket).

<a id="generating-a-random-number"></a>
### Menghasilkan Angka Acak

Mari kita mulai memakai `rand` untuk menghasilkan angka yang akan ditebak.
Langkah berikutnya adalah memperbarui _src/main.rs_, seperti yang
ditunjukkan pada Listing 2-3.

<Listing number="2-3" file-name="src/main.rs" caption="Menambahkan kode untuk menghasilkan angka acak">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

Pertama, kita menambahkan baris `use rand::prelude::*;`. *Module*
`prelude` memuat bagian-bagian yang paling sering dipakai dari *crate*
`rand`, dan `use` membuat item-item itu tersedia di *scope* program kita.

Berikutnya, kita menambahkan dua baris di tengah. Pada baris pertama, kita
memanggil fungsi `rand::rng` yang memberi kita random number generator
tertentu yang akan kita pakai: pembangkit yang lokal untuk thread eksekusi
saat ini dan di-seed oleh sistem operasi. Kemudian, kita memanggil method
`random_range` pada random number generator itu. Method ini didefinisikan
oleh *trait* `RngExt` yang merupakan bagian dari *module* `rand::prelude`
yang kita bawa ke dalam *scope* dengan statement `use rand::prelude::*;`.
Method `random_range` menerima expression range sebagai argumen dan
menghasilkan angka acak dalam range tersebut. Jenis expression range yang
kita pakai di sini berbentuk `start..=end` dan bersifat inklusif pada
batas bawah dan atasnya, jadi kita perlu menentukan `1..=100` untuk
meminta angka antara 1 dan 100.

> Catatan: Anda tidak akan langsung tahu apa yang harus dibawa ke dalam
> *scope* dan method serta fungsi apa yang harus dipanggil dari sebuah
> *crate*, jadi setiap *crate* memiliki dokumentasi berisi petunjuk
> pemakaiannya. Fitur rapi lain dari Cargo adalah bahwa menjalankan
> perintah `cargo doc --open` akan membangun dokumentasi yang disediakan
> semua dependency Anda secara lokal dan membukanya di peramban Anda.
> Misalnya, jika Anda tertarik pada fungsionalitas lain di *crate* `rand`,
> jalankan `cargo doc --open` dan klik `rand` di bilah sisi sebelah kiri.

Baris baru kedua mencetak angka rahasia. Ini berguna selagi kita
mengembangkan program agar bisa mengujinya, tetapi kita akan menghapusnya
dari versi final. Bukan permainan namanya jika program mencetak jawabannya
begitu dimulai!

Coba jalankan programnya beberapa kali:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

Anda seharusnya mendapat angka acak yang berbeda-beda, dan semuanya harus
berupa angka antara 1 dan 100. Jika Anda mendapat peringatan, peringatan
itu aman untuk diabaikan. Jika Anda mendapat error, periksa bahwa Anda
memiliki `rand = "0.10.1"` di *Cargo.toml* Anda, karena versi `rand` di
masa depan mungkin memiliki API yang berbeda, tetapi versi mana pun dalam
seri `0.10` seharusnya bekerja dengan kode di bab ini.

<a id="comparing-the-guess-to-the-secret-number"></a>
## Membandingkan Tebakan dengan Angka Rahasia

Sekarang setelah kita memiliki user input dan angka acak, kita dapat
membandingkan keduanya. Langkah itu ditunjukkan pada Listing 2-4.
Perhatikan bahwa kode ini belum akan terkompilasi, seperti yang akan kita
jelaskan.

<Listing number="2-4" file-name="src/main.rs" caption="Menangani return value yang mungkin dari perbandingan dua angka">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

Pertama, kita menambahkan statement `use` lain, membawa type bernama
`std::cmp::Ordering` ke dalam *scope* dari standard library. Type
`Ordering` adalah *enum* lain dan memiliki *variant* `Less`, `Greater`, dan
`Equal`. Ketiganya adalah tiga kemungkinan hasil ketika Anda membandingkan
dua nilai.

Kemudian, kita menambahkan lima baris baru di bagian bawah yang memakai
type `Ordering`. Method `cmp` membandingkan dua nilai dan dapat dipanggil
pada apa pun yang dapat dibandingkan. Method ini menerima sebuah
*reference* ke apa pun yang ingin Anda bandingkan dengannya: Di sini, ia
membandingkan `guess` dengan `secret_number`. Lalu, ia mengembalikan
*variant* dari *enum* `Ordering` yang kita bawa ke dalam *scope* dengan
statement `use`. Kita memakai expression [`match`][match]<!-- ignore -->
untuk memutuskan apa yang harus dilakukan berikutnya berdasarkan *variant*
`Ordering` mana yang dikembalikan dari pemanggilan `cmp` dengan nilai di
`guess` dan `secret_number`.

Sebuah expression `match` terdiri atas *arm* (lengan). Sebuah *arm* terdiri
atas sebuah pattern untuk dicocokkan, dan kode yang harus dijalankan jika
nilai yang diberikan ke `match` sesuai dengan pattern *arm* tersebut. Rust
mengambil nilai yang diberikan ke `match` dan memeriksa pattern tiap *arm*
secara bergiliran. Pattern dan konstruksi `match` adalah fitur Rust yang
ampuh: Keduanya memungkinkan Anda mengekspresikan berbagai situasi yang
mungkin dihadapi kode Anda, dan memastikan Anda menangani semuanya.
Fitur-fitur ini akan dibahas secara detail masing-masing di Bab 6 dan
Bab 19.

Mari kita telusuri sebuah contoh dengan expression `match` yang kita pakai
di sini. Katakanlah pengguna menebak 50 dan angka rahasia yang dihasilkan
secara acak kali ini adalah 38.

Ketika kode membandingkan 50 dengan 38, method `cmp` akan mengembalikan
`Ordering::Greater` karena 50 lebih besar daripada 38. Expression `match`
menerima nilai `Ordering::Greater` dan mulai memeriksa pattern tiap *arm*. Ia
melihat pattern *arm* pertama, `Ordering::Less`, dan melihat bahwa nilai
`Ordering::Greater` tidak cocok dengan `Ordering::Less`, jadi ia
mengabaikan kode di *arm* itu dan berpindah ke *arm* berikutnya. Pattern
*arm* berikutnya adalah `Ordering::Greater`, yang _memang_ cocok dengan
`Ordering::Greater`! Kode terkait di *arm* itu akan dieksekusi dan
mencetak `Too big!` ke layar. Expression `match` berakhir setelah kecocokan
pertama yang berhasil, jadi ia tidak akan melihat *arm* terakhir dalam
skenario ini.

Namun, kode di Listing 2-4 belum akan terkompilasi. Mari kita coba:

<!--
The error numbers in this output should be that of the code **WITHOUT** the
anchor or snip comments
-->

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

Inti errornya menyatakan bahwa terdapat _tipe yang tidak cocok_. Rust
memiliki type system statis yang kuat. Namun, ia juga memiliki inferensi
type. Ketika kita menulis `let mut guess = String::new()`, Rust mampu
menyimpulkan bahwa `guess` harus berupa `String` dan tidak memaksa kita
menulis typenya. Sebaliknya, `secret_number` adalah numeric type. Beberapa
numeric type Rust dapat memiliki nilai antara 1 dan 100: `i32`, angka
32-bit; `u32`, angka 32-bit tak bertanda; `i64`, angka 64-bit; serta
lainnya. Kecuali ditentukan lain, Rust secara bawaan memilih `i32`, yang
merupakan type `secret_number` kecuali Anda menambahkan informasi type di
tempat lain yang akan membuat Rust menyimpulkan numeric type yang berbeda.
Alasan terjadinya error adalah Rust tidak dapat membandingkan string
dengan numeric type.

Pada akhirnya, kita ingin mengonversi `String` yang dibaca program sebagai
input menjadi numeric type supaya kita dapat membandingkannya secara
numerik dengan angka rahasia. Kita melakukannya dengan menambahkan baris
ini ke badan fungsi `main`:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

Barisnya adalah:

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

Kita membuat variable bernama `guess`. Tetapi tunggu, bukankah programnya
sudah memiliki variable bernama `guess`? Memang, tetapi untungnya Rust
mengizinkan kita melakukan *shadowing* terhadap nilai `guess` sebelumnya
dengan nilai baru. *Shadowing* memungkinkan kita memakai ulang nama
variable `guess` alih-alih memaksa kita membuat dua variable unik, seperti
`guess_str` dan `guess`, misalnya. Kita akan membahasnya lebih detail di
[Bab 3][shadowing]<!-- ignore -->, tetapi untuk sekarang, ketahuilah bahwa
fitur ini sering dipakai ketika Anda ingin mengonversi nilai dari satu
type ke type lain.

Kita mengikat variable baru ini ke expression `guess.trim().parse()`.
`guess` dalam expression itu merujuk ke variable `guess` asli yang berisi
input sebagai string. Method `trim` pada instance `String` akan
menghapus whitespace apa pun di awal dan akhir, yang harus kita lakukan sebelum
kita dapat mengonversi string itu ke `u32`, yang hanya dapat memuat data
numerik. Pengguna harus menekan <kbd>enter</kbd> untuk memenuhi
`read_line` dan memasukkan tebakannya, yang menambahkan karakter newline
ke string. Misalnya, jika pengguna mengetik <kbd>5</kbd> dan menekan
<kbd>enter</kbd>, `guess` tampak seperti ini: `5\n`. `\n` mewakili
“newline”. (Di Windows, menekan <kbd>enter</kbd> menghasilkan carriage
return dan newline, `\r\n`.) Method `trim` menghapus `\n` atau `\r\n`,
sehingga hasilnya hanya `5`.

[Method `parse` pada string][parse]<!-- ignore --> mengonversi string ke
type lain. Di sini, kita memakainya untuk mengonversi dari string ke
angka. Kita perlu memberi tahu Rust numeric type persis yang kita inginkan
dengan memakai `let guess: u32`. Titik dua (`:`) setelah `guess` memberi
tahu Rust bahwa kita akan mengtype annotation variablenya. Rust memiliki
beberapa numeric type bawaan; `u32` yang terlihat di sini adalah integer
32-bit tak bertanda. Ini pilihan bawaan yang bagus untuk angka positif
kecil. Anda akan belajar tentang numeric type lainnya di
[Bab 3][integers]<!-- ignore -->.

Selain itu, anotasi `u32` dalam contoh program ini dan perbandingan dengan
`secret_number` berarti Rust akan menyimpulkan bahwa `secret_number` juga
harus berupa `u32`. Jadi, sekarang perbandingannya akan terjadi antara dua
nilai dengan type yang sama!

Method `parse` hanya akan bekerja pada karakter yang secara logis dapat
dikonversi menjadi angka sehingga ia dapat dengan mudah menyebabkan error.
Jika, misalnya, string berisi `A👍%`, tidak akan ada cara untuk
mengonversinya menjadi angka. Karena ia mungkin gagal, method `parse`
mengembalikan type `Result`, sama seperti yang dilakukan method
`read_line` (dibahas sebelumnya di [“Menangani Kemungkinan Kegagalan
dengan `Result`”](#handling-potential-failure-with-result)<!-- ignore -->).
Kita akan memperlakukan `Result` ini dengan cara yang sama, yaitu memakai
method `expect` lagi. Jika `parse` mengembalikan *variant* `Result` `Err`
karena ia tidak dapat membuat angka dari string itu, pemanggilan `expect`
akan membuat permainan crash dan mencetak pesan yang kita berikan. Jika
`parse` dapat mengonversi string menjadi angka, ia akan mengembalikan
*variant* `Ok` dari `Result`, dan `expect` akan mengembalikan angka yang
kita inginkan dari nilai `Ok` itu.

Mari kita jalankan programnya sekarang:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/
touch src/main.rs
cargo run
  76
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

Bagus! Meskipun ada spasi yang ditambahkan sebelum tebakan, program tetap
mengetahui bahwa pengguna menebak 76. Jalankan program beberapa kali untuk
memverifikasi perilaku yang berbeda dengan berbagai jenis input: Tebak
angkanya dengan benar, tebak angka yang terlalu tinggi, dan tebak angka
yang terlalu rendah.

Sebagian besar permainan sudah bekerja sekarang, tetapi pengguna hanya
bisa menebak satu kali. Mari kita ubah itu dengan menambahkan loop!

## Mengizinkan Beberapa Tebakan dengan Loop

*keyword* `loop` membuat infinite loop. Kita akan menambahkan
loop untuk memberi pengguna lebih banyak kesempatan menebak
angkanya:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

Seperti yang Anda lihat, kita telah memindahkan semuanya dari prompt
input tebakan dan seterusnya ke dalam loop. Pastikan untuk
mengindentasi baris-baris di dalam loop sebanyak empat spasi
tambahan masing-masing dan jalankan lagi programnya. Programnya sekarang
akan meminta tebakan lain selamanya, yang justru menimbulkan masalah baru.
Tampaknya pengguna tidak bisa berhenti!

Pengguna selalu dapat menyela program dengan memakai pintasan keyboard
<kbd>ctrl</kbd>-<kbd>C</kbd>. Tetapi ada cara lain untuk lolos dari
monster yang tak pernah kenyang ini, seperti yang disebutkan pada
pembahasan `parse` di [“Membandingkan Tebakan dengan Angka
Rahasia”](#comparing-the-guess-to-the-secret-number)<!-- ignore -->: Jika
pengguna memasukkan jawaban non-angka, programnya akan crash. Kita dapat
memanfaatkan itu untuk mengizinkan pengguna berhenti, seperti yang
ditunjukkan di sini:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' (6694925) panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Mengetik `quit` akan menghentikan permainan, tetapi seperti yang akan Anda
perhatikan, memasukkan input non-angka lain juga akan menghentikannya.
Ini kurang optimal, paling tidak; kita ingin permainannya juga berhenti
ketika angka yang benar ditebak.

<a id="quitting-after-a-correct-guess"></a>
### Berhenti Setelah Tebakan Benar

Mari kita program permainannya agar berhenti ketika pengguna menang dengan
menambahkan statement `break`:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

Menambahkan baris `break` setelah `You win!` membuat program keluar dari
loop ketika pengguna menebak angka rahasia dengan benar. Keluar dari
loop juga berarti keluar dari program, karena loop adalah
bagian terakhir dari `main`.

### Menangani Input yang Tidak Valid

Untuk lebih menyempurnakan perilaku permainan, alih-alih membuat program
crash ketika pengguna memasukkan non-angka, mari kita buat permainannya
mengabaikan non-angka supaya pengguna dapat terus menebak. Kita dapat
melakukannya dengan mengubah baris tempat `guess` dikonversi dari `String`
menjadi `u32`, seperti yang ditunjukkan pada Listing 2-5.

<Listing number="2-5" file-name="src/main.rs" caption="Mengabaikan tebakan non-angka dan meminta tebakan lain alih-alih membuat program crash">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

Kita beralih dari pemanggilan `expect` ke expression `match` untuk beralih
dari crash karena error menjadi menangani error. Ingat bahwa `parse`
mengembalikan type `Result` dan `Result` adalah *enum* yang memiliki
*variant* `Ok` dan `Err`. Kita memakai expression `match` di sini, seperti
yang kita lakukan dengan hasil `Ordering` dari method `cmp`.

Jika `parse` berhasil mengubah string menjadi angka, ia akan mengembalikan
nilai `Ok` yang memuat angka hasilnya. Nilai `Ok` itu akan cocok dengan
pattern *arm* pertama, dan expression `match` akan langsung mengembalikan nilai
`num` yang dihasilkan `parse` dan dimasukkan ke dalam nilai `Ok`. Angka itu
akan berakhir tepat di tempat yang kita inginkan, yaitu di variable `guess`
baru yang kita buat.

Jika `parse` _tidak_ dapat mengubah string menjadi angka, ia akan
mengembalikan nilai `Err` yang memuat informasi lebih lanjut tentang
errornya. Nilai `Err` tidak cocok dengan pattern `Ok(num)` di *arm* `match`
pertama, tetapi cocok dengan pattern `Err(_)` di *arm* kedua. Garis bawah,
`_`, adalah nilai yang menangkap apa saja; dalam contoh ini, kita
menyatakan bahwa kita ingin mencocokkan semua nilai `Err`, apa pun
informasi yang ada di dalamnya. Jadi, program akan mengeksekusi kode
*arm* kedua, `continue`, yang memberi tahu program untuk lanjut ke iterasi
`loop` berikutnya dan meminta tebakan lain. Jadi, secara efektif, program
mengabaikan semua error yang mungkin ditemui `parse`!

Sekarang semua yang ada di program seharusnya bekerja sesuai harapan.
Mari kita coba:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

Luar biasa! Dengan satu penyesuaian kecil terakhir, kita akan
menyelesaikan permainan tebak angka. Ingat bahwa programnya masih mencetak
angka rahasia. Itu bekerja baik untuk test, tetapi merusak
permainannya. Mari kita hapus `println!` yang mengeluarkan angka rahasia.
Listing 2-6 menunjukkan kode finalnya.

<Listing number="2-6" file-name="src/main.rs" caption="Kode permainan tebak angka yang lengkap">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

Pada titik ini, Anda telah berhasil membangun permainan tebak angka.
Selamat!

## Ringkasan

Proyek ini adalah cara praktik untuk memperkenalkan Anda pada banyak
konsep baru Rust: `let`, `match`, fungsi, penggunaan *crate* eksternal, dan
lainnya. Dalam beberapa bab berikutnya, Anda akan mempelajari
konsep-konsep ini lebih detail. Bab 3 membahas konsep yang dimiliki
sebagian besar bahasa pemrograman, seperti variable, data type, dan
fungsi, serta menunjukkan cara memakainya di Rust. Bab 4 mengeksplorasi
*ownership*, fitur yang membuat Rust berbeda dari bahasa lain. Bab 5
membahas *struct* dan sintaks method, dan Bab 6 menjelaskan cara kerja
*enum*.

[prelude]: ../std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: ../std/string/struct.String.html
[iostdin]: ../std/io/struct.Stdin.html
[read_line]: ../std/io/struct.Stdin.html#method.read_line
[result]: ../std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: ../std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: ../std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types
