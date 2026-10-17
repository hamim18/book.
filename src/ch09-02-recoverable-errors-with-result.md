## Error yang Dapat Dipulihkan dengan `Result`

Sebagian besar error tidak cukup serius untuk mengharuskan program berhenti
sepenuhnya. Terkadang, ketika sebuah fungsi gagal, ada alasan yang dapat Anda
tafsirkan dan tanggapi dengan mudah. Misalnya, jika Anda mencoba membuka
sebuah file dan operasi itu gagal karena filenya tidak ada, Anda mungkin
ingin membuat file itu alih-alih menghentikan proses.

Ingat dari [“Menangani Kemungkinan Kegagalan dengan
`Result`”][handle_failure]<!-- ignore --> di Bab 2 bahwa enum `Result`
didefinisikan memiliki dua variant, `Ok` dan `Err`, sebagai berikut:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` dan `E` adalah type parameter generik: kita akan membahas *generics*
(generic type) lebih detail di Bab 10. Yang perlu Anda ketahui saat ini
adalah bahwa `T` merepresentasikan type nilai yang akan dikembalikan pada
kasus sukses di dalam variant `Ok`, dan `E` merepresentasikan type error
yang akan dikembalikan pada kasus gagal di dalam variant `Err`. Karena
`Result` memiliki type parameter generik ini, kita dapat memakai type
`Result` dan fungsi-fungsi yang didefinisikan padanya di banyak situasi
berbeda ketika nilai sukses dan nilai error yang ingin kita kembalikan
mungkin berbeda.

Mari kita panggil sebuah fungsi yang mengembalikan nilai `Result` karena
fungsi itu bisa gagal. Di Listing 9-3, kita mencoba membuka sebuah file.

<Listing number="9-3" file-name="src/main.rs" caption="Membuka sebuah file">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

Type kembalian `File::open` adalah `Result<T, E>`. Parameter generik `T`
telah diisi oleh implementasi `File::open` dengan type nilai sukses,
`std::fs::File`, yang merupakan handle file. Type `E` yang dipakai pada
nilai error adalah `std::io::Error`. Type kembalian ini berarti pemanggilan
`File::open` mungkin berhasil dan mengembalikan handle file yang dapat kita
baca atau tulis. Pemanggilan fungsinya juga mungkin gagal: misalnya, file
mungkin tidak ada, atau kita mungkin tidak memiliki izin untuk mengakses
file itu. Fungsi `File::open` perlu punya cara memberi tahu kita apakah ia
berhasil atau gagal dan sekaligus memberi kita handle file atau informasi
error. Informasi ini persis seperti yang disampaikan *enum* `Result`.

Pada kasus ketika `File::open` berhasil, nilai di variable
`greeting_file_result` akan berupa instance `Ok` yang berisi handle file.
Pada kasus ketika ia gagal, nilai di `greeting_file_result` akan berupa
instance `Err` yang berisi lebih banyak informasi tentang jenis error yang
terjadi.

Kita perlu menambahkan kode ke Listing 9-3 untuk mengambil tindakan yang
berbeda bergantung pada nilai yang dikembalikan `File::open`. Listing 9-4
menunjukkan satu cara menangani `Result` memakai tool dasar, expression
`match` yang kita bahas di Bab 6.

<Listing number="9-4" file-name="src/main.rs" caption="Memakai expression `match` untuk menangani variant `Result` yang mungkin dikembalikan">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

Perhatikan bahwa, seperti *enum* `Option`, *enum* `Result` dan variant-nya telah
dibawa ke dalam *scope* oleh *prelude*, jadi kita tidak perlu menuliskan
`Result::` sebelum variant `Ok` dan `Err` di arm-arm `match`.

Ketika hasilnya `Ok`, kode ini akan mengembalikan nilai `file` bagian dalam
dari variant `Ok`, lalu kita menetapkan nilai handle file itu ke variable
`greeting_file`. Setelah `match`, kita dapat memakai handle file untuk
membaca atau menulis.

Arm `match` yang lain menangani kasus ketika kita mendapat nilai `Err` dari
`File::open`. Dalam contoh ini, kita memilih untuk memanggil *macro* `panic!`.
Jika tidak ada file bernama _hello.txt_ di direktori kita saat ini dan kita
menjalankan kode ini, kita akan melihat output berikut dari *macro* `panic!`:

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

Seperti biasa, output ini memberi tahu kita dengan tepat apa yang salah.

### Mencocokkan Error yang Berbeda

Kode di Listing 9-4 akan `panic!` apa pun alasan `File::open` gagal. Namun,
kita ingin mengambil tindakan yang berbeda untuk alasan kegagalan yang
berbeda. Jika `File::open` gagal karena filenya tidak ada, kita ingin
membuat file itu dan mengembalikan handle ke file baru. Jika `File::open`
gagal karena alasan lain—misalnya, karena kita tidak memiliki izin membuka
file—kita tetap ingin kodenya `panic!` dengan cara yang sama seperti di
Listing 9-4. Untuk ini, kita menambahkan expression `match` bagian dalam,
seperti yang ditunjukkan di Listing 9-5.

<Listing number="9-5" file-name="src/main.rs" caption="Menangani berbagai jenis error dengan berbagai cara">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

Type nilai yang dikembalikan `File::open` di dalam variant `Err` adalah
`io::Error`, yaitu sebuah *struct* yang disediakan standard library. *Struct* ini
memiliki method `kind`, yang dapat kita panggil untuk mendapatkan nilai
`io::ErrorKind`. *Enum* `io::ErrorKind` disediakan standard library dan
memiliki variant-variant yang merepresentasikan berbagai jenis error yang
mungkin dihasilkan dari operasi `io`. Variant yang ingin kita pakai adalah
`ErrorKind::NotFound`, yang mengindikasikan bahwa file yang kita coba buka
belum ada. Jadi, kita mencocokkan `greeting_file_result`, tetapi kita juga
memiliki match bagian dalam pada `error.kind()`.

Kondisi yang ingin kita periksa di match bagian dalam adalah apakah nilai
yang dikembalikan `error.kind()` adalah variant `NotFound` dari *enum*
`ErrorKind`. Jika ya, kita mencoba membuat file dengan `File::create`.
Namun, karena `File::create` juga bisa gagal, kita membutuhkan arm kedua di
expression `match` bagian dalam. Ketika file tidak dapat dibuat, pesan error
yang berbeda dicetak. Arm kedua dari `match` bagian luar tetap sama, jadi
program panic pada error apa pun selain error file tidak ditemukan.

> #### Alternatif untuk Memakai `match` dengan `Result<T, E>`
>
> Banyak sekali `match`-nya! Expression `match` sangat berguna tetapi juga
> sangat primitif. Di Bab 13, Anda akan mempelajari *closure*, yang dipakai
> bersama banyak method yang didefinisikan pada `Result<T, E>`.
> Method-method ini dapat lebih ringkas daripada memakai `match` ketika
> menangani nilai `Result<T, E>` di kode Anda.
>
> Misalnya, ini cara lain untuk menulis logika yang sama seperti yang
> ditunjukkan di Listing 9-5, kali ini memakai *closure* dan method
> `unwrap_or_else`:
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> Meskipun kode ini berperilaku sama dengan Listing 9-5, ia tidak memuat
> expression `match` apa pun dan lebih bersih untuk dibaca. Kembalilah ke
> contoh ini setelah Anda membaca Bab 13 dan carilah method
> `unwrap_or_else` di dokumentasi standard library. Banyak lagi method
> semacam ini yang dapat merapikan expression `match` bersarang yang besar
> ketika Anda berurusan dengan error.

<!-- Old headings. Do not remove or links may break. -->

<a id="shortcuts-for-panic-on-error-unwrap-and-expect"></a>

#### Pintasan untuk Panic saat Error

Memakai `match` cukup berhasil, tetapi bisa sedikit bertele-tele dan tidak
selalu mengomunikasikan maksud dengan baik. Type `Result<T, E>` memiliki
banyak method bantu yang didefinisikan padanya untuk melakukan berbagai
tugas yang lebih spesifik. Method `unwrap` adalah method pintasan yang
diimplementasikan persis seperti expression `match` yang kita tulis di Listing
9-4. Jika nilai `Result` adalah variant `Ok`, `unwrap` akan mengembalikan
nilai di dalam `Ok`. Jika `Result` adalah variant `Err`, `unwrap` akan
memanggil macro `panic!` untuk kita. Berikut contoh `unwrap` yang sedang
beraksi:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

Jika kita menjalankan kode ini tanpa file _hello.txt_, kita akan melihat
pesan error dari pemanggilan `panic!` yang dilakukan method `unwrap`:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Demikian pula, method `expect` juga memungkinkan kita memilih pesan error
`panic!`. Memakai `expect` alih-alih `unwrap` dan memberikan pesan error
yang baik dapat menyampaikan maksud Anda dan mempermudah pelacakan sumber
panic. Sintaks `expect` terlihat seperti ini:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

Kita memakai `expect` dengan cara yang sama seperti `unwrap`: untuk
mengembalikan handle file atau memanggil *macro* `panic!`. Pesan error yang
dipakai `expect` dalam pemanggilannya ke `panic!` adalah parameter yang kita
berikan ke `expect`, bukan pesan `panic!` default yang dipakai `unwrap`.
Inilah tampilannya:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Dalam kode berkualitas produksi, sebagian besar Rustacean memilih `expect`
alih-alih `unwrap` dan memberikan lebih banyak konteks tentang mengapa
operasi itu diharapkan selalu berhasil. Dengan begitu, jika asumsi Anda
ternyata salah, Anda memiliki lebih banyak informasi untuk dipakai dalam
men-debug.

### Meneruskan Error

Ketika implementasi sebuah fungsi memanggil sesuatu yang mungkin gagal,
alih-alih menangani errornya di dalam fungsi itu sendiri, Anda dapat
mengembalikan errornya ke kode pemanggil supaya kode itu dapat memutuskan
apa yang harus dilakukan. Ini dikenal sebagai *propagating* (meneruskan)
error dan memberi lebih banyak kendali kepada kode pemanggil, yang mungkin
memiliki lebih banyak informasi atau logika yang menentukan bagaimana error
itu harus ditangani daripada yang Anda miliki dalam konteks kode Anda.

Misalnya, Listing 9-6 menunjukkan fungsi yang membaca nama pengguna dari
sebuah file. Jika file tidak ada atau tidak dapat dibaca, fungsi ini akan
mengembalikan error-error itu ke kode yang memanggil fungsi tersebut.

<Listing number="9-6" file-name="src/main.rs" caption="Sebuah fungsi yang mengembalikan error ke kode pemanggil memakai `match`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

Fungsi ini dapat ditulis dengan cara yang jauh lebih pendek, tetapi kita
akan memulai dengan mengerjakan banyak bagiannya secara manual untuk
mengeksplorasi penanganan error; pada akhirnya, kita akan menunjukkan cara
yang lebih pendek. Mari kita lihat return type fungsinya terlebih dahulu:
`Result<String, io::Error>`. Ini berarti fungsi ini mengembalikan nilai
typed `Result<T, E>`, dengan parameter generik `T` diisi type konkret
`String` dan generic type `E` diisi type konkret `io::Error`.

Jika fungsi ini berhasil tanpa masalah apa pun, kode yang memanggil fungsi
ini akan menerima nilai `Ok` yang memegang sebuah `String`—`username` yang
dibaca fungsi ini dari file. Jika fungsi ini menemui masalah apa pun, kode
pemanggil akan menerima nilai `Err` yang memegang instance `io::Error` yang
berisi lebih banyak informasi tentang masalah apa yang terjadi. Kita
memilih `io::Error` sebagai return type fungsi ini karena kebetulan itu
adalah type nilai error yang dikembalikan dari kedua operasi yang kita
panggil di badan fungsi ini yang mungkin gagal: fungsi `File::open` dan
method `read_to_string`.

Badan fungsi dimulai dengan memanggil fungsi `File::open`. Lalu, kita
menangani nilai `Result` dengan `match` yang mirip dengan `match` di Listing
9-4. Jika `File::open` berhasil, handle file di variable pattern `file` menjadi
nilai di variable *mutable* `username_file` dan fungsinya berlanjut. Pada
kasus `Err`, alih-alih memanggil `panic!`, kita memakai *keyword* `return`
untuk keluar lebih awal dari fungsi sepenuhnya dan meneruskan nilai error
dari `File::open`, yang kini berada di variable pattern `e`, kembali ke kode
pemanggil sebagai nilai error fungsi ini.

Jadi, jika kita memiliki handle file di `username_file`, fungsi kemudian
membuat `String` baru di variable `username` dan memanggil method
`read_to_string` pada handle file di `username_file` untuk membaca isi file
ke dalam `username`. Method `read_to_string` juga mengembalikan `Result`
karena ia mungkin gagal, meskipun `File::open` berhasil. Jadi, kita
membutuhkan `match` lain untuk menangani `Result` itu: jika `read_to_string`
berhasil, fungsi kita pun berhasil, dan kita mengembalikan nama pengguna
dari file yang kini berada di `username` yang dibungkus dalam `Ok`. Jika
`read_to_string` gagal, kita mengembalikan nilai errornya dengan cara yang
sama seperti kita mengembalikan nilai error di `match` yang menangani nilai
kembalian `File::open`. Namun, kita tidak perlu menulis `return` secara
eksplisit, karena ini adalah expression terakhir di fungsi.

Kode yang memanggil kode ini kemudian akan menangani penerimaan nilai `Ok`
yang berisi nama pengguna atau nilai `Err` yang berisi `io::Error`. Terserah
kode pemanggil untuk memutuskan apa yang harus dilakukan dengan nilai-nilai
itu. Jika kode pemanggil mendapat nilai `Err`, ia dapat memanggil `panic!`
dan membuat program crash, memakai nama pengguna default, atau mencari nama
pengguna dari tempat selain file, misalnya. Kita tidak memiliki cukup
informasi tentang apa yang sebenarnya ingin dilakukan kode pemanggil, jadi
kita meneruskan semua informasi keberhasilan atau error ke atas untuk
ditangani dengan tepat.

Pattern meneruskan error ini begitu umum di Rust sehingga Rust menyediakan
operator tanda tanya `?` untuk mempermudahnya.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-shortcut-for-propagating-errors-the--operator"></a>

#### Pintasan Operator `?`

Listing 9-7 menunjukkan implementasi `read_username_from_file` yang
fungsionalitasnya sama dengan Listing 9-6, tetapi implementasi ini memakai
operator `?`.

<Listing number="9-7" file-name="src/main.rs" caption="Sebuah fungsi yang mengembalikan error ke kode pemanggil memakai operator `?`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

`?` yang ditempatkan setelah nilai `Result` didefinisikan untuk bekerja
dengan cara yang hampir sama dengan expression `match` yang kita definisikan
untuk menangani nilai `Result` di Listing 9-6. Jika nilai `Result` adalah
`Ok`, nilai di dalam `Ok` akan dikembalikan dari expression ini, dan program
akan berlanjut. Jika nilainya `Err`, `Err` akan dikembalikan dari seluruh
fungsi seolah-olah kita memakai *keyword* `return`, sehingga nilai
errornya diteruskan ke kode pemanggil.

Ada perbedaan antara yang dilakukan expression `match` dari Listing 9-6 dan
yang dilakukan operator `?`: nilai error yang dipanggilkan operator `?`
padanya melewati fungsi `from`, yang didefinisikan di *trait* `From` di
standard library, yang dipakai untuk mengonversi nilai dari satu type ke type
lain. Ketika operator `?` memanggil fungsi `from`, type error yang diterima
dikonversi menjadi type error yang didefinisikan di return type fungsi
saat ini. Ini berguna ketika sebuah fungsi mengembalikan satu type error
untuk merepresentasikan semua cara fungsi itu mungkin gagal, bahkan jika
bagian-bagiannya mungkin gagal karena banyak alasan berbeda.

Misalnya, kita dapat mengubah fungsi `read_username_from_file` di Listing
9-7 agar mengembalikan type error kustom bernama `OurError` yang kita
definisikan. Jika kita juga mendefinisikan `impl From<io::Error> for
OurError` untuk mengonstruksi instance `OurError` dari `io::Error`, maka
pemanggilan operator `?` di badan `read_username_from_file` akan memanggil
`from` dan mengonversi type errornya tanpa perlu menambahkan kode lagi ke
fungsi.

Dalam konteks Listing 9-7, `?` di akhir pemanggilan `File::open` akan
mengembalikan nilai di dalam `Ok` ke variable `username_file`. Jika terjadi
error, operator `?` akan keluar lebih awal dari seluruh fungsi dan
memberikan nilai `Err` apa pun kepada kode pemanggil. Hal yang sama berlaku
untuk `?` di akhir pemanggilan `read_to_string`.

Operator `?` menghilangkan banyak boilerplate dan membuat implementasi
fungsi ini lebih sederhana. Kita bahkan dapat mempersingkat kode ini lebih
jauh dengan merangkai pemanggilan method tepat setelah `?`, seperti yang
ditunjukkan di Listing 9-8.

<Listing number="9-8" file-name="src/main.rs" caption="Merangkai pemanggilan method setelah operator `?`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

Kita telah memindahkan pembuatan `String` baru di `username` ke awal
fungsi; bagian itu tidak berubah. Alih-alih membuat variable
`username_file`, kita merangkai pemanggilan `read_to_string` langsung pada
hasil `File::open("hello.txt")?`. Kita masih memiliki `?` di akhir
pemanggilan `read_to_string`, dan kita tetap mengembalikan nilai `Ok` yang
berisi `username` ketika `File::open` dan `read_to_string` sama-sama
berhasil alih-alih mengembalikan error. Fungsionalitasnya lagi-lagi sama
dengan Listing 9-6 dan Listing 9-7; ini hanya cara penulisan yang berbeda
dan lebih ergonomis.

Listing 9-9 menunjukkan cara membuat ini lebih pendek lagi memakai
`fs::read_to_string`.

<Listing number="9-9" file-name="src/main.rs" caption="Memakai `fs::read_to_string` alih-alih membuka lalu membaca file">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

Membaca file ke dalam string adalah operasi yang cukup umum, jadi pustaka
standar menyediakan fungsi `fs::read_to_string` yang praktis yang membuka
file, membuat `String` baru, membaca isi file, menaruh isinya ke `String`
itu, dan mengembalikannya. Tentu saja, memakai `fs::read_to_string` tidak
memberi kita kesempatan untuk menjelaskan semua penanganan errornya, jadi
kita mengerjakannya dengan cara yang lebih panjang terlebih dahulu.

<!-- Old headings. Do not remove or links may break. -->

<a id="where-the--operator-can-be-used"></a>

#### Tempat Memakai Operator `?`

Operator `?` hanya dapat dipakai di fungsi yang return typenya kompatibel
dengan nilai tempat `?` dipakai. Ini karena operator `?` didefinisikan untuk
melakukan return dini atas sebuah nilai keluar dari fungsi, dengan cara yang
sama seperti expression `match` yang kita definisikan di Listing 9-6. Di
Listing 9-6, `match` memakai nilai `Result`, dan arm return dini
mengembalikan nilai `Err(e)`. Type kembalian fungsi harus berupa `Result`
supaya kompatibel dengan `return` ini.

Di Listing 9-10, mari kita lihat error yang akan kita dapatkan jika kita
memakai operator `?` di fungsi `main` dengan return type yang tidak
kompatibel dengan type nilai tempat kita memakai `?`.

<Listing number="9-10" file-name="src/main.rs" caption="Mencoba memakai `?` di fungsi `main` yang mengembalikan `()` tidak akan terkompilasi.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

Kode ini membuka file, yang mungkin gagal. Operator `?` mengikuti nilai
`Result` yang dikembalikan `File::open`, tetapi fungsi `main` ini memiliki
return type `()`, bukan `Result`. Ketika kita mengompilasi kode ini, kita
mendapat pesan error berikut:

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

Error ini menunjukkan bahwa kita hanya diizinkan memakai operator `?` di
fungsi yang mengembalikan `Result`, `Option`, atau type lain yang
mengimplementasikan `FromResidual`.

Untuk memperbaiki errornya, Anda punya dua pilihan. Pilihan pertama adalah
mengubah return type fungsi Anda agar kompatibel dengan nilai tempat Anda
memakai operator `?` selama tidak ada pembatasan yang mencegahnya. Pilihan
lainnya adalah memakai `match` atau salah satu method `Result<T, E>` untuk
menangani `Result<T, E>` dengan cara apa pun yang sesuai.

Pesan errornya juga menyebutkan bahwa `?` dapat dipakai dengan nilai
`Option<T>` juga. Seperti halnya memakai `?` pada `Result`, Anda hanya dapat
memakai `?` pada `Option` di fungsi yang mengembalikan `Option`. Perilaku
operator `?` ketika dipanggil pada `Option<T>` mirip dengan perilakunya
ketika dipanggil pada `Result<T, E>`: jika nilainya `None`, `None` akan
dikembalikan lebih awal dari fungsi pada titik itu. Jika nilainya `Some`,
nilai di dalam `Some` adalah nilai hasil expression, dan fungsi berlanjut.
Listing 9-11 memiliki contoh fungsi yang menemukan karakter terakhir dari
baris pertama di teks yang diberikan.

<Listing number="9-11" caption="Memakai operator `?` pada nilai `Option<T>`">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

Fungsi ini mengembalikan `Option<char>` karena mungkin ada karakter di
sana, tetapi mungkin juga tidak ada. Kode ini menerima argumen string *slice*
`text` dan memanggil method `lines` padanya, yang mengembalikan *iterator*
atas baris-baris di string. Karena fungsi ini ingin memeriksa baris
pertama, ia memanggil `next` pada *iterator* untuk mendapatkan nilai pertama
dari *iterator*. Jika `text` adalah string kosong, pemanggilan `next` ini akan
mengembalikan `None`, dalam hal ini kita memakai `?` untuk berhenti dan
mengembalikan `None` dari `last_char_of_first_line`. Jika `text` bukan
string kosong, `next` akan mengembalikan nilai `Some` yang berisi string
*slice* dari baris pertama di `text`.

`?` mengekstrak string *slice*-nya, dan kita dapat memanggil `chars` pada
string *slice* itu untuk mendapatkan *iterator* karakter-karakternya. Kita
tertarik pada karakter terakhir di baris pertama ini, jadi kita memanggil
`last` untuk mengembalikan item terakhir di *iterator*. Ini adalah `Option`
karena mungkin saja baris pertamanya adalah string kosong; misalnya, jika
`text` dimulai dengan baris kosong tetapi memiliki karakter di baris lain,
seperti pada `"\nhi"`. Namun, jika ada karakter terakhir di baris pertama,
ia akan dikembalikan di dalam variant `Some`. Operator `?` di tengah memberi
kita cara yang ringkas untuk mengekspresikan logika ini, yang memungkinkan
kita mengimplementasikan fungsi dalam satu baris. Jika kita tidak dapat
memakai operator `?` pada `Option`, kita harus mengimplementasikan logika
ini memakai lebih banyak pemanggilan method atau expression `match`.

Perhatikan bahwa Anda dapat memakai operator `?` pada `Result` di fungsi
yang mengembalikan `Result`, dan Anda dapat memakai operator `?` pada
`Option` di fungsi yang mengembalikan `Option`, tetapi Anda tidak dapat
mencampur keduanya. Operator `?` tidak akan mengonversi `Result` menjadi
`Option` atau sebaliknya secara otomatis; dalam kasus-kasus itu, Anda dapat
memakai method seperti method `ok` pada `Result` atau method `ok_or` pada
`Option` untuk melakukan konversi secara eksplisit.

Sejauh ini, semua fungsi `main` yang kita pakai mengembalikan `()`. Fungsi
`main` istimewa karena ia adalah titik masuk dan titik keluar dari program
yang dapat dieksekusi, dan ada pembatasan return typenya agar program
berperilaku seperti yang diharapkan.

Untungnya, `main` juga dapat mengembalikan `Result<(), E>`. Listing 9-12
berisi kode dari Listing 9-10, tetapi kita telah mengubah return type
`main` menjadi `Result<(), Box<dyn Error>>` dan menambahkan return value
`Ok(())` di akhir. Kode ini kini akan terkompilasi.

<Listing number="9-12" file-name="src/main.rs" caption="Mengubah `main` agar mengembalikan `Result<(), E>` memungkinkan pemakaian operator `?` pada nilai `Result`.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

Type `Box<dyn Error>` adalah *trait object* (objek *trait*), yang akan kita
bicarakan di [“Memakai *Trait Object* untuk Mengabstraksi Perilaku
Bersama”][*trait*-objects]<!-- ignore --> di Bab 18. Untuk saat ini, Anda
dapat membaca `Box<dyn Error>` sebagai “error jenis apa pun.” Memakai `?`
pada nilai `Result` di fungsi `main` dengan type error `Box<dyn Error>`
diizinkan karena ini memungkinkan nilai `Err` apa pun dikembalikan lebih
awal. Meskipun badan fungsi `main` ini hanya akan mengembalikan error
typed `std::io::Error`, dengan menyebutkan `Box<dyn Error>`, *signature*
ini akan tetap benar bahkan jika lebih banyak kode yang mengembalikan error
lain ditambahkan ke badan `main`.

Ketika fungsi `main` mengembalikan `Result<(), E>`, program yang dapat
dieksekusi akan keluar dengan nilai `0` jika `main` mengembalikan `Ok(())`
dan akan keluar dengan nilai bukan nol jika `main` mengembalikan nilai
`Err`. Program yang dapat dieksekusi yang ditulis dalam C mengembalikan
bilangan bulat ketika keluar: program yang keluar dengan sukses
mengembalikan bilangan bulat `0`, dan program yang mengalami error
mengembalikan bilangan bulat selain `0`. Rust juga mengembalikan bilangan
bulat dari program yang dapat dieksekusi agar kompatibel dengan konvensi
ini.

Fungsi `main` boleh mengembalikan type apa pun yang mengimplementasikan
[trait `std::process::Termination`][termination]<!-- ignore -->, yang berisi
fungsi `report` yang mengembalikan `ExitCode`. Lihat dokumentasi pustaka
standar untuk informasi lebih lanjut tentang mengimplementasikan *trait*
`Termination` untuk type Anda sendiri.

Setelah kita membahas detail pemanggilan `panic!` atau pengembalian
`Result`, mari kita kembali ke topik tentang cara memutuskan mana yang tepat
dipakai pada kasus mana.

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: ../std/process/trait.Termination.html
