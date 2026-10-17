## Workspace Cargo

Di Bab 12, kita membangun sebuah *package* yang memuat *crate* binary dan *crate*
library. Seiring berkembangnya proyek Anda, Anda mungkin mendapati *crate*
library itu terus membesar dan Anda ingin memecah *package* Anda lebih jauh
menjadi beberapa *crate* library. Cargo menawarkan fitur yang disebut
_workspaces_ yang dapat membantu mengelola beberapa *package* terkait yang
dikembangkan secara bersamaan.

### Membuat Workspace

Sebuah _workspace_ adalah sekumpulan *package* yang berbagi _Cargo.lock_ dan
direktori keluaran yang sama. Mari kita buat proyek yang memakai workspace—kita
akan memakai kode sederhana supaya bisa berkonsentrasi pada struktur
workspace. Ada beberapa cara menyusun workspace, jadi kita hanya akan
menunjukkan satu cara yang umum. Kita akan memiliki workspace yang memuat satu
binary dan dua library. Binary, yang akan menyediakan fungsionalitas utama,
akan bergantung pada kedua library itu. Satu library akan menyediakan fungsi
`add_one` dan library lainnya fungsi `add_two`. Ketiga *crate* ini akan menjadi
bagian dari workspace yang sama. Kita mulai dengan membuat direktori baru
untuk workspace:

```console
$ mkdir add
$ cd add
```

Selanjutnya, di direktori _add_, kita membuat file _Cargo.toml_ yang akan
mengonfigurasi seluruh workspace. File ini tidak akan memiliki seksi
`[package]`. Sebagai gantinya, file itu akan diawali seksi `[workspace]` yang
memungkinkan kita menambahkan anggota ke workspace. Kita juga memastikan untuk
memakai versi terbaru dan terbaik dari algoritme resolver Cargo di workspace
kita dengan menetapkan nilai `resolver` menjadi `"3"`:

<span class="filename">Nama File: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

Selanjutnya, kita akan membuat *crate* binary `adder` dengan menjalankan
`cargo new` di dalam direktori _add_:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

Menjalankan `cargo new` di dalam sebuah workspace juga secara otomatis
menambahkan *package* yang baru dibuat ke kunci `members` dalam definisi
`[workspace]` di _Cargo.toml_ workspace itu, seperti ini:

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

Pada titik ini, kita dapat membangun workspace dengan menjalankan
`cargo build`. File-file di direktori _add_ Anda seharusnya tampak seperti ini:

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Workspace ini memiliki satu direktori _target_ di tingkat teratas tempat
artefak hasil kompilasi akan diletakkan; *package* `adder` tidak memiliki
direktori _target_ sendiri. Bahkan jika kita menjalankan `cargo build` dari
dalam direktori _adder_, artefak hasil kompilasi tetap akan berakhir di
_add/target_ alih-alih _add/adder/target_. Cargo menyusun direktori _target_
dalam sebuah workspace seperti ini karena *crate*-crate dalam workspace memang
dimaksudkan untuk saling bergantung. Jika setiap *crate* memiliki direktori
_target_ sendiri, setiap *crate* harus mengompilasi ulang setiap *crate* lain di
workspace untuk meletakkan artefaknya di direktori _target_-nya sendiri.
Dengan berbagi satu direktori _target_, *crate*-crate itu dapat menghindari
build ulang yang tidak perlu.

### Membuat Package Kedua di Workspace

Selanjutnya, mari kita buat *package* anggota lain di workspace dan menyebutnya
`add_one`. Buat *crate* library baru bernama `add_one`:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

_Cargo.toml_ tingkat teratas sekarang akan memuat *path* _add_one_ di daftar
`members`:

<span class="filename">Nama File: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

Direktori _add_ Anda sekarang seharusnya memiliki direktori dan file berikut:

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Di file _add_one/src/lib.rs_, mari kita tambahkan fungsi `add_one`:

