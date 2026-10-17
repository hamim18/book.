<a id="advanced-traits"></a>
## Trait Lanjutan

Pertama kali kita membahas *trait* di seksi [“Mendefinisikan Perilaku Bersama
dengan *Trait*”][traits]<!-- ignore --> pada Bab 10, tetapi kita belum membahas
detail-detail yang lebih lanjut. Sekarang setelah Anda tahu lebih banyak
tentang Rust, kita bisa masuk ke seluk-beluknya.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>
<a id="associated-types"></a>

### Mendefinisikan Trait dengan Type Asosiasi

*Associated type* (tipe asosiasi) menghubungkan type placeholder dengan
sebuah *trait* sedemikian rupa sehingga definisi-definisi method *trait* itu bisa
memakai type placeholder tersebut di *signature* mereka. Pengimplementasi
sebuah *trait* akan menentukan type konkret yang akan dipakai sebagai pengganti
type placeholder untuk implementasi tertentu. Dengan begitu, kita bisa
mendefinisikan *trait* yang memakai beberapa type tanpa perlu tahu persis
type-type apa itu sampai *trait* tersebut diimplementasikan.

Kami telah menggambarkan sebagian besar fitur lanjutan di bab ini sebagai
fitur yang jarang dibutuhkan. Type asosiasi ada di posisi tengah: Type ini
lebih jarang dipakai daripada fitur-fitur yang dijelaskan di bagian lain buku
ini, tetapi lebih sering daripada banyak fitur lain yang dibahas di bab ini.

Salah satu contoh *trait* dengan associated type adalah *trait* `Iterator` yang
disediakan standard library. Type asosiasinya diberi nama `Item` dan mewakili
type dari nilai-nilai yang sedang diiterasi oleh type yang
mengimplementasikan *trait* `Iterator`. Definisi *trait* `Iterator` adalah
seperti yang ditunjukkan di Listing 20-13.

<Listing number="20-13" caption="Definisi trait `Iterator` yang memiliki associated type `Item`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Type `Item` adalah placeholder, dan definisi method `next` menunjukkan bahwa
ia akan mengembalikan nilai typed `Option<Self::Item>`. Pengimplementasi
*trait* `Iterator` akan menentukan type konkret untuk `Item`, dan method `next`
akan mengembalikan `Option` yang berisi nilai dari type konkret itu.

Type asosiasi mungkin tampak seperti konsep yang mirip dengan *generics*,
dalam artian *generics* memungkinkan kita mendefinisikan fungsi tanpa
menentukan type apa saja yang bisa ditanganinya. Untuk menelaah perbedaan
antara kedua konsep itu, kita akan melihat implementasi *trait* `Iterator` pada
type bernama `Counter` yang menentukan bahwa type `Item` adalah `u32`:

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Sintaks ini tampak sebanding dengan sintaks *generics*. Jadi, mengapa tidak
mendefinisikan *trait* `Iterator` saja dengan *generics*, seperti yang
ditunjukkan di Listing 20-14?

<Listing number="20-14" caption="Definisi hipotetis trait `Iterator` yang memakai generics">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

Perbedaannya adalah, saat memakai *generics* seperti di Listing 20-14, kita
harus mengtype annotationnya pada setiap implementasi; karena kita juga bisa
mengimplementasikan `Iterator<String> for Counter` atau type lain apa pun,
kita bisa memiliki banyak implementasi `Iterator` untuk `Counter`. Dengan
kata lain, ketika sebuah *trait* memiliki parameter generik, *trait* itu bisa
diimplementasikan untuk sebuah type berkali-kali, dengan mengubah type
konkret parameter-type parameter generiknya setiap kali. Saat kita memakai
method `next` pada `Counter`, kita harus memberikan type annotation untuk
menunjukkan implementasi `Iterator` mana yang ingin kita pakai.

