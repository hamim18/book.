## Organisasi Test

Seperti yang disebutkan di awal bab, test adalah disiplin yang
kompleks, dan orang yang berbeda memakai terminologi dan pengorganisasian
yang berbeda. Komunitas Rust memikirkan test dalam dua kategori utama:
unit test dan integration test. _Unit tests_ (unit test) kecil
dan lebih fokus, menguji satu modul secara terisolasi pada satu waktu, dan
bisa menguji antarmuka privat. _Integration tests_ (integration test)
sepenuhnya berada di luar library Anda dan memakai kode Anda dengan cara
yang sama seperti yang dilakukan kode eksternal lain mana pun, hanya
memakai antarmuka publik dan berpotensi melatih beberapa modul per
test.

Menulis kedua jenis test itu penting untuk memastikan bahwa
bagian-bagian library Anda melakukan apa yang Anda harapkan, baik secara
terpisah maupun bersama-sama.

### Test Unit

Tujuan unit test adalah menguji setiap unit kode secara terisolasi
dari kode lainnya untuk dengan cepat menentukan di mana kode berfungsi dan
tidak berfungsi sebagaimana yang diharapkan. Anda akan meletakkan test
unit di direktori _src_ pada setiap file bersama kode yang sedang
diujinya. Konvensinya adalah membuat modul bernama `tests` di setiap file
untuk menampung fungsi-fungsi test dan menganotasi modul itu dengan
`cfg(test)`.

#### Modul `tests` dan `#[cfg(test)]`

Anotasi `#[cfg(test)]` pada modul `tests` memberi tahu Rust untuk
mengompilasi dan menjalankan kode test hanya ketika Anda menjalankan
`cargo test`, bukan ketika Anda menjalankan `cargo build`. Ini menghemat
waktu kompilasi ketika Anda hanya ingin membangun library dan menghemat
ruang pada artefak hasil kompilasi karena testnya tidak disertakan.
Anda akan melihat bahwa karena integration test berada di direktori yang
berbeda, mereka tidak memerlukan anotasi `#[cfg(test)]`. Namun, karena
unit test berada di file yang sama dengan kodenya, Anda akan memakai
`#[cfg(test)]` untuk menentukan bahwa test itu tidak boleh disertakan
dalam hasil kompilasi.

Ingat bahwa ketika kita membuat proyek `adder` baru di bagian pertama bab
ini, Cargo membuatkan kode ini untuk kita:

<span class="filename">Nama File: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

Pada modul `tests` yang dibuat otomatis, atribut `cfg` adalah kependekan
dari *configuration* (konfigurasi) dan memberi tahu Rust bahwa item
berikutnya hanya boleh disertakan jika opsi konfigurasi tertentu terpenuhi.
Dalam kasus ini, opsi konfigurasinya adalah `test`, yang disediakan Rust
untuk mengompilasi dan menjalankan test. Dengan memakai atribut `cfg`,
Cargo mengompilasi kode test kita hanya jika kita secara aktif
menjalankan test dengan `cargo test`. Ini mencakup fungsi pembantu
mana pun yang mungkin berada di dalam modul ini, selain fungsi-fungsi yang
dianotasi dengan `#[test]`.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-private-functions"></a>

#### Test Fungsi Privat

Ada perdebatan di dalam komunitas test tentang apakah fungsi privat
seharusnya diuji secara langsung atau tidak, dan bahasa-bahasa lain
membuatnya sulit atau mustahil untuk menguji fungsi privat. Terlepas dari
ideologi test mana yang Anda anut, aturan privasi Rust memang
mengizinkan Anda menguji fungsi privat. Perhatikan kode di Listing 11-12
dengan fungsi privat `internal_adder`.

<Listing number="11-12" file-name="src/lib.rs" caption="Menguji fungsi privat">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

Perhatikan bahwa fungsi `internal_adder` tidak ditandai sebagai `pub`.
Test hanyalah kode Rust, dan modul `tests` hanyalah modul lain.
Seperti yang kita bahas di [“*Path* untuk Merujuk Item di dalam Pohon
Modul”][paths]<!-- ignore -->, item di modul anak bisa memakai item di
modul leluhurnya. Dalam test ini, kita membawa semua item milik induk
modul `tests` ke dalam *scope* dengan `use super::*`, lalu test bisa
memanggil `internal_adder`. Jika Anda berpendapat fungsi privat tidak
seharusnya diuji, tidak ada apa pun di Rust yang akan memaksa Anda
melakukannya.

### Test Integrasi

Di Rust, integration test sepenuhnya berada di luar library Anda. Mereka
memakai library Anda dengan cara yang sama seperti kode lain mana pun, yang
berarti mereka hanya bisa memanggil fungsi yang merupakan bagian dari API
publik library Anda. Tujuannya adalah menguji apakah banyak bagian library
Anda bekerja bersama dengan benar. Unit-unit kode yang bekerja dengan benar
sendiri-sendiri bisa bermasalah ketika diintegrasikan, jadi coverage
atas kode yang terintegrasi juga penting. Untuk membuat test
integrasi, pertama Anda perlu direktori _tests_.

#### Direktori _tests_

Kita membuat direktori _tests_ di tingkat teratas direktori proyek kita,
bersebelahan dengan _src_. Cargo tahu untuk mencari file test
integrasi di direktori ini. Kita kemudian bisa membuat file test
sebanyak yang kita mau, dan Cargo akan mengompilasi setiap file sebagai
*crate* tersendiri.

Mari kita buat integration test. Dengan kode Listing 11-12 yang masih
berada di file _src/lib.rs_, buat direktori _tests_, dan buat file baru
bernama _tests/integration_test.rs_. Struktur direktori Anda seharusnya
terlihat seperti ini:

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

Masukkan kode di Listing 11-13 ke file _tests/integration_test.rs_.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="Test integrasi untuk fungsi di *crate* `adder`">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

Setiap file di direktori _tests_ adalah *crate* yang terpisah, jadi kita
perlu membawa library kita ke dalam *scope* setiap *crate* test. Karena
alasan itu, kita menambahkan `use adder::add_two;` di bagian atas kode,
yang tidak kita perlukan di unit test.

Kita tidak perlu menganotasi kode mana pun di
_tests/integration_test.rs_ dengan `#[cfg(test)]`. Cargo memperlakukan
direktori _tests_ secara khusus dan mengompilasi file di direktori ini
hanya ketika kita menjalankan `cargo test`. Jalankan `cargo test` sekarang:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

Ketiga bagian output itu mencakup unit test, integration test,
dan doc test. Perhatikan bahwa jika ada test dalam satu bagian yang
gagal, bagian-bagian berikutnya tidak akan dijalankan. Sebagai contoh, jika
sebuah unit test gagal, tidak akan ada output untuk test
integrasi dan doc test, karena test-test itu hanya akan
dijalankan jika semua unit test lulus.

Bagian pertama untuk unit test sama seperti yang selama ini kita
lihat: satu baris untuk setiap unit test (satu bernama `internal` yang
kita tambahkan di Listing 11-12), lalu baris ringkasan untuk test
unit.

Bagian integration test dimulai dengan baris `Running
tests/integration_test.rs`. Berikutnya, ada satu baris untuk setiap fungsi
test dalam integration test itu dan baris ringkasan untuk hasil
integration test tepat sebelum bagian `Doc-tests adder` dimulai.

Setiap file integration test memiliki bagiannya sendiri, jadi jika kita
menambahkan lebih banyak file di direktori _tests_, akan ada lebih banyak
bagian integration test.

Kita tetap bisa menjalankan fungsi integration test tertentu dengan
menentukan nama fungsi test itu sebagai argumen ke `cargo test`.
Untuk menjalankan semua test dalam file integration test tertentu,
pakai argumen `--test` dari `cargo test` diikuti nama filenya:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

Perintah ini hanya menjalankan test di file
_tests/integration_test.rs_.

#### Submodul dalam Test Integrasi

Ketika Anda menambahkan lebih banyak integration test, Anda mungkin
ingin membuat lebih banyak file di direktori _tests_ untuk membantu
mengorganisasikannya; misalnya, Anda bisa mengelompokkan fungsi test
berdasarkan fungsionalitas yang sedang diuji. Seperti yang disebutkan
sebelumnya, setiap file di direktori _tests_ dikompilasi sebagai crate
terpisahnya sendiri, yang berguna untuk membuat scope terpisah supaya lebih
meniru cara end user akan memakai crate Anda. Namun, ini berarti file
di direktori _tests_ tidak berbagi perilaku yang sama seperti file di
_src_, seperti yang Anda pelajari di Bab 7 mengenai cara memisahkan kode
menjadi modul dan file.

Perilaku file direktori _tests_ yang berbeda ini paling terlihat ketika
Anda memiliki sekumpulan fungsi pembantu untuk dipakai di beberapa file
integration test, dan Anda mencoba mengikuti langkah-langkah di bagian
[“Memisahkan Module ke dalam File yang Berbeda”][separating-modules-into-files]<!-- ignore --> pada Bab 7 untuk mengekstraknya menjadi modul bersama.
Sebagai contoh, jika kita membuat _tests/common.rs_ dan menempatkan fungsi
bernama `setup` di dalamnya, kita bisa menambahkan beberapa kode ke `setup`
yang ingin kita panggil dari beberapa fungsi test di beberapa file
test:

<span class="filename">Nama File: tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

Ketika kita menjalankan test lagi, kita akan melihat bagian baru di
output test untuk file _common.rs_, meskipun file ini tidak berisi
fungsi test apa pun dan kita juga tidak memanggil fungsi `setup` dari
mana pun:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

Melihat `common` muncul di hasil test dengan `running 0 tests`
ditampilkan untuknya bukanlah yang kita inginkan. Kita hanya ingin berbagi
beberapa kode dengan file integration test lainnya. Untuk menghindari
`common` muncul di output test, alih-alih membuat _tests/common.rs_,
kita akan membuat _tests/common/mod.rs_. Direktori proyeknya sekarang
terlihat seperti ini:

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

Ini adalah konvensi penamaan lama yang juga dipahami Rust yang kita
sebutkan di [“Path File Alternatif”][alt-paths]<!-- ignore --> pada Bab 7.
Menamai file dengan cara ini memberi tahu Rust untuk tidak memperlakukan
modul `common` sebagai file integration test. Ketika kita memindahkan
kode fungsi `setup` ke _tests/common/mod.rs_ dan menghapus file
_tests/common.rs_, bagian di output test itu tidak akan muncul lagi.
File di subdirektori direktori _tests_ tidak dikompilasi sebagai *crate*
terpisah dan tidak memiliki bagian di output test.

Setelah kita membuat _tests/common/mod.rs_, kita bisa memakainya dari file
integration test mana pun sebagai modul. Berikut contoh pemanggilan
fungsi `setup` dari test `it_adds_two` di _tests/integration_test.rs_:

<span class="filename">Nama File: tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

Perhatikan bahwa deklarasi `mod common;` sama dengan deklarasi modul yang
kita peragakan di Listing 7-21. Kemudian, di fungsi test, kita bisa
memanggil fungsi `common::setup()`.

#### Test Integrasi untuk Crate Binary

Jika proyek kita adalah *crate* binary yang hanya berisi file _src/main.rs_
dan tidak memiliki file _src/lib.rs_, kita tidak bisa membuat test
integrasi di direktori _tests_ dan membawa fungsi yang didefinisikan di
file _src/main.rs_ ke dalam *scope* dengan statement `use`. Hanya *crate*
library yang mengekspos fungsi yang bisa dipakai *crate* lain; *crate* binary
dimaksudkan untuk dijalankan sendiri.

Ini adalah salah satu alasan proyek Rust yang menyediakan binary memiliki
file _src/main.rs_ yang sederhana yang memanggil logika yang berada di file
_src/lib.rs_. Dengan memakai struktur itu, integration test _bisa_
menguji *crate* library dengan `use` untuk membuat fungsionalitas pentingnya
tersedia. Jika fungsionalitas pentingnya berfungsi, sedikit kode di file
_src/main.rs_ juga akan berfungsi, dan sedikit kode itu tidak perlu diuji.

## Ringkasan

Fitur test Rust menyediakan cara untuk menentukan bagaimana kode
seharusnya berfungsi guna memastikan bahwa ia terus bekerja seperti yang
Anda harapkan, bahkan ketika Anda membuat perubahan. Test unit melatih
bagian-bagian library yang berbeda secara terpisah dan bisa menguji detail
implementasi privat. Test integrasi memeriksa bahwa banyak bagian
library bekerja bersama dengan benar, dan mereka memakai API publik library
untuk menguji kode dengan cara yang sama seperti yang akan dilakukan kode
eksternal. Meskipun type system dan aturan *ownership* Rust membantu mencegah
beberapa jenis bug, test tetap penting untuk mengurangi bug logika
yang berkaitan dengan bagaimana kode Anda diharapkan berperilaku.

Mari kita gabungkan pengetahuan yang Anda pelajari di bab ini dan di
bab-bab sebelumnya untuk mengerjakan sebuah proyek!

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths
