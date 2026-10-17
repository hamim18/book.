## Mendefinisikan dan Menginstansiasi Struct

Struct mirip dengan tuple, yang dibahas di bagian [“Tipe Tuple”][tuples]<!--
ignore -->, dalam hal keduanya menampung banyak nilai yang berkaitan. Seperti
*tuple*, bagian-bagian sebuah *struct* dapat bertipe berbeda. Tidak seperti *tuple*,
pada *struct* Anda memberi nama pada setiap bagian data sehingga jelas apa arti
nilai-nilai tersebut. Penambahan nama ini berarti *struct* lebih fleksibel
daripada *tuple*: Anda tidak harus mengandalkan urutan data untuk menentukan
atau mengakses nilai-nilai sebuah instance.

Untuk mendefinisikan *struct*, kita menuliskan keyword `struct` dan memberi nama
pada keseluruhan *struct*. Nama sebuah *struct* sebaiknya menggambarkan makna
bagian-bagian data yang dikelompokkan bersama. Lalu, di dalam kurung kurawal,
kita mendefinisikan nama dan tipe bagian-bagian data tersebut, yang kita sebut
*field* (medan). Contohnya, Listing 5-1 menunjukkan sebuah *struct* yang
menyimpan informasi tentang akun pengguna.

<Listing number="5-1" file-name="src/main.rs" caption="Definisi struct `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

Untuk memakai *struct* setelah kita mendefinisikannya, kita membuat sebuah
instance dari *struct* itu dengan menentukan nilai konkret untuk setiap *field*.
Kita membuat instance dengan menyebutkan nama *struct* lalu menambahkan kurung
kurawal berisi pasangan _`key: value`_, dengan key adalah nama-nama *field* dan
value adalah data yang ingin kita simpan di *field* tersebut. Kita tidak harus
menyebutkan *field* sesuai urutan ketika kita mendeklarasikannya di dalam
*struct*. Dengan kata lain, definisi *struct* adalah seperti templat umum untuk
tipenya, dan instance mengisi templat itu dengan data tertentu untuk membuat
nilai dari tipe tersebut. Contohnya, kita dapat mendeklarasikan seorang
pengguna tertentu seperti yang ditunjukkan pada Listing 5-2.

<Listing number="5-2" file-name="src/main.rs" caption="Membuat instance struct `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-02/src/main.rs:here}}
```

</Listing>

Untuk mengambil nilai tertentu dari sebuah *struct*, kita memakai notasi titik.
Contohnya, untuk mengakses alamat email pengguna ini, kita memakai
`user1.email`. Jika instance-nya *mutable* (dapat diubah), kita dapat mengubah
sebuah nilai dengan memakai notasi titik dan menetapkan nilai ke *field*
tertentu. Listing
5-3 menunjukkan cara mengubah nilai pada *field* `email` sebuah instance `User`
yang *mutable*.

<Listing number="5-3" file-name="src/main.rs" caption="Mengubah nilai pada field `email` sebuah instance `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-03/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa seluruh instance harus *mutable*; Rust tidak mengizinkan kita
menandai *field* tertentu saja sebagai *mutable*. Seperti ekspresi mana pun, kita
dapat menyusun instance baru *struct* sebagai ekspresi terakhir di badan fungsi
untuk mengembalikan instance baru itu secara implisit.

Listing 5-4 menunjukkan fungsi `build_user` yang mengembalikan instance `User`
dengan email dan username yang diberikan. *Field* `active` mendapatkan nilai
`true`, dan `sign_in_count` mendapatkan nilai `1`.

<Listing number="5-4" file-name="src/main.rs" caption="Fungsi `build_user` yang menerima email dan username lalu mengembalikan instance `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

Masuk akal untuk menamai parameter fungsi dengan nama yang sama seperti *field*
*struct*, tetapi harus mengulang nama *field* dan variabel `email` serta
`username` agak melelahkan. Jika structnya memiliki lebih banyak *field*,
mengulang setiap nama akan semakin menjengkelkan. Untungnya, ada singkatan
yang praktis!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>

### Memakai Field Init Shorthand

Karena nama parameter dan nama *field* *struct* persis sama pada Listing 5-4,
kita dapat memakai sintaks *field init shorthand* (singkatan inisialisasi
*field*) untuk menulis ulang `build_user` sehingga perilakunya persis sama
tetapi tanpa pengulangan `username` dan `email`, seperti yang ditunjukkan pada
Listing 5-5.

<Listing number="5-5" file-name="src/main.rs" caption="Fungsi `build_user` yang memakai field init shorthand karena parameter `username` dan `email` bernama sama dengan field struct">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

Di sini, kita membuat instance baru *struct* `User`, yang memiliki *field*
bernama `email`. Kita ingin menetapkan nilai *field* `email` menjadi nilai pada
parameter `email` fungsi `build_user`. Karena *field* `email` dan parameter
`email` bernama sama, kita cukup menulis `email` alih-alih `email: email`.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-instances-from-other-instances-with-struct-update-syntax"></a>

### Membuat Instance dengan Sintaks Update Struct

Sering kali berguna untuk membuat instance baru sebuah *struct* yang menyertakan
sebagian besar nilai dari instance lain bertipe sama, tetapi mengubah sebagian
di antaranya. Anda dapat melakukannya memakai sintaks update *struct*.

Pertama, pada Listing 5-6 kita menunjukkan cara membuat instance `User` baru
di `user2` dengan cara biasa, tanpa sintaks update. Kita menetapkan nilai baru
untuk `email` tetapi selain itu memakai nilai yang sama dari `user1` yang kita
buat pada Listing 5-2.

<Listing number="5-6" file-name="src/main.rs" caption="Membuat instance `User` baru memakai semua nilai dari `user1` kecuali satu">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-06/src/main.rs:here}}
```

</Listing>

Dengan memakai sintaks update *struct*, kita dapat mencapai efek yang sama
dengan kode yang lebih sedikit, seperti yang ditunjukkan pada Listing 5-7.
Sintaks `..` menentukan bahwa *field*-field tersisa yang tidak ditetapkan secara
eksplisit sebaiknya memiliki nilai yang sama seperti *field* pada instance yang
diberikan.

<Listing number="5-7" file-name="src/main.rs" caption="Memakai sintaks update struct untuk menetapkan nilai `email` baru bagi instance `User` tetapi memakai nilai-nilai lainnya dari `user1`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

Kode pada Listing 5-7 juga membuat sebuah instance di `user2` yang memiliki
nilai berbeda untuk `email` tetapi memiliki nilai yang sama untuk *field*
`username`, `active`, dan `sign_in_count` dari `user1`. `..user1` harus
diletakkan terakhir untuk menentukan bahwa *field*-field tersisa sebaiknya
mengambil nilainya dari *field* yang bersesuaian di `user1`, tetapi kita dapat
memilih untuk menentukan nilai *field* sebanyak yang kita mau dengan urutan apa
pun, terlepas dari urutan *field* pada definisi *struct*.

Perhatikan bahwa sintaks update *struct* memakai `=` seperti sebuah penetapan;
ini karena ia memindahkan datanya, seperti yang kita lihat di bagian
[“Variabel dan Data yang Berinteraksi dengan
Move”][move]<!-- ignore -->. Pada contoh ini, kita tidak dapat lagi memakai
`user1` setelah membuat `user2` karena `String` pada *field* `username` milik
`user1` telah dipindahkan ke `user2`. Seandainya kita memberi `user2` nilai
`String` baru untuk `email` maupun `username`, dan dengan demikian hanya
memakai nilai `active` dan `sign_in_count` dari `user1`, maka `user1` akan
tetap valid setelah `user2` dibuat. Baik `active` maupun `sign_in_count`
adalah tipe yang mengimplementasikan *trait* `Copy`, jadi perilaku yang kita
bahas di bagian [“Data yang Hanya Ada di Stack: Copy”][copy]<!-- ignore -->
akan berlaku. Dalam contoh ini kita juga masih dapat memakai `user1.email`,
karena nilainya tidak dipindahkan keluar dari `user1`.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-tuple-structs-without-named-fields-to-create-different-types"></a>

<a id="creating-different-types-with-tuple-structs"></a>
### Membuat Tipe Berbeda dengan Tuple Struct

Rust juga mendukung *struct* yang tampak mirip *tuple*, yang disebut *tuple
struct* (*struct* *tuple*). *Tuple struct* memiliki makna tambahan yang diberikan
oleh nama *struct*-nya, tetapi tidak memiliki nama yang terkait dengan
*field*-fieldnya; alih-alih, ia hanya memiliki tipe dari *field*-fieldnya. *Tuple*
*struct* berguna ketika Anda ingin memberi nama pada keseluruhan *tuple* dan
menjadikan *tuple* itu tipe yang berbeda dari *tuple* lain, dan ketika menamai
setiap *field* seperti pada *struct* biasa akan terasa bertele-tele atau
berlebihan.

Untuk mendefinisikan *tuple struct*, mulailah dengan keyword `struct` dan nama
*struct*, yang diikuti tipe-tipe di dalam *tuple*. Contohnya, di sini kita
mendefinisikan dan memakai dua *tuple struct* bernama `Color` dan `Point`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-01-tuple-structs/src/main.rs}}
```

</Listing>