Dengan associated type, kita tidak perlu mengtype annotation, karena kita tidak
bisa mengimplementasikan sebuah *trait* pada sebuah type berkali-kali. Pada
Listing 20-13 dengan definisi yang memakai associated type, kita hanya bisa
memilih type `Item` satu kali karena hanya boleh ada satu `impl Iterator for
Counter`. Kita tidak perlu menentukan bahwa kita menginginkan *iterator* berisi
nilai `u32` di setiap tempat kita memanggil `next` pada `Counter`.

Type asosiasi juga menjadi bagian dari kontrak *trait*: Pengimplementasi *trait*
harus menyediakan sebuah type untuk menggantikan placeholder associated type
itu. Type asosiasi sering kali memiliki nama yang menggambarkan bagaimana
type itu akan dipakai, dan mendokumentasikan associated type itu di dokumentasi
API adalah praktik yang baik.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-generic-type-parameters-and-operator-overloading"></a>

### Memakai Parameter Generik Bawaan dan Operator Overloading

Saat kita memakai type parameter generik, kita bisa menentukan type konkret
bawaan untuk generic type itu. Ini menghilangkan kebutuhan pengimplementasi
*trait* untuk menentukan type konkret jika type bawaannya sudah cocok. Anda
menentukan type bawaan saat mendeklarasikan generic type dengan sintaks
`<PlaceholderType=ConcreteType>`.

Contoh bagus dari situasi di mana teknik ini berguna adalah pada *operator
overloading* (overload operator), yaitu ketika Anda menyesuaikan perilaku
sebuah operator (seperti `+`) dalam situasi-situasi tertentu.

Rust tidak mengizinkan Anda membuat operator sendiri atau meng-overload
operator sembarang. Tetapi Anda bisa meng-overload operasi dan *trait* terkait
yang didaftarkan di `std::ops` dengan mengimplementasikan *trait* yang
dikaitkan dengan operator itu. Misalnya, di Listing 20-15, kita
meng-overload operator `+` untuk menjumlahkan dua instance `Point`. Kita
melakukannya dengan mengimplementasikan *trait* `Add` pada *struct* `Point`.

<Listing number="20-15" file-name="src/main.rs" caption="Mengimplementasikan trait `Add` untuk meng-overload operator `+` bagi instance `Point`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

Method `add` menjumlahkan nilai `x` dari dua instance `Point` dan nilai `y`
dari dua instance `Point` untuk membuat sebuah `Point` baru. *Trait* `Add`
memiliki associated type bernama `Output` yang menentukan type yang
dikembalikan dari method `add`.

Type generik bawaan pada kode ini berada di dalam *trait* `Add`. Berikut
definisinya:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Kode ini seharusnya tampak familier secara umum: sebuah *trait* dengan satu
method dan satu associated type. Bagian barunya adalah `Rhs=Self`: Sintaks ini
disebut *default type parameter* (parameter tipe bawaan). Parameter type
generik `Rhs` (singkatan dari “right-hand side”, sisi kanan) mendefinisikan
type parameter `rhs` di method `add`. Jika kita tidak menentukan type konkret
untuk `Rhs` saat mengimplementasikan *trait* `Add`, type `Rhs` akan menjadi
`Self` secara bawaan, yaitu type tempat kita mengimplementasikan `Add`.

Saat kita mengimplementasikan `Add` untuk `Point`, kita memakai nilai bawaan
untuk `Rhs` karena kita ingin menjumlahkan dua instance `Point`. Mari kita
lihat contoh implementasi *trait* `Add` di mana kita ingin menyesuaikan type
`Rhs` alih-alih memakai nilai bawaannya.

Kita punya dua *struct*, `Millimeters` dan `Meters`, yang menyimpan nilai
dalam satuan yang berbeda. Pembungkusan tipis terhadap type yang sudah ada
di dalam *struct* lain ini dikenal sebagai *newtype pattern* (newtype pattern),
yang kita jelaskan lebih detail di seksi [“Mengimplementasikan *Trait*
Eksternal dengan Pattern Newtype”][newtype]<!-- ignore -->. Kita ingin
menjumlahkan nilai dalam milimeter dengan nilai dalam meter dan membuat
implementasi `Add` melakukan konversinya dengan benar. Kita bisa
mengimplementasikan `Add` untuk `Millimeters` dengan `Meters` sebagai `Rhs`,
seperti yang ditunjukkan di Listing 20-16.

