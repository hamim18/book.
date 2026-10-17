## Memakai Thread untuk Menjalankan Kode Secara Bersamaan

Di sebagian besar sistem operasi saat ini, kode program yang dieksekusi
dijalankan dalam sebuah _process_ (proses), dan sistem operasi mengelola
beberapa proses sekaligus. Di dalam sebuah program, Anda juga dapat memiliki
bagian-bagian independen yang berjalan secara bersamaan. Fitur yang
menjalankan bagian-bagian independen ini disebut _thread_. Sebagai contoh,
sebuah web server bisa memiliki beberapa thread supaya ia dapat menanggapi
lebih dari satu permintaan pada saat yang sama.

Memecah komputasi dalam program Anda menjadi beberapa thread untuk
menjalankan beberapa tugas pada saat yang sama dapat meningkatkan performa,
tetapi juga menambah kompleksitas. Karena thread dapat berjalan secara
bersamaan, tidak ada jaminan bawaan tentang urutan berjalannya bagian-bagian
kode Anda pada thread yang berbeda. Ini dapat menimbulkan masalah, seperti:

- Race condition, ketika thread mengakses data atau sumber daya dalam urutan yang
  tidak konsisten
- *Deadlock* (kebuntuan), ketika dua thread saling menunggu, sehingga
  mencegah keduanya untuk melanjutkan
- Bug yang hanya terjadi dalam situasi tertentu dan sulit direproduksi serta
  diperbaiki secara andal

Rust berupaya memitigasi efek negatif pemakaian thread, tetapi pemrograman
dalam konteks multithreaded tetap menuntut pemikiran yang cermat dan
membutuhkan struktur kode yang berbeda dari program yang berjalan dalam satu
thread.

Bahasa-bahasa pemrograman mengimplementasikan thread dengan beberapa cara
berbeda, dan banyak sistem operasi menyediakan API yang dapat dipanggil bahasa
pemrograman untuk membuat thread baru. Pustaka standar Rust memakai model
implementasi thread _1:1_, yang berarti sebuah program memakai satu thread
sistem operasi untuk setiap satu thread bahasa. Ada *crate*-crate yang
mengimplementasikan model threading lain yang membuat kompromi berbeda dari
model 1:1. (Sistem async Rust, yang akan kita lihat di bab berikutnya, juga
menyediakan pendekatan lain terhadap concurrency.)

<a id="creating-a-new-thread-with-spawn"></a>
### Membuat Thread Baru dengan `spawn`

Untuk membuat thread baru, kita memanggil fungsi `thread::spawn` dan
memberikannya sebuah *closure* (kita membahas *closure* di Bab 13) yang memuat
kode yang ingin kita jalankan di thread baru itu. Contoh di Listing 16-1
mencetak beberapa teks dari thread utama dan teks lain dari thread baru.