Perhatikan bahwa nilai `black` dan `origin` bertipe berbeda karena keduanya
adalah instance dari *tuple struct* yang berbeda. Setiap *struct* yang Anda
definisikan adalah tipenya sendiri, meskipun *field*-field di dalam *struct* itu
mungkin bertipe sama. Contohnya, fungsi yang menerima parameter bertipe
`Color` tidak dapat menerima `Point` sebagai argumen, meskipun kedua tipe itu
tersusun dari tiga nilai `i32`. Selain itu, instance *tuple struct* mirip dengan
*tuple* dalam hal Anda dapat mendestrukturisasinya menjadi bagian-bagian
individualnya, dan Anda dapat memakai `.` yang diikuti indeks untuk mengakses
sebuah nilai individual. Tidak seperti *tuple*, *tuple struct* mengharuskan Anda
menyebutkan tipe structnya ketika mendestrukturisasi. Contohnya, kita akan
menulis `let Point(x, y, z) = origin;` untuk mendestrukturisasi nilai-nilai di
titik `origin` menjadi variabel bernama `x`, `y`, dan `z`.

<!-- Old headings. Do not remove or links may break. -->

<a id="unit-like-structs-without-any-fields"></a>

### Mendefinisikan Struct Mirip Unit

Anda juga dapat mendefinisikan *struct* yang tidak memiliki *field* apa pun!
*Struct* ini disebut *unit-like struct* (*struct* mirip unit) karena perilakunya
mirip `()`, tipe unit yang kita sebutkan di bagian [“Tipe
Tuple”][tuples]<!-- ignore -->. Unit-like struct dapat berguna ketika Anda
perlu mengimplementasikan sebuah *trait* pada suatu tipe tetapi tidak memiliki
data apa pun yang ingin Anda simpan di dalam tipe itu sendiri. Kita akan
membahas *trait* di Bab 10. Berikut contoh mendeklarasikan dan menginstansiasi
unit *struct* bernama `AlwaysEqual`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-04-unit-like-structs/src/main.rs}}
```

</Listing>

Untuk mendefinisikan `AlwaysEqual`, kita memakai keyword `struct`, nama yang
kita inginkan, lalu titik koma. Tidak perlu kurung kurawal atau tanda kurung!
Lalu, kita bisa mendapatkan instance `AlwaysEqual` di variabel `subject`
dengan cara yang serupa: memakai nama yang kita definisikan, tanpa kurung
kurawal atau tanda kurung apa pun. Bayangkan nanti kita akan
mengimplementasikan perilaku untuk tipe ini sedemikian rupa sehingga setiap
instance `AlwaysEqual` selalu sama dengan setiap instance dari tipe lain mana
pun, mungkin untuk mendapatkan hasil yang diketahui demi keperluan pengujian.
Kita tidak memerlukan data apa pun untuk mengimplementasikan perilaku itu!
Anda akan melihat di Bab 10 cara mendefinisikan *trait* dan
mengimplementasikannya pada tipe mana pun, termasuk *unit-like struct*.

> ### Ownership pada Data Struct
>
> Pada definisi *struct* `User` di Listing 5-1, kita memakai tipe `String` yang
> dimiliki alih-alih tipe string *slice* `&str`. Ini adalah pilihan yang
> disengaja karena kita ingin setiap instance *struct* ini memiliki semua
> datanya dan data itu tetap valid selama keseluruhan *struct* valid.
>
> *Struct* juga dimungkinkan untuk menyimpan *reference* (referensi) ke data
> yang dimiliki oleh sesuatu yang lain, tetapi untuk melakukannya diperlukan
> *lifetime* (masa hidup), fitur Rust yang akan kita bahas di Bab 10. *Lifetime*
> memastikan bahwa data yang direferensikan oleh sebuah *struct* tetap valid
> selama *struct* itu masih ada. Katakanlah Anda mencoba menyimpan sebuah
> *reference* di dalam *struct* tanpa menyebutkan *lifetime*, seperti berikut ini di
> *src/main.rs*; ini tidak akan berhasil:
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> *struct* User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> *Compiler* (kompilator) akan mengeluh bahwa ia membutuhkan penanda *lifetime*:
>
> ```console
> $ cargo run
>    Compiling *structs* v0.1.0 (file:///projects/structs)
> error[E0106]: missing *lifetime* specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named *lifetime* parameter
>   |
> help: consider introducing a named *lifetime* parameter
>   |
> 1 ~ *struct* User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing *lifetime* specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named *lifetime* parameter
>   |
> help: consider introducing a named *lifetime* parameter
>   |
> 1 ~ *struct* User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "*structs*") due to 2 previous errors
> ```
>
> Di Bab 10, kita akan membahas cara memperbaiki galat-galat ini supaya Anda
> dapat menyimpan *reference* di dalam *struct*, tetapi untuk sekarang, kita akan
> memperbaiki galat seperti ini dengan memakai tipe yang dimiliki seperti
> `String`, bukan *reference* seperti `&str`.

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-move
[copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
