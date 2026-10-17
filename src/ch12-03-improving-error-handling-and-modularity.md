## Refactoring untuk Meningkatkan Modularitas dan Penanganan Error

Untuk memperbaiki program kita, kita akan menyelesaikan empat masalah yang
berkaitan dengan struktur program dan cara program ini menangani error yang
mungkin terjadi. Pertama, fungsi `main` kita kini melakukan dua tugas: fungsi
itu melakukan parsing argumen dan membaca file. Seiring pertumbuhan program
kita, jumlah tugas terpisah yang ditangani fungsi `main` akan bertambah.
Ketika sebuah fungsi memperoleh tanggung jawab, fungsi itu menjadi semakin
sulit untuk dinalar, semakin sulit untuk diuji, dan semakin sulit untuk diubah
tanpa merusak salah satu bagiannya. Sebaiknya fungsionalitas dipisahkan
sehingga setiap fungsi bertanggung jawab atas satu tugas.

Masalah ini juga berkaitan dengan masalah kedua: Meskipun `query` dan
`file_path` adalah configuration variable untuk program kita, variable seperti
`contents` dipakai untuk menjalankan logika program. Semakin panjang `main`,
semakin banyak variable yang perlu kita bawa ke dalam *scope*; semakin banyak
variable di dalam *scope*, semakin sulit melacak tujuan masing-masing.
Sebaiknya variable-configuration variable dikelompokkan ke dalam satu struktur
untuk memperjelas tujuannya.

Masalah ketiga adalah kita telah memakai `expect` untuk mencetak pesan error
ketika pembacaan file gagal, tetapi pesan error itu hanya mencetak
`Should have been able to read the file`. Membaca file dapat gagal dalam
berbagai cara: misalnya, file itu mungkin tidak ada, atau kita mungkin tidak
memiliki izin untuk membukanya. Saat ini, apa pun situasinya, kita akan
mencetak pesan error yang sama untuk semuanya, yang tidak memberi informasi
apa pun kepada pengguna!

Keempat, kita memakai `expect` untuk menangani error, dan jika pengguna
menjalankan program kita tanpa memberikan cukup argumen, mereka akan mendapat
error `index out of bounds` dari Rust yang tidak menjelaskan masalahnya dengan
jelas. Akan lebih baik jika seluruh kode penanganan error berada di satu
tempat sehingga pengelola kode di masa depan hanya perlu melihat satu tempat
jika logika penanganan errornya perlu diubah. Menaruh seluruh kode penanganan
error di satu tempat juga akan memastikan bahwa kita mencetak pesan yang
bermakna bagi pengguna akhir kita.

Mari kita tangani keempat masalah ini dengan melakukan refactoring pada
proyek kita.

<!-- Old headings. Do not remove or links may break. -->

<a id="separation-of-concerns-for-binary-projects"></a>

### Memisahkan Tanggung Jawab dalam Proyek Binary

Masalah organisasi berupa penyerahan tanggung jawab banyak tugas kepada fungsi
`main` ini umum dijumpai di banyak proyek binary. Akibatnya, banyak pemrogram
Rust merasa berguna untuk memisahkan berbagai tanggung jawab sebuah program
binary ketika fungsi `main` mulai membesar. Proses ini memiliki langkah-langkah
berikut:

- Pecah program Anda menjadi file _main.rs_ dan file _lib.rs_, lalu pindahkan
  logika program Anda ke _lib.rs_.
- Selama logika parsing baris perintah Anda masih kecil, logika itu dapat
  tetap berada di fungsi `main`.
- Ketika logika parsing baris perintah mulai menjadi rumit, ekstrak logika itu
  dari fungsi `main` ke fungsi atau type lain.

Tanggung jawab yang tersisa di fungsi `main` setelah proses ini sebaiknya
dibatasi pada hal-hal berikut:

- Memanggil logika parsing baris perintah dengan nilai-nilai argumen
- Menyiapkan konfigurasi lain apa pun
- Memanggil fungsi `run` di _lib.rs_
- Menangani error jika `run` mengembalikan error

Pattern ini berkaitan dengan pemisahan tanggung jawab: _main.rs_ menangani
jalannya program dan _lib.rs_ menangani seluruh logika tugas yang sedang
dikerjakan. Karena Anda tidak dapat menguji fungsi `main` secara langsung,
struktur ini memungkinkan Anda menguji seluruh logika program Anda dengan
memindahkannya keluar dari fungsi `main`. Kode yang tersisa di fungsi `main`
akan cukup kecil untuk diverifikasi kebenarannya hanya dengan membacanya. Mari
kita kerjakan ulang program kita dengan mengikuti proses ini.

#### Mengekstrak Parser Argumen

Kita akan mengekstrak fungsionalitas untuk parsing argumen ke dalam sebuah
fungsi yang akan dipanggil oleh `main`. Listing 12-5 menunjukkan awal baru
fungsi `main` yang memanggil fungsi baru `parse_config`, yang akan kita
definisikan di _src/main.rs_.

<Listing number="12-5" file-name="src/main.rs" caption="Mengekstrak fungsi `parse_config` dari `main`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

Kita masih mengumpulkan argumen baris perintah ke dalam sebuah vector, tetapi
alih-alih menetapkan nilai argumen pada indeks 1 ke variable `query` dan nilai
argumen pada indeks 2 ke variable `file_path` di dalam fungsi `main`, kita
meneruskan seluruh vector tersebut ke fungsi `parse_config`. Fungsi
`parse_config` kemudian memegang logika yang menentukan argumen mana yang masuk
ke variable mana, lalu meneruskan nilai-nilainya kembali ke `main`. Kita masih
membuat variable `query` dan `file_path` di `main`, tetapi `main` tidak lagi
bertanggung jawab menentukan bagaimana argumen baris perintah dan
variable-variable itu saling berkorespondensi.

Pengerjaan ulang ini mungkin tampak berlebihan untuk program sekecil ini,
tetapi kita melakukan refactoring dalam langkah-langkah kecil yang bertahap.
Setelah melakukan perubahan ini, jalankan lagi programnya untuk memastikan
parsing argumennya masih bekerja. Ada baiknya Anda sering memeriksa kemajuan
Anda, untuk membantu mengidentifikasi penyebab masalah saat masalah itu
terjadi.

#### Mengelompokkan Nilai Konfigurasi

Kita dapat mengambil satu langkah kecil lagi untuk memperbaiki fungsi
`parse_config` lebih jauh. Saat ini, kita mengembalikan sebuah *tuple*, tetapi
kemudian kita langsung memecah *tuple* itu menjadi bagian-bagian individual
lagi. Ini adalah tanda bahwa mungkin kita belum memiliki abstraksi yang tepat.

Indikator lain yang menunjukkan masih ada ruang untuk perbaikan adalah bagian
`config` dari `parse_config`, yang mengisyaratkan bahwa dua nilai yang kita
kembalikan saling berkaitan dan keduanya merupakan bagian dari satu nilai
konfigurasi. Saat ini kita belum menyampaikan makna ini di dalam struktur
datanya selain dengan mengelompokkan kedua nilai itu ke dalam sebuah *tuple*;
sebagai gantinya, kita akan menaruh kedua nilai tersebut ke dalam satu *struct*
dan memberi setiap *field* (medan) *struct* itu nama yang bermakna. Dengan
begitu, pengelola kode ini di masa depan akan lebih mudah memahami bagaimana
nilai-nilai yang berbeda saling berkaitan dan apa tujuan mereka.

Listing 12-6 menunjukkan perbaikan pada fungsi `parse_config`.

<Listing number="12-6" file-name="src/main.rs" caption="Melakukan refactoring pada `parse_config` agar mengembalikan sebuah instance dari struct `Config`">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

Kita telah menambahkan sebuah *struct* bernama `Config` yang didefinisikan
memiliki *field*-field bernama `query` dan `file_path`. Tanda tangan
`parse_config` kini menunjukkan bahwa fungsi itu mengembalikan sebuah nilai
`Config`. Di dalam badan `parse_config`, tempat yang sebelumnya kita pakai
untuk mengembalikan string *slice* yang mereferensikan nilai-nilai `String` di
`args`, kini kita mendefinisikan `Config` untuk memuat nilai-nilai `String`
yang dimiliki. Variable `args` di dalam `main` adalah *owner* (pemilik) dari
nilai-nilai argumen dan hanya membiarkan fungsi `parse_config` meminjam
nilai-nilai itu, yang berarti kita akan melanggar aturan *borrowing*
(*borrowing*) Rust jika `Config` mencoba mengambil *ownership* (kepemilikan)
atas nilai-nilai di dalam `args`.