<Listing number="16-1" file-name="src/main.rs" caption="Membuat thread baru untuk mencetak satu hal sementara thread utama mencetak hal lain">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```

</Listing>

Perhatikan bahwa ketika thread utama sebuah program Rust selesai, semua thread
yang dibuat akan dimatikan, entah mereka sudah selesai berjalan atau belum.
Output program ini mungkin sedikit berbeda setiap kali dijalankan, tetapi
akan tampak serupa dengan yang berikut:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

Panggilan ke `thread::sleep` memaksa sebuah thread menghentikan eksekusinya
untuk sesaat, sehingga memungkinkan thread lain berjalan. Thread-thread itu
kemungkinan besar akan bergiliran, tetapi itu tidak dijamin: Tergantung
bagaimana sistem operasi Anda menjadwalkan thread-thread itu. Pada
penjalanan ini, thread utama mencetak lebih dulu, meskipun statement cetak
dari thread yang dibuat muncul lebih dulu di kode. Dan meskipun kita menyuruh
thread yang dibuat itu mencetak sampai `i` bernilai `9`, ia hanya sampai `5`
sebelum thread utama dimatikan.

Jika Anda menjalankan kode ini dan hanya melihat output dari thread utama,
atau tidak melihat tumpang tindih sama sekali, coba perbesar angka pada
range-nya untuk menciptakan lebih banyak peluang bagi sistem operasi untuk
berpindah antar-thread.

<!-- Old headings. Do not remove or links may break. -->

<a id="waiting-for-all-threads-to-finish-using-join-handles"></a>

<a id="waiting-for-all-threads-to-finish"></a>
### Menunggu Semua Thread Selesai

Kode di Listing 16-1 tidak hanya menghentikan thread yang dibuat secara dini
pada sebagian besar waktu karena thread utamanya berakhir, tetapi karena tidak
ada jaminan tentang urutan berjalannya thread, kita juga tidak bisa menjamin
bahwa thread yang dibuat itu akan sempat berjalan sama sekali!

Kita dapat memperbaiki masalah thread yang dibuat tidak berjalan atau
berakhir terlalu dini dengan menyimpan return value `thread::spawn` di
sebuah variable. Type kembalian `thread::spawn` adalah `JoinHandle<T>`.
`JoinHandle<T>` adalah nilai yang dimiliki yang, ketika kita memanggil method
`join` padanya, akan menunggu thread-nya selesai. Listing 16-2 menunjukkan
cara memakai `JoinHandle<T>` dari thread yang kita buat di Listing 16-1 dan
cara memanggil `join` untuk memastikan thread yang dibuat selesai sebelum
`main` keluar.

<Listing number="16-2" file-name="src/main.rs" caption="Menyimpan `JoinHandle<T>` dari `thread::spawn` untuk menjamin thread dijalankan sampai selesai">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```

</Listing>

Memanggil `join` pada handle itu memblokir thread yang sedang berjalan sampai
thread yang direpresentasikan handle itu berakhir. _Blocking_ (pemblokiran)
sebuah thread berarti thread itu dicegah melakukan pekerjaan atau keluar.
Karena kita meletakkan panggilan ke `join` setelah loop `for` thread
utama, menjalankan Listing 16-2 seharusnya menghasilkan output yang serupa
dengan ini:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

Kedua thread terus bergantian, tetapi thread utama menunggu karena panggilan
ke `handle.join()` dan tidak berakhir sampai thread yang dibuat selesai.

Tetapi mari kita lihat apa yang terjadi ketika kita justru memindahkan
`handle.join()` ke sebelum loop `for` di `main`, seperti ini:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```

</Listing>

Thread utama akan menunggu thread yang dibuat selesai, lalu menjalankan
loop `for`-nya, jadi outputnya tidak akan saling menyelip lagi,
seperti ditunjukkan di sini:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

Detail kecil, seperti di mana `join` dipanggil, dapat memengaruhi apakah
thread-thread Anda berjalan pada saat yang sama atau tidak.

<a id="using-move-closures-with-threads"></a>
### Memakai Closure `move` dengan Thread

Kita akan sering memakai kata kunci `move` dengan *closure* yang diberikan ke
`thread::spawn` karena *closure* itu kemudian akan mengambil *ownership* atas
nilai-nilai yang dipakainya dari lingkungannya, sehingga memindahkan
*ownership* nilai-nilai itu dari satu thread ke thread lain. Di [“Menangkap
*Reference* atau Memindahkan *Ownership*”][capture]<!-- ignore --> di Bab 13,
kita membahas `move` dalam konteks *closure*. Sekarang kita akan lebih
berkonsentrasi pada interaksi antara `move` dan `thread::spawn`.

Perhatikan di Listing 16-1 bahwa *closure* yang kita berikan ke `thread::spawn`
tidak menerima argumen: Kita tidak memakai data apa pun dari thread utama di
kode thread yang dibuat. Untuk memakai data dari thread utama di thread yang
dibuat, *closure* thread yang dibuat itu harus menangkap nilai yang
dibutuhkannya. Listing 16-3 menunjukkan upaya membuat vector di thread utama
dan memakainya di thread yang dibuat. Namun, ini belum akan berhasil, seperti
yang akan Anda lihat sebentar lagi.

<Listing number="16-3" file-name="src/main.rs" caption="Mencoba memakai vector yang dibuat oleh thread utama di thread lain">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```

</Listing>

*Closure* itu memakai `v`, jadi ia akan menangkap `v` dan menjadikannya bagian
dari lingkungan *closure*. Karena `thread::spawn` menjalankan *closure* ini di
thread baru, seharusnya kita dapat mengakses `v` di dalam thread baru itu.
Tetapi ketika kita mengompilasi contoh ini, kita mendapat error berikut:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```

Rust _menginferensi_ cara menangkap `v`, dan karena `println!` hanya
membutuhkan *reference* ke `v`, *closure* itu mencoba meminjam `v`. Namun, ada
masalah: Rust tidak bisa tahu berapa lama thread yang dibuat akan berjalan,
jadi ia tidak tahu apakah *reference* ke `v` akan selalu valid.

Listing 16-4 menyediakan skenario yang lebih mungkin memiliki *reference* ke
`v` yang tidak akan valid.

<Listing number="16-4" file-name="src/main.rs" caption="Thread dengan closure yang mencoba menangkap reference ke `v` dari thread utama yang membebaskan `v`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```

</Listing>

Jika Rust mengizinkan kita menjalankan kode ini, ada kemungkinan thread yang
dibuat itu langsung ditempatkan di latar belakang tanpa berjalan sama sekali.
Thread yang dibuat itu memiliki *reference* ke `v` di dalamnya, tetapi thread
utama langsung membebaskan `v`, memakai fungsi `drop` yang kita bahas di Bab
15. Kemudian, ketika thread yang dibuat mulai mengeksekusi, `v` tidak lagi
valid, jadi *reference* padanya juga tidak valid. Waduh!

Untuk memperbaiki error *compiler* di Listing 16-3, kita dapat memakai saran
dari pesan error itu:

<!-- manual-regeneration
after automatic regeneration, look at listings/ch16-fearless-concurrency/listing-16-03/output.txt and copy the relevant part
-->

```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

Dengan menambahkan kata kunci `move` sebelum *closure*, kita memaksa *closure*
untuk mengambil *ownership* atas nilai-nilai yang dipakainya alih-alih
membiarkan Rust menginferensi bahwa ia harus meminjam nilai-nilai itu.
Modifikasi Listing 16-3 yang ditunjukkan pada Listing 16-5 akan terkompilasi
dan berjalan seperti yang kita maksud.

<Listing number="16-5" file-name="src/main.rs" caption="Memakai kata kunci `move` untuk memaksa closure mengambil ownership atas nilai-nilai yang dipakainya">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```

</Listing>

Kita mungkin tergoda mencoba hal yang sama untuk memperbaiki kode di Listing
16-4, tempat thread utama memanggil `drop`, dengan memakai *closure* `move`.
Namun, perbaikan ini tidak akan berhasil karena apa yang coba dilakukan
Listing 16-4 dilarang karena alasan yang berbeda. Jika kita menambahkan
`move` ke *closure* itu, kita akan memindahkan `v` ke lingkungan *closure*, dan
kita tidak bisa lagi memanggil `drop` padanya di thread utama. Kita akan
mendapat error *compiler* ini sebagai gantinya:

```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```

Aturan *ownership* Rust telah menyelamatkan kita lagi! Kita mendapat error dari
kode di Listing 16-3 karena Rust bersikap konservatif dan hanya meminjam `v`
untuk thread itu, yang berarti thread utama secara teoretis bisa membatalkan
validitas *reference* thread yang dibuat. Dengan menyuruh Rust memindahkan
*ownership* `v` ke thread yang dibuat, kita menjamin kepada Rust bahwa thread
utama tidak akan memakai `v` lagi. Jika kita mengubah Listing 16-4 dengan
cara yang sama, kita kemudian melanggar aturan *ownership* ketika mencoba
memakai `v` di thread utama. Kata kunci `move` menimpa default konservatif
Rust berupa *borrowing*; ia tidak mengizinkan kita melanggar aturan *ownership*.

Sekarang setelah kita membahas apa itu thread dan method-method yang
disediakan API thread, mari kita lihat beberapa situasi ketika kita dapat
memakai thread.

[capture]: ch13-01-closures.html#capturing-references-or-moving-ownership
