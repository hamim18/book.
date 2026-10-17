## Mendefinisikan Enum

Sementara struct memberi Anda cara untuk mengelompokkan field dan data yang
berkaitan, seperti `Rectangle` dengan `width` dan `height`-nya, enum memberi
Anda cara untuk menyatakan bahwa sebuah nilai adalah salah satu dari
sekumpulan nilai yang mungkin. Contohnya, kita mungkin ingin menyatakan bahwa
`Rectangle` adalah salah satu dari sekumpulan bentuk yang mungkin, yang juga
mencakup `Circle` dan `Triangle`. Untuk melakukannya, Rust mengizinkan kita
mengkodekan kemungkinan-kemungkinan ini sebagai sebuah enum.

Mari kita lihat situasi yang mungkin ingin kita nyatakan dalam kode dan lihat
mengapa enum berguna serta lebih tepat daripada struct pada kasus ini.
Katakanlah kita perlu mengolah alamat IP. Saat ini, ada dua standar utama
yang dipakai untuk alamat IP: versi empat dan versi enam. Karena hanya itulah
kemungkinan alamat IP yang akan ditemui program kita, kita dapat *enumerate*
(menyebutkan satu per satu) semua *variant* (varian) yang mungkin, dan dari
situlah nama enumerasi berasal.

Alamat IP mana pun dapat berupa alamat versi empat atau versi enam, tetapi
tidak keduanya sekaligus. Sifat alamat IP itu menjadikan struktur data enum
tepat untuk dipakai, karena sebuah nilai enum hanya dapat menjadi salah satu
variannya. Alamat versi empat dan versi enam pada dasarnya tetap alamat IP,
jadi keduanya seharusnya diperlakukan sebagai tipe yang sama ketika kode
menangani situasi yang berlaku untuk alamat IP jenis apa pun.

Kita dapat menyatakan konsep ini dalam kode dengan mendefinisikan enumerasi
`IpAddrKind` dan mendaftarkan jenis-jenis yang mungkin dimiliki alamat IP,
`V4` dan `V6`. Inilah *variant*-*variant* enum tersebut:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

`IpAddrKind` kini adalah tipe data kustom yang dapat kita pakai di bagian lain
kode kita.

<a id="enum-values"></a>
### Nilai Enum

Kita dapat membuat instance dari masing-masing dua *variant* `IpAddrKind`
seperti ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

Perhatikan bahwa *variant*-*variant* enum berada dalam ruang nama di bawah
pengenalnya, dan kita memakai titik dua ganda untuk memisahkan keduanya. Ini
berguna karena kini nilai `IpAddrKind::V4` dan `IpAddrKind::V6` sama-sama
bertipe `IpAddrKind`. Kita kemudian dapat, misalnya, mendefinisikan sebuah
fungsi yang menerima `IpAddrKind` apa pun:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

Dan kita dapat memanggil fungsi ini dengan *variant* mana pun:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

Memakai enum memiliki lebih banyak lagi keunggulan. Kalau dipikirkan lebih
jauh tentang tipe alamat IP kita, saat ini kita belum punya cara untuk
menyimpan _data_ alamat IP yang sesungguhnya; kita hanya tahu _jenisnya_.
Mengingat Anda baru mempelajari struct di Bab 5, Anda mungkin tergoda untuk
menangani masalah ini dengan struct seperti yang ditunjukkan pada Listing
6-1.

<Listing number="6-1" caption="Menyimpan data dan varian `IpAddrKind` dari sebuah alamat IP memakai `struct`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-01/src/main.rs:here}}
```

</Listing>

Di sini, kita telah mendefinisikan struct `IpAddr` yang memiliki dua field:
field `kind` bertipe `IpAddrKind` (enum yang kita definisikan sebelumnya) dan
field `address` bertipe `String`. Kita memiliki dua instance struct ini. Yang
pertama adalah `home`, yang memiliki nilai `IpAddrKind::V4` sebagai `kind`-nya
beserta data alamat terkait `127.0.0.1`. Instance kedua adalah `loopback`. Ia
memiliki *variant* lain dari `IpAddrKind`, yaitu `V6`, sebagai nilai
`kind`-nya, dan memiliki alamat `::1` yang terkait dengannya. Kita telah
memakai struct untuk menggabungkan nilai `kind` dan `address`, sehingga kini
*variant* tersebut terkait dengan nilainya.

Namun, merepresentasikan konsep yang sama hanya dengan enum lebih ringkas:
alih-alih enum di dalam struct, kita dapat meletakkan data langsung ke dalam
setiap *variant* enum. Definisi baru enum `IpAddr` ini menyatakan bahwa
*variant* `V4` maupun `V6` akan memiliki nilai `String` yang terkait:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-02-enum-with-data/src/main.rs:here}}
```