Ada sejumlah cara untuk mengelola data `String`; rute termudah, meskipun agak
tidak efisien, adalah memanggil method `clone` pada nilai-nilai tersebut. Cara
ini akan membuat copy penuh dari data tersebut untuk dimiliki oleh instance
`Config`, yang memakan lebih banyak waktu dan memori daripada menyimpan sebuah
*reference* ke data string itu. Akan tetapi, meng-clone data juga membuat kode
kita sangat lugas karena kita tidak perlu mengelola *lifetime* dari
*reference*-reference itu; dalam keadaan ini, melepaskan sedikit performa demi
kesederhanaan adalah pertukaran yang layak.

> ### Pertukaran dari Pemakaian `clone`
>
> Ada kecenderungan di antara banyak Rustaceans untuk menghindari pemakaian
> `clone` untuk menyelesaikan masalah *ownership* karena biaya runtime-nya. Di
> [Bab 13][ch13]<!-- ignore -->, Anda akan mempelajari cara memakai method
> yang lebih efisien dalam situasi semacam ini. Tetapi untuk saat ini, tidak
> apa-apa menyalin beberapa string untuk terus membuat kemajuan karena Anda
> hanya akan membuat copy-copy ini sekali dan *path* file serta string
> kueri Anda sangat kecil. Lebih baik memiliki program yang bekerja meskipun
> sedikit tidak efisien daripada mencoba mengoptimasi kode secara berlebihan
> pada percobaan pertama Anda. Seiring bertambahnya pengalaman Anda dengan
> Rust, akan lebih mudah untuk memulai dengan solusi yang paling efisien,
> tetapi untuk saat ini, memanggil `clone` sepenuhnya dapat diterima.

Kita telah memperbarui `main` sehingga ia menaruh instance `Config` yang
dikembalikan oleh `parse_config` ke dalam sebuah variable bernama `config`,
dan kita memperbarui kode yang sebelumnya memakai variable `query` dan
`file_path` yang terpisah sehingga kini memakai *field*-field pada *struct*
`Config`.

Sekarang kode kita menyampaikan dengan lebih jelas bahwa `query` dan
`file_path` saling berkaitan dan tujuan mereka adalah mengonfigurasi cara
kerja program. Kode mana pun yang memakai nilai-nilai ini tahu bahwa
nilai-nilai itu dapat ditemukan di instance `config`, pada *field*-field yang
dinamai sesuai tujuannya.

#### Membuat Konstruktor untuk `Config`

Sejauh ini, kita telah mengekstrak logika yang bertanggung jawab atas parsing
argumen baris perintah dari `main` dan menaruhnya di fungsi `parse_config`.
Hal ini membantu kita melihat bahwa nilai `query` dan `file_path` saling
berkaitan, dan hubungan itu seharusnya disampaikan di dalam kode kita. Kita
kemudian menambahkan *struct* `Config` untuk menamai tujuan bersama dari
`query` dan `file_path`, serta agar nama-nama nilai itu dapat dikembalikan
sebagai nama *field* *struct* dari fungsi `parse_config`.

Jadi, sekarang karena tujuan fungsi `parse_config` adalah membuat sebuah
instance `Config`, kita dapat mengubah `parse_config` dari fungsi biasa
menjadi sebuah fungsi bernama `new` yang terasosiasi dengan *struct* `Config`.
Perubahan ini akan membuat kode lebih idiomatis. Kita dapat membuat instance
type-type di pustaka standar, seperti `String`, dengan memanggil `String::new`.
Demikian pula, dengan mengubah `parse_config` menjadi fungsi `new` yang
terasosiasi dengan `Config`, kita akan dapat membuat instance `Config` dengan
memanggil `Config::new`. Listing 12-7 menunjukkan perubahan yang perlu kita
buat.

<Listing number="12-7" file-name="src/main.rs" caption="Mengubah `parse_config` menjadi `Config::new`">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

Kita telah memperbarui `main`, dari yang semula memanggil `parse_config`
menjadi memanggil `Config::new`. Kita telah mengubah nama `parse_config`
menjadi `new` dan memindahkannya ke dalam sebuah blok `impl`, yang
mengasosiasikan fungsi `new` dengan `Config`. Coba kompilasi lagi kode ini
untuk memastikan ia bekerja.