<span class="filename">Nama File: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
```

Sekarang kita dapat membuat *package* `adder` dengan binary kita bergantung pada
*package* `add_one` yang memuat library kita. Pertama, kita perlu menambahkan
dependensi *path* pada `add_one` ke _adder/Cargo.toml_.

<span class="filename">Nama File: adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

Cargo tidak berasumsi bahwa *crate*-crate di sebuah workspace akan saling
bergantung, jadi kita perlu menegaskan hubungan dependensinya secara eksplisit.

Selanjutnya, mari kita pakai fungsi `add_one` (dari *crate* `add_one`) di *crate*
`adder`. Buka file _adder/src/main.rs_ dan ubah fungsi `main` untuk memanggil
fungsi `add_one`, seperti pada Listing 14-7.

<Listing number="14-7" file-name="adder/src/main.rs" caption="Memakai crate library `add_one` dari crate `adder`">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

Mari kita bangun workspace itu dengan menjalankan `cargo build` di direktori
tingkat teratas _add_!

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

Untuk menjalankan *crate* binary dari direktori _add_, kita dapat menyebutkan
*package* mana di workspace yang ingin kita jalankan dengan memakai argumen `-p`
beserta nama *package* pada `cargo run`:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

Ini menjalankan kode di _adder/src/main.rs_, yang bergantung pada *crate*
`add_one`.

<!-- Old headings. Do not remove or links may break. -->

<a id="depending-on-an-external-package-in-a-workspace"></a>

### Bergantung pada Package Eksternal

Perhatikan bahwa workspace ini hanya memiliki satu file _Cargo.lock_ di
tingkat teratas, alih-alih memiliki _Cargo.lock_ di direktori setiap *crate*.
Ini memastikan semua *crate* memakai versi yang sama dari semua dependensi. Jika
kita menambahkan *package* `rand` ke file _adder/Cargo.toml_ dan
_add_one/Cargo.toml_, Cargo akan menyelesaikan keduanya menjadi satu versi
`rand` dan mencatatnya di _Cargo.lock_ yang satu itu. Membuat semua crate di
workspace memakai dependensi yang sama berarti crate-crate itu akan selalu
kompatibel satu sama lain. Mari kita tambahkan crate `rand` ke seksi
`[dependencies]` di file _add_one/Cargo.toml_ supaya kita dapat memakai *crate*
`rand` di *crate* `add_one`:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">Nama File: add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

Sekarang kita dapat menambahkan `use rand;` ke file _add_one/src/lib.rs_, dan
membangun seluruh workspace dengan menjalankan `cargo build` di direktori
_add_ akan menarik dan mengompilasi *crate* `rand`. Kita akan mendapat satu
peringatan karena kita tidak merujuk `rand` yang kita bawa ke *scope*:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.10.1
   --snip--
   Compiling rand v0.10.1
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

_Cargo.lock_ tingkat teratas sekarang memuat informasi tentang dependensi
`add_one` pada `rand`. Namun, meskipun `rand` dipakai di suatu tempat di
workspace, kita tidak dapat memakainya di *crate* lain di workspace kecuali kita
menambahkan `rand` ke file _Cargo.toml_ mereka juga. Sebagai contoh, jika kita
menambahkan `use rand;` ke file _adder/src/main.rs_ untuk *package* `adder`,
kita akan mendapat galat:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

Untuk memperbaikinya, sunting file _Cargo.toml_ untuk *package* `adder` dan
nyatakan bahwa `rand` juga merupakan dependensi baginya. Membangun *package*
`adder` akan menambahkan `rand` ke daftar dependensi untuk `adder` di
_Cargo.lock_, tetapi tidak ada salinan tambahan `rand` yang akan diunduh.
Cargo akan memastikan bahwa setiap *crate* di setiap *package* dalam workspace
yang memakai *package* `rand` akan memakai versi yang sama selama mereka
menyebutkan versi `rand` yang kompatibel, menghemat ruang kita dan memastikan
*crate*-crate di workspace akan kompatibel satu sama lain.

Jika *crate*-crate di workspace menyebutkan versi yang tidak kompatibel dari
dependensi yang sama, Cargo akan menyelesaikan masing-masing versi itu, tetapi
tetap berusaha menyelesaikan sesedikit mungkin versi.

### Menambahkan Pengujian ke Workspace

Untuk peningkatan lain, mari kita tambahkan *test* (pengujian) untuk fungsi
`add_one::add_one` di dalam *crate* `add_one`:

<span class="filename">Nama File: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

Sekarang jalankan `cargo test` di direktori tingkat teratas _add_. Menjalankan
`cargo test` di workspace yang tersusun seperti ini akan menjalankan test
untuk semua *crate* di workspace:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Seksi pertama dari keluaran itu menunjukkan bahwa test `it_works` di *crate*
`add_one` lulus. Seksi berikutnya menunjukkan bahwa nol test ditemukan di
*crate* `adder`, lalu seksi terakhir menunjukkan bahwa nol *documentation test*
ditemukan di *crate* `add_one`.

Kita juga dapat menjalankan test untuk satu *crate* tertentu di sebuah workspace
dari direktori tingkat teratas dengan memakai flag `-p` dan menyebutkan nama
*crate* yang ingin kita uji:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Keluaran ini menunjukkan `cargo test` hanya menjalankan test untuk *crate*
`add_one` dan tidak menjalankan test *crate* `adder`.

Jika Anda menerbitkan *crate*-crate di workspace itu ke
[crates.io](https://crates.io/)<!-- ignore -->, setiap *crate* di workspace perlu
diterbitkan secara terpisah. Seperti `cargo test`, kita dapat menerbitkan
*crate* tertentu di workspace kita dengan memakai flag `-p` dan menyebutkan nama
*crate* yang ingin kita terbitkan.

Untuk latihan tambahan, tambahkan *crate* `add_two` ke workspace ini dengan cara
yang serupa seperti *crate* `add_one`!

Seiring pertumbuhan proyek Anda, pertimbangkan untuk memakai workspace:
Workspace memungkinkan Anda bekerja dengan komponen yang lebih kecil dan lebih
mudah dipahami daripada satu gumpalan kode besar. Lebih jauh lagi, menjaga
*crate*-crate tetap dalam satu workspace dapat mempermudah koordinasi antar-crate
jika *crate*-crate itu sering diubah pada saat yang sama.
