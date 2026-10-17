## Type Data Generik

Kita memakai *generics* untuk membuat definisi item seperti tanda tangan
fungsi atau *struct*, yang kemudian bisa kita pakai dengan banyak data type
konkret yang berbeda. Mari kita lihat dulu cara mendefinisikan fungsi,
*struct*, *enum*, dan metode dengan memakai *generics*. Kemudian, kita akan
membahas bagaimana *generics* memengaruhi kinerja kode.

### Dalam Definisi Fungsi

Saat mendefinisikan fungsi yang memakai *generics*, kita menempatkan *generics*
di tanda tangan fungsi, tepat di tempat kita biasanya menentukan data type
parameter dan nilai kembaliannya. Melakukannya membuat kode kita lebih
fleksibel dan menyediakan lebih banyak fungsionalitas bagi pemanggil fungsi
kita sekaligus mencegah duplikasi kode.

Melanjutkan fungsi `largest` kita, Listing 10-4 menunjukkan dua fungsi yang
sama-sama menemukan nilai terbesar dalam sebuah *slice*. Kita kemudian akan
menggabungkan keduanya menjadi satu fungsi yang memakai *generics*.

<Listing number="10-4" file-name="src/main.rs" caption="Dua fungsi yang hanya berbeda pada nama dan type di tanda tangannya">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Listing>

Fungsi `largest_i32` adalah fungsi yang kita ekstrak di Listing 10-3 untuk
menemukan `i32` terbesar dalam sebuah *slice*. Fungsi `largest_char`
menemukan `char` terbesar dalam sebuah *slice*. Badan kedua fungsi memiliki
kode yang sama, jadi mari kita hilangkan duplikasinya dengan memperkenalkan
type parameter generik dalam satu fungsi.

Untuk memparameterisasi type-type dalam satu fungsi baru, kita perlu menamai
type parameter tersebut, sama seperti kita menamai parameter nilai sebuah
fungsi. Anda bisa memakai *identifier* (pengidentifikasi) mana pun sebagai
nama type parameter. Akan tetapi, kita akan memakai `T` karena, menurut
konvensi, nama type parameter di Rust pendek, sering kali hanya satu huruf,
dan konvensi penamaan type Rust adalah UpperCamelCase. Sebagai kependekan
dari _type_, `T` adalah pilihan bawaan sebagian besar pemrogram Rust.

Ketika kita memakai sebuah parameter di badan fungsi, kita harus
mendeklarasikan nama parameter itu di tanda tangan supaya *compiler* tahu apa
arti nama tersebut. Demikian pula, ketika kita memakai nama type parameter di
tanda tangan fungsi, kita harus mendeklarasikan nama type parameter itu
sebelum memakainya. Untuk mendefinisikan fungsi generik `largest`, kita
menempatkan deklarasi nama type di dalam kurung sudut, `<>`, di antara nama
fungsi dan daftar parameternya, seperti ini:

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

Kita membaca definisi ini sebagai “Fungsi `largest` bersifat generik atas
suatu type `T`.” Fungsi ini memiliki satu parameter bernama `list`, yang
berupa *slice* berisi nilai-nilai typed `T`. Fungsi `largest` akan
mengembalikan sebuah *reference* ke nilai typed `T` yang sama.

Listing 10-5 menunjukkan definisi fungsi `largest` gabungan yang memakai
data generic type di tanda tangannya. Listing itu juga menunjukkan bagaimana
kita bisa memanggil fungsi tersebut dengan *slice* berisi nilai `i32` ataupun
nilai `char`. Perhatikan bahwa kode ini belum bisa dikompilasi.

<Listing number="10-5" file-name="src/main.rs" caption="Fungsi `largest` yang memakai type parameter generik; kode ini belum bisa dikompilasi">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Listing>

Jika kita mengompilasi kode ini sekarang, kita akan mendapatkan error
berikut:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