### Memperbaiki Penanganan Error

Sekarang kita akan memperbaiki penanganan error kita. Ingat bahwa mencoba
mengakses nilai-nilai di dalam vector `args` pada indeks 1 atau indeks 2 akan
menyebabkan program panic jika vector itu memuat kurang dari tiga item. Coba
jalankan program ini tanpa argumen apa pun; hasilnya akan tampak seperti ini:

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

Baris `index out of bounds: the len is 1 but the index is 1` adalah pesan
error yang ditujukan untuk pemrogram. Pesan itu tidak akan membantu pengguna
akhir kita memahami apa yang seharusnya mereka lakukan. Mari kita perbaiki
sekarang.

#### Memperbaiki Pesan Error

Di Listing 12-8, kita menambahkan sebuah pemeriksaan di fungsi `new` yang akan
memverifikasi bahwa *slice* itu cukup panjang sebelum mengakses indeks 1 dan
indeks 2. Jika *slice* itu tidak cukup panjang, program akan panic dan
menampilkan pesan error yang lebih baik.

<Listing number="12-8" file-name="src/main.rs" caption="Menambahkan pemeriksaan jumlah argumen">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

Kode ini mirip dengan [fungsi `Guess::new` yang kita tulis di Listing
9-13][ch9-custom-types]<!-- ignore -->, tempat kita memanggil `panic!` ketika
argumen `value` berada di luar rentang nilai yang valid. Alih-alih memeriksa
rentang nilai di sini, kita memeriksa bahwa panjang `args` setidaknya `3`, dan
sisa fungsi dapat beroperasi dengan asumsi bahwa kondisi ini telah terpenuhi.
Jika `args` memuat kurang dari tiga item, kondisi ini akan bernilai `true`,
dan kita memanggil makro `panic!` untuk segera mengakhiri program.

Dengan beberapa baris kode tambahan di `new` ini, mari kita jalankan lagi
program tanpa argumen apa pun untuk melihat seperti apa errornya sekarang:

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

Output ini lebih baik: Sekarang kita memiliki pesan error yang masuk akal.
Namun, kita juga memiliki informasi tambahan yang tidak ingin kita berikan
kepada pengguna. Mungkin teknik yang kita pakai di Listing 9-13 bukanlah yang
terbaik untuk dipakai di sini: Pemanggilan `panic!` lebih cocok untuk masalah
pemrograman daripada masalah pemakaian, [seperti yang dibahas di Bab
9][ch9-error-guidelines]<!-- ignore -->. Sebagai gantinya, kita akan memakai
teknik lain yang Anda pelajari di Bab 9—[mengembalikan `Result`][ch9-result]<!--
ignore --> yang menunjukkan keberhasilan ataupun error.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### Mengembalikan `Result` Alih-alih Memanggil `panic!`

Sebagai gantinya, kita dapat mengembalikan sebuah nilai `Result` yang akan
memuat instance `Config` pada kasus keberhasilan dan akan menjelaskan
masalahnya pada kasus error. Kita juga akan mengubah nama fungsinya dari `new`
menjadi `build` karena banyak pemrogram mengharapkan fungsi `new` tidak pernah
gagal. Ketika `Config::build` berkomunikasi dengan `main`, kita dapat memakai
type `Result` untuk memberi sinyal bahwa ada masalah. Kemudian, kita dapat
mengubah `main` untuk mengubah sebuah *variant* (varian) `Err` menjadi error
yang lebih praktis bagi pengguna kita, tanpa teks pelingkup tentang
`thread 'main'` dan `RUST_BACKTRACE` yang disebabkan oleh pemanggilan
`panic!`.

Listing 12-9 menunjukkan perubahan yang perlu kita buat pada return value
fungsi yang kini kita sebut `Config::build`, serta badan fungsi yang diperlukan
untuk mengembalikan sebuah `Result`. Perhatikan bahwa kode ini tidak akan
terkompilasi sampai kita memperbarui `main` juga, yang akan kita lakukan di
listing berikutnya.

<Listing number="12-9" file-name="src/main.rs" caption="Mengembalikan `Result` dari `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

Fungsi `build` kita mengembalikan sebuah `Result` dengan instance `Config`
pada kasus keberhasilan dan sebuah *string literal* pada kasus error.
Nilai-nilai error kita akan selalu berupa *string literal* yang memiliki
*lifetime* (masa hidup) `'static`.