<Listing number="20-16" file-name="src/lib.rs" caption="Mengimplementasikan trait `Add` pada `Millimeters` untuk menjumlahkan `Millimeters` dan `Meters`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

Untuk menjumlahkan `Millimeters` dan `Meters`, kita menulis `impl
Add<Meters>` untuk menetapkan nilai type parameter `Rhs` alih-alih memakai
nilai bawaan `Self`.

Anda akan memakai type parameter bawaan dengan dua cara utama:

1. Untuk memperluas sebuah type tanpa merusak kode yang sudah ada
2. Untuk memungkinkan kustomisasi pada kasus-kasus spesifik yang tidak
   dibutuhkan sebagian besar pengguna

*Trait* `Add` dari standard library adalah contoh tujuan kedua: Biasanya, Anda
akan menjumlahkan dua type yang sejenis, tetapi *trait* `Add` menyediakan
kemampuan untuk menyesuaikan lebih dari itu. Memakai type parameter bawaan
di definisi *trait* `Add` berarti Anda tidak perlu menentukan parameter
tambahan itu pada sebagian besar waktu. Dengan kata lain, sedikit boilerplate
implementasi tidak lagi diperlukan, sehingga *trait* itu lebih mudah dipakai.

Tujuan pertama mirip dengan tujuan kedua, tetapi sebaliknya: Jika Anda ingin
menambahkan type parameter ke *trait* yang sudah ada, Anda bisa memberinya
nilai bawaan untuk memungkinkan perluasan fungsionalitas *trait* itu tanpa
merusak kode implementasi yang sudah ada.

<!-- Old headings. Do not remove or links may break. -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>
<a id="disambiguating-between-methods-with-the-same-name"></a>

### Mendisambiguasi Method dengan Nama yang Sama

Tidak ada apa pun di Rust yang mencegah sebuah *trait* memiliki method dengan
nama yang sama dengan method *trait* lain, dan Rust juga tidak mencegah Anda
mengimplementasikan kedua *trait* itu pada satu type. Anda juga bisa
mengimplementasikan sebuah method langsung pada type dengan nama yang sama
dengan method-method dari *trait*.

Saat memanggil method-method dengan nama yang sama, Anda perlu memberi tahu
Rust mana yang ingin Anda pakai. Perhatikan kode di Listing 20-17, tempat
kita mendefinisikan dua *trait*, `Pilot` dan `Wizard`, yang sama-sama memiliki
method bernama `fly`. Kita kemudian mengimplementasikan kedua *trait* itu pada
type `Human` yang sudah memiliki method bernama `fly` yang
diimplementasikan padanya. Setiap method `fly` melakukan hal yang berbeda.

<Listing number="20-17" file-name="src/main.rs" caption="Dua trait didefinisikan dengan method `fly` dan diimplementasikan pada type `Human`, dan sebuah method `fly` diimplementasikan langsung pada `Human`.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Saat kita memanggil `fly` pada sebuah instance `Human`, *compiler* secara
bawaan memanggil method yang diimplementasikan langsung pada type itu,
seperti yang ditunjukkan di Listing 20-18.

<Listing number="20-18" file-name="src/main.rs" caption="Memanggil `fly` pada instance `Human`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

Menjalankan kode ini akan mencetak `*waving arms furiously*`, yang
menunjukkan bahwa Rust memanggil method `fly` yang diimplementasikan
langsung pada `Human`.

Untuk memanggil method `fly` dari *trait* `Pilot` ataupun *trait* `Wizard`, kita
perlu memakai sintaks yang lebih eksplisit untuk menentukan method `fly`
mana yang kita maksud. Listing 20-19 menunjukkan sintaks ini.

<Listing number="20-19" file-name="src/main.rs" caption="Menentukan method `fly` dari trait mana yang ingin kita panggil">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Menuliskan nama *trait* sebelum nama method memperjelas kepada Rust
implementasi `fly` mana yang ingin kita panggil. Kita juga bisa menulis
`Human::fly(&person)`, yang setara dengan `person.fly()` yang kita pakai di
Listing 20-19, tetapi ini sedikit lebih panjang untuk ditulis jika kita tidak
perlu mendisambiguasi.

Menjalankan kode ini mencetak hal berikut:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Karena method `fly` menerima parameter `self`, jika kita memiliki dua *type*
yang sama-sama mengimplementasikan satu *trait*, Rust bisa menentukan
implementasi *trait* mana yang dipakai berdasarkan type dari `self`.

Akan tetapi, *associated function* (fungsi asosiasi) yang bukan method tidak
memiliki parameter `self`. Ketika ada banyak type atau *trait* yang
mendefinisikan fungsi non-method dengan nama fungsi yang sama, Rust tidak
selalu tahu type mana yang Anda maksud kecuali Anda memakai sintaks *fully
qualified*. Misalnya, di Listing 20-20, kita membuat *trait* untuk sebuah
penampungan hewan yang ingin menamai semua bayi anjing dengan nama Spot.
Kita membuat *trait* `Animal` dengan fungsi asosiasi non-method `baby_name`.
*Trait* `Animal` diimplementasikan untuk *struct* `Dog`, yang padanya kita juga
menyediakan fungsi asosiasi non-method `baby_name` secara langsung.

<Listing number="20-20" file-name="src/main.rs" caption="Sebuah trait dengan fungsi asosiasi dan sebuah type dengan fungsi asosiasi bernama sama yang juga mengimplementasikan trait itu">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Kita mengimplementasikan kode untuk menamai semua anak anjing dengan nama
Spot di fungsi asosiasi `baby_name` yang didefinisikan pada `Dog`. Type
`Dog` juga mengimplementasikan *trait* `Animal`, yang menggambarkan
karakteristik yang dimiliki semua hewan. Bayi anjing disebut puppy, dan hal
itu diungkapkan dalam implementasi *trait* `Animal` pada `Dog` di fungsi
`baby_name` yang dikaitkan dengan *trait* `Animal`.

Di `main`, kita memanggil fungsi `Dog::baby_name`, yang memanggil fungsi
asosiasi yang didefinisikan langsung pada `Dog`. Kode ini mencetak hal
berikut:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Output ini bukan yang kita inginkan. Kita ingin memanggil fungsi `baby_name`
yang menjadi bagian dari *trait* `Animal` yang kita implementasikan pada `Dog`
supaya kode itu mencetak `A baby dog is called a puppy`. Teknik menentukan
nama *trait* yang kita pakai di Listing 20-19 tidak membantu di sini; jika kita
mengubah `main` menjadi kode di Listing 20-21, kita akan mendapat error
kompilasi.

<Listing number="20-21" file-name="src/main.rs" caption="Berusaha memanggil fungsi `baby_name` dari trait `Animal`, tetapi Rust tidak tahu implementasi mana yang dipakai">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Karena `Animal::baby_name` tidak memiliki parameter `self`, dan mungkin ada
type-type lain yang mengimplementasikan *trait* `Animal`, Rust tidak bisa
menentukan implementasi `Animal::baby_name` mana yang kita inginkan. Kita
akan mendapat error *compiler* berikut:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Untuk mendisambiguasi dan memberi tahu Rust bahwa kita ingin memakai
implementasi `Animal` untuk `Dog`, alih-alih implementasi `Animal` untuk type
lain, kita perlu memakai sintaks fully qualified. Listing 20-22 menunjukkan
cara memakai sintaks fully qualified.

<Listing number="20-22" file-name="src/main.rs" caption="Memakai sintaks fully qualified untuk menentukan bahwa kita ingin memanggil fungsi `baby_name` dari trait `Animal` sebagaimana diimplementasikan pada `Dog`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

Kita memberikan Rust sebuah type annotation di dalam kurung sudut, yang
menunjukkan bahwa kita ingin memanggil method `baby_name` dari *trait*
`Animal` sebagaimana diimplementasikan pada `Dog`, dengan menyatakan bahwa
kita ingin memperlakukan type `Dog` sebagai `Animal` untuk pemanggilan fungsi
ini. Kode ini sekarang akan mencetak apa yang kita inginkan:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

Secara umum, sintaks fully qualified didefinisikan sebagai berikut:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

Untuk fungsi asosiasi yang bukan method, tidak akan ada *receiver*
(penerima): Yang ada hanya daftar argumen-argumen lain. Anda bisa memakai
sintaks fully qualified di setiap tempat Anda memanggil fungsi atau method.
Akan tetapi, Anda boleh menghilangkan bagian mana pun dari sintaks ini yang
bisa disimpulkan Rust dari informasi lain di program. Anda hanya perlu
memakai sintaks yang lebih panjang ini pada kasus ketika ada banyak
implementasi yang memakai nama yang sama dan Rust membutuhkan bantuan untuk
mengenali implementasi mana yang ingin Anda panggil.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>

### Memakai Supertrait

Terkadang Anda mungkin menulis definisi *trait* yang bergantung pada *trait*
lain: Agar sebuah type bisa mengimplementasikan *trait* pertama, Anda ingin
mewajibkan type itu untuk juga mengimplementasikan *trait* kedua. Anda
melakukan ini supaya definisi *trait* Anda bisa memakai item-item asosiasi dari
*trait* kedua. *Trait* yang diandalkan definisi *trait* Anda disebut *supertrait*
dari *trait* Anda.

Sebagai contoh, katakanlah kita ingin membuat *trait* `OutlinePrint` dengan
method `outline_print` yang akan mencetak sebuah nilai yang diberikan dengan
format yang dibingkai tanda bintang. Artinya, jika ada *struct* `Point` yang
mengimplementasikan *trait* `Display` dari standard library sehingga
menghasilkan `(x, y)`, saat kita memanggil `outline_print` pada instance
`Point` yang memiliki `1` untuk `x` dan `3` untuk `y`, ia harusnya mencetak
hal berikut:

```text
**********
*        *
* (1, 3) *
*        *
**********
```

Dalam implementasi method `outline_print`, kita ingin memakai fungsionalitas
*trait* `Display`. Karena itu, kita perlu menentukan bahwa *trait* `OutlinePrint`
hanya akan bekerja untuk type-type yang juga mengimplementasikan `Display`
dan menyediakan fungsionalitas yang dibutuhkan `OutlinePrint`. Kita bisa
melakukannya di definisi *trait* dengan menuliskan `OutlinePrint: Display`.
Teknik ini mirip dengan menambahkan *trait bound* pada *trait* itu. Listing 20-23
menunjukkan implementasi *trait* `OutlinePrint`.

<Listing number="20-23" file-name="src/main.rs" caption="Mengimplementasikan trait `OutlinePrint` yang memerlukan fungsionalitas dari `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Karena kita telah menentukan bahwa `OutlinePrint` memerlukan *trait*
`Display`, kita bisa memakai fungsi `to_string` yang diimplementasikan secara
otomatis untuk type apa pun yang mengimplementasikan `Display`. Jika kita
mencoba memakai `to_string` tanpa menambahkan tanda titik dua dan menuliskan
*trait* `Display` setelah nama *trait*, kita akan mendapat error yang menyatakan
bahwa tidak ada method bernama `to_string` yang ditemukan untuk type `&Self`
di *scope* saat ini.

Mari kita lihat apa yang terjadi saat kita mencoba mengimplementasikan
`OutlinePrint` pada type yang tidak mengimplementasikan `Display`, seperti
*struct* `Point`:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Kita mendapat error yang menyatakan bahwa `Display` diperlukan tetapi belum
diimplementasikan:

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

Untuk memperbaikinya, kita mengimplementasikan `Display` pada `Point` dan
memenuhi batasan yang diwajibkan `OutlinePrint`, seperti berikut:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

Kemudian, mengimplementasikan *trait* `OutlinePrint` pada `Point` akan
terkompilasi dengan sukses, dan kita bisa memanggil `outline_print` pada
instance `Point` untuk menampilkannya di dalam bingkai tanda bintang.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-to-implement-external-traits-on-external-types"></a>
<a id="using-the-newtype-pattern-to-implement-external-traits"></a>

<a id="implementing-external-traits-with-the-newtype-pattern"></a>
### Mengimplementasikan Trait Eksternal dengan Pattern Newtype

Di seksi [“Mengimplementasikan Trait pada Suatu Type”][implementing-a-trait-on-a-type]<!--
ignore --> pada Bab 10, kita menyebutkan *orphan rule* yang menyatakan bahwa
kita hanya boleh mengimplementasikan sebuah *trait* pada sebuah type jika *trait*
atau type itu, atau keduanya, bersifat lokal bagi *crate* kita. Batasan ini
bisa diakali dengan memakai newtype pattern, yang melibatkan pembuatan type baru
di dalam *tuple struct*. (Kita membahas *tuple struct* di seksi [“Membuat Type
Berbeda dengan *Tuple Struct*”][*tuple*-structs]<!-- ignore --> pada Bab 5.)
*Tuple struct* itu akan memiliki satu *field* dan menjadi wrapper tipis di
sekeliling type yang ingin kita implementasikan *trait*-nya. Dengan begitu,
type wrapper itu bersifat lokal bagi *crate* kita, dan kita bisa
mengimplementasikan *trait* itu pada wrapper. *Newtype* adalah istilah yang
berasal dari bahasa pemrograman Haskell. Tidak ada performance penalty runtime
untuk memakai pattern ini, dan type wrapper-nya dihilangkan pada waktu
kompilasi.

Sebagai contoh, katakanlah kita ingin mengimplementasikan `Display` pada
`Vec<T>`, yang tidak bisa kita lakukan secara langsung karena dilarang orphan
rule, sebab *trait* `Display` dan type `Vec<T>` didefinisikan di luar *crate*
kita. Kita bisa membuat *struct* `Wrapper` yang menyimpan sebuah instance
`Vec<T>`; kemudian, kita bisa mengimplementasikan `Display` pada `Wrapper`
dan memakai nilai `Vec<T>` itu, seperti yang ditunjukkan di Listing 20-24.

<Listing number="20-24" file-name="src/main.rs" caption="Membuat type `Wrapper` di sekeliling `Vec<String>` untuk mengimplementasikan `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

Implementasi `Display` memakai `self.0` untuk mengakses `Vec<T>` di
dalamnya karena `Wrapper` adalah *tuple struct* dan `Vec<T>` adalah item pada
indeks 0 di *tuple* itu. Kemudian, kita bisa memakai fungsionalitas *trait*
`Display` pada `Wrapper`.

Kekurangan dari teknik ini adalah `Wrapper` adalah type baru, jadi ia tidak
memiliki method-method dari nilai yang disimpannya. Kita harus
mengimplementasikan semua method `Vec<T>` langsung pada `Wrapper` sedemikian
rupa sehingga method-method itu mendelegasikan ke `self.0`, yang
memungkinkan kita memperlakukan `Wrapper` persis seperti `Vec<T>`. Jika kita
ingin type baru itu memiliki semua method yang dimiliki type di dalamnya,
mengimplementasikan *trait* `Deref` pada `Wrapper` untuk mengembalikan type di
dalamnya akan menjadi solusi (kita membahas implementasi *trait* `Deref` di
seksi [“Memperlakukan Smart Pointer Seperti Reference Biasa”][smart-pointer-deref]<!-- ignore
--> pada Bab 15). Jika kita tidak ingin type `Wrapper` memiliki semua method
type di dalamnya—misalnya, untuk membatasi perilaku type `Wrapper`—kita
harus mengimplementasikan secara manual hanya method-method yang memang kita
inginkan.

Pattern newtype ini juga berguna bahkan ketika tidak ada *trait* yang terlibat.
Mari kita alihkan fokus dan melihat beberapa cara lanjutan untuk berinteraksi
dengan type system Rust.

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
