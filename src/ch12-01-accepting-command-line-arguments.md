## Menerima Argumen Baris Perintah

Mari kita membuat proyek baru dengan, seperti biasa, `cargo new`. Kita akan
menamai proyek kita `minigrep` untuk membedakannya dari tool `grep` yang
mungkin sudah ada di sistem Anda:

```console
$ cargo new minigrep
     Created binary (application) `minigrep` project
$ cd minigrep
```

Tugas pertama adalah membuat `minigrep` menerima dua argumen baris
perintahnya: *path* file dan sebuah string yang akan dicari. Artinya, kita ingin
dapat menjalankan program kita dengan `cargo run`, dua tanda hubung untuk
menandakan bahwa argumen-argumen berikutnya ditujukan untuk program kita dan
bukan untuk `cargo`, sebuah string yang dicari, dan sebuah *path* menuju file
yang akan dicari di dalamnya, seperti berikut:

```console
$ cargo run -- searchstring example-filename.txt
```

Saat ini, program yang dihasilkan oleh `cargo new` belum dapat memproses
argumen yang kita berikan. Beberapa pustaka yang sudah ada di
[crates.io](https://crates.io/) dapat membantu menulis program yang menerima
argumen command line, tetapi karena Anda baru saja mempelajari konsep ini,
mari kita implementasikan kemampuan ini sendiri.

### Membaca Nilai Argumen

Agar `minigrep` dapat membaca nilai-nilai argumen command line yang kita
teruskan kepadanya, kita memerlukan fungsi `std::env::args` yang disediakan
oleh standard library Rust. Fungsi ini mengembalikan sebuah *iterator* atas
argumen-argumen command line yang diteruskan ke `minigrep`. Kita akan
membahas *iterator* secara menyeluruh di [Bab 13][ch13]<!-- ignore -->. Untuk
saat ini, Anda hanya perlu mengetahui dua hal tentang *iterator*: *Iterator*
menghasilkan serangkaian nilai, dan kita dapat memanggil method `collect` pada
sebuah *iterator* untuk mengubahnya menjadi sebuah collection, seperti vector,
yang memuat semua elemen yang dihasilkan oleh *iterator* tersebut.

Kode di Listing 12-1 memungkinkan program `minigrep` Anda membaca semua
argumen command line yang diteruskan kepadanya, lalu mengumpulkan nilainya
ke dalam sebuah vector.

<Listing number="12-1" file-name="src/main.rs" caption="Mengumpulkan argumen command line ke dalam sebuah vector dan mencetaknya">

```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-01/src/main.rs}}
```

</Listing>

Pertama, kita membawa *module* (modul) `std::env` ke dalam *scope* (cakupan)
dengan statement `use` sehingga kita dapat memakai fungsi `args`-nya.
Perhatikan bahwa fungsi `std::env::args` bersarang di dalam dua tingkat modul.
Seperti yang kita bahas di [Bab 7][ch7-idiomatic-use]<!-- ignore -->, ketika
fungsi yang diinginkan bersarang di dalam lebih dari satu modul, kita memilih
untuk membawa modul *parent* (induk) ke dalam *scope* alih-alih fungsinya.
Dengan begitu, kita dapat dengan mudah memakai fungsi-fungsi lain dari
`std::env`. Cara ini juga lebih tidak ambigu daripada menambahkan
`use std::env::args` lalu memanggil fungsinya dengan `args` saja, karena
`args` dapat dengan mudah disangka sebagai fungsi yang didefinisikan di modul
saat ini.

> ### Fungsi `args` dan Unicode yang Tidak Valid
>
> Perhatikan bahwa `std::env::args` akan panic jika ada argumen yang memuat
> Unicode yang tidak valid. Jika program Anda perlu menerima argumen yang
> memuat Unicode yang tidak valid, pakailah `std::env::args_os`. Fungsi itu
> mengembalikan sebuah *iterator* yang menghasilkan nilai `OsString`, bukan
> nilai `String`. Di sini kita memilih memakai `std::env::args` demi
> kesederhanaan karena nilai `OsString` berbeda-beda di tiap platform dan
> lebih rumit untuk diolah daripada nilai `String`.

Pada baris pertama `main`, kita memanggil `env::args`, lalu segera memakai
`collect` untuk mengubah *iterator* tersebut menjadi sebuah vector yang memuat
semua nilai yang dihasilkan oleh *iterator* itu. Kita dapat memakai fungsi
`collect` untuk membuat berbagai jenis collection, jadi kita mengtype annotation
`args` secara eksplisit untuk menyatakan bahwa kita menginginkan sebuah vector
berisi string. Meskipun Anda sangat jarang perlu mengtype annotation di Rust,
`collect` adalah salah satu fungsi yang memang sering perlu Anda anotasi
karena Rust tidak mampu menginferensi jenis collection yang Anda inginkan.

Akhirnya, kita mencetak vector tersebut memakai *macro* (makro) debug. Mari
kita coba menjalankan kode ini, mula-mula tanpa argumen lalu dengan dua
argumen:

```console
{{#include ../listings/ch12-an-io-project/listing-12-01/output.txt}}
```

```console
{{#include ../listings/ch12-an-io-project/output-only-01-with-args/output.txt}}
```

Perhatikan bahwa nilai pertama di dalam vector itu adalah
`"target/debug/minigrep"`, yaitu nama binary kita. Ini cocok dengan perilaku
daftar argumen di C, yang memungkinkan program memakai nama yang digunakan
untuk memanggilnya saat dieksekusi. Akses ke nama program sering kali berguna
jika Anda ingin mencetaknya di dalam pesan atau mengubah perilaku program
berdasarkan alias command line yang dipakai untuk memanggil program
tersebut. Tetapi untuk keperluan bab ini, kita akan mengabaikannya dan hanya
menyimpan dua argumen yang kita butuhkan.

### Menyimpan Nilai Argumen di dalam Variable

Saat ini program sudah dapat mengakses nilai-nilai yang diberikan sebagai
argumen command line. Sekarang kita perlu menyimpan nilai kedua argumen
tersebut di dalam variable agar kita dapat memakai nilai-nilai itu di seluruh
bagian program selanjutnya. Kita melakukannya di Listing 12-2.

<Listing number="12-2" file-name="src/main.rs" caption="Membuat variable untuk menampung argumen kueri dan argumen path file">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-02/src/main.rs}}
```

</Listing>

Seperti yang kita lihat saat mencetak vector tersebut, nama program menempati
nilai pertama di dalam vector pada `args[0]`, jadi kita memulai argumen dari
indeks 1. Argumen pertama yang diterima `minigrep` adalah string yang kita
cari, jadi kita menaruh sebuah *reference* (referensi) ke argumen pertama di
dalam variable `query`. Argumen kedua adalah *path* file, jadi kita menaruh
sebuah *reference* ke argumen kedua di dalam variable `file_path`.

Kita mencetak nilai variable-variable ini untuk sementara guna membuktikan
bahwa kode ini bekerja seperti yang kita inginkan. Mari kita jalankan lagi
program ini dengan argumen `test` dan `sample.txt`:

```console
{{#include ../listings/ch12-an-io-project/listing-12-02/output.txt}}
```

Hebat, programnya bekerja! Nilai-nilai argumen yang kita butuhkan tersimpan di
variable yang tepat. Nanti kita akan menambahkan penanganan error untuk
menangani situasi-situasi yang berpotensi keliru, misalnya ketika pengguna
tidak memberikan argumen; untuk saat ini, kita akan mengabaikan situasi itu
dan mengerjakan penambahan kemampuan membaca file.

[ch13]: ch13-00-functional-features.html
[ch7-idiomatic-use]: ch07-04-bringing-paths-into-scope-with-the-use-keyword.html#creating-idiomatic-use-paths
