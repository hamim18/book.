<a id="data-types"></a>
## Type Data

Setiap nilai di Rust memiliki data type tertentu, yang memberi tahu Rust jenis
data apa yang sedang ditentukan sehingga ia tahu cara mengolah data tersebut.
Kita akan melihat dua himpunan bagian data type: skalar dan majemuk.

Ingatlah bahwa Rust adalah bahasa yang *statically typed* (bertipe statis),
artinya bahasa ini harus mengetahui type semua variable pada waktu kompilasi.
*Compiler* biasanya dapat menyimpulkan type apa yang ingin kita pakai berdasarkan
nilainya dan cara kita memakainya. Pada kasus ketika banyak type yang mungkin,
seperti ketika kita mengonversi `String` menjadi type numerik memakai `parse`
di bagian [“Membandingkan Tebakan dengan Angka
Rahasia”][comparing-the-guess-to-the-secret-number]<!-- ignore --> pada Bab 2,
kita harus menambahkan type annotation, seperti ini:

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

Jika kita tidak menambahkan type annotation `: u32` yang ditunjukkan pada kode
sebelumnya, Rust akan menampilkan error berikut, yang berarti *compiler*
membutuhkan lebih banyak informasi dari kita untuk mengetahui type mana yang
ingin kita pakai:

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

Anda akan melihat type annotation yang berbeda untuk data type lainnya.

### Type Skalar

Type skalar merepresentasikan sebuah nilai tunggal. Rust memiliki empat type
skalar utama: integer, bilangan floating-point, Boolean, dan karakter. Anda
mungkin mengenalinya dari bahasa pemrograman lain. Mari kita langsung lihat
cara kerjanya di Rust.

<a id="integer-types"></a>
#### Type Integer

Sebuah integer adalah angka tanpa komponen pecahan. Kita memakai satu type
integer di Bab 2, yaitu type `u32`. Deklarasi type ini menandakan bahwa nilai
yang terkait dengannya harus berupa integer tak bertanda (type integer bertanda
diawali dengan `i`, bukan `u`) yang menempati ruang 32 bit. Tabel 3-1
menunjukkan type integer bawaan di Rust. Kita dapat memakai salah satu dari
varian-varian ini untuk mendeklarasikan type sebuah nilai integer.

<span class="caption">Tabel 3-1: Type Integer di Rust</span>

| Panjang              | Bertanda | Tak Bertanda |
| ------- | ------- | -------- |
| 8-bit   | `i8`    | `u8`     |
| 16-bit  | `i16`   | `u16`    |
| 32-bit  | `i32`   | `u32`    |
| 64-bit  | `i64`   | `u64`    |
| 128-bit | `i128`  | `u128`   |
| Bergantung arsitektur | `isize` | `usize`  |

Setiap varian dapat bersifat signed atau unsigned dan memiliki ukuran yang
eksplisit. *Signed* (bertanda) dan *unsigned* (tak bertanda) merujuk pada
apakah angka itu mungkin bernilai negatif—dengan kata lain, apakah angka itu
perlu membawa tanda (signed) atau hanya akan selalu positif sehingga dapat
direpresentasikan tanpa tanda (unsigned). Ini seperti menulis angka di kertas:
ketika tandanya penting, sebuah angka ditulis dengan tanda plus atau tanda
minus; tetapi ketika aman untuk mengasumsikan angka itu positif, angka itu
ditulis tanpa tanda. Angka signed disimpan dengan representasi
[komplemen dua][twos-complement]<!-- ignore
-->.

Setiap varian signed dapat menyimpan angka dari −(2<sup>n − 1</sup>) sampai
2<sup>n − 1</sup> − 1 secara inklusif, dengan _n_ adalah jumlah bit yang
dipakai varian tersebut. Jadi, sebuah `i8` dapat menyimpan angka dari
−(2<sup>7</sup>) sampai 2<sup>7</sup> − 1, yang setara dengan −128 sampai 127.
Varian unsigned dapat menyimpan angka dari 0 sampai 2<sup>n</sup> − 1, jadi
sebuah `u8` dapat menyimpan angka dari 0 sampai 2<sup>8</sup> − 1, yang setara
dengan 0 sampai 255.

Selain itu, type `isize` dan `usize` bergantung pada arsitektur komputer tempat
program Anda berjalan: 64 bit jika Anda berada pada arsitektur 64-bit dan 32
bit jika Anda berada pada arsitektur 32-bit.

