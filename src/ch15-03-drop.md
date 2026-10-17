## Menjalankan Kode pada Saat Pembersihan dengan Trait `Drop`

*Trait* kedua yang penting bagi pattern *smart pointer* adalah `Drop`, yang
memungkinkan Anda menyesuaikan apa yang terjadi ketika sebuah nilai akan
keluar dari *scope*. Anda dapat menyediakan implementasi untuk *trait* `Drop` pada
type apa pun, dan kode itu dapat dipakai untuk melepaskan sumber daya seperti file
atau koneksi jaringan.

Kita memperkenalkan `Drop` dalam konteks *smart pointer* karena fungsionalitas
*trait* `Drop` hampir selalu dipakai ketika mengimplementasikan *smart pointer*.
Sebagai contoh, ketika sebuah `Box<T>` dibebaskan, ia akan mendealokasikan
ruang di *heap* yang ditunjuk *box* itu.

Di beberapa bahasa, untuk beberapa type, programmer harus memanggil kode untuk
membebaskan memori atau sumber daya setiap kali mereka selesai memakai instance
type-type itu. Contohnya antara lain handle file, soket, dan kunci. Jika
programmer lupa, sistem bisa kelebihan beban dan crash. Di Rust, Anda dapat
menentukan bahwa potongan kode tertentu dijalankan setiap kali sebuah nilai
keluar dari *scope*, dan *compiler* akan menyisipkan kode ini secara otomatis.
Akibatnya, Anda tidak perlu berhati-hati menempatkan kode pembersihan di
seluruh bagian program yang telah selesai memakai instance type tertentu—Anda
tetap tidak akan membocorkan resource!

Anda menentukan kode yang dijalankan ketika sebuah nilai keluar dari *scope*
dengan mengimplementasikan *trait* `Drop`. *Trait* `Drop` mewajibkan Anda
mengimplementasikan satu method bernama `drop` yang menerima *mutable* *reference*
ke `self`. Untuk melihat kapan Rust memanggil `drop`, untuk sekarang mari kita
implementasikan `drop` dengan statement `println!`.

Listing 15-14 menunjukkan *struct* `CustomSmartPointer` yang satu-satunya
fungsionalitas khususnya adalah mencetak `Dropping CustomSmartPointer!` ketika
instance-nya keluar dari *scope*, untuk menunjukkan kapan Rust menjalankan
method `drop`.

<Listing number="15-14" file-name="src/main.rs" caption="Struct `CustomSmartPointer` yang mengimplementasikan trait `Drop` tempat kita akan meletakkan kode pembersihan">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-14/src/main.rs}}
```

</Listing>

*Trait* `Drop` disertakan di prelude, jadi kita tidak perlu membawanya ke dalam
*scope*. Kita mengimplementasikan *trait* `Drop` pada `CustomSmartPointer` dan
menyediakan implementasi untuk method `drop` yang memanggil `println!`. Badan
method `drop` adalah tempat Anda meletakkan logika apa pun yang ingin Anda
jalankan ketika instance type Anda keluar dari *scope*. Kita mencetak beberapa
teks di sini untuk menunjukkan secara visual kapan Rust akan memanggil `drop`.

Di `main`, kita membuat dua instance `CustomSmartPointer`, lalu mencetak
`CustomSmartPointers created`. Di akhir `main`, instance `CustomSmartPointer`
kita akan keluar dari *scope*, dan Rust akan memanggil kode yang kita letakkan
di method `drop`, mencetak pesan terakhir kita. Perhatikan bahwa kita tidak
perlu memanggil method `drop` secara eksplisit.

Ketika kita menjalankan program ini, kita akan melihat output berikut:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-14/output.txt}}
```

Rust otomatis memanggil `drop` untuk kita ketika instance kita keluar dari
*scope*, menjalankan kode yang kita tentukan. Variable dibebaskan dalam urutan
terbalik dari pembuatannya, jadi `d` dibebaskan sebelum `c`. Tujuan contoh ini
adalah memberi Anda panduan visual tentang cara kerja method `drop`; biasanya
Anda akan menentukan kode pembersihan yang perlu dijalankan type Anda alih-alih
pesan cetak.

<!-- Old headings. Do not remove or links may break. -->

<a id="dropping-a-value-early-with-std-mem-drop"></a>

