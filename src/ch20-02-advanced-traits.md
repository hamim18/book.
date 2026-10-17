<a id="advanced-traits"></a>
## Trait Lanjutan

Pertama kali kita membahas trait di seksi [“Mendefinisikan Perilaku Bersama
dengan Trait”][traits]<!-- ignore --> pada Bab 10, tetapi kita belum membahas
detail-detail yang lebih lanjut. Sekarang setelah Anda tahu lebih banyak
tentang Rust, kita bisa masuk ke seluk-beluknya.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>
<a id="associated-types"></a>

### Mendefinisikan Trait dengan Tipe Asosiasi

*Associated type* (tipe asosiasi) menghubungkan tipe placeholder dengan
sebuah trait sedemikian rupa sehingga definisi-definisi metode trait itu bisa
memakai tipe placeholder tersebut di tanda tangan mereka. Pengimplementasi
sebuah trait akan menentukan tipe konkret yang akan dipakai sebagai pengganti
tipe placeholder untuk implementasi tertentu. Dengan begitu, kita bisa
mendefinisikan trait yang memakai beberapa tipe tanpa perlu tahu persis
tipe-tipe apa itu sampai trait tersebut diimplementasikan.

Kami telah menggambarkan sebagian besar fitur lanjutan di bab ini sebagai
fitur yang jarang dibutuhkan. Tipe asosiasi ada di posisi tengah: Tipe ini
lebih jarang dipakai daripada fitur-fitur yang dijelaskan di bagian lain buku
ini, tetapi lebih sering daripada banyak fitur lain yang dibahas di bab ini.

Salah satu contoh trait dengan tipe asosiasi adalah trait `Iterator` yang
disediakan pustaka standar. Tipe asosiasinya diberi nama `Item` dan mewakili
tipe dari nilai-nilai yang sedang diiterasi oleh tipe yang
mengimplementasikan trait `Iterator`. Definisi trait `Iterator` adalah
seperti yang ditunjukkan di Listing 20-13.

<Listing number="20-13" caption="Definisi trait `Iterator` yang memiliki tipe asosiasi `Item`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Tipe `Item` adalah placeholder, dan definisi metode `next` menunjukkan bahwa
ia akan mengembalikan nilai bertipe `Option<Self::Item>`. Pengimplementasi
trait `Iterator` akan menentukan tipe konkret untuk `Item`, dan metode `next`
akan mengembalikan `Option` yang berisi nilai dari tipe konkret itu.

Tipe asosiasi mungkin tampak seperti konsep yang mirip dengan generics,
dalam artian generics memungkinkan kita mendefinisikan fungsi tanpa
menentukan tipe apa saja yang bisa ditanganinya. Untuk menelaah perbedaan
antara kedua konsep itu, kita akan melihat implementasi trait `Iterator` pada
tipe bernama `Counter` yang menentukan bahwa tipe `Item` adalah `u32`:

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Sintaks ini tampak sebanding dengan sintaks generics. Jadi, mengapa tidak
mendefinisikan trait `Iterator` saja dengan generics, seperti yang
ditunjukkan di Listing 20-14?

<Listing number="20-14" caption="Definisi hipotetis trait `Iterator` yang memakai generics">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

Perbedaannya adalah, saat memakai generics seperti di Listing 20-14, kita
harus menganotasi tipenya pada setiap implementasi; karena kita juga bisa
mengimplementasikan `Iterator<String> for Counter` atau tipe lain apa pun,
kita bisa memiliki banyak implementasi `Iterator` untuk `Counter`. Dengan
kata lain, ketika sebuah trait memiliki parameter generik, trait itu bisa
diimplementasikan untuk sebuah tipe berkali-kali, dengan mengubah tipe
konkret parameter-parameter tipe generiknya setiap kali. Saat kita memakai
metode `next` pada `Counter`, kita harus memberikan anotasi tipe untuk
menunjukkan implementasi `Iterator` mana yang ingin kita pakai.

Dengan tipe asosiasi, kita tidak perlu menganotasi tipe, karena kita tidak
bisa mengimplementasikan sebuah trait pada sebuah tipe berkali-kali. Pada
Listing 20-13 dengan definisi yang memakai tipe asosiasi, kita hanya bisa
memilih tipe `Item` satu kali karena hanya boleh ada satu `impl Iterator for
Counter`. Kita tidak perlu menentukan bahwa kita menginginkan iterator berisi
nilai `u32` di setiap tempat kita memanggil `next` pada `Counter`.

Tipe asosiasi juga menjadi bagian dari kontrak trait: Pengimplementasi trait
harus menyediakan sebuah tipe untuk menggantikan placeholder tipe asosiasi
itu. Tipe asosiasi sering kali memiliki nama yang menggambarkan bagaimana
tipe itu akan dipakai, dan mendokumentasikan tipe asosiasi itu di dokumentasi
API adalah praktik yang baik.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-generic-type-parameters-and-operator-overloading"></a>

### Memakai Parameter Generik Bawaan dan Operator Overloading

Saat kita memakai parameter tipe generik, kita bisa menentukan tipe konkret
bawaan untuk tipe generik itu. Ini menghilangkan kebutuhan pengimplementasi
trait untuk menentukan tipe konkret jika tipe bawaannya sudah cocok. Anda
menentukan tipe bawaan saat mendeklarasikan tipe generik dengan sintaks
`<PlaceholderType=ConcreteType>`.

Contoh bagus dari situasi di mana teknik ini berguna adalah pada *operator
overloading* (overload operator), yaitu ketika Anda menyesuaikan perilaku
sebuah operator (seperti `+`) dalam situasi-situasi tertentu.

Rust tidak mengizinkan Anda membuat operator sendiri atau meng-overload
operator sembarang. Tetapi Anda bisa meng-overload operasi dan trait terkait
yang didaftarkan di `std::ops` dengan mengimplementasikan trait yang
dikaitkan dengan operator itu. Misalnya, di Listing 20-15, kita
meng-overload operator `+` untuk menjumlahkan dua instance `Point`. Kita
melakukannya dengan mengimplementasikan trait `Add` pada struct `Point`.

<Listing number="20-15" file-name="src/main.rs" caption="Mengimplementasikan trait `Add` untuk meng-overload operator `+` bagi instance `Point`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

Metode `add` menjumlahkan nilai `x` dari dua instance `Point` dan nilai `y`
dari dua instance `Point` untuk membuat sebuah `Point` baru. Trait `Add`
memiliki tipe asosiasi bernama `Output` yang menentukan tipe yang
dikembalikan dari metode `add`.

Tipe generik bawaan pada kode ini berada di dalam trait `Add`. Berikut
definisinya:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Kode ini seharusnya tampak familier secara umum: sebuah trait dengan satu
metode dan satu tipe asosiasi. Bagian barunya adalah `Rhs=Self`: Sintaks ini
disebut *default type parameter* (parameter tipe bawaan). Parameter tipe
generik `Rhs` (singkatan dari “right-hand side”, sisi kanan) mendefinisikan
tipe parameter `rhs` di metode `add`. Jika kita tidak menentukan tipe konkret
untuk `Rhs` saat mengimplementasikan trait `Add`, tipe `Rhs` akan menjadi
`Self` secara bawaan, yaitu tipe tempat kita mengimplementasikan `Add`.

Saat kita mengimplementasikan `Add` untuk `Point`, kita memakai nilai bawaan
untuk `Rhs` karena kita ingin menjumlahkan dua instance `Point`. Mari kita
lihat contoh implementasi trait `Add` di mana kita ingin menyesuaikan tipe
`Rhs` alih-alih memakai nilai bawaannya.

Kita punya dua struct, `Millimeters` dan `Meters`, yang menyimpan nilai
dalam satuan yang berbeda. Pembungkusan tipis terhadap tipe yang sudah ada
di dalam struct lain ini dikenal sebagai *newtype pattern* (pola newtype),
yang kita jelaskan lebih detail di seksi [“Mengimplementasikan Trait
Eksternal dengan Pola Newtype”][newtype]<!-- ignore -->. Kita ingin
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
Add<Meters>` untuk menetapkan nilai parameter tipe `Rhs` alih-alih memakai
nilai bawaan `Self`.

Anda akan memakai parameter tipe bawaan dengan dua cara utama:

1. Untuk memperluas sebuah tipe tanpa merusak kode yang sudah ada
2. Untuk memungkinkan kustomisasi pada kasus-kasus spesifik yang tidak
   dibutuhkan sebagian besar pengguna

Trait `Add` dari pustaka standar adalah contoh tujuan kedua: Biasanya, Anda
akan menjumlahkan dua tipe yang sejenis, tetapi trait `Add` menyediakan
kemampuan untuk menyesuaikan lebih dari itu. Memakai parameter tipe bawaan
di definisi trait `Add` berarti Anda tidak perlu menentukan parameter
tambahan itu pada sebagian besar waktu. Dengan kata lain, sedikit boilerplate
implementasi tidak lagi diperlukan, sehingga trait itu lebih mudah dipakai.

Tujuan pertama mirip dengan tujuan kedua, tetapi sebaliknya: Jika Anda ingin
menambahkan parameter tipe ke trait yang sudah ada, Anda bisa memberinya
nilai bawaan untuk memungkinkan perluasan fungsionalitas trait itu tanpa
merusak kode implementasi yang sudah ada.

<!-- Old headings. Do not remove or links may break. -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>
<a id="disambiguating-between-methods-with-the-same-name"></a>

### Mendisambiguasi Metode dengan Nama yang Sama

Tidak ada apa pun di Rust yang mencegah sebuah trait memiliki metode dengan
nama yang sama dengan metode trait lain, dan Rust juga tidak mencegah Anda
mengimplementasikan kedua trait itu pada satu tipe. Anda juga bisa
mengimplementasikan sebuah metode langsung pada tipe dengan nama yang sama
dengan metode-metode dari trait.

Saat memanggil metode-metode dengan nama yang sama, Anda perlu memberi tahu
Rust mana yang ingin Anda pakai. Perhatikan kode di Listing 20-17, tempat
kita mendefinisikan dua trait, `Pilot` dan `Wizard`, yang sama-sama memiliki
metode bernama `fly`. Kita kemudian mengimplementasikan kedua trait itu pada
tipe `Human` yang sudah memiliki metode bernama `fly` yang
diimplementasikan padanya. Setiap metode `fly` melakukan hal yang berbeda.

<Listing number="20-17" file-name="src/main.rs" caption="Dua trait didefinisikan dengan metode `fly` dan diimplementasikan pada tipe `Human`, dan sebuah metode `fly` diimplementasikan langsung pada `Human`.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Saat kita memanggil `fly` pada sebuah instance `Human`, kompilator secara
bawaan memanggil metode yang diimplementasikan langsung pada tipe itu,
seperti yang ditunjukkan di Listing 20-18.

<Listing number="20-18" file-name="src/main.rs" caption="Memanggil `fly` pada instance `Human`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

Menjalankan kode ini akan mencetak `*waving arms furiously*`, yang
menunjukkan bahwa Rust memanggil metode `fly` yang diimplementasikan
langsung pada `Human`.

Untuk memanggil metode `fly` dari trait `Pilot` ataupun trait `Wizard`, kita
perlu memakai sintaks yang lebih eksplisit untuk menentukan metode `fly`
mana yang kita maksud. Listing 20-19 menunjukkan sintaks ini.

<Listing number="20-19" file-name="src/main.rs" caption="Menentukan metode `fly` dari trait mana yang ingin kita panggil">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Menuliskan nama trait sebelum nama metode memperjelas kepada Rust
implementasi `fly` mana yang ingin kita panggil. Kita juga bisa menulis
`Human::fly(&person)`, yang setara dengan `person.fly()` yang kita pakai di
Listing 20-19, tetapi ini sedikit lebih panjang untuk ditulis jika kita tidak
perlu mendisambiguasi.

Menjalankan kode ini mencetak hal berikut:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Karena metode `fly` menerima parameter `self`, jika kita memiliki dua *tipe*
yang sama-sama mengimplementasikan satu *trait*, Rust bisa menentukan
implementasi trait mana yang dipakai berdasarkan tipe dari `self`.

Akan tetapi, *associated function* (fungsi asosiasi) yang bukan metode tidak
memiliki parameter `self`. Ketika ada banyak tipe atau trait yang
mendefinisikan fungsi non-metode dengan nama fungsi yang sama, Rust tidak
selalu tahu tipe mana yang Anda maksud kecuali Anda memakai sintaks *fully
qualified*. Misalnya, di Listing 20-20, kita membuat trait untuk sebuah
penampungan hewan yang ingin menamai semua bayi anjing dengan nama Spot.
Kita membuat trait `Animal` dengan fungsi asosiasi non-metode `baby_name`.
Trait `Animal` diimplementasikan untuk struct `Dog`, yang padanya kita juga
menyediakan fungsi asosiasi non-metode `baby_name` secara langsung.

<Listing number="20-20" file-name="src/main.rs" caption="Sebuah trait dengan fungsi asosiasi dan sebuah tipe dengan fungsi asosiasi bernama sama yang juga mengimplementasikan trait itu">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Kita mengimplementasikan kode untuk menamai semua anak anjing dengan nama
Spot di fungsi asosiasi `baby_name` yang didefinisikan pada `Dog`. Tipe
`Dog` juga mengimplementasikan trait `Animal`, yang menggambarkan
karakteristik yang dimiliki semua hewan. Bayi anjing disebut puppy, dan hal
itu diungkapkan dalam implementasi trait `Animal` pada `Dog` di fungsi
`baby_name` yang dikaitkan dengan trait `Animal`.

Di `main`, kita memanggil fungsi `Dog::baby_name`, yang memanggil fungsi
asosiasi yang didefinisikan langsung pada `Dog`. Kode ini mencetak hal
berikut:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Output ini bukan yang kita inginkan. Kita ingin memanggil fungsi `baby_name`
yang menjadi bagian dari trait `Animal` yang kita implementasikan pada `Dog`
supaya kode itu mencetak `A baby dog is called a puppy`. Teknik menentukan
nama trait yang kita pakai di Listing 20-19 tidak membantu di sini; jika kita
mengubah `main` menjadi kode di Listing 20-21, kita akan mendapat galat
kompilasi.

<Listing number="20-21" file-name="src/main.rs" caption="Berusaha memanggil fungsi `baby_name` dari trait `Animal`, tetapi Rust tidak tahu implementasi mana yang dipakai">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Karena `Animal::baby_name` tidak memiliki parameter `self`, dan mungkin ada
tipe-tipe lain yang mengimplementasikan trait `Animal`, Rust tidak bisa
menentukan implementasi `Animal::baby_name` mana yang kita inginkan. Kita
akan mendapat galat kompilator berikut:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Untuk mendisambiguasi dan memberi tahu Rust bahwa kita ingin memakai
implementasi `Animal` untuk `Dog`, alih-alih implementasi `Animal` untuk tipe
lain, kita perlu memakai sintaks fully qualified. Listing 20-22 menunjukkan
cara memakai sintaks fully qualified.

<Listing number="20-22" file-name="src/main.rs" caption="Memakai sintaks fully qualified untuk menentukan bahwa kita ingin memanggil fungsi `baby_name` dari trait `Animal` sebagaimana diimplementasikan pada `Dog`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

Kita memberikan Rust sebuah anotasi tipe di dalam kurung sudut, yang
menunjukkan bahwa kita ingin memanggil metode `baby_name` dari trait
`Animal` sebagaimana diimplementasikan pada `Dog`, dengan menyatakan bahwa
kita ingin memperlakukan tipe `Dog` sebagai `Animal` untuk pemanggilan fungsi
ini. Kode ini sekarang akan mencetak apa yang kita inginkan:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

Secara umum, sintaks fully qualified didefinisikan sebagai berikut:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

Untuk fungsi asosiasi yang bukan metode, tidak akan ada *receiver*
(penerima): Yang ada hanya daftar argumen-argumen lain. Anda bisa memakai
sintaks fully qualified di setiap tempat Anda memanggil fungsi atau metode.
Akan tetapi, Anda boleh menghilangkan bagian mana pun dari sintaks ini yang
bisa disimpulkan Rust dari informasi lain di program. Anda hanya perlu
memakai sintaks yang lebih panjang ini pada kasus ketika ada banyak
implementasi yang memakai nama yang sama dan Rust membutuhkan bantuan untuk
mengenali implementasi mana yang ingin Anda panggil.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>

### Memakai Supertrait

Terkadang Anda mungkin menulis definisi trait yang bergantung pada trait
lain: Agar sebuah tipe bisa mengimplementasikan trait pertama, Anda ingin
mewajibkan tipe itu untuk juga mengimplementasikan trait kedua. Anda
melakukan ini supaya definisi trait Anda bisa memakai item-item asosiasi dari
trait kedua. Trait yang diandalkan definisi trait Anda disebut *supertrait*
dari trait Anda.

Sebagai contoh, katakanlah kita ingin membuat trait `OutlinePrint` dengan
metode `outline_print` yang akan mencetak sebuah nilai yang diberikan dengan
format yang dibingkai tanda bintang. Artinya, jika ada struct `Point` yang
mengimplementasikan trait `Display` dari pustaka standar sehingga
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

Dalam implementasi metode `outline_print`, kita ingin memakai fungsionalitas
trait `Display`. Karena itu, kita perlu menentukan bahwa trait `OutlinePrint`
hanya akan bekerja untuk tipe-tipe yang juga mengimplementasikan `Display`
dan menyediakan fungsionalitas yang dibutuhkan `OutlinePrint`. Kita bisa
melakukannya di definisi trait dengan menuliskan `OutlinePrint: Display`.
Teknik ini mirip dengan menambahkan trait bound pada trait itu. Listing 20-23
menunjukkan implementasi trait `OutlinePrint`.

<Listing number="20-23" file-name="src/main.rs" caption="Mengimplementasikan trait `OutlinePrint` yang memerlukan fungsionalitas dari `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Karena kita telah menentukan bahwa `OutlinePrint` memerlukan trait
`Display`, kita bisa memakai fungsi `to_string` yang diimplementasikan secara
otomatis untuk tipe apa pun yang mengimplementasikan `Display`. Jika kita
mencoba memakai `to_string` tanpa menambahkan tanda titik dua dan menuliskan
trait `Display` setelah nama trait, kita akan mendapat galat yang menyatakan
bahwa tidak ada metode bernama `to_string` yang ditemukan untuk tipe `&Self`
di scope saat ini.

Mari kita lihat apa yang terjadi saat kita mencoba mengimplementasikan
`OutlinePrint` pada tipe yang tidak mengimplementasikan `Display`, seperti
struct `Point`:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Kita mendapat galat yang menyatakan bahwa `Display` diperlukan tetapi belum
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

Kemudian, mengimplementasikan trait `OutlinePrint` pada `Point` akan
terkompilasi dengan sukses, dan kita bisa memanggil `outline_print` pada
instance `Point` untuk menampilkannya di dalam bingkai tanda bintang.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-to-implement-external-traits-on-external-types"></a>
<a id="using-the-newtype-pattern-to-implement-external-traits"></a>

<a id="implementing-external-traits-with-the-newtype-pattern"></a>
### Mengimplementasikan Trait Eksternal dengan Pola Newtype

Di seksi [“Mengimplementasikan Trait pada Suatu Tipe”][implementing-a-trait-on-a-type]<!--
ignore --> pada Bab 10, kita menyebutkan orphan rule yang menyatakan bahwa
kita hanya boleh mengimplementasikan sebuah trait pada sebuah tipe jika trait
atau tipe itu, atau keduanya, bersifat lokal bagi crate kita. Batasan ini
bisa diakali dengan memakai pola newtype, yang melibatkan pembuatan tipe baru
di dalam tuple struct. (Kita membahas tuple struct di seksi [“Membuat Tipe
Berbeda dengan Tuple Struct”][tuple-structs]<!-- ignore --> pada Bab 5.)
Tuple struct itu akan memiliki satu field dan menjadi wrapper tipis di
sekeliling tipe yang ingin kita implementasikan trait-nya. Dengan begitu,
tipe wrapper itu bersifat lokal bagi crate kita, dan kita bisa
mengimplementasikan trait itu pada wrapper. *Newtype* adalah istilah yang
berasal dari bahasa pemrograman Haskell. Tidak ada denda performa runtime
untuk memakai pola ini, dan tipe wrapper-nya dihilangkan pada waktu
kompilasi.

Sebagai contoh, katakanlah kita ingin mengimplementasikan `Display` pada
`Vec<T>`, yang tidak bisa kita lakukan secara langsung karena dilarang orphan
rule, sebab trait `Display` dan tipe `Vec<T>` didefinisikan di luar crate
kita. Kita bisa membuat struct `Wrapper` yang menyimpan sebuah instance
`Vec<T>`; kemudian, kita bisa mengimplementasikan `Display` pada `Wrapper`
dan memakai nilai `Vec<T>` itu, seperti yang ditunjukkan di Listing 20-24.

<Listing number="20-24" file-name="src/main.rs" caption="Membuat tipe `Wrapper` di sekeliling `Vec<String>` untuk mengimplementasikan `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

Implementasi `Display` memakai `self.0` untuk mengakses `Vec<T>` di
dalamnya karena `Wrapper` adalah tuple struct dan `Vec<T>` adalah item pada
indeks 0 di tuple itu. Kemudian, kita bisa memakai fungsionalitas trait
`Display` pada `Wrapper`.

Kekurangan dari teknik ini adalah `Wrapper` adalah tipe baru, jadi ia tidak
memiliki metode-metode dari nilai yang disimpannya. Kita harus
mengimplementasikan semua metode `Vec<T>` langsung pada `Wrapper` sedemikian
rupa sehingga metode-metode itu mendelegasikan ke `self.0`, yang
memungkinkan kita memperlakukan `Wrapper` persis seperti `Vec<T>`. Jika kita
ingin tipe baru itu memiliki semua metode yang dimiliki tipe di dalamnya,
mengimplementasikan trait `Deref` pada `Wrapper` untuk mengembalikan tipe di
dalamnya akan menjadi solusi (kita membahas implementasi trait `Deref` di
seksi [“Memperlakukan Smart Pointer Seperti Reference Biasa”][smart-pointer-deref]<!-- ignore
--> pada Bab 15). Jika kita tidak ingin tipe `Wrapper` memiliki semua metode
tipe di dalamnya—misalnya, untuk membatasi perilaku tipe `Wrapper`—kita
harus mengimplementasikan secara manual hanya metode-metode yang memang kita
inginkan.

Pola newtype ini juga berguna bahkan ketika tidak ada trait yang terlibat.
Mari kita alihkan fokus dan melihat beberapa cara lanjutan untuk berinteraksi
dengan sistem tipe Rust.

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
