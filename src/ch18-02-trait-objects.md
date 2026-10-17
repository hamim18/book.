<!-- Old headings. Do not remove or links may break. -->

<a id="using-trait-objects-that-allow-for-values-of-different-types"></a>

<a id="using-trait-objects-to-abstract-over-shared-behavior"></a>
## Memakai Trait Object untuk Mengabstraksi Perilaku Bersama

Di Bab 8, kami menyebutkan bahwa salah satu keterbatasan vektor adalah mereka
hanya bisa menyimpan elemen dari satu tipe. Kita membuat jalan keluar di
Listing 8-9 dengan mendefinisikan *enum* `SpreadsheetCell` yang memiliki varian
untuk menampung integer, float, dan teks. Ini berarti kita bisa menyimpan
berbagai tipe data di setiap sel dan tetap memiliki vektor yang
merepresentasikan satu baris sel. Ini solusi yang sepenuhnya bagus ketika
item-item yang saling dapat dipertukarkan adalah sekumpulan tipe tetap yang
kita ketahui saat kode kita dikompilasi.

Akan tetapi, terkadang kita ingin pengguna library kita bisa memperluas
kumpulan tipe yang valid dalam situasi tertentu. Untuk menunjukkan cara kita
mencapainya, kita akan membuat contoh alat antarmuka pengguna grafis (GUI)
yang mengiterasi daftar item, memanggil metode `draw` pada setiap item untuk
menggambarnya ke layar—teknik yang umum untuk alat GUI. Kita akan membuat
*crate* library bernama `gui` yang memuat struktur library GUI. *Crate* ini
mungkin menyertakan beberapa tipe untuk dipakai orang, seperti `Button` atau
`TextField`. Selain itu, pengguna `gui` akan ingin membuat tipe mereka
sendiri yang bisa digambar: misalnya, satu pemrogram mungkin menambahkan
`Image`, dan pemrogram lain mungkin menambahkan `SelectBox`.

Pada saat menulis library itu, kita tidak bisa mengetahui dan mendefinisikan
semua tipe yang mungkin ingin dibuat pemrogram lain. Tetapi kita tahu bahwa
`gui` perlu melacak banyak nilai dari tipe yang berbeda, dan perlu memanggil
metode `draw` pada setiap nilai yang bertipe berbeda ini. `gui` tidak perlu
tahu persis apa yang akan terjadi ketika kita memanggil metode `draw`, cukup
bahwa nilai itu akan memiliki metode tersebut tersedia untuk kita panggil.

Untuk melakukannya di bahasa dengan *inheritance*, kita mungkin mendefinisikan
kelas bernama `Component` yang memiliki metode bernama `draw`. Kelas-kelas
lain, seperti `Button`, `Image`, dan `SelectBox`, akan mewarisi dari
`Component` dan dengan demikian mewarisi metode `draw`. Mereka masing-masing
bisa menimpa metode `draw` untuk mendefinisikan perilaku kustomnya, tetapi
framework itu bisa memperlakukan semua tipe seolah-olah mereka adalah
instance `Component` dan memanggil `draw` pada mereka. Namun, karena Rust
tidak memiliki *inheritance*, kita butuh cara lain untuk menstrukturkan
library `gui` agar pengguna bisa membuat tipe baru yang kompatibel dengan
library itu.

### Mendefinisikan Trait untuk Perilaku Bersama