Anda dapat menulis literal integer dalam bentuk mana pun yang ditunjukkan pada
Tabel 3-2. Perhatikan bahwa literal angka yang bisa menjadi beberapa type
numerik mengizinkan sufiks type, seperti `57u8`, untuk menetapkan typenya.
Literal angka juga dapat memakai `_` sebagai pemisah visual agar angkanya lebih
mudah dibaca, seperti `1_000`, yang nilainya akan sama seperti jika Anda
menuliskan `1000`.

<span class="caption">Tabel 3-2: Literal Integer di Rust</span>

| Literal angka     | Contoh        |
| ---------------- | ------------- |
| Desimal          | `98_222`      |
| Heksadesimal     | `0xff`        |
| Oktal            | `0o77`        |
| Biner            | `0b1111_0000` |
| Byte (hanya `u8`) | `b'A'`        |

Jadi, bagaimana Anda tahu type integer mana yang harus dipakai? Jika Anda ragu,
bawaan Rust umumnya adalah titik awal yang baik: type integer secara bawaan
adalah `i32`. Situasi utama ketika Anda memakai `isize` atau `usize` adalah
saat melakukan pengindeksan terhadap suatu collection.

> ##### Integer Overflow
>
> Misalkan Anda memiliki variable typed `u8` yang dapat menampung nilai
> antara 0 dan 255. Jika Anda mencoba mengubah variable itu menjadi nilai di
> luar rentang tersebut, seperti 256, integer overflow akan terjadi, dan ini
> dapat menghasilkan salah satu dari dua perilaku. Ketika Anda mengompilasi
> dalam mode debug, Rust menyertakan pemeriksaan integer overflow yang membuat
> program Anda panic pada saat runtime jika perilaku ini terjadi. Rust memakai
> istilah _panicking_ ketika sebuah program keluar dengan error; kita akan
> membahas panic lebih dalam di bagian [“Error yang Tidak Dapat Dipulihkan
> dengan `panic!`”][unrecoverable-errors-with-panic]<!-- ignore --> pada Bab 9.
>
> Ketika Anda mengompilasi dalam mode release dengan flag `--release`, Rust
> _tidak_ menyertakan pemeriksaan integer overflow yang menyebabkan panic.
> Sebagai gantinya, jika overflow terjadi, Rust melakukan _pembungkusan
> komplemen dua_. Singkatnya, nilai yang lebih besar daripada nilai maksimum
> yang dapat ditampung type tersebut akan “membungkus” ke nilai minimum yang
> dapat ditampung type tersebut. Pada kasus `u8`, nilai 256 menjadi 0, nilai
> 257 menjadi 1, dan seterusnya. Program tidak akan panic, tetapi variablenya
> akan memiliki nilai yang mungkin bukan seperti yang Anda harapkan.
> Mengandalkan perilaku pembungkusan integer overflow dianggap sebagai sebuah
> error.
>
> Untuk menangani kemungkinan overflow secara eksplisit, Anda dapat memakai
> keluarga method berikut yang disediakan oleh standard library untuk type
> numerik primitif:
>
> - Membungkus dalam semua mode kompilasi dengan method `wrapping_*`, seperti 
>   `wrapping_add`.
> - Mengembalikan nilai `None` jika terjadi overflow dengan method `checked_*`.
> - Mengembalikan nilai beserta sebuah Boolean yang menandakan apakah overflow
>   terjadi dengan method `overflowing_*`.
> - Menjenuhkan pada nilai minimum atau maksimum dengan method `saturating_*`.

#### Type Floating-Point

Rust juga memiliki dua primitive type untuk *floating-point* (floating point),
yaitu angka dengan titik desimal. Type floating-point di Rust adalah `f32` dan
`f64`, yang masing-masing berukuran 32 bit dan 64 bit. Type bawaannya adalah
`f64` karena pada CPU modern, kecepatannya kurang lebih sama dengan `f32`
tetapi mampu memberikan presisi lebih tinggi. Semua type floating-point
bersifat signed.

Berikut contoh yang memperlihatkan bilangan floating-point sedang beraksi:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

Bilangan floating-point direpresentasikan sesuai standar IEEE-754.

#### Operasi Numerik

Rust mendukung operasi matematika dasar yang Anda harapkan untuk semua type
angka: penjumlahan, pengurangan, perkalian, pembagian, dan sisa bagi. Pembagian
integer memotong ke arah nol menuju integer terdekat. Kode berikut menunjukkan
cara memakai setiap operasi numerik dalam statement `let`:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Setiap expression dalam statement-statement ini memakai sebuah operator
matematika dan mengevaluasi menjadi satu nilai, yang kemudian diikat ke sebuah
variable. [Lampiran B][appendix_b]<!-- ignore --> memuat daftar semua operator
yang disediakan Rust.

#### Type Boolean

Seperti pada sebagian besar bahasa pemrograman lain, type Boolean di Rust
memiliki dua nilai yang mungkin: `true` dan `false`. Ukuran Boolean adalah satu
byte. Type Boolean di Rust ditulis dengan `bool`. Contohnya:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

Cara utama memakai nilai Boolean adalah melalui kondisional, seperti expression
`if`. Kita akan membahas cara kerja expression `if` di Rust pada bagian
[“Alur Kontrol”][control-flow]<!-- ignore -->.

#### Type Karakter

Type `char` di Rust adalah type alfabetis paling primitif dalam bahasa ini.
Berikut beberapa contoh pendeklarasian nilai `char`:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Perhatikan bahwa kita menuliskan literal `char` dengan tanda kutip tunggal,
berbeda dengan literal string yang memakai tanda kutip ganda. Type `char` di
Rust berukuran 4 byte dan merepresentasikan sebuah nilai skalar Unicode, yang
berarti ia dapat merepresentasikan jauh lebih banyak daripada sekadar ASCII.
Huruf beraksen; karakter Tionghoa, Jepang, dan Korea; emoji; dan spasi lebar
nol semuanya adalah nilai `char` yang valid di Rust. Nilai skalar Unicode
berkisar dari `U+0000` sampai `U+D7FF` dan `U+E000` sampai `U+10FFFF` secara
inklusif. Akan tetapi, “karakter” sebenarnya bukan sebuah konsep di Unicode,
sehingga intuisi Anda tentang apa itu “karakter” mungkin tidak cocok dengan apa
itu `char` di Rust. Kita akan membahas topik ini secara mendetail di
[“Menyimpan Teks Terenkode UTF-8 dengan String”][strings]<!-- ignore --> pada
Bab 8.

### Type Majemuk

Type majemuk dapat mengelompokkan beberapa nilai menjadi satu type. Rust
memiliki dua compound type primitif: *tuple* dan array.

<a id="the-tuple-type"></a>
#### Type Tuple

Sebuah *tuple* adalah cara umum untuk mengelompokkan sejumlah nilai dengan
beragam type menjadi satu compound type. *Tuple* memiliki panjang yang tetap:
begitu dideklarasikan, ukurannya tidak dapat membesar atau mengecil.

Kita membuat *tuple* dengan menuliskan daftar nilai yang dipisahkan koma di
dalam tanda kurung. Setiap posisi di dalam *tuple* memiliki type, dan type
nilai-nilai yang berbeda di dalam *tuple* tidak harus sama. Kita menambahkan
type annotation opsional pada contoh ini:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

Variable `tup` terikat pada keseluruhan *tuple* karena *tuple* dianggap sebagai
satu elemen majemuk tunggal. Untuk mengambil nilai-nilai individual dari
sebuah *tuple*, kita dapat memakai *pattern matching* (pencocokan pattern) untuk
mendestrukturisasi nilai *tuple*, seperti ini:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

Program ini mula-mula membuat sebuah *tuple* dan mengikatnya ke variable `tup`.
Lalu program memakai sebuah pattern dengan `let` untuk mengambil `tup` dan
mengubahnya menjadi tiga variable terpisah, `x`, `y`, dan `z`. Ini disebut
*destructuring* (destrukturisasi) karena ia memecah satu *tuple* menjadi tiga
bagian. Terakhir, program mencetak nilai `y`, yaitu `6.4`.

Kita juga dapat mengakses elemen *tuple* secara langsung dengan memakai titik
(`.`) yang diikuti indeks nilai yang ingin kita akses. Contohnya:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

Program ini membuat *tuple* `x` lalu mengakses setiap elemen *tuple* dengan memakai
indeksnya masing-masing. Seperti pada sebagian besar bahasa pemrograman, indeks
pertama dalam sebuah *tuple* adalah 0.

*Tuple* tanpa nilai apa pun memiliki nama khusus, *unit*. Nilai ini dan type yang
bersesuaian dengannya sama-sama ditulis `()` dan merepresentasikan nilai kosong
atau return type kosong. Expression secara implisit mengembalikan nilai unit
jika tidak mengembalikan nilai lain.

#### Type Array

Cara lain untuk memiliki collection berisi banyak nilai adalah dengan array.
Tidak seperti *tuple*, setiap elemen array harus memiliki type yang sama. Tidak
seperti array pada beberapa bahasa lain, array di Rust memiliki panjang yang
tetap.

Kita menuliskan nilai-nilai dalam array sebagai daftar yang dipisahkan koma di
dalam kurung siku:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

Array berguna ketika Anda ingin data Anda dialokasikan di *stack* (tumpukan),
sama seperti type-type lain yang telah kita lihat sejauh ini, alih-alih di
*heap* (timbunan) (kita akan membahas *stack* dan *heap* lebih lanjut di
[Bab 4][stack-and-heap]<!-- ignore -->) atau ketika Anda ingin memastikan
bahwa Anda selalu memiliki jumlah elemen yang tetap. Meski begitu, array tidak
sefleksibel type vector. Vector adalah type collection serupa yang disediakan oleh
standard library yang _diizinkan_ untuk membesar atau mengecil ukurannya karena
isinya berada di *heap*. Jika Anda ragu apakah harus memakai array atau vector,
kemungkinan besar Anda sebaiknya memakai vector. [Bab 8][vectors]<!-- ignore
--> membahas vector secara lebih mendetail.

Namun, array lebih berguna ketika Anda tahu bahwa jumlah elemennya tidak akan
perlu berubah. Contohnya, jika Anda memakai nama-nama bulan dalam sebuah
program, Anda mungkin akan memakai array alih-alih vector karena Anda tahu
array itu akan selalu berisi 12 elemen:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

Anda menuliskan type array dengan memakai kurung siku yang berisi type setiap
elemen, tanda titik koma, lalu jumlah elemen dalam array, seperti ini:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Di sini, `i32` adalah type setiap elemen. Setelah titik koma, angka `5`
menandakan bahwa array tersebut berisi lima elemen.

Anda juga dapat menginisialisasi array agar berisi nilai yang sama untuk
setiap elemen dengan menuliskan nilai awal, diikuti titik koma, lalu panjang
array dalam kurung siku, seperti yang ditunjukkan di sini:

```rust
let a = [3; 5];
```

Array bernama `a` akan berisi `5` elemen yang semuanya diisi nilai `3` pada
awalnya. Ini sama dengan menulis `let a = [3, 3, 3, 3, 3];` tetapi dengan cara
yang lebih ringkas.

<!-- Old headings. Do not remove or links may break. -->
<a id="accessing-array-elements"></a>

#### Mengakses Elemen Array

Array adalah satu bongkah memori berukuran tetap yang diketahui dan dapat
dialokasikan di *stack*. Anda dapat mengakses elemen-elemen array dengan
pengindeksan, seperti ini:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

Pada contoh ini, variable bernama `first` akan mendapatkan nilai `1` karena
itulah nilai pada indeks `[0]` di dalam array. Variable bernama `second` akan
mendapatkan nilai `2` dari indeks `[1]` di dalam array.

#### Akses Elemen Array yang Tidak Valid

Mari kita lihat apa yang terjadi jika Anda mencoba mengakses elemen array yang
berada di luar ujung array. Misalkan Anda menjalankan kode ini, mirip dengan
permainan tebak angka di Bab 2, untuk mendapatkan indeks array dari pengguna:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

Kode ini berhasil dikompilasi. Jika Anda menjalankan kode ini dengan
`cargo run` dan memasukkan `0`, `1`, `2`, `3`, atau `4`, program akan mencetak
nilai yang bersesuaian pada indeks tersebut di dalam array. Jika Anda justru
memasukkan angka di luar ujung array, seperti `10`, Anda akan melihat output
seperti ini:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Program ini menghasilkan error runtime pada saat memakai nilai yang tidak
valid dalam operasi pengindeksan. Program keluar dengan pesan error dan tidak
mengeksekusi statement `println!` terakhir. Ketika Anda mencoba mengakses
sebuah elemen dengan pengindeksan, Rust akan memeriksa bahwa indeks yang Anda
berikan lebih kecil daripada panjang array. Jika indeksnya lebih besar daripada
atau sama dengan panjangnya, Rust akan panic. Pemeriksaan ini harus terjadi
pada saat runtime, khususnya pada kasus ini, karena *compiler* tidak mungkin tahu
nilai apa yang akan dimasukkan pengguna ketika mereka menjalankan kodenya
nanti.

Ini adalah contoh prinsip memory safety Rust sedang beraksi. Pada banyak
low-level language, pemeriksaan semacam ini tidak dilakukan, dan ketika Anda
memberikan indeks yang salah, memori yang tidak valid dapat diakses. Rust
melindungi Anda dari error semacam ini dengan segera keluar alih-alih
mengizinkan akses memori itu dan melanjutkan eksekusi. Bab 9 membahas lebih
lanjut penanganan error di Rust dan cara menulis kode yang mudah dibaca dan
aman yang tidak pernah panic maupun mengizinkan akses memori yang tidak valid.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md