Sayangnya, mematikan fungsionalitas otomatis `drop` tidaklah mudah. Mematikan
`drop` biasanya tidak perlu; inti dari *trait* `Drop` justru adalah bahwa ia
ditangani secara otomatis. Namun, sesekali Anda mungkin ingin membersihkan
nilai lebih awal. Salah satu contohnya adalah ketika memakai *smart pointer*
yang mengelola kunci: Anda mungkin ingin memaksa method `drop` yang melepaskan
kunci itu berjalan supaya kode lain di *scope* yang sama dapat memperoleh kunci
itu. Rust tidak mengizinkan Anda memanggil method `drop` dari *trait* `Drop`
secara manual; sebagai gantinya, Anda harus memanggil fungsi `std::mem::drop`
yang disediakan standard library jika Anda ingin memaksa sebuah nilai dibebaskan
sebelum akhir *scope*-nya.

Mencoba memanggil method `drop` dari *trait* `Drop` secara manual dengan
mengubah fungsi `main` dari Listing 15-14 tidak akan berhasil, seperti
ditunjukkan pada Listing 15-15.

<Listing number="15-15" file-name="src/main.rs" caption="Mencoba memanggil method `drop` dari trait `Drop` secara manual untuk membersihkan lebih awal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-15/src/main.rs:here}}
```

</Listing>

Ketika kita mencoba mengompilasi kode ini, kita akan mendapat error berikut:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-15/output.txt}}
```

Pesan error ini menyatakan bahwa kita tidak diizinkan memanggil `drop` secara
eksplisit. Pesan error itu memakai istilah _destructor_ (destruktor), yang
merupakan istilah pemrograman umum untuk fungsi yang membersihkan sebuah
instance. Sebuah _destructor_ serupa dengan _constructor_ (konstruktor), yang
membuat instance. Fungsi `drop` di Rust adalah salah satu destructor khusus.

Rust tidak mengizinkan kita memanggil `drop` secara eksplisit, karena Rust
tetap akan otomatis memanggil `drop` pada nilai itu di akhir `main`. Ini akan
menyebabkan error *double free* karena Rust akan mencoba membersihkan nilai yang
sama dua kali.

Kita tidak bisa mematikan penyisipan otomatis `drop` ketika sebuah nilai
keluar dari *scope*, dan kita tidak bisa memanggil method `drop` secara
eksplisit. Jadi, jika kita perlu memaksa sebuah nilai dibersihkan lebih awal,
kita memakai fungsi `std::mem::drop`.

Fungsi `std::mem::drop` berbeda dari method `drop` di *trait* `Drop`. Kita
memanggilnya dengan memberikan nilai yang ingin kita paksa untuk dibebaskan
sebagai argumen. Fungsi itu ada di prelude, jadi kita dapat mengubah `main` di
Listing 15-15 untuk memanggil fungsi `drop`, seperti ditunjukkan pada Listing
15-16.

<Listing number="15-16" file-name="src/main.rs" caption="Memanggil `std::mem::drop` untuk secara eksplisit membebaskan sebuah nilai sebelum ia keluar dari scope">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-16/src/main.rs:here}}
```

</Listing>

Menjalankan kode ini akan mencetak hal berikut:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-16/output.txt}}
```

Teks ``Dropping CustomSmartPointer with data `some data`!`` dicetak di antara
teks `CustomSmartPointer created` dan `CustomSmartPointer dropped before the
end of main`, menunjukkan bahwa kode method `drop` dipanggil untuk membebaskan
`c` pada titik itu.

Anda dapat memakai kode yang ditentukan dalam implementasi *trait* `Drop` dengan
berbagai cara untuk membuat pembersihan menjadi nyaman dan aman: Sebagai
contoh, Anda bisa memakainya untuk membuat *memory allocator* Anda sendiri!
Dengan *trait* `Drop` dan sistem *ownership* Rust, Anda tidak perlu ingat untuk
membersihkan, karena Rust melakukannya secara otomatis.

Anda juga tidak perlu mengkhawatirkan masalah akibat ketidaksengajaan
membersihkan nilai yang masih dipakai: Sistem *ownership* yang memastikan
*reference* selalu valid juga memastikan bahwa `drop` hanya dipanggil sekali
ketika nilai itu tidak lagi dipakai.

Sekarang kita telah memeriksa `Box<T>` dan sebagian karakteristik smart
*pointer*, mari kita lihat beberapa *smart pointer* lain yang didefinisikan di
standard library.
