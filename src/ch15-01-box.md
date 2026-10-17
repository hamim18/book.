## Memakai `Box<T>` untuk Menunjuk ke Data di Heap

*Smart pointer* yang paling sederhana adalah _box_, yang typenya ditulis
`Box<T>`. _Box_ memungkinkan Anda menyimpan data di *heap* alih-alih di *stack*.
Yang tersisa di *stack* adalah *pointer* ke data di *heap* itu. Baca kembali Bab 4
untuk mengulas perbedaan antara *stack* dan *heap*.

*Box* tidak memiliki overhead performa, selain menyimpan datanya di *heap*
alih-alih di *stack*. Namun, *box* juga tidak memiliki banyak kemampuan tambahan.
Anda paling sering akan memakainya dalam situasi-situasi berikut:

- Ketika Anda memiliki type yang ukurannya tidak bisa diketahui pada waktu
  kompilasi, dan Anda ingin memakai nilai typed itu dalam konteks yang
  menuntut ukuran yang pasti
- Ketika Anda memiliki data dalam jumlah besar, dan Anda ingin memindahkan
  *ownership* tetapi memastikan data itu tidak akan disalin ketika Anda
  melakukannya
- Ketika Anda ingin memiliki sebuah nilai, dan Anda hanya peduli bahwa nilai
  itu typed yang mengimplementasikan *trait* tertentu alih-alih typed
  spesifik tertentu

Kita akan menunjukkan situasi pertama di [“Mengaktifkan Type Rekursif dengan
Boxes”](#enabling-recursive-types-with-boxes)<!-- ignore -->. Pada kasus
kedua, memindahkan *ownership* data dalam jumlah besar bisa memakan waktu lama
karena data itu disalin bolak-balik di *stack*. Untuk meningkatkan performa
dalam situasi ini, kita dapat menyimpan data berjumlah besar itu di *heap* dalam
sebuah *box*. Dengan begitu, hanya data *pointer* yang berjumlah kecil yang
disalin bolak-balik di *stack*, sementara data yang dirujuknya tetap berada di
satu tempat di *heap*. Kasus ketiga dikenal sebagai _trait object_ (objek
*trait*), dan [“Memakai *Trait Object* untuk Mengabstraksi Perilaku
Bersama”][*trait*-objects]<!-- ignore --> di Bab 18 dikhususkan untuk topik itu.
Jadi, apa yang Anda pelajari di sini akan Anda terapkan lagi di seksi itu!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-store-data-on-the-heap"></a>

### Menyimpan Data di Heap

Sebelum membahas kasus penggunaan penyimpanan *heap* untuk `Box<T>`, kita akan
membahas sintaks dan cara berinteraksi dengan nilai yang disimpan di dalam
sebuah `Box<T>`.

Listing 15-1 menunjukkan cara memakai *box* untuk menyimpan nilai `i32` di *heap*.

<Listing number="15-1" file-name="src/main.rs" caption="Menyimpan nilai `i32` di heap menggunakan sebuah box">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-01/src/main.rs}}
```

</Listing>

Kita mendefinisikan variable `b` agar memiliki nilai sebuah `Box` yang
menunjuk ke nilai `5`, yang dialokasikan di *heap*. Program ini akan mencetak
`b = 5`; dalam kasus ini, kita dapat mengakses data di dalam *box* dengan cara
yang serupa seperti jika data itu berada di *stack*. Sama seperti nilai yang
dimiliki mana pun, ketika sebuah *box* keluar dari *scope*, seperti yang dialami
`b` di akhir `main`, *box* itu akan didealokasikan. Dealokasi terjadi untuk *box*
(disimpan di *stack*) sekaligus data yang ditunjuknya (disimpan di *heap*).

Meletakkan satu nilai saja di *heap* tidak terlalu berguna, jadi Anda tidak
akan sering memakai *box* sendirian dengan cara seperti ini. Menyimpan nilai
seperti satu `i32` di *stack*, tempat nilai itu disimpan secara default, lebih
tepat pada sebagian besar situasi. Mari kita lihat kasus di mana *box*
memungkinkan kita mendefinisikan type yang tidak boleh kita definisikan jika
kita tidak memiliki *box*.

<a id="enabling-recursive-types-with-boxes"></a>
### Mengaktifkan Type Rekursif dengan Boxes

Sebuah nilai typed _recursive type_ (type rekursif) dapat memiliki nilai
lain typed sama sebagai bagian dari dirinya sendiri. Type rekursif
menimbulkan masalah karena Rust perlu tahu pada waktu kompilasi berapa banyak
ruang yang ditempati sebuah type. Namun, penyarangan nilai-nilai typed
rekursif secara teoretis bisa berlanjut tanpa batas, jadi Rust tidak bisa tahu
berapa banyak ruang yang dibutuhkan nilai itu. Karena *box* memiliki ukuran yang
diketahui, kita dapat mengaktifkan type rekursif dengan menyisipkan sebuah *box*
di definisi type rekursif itu.

Sebagai contoh type rekursif, mari kita jelajahi *cons list*. Ini adalah type
data yang umum ditemukan di bahasa-bahasa pemrograman fungsional. Type cons
list yang akan kita definisikan ini sederhana, kecuali bagian rekursinya;
karena itu, konsep-konsep dalam contoh yang akan kita kerjakan akan berguna
kapan pun Anda menghadapi situasi yang lebih kompleks yang melibatkan type
rekursif.

<!-- Old headings. Do not remove or links may break. -->

<a id="more-information-about-the-cons-list"></a>

#### Memahami Cons List

_Cons list_ adalah struktur data yang berasal dari bahasa pemrograman Lisp dan
dialek-dialeknya, tersusun dari pasangan-pasangan bersarang, dan merupakan
versi Lisp dari *linked list* (senarai berantai). Namanya berasal dari fungsi
`cons` (singkatan dari _construct function_ atau fungsi pembangun) di Lisp
yang membangun sebuah pasangan baru dari dua argumennya. Dengan memanggil
`cons` pada pasangan yang terdiri atas sebuah nilai dan pasangan lain, kita
dapat membangun *cons list* yang tersusun dari pasangan-pasangan rekursif.

Sebagai contoh, berikut representasi pseudokode sebuah *cons list* yang memuat
list `1, 2, 3` dengan setiap pasangan di dalam tanda kurung:

```text
(1, (2, (3, Nil)))
```

Setiap item dalam *cons list* memuat dua elemen: nilai item saat ini dan item
berikutnya. Item terakhir dalam list hanya memuat nilai yang disebut `Nil`
tanpa item berikutnya. Sebuah *cons list* dihasilkan dengan memanggil fungsi
`cons` secara rekursif. Nama kanonis untuk menyatakan kasus dasar rekursi itu
adalah `Nil`. Perhatikan bahwa ini tidak sama dengan konsep “null” atau “nil”
yang dibahas di Bab 6, yang merupakan nilai yang tidak valid atau tidak ada.

*Cons list* bukanlah struktur data yang umum dipakai di Rust. Sebagian besar
waktu, ketika Anda memiliki list berisi item-item di Rust, `Vec<T>` adalah
pilihan yang lebih baik. Type data rekursif lain yang lebih kompleks _memang_
berguna dalam berbagai situasi, tetapi dengan memulai dari *cons list* di bab
ini, kita dapat mengeksplorasi bagaimana *box* memungkinkan kita mendefinisikan
data type rekursif tanpa banyak gangguan.

Listing 15-2 memuat definisi *enum* untuk sebuah *cons list*. Perhatikan bahwa
kode ini belum bisa dikompilasi, karena type `List` tidak memiliki ukuran yang
diketahui, yang akan kita tunjukkan.

<Listing number="15-2" file-name="src/main.rs" caption="Percobaan pertama mendefinisikan enum untuk merepresentasikan struktur data cons list berisi nilai `i32`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-02/src/main.rs:here}}
```

</Listing>

> Catatan: Kita mengimplementasikan *cons list* yang hanya menampung nilai
> `i32` demi keperluan contoh ini. Kita bisa saja mengimplementasikannya
> menggunakan *generics*, seperti yang kita bahas di Bab 10, untuk mendefinisikan
> type *cons list* yang dapat menyimpan nilai typed apa pun.

Memakai type `List` untuk menyimpan list `1, 2, 3` akan tampak seperti kode
di Listing 15-3.

<Listing number="15-3" file-name="src/main.rs" caption="Memakai enum `List` untuk menyimpan list `1, 2, 3`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-03/src/main.rs:here}}
```

</Listing>

Nilai `Cons` pertama menampung `1` dan nilai `List` lain. Nilai `List` ini
adalah nilai `Cons` lain yang menampung `2` dan nilai `List` lain. Nilai
`List` ini adalah satu lagi nilai `Cons` yang menampung `3` dan sebuah nilai
`List`, yang akhirnya berupa `Nil`, variant non-rekursif yang menandai akhir
list.

Jika kita mencoba mengompilasi kode di Listing 15-3, kita mendapat error yang
ditunjukkan pada Listing 15-4.

<Listing number="15-4" caption="Error yang kita dapat ketika mencoba mendefinisikan enum rekursif">

```console
{{#include ../listings/ch15-smart-pointers/listing-15-03/output.txt}}
```

</Listing>

Error itu menunjukkan bahwa type ini “memiliki ukuran tak terhingga.” Alasannya
adalah kita telah mendefinisikan `List` dengan sebuah variant yang rekursif:
Variant itu langsung menampung nilai lain dari dirinya sendiri. Akibatnya,
Rust tidak bisa memperhitungkan berapa banyak ruang yang dibutuhkannya untuk
menyimpan nilai `List`. Mari kita uraikan mengapa kita mendapat error ini.
Pertama, kita akan melihat cara Rust memutuskan berapa banyak ruang yang
dibutuhkannya untuk menyimpan nilai typed non-rekursif.

#### Menghitung Ukuran Type Non-Rekursif

Ingat kembali *enum* `Message` yang kita definisikan di Listing 6-2 ketika kita
membahas definisi *enum* di Bab 6:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

Untuk menentukan berapa banyak ruang yang dialokasikan bagi nilai `Message`,
Rust menelusuri setiap variant untuk melihat variant mana yang membutuhkan
ruang paling banyak. Rust melihat bahwa `Message::Quit` tidak membutuhkan
ruang, `Message::Move` membutuhkan ruang yang cukup untuk menyimpan dua nilai
`i32`, dan seterusnya. Karena hanya satu variant yang akan dipakai, ruang
paling banyak yang akan dibutuhkan nilai `Message` adalah ruang yang
dibutuhkan untuk menyimpan variant terbesarnya.

Bandingkan hal itu dengan yang terjadi ketika Rust mencoba menentukan berapa
banyak ruang yang dibutuhkan type rekursif seperti *enum* `List` di Listing
15-2. Kompilator mulai dengan melihat variant `Cons`, yang menampung sebuah
nilai typed `i32` dan sebuah nilai typed `List`. Karena itu, `Cons`
membutuhkan ruang sebesar ukuran sebuah `i32` ditambah ukuran sebuah `List`.
Untuk memperhitungkan berapa banyak memori yang dibutuhkan type `List`,
kompilator melihat variant-variantnya, dimulai dengan variant `Cons`. Variant
`Cons` menampung sebuah nilai typed `i32` dan sebuah nilai typed `List`,
dan proses ini berlanjut tanpa batas, seperti ditunjukkan pada Gambar 15-1.

<img alt="Cons list tak terhingga: sebuah persegi panjang berlabel 'Cons' yang terbagi menjadi dua persegi panjang lebih kecil. Persegi panjang kecil pertama memuat label 'i32', dan persegi panjang kecil kedua memuat label 'Cons' beserta versi lebih kecil dari persegi panjang 'Cons' luar. Persegi panjang 'Cons' terus memuat versi dirinya yang semakin kecil sampai persegi panjang terkecil yang masih cukup besar memuat simbol tak hingga, yang menunjukkan bahwa pengulangan ini berlangsung selamanya." src="img/trpl15-01.svg" class="center" style="width: 50%;" />

<span class="caption">Gambar 15-1: `List` tak terhingga yang terdiri atas
variant `Cons` yang tak terhingga</span>

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-get-a-recursive-type-with-a-known-size"></a>

#### Mendapatkan Type Rekursif dengan Ukuran yang Diketahui

Karena Rust tidak bisa memperhitungkan berapa banyak ruang yang dialokasikan
untuk type yang didefinisikan secara rekursif, kompilator memberikan error
dengan saran yang membantu berikut:

<!-- manual-regeneration
after doing automatic regeneration, look at listings/ch15-smart-pointers/listing-15-03/output.txt and copy the relevant line
-->

```text
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

Dalam saran ini, _indirection_ (indireksi) berarti alih-alih menyimpan nilai
secara langsung, kita harus mengubah struktur data itu untuk menyimpan nilai
secara tidak langsung dengan menyimpan *pointer* ke nilai itu.

Karena `Box<T>` adalah sebuah *pointer*, Rust selalu tahu berapa banyak ruang
yang dibutuhkan `Box<T>`: Ukuran *pointer* tidak berubah berdasarkan banyaknya
data yang ditunjuknya. Ini berarti kita dapat meletakkan `Box<T>` di dalam
variant `Cons` alih-alih nilai `List` lain secara langsung. `Box<T>` itu akan
menunjuk ke nilai `List` berikutnya yang akan berada di *heap* alih-alih di
dalam variant `Cons`. Secara konseptual, kita tetap memiliki list, yang dibuat
dari list yang menampung list lain, tetapi implementasi ini sekarang lebih
seperti menempatkan item-item bersebelahan alih-alih saling bertumpuk di
dalam satu sama lain.

Kita dapat mengubah definisi *enum* `List` di Listing 15-2 dan pemakaian `List`
di Listing 15-3 menjadi kode di Listing 15-5, yang akan terkompilasi.

<Listing number="15-5" file-name="src/main.rs" caption="Definisi `List` yang memakai `Box<T>` agar memiliki ukuran yang diketahui">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-05/src/main.rs}}
```

</Listing>

Variant `Cons` membutuhkan ukuran sebuah `i32` ditambah ruang untuk menyimpan
data *pointer* *box*. Variant `Nil` tidak menyimpan nilai, jadi ia membutuhkan
lebih sedikit ruang di *stack* daripada variant `Cons`. Sekarang kita tahu bahwa
nilai `List` mana pun akan menempati ukuran sebuah `i32` ditambah ukuran data
*pointer* *box*. Dengan memakai *box*, kita telah memutus rantai rekursif yang tak
terhingga, sehingga kompilator dapat memperhitungkan ukuran yang
dibutuhkannya untuk menyimpan nilai `List`. Gambar 15-2 menunjukkan seperti
apa variant `Cons` sekarang.

<img alt="Persegi panjang berlabel 'Cons' yang terbagi menjadi dua persegi panjang lebih kecil. Persegi panjang kecil pertama memuat label 'i32', dan persegi panjang kecil kedua memuat label 'Box' dengan satu persegi panjang di dalamnya yang memuat label 'usize', yang merepresentasikan ukuran terbatas pointer box." src="img/trpl15-02.svg" class="center" />

<span class="caption">Gambar 15-2: `List` yang ukurannya tidak tak terhingga,
karena `Cons` menampung sebuah `Box`</span>

*Box* hanya menyediakan indireksi dan alokasi *heap*; *box* tidak memiliki
kemampuan khusus lain, seperti yang akan kita lihat pada type *smart pointer*
lainnya. *Box* juga tidak memiliki overhead performa yang ditimbulkan oleh
kemampuan-kemampuan khusus itu, jadi *box* dapat berguna dalam kasus seperti
*cons list* di mana indireksi adalah satu-satunya fitur yang kita butuhkan.
Kita akan melihat lebih banyak kasus penggunaan *box* di Bab 18.

Type `Box<T>` adalah *smart pointer* karena ia mengimplementasikan *trait*
`Deref`, yang memungkinkan nilai `Box<T>` diperlakukan seperti *reference*.
Ketika sebuah nilai `Box<T>` keluar dari *scope*, data *heap* yang ditunjuk *box*
itu juga dibersihkan karena implementasi *trait* `Drop`. Kedua *trait* ini akan
menjadi lebih penting lagi bagi fungsionalitas yang disediakan type-type
*smart pointer* lain yang akan kita bahas di sisa bab ini. Mari kita jelajahi
kedua *trait* ini lebih jauh.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
