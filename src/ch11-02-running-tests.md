<a id="controlling-how-tests-are-run"></a>
## Mengontrol Cara Test Dijalankan

Sama seperti `cargo run` mengompilasi kode Anda lalu menjalankan binary
yang dihasilkan, `cargo test` mengompilasi kode Anda dalam mode test
dan menjalankan binary test yang dihasilkan. Perilaku bawaan binary
yang dihasilkan `cargo test` adalah menjalankan semua test secara
paralel dan menangkap output yang dihasilkan selama test berjalan,
mencegah output itu ditampilkan dan membuatnya lebih mudah untuk membaca
output yang berkaitan dengan hasil test. Namun, Anda bisa
menentukan opsi command line untuk mengubah perilaku bawaan ini.

Sebagian opsi command line diteruskan ke `cargo test`, dan sebagian lagi ke
binary test yang dihasilkan. Untuk memisahkan kedua jenis argumen ini,
Anda mendaftarkan argumen yang diteruskan ke `cargo test`, diikuti pemisah
`--`, lalu argumen-argumen yang diteruskan ke binary test. Menjalankan
`cargo test --help` menampilkan opsi-opsi yang bisa Anda pakai bersama
`cargo test`, dan menjalankan `cargo test -- --help` menampilkan opsi-opsi
yang bisa Anda pakai setelah pemisah. Opsi-opsi ini juga didokumentasikan di
[bagian “Tests” pada _The `rustc` Book_][tests].

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Menjalankan Test secara Paralel atau Berurutan

Ketika Anda menjalankan beberapa test, secara bawaan mereka berjalan
paralel memakai thread, yang berarti mereka lebih cepat selesai berjalan
dan Anda lebih cepat mendapat umpan balik. Karena test-test itu
berjalan pada saat yang sama, Anda harus memastikan test Anda tidak
bergantung satu sama lain atau pada shared state mana pun, termasuk
lingkungan bersama seperti direktori kerja saat ini atau variable
lingkungan.

Sebagai contoh, katakanlah setiap test Anda menjalankan beberapa kode
yang membuat file di disk bernama _test-output.txt_ dan menulis beberapa
data ke file itu. Kemudian, setiap test membaca data di file itu dan
menegaskan bahwa file tersebut berisi nilai tertentu, yang berbeda di
setiap test. Karena test-test itu berjalan pada saat yang
sama, satu test mungkin menimpa file itu di selang waktu antara saat
test lain menulis dan membaca file itu. Test kedua kemudian akan
gagal, bukan karena kodenya salah, melainkan karena test-test itu
saling mengganggu saat berjalan paralel. Salah satu solusinya adalah
memastikan setiap test menulis ke file yang berbeda; solusi lain
adalah menjalankan test satu per satu.

Jika Anda tidak ingin menjalankan test secara paralel atau jika Anda
ingin kontrol yang lebih halus atas jumlah thread yang dipakai, Anda bisa
mengirimkan flag `--test-threads` dan jumlah thread yang ingin Anda pakai
ke binary test. Lihat contoh berikut:

```console
$ cargo test -- --test-threads=1
```

Kita menetapkan jumlah thread test menjadi `1`, memberi tahu program
untuk tidak memakai paralelisme apa pun. Menjalankan test memakai satu
thread akan memakan waktu lebih lama daripada menjalankannya secara
paralel, tetapi test-test itu tidak akan saling mengganggu jika
mereka berbagi state.

### Menampilkan Output Fungsi

Secara bawaan, jika sebuah test lulus, pustaka test Rust
menangkap apa pun yang dicetak ke standard output. Sebagai contoh, jika
kita memanggil `println!` dalam sebuah test dan test itu lulus,
kita tidak akan melihat output `println!` di terminal; kita hanya akan
melihat baris yang menandakan test itu lulus. Jika sebuah test
gagal, kita akan melihat apa pun yang dicetak ke standard output bersama
sisa pesan kegagalannya.

Sebagai contoh, Listing 11-10 memiliki fungsi konyol yang mencetak nilai
parameternya dan mengembalikan 10, beserta test yang lulus dan
test yang gagal.

<Listing number="11-10" file-name="src/lib.rs" caption="Test untuk fungsi yang memanggil `println!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

Ketika kita menjalankan test-test ini dengan `cargo test`, kita
akan melihat output berikut:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

Perhatikan bahwa di output ini tidak ada tempat kita melihat `I got the
value 4`, yang dicetak ketika test yang lulus dijalankan. Output itu
telah ditangkap. Output dari test yang gagal, `I got the value 8`,
muncul di bagian output ringkasan test, yang juga menunjukkan
penyebab kegagalan test.

Jika kita ingin melihat nilai yang dicetak untuk test yang lulus juga,
kita bisa memberi tahu Rust untuk menampilkan juga output test yang
berhasil dengan `--show-output`:

```console
$ cargo test -- --show-output
```

Ketika kita menjalankan lagi test di Listing 11-10 dengan flag
`--show-output`, kita melihat output berikut:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

<a id="running-a-subset-of-tests-by-name"></a>
### Menjalankan Sebagian Test Berdasarkan Nama

Menjalankan test suite penuh kadang bisa memakan waktu lama. Jika Anda
sedang mengerjakan kode di area tertentu, Anda mungkin ingin menjalankan
hanya test yang berkaitan dengan kode itu. Anda bisa memilih test
mana yang dijalankan dengan meneruskan nama test yang ingin Anda
jalankan ke `cargo test` sebagai argumen.

Untuk mendemonstrasikan cara menjalankan sebagian test, pertama kita
akan membuat tiga test untuk fungsi `add_two` kita, seperti yang
ditunjukkan di Listing 11-11, lalu memilih mana yang akan dijalankan.

<Listing number="11-11" file-name="src/lib.rs" caption="Tiga test dengan tiga nama berbeda">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

Jika kita menjalankan test tanpa meneruskan argumen apa pun, seperti
yang kita lihat sebelumnya, semua test akan berjalan paralel:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### Menjalankan Satu Test

Kita bisa meneruskan nama fungsi test mana pun ke `cargo test` untuk
menjalankan test itu saja:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

Hanya test dengan nama `one_hundred` yang berjalan; dua test
lainnya tidak cocok dengan nama itu. Output test memberi tahu kita
bahwa ada test lain yang tidak dijalankan dengan menampilkan `2
filtered out` di bagian akhir.

Kita tidak bisa menentukan nama beberapa test dengan cara ini; hanya
nilai pertama yang diberikan ke `cargo test` yang akan dipakai. Namun, ada
cara untuk menjalankan beberapa test.

#### Menyaring untuk Menjalankan Beberapa Test

Kita bisa menentukan sebagian nama test, dan test mana pun yang
namanya cocok dengan nilai itu akan dijalankan. Sebagai contoh, karena dua
nama test kita mengandung `add`, kita bisa menjalankan keduanya dengan
menjalankan `cargo test add`:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

Perintah ini menjalankan semua test dengan `add` di namanya dan
menyaring keluar test bernama `one_hundred`. Perhatikan juga bahwa
modul tempat sebuah test muncul menjadi bagian dari nama test itu,
jadi kita bisa menjalankan semua test dalam sebuah modul dengan
menyaring berdasarkan nama modulnya.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

<a id="ignoring-tests-unless-specifically-requested"></a>
### Mengabaikan Test Kecuali Diminta Secara Spesifik

Terkadang beberapa test tertentu bisa sangat memakan waktu untuk
dieksekusi, jadi Anda mungkin ingin mengecualikannya pada sebagian besar
penjalanan `cargo test`. Alih-alih mendaftarkan semua test yang ingin
Anda jalankan sebagai argumen, Anda bisa menganotasi test yang memakan
waktu itu memakai atribut `ignore` untuk mengecualikannya, seperti yang
ditunjukkan di sini:

<span class="filename">Nama File: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

Setelah `#[test]`, kita menambahkan baris `#[ignore]` ke test yang
ingin kita kecualikan. Sekarang ketika kita menjalankan test,
`it_works` berjalan, tetapi `expensive_test` tidak:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

Fungsi `expensive_test` didaftarkan sebagai `ignored`. Jika kita ingin
menjalankan hanya test yang diabaikan, kita bisa memakai `cargo test
-- --ignored`:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

Dengan mengontrol test mana yang dijalankan, Anda bisa memastikan
hasil `cargo test` Anda akan kembali dengan cepat. Ketika Anda berada pada
titik ketika masuk akal untuk memeriksa hasil test `ignored` dan Anda
punya waktu untuk menunggu hasilnya, Anda bisa menjalankan `cargo test --
--ignored`. Jika Anda ingin menjalankan semua test, baik yang
diabaikan maupun tidak, Anda bisa menjalankan `cargo test --
--include-ignored`.
