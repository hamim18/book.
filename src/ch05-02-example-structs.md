## Contoh Program yang Memakai Struct

Untuk memahami kapan kita mungkin ingin memakai *struct*, mari kita tulis
sebuah program yang menghitung luas persegi panjang. Kita akan mulai dengan
memakai variable tunggal, lalu melakukan refactoring pada programnya sampai
kita memakai *struct*.

Mari kita buat proyek binary baru dengan Cargo bernama _rectangles_ yang akan
menerima lebar dan tinggi sebuah persegi panjang dalam piksel, lalu menghitung
luas persegi panjang itu. Listing 5-8 menunjukkan program singkat dengan salah
satu cara untuk melakukan hal itu di _src/main.rs_ proyek kita.

<Listing number="5-8" file-name="src/main.rs" caption="Menghitung luas persegi panjang yang ditentukan oleh variable width dan height yang terpisah">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

Sekarang, jalankan program ini dengan `cargo run`:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

Kode ini berhasil menghitung luas persegi panjang dengan memanggil fungsi
`area` beserta masing-masing dimensinya, tetapi kita bisa berbuat lebih banyak
untuk membuat kode ini jelas dan mudah dibaca.

Masalah pada kode ini tampak jelas pada tanda tangan `area`:

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

Fungsi `area` seharusnya menghitung luas satu persegi panjang, tetapi fungsi
yang kita tulis memiliki dua parameter, dan tidak jelas di bagian mana pun
program kita bahwa kedua parameter itu saling berkaitan. Akan lebih mudah
dibaca dan dikelola jika lebar dan tinggi dikelompokkan bersama. Kita telah
membahas satu cara untuk melakukannya di bagian [“Type
*Tuple*”][the-tuple-type]<!-- ignore --> pada Bab 3: dengan memakai *tuple*.

### Refactoring dengan Tuple

Listing 5-9 menunjukkan versi lain program kita yang memakai *tuple*.

<Listing number="5-9" file-name="src/main.rs" caption="Menentukan width dan height persegi panjang dengan tuple">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

Dari satu sisi, program ini lebih baik. *Tuple* memungkinkan kita menambahkan
sedikit struktur, dan kini kita hanya meneruskan satu argumen. Tetapi dari
sisi lain, versi ini kurang jelas: *tuple* tidak menamai elemen-elemennya, jadi
kita harus mengindeks bagian-bagian *tuple*, sehingga perhitungan kita menjadi
kurang gamblang.

Tertukarnya lebar dan tinggi tidak akan berpengaruh pada perhitungan luas,
tetapi jika kita ingin menggambar persegi panjang itu di layar, hal itu akan
berpengaruh! Kita harus ingat bahwa `width` adalah indeks *tuple* `0` dan
`height` adalah indeks *tuple* `1`. Ini akan lebih sulit lagi untuk dipahami dan
diingat oleh orang lain jika mereka memakai kode kita. Karena kita tidak
menyampaikan makna data kita di dalam kode, kini lebih mudah terjadi error.

<!-- Old headings. Do not remove or links may break. -->

<a id="refactoring-with-structs-adding-more-meaning"></a>

### Refactoring dengan Struct

Kita memakai *struct* untuk menambahkan makna dengan memberi label pada data.
Kita dapat mengubah *tuple* yang kita pakai menjadi *struct* dengan nama untuk
keseluruhannya sekaligus nama untuk bagian-bagiannya, seperti yang ditunjukkan
pada Listing 5-10.

<Listing number="5-10" file-name="src/main.rs" caption="Mendefinisikan struct `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

Di sini, kita telah mendefinisikan sebuah *struct* dan menamainya `Rectangle`.
Di dalam kurung kurawal, kita mendefinisikan *field*-nya sebagai `width` dan
`height`, yang keduanya typed `u32`. Lalu, di dalam `main`, kita membuat
sebuah instance `Rectangle` tertentu yang memiliki lebar `30` dan tinggi `50`.

Fungsi `area` kita kini didefinisikan dengan satu parameter, yang kita namai
`rectangle`, yang typenya adalah peminjaman *immutable* (tidak dapat diubah)
atas instance *struct* `Rectangle`. Seperti yang disebutkan di Bab 4, kita
ingin meminjam *struct* alih-alih mengambil *ownership* (kepemilikan). Dengan demikian, `main` mempertahankan
kepemilikannya dan dapat terus memakai `rect1`, itulah sebabnya kita memakai
`&` pada tanda tangan fungsi dan di tempat kita memanggil fungsinya.

Fungsi `area` mengakses *field* `width` dan `height` dari instance `Rectangle`
(perhatikan bahwa mengakses *field* dari instance *struct* yang dipinjam tidak
memindahkan nilai *field*-nya, itulah sebabnya Anda sering melihat *struct*
dipinjam). Tanda tangan fungsi `area` kita kini menyatakan dengan tepat apa
yang kita maksud: hitung luas `Rectangle`, dengan memakai *field* `width` dan
`height`-nya. Ini menyampaikan bahwa lebar dan tinggi saling berkaitan, dan
memberi nama deskriptif pada nilai-nilainya alih-alih memakai nilai indeks
*tuple* `0` dan `1`. Ini adalah kemenangan untuk kejelasan.

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-useful-functionality-with-derived-traits"></a>

### Menambah Fungsionalitas dengan Trait yang Diturunkan

Akan berguna jika kita dapat mencetak instance `Rectangle` selagi men-debug
program kita dan melihat nilai semua *field*-nya. Listing 5-11 mencoba memakai
[macro `println!`][println]<!-- ignore --> seperti yang telah kita pakai pada
bab-bab sebelumnya. Namun, ini tidak akan berhasil.

<Listing number="5-11" file-name="src/main.rs" caption="Mencoba mencetak instance `Rectangle`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</Listing>

Ketika kita mengompilasi kode ini, kita mendapatkan error dengan pesan inti
berikut:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

*Macro* `println!` dapat melakukan banyak jenis format, dan secara bawaan,
kurung kurawalnya memberi tahu `println!` untuk memakai format yang dikenal
sebagai `Display`: output yang ditujukan untuk konsumsi langsung oleh
pengguna akhir. Type-primitive type yang telah kita lihat sejauh ini
mengimplementasikan `Display` secara bawaan karena hanya ada satu cara untuk
menampilkan `1` atau primitive type lain kepada pengguna. Tetapi untuk *struct*,
cara `println!` memformat output-nya kurang jelas karena ada lebih banyak
kemungkinan tampilan: apakah Anda ingin koma atau tidak? Apakah Anda ingin
kurung kurawalnya dicetak? Apakah semua *field* harus ditampilkan? Karena
ambiguitas ini, Rust tidak mencoba menebak apa yang kita inginkan, dan *struct*
tidak memiliki implementasi `Display` yang disediakan untuk dipakai bersama
`println!` dan placeholder `{}`.

Jika kita terus membaca errornya, kita akan menemukan catatan yang membantu
ini:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

Mari kita coba! Pemanggilan *macro* `println!` kini akan terlihat seperti
`println!("rect1 is {rect1:?}");`. Meletakkan penanda `:?` di dalam kurung
kurawal memberi tahu `println!` bahwa kita ingin memakai format output bernama
`Debug`. *Trait* `Debug` memungkinkan kita mencetak *struct* dengan cara yang
berguna bagi pengembang sehingga kita dapat melihat nilainya selagi men-debug
kode kita.

Kompilasi kodenya dengan perubahan ini. Aduh! Kita masih mendapatkan error:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

Tetapi sekali lagi, *compiler* (kompilator) memberikan catatan yang
membantu:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

Rust _memang_ menyertakan fungsionalitas untuk mencetak informasi debug,
tetapi kita harus memilihnya secara eksplisit supaya fungsionalitas itu
tersedia untuk *struct* kita. Untuk melakukannya, kita menambahkan atribut luar
`#[derive(Debug)]` tepat sebelum definisi *struct*, seperti yang ditunjukkan
pada Listing 5-12.

<Listing number="5-12" file-name="src/main.rs" caption="Menambahkan atribut untuk menurunkan trait `Debug` dan mencetak instance `Rectangle` memakai format debug">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</Listing>

Sekarang ketika kita menjalankan programnya, kita tidak akan mendapatkan
error apa pun, dan kita akan melihat output berikut:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

Bagus! Keluarannya bukan yang terindah, tetapi ia menunjukkan nilai semua
*field* untuk instance ini, yang pasti membantu selama proses debug. Ketika kita
memiliki *struct* yang lebih besar, berguna untuk memiliki output yang sedikit
lebih mudah dibaca; pada kasus seperti itu, kita dapat memakai `{:#?}`
alih-alih `{:?}` di dalam string `println!`. Pada contoh ini, memakai gaya
`{:#?}` akan menghasilkan output berikut:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

Cara lain untuk mencetak sebuah nilai dengan format `Debug` adalah memakai
[macro `dbg!`][dbg]<!-- ignore -->, yang mengambil kepemilikan sebuah expression
(berbeda dengan `println!`, yang menerima sebuah *reference*), mencetak file dan
nomor baris tempat pemanggilan *macro* `dbg!` terjadi di kode Anda beserta nilai
hasil expression itu, dan mengembalikan kepemilikan nilainya.

> Catatan: Memanggil *macro* `dbg!` mencetak ke aliran konsol standard error
> (`stderr`), berbeda dengan `println!`, yang mencetak ke aliran konsol
> standard output (`stdout`). Kita akan membahas `stderr` dan `stdout` lebih
> lanjut di [bagian “Mengalihkan Error ke Standard Error” di Bab
> 12][err]<!-- ignore -->.

Berikut contoh ketika kita tertarik pada nilai yang ditetapkan ke *field*
`width`, sekaligus nilai keseluruhan *struct* di `rect1`:

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

Kita dapat meletakkan `dbg!` mengelilingi expression `30 * scale` dan, karena
`dbg!` mengembalikan kepemilikan nilai expressionnya, *field* `width` akan
mendapatkan nilai yang sama seolah-olah tidak ada pemanggilan `dbg!` di sana.
Kita tidak ingin `dbg!` mengambil kepemilikan `rect1`, jadi kita memakai
*reference* ke `rect1` pada pemanggilan berikutnya. Berikut tampilan output
contoh ini:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

Kita dapat melihat bahwa bagian pertama output berasal dari _src/main.rs_
baris 10, tempat kita men-debug expression `30 * scale`, dan nilai hasilnya
adalah `60` (format `Debug` yang diimplementasikan untuk integer hanya
mencetak nilainya). Pemanggilan `dbg!` pada baris 14 _src/main.rs_
mengeluarkan nilai `&rect1`, yang merupakan *struct* `Rectangle`. Output ini
memakai format `Debug` cantik milik type `Rectangle`. *Macro* `dbg!` bisa sangat
membantu ketika Anda mencoba memahami apa yang dilakukan kode Anda!

Selain *trait* `Debug`, Rust telah menyediakan sejumlah *trait* untuk kita pakai
bersama atribut `derive` yang dapat menambahkan perilaku berguna pada
type-custom type kita. *Trait*-trait itu dan perilakunya tercantum di
[Lampiran C][app-c]<!-- ignore -->. Kita akan membahas cara mengimplementasikan
*trait*-trait ini dengan perilaku kustom serta cara membuat *trait* Anda sendiri
di Bab 10. Ada juga banyak atribut selain `derive`; untuk informasi lebih
lanjut, lihat [bagian “Attributes” di Rust *Reference*][attributes].

Fungsi `area` kita sangat spesifik: ia hanya menghitung luas persegi panjang.
Akan membantu jika perilaku ini diikat lebih erat ke *struct* `Rectangle` kita
karena ia tidak akan bekerja dengan type lain mana pun. Mari kita lihat
bagaimana kita dapat terus melakukan refactoring pada kode ini dengan
mengubah fungsi `area` menjadi metode `area` yang didefinisikan pada type
`Rectangle` kita.

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: ../std/macro.println.html
[dbg]: ../std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: ../reference/attributes.html