Untuk mengimplementasikan perilaku yang kita inginkan pada `gui`, kita akan
mendefinisikan *trait* bernama `Draw` yang memiliki satu metode bernama `draw`.
Kemudian, kita bisa mendefinisikan vektor yang menerima *trait object*. Sebuah
_trait object_ (objek *trait*) menunjuk ke instance tipe yang
mengimplementasikan *trait* yang kita tentukan sekaligus ke tabel yang dipakai
untuk mencari metode *trait* pada tipe itu saat runtime. Kita membuat *trait*
object dengan menentukan semacam *pointer*, seperti *reference* atau smart
*pointer* `Box<T>`, lalu kata kunci `dyn`, dan kemudian *trait* yang relevan.
(Kita akan membahas alasan *trait object* harus memakai *pointer* di [“Tipe
Berukuran Dinamis dan Trait `Sized`”][dynamically-sized]<!-- ignore --> di Bab
20.) Kita bisa memakai *trait object* sebagai pengganti tipe generik atau tipe
konkret. Di mana pun kita memakai *trait object*, sistem tipe Rust akan
memastikan pada waktu kompilasi bahwa nilai apa pun yang dipakai dalam konteks
itu akan mengimplementasikan *trait* dari *trait object* tersebut. Akibatnya,
kita tidak perlu mengetahui semua tipe yang mungkin pada waktu kompilasi.

Kami telah menyebutkan bahwa, di Rust, kita menahan diri untuk tidak menyebut
*struct* dan *enum* sebagai “objek” untuk membedakannya dari objek bahasa lain.
Pada *struct* atau *enum*, data di *field* *struct* dan perilaku di blok `impl`
terpisah, sedangkan di bahasa lain, data dan perilaku yang digabung menjadi
satu konsep sering diberi label objek. *Trait object* berbeda dari objek di
bahasa lain karena kita tidak bisa menambahkan data ke *trait object*. *Trait*
object tidak seumumnya berguna seperti objek di bahasa lain: tujuan spesifik
mereka adalah memungkinkan abstraksi lintas perilaku bersama.

Listing 18-3 menunjukkan cara mendefinisikan *trait* bernama `Draw` dengan satu
metode bernama `draw`.

<Listing number="18-3" file-name="src/lib.rs" caption="Definisi trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-03/src/lib.rs}}
```

</Listing>

Sintaks ini seharusnya terasa familier dari pembahasan kita tentang cara
mendefinisikan *trait* di Bab 10. Berikutnya ada beberapa sintaks baru: Listing
18-4 mendefinisikan *struct* bernama `Screen` yang menampung vektor bernama
`components`. Vektor ini bertipe `Box<dyn Draw>`, yang merupakan *trait*
object; ia adalah pengganti untuk tipe apa pun di dalam `Box` yang
mengimplementasikan *trait* `Draw`.

<Listing number="18-4" file-name="src/lib.rs" caption="Definisi struct `Screen` dengan field `components` yang menampung vektor trait object yang mengimplementasikan trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-04/src/lib.rs:here}}
```

</Listing>

Pada *struct* `Screen`, kita akan mendefinisikan metode bernama `run` yang akan
memanggil metode `draw` pada setiap `components`-nya, seperti yang
ditunjukkan di Listing 18-5.

<Listing number="18-5" file-name="src/lib.rs" caption="Metode `run` pada `Screen` yang memanggil metode `draw` pada setiap component">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-05/src/lib.rs:here}}
```

</Listing>

Ini bekerja berbeda dari mendefinisikan *struct* yang memakai parameter tipe
generik dengan *trait bound*. Parameter tipe generik hanya bisa digantikan
dengan satu tipe konkret pada satu waktu, sedangkan *trait object* memungkinkan
beberapa tipe konkret mengisi peran *trait object* itu saat runtime. Contohnya,
kita bisa saja mendefinisikan *struct* `Screen` menggunakan tipe generik dan
*trait bound*, seperti di Listing 18-6.

<Listing number="18-6" file-name="src/lib.rs" caption="Implementasi alternatif struct `Screen` dan metode `run`-nya menggunakan generics dan trait bound">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-06/src/lib.rs:here}}
```

</Listing>

Ini membatasi kita pada instance `Screen` yang memiliki daftar component yang
semuanya bertipe `Button` atau semuanya bertipe `TextField`. Jika Anda hanya
akan memiliki koleksi yang homogen, memakai *generics* dan *trait bound* lebih
disukai karena definisinya akan dimonomorfisasi pada waktu kompilasi untuk
memakai tipe-tipe konkretnya.

Di sisi lain, dengan metode yang memakai *trait object*, satu instance `Screen`
bisa menampung `Vec<T>` yang berisi `Box<Button>` sekaligus `Box<TextField>`.
Mari kita lihat cara kerjanya, lalu kita akan membahas implikasi performa
runtime-nya.

### Mengimplementasikan Trait

Sekarang kita akan menambahkan beberapa tipe yang mengimplementasikan *trait*
`Draw`. Kita akan menyediakan tipe `Button`. Sekali lagi, benar-benar
mengimplementasikan library GUI berada di luar cakupan buku ini, jadi metode
`draw` tidak akan memiliki implementasi yang berguna di badannya. Untuk
membayangkan seperti apa implementasinya, *struct* `Button` mungkin memiliki
*field* untuk `width`, `height`, dan `label`, seperti yang ditunjukkan di
Listing 18-7.

<Listing number="18-7" file-name="src/lib.rs" caption="Struct `Button` yang mengimplementasikan trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-07/src/lib.rs:here}}
```

</Listing>

*Field* `width`, `height`, dan `label` pada `Button` akan berbeda dari *field*
pada component lain; contohnya, tipe `TextField` mungkin memiliki
*field*-field yang sama itu plus *field* `placeholder`. Setiap tipe yang ingin
kita gambar di layar akan mengimplementasikan *trait* `Draw` tetapi memakai kode
yang berbeda di metode `draw` untuk mendefinisikan cara menggambar tipe
tertentu itu, seperti yang dilakukan `Button` di sini (tanpa kode GUI
sebenarnya, seperti disebutkan). Tipe `Button`, misalnya, mungkin memiliki
blok `impl` tambahan berisi metode-metode yang berkaitan dengan apa yang
terjadi ketika pengguna mengeklik tombol itu. Metode-metode semacam ini tidak
akan berlaku untuk tipe seperti `TextField`.

Jika seseorang yang memakai library kita memutuskan untuk mengimplementasikan
*struct* `SelectBox` yang memiliki *field* `width`, `height`, dan `options`,
mereka juga akan mengimplementasikan *trait* `Draw` pada tipe `SelectBox`,
seperti yang ditunjukkan di Listing 18-8.

<Listing number="18-8" file-name="src/main.rs" caption="Crate lain yang memakai `gui` dan mengimplementasikan trait `Draw` pada struct `SelectBox`">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-08/src/main.rs:here}}
```

</Listing>

Pengguna library kita sekarang bisa menulis fungsi `main` mereka untuk
membuat instance `Screen`. Ke instance `Screen` itu, mereka bisa menambahkan
`SelectBox` dan `Button` dengan menaruh masing-masing di dalam `Box<T>` untuk
menjadi *trait object*. Mereka kemudian bisa memanggil metode `run` pada
instance `Screen`, yang akan memanggil `draw` pada setiap component. Listing
18-9 menunjukkan implementasi ini.

<Listing number="18-9" file-name="src/main.rs" caption="Memakai trait object untuk menyimpan nilai dari tipe berbeda yang mengimplementasikan trait yang sama">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-09/src/main.rs:here}}
```

</Listing>

Ketika kami menulis library itu, kami tidak tahu bahwa seseorang mungkin
menambahkan tipe `SelectBox`, tetapi implementasi `Screen` kami bisa
mengoperasikan tipe baru itu dan menggambarnya karena `SelectBox`
mengimplementasikan *trait* `Draw`, yang berarti ia mengimplementasikan metode
`draw`.

Konsep ini—hanya peduli pada pesan yang direspons sebuah nilai alih-alih tipe
konkret nilai itu—mirip dengan konsep _duck typing_ (pengetikan bebek) di
bahasa bertipe dinamis: jika ia berjalan seperti bebek dan berkuek seperti
bebek, maka ia pasti bebek! Di implementasi `run` pada `Screen` di Listing
18-5, `run` tidak perlu tahu apa tipe konkret setiap component. Ia tidak
mengecek apakah sebuah component adalah instance `Button` atau `SelectBox`,
ia hanya memanggil metode `draw` pada component itu. Dengan menentukan
`Box<dyn Draw>` sebagai tipe nilai di vektor `components`, kita telah
mendefinisikan `Screen` sebagai memerlukan nilai-nilai yang bisa kita panggil
metode `draw`-nya.

Keuntungan memakai *trait object* dan sistem tipe Rust untuk menulis kode yang
mirip dengan kode pemakai *duck typing* adalah kita tidak pernah harus mengecek
apakah sebuah nilai mengimplementasikan metode tertentu saat runtime atau
khawatir mendapat galat jika sebuah nilai tidak mengimplementasikan sebuah
metode tetapi tetap kita panggil. Rust tidak akan mengompilasi kode kita jika
nilai-nilai itu tidak mengimplementasikan *trait* yang dibutuhkan *trait object*
tersebut.

Contohnya, Listing 18-10 menunjukkan apa yang terjadi jika kita mencoba
membuat `Screen` dengan `String` sebagai component.

<Listing number="18-10" file-name="src/main.rs" caption="Mencoba memakai tipe yang tidak mengimplementasikan trait dari trait object itu">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-10/src/main.rs}}
```

</Listing>

Kita akan mendapat galat ini karena `String` tidak mengimplementasikan *trait*
`Draw`:

```console
{{#include ../listings/ch18-oop/listing-18-10/output.txt}}
```

Galat ini memberi tahu kita bahwa entah kita meneruskan sesuatu ke `Screen`
yang tidak kita maksudkan untuk diteruskan sehingga seharusnya meneruskan tipe
yang berbeda, atau kita harus mengimplementasikan `Draw` pada `String` supaya
`Screen` bisa memanggil `draw` padanya.

<!-- Old headings. Do not remove or links may break. -->

<a id="trait-objects-perform-dynamic-dispatch"></a>

### Melakukan Dynamic Dispatch

Ingat kembali di [“Kinerja Kode yang Memakai
Generics”][performance-of-code-using-generics]<!-- ignore --> di Bab 10,
pembahasan kita tentang proses monomorfisasi yang dilakukan kompilator pada
*generics*: kompilator menghasilkan implementasi nongenerik dari fungsi dan
metode untuk setiap tipe konkret yang kita pakai sebagai pengganti parameter
tipe generik. Kode yang dihasilkan monomorfisasi melakukan _static dispatch_
(dispatch statis), yaitu ketika kompilator tahu metode apa yang Anda panggil
pada waktu kompilasi. Ini berlawanan dengan _dynamic dispatch_ (dispatch
dinamis), yaitu ketika kompilator tidak bisa mengetahui pada waktu kompilasi
metode mana yang Anda panggil. Pada kasus *dynamic dispatch*, kompilator
menghasilkan kode yang pada saat runtime akan tahu metode mana yang harus
dipanggil.

Ketika kita memakai *trait object*, Rust harus memakai *dynamic dispatch*.
Kompilator tidak mengetahui semua tipe yang mungkin dipakai dengan kode yang
memakai *trait object*, jadi ia tidak tahu metode mana yang diimplementasikan
pada tipe mana yang harus dipanggil. Sebagai gantinya, pada saat runtime, Rust
memakai *pointer* di dalam *trait object* untuk mengetahui metode mana yang harus
dipanggil. Pencarian ini menimbulkan biaya runtime yang tidak terjadi pada
*static dispatch*. *Dynamic dispatch* juga mencegah kompilator memilih untuk
meng-inline kode sebuah metode, yang pada gilirannya mencegah beberapa
optimasi, dan Rust punya beberapa aturan tentang di mana Anda boleh dan tidak
boleh memakai *dynamic dispatch*, yang disebut _dyn compatibility_
(kompatibilitas dyn). Aturan-aturan itu berada di luar cakupan pembahasan ini,
tetapi Anda bisa membaca lebih lanjut [di reference][dyn-compatibility]<!-- ignore -->.
Akan tetapi, kita memang mendapat fleksibilitas tambahan pada kode yang kita
tulis di Listing 18-5 dan bisa dukung di Listing 18-9, jadi itu kompromi yang
perlu dipertimbangkan.

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility
