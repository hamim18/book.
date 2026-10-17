<a id="methods"></a>
## Metode

Metode mirip dengan fungsi: kita mendeklarasikannya dengan keyword `fn` dan
sebuah nama, ia dapat memiliki parameter dan nilai kembalian, dan ia berisi
sejumlah kode yang dijalankan ketika metodenya dipanggil dari tempat lain.
Tidak seperti fungsi, metode didefinisikan di dalam konteks sebuah *struct*
(atau *enum* atau *trait object*, yang kita bahas masing-masing di
[Bab 6][enums]<!-- ignore --> dan [Bab 18][trait-objects]<!-- ignore -->), dan
parameter pertamanya selalu `self`, yang merepresentasikan instance *struct*
tempat metode itu dipanggil.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-methods"></a>

<a id="method-syntax"></a>
### Sintaks Metode

Mari kita ubah fungsi `area` yang memiliki instance `Rectangle` sebagai
parameter, dan sebagai gantinya membuat metode `area` yang didefinisikan pada
*struct* `Rectangle`, seperti yang ditunjukkan pada Listing 5-13.

<Listing number="5-13" file-name="src/main.rs" caption="Mendefinisikan metode `area` pada struct `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Listing>

Untuk mendefinisikan fungsi di dalam konteks `Rectangle`, kita memulai blok
`impl` (implementation) untuk `Rectangle`. Semua yang ada di dalam blok `impl`
ini akan terkait dengan tipe `Rectangle`. Lalu, kita memindahkan fungsi `area`
ke dalam kurung kurawal `impl` dan mengubah parameter pertama (dan pada kasus
ini, satu-satunya) menjadi `self` di tanda tangan dan di semua tempat dalam
badannya. Di `main`, tempat kita memanggil fungsi `area` dan meneruskan
`rect1` sebagai argumen, kita kini dapat memakai *method syntax* (sintaks
metode) untuk memanggil metode `area` pada instance `Rectangle` kita. Method
syntax diletakkan setelah instance: kita menambahkan titik yang diikuti nama
metode, tanda kurung, dan argumen apa pun.

Pada tanda tangan `area`, kita memakai `&self`, bukan `rectangle: &Rectangle`.
`&self` sebenarnya adalah singkatan dari `self: &Self`. Di dalam blok `impl`,
tipe `Self` adalah alias untuk tipe yang menjadi sasaran blok `impl` itu. Metode
harus memiliki parameter bernama `self` bertipe `Self` sebagai parameter
pertamanya, jadi Rust mengizinkan Anda menyingkatnya hanya dengan nama `self`
di posisi parameter pertama. Perhatikan bahwa kita tetap perlu memakai `&` di
depan singkatan `self` untuk menandakan bahwa metode ini meminjam instance
`Self`, sama seperti yang kita lakukan di `rectangle: &Rectangle`. Metode
dapat mengambil kepemilikan `self`, meminjam `self` secara *immutable*
(tidak dapat diubah) seperti yang kita lakukan di sini, atau meminjam `self`
secara *mutable* (dapat diubah), sama seperti parameter lainnya.

Kita memilih `&self` di sini dengan alasan yang sama ketika kita memakai
`&Rectangle` pada versi fungsinya: kita tidak ingin mengambil kepemilikan, dan
kita hanya ingin membaca data di dalam *struct*, bukan menulisnya. Jika kita
ingin mengubah instance tempat metode dipanggil sebagai bagian dari pekerjaan
metodenya, kita akan memakai `&mut self` sebagai parameter pertama. Memiliki
metode yang mengambil kepemilikan instance dengan hanya memakai `self` sebagai
parameter pertama jarang terjadi; teknik ini biasanya dipakai ketika metode
mengubah `self` menjadi sesuatu yang lain dan Anda ingin mencegah pemanggilnya
memakai instance aslinya setelah transformasi itu.

Alasan utama memakai metode alih-alih fungsi, selain menyediakan method
syntax dan tidak perlu mengulang tipe `self` di setiap tanda tangan metode,
adalah untuk pengorganisasian. Kita telah meletakkan semua hal yang dapat kita
lakukan dengan instance sebuah tipe dalam satu blok `impl`, alih-alih membuat
pengguna kode kita di masa depan mencari kemampuan `Rectangle` di berbagai
tempat pada pustaka yang kita sediakan.

Perhatikan bahwa kita dapat memilih untuk memberi metode nama yang sama dengan
salah satu *field* *struct*. Contohnya, kita dapat mendefinisikan metode pada
`Rectangle` yang juga bernama `width`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Listing>

Di sini, kita memilih untuk membuat metode `width` mengembalikan `true` jika
nilai pada *field* `width` instance lebih besar daripada `0` dan `false` jika
nilainya `0`: kita dapat memakai *field* di dalam metode dengan nama yang sama
untuk tujuan apa pun. Di `main`, ketika kita mengikuti `rect1.width` dengan
tanda kurung, Rust tahu bahwa yang kita maksud adalah metode `width`. Ketika
kita tidak memakai tanda kurung, Rust tahu bahwa yang kita maksud adalah *field*
`width`.

Sering kali, tetapi tidak selalu, ketika kita memberi sebuah metode nama yang
sama dengan sebuah *field*, kita ingin metode itu hanya mengembalikan nilai di
dalam *field* dan tidak melakukan hal lain. Metode seperti ini disebut *getter*,
dan Rust tidak mengimplementasikannya secara otomatis untuk *field* *struct*
seperti yang dilakukan beberapa bahasa lain. Getter berguna karena Anda dapat
membuat *field*-nya privat tetapi metodenya publik, sehingga memungkinkan akses
baca-saja ke *field* itu sebagai bagian dari API publik tipe tersebut. Kita akan
membahas apa itu publik dan privat serta cara menetapkan *field* atau metode
sebagai publik atau privat di [Bab 7][public]<!-- ignore -->.

<a id="wheres-the---operator"></a>
> ### Di Mana Operator `->`?
>
> Di C dan C++, dua operator berbeda dipakai untuk memanggil metode: Anda
> memakai `.` jika memanggil metode pada objeknya secara langsung dan `->`
> jika memanggil metode pada penunjuk ke objek itu dan perlu mendereferensi
> penunjuknya terlebih dahulu. Dengan kata lain, jika `object` adalah sebuah
> penunjuk, `object->something()` serupa dengan `(*object).something()`.
>
> Rust tidak memiliki padanan operator `->`; sebagai gantinya, Rust memiliki
> fitur yang disebut *automatic referencing and dereferencing* (referensi dan
> dereferensi otomatis). Memanggil metode adalah salah satu dari sedikit
> tempat di Rust yang memiliki perilaku ini.
>
> Begini cara kerjanya: ketika Anda memanggil metode dengan
> `object.something()`, Rust secara otomatis menambahkan `&`, `&mut`, atau `*`
> supaya `object` cocok dengan tanda tangan metodenya. Dengan kata lain,
> keduanya berikut ini sama:
>
> <!-- CAN'T EXTRACT SEE BUG https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust
> # #[derive(Debug,Copy,Clone)]
> # struct Point {
> #     x: f64,
> #     y: f64,
> # }
> #
> # impl Point {
> #    fn distance(&self, other: &Point) -> f64 {
> #        let x_squared = f64::powi(other.x - self.x, 2);
> #        let y_squared = f64::powi(other.y - self.y, 2);
> #
> #        f64::sqrt(x_squared + y_squared)
> #    }
> # }
> # let p1 = Point { x: 0.0, y: 0.0 };
> # let p2 = Point { x: 5.0, y: 6.5 };
> p1.distance(&p2);
> (&p1).distance(&p2);
> ```
>
> Yang pertama tampak jauh lebih bersih. Perilaku referensi otomatis ini
> bekerja karena metode memiliki *receiver* (penerima) yang jelas—tipe dari
> `self`. Dengan mengetahui penerima dan nama sebuah metode, Rust dapat
> memastikan secara definitif apakah metodenya membaca (`&self`), mengubah
> (`&mut self`), atau mengonsumsi (`self`). Fakta bahwa Rust membuat
> peminjaman menjadi implisit untuk penerima metode adalah bagian besar dari
> menjadikan *ownership* (kepemilikan) ergonomis dalam praktik.

### Metode dengan Parameter Lebih Banyak

Mari kita berlatih memakai metode dengan mengimplementasikan metode kedua
pada *struct* `Rectangle`. Kali ini kita ingin sebuah instance `Rectangle`
menerima instance `Rectangle` lain dan mengembalikan `true` jika `Rectangle`
kedua dapat muat sepenuhnya di dalam `self` (`Rectangle` pertama); jika tidak,
ia seharusnya mengembalikan `false`. Artinya, setelah kita mendefinisikan
metode `can_hold`, kita ingin dapat menulis program yang ditunjukkan pada
Listing 5-14.

<Listing number="5-14" file-name="src/main.rs" caption="Memakai metode `can_hold` yang belum ditulis">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Listing>

Keluaran yang diharapkan akan terlihat seperti berikut karena kedua dimensi
`rect2` lebih kecil daripada dimensi `rect1`, tetapi `rect3` lebih lebar
daripada `rect1`:

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

Kita tahu bahwa kita ingin mendefinisikan sebuah metode, jadi ia akan berada
di dalam blok `impl Rectangle`. Nama metodenya adalah `can_hold`, dan ia akan
menerima peminjaman *immutable* atas `Rectangle` lain sebagai parameter. Kita
bisa tahu tipe parameternya dengan melihat kode yang memanggil metodenya:
`rect1.can_hold(&rect2)` meneruskan `&rect2`, yang merupakan peminjaman
*immutable* atas `rect2`, sebuah instance `Rectangle`. Ini masuk akal karena
kita hanya perlu membaca `rect2` (bukan menulis, yang berarti kita akan butuh
peminjaman *mutable*), dan kita ingin `main` mempertahankan kepemilikan `rect2`
supaya kita dapat memakainya lagi setelah memanggil metode `can_hold`. Nilai
kembalian `can_hold` adalah Boolean, dan implementasinya akan memeriksa
apakah lebar dan tinggi `self` masing-masing lebih besar daripada lebar dan
tinggi `Rectangle` yang lain. Mari kita tambahkan metode `can_hold` yang baru
ke blok `impl` dari Listing 5-13, seperti yang ditunjukkan pada Listing 5-15.

<Listing number="5-15" file-name="src/main.rs" caption="Mengimplementasikan metode `can_hold` pada `Rectangle` yang menerima instance `Rectangle` lain sebagai parameter">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Listing>

Ketika kita menjalankan kode ini dengan fungsi `main` pada Listing 5-14,
kita akan mendapatkan keluaran yang kita inginkan. Metode dapat menerima
banyak parameter yang kita tambahkan ke tanda tangan setelah parameter
`self`, dan parameter-parameter itu bekerja persis seperti parameter pada
fungsi.

### Fungsi Asosiasi

Semua fungsi yang didefinisikan di dalam blok `impl` disebut *associated
function* (fungsi asosiasi) karena ia terkait dengan tipe yang disebutkan
setelah `impl`. Kita dapat mendefinisikan *associated function* yang tidak
memiliki `self` sebagai parameter pertamanya (dan dengan demikian bukan
metode) karena ia tidak memerlukan instance dari tipenya untuk bekerja. Kita
telah memakai satu fungsi seperti ini: fungsi `String::from` yang didefinisikan
pada tipe `String`.

*Associated function* yang bukan metode sering dipakai sebagai konstruktor yang
mengembalikan instance baru *struct*. Fungsi seperti ini sering disebut `new`,
tetapi `new` bukanlah nama istimewa dan tidak dibangun ke dalam bahasa.
Contohnya, kita dapat memilih untuk menyediakan *associated function* bernama
`square` yang memiliki satu parameter dimensi dan memakainya sebagai lebar
sekaligus tinggi, sehingga lebih mudah membuat `Rectangle` persegi daripada
harus menyebutkan nilai yang sama dua kali:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

Keyword `Self` pada tipe kembalian dan pada badan fungsi adalah alias untuk
tipe yang muncul setelah keyword `impl`, yang pada kasus ini adalah
`Rectangle`.

Untuk memanggil *associated function* ini, kita memakai sintaks `::` dengan nama
*struct*; `let sq = Rectangle::square(3);` adalah contohnya. Fungsi ini berada
dalam ruang nama *struct*: sintaks `::` dipakai untuk *associated function* maupun
ruang nama yang dibuat oleh *module* (modul). Kita akan membahas *module* di
[Bab 7][modules]<!-- ignore -->.

### Beberapa Blok `impl`

Setiap *struct* diizinkan memiliki beberapa blok `impl`. Contohnya, Listing 5-15
setara dengan kode yang ditunjukkan pada Listing 5-16, yang menempatkan setiap
metode di blok `impl`-nya sendiri.

<Listing number="5-16" caption="Menulis ulang Listing 5-15 memakai beberapa blok `impl`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Listing>

Tidak ada alasan untuk memisahkan metode-metode ini ke beberapa blok `impl` di
sini, tetapi ini adalah sintaks yang valid. Kita akan melihat kasus ketika
beberapa blok `impl` berguna di Bab 10, tempat kita membahas tipe generik dan
*trait*.

## Ringkasan

*Struct* memungkinkan Anda membuat tipe kustom yang bermakna bagi domain Anda.
Dengan memakai *struct*, Anda dapat menjaga bagian-bagian data yang berkaitan
tetap saling terhubung dan memberi nama pada setiap bagiannya untuk membuat
kode Anda jelas. Di dalam blok `impl`, Anda dapat mendefinisikan fungsi yang
terkait dengan tipe Anda, dan metode adalah salah satu jenis associated
function yang memungkinkan Anda menentukan perilaku yang dimiliki instance
*struct* Anda.

Tetapi *struct* bukanlah satu-satunya cara untuk membuat tipe kustom: mari kita
beralih ke fitur *enum* milik Rust untuk menambah alat lain ke kotak peralatan
Anda.

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
