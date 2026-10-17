<!-- Old headings. Do not remove or links may break. -->

<a id="treating-smart-pointers-like-regular-references-with-the-deref-trait"></a>
<a id="treating-smart-pointers-like-regular-references-with-deref"></a>

<a id="treating-smart-pointers-like-regular-references"></a>
## Memperlakukan Smart Pointer Seperti Reference Biasa

Mengimplementasikan *trait* `Deref` memungkinkan Anda menyesuaikan perilaku
_operator dereferensi_ `*` (jangan tertukar dengan operator perkalian atau
operator glob). Dengan mengimplementasikan `Deref` sedemikian rupa sehingga
*smart pointer* dapat diperlakukan seperti *reference* biasa, Anda dapat menulis
kode yang beroperasi pada *reference* dan memakai kode itu dengan *smart pointer*
juga.

Mari kita lihat dulu cara kerja operator dereferensi dengan *reference* biasa.
Lalu, kita akan mencoba mendefinisikan type buatan sendiri yang berperilaku
seperti `Box<T>` dan melihat mengapa operator dereferensi tidak bekerja
seperti *reference* pada type yang baru kita definisikan itu. Kita akan
mengeksplorasi bagaimana mengimplementasikan *trait* `Deref` memungkinkan smart
*pointer* bekerja dengan cara yang serupa dengan *reference*. Kemudian, kita akan
melihat fitur *deref coercion* dari Rust dan bagaimana fitur itu memungkinkan
kita bekerja dengan *reference* ataupun *smart pointer*.

<!-- Old headings. Do not remove or links may break. -->

<a id="following-the-pointer-to-the-value-with-the-dereference-operator"></a>
<a id="following-the-pointer-to-the-value"></a>

### Mengikuti Reference Menuju Nilai

*Reference* biasa adalah salah satu jenis *pointer*, dan salah satu cara
memandang *pointer* adalah sebagai anak panah menuju nilai yang tersimpan di
tempat lain. Di Listing 15-6, kita membuat *reference* ke nilai `i32`, lalu
memakai operator dereferensi untuk mengikuti *reference* itu menuju nilainya.

<Listing number="15-6" file-name="src/main.rs" caption="Memakai operator dereferensi untuk mengikuti sebuah reference menuju nilai `i32`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-06/src/main.rs}}
```

</Listing>

Variable `x` menampung nilai `i32`, yaitu `5`. Kita menetapkan `y` sama
dengan *reference* ke `x`. Kita dapat menegaskan bahwa `x` sama dengan `5`.
Namun, jika kita ingin membuat asersi tentang nilai di dalam `y`, kita harus
memakai `*y` untuk mengikuti *reference* itu menuju nilai yang ditunjuknya
(karena itu disebut _dereference_ atau dereferensi) supaya *compiler* dapat
membandingkan nilai sebenarnya. Begitu kita melakukan dereferensi pada `y`,
kita memiliki akses ke nilai integer yang ditunjuk `y` untuk kita bandingkan
dengan `5`.

Jika kita mencoba menulis `assert_eq!(5, y);` saja, kita akan mendapat error
kompilasi ini:

```console
{{#include ../listings/ch15-smart-pointers/output-only-01-comparing-to-reference/output.txt}}
```

Membandingkan angka dengan *reference* ke angka tidak diizinkan karena keduanya
typed berbeda. Kita harus memakai operator dereferensi untuk mengikuti
*reference* itu menuju nilai yang ditunjuknya.

### Memakai `Box<T>` Seperti Reference

Kita dapat menulis ulang kode di Listing 15-6 untuk memakai `Box<T>` alih-alih
*reference*; operator dereferensi yang dipakai pada `Box<T>` di Listing 15-7
berfungsi dengan cara yang sama seperti operator dereferensi yang dipakai pada
*reference* di Listing 15-6.

<Listing number="15-7" file-name="src/main.rs" caption="Memakai operator dereferensi pada `Box<i32>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-07/src/main.rs}}
```

</Listing>

Perbedaan utama antara Listing 15-7 dan Listing 15-6 adalah bahwa di sini kita
menetapkan `y` sebagai instance dari sebuah *box* yang menunjuk ke copy nilai
`x`, alih-alih *reference* yang menunjuk ke nilai `x`. Pada asersi terakhir,
kita dapat memakai operator dereferensi untuk mengikuti *pointer* *box* dengan
cara yang sama seperti yang kita lakukan ketika `y` adalah *reference*.
Selanjutnya, kita akan mengeksplorasi apa yang istimewa dari `Box<T>` yang
memungkinkan kita memakai operator dereferensi, dengan mendefinisikan type *box*
kita sendiri.

### Mendefinisikan Smart Pointer Kita Sendiri

Mari kita bangun type *wrapper* (pembungkus) yang serupa dengan type `Box<T>`
yang disediakan standard library untuk merasakan bagaimana type *smart pointer*
berperilaku berbeda dari *reference* secara default. Kemudian, kita akan melihat
cara menambahkan kemampuan untuk memakai operator dereferensi.

> Catatan: Ada satu perbedaan besar antara type `MyBox<T>` yang akan kita
> bangun dan `Box<T>` yang asli: Versi kita tidak akan menyimpan datanya di
> *heap*. Kita memfokuskan contoh ini pada `Deref`, jadi di mana data itu
> sebenarnya disimpan kurang penting daripada perilaku yang menyerupai *pointer*.

Type `Box<T>` pada akhirnya didefinisikan sebagai *tuple struct* dengan satu
elemen, jadi Listing 15-8 mendefinisikan type `MyBox<T>` dengan cara yang
sama. Kita juga akan mendefinisikan fungsi `new` untuk mencocokkan fungsi
`new` yang didefinisikan pada `Box<T>`.

<Listing number="15-8" file-name="src/main.rs" caption="Mendefinisikan type `MyBox<T>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-08/src/main.rs:here}}
```

</Listing>

Kita mendefinisikan *struct* bernama `MyBox` dan mendeklarasikan parameter
generik `T` karena kita ingin type kita menampung nilai typed apa pun. Type
`MyBox` adalah *tuple struct* dengan satu elemen typed `T`. Fungsi
`MyBox::new` menerima satu parameter typed `T` dan mengembalikan instance
`MyBox` yang menampung nilai yang diberikan.

Mari kita coba menambahkan fungsi `main` di Listing 15-7 ke Listing 15-8 dan
mengubahnya untuk memakai type `MyBox<T>` yang telah kita definisikan alih-alih
`Box<T>`. Kode di Listing 15-9 tidak akan terkompilasi, karena Rust tidak tahu
cara melakukan dereferensi pada `MyBox`.

<Listing number="15-9" file-name="src/main.rs" caption="Mencoba memakai `MyBox<T>` dengan cara yang sama seperti kita memakai reference dan `Box<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-09/src/main.rs:here}}
```

</Listing>

Berikut error kompilasi yang dihasilkan:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-09/output.txt}}
```

Type `MyBox<T>` kita tidak bisa dilakukan dereferensi karena kita belum
mengimplementasikan kemampuan itu pada type kita. Untuk mengaktifkan
dereferensi dengan operator `*`, kita mengimplementasikan *trait* `Deref`.

<!-- Old headings. Do not remove or links may break. -->

<a id="treating-a-type-like-a-reference-by-implementing-the-deref-trait"></a>

### Mengimplementasikan Trait `Deref`

Seperti yang dibahas di [“Mengimplementasikan *Trait* pada Suatu
Type”][impl-trait]<!-- ignore --> di Bab 10, untuk mengimplementasikan sebuah
*trait* kita perlu menyediakan implementasi untuk method-method yang diwajibkan
*trait* itu. *Trait* `Deref`, yang disediakan standard library, mewajibkan kita
mengimplementasikan satu method bernama `deref` yang meminjam `self` dan
mengembalikan *reference* ke data bagian dalam. Listing 15-10 memuat
implementasi `Deref` untuk ditambahkan ke definisi `MyBox<T>`.

<Listing number="15-10" file-name="src/main.rs" caption="Mengimplementasikan `Deref` pada `MyBox<T>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-10/src/main.rs:here}}
```

</Listing>

Sintaks `type Target = T;` mendefinisikan *associated type* (tipe asosiasi)
untuk dipakai oleh *trait* `Deref`. *Associated type* adalah cara yang sedikit
berbeda dalam mendeklarasikan parameter generik, tetapi Anda tidak perlu
mengkhawatirkannya untuk sekarang; kita akan membahasnya lebih jauh di Bab 20.

Kita mengisi badan method `deref` dengan `&self.0` sehingga `deref`
mengembalikan *reference* ke nilai yang ingin kita akses dengan operator `*`;
ingat kembali dari [“Membuat Type Berbeda dengan Tuple Struct”][tuple-structs]<!--
ignore --> di Bab 5 bahwa `.0` mengakses nilai pertama dalam *tuple struct*.
Fungsi `main` di Listing 15-9 yang memanggil `*` pada nilai `MyBox<T>` sekarang
terkompilasi, dan asersinya lulus!

Tanpa *trait* `Deref`, *compiler* hanya bisa melakukan dereferensi pada
*reference* `&`. Method `deref` memberi *compiler* kemampuan untuk mengambil
nilai typed apa pun yang mengimplementasikan `Deref` dan memanggil method
`deref` untuk mendapatkan *reference* yang ia tahu cara melakukan dereferensi
padanya.

Ketika kita menulis `*y` di Listing 15-9, di belakang layar Rust sebenarnya
menjalankan kode ini:

```rust,ignore
*(y.deref())
```

Rust menggantikan operator `*` dengan panggilan ke method `deref` lalu sebuah
dereferensi biasa sehingga kita tidak perlu memikirkan apakah kita perlu
memanggil method `deref` atau tidak. Fitur Rust ini memungkinkan kita menulis
kode yang berfungsi identik entah kita memiliki *reference* biasa ataupun type
yang mengimplementasikan `Deref`.

Alasan method `deref` mengembalikan *reference* ke nilai, dan dereferensi biasa
di luar tanda kurung pada `*(y.deref())` tetap diperlukan, berkaitan dengan
sistem *ownership*. Jika method `deref` mengembalikan nilainya langsung
alih-alih *reference* ke nilai itu, nilai itu akan dipindahkan keluar dari
`self`. Kita tidak ingin mengambil *ownership* nilai bagian dalam `MyBox<T>`
dalam kasus ini maupun di sebagian besar kasus ketika kita memakai operator
dereferensi.

Perhatikan bahwa operator `*` digantikan dengan panggilan ke method `deref`
lalu panggilan ke operator `*` tepat satu kali, setiap kali kita memakai `*`
di kode kita. Karena substitusi operator `*` itu tidak berulang tanpa batas,
kita berakhir dengan data typed `i32`, yang cocok dengan `5` di `assert_eq!`
pada Listing 15-9.

<!-- Old headings. Do not remove or links may break. -->

<a id="implicit-deref-coercions-with-functions-and-methods"></a>
<a id="using-deref-coercions-in-functions-and-methods"></a>

### Menggunakan Deref Coercions di dalam Fungsi dan Method

_Deref coercion_ mengubah sebuah *reference* ke type yang mengimplementasikan
*trait* `Deref` menjadi *reference* ke type lain. Sebagai contoh, *deref coercion*
dapat mengubah `&String` menjadi `&str` karena `String` mengimplementasikan
*trait* `Deref` sedemikian rupa sehingga ia mengembalikan `&str`. *Deref coercion*
adalah kemudahan yang dilakukan Rust pada argumen fungsi dan method, dan ia
hanya bekerja pada type yang mengimplementasikan *trait* `Deref`. *Deref coercion*
terjadi secara otomatis ketika kita memberikan *reference* ke nilai typed
tertentu sebagai argumen ke fungsi atau method yang tidak cocok dengan type
parameter dalam definisi fungsi atau method itu. Serangkaian panggilan ke
method `deref` mengubah type yang kita berikan menjadi type yang dibutuhkan
parameter.

*Deref coercion* ditambahkan ke Rust supaya programmer yang menulis panggilan
fungsi dan method tidak perlu menambahkan sebanyak itu *reference* dan
dereferensi eksplisit dengan `&` dan `*`. Fitur *deref coercion* juga
memungkinkan kita menulis lebih banyak kode yang dapat bekerja untuk *reference*
ataupun *smart pointer*.

Untuk melihat *deref coercion* beraksi, mari kita pakai type `MyBox<T>` yang
kita definisikan di Listing 15-8 serta implementasi `Deref` yang kita
tambahkan di Listing 15-10. Listing 15-11 menunjukkan definisi fungsi yang
memiliki parameter string *slice*.

<Listing number="15-11" file-name="src/main.rs" caption="Fungsi `hello` yang memiliki parameter `name` typed `&str`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-11/src/main.rs:here}}
```

</Listing>

Kita dapat memanggil fungsi `hello` dengan string *slice* sebagai argumen,
misalnya `hello("Rust");`. *Deref coercion* memungkinkan pemanggilan `hello`
dengan *reference* ke nilai typed `MyBox<String>`, seperti ditunjukkan pada
Listing 15-12.

<Listing number="15-12" file-name="src/main.rs" caption="Memanggil `hello` dengan reference ke nilai `MyBox<String>`, yang bekerja karena deref coercion">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-12/src/main.rs:here}}
```

</Listing>

Di sini kita memanggil fungsi `hello` dengan argumen `&m`, yang merupakan
*reference* ke nilai `MyBox<String>`. Karena kita mengimplementasikan *trait*
`Deref` pada `MyBox<T>` di Listing 15-10, Rust dapat mengubah `&MyBox<String>`
menjadi `&String` dengan memanggil `deref`. Pustaka standar menyediakan
implementasi `Deref` pada `String` yang mengembalikan string *slice*, dan ini
ada di dokumentasi API untuk `Deref`. Rust memanggil `deref` lagi untuk
mengubah `&String` menjadi `&str`, yang cocok dengan definisi fungsi `hello`.

Jika Rust tidak mengimplementasikan *deref coercion*, kita harus menulis kode di
Listing 15-13 alih-alih kode di Listing 15-12 untuk memanggil `hello` dengan
nilai typed `&MyBox<String>`.

<Listing number="15-13" file-name="src/main.rs" caption="Kode yang harus kita tulis jika Rust tidak memiliki deref coercion">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-13/src/main.rs:here}}
```

</Listing>

`(*m)` melakukan dereferensi pada `MyBox<String>` menjadi `String`. Lalu, `&`
dan `[..]` mengambil string *slice* dari `String` itu yang sama dengan seluruh
string untuk mencocokkan *signature* `hello`. Kode tanpa *deref coercion* ini
lebih sulit dibaca, ditulis, dan dipahami karena semua simbol yang terlibat.
*Deref coercion* memungkinkan Rust menangani konversi-konversi itu untuk kita
secara otomatis.

Ketika *trait* `Deref` didefinisikan untuk type-type yang terlibat, Rust akan
menganalisis type-type itu dan memakai `Deref::deref` sebanyak yang
diperlukan untuk mendapatkan *reference* yang cocok dengan type parameter.
Jumlah pemanggilan `Deref::deref` yang perlu disisipkan diselesaikan pada
waktu kompilasi, jadi tidak ada denda runtime karena memanfaatkan deref
coercion!

<!-- Old headings. Do not remove or links may break. -->

<a id="how-deref-coercion-interacts-with-mutability"></a>

### Menangani Deref Coercion dengan Mutable References

Serupa dengan cara Anda memakai *trait* `Deref` untuk mengganti operator `*`
pada *immutable* *reference*, Anda dapat memakai *trait* `DerefMut` untuk mengganti
operator `*` pada *mutable* *reference*.

Rust melakukan *deref coercion* ketika ia menemukan type dan implementasi *trait*
dalam tiga kasus:

1. Dari `&T` ke `&U` ketika `T: Deref<Target=U>`
2. Dari `&mut T` ke `&mut U` ketika `T: DerefMut<Target=U>`
3. Dari `&mut T` ke `&U` ketika `T: Deref<Target=U>`

Dua kasus pertama sama, kecuali bahwa kasus kedua mengimplementasikan
mutabilitas. Kasus pertama menyatakan bahwa jika Anda memiliki `&T`, dan `T`
mengimplementasikan `Deref` ke suatu type `U`, Anda dapat memperoleh `&U`
secara transparan. Kasus kedua menyatakan bahwa *deref coercion* yang sama
terjadi untuk *mutable* *reference*.

Kasus ketiga lebih rumit: Rust juga akan mengoersi *mutable* *reference* menjadi
*immutable*. Tetapi kebalikannya _tidak_ mungkin: *Immutable* *reference* tidak akan
pernah dikoersi menjadi *mutable* *reference*. Karena aturan *borrowing*, jika Anda
memiliki *mutable* *reference*, *mutable* *reference* itu harus menjadi satu-satunya
*reference* ke data itu (jika tidak, program tidak akan terkompilasi). Mengubah
satu *mutable* *reference* menjadi satu *immutable* *reference* tidak akan pernah
melanggar aturan *borrowing*. Mengubah *immutable* *reference* menjadi *mutable*
*reference* akan menuntut bahwa *immutable* *reference* awal itu adalah satu-satunya
*immutable* *reference* ke data itu, tetapi aturan *borrowing* tidak menjamin hal
itu. Karena itu, Rust tidak bisa berasumsi bahwa mengubah *immutable* *reference*
menjadi *mutable* *reference* itu mungkin.

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