Kita melampirkan data ke setiap *variant* enum secara langsung, jadi tidak
perlu struct tambahan. Di sini, juga lebih mudah melihat detail lain dari
cara kerja enum: nama setiap *variant* enum yang kita definisikan juga menjadi
fungsi yang menyusun instance enum. Artinya, `IpAddr::V4()` adalah pemanggilan
fungsi yang menerima argumen `String` dan mengembalikan instance bertipe
`IpAddr`. Kita otomatis mendapatkan fungsi konstruktor ini terdefinisi
sebagai hasil dari mendefinisikan enum.

Ada keunggulan lain dari memakai enum alih-alih struct: setiap *variant*
dapat memiliki tipe dan jumlah data terkait yang berbeda. Alamat IP versi
empat akan selalu memiliki empat komponen numerik yang nilainya antara 0 dan
255. Jika kita ingin menyimpan alamat `V4` sebagai empat nilai `u8` tetapi
tetap menyatakan alamat `V6` sebagai satu nilai `String`, kita tidak akan bisa
melakukannya dengan struct. Enum menangani kasus ini dengan mudah:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-03-variants-with-different-data/src/main.rs:here}}
```

Kita telah menunjukkan beberapa cara berbeda untuk mendefinisikan struktur
data guna menyimpan alamat IP versi empat dan versi enam. Akan tetapi,
ternyata keinginan untuk menyimpan alamat IP dan mengkodekan jenisnya begitu
umum sehingga [pustaka standar memiliki definisi yang dapat kita
pakai!][IpAddr]<!-- ignore --> Mari kita lihat bagaimana pustaka standar
mendefinisikan `IpAddr`. Ia memiliki enum dan *variant* yang persis seperti
yang telah kita definisikan dan pakai, tetapi ia menanamkan data alamat di
dalam *variant*-nya dalam bentuk dua struct berbeda, yang didefinisikan secara
berbeda untuk setiap *variant*:

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

Kode ini mengilustrasikan bahwa Anda dapat meletakkan data jenis apa pun di
dalam *variant* enum: string, tipe numerik, atau struct, misalnya. Anda
bahkan dapat menyertakan enum lain! Selain itu, tipe-tipe pustaka standar
sering kali tidak jauh lebih rumit daripada yang mungkin Anda buat sendiri.

Perhatikan bahwa meskipun pustaka standar memuat definisi untuk `IpAddr`,
kita tetap dapat membuat dan memakai definisi kita sendiri tanpa konflik
karena kita belum membawa definisi pustaka standar ke dalam *scope* (cakupan)
kita. Kita akan membahas lebih lanjut cara membawa tipe ke dalam *scope* di Bab
7.

Mari kita lihat contoh enum lain pada Listing 6-2: yang ini memiliki beragam
tipe yang tertanam di *variant*-nya.

<Listing number="6-2" caption="Enum `Message` yang varian-variannya masing-masing menyimpan jumlah dan tipe nilai yang berbeda">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Listing>

Enum ini memiliki empat *variant* dengan tipe yang berbeda:

- `Quit`: tidak memiliki data apa pun yang terkait dengannya
- `Move`: memiliki field bernama, seperti struct
- `Write`: menyertakan sebuah `String` tunggal
- `ChangeColor`: menyertakan tiga nilai `i32`

Mendefinisikan enum dengan *variant*-*variant* seperti pada Listing 6-2 mirip
dengan mendefinisikan berbagai jenis definisi struct, hanya saja enum tidak
memakai keyword `struct` dan semua *variant*-nya dikelompokkan di bawah tipe
`Message`. Struct-struct berikut dapat menampung data yang sama seperti yang
ditampung *variant*-*variant* enum sebelumnya:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

Tetapi jika kita memakai struct-struct yang berbeda, yang masing-masing
memiliki tipenya sendiri, kita tidak dapat semudah itu mendefinisikan sebuah
fungsi yang menerima pesan jenis apa pun, tidak seperti dengan enum `Message`
yang didefinisikan pada Listing 6-2, yang merupakan satu tipe.

Ada satu kemiripan lagi antara enum dan struct: sama seperti kita dapat
mendefinisikan metode pada struct dengan `impl`, kita juga dapat
mendefinisikan metode pada enum. Berikut metode bernama `call` yang dapat kita
definisikan pada enum `Message` kita:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

Badan metodenya akan memakai `self` untuk mendapatkan nilai tempat metode itu
dipanggil. Pada contoh ini, kita telah membuat variabel `m` yang memiliki
nilai `Message::Write(String::from("hello"))`, dan itulah yang akan menjadi
`self` di badan metode `call` ketika `m.call()` dijalankan.

Mari kita lihat enum lain di pustaka standar yang sangat umum dan berguna:
`Option`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-option-enum-and-its-advantages-over-null-values"></a>

### Enum `Option`

Bagian ini mengeksplorasi studi kasus `Option`, yang merupakan enum lain yang
didefinisikan oleh pustaka standar. Tipe `Option` mengkodekan skenario yang
sangat umum ketika sebuah nilai bisa berupa sesuatu, atau bisa juga bukan
apa-apa.

Contohnya, jika Anda meminta item pertama dari daftar yang tidak kosong, Anda
akan mendapatkan sebuah nilai. Jika Anda meminta item pertama dari daftar
kosong, Anda tidak akan mendapatkan apa-apa. Menyatakan konsep ini dalam
bentuk sistem tipe berarti *compiler* (kompilator) dapat memeriksa apakah Anda
telah menangani semua kasus yang seharusnya Anda tangani; fungsionalitas ini
dapat mencegah bug yang sangat umum terjadi di bahasa pemrograman lain.

Desain bahasa pemrograman sering kali dipikirkan berdasarkan fitur-fitur apa
yang disertakan, tetapi fitur-fitur yang dikecualikan juga penting. Rust tidak
memiliki fitur null seperti yang dimiliki banyak bahasa lain. *Null* adalah
nilai yang berarti tidak ada nilai di sana. Pada bahasa yang memiliki null,
variabel selalu dapat berada dalam salah satu dari dua keadaan: null atau
tidak-null.

Dalam presentasinya tahun 2009 yang berjudul “Null References: The Billion
Dollar Mistake,” Tony Hoare, penemu null, berkata:

> Saya menyebutnya kesalahan senilai satu miliar dolar. Saat itu, saya sedang
> merancang sistem tipe komprehensif pertama untuk reference di sebuah bahasa
> berorientasi objek. Tujuan saya adalah memastikan bahwa semua penggunaan
> reference benar-benar aman, dengan pemeriksaan yang dilakukan otomatis oleh
> compiler. Tetapi saya tidak kuasa menahan godaan untuk memasukkan null
> reference, semata-mata karena begitu mudah diimplementasikan. Ini telah
> menyebabkan galat, kerentanan, dan crash sistem yang tak terhitung
> banyaknya, yang mungkin telah menimbulkan penderitaan dan kerusakan senilai
> satu miliar dolar dalam empat puluh tahun terakhir.

Masalah dengan nilai null adalah, jika Anda mencoba memakai nilai null
sebagai nilai tidak-null, Anda akan mendapatkan semacam galat. Karena sifat
null-atau-tidak-null ini merata di mana-mana, sangatlah mudah untuk membuat
galat semacam ini.

Namun, konsep yang coba diungkapkan null tetaplah berguna: null adalah nilai
yang saat ini tidak valid atau tidak ada karena suatu alasan.

Masalahnya sebenarnya bukan pada konsepnya, melainkan pada implementasi
tertentu. Karena itu, Rust tidak memiliki null, tetapi ia memiliki sebuah enum
yang dapat mengkodekan konsep nilai yang ada atau tidak ada. Enum ini adalah
`Option<T>`, dan ia [didefinisikan oleh pustaka standar][option]<!-- ignore -->
sebagai berikut:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

Enum `Option<T>` begitu berguna sampai-sampai ia disertakan dalam *prelude*;
Anda tidak perlu membawanya ke dalam *scope* secara eksplisit. *variant*-*variant*-nya
juga disertakan dalam *prelude*: Anda dapat memakai `Some` dan `None` secara
langsung tanpa awalan `Option::`. Enum `Option<T>` tetap hanyalah enum biasa,
dan `Some(T)` serta `None` tetaplah *variant* bertipe `Option<T>`.

Sintaks `<T>` adalah fitur Rust yang belum kita bahas. Ia adalah parameter
tipe generik, dan kita akan membahas *generics* (tipe generik) lebih mendetail di Bab 10.
Untuk sekarang, yang perlu Anda ketahui hanyalah `<T>` berarti *variant*
`Some` dari enum `Option` dapat menampung satu potong data bertipe apa pun,
dan setiap tipe konkret yang dipakai menggantikan `T` menjadikan keseluruhan
tipe `Option<T>` sebagai tipe yang berbeda. Berikut beberapa contoh pemakaian
nilai `Option` untuk menampung tipe angka dan tipe char:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-06-option-examples/src/main.rs:here}}
```

Tipe `some_number` adalah `Option<i32>`. Tipe `some_char` adalah
`Option<char>`, yang merupakan tipe yang berbeda. Rust dapat menyimpulkan
tipe-tipe ini karena kita telah menentukan nilai di dalam *variant* `Some`.
Untuk `absent_number`, Rust mengharuskan kita memberi anotasi pada
keseluruhan tipe `Option`: compiler tidak dapat menyimpulkan tipe yang akan
ditampung *variant* `Some` yang bersesuaian hanya dengan melihat nilai `None`.
Di sini, kita memberi tahu Rust bahwa yang kita maksud adalah `absent_number`
bertipe `Option<i32>`.

Ketika kita memiliki nilai `Some`, kita tahu bahwa ada nilai, dan nilai itu
ditampung di dalam `Some`. Ketika kita memiliki nilai `None`, dalam arti
tertentu itu sama dengan null: kita tidak memiliki nilai yang valid. Jadi,
mengapa memiliki `Option<T>` lebih baik daripada memiliki null?

Singkatnya, karena `Option<T>` dan `T` (dengan `T` dapat berupa tipe apa pun)
adalah tipe yang berbeda, compiler tidak akan mengizinkan kita memakai nilai
`Option<T>` seolah-olah ia pasti nilai yang valid. Contohnya, kode ini tidak
akan terkompilasi, karena ia mencoba menambahkan `i8` ke `Option<i8>`:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

Jika kita menjalankan kode ini, kita mendapatkan pesan galat seperti ini:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

Sengit! Pada dasarnya, pesan galat ini berarti Rust tidak memahami cara
menambahkan `i8` dan `Option<i8>`, karena keduanya adalah tipe yang berbeda.
Ketika kita memiliki nilai bertipe seperti `i8` di Rust, compiler akan
memastikan bahwa kita selalu memiliki nilai yang valid. Kita dapat melangkah
dengan percaya diri tanpa harus memeriksa null sebelum memakai nilai itu.
Hanya ketika kita memiliki `Option<i8>` (atau tipe nilai apa pun yang sedang
kita olah) kita harus mengkhawatirkan kemungkinan tidak adanya nilai, dan
compiler akan memastikan kita menangani kasus itu sebelum memakai nilainya.

Dengan kata lain, Anda harus mengonversi `Option<T>` menjadi `T` sebelum Anda
dapat melakukan operasi `T` dengannya. Umumnya, ini membantu menangkap salah
satu masalah paling umum dengan null: menganggap bahwa sesuatu tidak null
padahal sebenarnya null.

Menghilangkan risiko keliru menganggap sebuah nilai tidak-null membantu Anda
lebih percaya diri terhadap kode Anda. Untuk memiliki nilai yang mungkin saja
null, Anda harus memilihnya secara eksplisit dengan membuat tipe nilai itu
`Option<T>`. Lalu, ketika Anda memakai nilai itu, Anda diwajibkan untuk secara
eksplisit menangani kasus ketika nilainya null. Di mana pun sebuah nilai
bertipe selain `Option<T>`, Anda _dapat_ dengan aman mengasumsikan bahwa nilai
itu tidak null. Ini adalah keputusan desain yang disengaja oleh Rust untuk
membatasi meratanya null dan meningkatkan keamanan kode Rust.

Jadi, bagaimana cara mengeluarkan nilai `T` dari *variant* `Some` ketika Anda
memiliki nilai bertipe `Option<T>` supaya Anda dapat memakai nilai itu? Enum
`Option<T>` memiliki banyak metode yang berguna dalam berbagai situasi; Anda
dapat melihatnya di [dokumentasinya][docs]<!-- ignore -->. Membiasakan diri
dengan metode-metode pada `Option<T>` akan sangat berguna dalam perjalanan
Anda bersama Rust.

Secara umum, untuk memakai nilai `Option<T>`, Anda ingin memiliki kode yang
menangani setiap *variant*. Anda ingin ada kode yang berjalan hanya ketika
Anda memiliki nilai `Some(T)`, dan kode ini diizinkan memakai `T` di
dalamnya. Anda ingin ada kode lain yang berjalan hanya jika Anda memiliki
nilai `None`, dan kode itu tidak memiliki nilai `T` yang tersedia. Ekspresi
`match` adalah konstruk alur kontrol yang melakukan hal ini ketika dipakai
bersama enum: ia akan menjalankan kode yang berbeda bergantung pada
*variant* enum mana yang dimilikinya, dan kode itu dapat memakai data di
dalam nilai yang dicocokkan.

[IpAddr]: ../std/net/enum.IpAddr.html
[option]: ../std/option/enum.Option.html
[docs]: ../std/option/enum.Option.html
