<a id="controlling-how-tests-are-run"></a>
## Mengontrol Cara Pengujian Dijalankan

Sama seperti `cargo run` mengompilasi kode Anda lalu menjalankan binary
yang dihasilkan, `cargo test` mengompilasi kode Anda dalam mode pengujian
dan menjalankan binary pengujian yang dihasilkan. Perilaku bawaan binary
yang dihasilkan `cargo test` adalah menjalankan semua pengujian secara
paralel dan menangkap keluaran yang dihasilkan selama pengujian berjalan,
mencegah keluaran itu ditampilkan dan membuatnya lebih mudah untuk membaca
keluaran yang berkaitan dengan hasil pengujian. Namun, Anda bisa
menentukan opsi baris perintah untuk mengubah perilaku bawaan ini.

Sebagian opsi baris perintah diteruskan ke `cargo test`, dan sebagian lagi ke
binary pengujian yang dihasilkan. Untuk memisahkan kedua jenis argumen ini,
Anda mendaftarkan argumen yang diteruskan ke `cargo test`, diikuti pemisah
`--`, lalu argumen-argumen yang diteruskan ke binary pengujian. Menjalankan
`cargo test --help` menampilkan opsi-opsi yang bisa Anda pakai bersama
`cargo test`, dan menjalankan `cargo test -- --help` menampilkan opsi-opsi
yang bisa Anda pakai setelah pemisah. Opsi-opsi ini juga didokumentasikan di
[bagian “Tests” pada _The `rustc` Book_][tests].

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Menjalankan Pengujian secara Paralel atau Berurutan

Ketika Anda menjalankan beberapa pengujian, secara bawaan mereka berjalan
paralel memakai thread, yang berarti mereka lebih cepat selesai berjalan
dan Anda lebih cepat mendapat umpan balik. Karena pengujian-pengujian itu
berjalan pada saat yang sama, Anda harus memastikan pengujian Anda tidak
bergantung satu sama lain atau pada state bersama mana pun, termasuk
lingkungan bersama seperti direktori kerja saat ini atau variabel
lingkungan.

Sebagai contoh, katakanlah setiap pengujian Anda menjalankan beberapa kode
yang membuat file di disk bernama _test-output.txt_ dan menulis beberapa
data ke file itu. Kemudian, setiap pengujian membaca data di file itu dan
menegaskan bahwa file tersebut berisi nilai tertentu, yang berbeda di
setiap pengujian. Karena pengujian-pengujian itu berjalan pada saat yang
sama, satu pengujian mungkin menimpa file itu di selang waktu antara saat
pengujian lain menulis dan membaca file itu. Pengujian kedua kemudian akan
gagal, bukan karena kodenya salah, melainkan karena pengujian-pengujian itu
saling mengganggu saat berjalan paralel. Salah satu solusinya adalah
memastikan setiap pengujian menulis ke file yang berbeda; solusi lain
adalah menjalankan pengujian satu per satu.

Jika Anda tidak ingin menjalankan pengujian secara paralel atau jika Anda
ingin kontrol yang lebih halus atas jumlah thread yang dipakai, Anda bisa
mengirimkan flag `--test-threads` dan jumlah thread yang ingin Anda pakai
ke binary pengujian. Lihat contoh berikut:

```console
$ cargo test -- --test-threads=1
```

Kita menetapkan jumlah thread pengujian menjadi `1`, memberi tahu program
untuk tidak memakai paralelisme apa pun. Menjalankan pengujian memakai satu
thread akan memakan waktu lebih lama daripada menjalankannya secara
paralel, tetapi pengujian-pengujian itu tidak akan saling mengganggu jika
mereka berbagi state.

### Menampilkan Keluaran Fungsi

Secara bawaan, jika sebuah pengujian lulus, pustaka pengujian Rust
menangkap apa pun yang dicetak ke standard output. Sebagai contoh, jika
kita memanggil `println!` dalam sebuah pengujian dan pengujian itu lulus,
kita tidak akan melihat keluaran `println!` di terminal; kita hanya akan
melihat baris yang menandakan pengujian itu lulus. Jika sebuah pengujian
gagal, kita akan melihat apa pun yang dicetak ke standard output bersama
sisa pesan kegagalannya.

Sebagai contoh, Listing 11-10 memiliki fungsi konyol yang mencetak nilai
parameternya dan mengembalikan 10, beserta pengujian yang lulus dan
pengujian yang gagal.

<Listing number="11-10" file-name="src/lib.rs" caption="Pengujian untuk fungsi yang memanggil `println!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

Ketika kita menjalankan pengujian-pengujian ini dengan `cargo test`, kita
akan melihat keluaran berikut:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

Perhatikan bahwa di keluaran ini tidak ada tempat kita melihat `I got the
value 4`, yang dicetak ketika pengujian yang lulus dijalankan. Keluaran itu
telah ditangkap. Keluaran dari pengujian yang gagal, `I got the value 8`,
muncul di bagian keluaran ringkasan pengujian, yang juga menunjukkan
penyebab kegagalan pengujian.

Jika kita ingin melihat nilai yang dicetak untuk pengujian yang lulus juga,
kita bisa memberi tahu Rust untuk menampilkan juga keluaran pengujian yang
berhasil dengan `--show-output`:

```console
$ cargo test -- --show-output
```

Ketika kita menjalankan lagi pengujian di Listing 11-10 dengan flag
`--show-output`, kita melihat keluaran berikut:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

<a id="running-a-subset-of-tests-by-name"></a>
### Menjalankan Sebagian Pengujian Berdasarkan Nama

Menjalankan test suite penuh kadang bisa memakan waktu lama. Jika Anda
sedang mengerjakan kode di area tertentu, Anda mungkin ingin menjalankan
hanya pengujian yang berkaitan dengan kode itu. Anda bisa memilih pengujian
mana yang dijalankan dengan meneruskan nama pengujian yang ingin Anda
jalankan ke `cargo test` sebagai argumen.

Untuk mendemonstrasikan cara menjalankan sebagian pengujian, pertama kita
akan membuat tiga pengujian untuk fungsi `add_two` kita, seperti yang
ditunjukkan di Listing 11-11, lalu memilih mana yang akan dijalankan.

<Listing number="11-11" file-name="src/lib.rs" caption="Tiga pengujian dengan tiga nama berbeda">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

Jika kita menjalankan pengujian tanpa meneruskan argumen apa pun, seperti
yang kita lihat sebelumnya, semua pengujian akan berjalan paralel:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### Menjalankan Satu Pengujian

Kita bisa meneruskan nama fungsi pengujian mana pun ke `cargo test` untuk
menjalankan pengujian itu saja:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

Hanya pengujian dengan nama `one_hundred` yang berjalan; dua pengujian
lainnya tidak cocok dengan nama itu. Keluaran pengujian memberi tahu kita
bahwa ada pengujian lain yang tidak dijalankan dengan menampilkan `2
filtered out` di bagian akhir.

Kita tidak bisa menentukan nama beberapa pengujian dengan cara ini; hanya
nilai pertama yang diberikan ke `cargo test` yang akan dipakai. Namun, ada
cara untuk menjalankan beberapa pengujian.

#### Menyaring untuk Menjalankan Beberapa Pengujian

Kita bisa menentukan sebagian nama pengujian, dan pengujian mana pun yang
namanya cocok dengan nilai itu akan dijalankan. Sebagai contoh, karena dua
nama pengujian kita mengandung `add`, kita bisa menjalankan keduanya dengan
menjalankan `cargo test add`:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

Perintah ini menjalankan semua pengujian dengan `add` di namanya dan
menyaring keluar pengujian bernama `one_hundred`. Perhatikan juga bahwa
modul tempat sebuah pengujian muncul menjadi bagian dari nama pengujian itu,
jadi kita bisa menjalankan semua pengujian dalam sebuah modul dengan
menyaring berdasarkan nama modulnya.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

<a id="ignoring-tests-unless-specifically-requested"></a>
### Mengabaikan Pengujian Kecuali Diminta Secara Spesifik

Terkadang beberapa pengujian tertentu bisa sangat memakan waktu untuk
dieksekusi, jadi Anda mungkin ingin mengecualikannya pada sebagian besar
penjalanan `cargo test`. Alih-alih mendaftarkan semua pengujian yang ingin
Anda jalankan sebagai argumen, Anda bisa menganotasi pengujian yang memakan
waktu itu memakai atribut `ignore` untuk mengecualikannya, seperti yang
ditunjukkan di sini:

<span class="filename">Nama File: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

Setelah `#[test]`, kita menambahkan baris `#[ignore]` ke pengujian yang
ingin kita kecualikan. Sekarang ketika kita menjalankan pengujian,
`it_works` berjalan, tetapi `expensive_test` tidak:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

Fungsi `expensive_test` didaftarkan sebagai `ignored`. Jika kita ingin
menjalankan hanya pengujian yang diabaikan, kita bisa memakai `cargo test
-- --ignored`:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

Dengan mengontrol pengujian mana yang dijalankan, Anda bisa memastikan
hasil `cargo test` Anda akan kembali dengan cepat. Ketika Anda berada pada
titik ketika masuk akal untuk memeriksa hasil pengujian `ignored` dan Anda
punya waktu untuk menunggu hasilnya, Anda bisa menjalankan `cargo test --
--ignored`. Jika Anda ingin menjalankan semua pengujian, baik yang
diabaikan maupun tidak, Anda bisa menjalankan `cargo test --
--include-ignored`.