Teks bantuannya menyebut `std::cmp::PartialOrd`, yang merupakan sebuah
*trait*, dan kita akan membahas *trait* di bagian berikutnya. Untuk sekarang,
ketahuilah bahwa error ini menyatakan bahwa badan `largest` tidak akan
berfungsi untuk semua type yang mungkin menjadi `T`. Karena kita ingin
membandingkan nilai typed `T` di dalam badan fungsi, kita hanya bisa
memakai type-type yang nilainya bisa diurutkan. Untuk memungkinkan
perbandingan, pustaka standar memiliki *trait* `std::cmp::PartialOrd` yang bisa
Anda implementasikan pada type-type (lihat Lampiran C untuk penjelasan lebih
lanjut tentang *trait* ini). Untuk memperbaiki Listing 10-5, kita bisa
mengikuti saran teks bantuan itu dan membatasi type-type yang sah untuk `T`
menjadi hanya type-type yang mengimplementasikan `PartialOrd`. Listing
tersebut kemudian akan terkompilasi, karena pustaka standar
mengimplementasikan `PartialOrd` pada `i32` maupun `char`.

### Dalam Definisi Struct

Kita juga bisa mendefinisikan *struct* untuk memakai type parameter generik di
satu *field* (medan) atau lebih dengan memakai sintaks `<>`. Listing 10-6
mendefinisikan *struct* `Point<T>` untuk menampung nilai koordinat `x` dan `y`
typed apa pun.

<Listing number="10-6" file-name="src/main.rs" caption="Struct `Point<T>` yang menampung nilai `x` dan `y` typed `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Listing>

Sintaks pemakaian *generics* dalam definisi *struct* mirip dengan yang dipakai
dalam definisi fungsi. Pertama, kita mendeklarasikan nama type parameter di
dalam kurung sudut tepat setelah nama *struct*. Kemudian, kita memakai type
generik dalam definisi *struct* di tempat yang biasanya kita pakai untuk
menentukan data type konkret.

Perhatikan bahwa karena kita hanya memakai satu generic type untuk
mendefinisikan `Point<T>`, definisi ini menyatakan bahwa *struct* `Point<T>`
bersifat generik atas suatu type `T`, dan *field* `x` serta `y` _keduanya_
typed sama, apa pun type itu. Jika kita membuat sebuah instance
`Point<T>` yang memiliki nilai-nilai typed berbeda, seperti di Listing
10-7, kode kita tidak akan terkompilasi.

<Listing number="10-7" file-name="src/main.rs" caption="Field `x` dan `y` harus typed sama karena keduanya memiliki data generic type `T` yang sama.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Listing>

Dalam contoh ini, ketika kita menetapkan nilai integer `5` ke `x`, kita
memberi tahu *compiler* bahwa generic type `T` akan berupa integer untuk
instance `Point<T>` ini. Kemudian, ketika kita menentukan `4.0` untuk `y`,
yang telah kita definisikan typed sama dengan `x`, kita akan mendapatkan
error ketidakcocokan type seperti ini:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

Untuk mendefinisikan *struct* `Point` yang `x` dan `y`-nya sama-sama generik
tetapi bisa typed berbeda, kita bisa memakai beberapa type parameter
generik. Sebagai contoh, di Listing 10-8, kita mengubah definisi `Point`
agar generik atas type `T` dan `U`, dengan `x` typed `T` dan `y` typed
`U`.

<Listing number="10-8" file-name="src/main.rs" caption="`Point<T, U>` yang generik atas dua type sehingga `x` dan `y` bisa berupa nilai typed berbeda">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Listing>

Sekarang semua instance `Point` yang ditampilkan diizinkan! Anda bisa
memakai type parameter generik sebanyak yang Anda mau dalam sebuah definisi,
tetapi memakai lebih dari beberapa parameter membuat kode Anda sulit dibaca.
Jika Anda merasa butuh banyak generic type dalam kode Anda, itu bisa menjadi
pertanda bahwa kode Anda perlu direstrukturisasi menjadi bagian-bagian yang
lebih kecil.

### Dalam Definisi Enum

Seperti yang kita lakukan dengan *struct*, kita bisa mendefinisikan *enum* untuk
menampung data generic type di dalam *variant* (varian)-nya. Mari kita lihat
lagi *enum* `Option<T>` yang disediakan pustaka standar, yang kita pakai di
Bab 6:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Definisi ini seharusnya sekarang lebih masuk akal bagi Anda. Seperti yang
Anda lihat, *enum* `Option<T>` bersifat generik atas type `T` dan memiliki dua
varian: `Some`, yang menampung satu nilai typed `T`, dan varian `None` yang
tidak menampung nilai apa pun. Dengan memakai *enum* `Option<T>`, kita bisa
mengekspresikan konsep abstrak tentang nilai opsional, dan karena
`Option<T>` generik, kita bisa memakai abstraksi ini apa pun type nilai
opsionalnya.

*Enum* juga bisa memakai beberapa generic type. Definisi *enum* `Result` yang
kita pakai di Bab 9 adalah salah satu contohnya:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

*Enum* `Result` bersifat generik atas dua type, `T` dan `E`, dan memiliki dua
varian: `Ok`, yang menampung sebuah nilai typed `T`, dan `Err`, yang
menampung sebuah nilai typed `E`. Definisi ini memudahkan kita memakai *enum*
`Result` di mana pun kita memiliki operasi yang mungkin berhasil
(mengembalikan nilai typed `T`) atau gagal (mengembalikan error typed
`E`). Nyatanya, inilah yang kita pakai untuk membuka file di Listing 9-3,
ketika `T` diisi dengan type `std::fs::File` jika file berhasil dibuka dan
`E` diisi dengan type `std::io::Error` ketika ada masalah saat membuka file.

Ketika Anda mengenali situasi dalam kode Anda dengan beberapa definisi
*struct* atau *enum* yang hanya berbeda pada type nilai yang ditampungnya, Anda
bisa menghindari duplikasi dengan memakai generic type.

### Dalam Definisi Metode

Kita bisa mengimplementasikan metode pada *struct* dan *enum* (seperti yang kita
lakukan di Bab 5) dan memakai generic type dalam definisinya juga. Listing
10-9 menunjukkan *struct* `Point<T>` yang kita definisikan di Listing 10-6
dengan sebuah metode bernama `x` yang diimplementasikan padanya.

<Listing number="10-9" file-name="src/main.rs" caption="Mengimplementasikan metode bernama `x` pada struct `Point<T>` yang akan mengembalikan reference ke field `x` typed `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Listing>

Di sini, kita telah mendefinisikan metode bernama `x` pada `Point<T>` yang
mengembalikan sebuah *reference* ke data di dalam *field* `x`.

Perhatikan bahwa kita harus mendeklarasikan `T` tepat setelah `impl` supaya
kita bisa memakai `T` untuk menyatakan bahwa kita sedang mengimplementasikan
metode pada type `Point<T>`. Dengan mendeklarasikan `T` sebagai generic type
setelah `impl`, Rust bisa mengidentifikasi bahwa type di dalam kurung sudut
pada `Point` adalah generic type, bukan type konkret. Kita bisa saja memilih
nama yang berbeda untuk parameter generik ini daripada parameter generik
yang dideklarasikan dalam definisi *struct*, tetapi memakai nama yang sama
sudah menjadi konvensi. Jika Anda menulis metode di dalam `impl` yang
mendeklarasikan generic type, metode itu akan didefinisikan pada instance
mana pun dari type tersebut, apa pun type konkret yang akhirnya menggantikan
generic typenya.

Kita juga bisa menentukan batasan pada generic type ketika mendefinisikan
metode pada type tersebut. Misalnya, kita bisa mengimplementasikan metode
hanya pada instance `Point<f32>`, alih-alih pada instance `Point<T>` dengan
generic type apa pun. Di Listing 10-10, kita memakai type konkret `f32`,
artinya kita tidak mendeklarasikan type apa pun setelah `impl`.

<Listing number="10-10" file-name="src/main.rs" caption="Blok `impl` yang hanya berlaku untuk struct dengan type konkret tertentu untuk type parameter generik `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Listing>

Kode ini berarti type `Point<f32>` akan memiliki metode
`distance_from_origin`; instance lain `Point<T>` yang `T`-nya bukan typed
`f32` tidak akan memiliki metode ini. Metode tersebut mengukur seberapa jauh
titik kita dari titik pada koordinat (0.0, 0.0) dan memakai operasi matematis
yang hanya tersedia untuk type titik mengambang.

Parameter generic type dalam definisi *struct* tidak selalu sama dengan yang
Anda pakai di tanda tangan metode *struct* yang sama. Listing 10-11 memakai
generic type `X1` dan `Y1` untuk *struct* `Point` dan `X2` serta `Y2` untuk
tanda tangan metode `mixup` agar contohnya lebih jelas. Metode ini membuat
sebuah instance `Point` baru dengan nilai `x` dari `Point` `self` (typed
`X1`) dan nilai `y` dari `Point` yang diteruskan (typed `Y2`).

<Listing number="10-11" file-name="src/main.rs" caption="Metode yang memakai generic type yang berbeda dari definisi struct-nya">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Listing>

Di dalam `main`, kita telah mendefinisikan sebuah `Point` yang memiliki
`i32` untuk `x` (dengan nilai `5`) dan `f64` untuk `y` (dengan nilai `10.4`).
Variabel `p2` adalah *struct* `Point` yang memiliki *string slice* untuk `x`
(dengan nilai `"Hello"`) dan `char` untuk `y` (dengan nilai `c`). Memanggil
`mixup` pada `p1` dengan argumen `p2` menghasilkan `p3`, yang akan memiliki
`i32` untuk `x` karena `x` berasal dari `p1`. Variabel `p3` akan memiliki
`char` untuk `y` karena `y` berasal dari `p2`. Panggilan *macro* (makro)
`println!` akan mencetak `p3.x = 5, p3.y = c`.

Tujuan contoh ini adalah untuk memperlihatkan situasi ketika sebagian
parameter generik dideklarasikan dengan `impl` dan sebagian lagi
dideklarasikan dengan definisi metode. Di sini, parameter generik `X1` dan
`Y1` dideklarasikan setelah `impl` karena mereka menyertai definisi *struct*.
Parameter generik `X2` dan `Y2` dideklarasikan setelah `fn mixup` karena
mereka hanya relevan untuk metode tersebut.

<a id="performance-of-code-using-generics"></a>
### Kinerja Kode yang Memakai Generics

Anda mungkin bertanya-tanya apakah ada biaya *runtime* ketika memakai
type parameter generik. Kabar baiknya, memakai generic type tidak akan
membuat program Anda berjalan lebih lambat dibandingkan dengan type konkret.

Rust mencapai hal ini dengan melakukan monomorfisasi pada kode yang memakai
*generics* di waktu kompilasi. *Monomorphization* (monomorfisasi) adalah proses
mengubah kode generik menjadi kode spesifik dengan mengisi type-type konkret
yang dipakai saat dikompilasi. Dalam proses ini, *compiler* melakukan
kebalikan dari langkah-langkah yang kita pakai untuk membuat fungsi generik
di Listing 10-5: *compiler* melihat semua tempat kode generik dipanggil dan
membangkitkan kode untuk type-type konkret yang dipakai untuk memanggil kode
generik tersebut.

Mari kita lihat cara kerjanya dengan memakai *enum* generik `Option<T>` dari
pustaka standar:

```rust
let integer = Some(5);
let float = Some(5.0);
```

Ketika Rust mengompilasi kode ini, ia melakukan monomorfisasi. Selama proses
itu, *compiler* membaca nilai-nilai yang telah dipakai dalam instance
`Option<T>` dan mengidentifikasi dua jenis `Option<T>`: satu adalah `i32` dan
satunya lagi `f64`. Dengan demikian, ia memperluas definisi generik
`Option<T>` menjadi dua definisi yang terspesialisasi untuk `i32` dan `f64`,
lalu mengganti definisi generiknya dengan definisi-definisi spesifik
tersebut.

Versi kode yang telah dimonomorfisasi tampak mirip dengan yang berikut
(*compiler* memakai nama yang berbeda dari yang kita pakai di sini untuk
ilustrasi):

<Listing file-name="src/main.rs">

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

</Listing>

`Option<T>` yang generik diganti dengan definisi-definisi spesifik yang
dibuat *compiler*. Karena Rust mengompilasi kode generik menjadi kode yang
menentukan type di setiap instance, kita tidak membayar biaya *runtime*
untuk memakai *generics*. Ketika kode berjalan, kinerjanya sama seperti jika
kita menduplikasi setiap definisi secara manual. Proses monomorfisasi
membuat *generics* Rust sangat efisien di *runtime*.
