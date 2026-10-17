## Membawa Path ke dalam Scope dengan Kata Kunci `use`

Harus menuliskan *path* untuk memanggil fungsi bisa terasa tidak praktis dan
berulang-ulang. Di Listing 7-7, entah kita memilih *path* absolut maupun
relatif menuju fungsi `add_to_waitlist`, setiap kali ingin memanggil
`add_to_waitlist` kita harus menyebutkan `front_of_house` dan `hosting` juga.
Untungnya, ada cara untuk menyederhanakan proses ini: kita dapat membuat
pintasan menuju sebuah *path* dengan kata kunci `use` satu kali, lalu memakai
nama yang lebih pendek di tempat lain mana pun di dalam *scope*.

Di Listing 7-11, kita membawa *module* `crate::front_of_house::hosting` ke
dalam *scope* fungsi `eat_at_restaurant` supaya kita hanya perlu menyebutkan
`hosting::add_to_waitlist` untuk memanggil fungsi `add_to_waitlist` di
`eat_at_restaurant`.

<Listing number="7-11" file-name="src/lib.rs" caption="Membawa sebuah module ke dalam scope dengan `use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

Menambahkan `use` dan sebuah *path* di dalam sebuah *scope* mirip dengan membuat
tautan simbolik di sistem file. Dengan menambahkan `use
crate::front_of_house::hosting` di crate root, `hosting` kini menjadi nama
yang valid di *scope* tersebut, seolah-olah *module* `hosting` telah
didefinisikan di *crate root*. *Path* yang dibawa ke dalam *scope* dengan `use`
juga diperiksa privasinya, seperti *path*-path lainnya.

Perhatikan bahwa `use` hanya membuat pintasan untuk *scope* tertentu tempat
`use` itu berada. Listing 7-12 memindahkan fungsi `eat_at_restaurant` ke
dalam *module* anak baru bernama `customer`, yang kemudian menjadi *scope* yang
berbeda dari pernyataan `use`, sehingga badan fungsi itu tidak akan
terkompilasi.

<Listing number="7-12" file-name="src/lib.rs" caption="Sebuah pernyataan `use` hanya berlaku di scope tempatnya berada.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

Galat *compiler* menunjukkan bahwa pintasan itu tidak lagi berlaku di dalam
*module* `customer`:

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Perhatikan bahwa ada juga peringatan bahwa `use` tidak lagi dipakai di dalam
*scope*-nya! Untuk memperbaiki masalah ini, pindahkan `use` ke dalam *module*
`customer` juga, atau rujuk pintasan di *module* induk dengan `super::hosting`
di dalam *module* anak `customer`.

<a id="creating-idiomatic-use-paths"></a>
### Membuat Path `use` yang Idiomatis

Di Listing 7-11, Anda mungkin bertanya-tanya mengapa kita menuliskan `use
crate::front_of_house::hosting` lalu memanggil `hosting::add_to_waitlist` di
`eat_at_restaurant`, alih-alih menuliskan *path* `use` langsung sampai ke
fungsi `add_to_waitlist` untuk mencapai hasil yang sama, seperti di Listing
7-13.

<Listing number="7-13" file-name="src/lib.rs" caption="Membawa fungsi `add_to_waitlist` ke dalam scope dengan `use`, yang tidak idiomatis">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Meskipun Listing 7-11 dan Listing 7-13 sama-sama menyelesaikan tugas yang
sama, Listing 7-11 adalah cara yang idiomatis untuk membawa sebuah fungsi ke
dalam *scope* dengan `use`. Membawa *module* induk fungsi ke dalam *scope* dengan
`use` berarti kita harus menyebutkan *module* induknya ketika memanggil fungsi
tersebut. Menyebutkan *module* induk ketika memanggil fungsi memperjelas bahwa
fungsi itu tidak didefinisikan secara lokal, sambil tetap meminimalkan
pengulangan *path* lengkap. Kode di Listing 7-13 tidak jelas mengenai di mana
`add_to_waitlist` didefinisikan.

Di sisi lain, ketika membawa *struct*, *enum*, dan item lain dengan `use`, adalah
idiomatis untuk menuliskan *path* lengkapnya. Listing 7-14 menunjukkan cara
yang idiomatis untuk membawa *struct* `HashMap` dari pustaka standar ke dalam
*scope* sebuah *crate* binary.

<Listing number="7-14" file-name="src/main.rs" caption="Membawa `HashMap` ke dalam scope dengan cara yang idiomatis">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Tidak ada alasan yang kuat di balik idiom ini: ini sekadar konvensi yang
telah muncul, dan orang-orang telah terbiasa membaca dan menulis kode Rust
dengan cara ini.

Pengecualian untuk idiom ini adalah jika kita membawa dua item dengan nama
yang sama ke dalam *scope* dengan pernyataan `use`, karena Rust tidak
mengizinkannya. Listing 7-15 menunjukkan cara membawa dua tipe `Result` ke
dalam *scope* yang memiliki nama yang sama tetapi *module* induk yang berbeda,
dan cara merujuk keduanya.

<Listing number="7-15" file-name="src/lib.rs" caption="Membawa dua tipe dengan nama yang sama ke dalam scope yang sama mengharuskan pemakaian module induk keduanya.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Seperti yang Anda lihat, memakai *module* induk membedakan kedua tipe
`Result`. Jika alih-alih kita menuliskan `use std::fmt::Result` dan `use
std::io::Result`, kita akan memiliki dua tipe `Result` di *scope* yang sama,
dan Rust tidak akan tahu yang mana yang kita maksud ketika kita memakai
`Result`.

### Memberi Nama Baru dengan Kata Kunci `as`

Ada solusi lain untuk masalah membawa dua tipe dengan nama yang sama ke dalam
*scope* yang sama dengan `use`: setelah *path*, kita dapat menuliskan `as` dan
sebuah nama lokal baru, atau *alias*, untuk tipe tersebut. Listing 7-16
menunjukkan cara lain untuk menulis kode di Listing 7-15 dengan mengganti
nama salah satu dari dua tipe `Result` memakai `as`.

<Listing number="7-16" file-name="src/lib.rs" caption="Mengganti nama sebuah tipe saat tipe itu dibawa ke dalam scope dengan kata kunci `as`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

Pada pernyataan `use` kedua, kita memilih nama baru `IoResult` untuk tipe
`std::io::Result`, yang tidak akan bentrok dengan `Result` dari `std::fmt`
yang juga kita bawa ke dalam *scope*. Listing 7-15 dan Listing 7-16 sama-sama
dianggap idiomatis, jadi pilihannya ada di tangan Anda!

### Mengekspor Ulang Nama dengan `pub use`

Ketika kita membawa sebuah nama ke dalam *scope* dengan kata kunci `use`, nama
tersebut bersifat privat terhadap *scope* tempat kita mengimpornya. Untuk
memungkinkan kode di luar *scope* itu merujuk nama tersebut seolah-olah nama
itu telah didefinisikan di *scope* itu, kita dapat menggabungkan `pub` dan
`use`. Teknik ini disebut *re-exporting* (mengekspor ulang) karena kita
membawa sebuah item ke dalam *scope*, tetapi juga menjadikan item itu tersedia
untuk dibawa orang lain ke *scope* mereka.

Listing 7-17 menunjukkan kode di Listing 7-11 dengan `use` di *module* akar
diubah menjadi `pub use`.

<Listing number="7-17" file-name="src/lib.rs" caption="Menjadikan sebuah nama tersedia untuk dipakai kode mana pun dari scope baru dengan `pub use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

Sebelum perubahan ini, kode eksternal harus memanggil fungsi
`add_to_waitlist` dengan memakai *path*
`restaurant::front_of_house::hosting::add_to_waitlist()`, yang juga
mengharuskan *module* `front_of_house` ditandai sebagai `pub`. Kini, setelah
`pub use` ini mengekspor ulang *module* `hosting` dari *module* akar, kode
eksternal dapat memakai *path* `restaurant::hosting::add_to_waitlist()`
sebagai gantinya.

Re-exporting berguna ketika struktur internal kode Anda berbeda dari cara
pemrogram yang memanggil kode Anda memikirkan domainnya. Misalnya, dalam
metafora restoran ini, orang-orang yang menjalankan restoran memikirkan
“front of house” dan “back of house.” Tetapi pelanggan yang mengunjungi
sebuah restoran mungkin tidak akan memikirkan bagian-bagian restoran dalam
istilah-istilah tersebut. Dengan `pub use`, kita dapat menulis kode kita
dengan satu struktur tetapi mengekspos struktur yang berbeda. Melakukannya
membuat library kita tertata dengan baik bagi pemrogram yang mengerjakan
library dan pemrogram yang memanggil library. Kita akan melihat contoh lain
dari `pub use` dan bagaimana pengaruhnya terhadap dokumentasi *crate* Anda di
[“Mengekspor API Publik yang Mudah Dipakai”][ch14-pub-use]<!-- ignore -->
di Bab 14.

### Memakai Package Eksternal

Di Bab 2, kita memprogram proyek permainan tebak angka yang memakai *package*
eksternal bernama `rand` untuk mendapatkan angka acak. Untuk memakai `rand`
di proyek kita, kita menambahkan baris ini ke _Cargo.toml_:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