Kita telah membuat dua perubahan di badan fungsi: Alih-alih memanggil
`panic!` ketika pengguna tidak meneruskan cukup argumen, kini kita
mengembalikan nilai `Err`, dan kita telah membungkus return value `Config`
di dalam `Ok`. Perubahan-perubahan ini membuat fungsi itu menyesuaikan diri
dengan type *signature* barunya.

Mengembalikan nilai `Err` dari `Config::build` memungkinkan fungsi `main`
menangani nilai `Result` yang dikembalikan dari fungsi `build` dan keluar dari
proses dengan lebih bersih pada kasus error.

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### Memanggil `Config::build` dan Menangani Error

Untuk menangani kasus error dan mencetak pesan yang ramah pengguna, kita perlu
memperbarui `main` untuk menangani `Result` yang dikembalikan oleh
`Config::build`, seperti yang ditunjukkan di Listing 12-10. Kita juga akan
mengambil alih tanggung jawab mengeluarkan alat baris perintah ini dengan kode
error bukan nol dari `panic!`, lalu mengimplementasikannya secara manual.
Status keluar bukan nol adalah sebuah konvensi untuk memberi sinyal kepada
proses yang memanggil program kita bahwa program itu keluar dalam keadaan
error.

<Listing number="12-10" file-name="src/main.rs" caption="Keluar dengan kode error jika pembuatan `Config` gagal">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

Di listing ini, kita telah memakai sebuah method yang belum kita bahas secara
mendetail: `unwrap_or_else`, yang didefinisikan pada `Result<T, E>` oleh
pustaka standar. Memakai `unwrap_or_else` memungkinkan kita mendefinisikan
penanganan error khusus yang bukan `panic!`. Jika `Result`-nya berupa nilai
`Ok`, perilaku method ini mirip dengan `unwrap`: Ia mengembalikan nilai di
dalamnya yang sedang dibungkus oleh `Ok`. Akan tetapi, jika nilainya berupa
nilai `Err`, method ini memanggil kode di dalam *closure*, yaitu sebuah fungsi
anonim yang kita definisikan dan teruskan sebagai argumen ke `unwrap_or_else`.
Kita akan membahas *closure* secara lebih mendetail di [Bab 13][ch13]<!--
ignore -->. Untuk saat ini, Anda hanya perlu tahu bahwa `unwrap_or_else` akan
meneruskan nilai di dalam `Err`—dalam kasus ini string statis `"not enough
arguments"` yang kita tambahkan di Listing 12-9—ke *closure* kita melalui
argumen `err` yang muncul di antara garis-garis vertikal itu. Kode di dalam
*closure* itu kemudian dapat memakai nilai `err` saat dijalankan.

Kita telah menambahkan baris `use` baru untuk membawa `process` dari pustaka
standar ke dalam *scope*. Kode di dalam *closure* yang akan dijalankan pada
kasus error hanya terdiri dari dua baris: Kita mencetak nilai `err`, lalu
memanggil `process::exit`. Fungsi `process::exit` akan menghentikan program
dengan segera dan mengembalikan angka yang diteruskan sebagai kode status
keluar. Ini mirip dengan penanganan berbasis `panic!` yang kita pakai di
Listing 12-8, tetapi kini kita tidak lagi mendapat semua output tambahan
itu. Mari kita coba:

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

Hebat! Output ini jauh lebih ramah bagi pengguna kita.

<!-- Old headings. Do not remove or links may break. -->

<a id="extracting-logic-from-the-main-function"></a>

### Mengekstrak Logika dari `main`

Setelah selesai melakukan refactoring pada parsing konfigurasi, mari kita
beralih ke logika programnya. Seperti yang kita nyatakan di [“Memisahkan
Tanggung Jawab dalam Proyek Binary”](#separation-of-concerns-for-binary-projects)<!--
ignore -->, kita akan mengekstrak sebuah fungsi bernama `run` yang akan memuat
semua logika yang kini berada di fungsi `main` dan tidak terlibat dalam
menyiapkan konfigurasi atau menangani error. Setelah selesai, fungsi `main`
akan menjadi ringkas dan mudah diverifikasi hanya dengan membacanya, dan kita
akan dapat menulis pengujian untuk semua logika lainnya.

Listing 12-11 menunjukkan perbaikan kecil dan bertahap berupa ekstraksi fungsi
`run`.

<Listing number="12-11" file-name="src/main.rs" caption="Mengekstrak fungsi `run` yang memuat sisa logika program">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</Listing>

Fungsi `run` kini memuat semua logika yang tersisa dari `main`, dimulai dari
membaca file. Fungsi `run` menerima instance `Config` sebagai argumen.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-errors-from-the-run-function"></a>

#### Mengembalikan Error dari `run`

Dengan sisa logika program yang telah dipisahkan ke dalam fungsi `run`, kita
dapat memperbaiki penanganan errornya, seperti yang kita lakukan pada
`Config::build` di Listing 12-9. Alih-alih membiarkan program panic dengan
memanggil `expect`, fungsi `run` akan mengembalikan `Result<T, E>` ketika ada
yang tidak beres. Ini akan memungkinkan kita untuk lebih mengonsolidasikan
logika penanganan error ke dalam `main` dengan cara yang ramah pengguna.
Listing 12-12 menunjukkan perubahan yang perlu kita buat pada *signature* dan
badan `run`.

<Listing number="12-12" file-name="src/main.rs" caption="Mengubah fungsi `run` agar mengembalikan `Result`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

Di sini kita telah membuat tiga perubahan penting. Pertama, kita mengubah type
kembalian fungsi `run` menjadi `Result<(), Box<dyn Error>>`. Sebelumnya fungsi
ini mengembalikan type *unit*, `()`, dan kita mempertahankannya sebagai nilai
yang dikembalikan pada kasus `Ok`.

Untuk type errornya, kita memakai *trait object* `Box<dyn Error>` (dan kita
membawa `std::error::Error` ke dalam *scope* dengan statement `use` di bagian
atas). Kita akan membahas *trait object* di [Bab 18][ch18]<!-- ignore -->.
Untuk saat ini, cukup ketahui bahwa `Box<dyn Error>` berarti fungsi ini akan
mengembalikan sebuah type yang mengimplementasikan *trait* `Error`, tetapi
kita tidak perlu menentukan type tertentu apa return valuenya. Ini memberi
kita fleksibilitas untuk mengembalikan nilai-nilai error yang mungkin berbeda
typenya pada kasus-kasus error yang berbeda. *Keyword* (kata kunci) `dyn`
adalah singkatan dari _dynamic_.

Kedua, kita telah menghapus pemanggilan `expect` demi operator `?`, seperti
yang kita bicarakan di [Bab 9][ch9-question-mark]<!-- ignore -->. Alih-alih
melakukan `panic!` saat ada error, `?` akan mengembalikan nilai error tersebut
dari fungsi saat ini untuk ditangani oleh pemanggilnya.

Ketiga, fungsi `run` kini mengembalikan nilai `Ok` pada kasus keberhasilan.
Kita telah mendeklarasikan type keberhasilan fungsi `run` sebagai `()` di
*signature*nya, yang berarti kita perlu membungkus nilai type *unit* itu di
dalam nilai `Ok`. Sintaks `Ok(())` ini mungkin tampak agak aneh pada awalnya.
Tetapi memakai `()` seperti ini adalah cara idiomatis untuk menunjukkan bahwa
kita memanggil `run` hanya demi efek sampingnya; fungsi itu tidak
mengembalikan nilai yang kita perlukan.

Ketika Anda menjalankan kode ini, ia akan terkompilasi tetapi akan menampilkan
sebuah peringatan:

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

Rust memberi tahu kita bahwa kode kita mengabaikan nilai `Result` tersebut,
dan nilai `Result` itu mungkin menandakan terjadinya error. Tetapi kita tidak
memeriksa apakah ada error atau tidak, dan *compiler* (kompilator)
mengingatkan kita bahwa kita mungkin bermaksud menaruh kode penanganan error
di sini! Mari kita perbaiki masalah itu sekarang.

#### Menangani Error yang Dikembalikan dari `run` di dalam `main`

Kita akan memeriksa error dan menanganinya memakai teknik yang mirip dengan
yang kita pakai pada `Config::build` di Listing 12-10, tetapi dengan sedikit
perbedaan:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

Kita memakai `if let` alih-alih `unwrap_or_else` untuk memeriksa apakah `run`
mengembalikan nilai `Err`, dan memanggil `process::exit(1)` jika demikian.
Fungsi `run` tidak mengembalikan nilai yang ingin kita `unwrap` sebagaimana
`Config::build` mengembalikan instance `Config`. Karena `run` mengembalikan
`()` pada kasus keberhasilan, kita hanya peduli pada pendeteksian error, jadi
kita tidak memerlukan `unwrap_or_else` untuk mengembalikan nilai hasil unwrap,
yang hanya akan berupa `()`.

Badan dari fungsi `if let` dan `unwrap_or_else` itu sama di kedua kasus: Kita
mencetak errornya lalu keluar.

### Memisahkan Kode ke dalam Crate Library

Proyek `minigrep` kita sejauh ini tampak bagus! Sekarang kita akan memisahkan
file _src/main.rs_ dan menaruh sebagian kode ke dalam file _src/lib.rs_.
Dengan begitu, kita dapat menguji kodenya dan memiliki file _src/main.rs_
dengan tanggung jawab yang lebih sedikit.

Kita akan mendefinisikan kode yang bertanggung jawab atas pencarian teks di
_src/lib.rs_ alih-alih di _src/main.rs_, yang akan memungkinkan kita (atau
siapa pun yang memakai pustaka `minigrep` kita) memanggil fungsi pencarian itu
dari lebih banyak konteks daripada sekadar binary `minigrep` kita.

Pertama, mari kita definisikan *signature* fungsi `search` di _src/lib.rs_
seperti yang ditunjukkan di Listing 12-13, dengan badan yang memanggil makro
`unimplemented!`. Kita akan menjelaskan *signature* ini secara lebih
mendetail saat mengisi implementasinya.

<Listing number="12-13" file-name="src/lib.rs" caption="Mendefinisikan fungsi `search` di *src/lib.rs*">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs}}
```

</Listing>

Kita telah memakai kata kunci `pub` pada definisi fungsi tersebut untuk
menandai `search` sebagai bagian dari API publik *crate* library kita. Sekarang
kita memiliki sebuah *crate* library yang dapat kita pakai dari *crate* binary
kita dan yang dapat kita uji!

Sekarang kita perlu membawa kode yang didefinisikan di _src/lib.rs_ ke dalam
*scope* *crate* binary di _src/main.rs_ dan memanggilnya, seperti yang
ditunjukkan di Listing 12-14.

<Listing number="12-14" file-name="src/main.rs" caption="Memakai fungsi `search` dari crate library `minigrep` di *src/main.rs*">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

Kita menambahkan baris `use minigrep::search` untuk membawa fungsi `search`
dari *crate* library ke dalam *scope* *crate* binary. Kemudian, di dalam fungsi
`run`, alih-alih mencetak isi file, kita memanggil fungsi `search` dan
meneruskan nilai `config.query` dan `contents` sebagai argumen. Lalu, `run`
akan memakai sebuah loop `for` untuk mencetak setiap baris yang
dikembalikan dari `search` yang cocok dengan kueri. Ini juga saat yang tepat
untuk menghapus pemanggilan `println!` di fungsi `main` yang menampilkan
kueri dan *path* file, sehingga program kita hanya mencetak hasil pencarian
(jika tidak ada error yang terjadi).

Perhatikan bahwa fungsi pencarian akan mengumpulkan semua hasil ke dalam
sebuah vector yang dikembalikannya sebelum pencetakan apa pun terjadi.
Implementasi ini bisa lambat menampilkan hasil saat mencari di file-file
besar, karena hasilnya tidak dicetak begitu ditemukan; kita akan membahas
salah satu cara yang mungkin untuk memperbaikinya dengan memakai *iterator*
di Bab 13.

Fiuh! Itu tadi pekerjaan yang banyak, tetapi kita telah menyiapkan diri untuk
keberhasilan di masa depan. Sekarang menangani error menjadi jauh lebih mudah,
dan kita telah membuat kodenya lebih modular. Hampir semua pekerjaan kita
mulai sekarang akan dilakukan di _src/lib.rs_.

Mari kita manfaatkan modularitas yang baru diperoleh ini dengan melakukan
sesuatu yang akan sulit dilakukan dengan kode lama tetapi mudah dengan kode
baru: Kita akan menulis beberapa pengujian!

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator
