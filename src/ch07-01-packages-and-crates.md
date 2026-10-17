## Package dan Crate

Bagian pertama dari *module system* yang akan kita bahas adalah *package* dan
*crate*.

Sebuah *crate* adalah jumlah kode terkecil yang dipertimbangkan oleh
*compiler* (kompilator) Rust pada suatu waktu. Bahkan jika Anda menjalankan
`rustc` alih-alih `cargo` dan memberikan satu file kode sumber (seperti yang
kita lakukan jauh di [“Dasar-Dasar Program Rust”][basics]<!-- ignore
--> di Bab 1), compiler menganggap file tersebut sebagai sebuah crate. Crate
dapat berisi *module*, dan *module* tersebut dapat didefinisikan di file lain yang
ikut dikompilasi bersama *crate*, seperti yang akan kita lihat di bagian-bagian
selanjutnya.

Sebuah *crate* dapat hadir dalam salah satu dari dua bentuk: *crate* binary atau
*crate* library. *Crate binary* adalah program yang dapat Anda kompilasi menjadi
file yang dapat dieksekusi yang dapat Anda jalankan, seperti program baris
perintah atau server. Masing-masing harus memiliki sebuah fungsi bernama
`main` yang menentukan apa yang terjadi ketika file yang dapat dieksekusi itu
dijalankan. Semua *crate* yang kita buat sejauh ini adalah *crate* binary.

*Crate library* tidak memiliki fungsi `main`, dan tidak dikompilasi menjadi
file yang dapat dieksekusi. Alih-alih, *crate* library mendefinisikan
fungsionalitas yang dimaksudkan untuk dibagikan ke beberapa proyek. Misalnya,
crate `rand` yang kita pakai di [Bab 2][rand]<!-- ignore --> menyediakan
fungsionalitas yang menghasilkan angka acak. Sebagian besar waktu, ketika para
Rustacean menyebut “*crate*”, yang mereka maksud adalah *crate* library, dan
mereka memakai “*crate*” secara bergantian dengan konsep pemrograman umum
“library”.

*Crate root* (akar *crate*) adalah file sumber yang menjadi titik awal *compiler*
Rust dan menyusun *module* akar dari *crate* Anda (kita akan menjelaskan *module*
secara mendalam di [“Mengontrol *Scope* dan Privasi dengan
Module”][modules]<!-- ignore -->).

Sebuah *package* (paket) adalah bundel berisi satu *crate* atau lebih yang
menyediakan sekumpulan fungsionalitas. Sebuah *package* berisi file _Cargo.toml_
yang menjelaskan cara membangun *crate*-crate tersebut. Cargo sendiri sebenarnya
adalah sebuah *package* yang berisi *crate* binary untuk alat baris perintah yang
selama ini Anda pakai untuk membangun kode Anda. *Package* Cargo juga berisi
sebuah *crate* library yang menjadi dependensi *crate* binary tersebut. Proyek
lain dapat bergantung pada *crate* library Cargo untuk memakai logika yang sama
dengan yang dipakai alat baris perintah Cargo.

Sebuah *package* dapat berisi *crate* binary sebanyak yang Anda mau, tetapi paling
banyak hanya satu *crate* library. Sebuah *package* harus berisi paling sedikit
satu *crate*, entah itu *crate* library maupun *crate* binary.

Mari kita telusuri apa yang terjadi ketika kita membuat sebuah *package*.
Pertama, kita masukkan perintah `cargo new my-project`:

```console
$ cargo new my-project
     Created binary (application) `my-project` package
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

Setelah menjalankan `cargo new my-project`, kita memakai `ls` untuk melihat
apa yang dibuat Cargo. Di dalam direktori _my-project_, ada file _Cargo.toml_
yang memberi kita sebuah *package*. Ada juga direktori _src_ yang berisi
_main.rs_. Buka _Cargo.toml_ di editor teks Anda dan perhatikan bahwa tidak
ada penyebutan _src/main.rs_ di sana. Cargo mengikuti konvensi bahwa
_src/main.rs_ adalah *crate root* dari sebuah *crate* binary dengan nama yang sama
dengan *package*. Demikian pula, Cargo tahu bahwa jika direktori *package* berisi
_src/lib.rs_, *package* tersebut berisi sebuah *crate* library dengan nama yang
sama dengan *package*, dan _src/lib.rs_ adalah *crate root*-nya. Cargo meneruskan
file-file *crate root* tersebut ke `rustc` untuk membangun library atau binary.

Di sini, kita memiliki sebuah *package* yang hanya berisi _src/main.rs_, yang
berarti *package* ini hanya berisi sebuah *crate* binary bernama `my-project`.
Jika sebuah *package* berisi _src/main.rs_ dan _src/lib.rs_, *package* itu
memiliki dua *crate*: sebuah *crate* binary dan sebuah *crate* library, keduanya
dengan nama yang sama dengan *package*. Sebuah *package* dapat memiliki beberapa
*crate* binary dengan menempatkan file-file di direktori _src/bin_: setiap file
akan menjadi sebuah *crate* binary yang terpisah.

[basics]: ch01-02-hello-world.html#rust-program-basics
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