Menambahkan `rand` sebagai dependensi di _Cargo.toml_ memberi tahu Cargo
untuk mengunduh *package* `rand` dan dependensi apa pun dari
[crates.io](https://crates.io/) dan menjadikan `rand` tersedia untuk proyek
kita.

Lalu, untuk membawa definisi-definisi `rand` ke dalam *scope* *package* kita,
kita menambahkan baris `use` yang dimulai dengan nama *crate*, `rand`, dan
mendaftar item-item yang ingin kita bawa ke dalam *scope*. Ingat bahwa di
[“Menghasilkan Angka Acak”][rand]<!-- ignore --> di Bab 2, kita membawa
item-item di *module* `rand::prelude` ke dalam *scope* dan memanggil fungsi
`rand::rng`:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

Anggota komunitas Rust telah menyediakan banyak *package* di
[crates.io](https://crates.io/), dan menarik salah satunya ke dalam *package*
Anda melibatkan langkah-langkah yang sama: mendaftarkannya di file
_Cargo.toml_ *package* Anda dan memakai `use` untuk membawa item-item dari
*crate* mereka ke dalam *scope*.

Perhatikan bahwa pustaka standar `std` juga adalah sebuah *crate* yang
eksternal bagi *package* kita. Karena pustaka standar dikirim bersama bahasa
Rust, kita tidak perlu mengubah _Cargo.toml_ untuk menyertakan `std`. Tetapi
kita memang perlu merujuknya dengan `use` untuk membawa item-item dari sana
ke dalam *scope* *package* kita. Misalnya, dengan `HashMap` kita akan memakai
baris ini:

```rust
use std::collections::HashMap;
```

Ini adalah *path* absolut yang dimulai dengan `std`, nama *crate* pustaka
standar.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-nested-paths-to-clean-up-large-use-lists"></a>

### Memakai Nested Path untuk Merapikan Daftar `use`

Jika kita memakai beberapa item yang didefinisikan di *crate* atau *module* yang
sama, mendaftar setiap item di barisnya sendiri dapat memakan banyak ruang
vertikal di file kita. Misalnya, dua pernyataan `use` yang kita miliki di
permainan tebak angka di Listing 2-4 ini membawa item-item dari `std` ke
dalam *scope*:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Sebagai gantinya, kita dapat memakai *nested path* (*path* bersarang) untuk
membawa item-item yang sama ke dalam *scope* dalam satu baris. Kita
melakukannya dengan menuliskan bagian *path* yang sama, diikuti dua titik dua,
lalu kurung kurawal di sekeliling daftar bagian-bagian *path* yang berbeda,
seperti yang ditunjukkan di Listing 7-18.

<Listing number="7-18" file-name="src/main.rs" caption="Menuliskan nested path untuk membawa beberapa item dengan awalan yang sama ke dalam scope">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

Di program yang lebih besar, membawa banyak item ke dalam *scope* dari *crate*
atau *module* yang sama memakai *nested path* dapat mengurangi jumlah pernyataan
`use` terpisah yang dibutuhkan secara signifikan!

Kita dapat memakai *nested path* di tingkat mana pun dalam sebuah *path*, yang
berguna ketika menggabungkan dua pernyataan `use` yang berbagi sebuah
subpath. Misalnya, Listing 7-19 menunjukkan dua pernyataan `use`: satu yang
membawa `std::io` ke dalam *scope* dan satu yang membawa `std::io::Write` ke
dalam *scope*.

<Listing number="7-19" file-name="src/lib.rs" caption="Dua pernyataan `use` ketika salah satunya adalah subpath dari yang lain">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

Bagian yang sama dari kedua *path* ini adalah `std::io`, dan itu adalah *path*
pertama secara lengkap. Untuk menggabungkan kedua *path* ini menjadi satu
pernyataan `use`, kita dapat memakai `self` di dalam *nested path*, seperti
yang ditunjukkan di Listing 7-20.

<Listing number="7-20" file-name="src/lib.rs" caption="Menggabungkan path-path di Listing 7-19 menjadi satu pernyataan `use`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Baris ini membawa `std::io` dan `std::io::Write` ke dalam *scope*.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-glob-operator"></a>

### Mengimpor Item dengan Glob Operator

Jika kita ingin membawa _semua_ item publik yang didefinisikan di sebuah
*path* ke dalam *scope*, kita dapat menuliskan *path* tersebut diikuti operator
*glob* `*`:

```rust
use std::collections::*;
```

Pernyataan `use` ini membawa semua item publik yang didefinisikan di
`std::collections` ke dalam *scope* saat ini. Berhati-hatilah saat memakai
operator glob! Glob dapat mempersulit mengetahui nama apa saja yang berada di
dalam *scope* dan di mana sebuah nama yang dipakai di program Anda
didefinisikan. Selain itu, jika dependensi mengubah definisinya, apa yang
Anda impor ikut berubah, yang dapat menyebabkan galat *compiler* ketika Anda
memperbarui dependensi jika dependensi itu menambahkan definisi dengan nama
yang sama dengan definisi milik Anda di *scope* yang sama, misalnya.

Operator glob sering dipakai saat menguji untuk membawa semua yang sedang
diuji ke dalam *module* `tests`; kita akan membahasnya di [“Cara Menulis
Pengujian”][writing-tests]<!-- ignore --> di Bab 11. Operator glob juga
kadang dipakai sebagai bagian dari pola prelude: lihat [dokumentasi pustaka
standar](../std/prelude/index.html#other-preludes)<!-- ignore --> untuk
informasi lebih lanjut tentang pola itu.

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests
