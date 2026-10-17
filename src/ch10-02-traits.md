<!-- Old headings. Do not remove or links may break. -->

<a id="traits-defining-shared-behavior"></a>

## Mendefinisikan Perilaku Bersama dengan Trait

Sebuah *trait* mendefinisikan fungsionalitas yang dimiliki suatu tipe
tertentu dan bisa dibagikan dengan tipe-tipe lain. Kita bisa memakai *trait*
untuk mendefinisikan perilaku bersama secara abstrak. Kita bisa memakai
*trait bound* (batasan *trait*) untuk menentukan bahwa sebuah tipe generik
bisa berupa tipe apa pun yang memiliki perilaku tertentu.

> Catatan: *Trait* mirip dengan fitur yang sering disebut *interface*
> (antarmuka) dalam bahasa-bahasa lain, meskipun dengan beberapa perbedaan.

### Mendefinisikan Trait

Perilaku sebuah tipe terdiri atas metode-metode yang bisa kita panggil pada
tipe tersebut. Tipe-tipe yang berbeda berbagi perilaku yang sama jika kita
bisa memanggil metode-metode yang sama pada semua tipe itu. Definisi *trait*
adalah cara mengelompokkan tanda tangan metode untuk mendefinisikan
sekumpulan perilaku yang diperlukan untuk mencapai tujuan tertentu.

Sebagai contoh, katakanlah kita memiliki beberapa *struct* yang menampung
berbagai jenis dan jumlah teks: *struct* `NewsArticle` yang menampung berita
yang dilaporkan dari lokasi tertentu dan `SocialPost` yang bisa berisi
paling banyak 280 karakter beserta metadata yang menunjukkan apakah post
tersebut merupakan post baru, repost, atau balasan untuk post lain.

Kita ingin membuat *crate* library agregator media bernama `aggregator`
yang bisa menampilkan ringkasan data yang mungkin tersimpan dalam instance
`NewsArticle` atau `SocialPost`. Untuk melakukannya, kita memerlukan
ringkasan dari masing-masing tipe, dan kita akan meminta ringkasan itu
dengan memanggil metode `summarize` pada sebuah instance. Listing 10-12
menunjukkan definisi *trait* publik `Summary` yang mengekspresikan perilaku
ini.

<Listing number="10-12" file-name="src/lib.rs" caption="Trait `Summary` yang terdiri atas perilaku yang disediakan oleh metode `summarize`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

Di sini, kita mendeklarasikan sebuah *trait* memakai kata kunci `trait` lalu
nama *trait*-nya, yang dalam kasus ini adalah `Summary`. Kita juga
mendeklarasikan *trait* itu sebagai `pub` supaya *crate*-crate yang bergantung
pada *crate* ini juga bisa memakai *trait* ini, seperti yang akan kita lihat
dalam beberapa contoh. Di dalam kurung kurawal, kita mendeklarasikan tanda
tangan metode yang mendeskripsikan perilaku tipe-tipe yang
mengimplementasikan *trait* ini, yang dalam kasus ini adalah `fn summarize(&self)
-> String`.

Setelah tanda tangan metode, alih-alih memberikan implementasi di dalam
kurung kurawal, kita memakai titik koma. Setiap tipe yang mengimplementasikan
*trait* ini harus memberikan perilaku kustomnya sendiri untuk badan metode
tersebut. *Compiler* (kompilator) akan memastikan bahwa tipe apa pun yang
memiliki *trait* `Summary` akan memiliki metode `summarize` yang didefinisikan
dengan tanda tangan persis seperti ini.

Sebuah *trait* bisa memiliki banyak metode di badannya: tanda tangan
metodenya didaftarkan satu per baris, dan setiap baris diakhiri titik koma.

<a id="implementing-a-trait-on-a-type"></a>
### Mengimplementasikan Trait pada Suatu Tipe

Sekarang setelah kita mendefinisikan tanda tangan yang diinginkan untuk
metode-metode *trait* `Summary`, kita bisa mengimplementasikannya pada
tipe-tipe di agregator media kita. Listing 10-13 menunjukkan implementasi
*trait* `Summary` pada *struct* `NewsArticle` yang memakai judul berita,
penulis, dan lokasi untuk membuat nilai kembalian `summarize`. Untuk *struct*
`SocialPost`, kita mendefinisikan `summarize` sebagai nama pengguna yang
diikuti seluruh teks post, dengan asumsi bahwa konten post sudah dibatasi
menjadi 280 karakter.

<Listing number="10-13" file-name="src/lib.rs" caption="Mengimplementasikan trait `Summary` pada tipe `NewsArticle` dan `SocialPost`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

Mengimplementasikan *trait* pada sebuah tipe mirip dengan mengimplementasikan
metode biasa. Bedanya, setelah `impl`, kita menuliskan nama *trait* yang ingin
kita implementasikan, lalu memakai kata kunci `for`, dan kemudian menentukan
nama tipe yang ingin kita implementasikan *trait* tersebut. Di dalam blok
`impl`, kita menuliskan tanda tangan metode yang telah didefinisikan oleh
definisi *trait*. Alih-alih menambahkan titik koma setelah setiap tanda
tangan, kita memakai kurung kurawal dan mengisi badan metode dengan perilaku
spesifik yang kita inginkan dari metode-metode *trait* itu untuk tipe
tertentu.

Sekarang setelah library telah mengimplementasikan *trait* `Summary` pada
`NewsArticle` dan `SocialPost`, pengguna *crate* bisa memanggil metode-metode
*trait* itu pada instance `NewsArticle` dan `SocialPost` dengan cara yang sama
seperti kita memanggil metode biasa. Satu-satunya perbedaan adalah pengguna
harus membawa *trait* tersebut ke dalam *scope* (cakupan), bersama dengan
tipe-tipenya. Berikut contoh bagaimana sebuah *crate* binary bisa memakai
*crate* library `aggregator` kita:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

Kode ini mencetak `1 new post: horse_ebooks: of course, as you probably
already know, people`.

Crate-crate lain yang bergantung pada crate `aggregator` juga bisa membawa
trait `Summary` ke dalam scope untuk mengimplementasikan `Summary` pada
tipe-tipe mereka sendiri. Satu batasan yang perlu diperhatikan adalah kita
hanya bisa mengimplementasikan sebuah trait pada sebuah tipe jika trait
atau tipe tersebut, atau keduanya, bersifat lokal untuk crate kita. Sebagai
contoh, kita bisa mengimplementasikan trait pustaka standar seperti
`Display` pada tipe kustom seperti `SocialPost` sebagai bagian dari
fungsionalitas crate `aggregator` kita karena tipe `SocialPost` bersifat
lokal untuk crate `aggregator` kita. Kita juga bisa mengimplementasikan
`Summary` pada `Vec<T>` di crate `aggregator` kita karena trait `Summary`
bersifat lokal untuk crate `aggregator` kita.

Akan tetapi, kita tidak bisa mengimplementasikan trait eksternal pada tipe
eksternal. Sebagai contoh, kita tidak bisa mengimplementasikan trait
`Display` pada `Vec<T>` di dalam crate `aggregator` kita, karena `Display`
dan `Vec<T>` sama-sama didefinisikan di pustaka standar dan tidak bersifat
lokal untuk crate `aggregator` kita. Batasan ini adalah bagian dari
properti yang disebut *coherence* (koherensi), dan lebih spesifiknya
*orphan rule* (aturan anak yatim), dinamai demikian karena tipe induknya
tidak ada. Aturan ini memastikan bahwa kode orang lain tidak bisa merusak
kode Anda, dan sebaliknya. Tanpa aturan itu, dua crate bisa
mengimplementasikan trait yang sama untuk tipe yang sama, dan Rust tidak
akan tahu implementasi mana yang harus dipakai.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-implementations"></a>

### Memakai Implementasi Bawaan

Terkadang berguna untuk memiliki perilaku bawaan untuk sebagian atau semua
metode dalam sebuah trait, alih-alih mewajibkan implementasi untuk semua
metode pada setiap tipe. Kemudian, saat kita mengimplementasikan trait itu
pada tipe tertentu, kita bisa mempertahankan atau menimpa perilaku bawaan
setiap metode.

Di Listing 10-14, kita menentukan string bawaan untuk metode `summarize`
dari trait `Summary`, alih-alih hanya mendefinisikan tanda tangan
metodenya, seperti yang kita lakukan di Listing 10-12.

<Listing number="10-14" file-name="src/lib.rs" caption="Mendefinisikan trait `Summary` dengan implementasi bawaan untuk metode `summarize`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

Untuk memakai implementasi bawaan guna meringkas instance `NewsArticle`,
kita menentukan blok `impl` kosong dengan `impl Summary for NewsArticle {}`.

Meskipun kita tidak lagi mendefinisikan metode `summarize` pada
`NewsArticle` secara langsung, kita telah menyediakan implementasi bawaan
dan menentukan bahwa `NewsArticle` mengimplementasikan *trait* `Summary`.
Alhasil, kita tetap bisa memanggil metode `summarize` pada instance
`NewsArticle`, seperti ini:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

Kode ini mencetak `New article available! (Read more...)`.

Membuat implementasi bawaan tidak mengharuskan kita mengubah apa pun pada
implementasi `Summary` di `SocialPost` pada Listing 10-13. Alasannya,
sintaks untuk menimpa implementasi bawaan sama dengan sintaks untuk
mengimplementasikan metode *trait* yang tidak memiliki implementasi bawaan.

Implementasi bawaan bisa memanggil metode lain dalam *trait* yang sama,
bahkan jika metode lain itu tidak memiliki implementasi bawaan. Dengan cara
ini, sebuah *trait* bisa menyediakan banyak fungsionalitas yang berguna dan
hanya mewajibkan pengimplementasinya menentukan sebagian kecil darinya.
Sebagai contoh, kita bisa mendefinisikan *trait* `Summary` agar memiliki
metode `summarize_author` yang implementasinya diwajibkan, lalu
mendefinisikan metode `summarize` yang memiliki implementasi bawaan yang
memanggil metode `summarize_author`:

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

Untuk memakai versi `Summary` ini, kita hanya perlu mendefinisikan
`summarize_author` ketika kita mengimplementasikan *trait* itu pada sebuah
tipe:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

Setelah kita mendefinisikan `summarize_author`, kita bisa memanggil
`summarize` pada instance *struct* `SocialPost`, dan implementasi bawaan
`summarize` akan memanggil definisi `summarize_author` yang telah kita
sediakan. Karena kita telah mengimplementasikan `summarize_author`, *trait*
`Summary` telah memberi kita perilaku metode `summarize` tanpa mewajibkan
kita menulis kode lagi. Berikut tampilannya:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

Kode ini mencetak `1 new post: (Read more from @horse_ebooks...)`.

Perhatikan bahwa tidak mungkin memanggil implementasi bawaan dari
implementasi yang menimpa metode yang sama.

<!-- Old headings. Do not remove or links may break. -->

<a id="traits-as-parameters"></a>

### Memakai Trait sebagai Parameter

Sekarang setelah Anda tahu cara mendefinisikan dan mengimplementasikan
*trait*, kita bisa mengeksplorasi cara memakai *trait* untuk mendefinisikan
fungsi yang menerima banyak tipe berbeda. Kita akan memakai *trait* `Summary`
yang kita implementasikan pada tipe `NewsArticle` dan `SocialPost` di
Listing 10-13 untuk mendefinisikan fungsi `notify` yang memanggil metode
`summarize` pada parameter `item`-nya, yang bertipe tertentu yang
mengimplementasikan *trait* `Summary`. Untuk melakukannya, kita memakai
sintaks `impl Trait`, seperti ini:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

Alih-alih tipe konkret untuk parameter `item`, kita menentukan kata kunci
`impl` dan nama *trait*. Parameter ini menerima tipe apa pun yang
mengimplementasikan *trait* yang ditentukan. Di dalam badan `notify`, kita
bisa memanggil metode apa pun pada `item` yang berasal dari *trait* `Summary`,
seperti `summarize`. Kita bisa memanggil `notify` dan meneruskan instance
`NewsArticle` atau `SocialPost` mana pun. Kode yang memanggil fungsi itu
dengan tipe lain apa pun, seperti `String` atau `i32`, tidak akan
terkompilasi karena tipe-tipe tersebut tidak mengimplementasikan `Summary`.

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### Sintaks Trait Bound

Sintaks `impl Trait` berfungsi untuk kasus-kasus yang sederhana, tetapi
sebenarnya itu adalah gula sintaks untuk bentuk yang lebih panjang yang
dikenal sebagai *trait bound*; bentuknya terlihat seperti ini:

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

Bentuk yang lebih panjang ini setara dengan contoh di bagian sebelumnya
tetapi lebih panjang lebar. Kita menempatkan *trait bound* bersama deklarasi
parameter tipe generik setelah tanda titik dua dan di dalam kurung sudut.

Sintaks `impl Trait` praktis dan menghasilkan kode yang lebih ringkas dalam
kasus-kasus sederhana, sementara bentuk *trait bound* yang lebih lengkap bisa
mengekspresikan kompleksitas yang lebih besar dalam kasus lain. Sebagai
contoh, kita bisa memiliki dua parameter yang mengimplementasikan `Summary`.
Melakukannya dengan sintaks `impl Trait` terlihat seperti ini:

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

Memakai `impl Trait` cocok jika kita ingin fungsi ini mengizinkan `item1`
dan `item2` bertipe berbeda (selama kedua tipe mengimplementasikan
`Summary`). Namun, jika kita ingin memaksa kedua parameter bertipe sama,
kita harus memakai *trait bound*, seperti ini:

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

Tipe generik `T` yang ditentukan sebagai tipe parameter `item1` dan `item2`
membatasi fungsi itu sehingga tipe konkret dari nilai yang diteruskan
sebagai argumen untuk `item1` dan `item2` harus sama.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### Beberapa Trait Bound dengan Sintaks `+`

Kita juga bisa menentukan lebih dari satu *trait bound*. Katakanlah kita
ingin `notify` memakai pemformatan display selain `summarize` pada `item`:
kita menentukan dalam definisi `notify` bahwa `item` harus
mengimplementasikan `Display` dan `Summary`. Kita bisa melakukannya dengan
memakai sintaks `+`:

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

Sintaks `+` juga sah untuk *trait bound* pada tipe generik:

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

Dengan dua *trait bound* yang ditentukan, badan `notify` bisa memanggil
`summarize` dan memakai `{}` untuk memformat `item`.

#### Trait Bound yang Lebih Jelas dengan Klausa `where`

Memakai terlalu banyak *trait bound* memiliki kekurangannya sendiri. Setiap
generik memiliki *trait bound*-nya sendiri, jadi fungsi dengan banyak
parameter tipe generik bisa berisi banyak informasi *trait bound* di antara
nama fungsi dan daftar parameternya, sehingga tanda tangan fungsinya sulit
dibaca. Karena alasan ini, Rust memiliki sintaks alternatif untuk
menentukan *trait bound* di dalam klausa `where` setelah tanda tangan fungsi.
Jadi, alih-alih menulis ini:

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

kita bisa memakai klausa `where`, seperti ini:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

Tanda tangan fungsi ini tidak terlalu sesak: nama fungsi, daftar parameter,
dan tipe kembaliannya berdekatan, mirip fungsi tanpa banyak *trait bound*.

### Mengembalikan Tipe yang Mengimplementasikan Trait

Kita juga bisa memakai sintaks `impl Trait` di posisi nilai kembalian untuk
mengembalikan nilai bertipe tertentu yang mengimplementasikan sebuah *trait*,
seperti yang ditunjukkan di sini:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

Dengan memakai `impl Summary` untuk tipe kembalian, kita menentukan bahwa
fungsi `returns_summarizable` mengembalikan tipe tertentu yang
mengimplementasikan *trait* `Summary` tanpa menyebut nama tipe konkretnya.
Dalam kasus ini, `returns_summarizable` mengembalikan sebuah `SocialPost`,
tetapi kode yang memanggil fungsi ini tidak perlu mengetahuinya.

Kemampuan untuk menentukan tipe kembalian hanya berdasarkan *trait* yang
diimplementasikannya sangat berguna dalam konteks *closure* dan *iterator*,
yang kita bahas di Bab 13. *Closure* dan *iterator* membuat tipe yang hanya
diketahui *compiler* atau tipe yang sangat panjang untuk ditentukan. Sintaks
`impl Trait` memungkinkan Anda menentukan secara ringkas bahwa sebuah fungsi
mengembalikan tipe tertentu yang mengimplementasikan *trait* `Iterator` tanpa
perlu menuliskan tipe yang sangat panjang.

Akan tetapi, Anda hanya bisa memakai `impl Trait` jika Anda mengembalikan
satu tipe saja. Sebagai contoh, kode ini yang mengembalikan `NewsArticle`
atau `SocialPost` dengan tipe kembalian yang ditentukan sebagai `impl
Summary` tidak akan berfungsi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

Mengembalikan `NewsArticle` atau `SocialPost` tidak diizinkan karena
batasan-batasan seputar cara sintaks `impl Trait` diimplementasikan dalam
*compiler*. Kita akan membahas cara menulis fungsi dengan perilaku ini di
bagian [“Memakai *Trait Object* untuk Mengabstraksi Perilaku
Bersama”][*trait*-objects]<!-- ignore --> pada Bab 18.

### Memakai Trait Bound untuk Mengimplementasikan Metode secara Bersyarat

Dengan memakai *trait bound* bersama blok `impl` yang memakai parameter tipe
generik, kita bisa mengimplementasikan metode secara bersyarat untuk
tipe-tipe yang mengimplementasikan *trait* yang ditentukan. Sebagai contoh,
tipe `Pair<T>` di Listing 10-15 selalu mengimplementasikan fungsi `new`
untuk mengembalikan instance baru `Pair<T>` (ingat kembali dari bagian
[“Metode”][methods]<!-- ignore --> pada Bab 5 bahwa `Self` adalah alias
tipe untuk tipe dari blok `impl`, yang dalam kasus ini adalah `Pair<T>`).
Akan tetapi, di blok `impl` berikutnya, `Pair<T>` hanya mengimplementasikan
metode `cmp_display` jika tipe dalamnya `T` mengimplementasikan *trait*
`PartialOrd` yang memungkinkan perbandingan _dan_ *trait* `Display` yang
memungkinkan pencetakan.

<Listing number="10-15" file-name="src/lib.rs" caption="Mengimplementasikan metode secara bersyarat pada tipe generik tergantung pada trait bound">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Listing>

Kita juga bisa mengimplementasikan sebuah *trait* secara bersyarat untuk tipe
apa pun yang mengimplementasikan *trait* lain. Implementasi *trait* pada tipe
apa pun yang memenuhi *trait bound* disebut *blanket implementation*
(implementasi menyeluruh) dan dipakai secara ekstensif di pustaka standar
Rust. Sebagai contoh, pustaka standar mengimplementasikan *trait* `ToString`
pada tipe apa pun yang mengimplementasikan *trait* `Display`. Blok `impl` di
pustaka standar terlihat mirip dengan kode ini:

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

Karena pustaka standar memiliki *blanket implementation* ini, kita bisa
memanggil metode `to_string` yang didefinisikan oleh *trait* `ToString` pada
tipe apa pun yang mengimplementasikan *trait* `Display`. Sebagai contoh, kita
bisa mengubah integer menjadi nilai `String` yang bersesuaian seperti ini
karena integer mengimplementasikan `Display`:

```rust
let s = 3.to_string();
```

*Blanket implementation* muncul di dokumentasi *trait* pada bagian
“Implementors”.

*Trait* dan *trait bound* memungkinkan kita menulis kode yang memakai parameter
tipe generik untuk mengurangi duplikasi, tetapi juga memberi tahu *compiler*
bahwa kita ingin tipe generiknya memiliki perilaku tertentu. *Compiler*
kemudian bisa memakai informasi *trait bound* untuk memeriksa bahwa semua tipe
konkret yang dipakai bersama kode kita memberikan perilaku yang benar. Dalam
bahasa *dynamically typed* (bertipe dinamis), kita akan mendapatkan error di
*runtime* jika kita memanggil metode pada tipe yang tidak mendefinisikan
metode tersebut. Namun, Rust memindahkan error-error ini ke waktu kompilasi
sehingga kita dipaksa memperbaiki masalahnya bahkan sebelum kode kita bisa
berjalan. Selain itu, kita tidak perlu menulis kode yang memeriksa perilaku
di runtime, karena kita sudah memeriksanya di waktu kompilasi. Melakukannya
meningkatkan kinerja tanpa harus melepaskan fleksibilitas *generics*.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax
