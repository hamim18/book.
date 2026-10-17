<a id="validating-references-with-lifetimes"></a>
## Memvalidasi Reference dengan Lifetime

*Lifetime* adalah jenis generik lain yang sudah kita pakai. Alih-alih
memastikan bahwa sebuah type memiliki perilaku yang kita inginkan, *lifetime*
memastikan bahwa *reference* tetap valid selama kita membutuhkannya.

Satu detail yang tidak kita bahas di bagian [“*References* dan
*Borrowing*”][*references*-and-borrowing]<!-- ignore --> pada Bab 4 adalah
bahwa setiap *reference* di Rust memiliki sebuah *lifetime*, yaitu *scope*
(cakupan) tempat *reference* tersebut valid. Sebagian besar waktu, *lifetime*
bersifat implisit dan diinferensi, sama seperti sebagian besar waktu type
diinferensi. Kita hanya diwajibkan mengtype annotation ketika ada banyak type
yang mungkin. Dengan cara serupa, kita harus menganotasi *lifetime* ketika
*lifetime* dari beberapa *reference* bisa saling terkait dalam beberapa cara
yang berbeda. Rust mewajibkan kita menganotasi hubungan tersebut memakai
parameter *lifetime* generik untuk memastikan bahwa *reference* yang
sesungguhnya dipakai pada saat *runtime* pasti valid.

Menganotasi *lifetime* bahkan bukan konsep yang dimiliki sebagian besar
bahasa pemrograman lain, jadi ini akan terasa asing. Meskipun kita tidak
akan membahas *lifetime* secara menyeluruh dalam bab ini, kita akan membahas
cara-cara umum Anda menemui sintaks *lifetime* supaya Anda bisa merasa nyaman
dengan konsepnya.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-dangling-references-with-lifetimes"></a>

### Reference Dangling

Tujuan utama *lifetime* adalah mencegah *reference* *dangling*, yang jika
diizinkan ada, akan membuat sebuah program merujuk data selain data yang
seharusnya dirujuk. Perhatikan program di Listing 10-16, yang memiliki
sebuah *scope* luar dan sebuah *scope* dalam.

<Listing number="10-16" caption="Upaya memakai reference yang nilainya telah keluar dari scope">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/src/main.rs}}
```

</Listing>

> Catatan: Contoh-contoh di Listing 10-16, 10-17, dan 10-23 mendeklarasikan
> variable tanpa memberikan nilai awal, sehingga nama variablenya ada di
> *scope* luar. Sepintas, ini mungkin tampak bertentangan dengan Rust yang
> tidak memiliki nilai null. Akan tetapi, jika kita mencoba memakai variable
> sebelum memberinya nilai, kita akan mendapatkan error waktu kompilasi,
> yang menunjukkan bahwa Rust memang tidak mengizinkan nilai null.

*Scope* luar mendeklarasikan variable bernama `r` tanpa nilai awal, dan *scope*
dalam mendeklarasikan variable bernama `x` dengan nilai awal `5`. Di dalam
*scope* dalam, kita mencoba menetapkan nilai `r` sebagai *reference* ke `x`.
Kemudian, *scope* dalam berakhir, dan kita mencoba mencetak nilai di `r`.
Kode ini tidak akan terkompilasi, karena nilai yang dirujuk `r` telah keluar
dari *scope* sebelum kita mencoba memakainya. Berikut pesan errornya:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

Pesan error itu mengatakan bahwa variable `x` “does not live long enough.”
Alasannya, `x` akan berada di luar *scope* ketika *scope* dalam berakhir pada
baris 7. Akan tetapi, `r` masih valid untuk *scope* luar; karena *scope*-nya
lebih besar, kita katakan bahwa ia “lives longer.” Jika Rust mengizinkan
kode ini berfungsi, `r` akan merujuk memori yang didealokasikan ketika `x`
keluar dari *scope*, dan apa pun yang kita coba lakukan dengan `r` tidak akan
berjalan dengan benar. Jadi, bagaimana Rust menentukan bahwa kode ini tidak
sah? Ia memakai *borrow checker*.

### Borrow Checker

*Compiler* (*compiler*) Rust memiliki *borrow checker* yang membandingkan
*scope*-scope untuk menentukan apakah semua *borrowing* valid. Listing 10-17
menunjukkan kode yang sama seperti Listing 10-16, tetapi dengan anotasi yang
menunjukkan *lifetime* dari variable-variablenya.

<Listing number="10-17" caption="Anotasi lifetime `r` dan `x`, masing-masing dinamai `'a` dan `'b`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

Di sini, kita telah menganotasi *lifetime* `r` dengan `'a` dan *lifetime* `x`
dengan `'b`. Seperti yang Anda lihat, blok `'b` dalam jauh lebih kecil
daripada blok *lifetime* `'a` luar. Pada waktu kompilasi, Rust membandingkan
ukuran kedua *lifetime* itu dan melihat bahwa `r` memiliki *lifetime* `'a`
tetapi ia merujuk memori dengan *lifetime* `'b`. Program ini ditolak karena
`'b` lebih pendek daripada `'a`: yang dirujuk *reference* itu tidak hidup
selama *reference*-nya.

Listing 10-18 memperbaiki kode itu sehingga tidak memiliki *reference*
*dangling* dan terkompilasi tanpa error.

<Listing number="10-18" caption="Reference yang valid karena datanya memiliki lifetime yang lebih panjang daripada reference-nya">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

Di sini, `x` memiliki *lifetime* `'b`, yang dalam kasus ini lebih besar
daripada `'a`. Ini berarti `r` boleh merujuk `x` karena Rust tahu bahwa
*reference* di `r` akan selalu valid selama `x` valid.

Sekarang setelah Anda tahu di mana letak *lifetime* *reference* dan bagaimana
Rust menganalisis *lifetime* untuk memastikan bahwa *reference* akan selalu
valid, mari kita eksplorasi *lifetime* generik dalam parameter fungsi dan
return value.

### Lifetime Generik dalam Fungsi

Kita akan menulis sebuah fungsi yang mengembalikan yang lebih panjang dari
dua *string slice*. Fungsi ini akan menerima dua string *slice* dan
mengembalikan satu string *slice*. Setelah kita mengimplementasikan fungsi
`longest`, kode di Listing 10-19 seharusnya mencetak `The longest string is
abcd`.

<Listing number="10-19" file-name="src/main.rs" caption="Fungsi `main` yang memanggil fungsi `longest` untuk menemukan yang lebih panjang dari dua string slice">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Perhatikan bahwa kita ingin fungsi itu menerima string *slice*, yang
merupakan *reference*, alih-alih string, karena kita tidak ingin fungsi
`longest` mengambil *ownership* (kepemilikan) parameternya. Lihat
[“Slice String sebagai Parameter”][string-slices-as-parameters]<!-- ignore
--> di Bab 4 untuk pembahasan lebih lanjut tentang alasan parameter yang
kita pakai di Listing 10-19 adalah parameter yang kita inginkan.

Jika kita mencoba mengimplementasikan fungsi `longest` seperti yang
ditunjukkan di Listing 10-20, kode itu tidak akan terkompilasi.

<Listing number="10-20" file-name="src/main.rs" caption="Implementasi fungsi `longest` yang mengembalikan yang lebih panjang dari dua string slice tetapi belum terkompilasi">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

Sebagai gantinya, kita mendapatkan error berikut yang membahas tentang
*lifetime*:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

Teks bantuan itu mengungkapkan bahwa return typenya memerlukan parameter
*lifetime* generik karena Rust tidak bisa membedakan apakah *reference* yang
dikembalikan merujuk `x` atau `y`. Sebenarnya, kita juga tidak tahu, karena
blok `if` di badan fungsi ini mengembalikan *reference* ke `x` dan blok
`else` mengembalikan *reference* ke `y`!

Ketika kita mendefinisikan fungsi ini, kita tidak tahu nilai konkret yang
akan diteruskan ke fungsi ini, jadi kita tidak tahu apakah kasus `if` atau
kasus `else` yang akan dieksekusi. Kita juga tidak tahu *lifetime* konkret
*reference* yang akan diteruskan, jadi kita tidak bisa melihat *scope*-scope
seperti yang kita lakukan di Listing 10-17 dan 10-18 untuk menentukan
apakah *reference* yang kita kembalikan akan selalu valid. *Borrow checker*
juga tidak bisa menentukannya, karena ia tidak tahu bagaimana *lifetime* `x`
dan `y` berhubungan dengan *lifetime* return valuenya. Untuk memperbaiki
error ini, kita akan menambahkan parameter *lifetime* generik yang
mendefinisikan hubungan antarreference sehingga *borrow checker* bisa
melakukan analisisnya.

### Sintaks Anotasi Lifetime

Anotasi *lifetime* tidak mengubah berapa lama *reference* mana pun hidup.
Sebaliknya, anotasi itu mendeskripsikan hubungan *lifetime* dari beberapa
*reference* satu sama lain tanpa memengaruhi *lifetime*-nya. Sama seperti
fungsi yang bisa menerima type apa pun ketika *signature*nya menentukan
type parameter generik, fungsi bisa menerima *reference* dengan *lifetime* apa
pun dengan menentukan parameter *lifetime* generik.

Anotasi *lifetime* memiliki sintaks yang sedikit tidak biasa: nama parameter
*lifetime* harus dimulai dengan tanda apostrof (`'`) dan biasanya semuanya
huruf kecil serta sangat pendek, seperti generic type. Kebanyakan orang
memakai nama `'a` untuk anotasi *lifetime* yang pertama. Kita menempatkan
anotasi parameter *lifetime* setelah `&` pada sebuah *reference*, memakai spasi
untuk memisahkan anotasi itu dari type *reference*-nya.

Berikut beberapa contoh—*reference* ke `i32` tanpa parameter *lifetime*,
*reference* ke `i32` yang memiliki parameter *lifetime* bernama `'a`, dan
*reference* *mutable* (dapat diubah) ke `i32` yang juga memiliki *lifetime*
`'a`:

```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

Satu anotasi *lifetime* saja tidak memiliki banyak makna, karena anotasi
ditujukan untuk memberi tahu Rust bagaimana parameter *lifetime* generik dari
beberapa *reference* saling berhubungan. Mari kita periksa bagaimana anotasi
*lifetime* saling berhubungan dalam konteks fungsi `longest`.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-function-signatures"></a>

### Dalam Tanda Tangan Fungsi

Untuk memakai anotasi *lifetime* di *signature* fungsi, kita perlu
mendeklarasikan parameter *lifetime* generik di dalam kurung sudut antara
nama fungsi dan daftar parameternya, sama seperti yang kita lakukan dengan
type parameter generik.

Kita ingin *signature* itu mengekspresikan batasan berikut: *reference* yang
dikembalikan akan valid selama kedua parameter valid. Inilah hubungan antara
*lifetime* parameter dan return value. Kita akan menamai *lifetime* itu
`'a`, lalu menambahkannya ke setiap *reference*, seperti yang ditunjukkan di
Listing 10-21.

<Listing number="10-21" file-name="src/main.rs" caption="Definisi fungsi `longest` yang menentukan bahwa semua reference di *signature* harus memiliki lifetime `'a` yang sama">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

Kode ini seharusnya terkompilasi dan menghasilkan hasil yang kita inginkan
ketika kita memakainya bersama fungsi `main` di Listing 10-19.

Tanda tangan fungsi sekarang memberi tahu Rust bahwa untuk suatu *lifetime*
`'a`, fungsi itu menerima dua parameter, keduanya berupa string *slice* yang
hidup paling tidak selama *lifetime* `'a`. Tanda tangan fungsi juga memberi
tahu Rust bahwa string *slice* yang dikembalikan dari fungsi itu akan hidup
paling tidak selama *lifetime* `'a`. Dalam praktiknya, itu berarti *lifetime*
dari *reference* yang dikembalikan fungsi `longest` sama dengan yang lebih
kecil di antara *lifetime* nilai-nilai yang dirujuk argumen fungsi. Hubungan
inilah yang kita ingin Rust pakai ketika menganalisis kode ini.

Ingat, ketika kita menentukan parameter *lifetime* di *signature* fungsi ini,
kita tidak mengubah *lifetime* nilai mana pun yang diteruskan atau
dikembalikan. Sebaliknya, kita menentukan bahwa *borrow checker* harus
menolak nilai mana pun yang tidak mematuhi batasan ini. Perhatikan bahwa
fungsi `longest` tidak perlu tahu persis berapa lama `x` dan `y` akan
hidup, ia hanya perlu tahu bahwa ada *scope* yang bisa disubstitusikan untuk
`'a` yang akan memenuhi *signature* ini.

Ketika menganotasi *lifetime* dalam fungsi, anotasinya berada di *signature*
fungsi, bukan di badan fungsi. Anotasi *lifetime* menjadi bagian dari kontrak
fungsi, mirip dengan type-type di *signature*. Tanda tangan fungsi yang
memuat kontrak *lifetime* membuat analisis yang dilakukan *compiler* Rust
menjadi lebih sederhana. Jika ada masalah dengan cara sebuah fungsi
dianotasi atau cara ia dipanggil, error *compiler* bisa menunjuk ke bagian
kode kita dan batasannya secara lebih presisi. Sebaliknya, jika *compiler*
Rust membuat lebih banyak inferensi tentang hubungan *lifetime* yang kita
maksudkan, *compiler* mungkin hanya bisa menunjuk pemakaian kode kita yang
jauh beberapa langkah dari penyebab masalahnya.

Ketika kita meneruskan *reference* konkret ke `longest`, *lifetime* konkret
yang disubstitusikan untuk `'a` adalah bagian dari *scope* `x` yang tumpang
tindih dengan *scope* `y`. Dengan kata lain, *lifetime* generik `'a` akan
mendapatkan *lifetime* konkret yang sama dengan yang lebih kecil di antara
*lifetime* `x` dan `y`. Karena kita telah menganotasi *reference* yang
dikembalikan dengan parameter *lifetime* `'a` yang sama, *reference* yang
dikembalikan juga akan valid selama yang lebih kecil di antara *lifetime* `x`
dan `y`.

Mari kita lihat bagaimana anotasi *lifetime* membatasi fungsi `longest`
dengan meneruskan *reference* yang memiliki *lifetime* konkret yang berbeda.
Listing 10-22 adalah contoh yang sederhana.

<Listing number="10-22" file-name="src/main.rs" caption="Memakai fungsi `longest` dengan reference ke nilai `String` yang memiliki lifetime konkret berbeda">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

Dalam contoh ini, `string1` valid sampai akhir *scope* luar, `string2` valid
sampai akhir *scope* dalam, dan `result` merujuk sesuatu yang valid sampai
akhir *scope* dalam. Jalankan kode ini dan Anda akan melihat bahwa borrow
checker menyetujuinya; kode itu akan terkompilasi dan mencetak `The longest
string is long string is long`.

Selanjutnya, mari kita coba contoh yang menunjukkan bahwa *lifetime*
*reference* di `result` harus merupakan *lifetime* yang lebih kecil dari kedua
argumen. Kita akan memindahkan deklarasi variable `result` ke luar *scope*
dalam, tetapi membiarkan assignment nilai ke variable `result` di dalam
*scope* bersama `string2`. Kemudian, kita akan memindahkan `println!` yang
memakai `result` ke luar *scope* dalam, setelah *scope* dalam berakhir. Kode di
Listing 10-23 tidak akan terkompilasi.

<Listing number="10-23" file-name="src/main.rs" caption="Mencoba memakai `result` setelah `string2` keluar dari scope">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

Ketika kita mencoba mengompilasi kode ini, kita mendapatkan error berikut:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

Error itu menunjukkan bahwa agar `result` valid untuk statement `println!`,
`string2` harus tetap valid sampai akhir *scope* luar. Rust mengetahui hal ini
karena kita menganotasi *lifetime* parameter fungsi dan return valuenya
memakai parameter *lifetime* `'a` yang sama.

Sebagai manusia, kita bisa melihat kode ini dan mengetahui bahwa `string1`
lebih panjang daripada `string2`, dan karenanya `result` akan berisi
*reference* ke `string1`. Karena `string1` belum keluar dari *scope*, *reference*
ke `string1` masih akan valid untuk statement `println!`. Akan tetapi,
*compiler* tidak bisa melihat bahwa *reference* itu valid dalam kasus ini. Kita
telah memberi tahu Rust bahwa *lifetime* *reference* yang dikembalikan fungsi
`longest` sama dengan yang lebih kecil di antara *lifetime* *reference* yang
diteruskan. Karena itu, *borrow checker* melarang kode di Listing 10-23
sebagai kode yang mungkin memiliki *reference* yang tidak valid.

Cobalah merancang eksperimen lain yang memvariasikan nilai dan *lifetime*
*reference* yang diteruskan ke fungsi `longest` dan bagaimana *reference* yang
dikembalikan dipakai. Buatlah hipotesis tentang apakah eksperimen Anda akan
lolos *borrow checker* sebelum Anda mengompilasinya; lalu, periksalah apakah
tebakan Anda benar!

<!-- Old headings. Do not remove or links may break. -->

<a id="thinking-in-terms-of-lifetimes"></a>

### Hubungan

Cara Anda perlu menentukan parameter *lifetime* bergantung pada apa yang
dilakukan fungsi Anda. Sebagai contoh, jika kita mengubah implementasi
fungsi `longest` agar selalu mengembalikan parameter pertama alih-alih
string *slice* terpanjang, kita tidak perlu menentukan *lifetime* pada parameter
`y`. Kode berikut akan terkompilasi:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

Kita telah menentukan parameter *lifetime* `'a` untuk parameter `x` dan type
kembaliannya, tetapi tidak untuk parameter `y`, karena *lifetime* `y` tidak
memiliki hubungan apa pun dengan *lifetime* `x` atau return valuenya.

Ketika mengembalikan *reference* dari sebuah fungsi, parameter *lifetime* untuk
return type harus cocok dengan parameter *lifetime* salah satu
parameternya. Jika *reference* yang dikembalikan _tidak_ merujuk salah satu
parameter, ia harus merujuk nilai yang dibuat di dalam fungsi ini. Namun,
ini akan menjadi *reference* *dangling* karena nilainya akan keluar dari
*scope* di akhir fungsi. Perhatikan percobaan implementasi fungsi `longest`
ini yang tidak akan terkompilasi:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

Di sini, meskipun kita telah menentukan parameter *lifetime* `'a` untuk type
kembalian, implementasi ini akan gagal terkompilasi karena *lifetime* nilai
kembaliannya tidak berhubungan sama sekali dengan *lifetime* parameternya.
Berikut pesan error yang kita dapatkan:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

Masalahnya, `result` keluar dari *scope* dan dibersihkan di akhir fungsi
`longest`. Kita juga mencoba mengembalikan *reference* ke `result` dari
fungsi itu. Tidak ada cara untuk menentukan parameter *lifetime* yang akan
mengubah *reference* *dangling* itu, dan Rust tidak akan membiarkan kita
membuat *reference* *dangling*. Dalam kasus ini, perbaikan terbaik adalah
mengembalikan data type yang dimiliki alih-alih *reference* sehingga fungsi
pemanggil yang bertanggung jawab membersihkan nilainya.

Pada akhirnya, sintaks *lifetime* adalah tentang menghubungkan *lifetime*
berbagai parameter dan return value fungsi. Setelah mereka terhubung,
Rust memiliki informasi yang cukup untuk mengizinkan operasi yang aman bagi
memori dan melarang operasi yang akan membuat *pointer* *dangling* atau
melanggar memory safety.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-struct-definitions"></a>

### Dalam Definisi Struct

Sejauh ini, semua *struct* yang kita definisikan menampung type yang
dimiliki. Kita bisa mendefinisikan *struct* untuk menampung *reference*, tetapi
dalam kasus itu, kita perlu menambahkan anotasi *lifetime* pada setiap
*reference* di definisi *struct*. Listing 10-24 memiliki *struct* bernama
`ImportantExcerpt` yang menampung sebuah string *slice*.

<Listing number="10-24" file-name="src/main.rs" caption="Struct yang menampung reference, sehingga memerlukan anotasi lifetime">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

*Struct* ini memiliki satu *field* `part` yang menampung sebuah string *slice*,
yang merupakan *reference*. Seperti data generic type, kita mendeklarasikan
nama parameter *lifetime* generik di dalam kurung sudut setelah nama *struct*
supaya kita bisa memakai parameter *lifetime* itu di badan definisi *struct*.
Anotasi ini berarti instance `ImportantExcerpt` tidak bisa hidup lebih lama
daripada *reference* yang ditampungnya di *field* `part`.

Fungsi `main` di sini membuat instance *struct* `ImportantExcerpt` yang
menampung *reference* ke kalimat pertama dari `String` yang dimiliki variable
`novel`. Data di `novel` ada sebelum instance `ImportantExcerpt` dibuat.
Selain itu, `novel` tidak keluar dari *scope* sampai setelah
`ImportantExcerpt` keluar dari *scope*, sehingga *reference* di instance
`ImportantExcerpt` valid.

### Elision Lifetime

Anda telah mempelajari bahwa setiap *reference* memiliki *lifetime* dan bahwa
Anda perlu menentukan parameter *lifetime* untuk fungsi atau *struct* yang
memakai *reference*. Namun, kita memiliki fungsi di Listing 4-9, yang
ditampilkan lagi di Listing 10-25, yang terkompilasi tanpa anotasi *lifetime*.

<Listing number="10-25" file-name="src/lib.rs" caption="Fungsi yang kita definisikan di Listing 4-9 yang terkompilasi tanpa anotasi lifetime, meskipun parameter dan return typenya berupa reference">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

Alasan fungsi ini terkompilasi tanpa anotasi *lifetime* bersifat historis:
pada versi-versi awal (sebelum 1.0) Rust, kode ini tidak akan terkompilasi,
karena setiap *reference* memerlukan *lifetime* eksplisit. Pada masa itu, tanda
tangan fungsinya akan ditulis seperti ini:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Setelah menulis banyak kode Rust, tim Rust menemukan bahwa programmer Rust
memasukkan anotasi *lifetime* yang sama berulang-ulang dalam situasi-situasi
tertentu. Situasi-situasi ini dapat diprediksi dan mengikuti beberapa pattern
deterministik. Para pengembang memprogram pattern-pattern ini ke dalam kode
*compiler* sehingga *borrow checker* bisa menginferensi *lifetime* dalam
situasi-situasi itu tanpa memerlukan anotasi eksplisit.

Sepenggal sejarah Rust ini relevan karena ada kemungkinan lebih banyak pattern
deterministik yang akan muncul dan ditambahkan ke *compiler*. Di masa depan,
anotasi *lifetime* yang diperlukan mungkin menjadi lebih sedikit lagi.

Pattern-pattern yang diprogram ke dalam analisis *reference* Rust disebut
*lifetime elision rules* (aturan elision *lifetime*). Ini bukan aturan yang
harus dipatuhi programmer; ini adalah sekumpulan kasus tertentu yang akan
dipertimbangkan *compiler*, dan jika kode Anda cocok dengan kasus-kasus ini,
Anda tidak perlu menulis *lifetime* secara eksplisit.

Aturan-aturan elision tidak memberikan inferensi penuh. Jika masih ada
ambiguitas tentang *lifetime* yang dimiliki *reference* setelah Rust menerapkan
aturan-aturannya, *compiler* tidak akan menebak *lifetime* *reference* yang
tersisa. Alih-alih menebak, *compiler* akan memberikan error yang bisa Anda
selesaikan dengan menambahkan anotasi *lifetime*.

*Lifetime* pada parameter fungsi atau method disebut *input lifetime*
(*lifetime* input), dan *lifetime* pada return value disebut *output
lifetime* (*lifetime* output).

*Compiler* memakai tiga aturan untuk mengetahui *lifetime* *reference* ketika
tidak ada anotasi eksplisit. Aturan pertama berlaku untuk *lifetime* input,
dan aturan kedua serta ketiga berlaku untuk *lifetime* output. Jika *compiler*
sudah sampai di akhir ketiga aturan dan masih ada *reference* yang
*lifetime*-nya tidak bisa ia ketahui, *compiler* akan berhenti dengan sebuah
error. Aturan-aturan ini berlaku untuk definisi `fn` maupun blok `impl`.

Aturan pertama adalah *compiler* menetapkan sebuah parameter *lifetime* untuk
setiap parameter yang berupa *reference*. Dengan kata lain, fungsi dengan
satu parameter mendapatkan satu parameter *lifetime*: `fn foo<'a>(x: &'a
i32)`; fungsi dengan dua parameter mendapatkan dua parameter *lifetime*
terpisah: `fn foo<'a, 'b>(x: &'a i32, y: &'b i32)`; dan seterusnya.

Aturan kedua adalah, jika ada tepat satu parameter *lifetime* input,
*lifetime* itu ditetapkan untuk semua parameter *lifetime* output: `fn
foo<'a>(x: &'a i32) -> &'a i32`.

Aturan ketiga adalah, jika ada beberapa parameter *lifetime* input, tetapi
salah satunya adalah `&self` atau `&mut self` karena ini adalah method,
*lifetime* `self` ditetapkan untuk semua parameter *lifetime* output. Aturan
ketiga ini membuat method jauh lebih enak dibaca dan ditulis karena lebih
sedikit simbol yang diperlukan.

Mari kita berperan sebagai *compiler*. Kita akan menerapkan aturan-aturan ini
untuk mengetahui *lifetime* *reference* di *signature* fungsi `first_word`
pada Listing 10-25. Tanda tangan itu dimulai tanpa *lifetime* apa pun yang
dikaitkan dengan *reference*:

```rust,ignore
fn first_word(s: &str) -> &str {
```

Kemudian, *compiler* menerapkan aturan pertama, yang menentukan bahwa setiap
parameter mendapatkan *lifetime*-nya sendiri. Kita akan menamainya `'a`
seperti biasa, jadi sekarang *signature*nya seperti ini:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

Aturan kedua berlaku karena ada tepat satu *lifetime* input. Aturan kedua
menentukan bahwa *lifetime* dari satu parameter input itu ditetapkan ke
*lifetime* output, jadi *signature*nya sekarang seperti ini:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Sekarang semua *reference* di *signature* fungsi ini memiliki *lifetime*, dan
*compiler* bisa melanjutkan analisisnya tanpa perlu programmer menganotasi
*lifetime* di *signature* fungsi ini.

Mari kita lihat contoh lain, kali ini memakai fungsi `longest` yang tidak
memiliki parameter *lifetime* ketika kita mulai mengerjakannya di Listing
10-20:

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

Mari kita terapkan aturan pertama: setiap parameter mendapatkan
*lifetime*-nya sendiri. Kali ini kita memiliki dua parameter alih-alih satu,
jadi kita memiliki dua *lifetime*:

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

Anda bisa melihat bahwa aturan kedua tidak berlaku, karena ada lebih dari
satu *lifetime* input. Aturan ketiga juga tidak berlaku, karena `longest`
adalah fungsi alih-alih method, jadi tidak ada parameternya yang berupa
`self`. Setelah melewati ketiga aturan, kita masih belum tahu berapa
*lifetime* return typenya. Inilah alasan kita mendapatkan error ketika
mencoba mengompilasi kode di Listing 10-20: *compiler* telah melewati
aturan-aturan elision *lifetime*, tetapi masih belum bisa mengetahui semua
*lifetime* *reference* di *signature* itu.

Karena aturan ketiga sebenarnya hanya berlaku di *signature* method, kita
akan melihat *lifetime* dalam konteks itu berikutnya untuk memahami alasan
aturan ketiga membuat kita tidak perlu menganotasi *lifetime* di *signature*
method terlalu sering.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-method-definitions"></a>

### Dalam Definisi Method

Ketika kita mengimplementasikan method pada *struct* yang memiliki *lifetime*,
kita memakai sintaks yang sama seperti sintaks type parameter generik,
seperti yang ditunjukkan di Listing 10-11. Tempat kita mendeklarasikan dan
memakai parameter *lifetime* bergantung pada apakah parameter itu terkait
dengan *field* *struct* atau dengan parameter dan return value method.

Nama-nama *lifetime* untuk *field* *struct* selalu perlu dideklarasikan setelah
*keyword* `impl`, lalu dipakai setelah nama *struct*, karena *lifetime*
tersebut merupakan bagian dari type *struct*.

Di *signature* method dalam blok `impl`, *reference* mungkin terikat dengan
*lifetime* *reference* di *field* *struct*, atau mungkin independen. Selain itu,
aturan-aturan elision *lifetime* sering membuat anotasi *lifetime* tidak
diperlukan di *signature* method. Mari kita lihat beberapa contoh memakai
*struct* bernama `ImportantExcerpt` yang kita definisikan di Listing 10-24.

Pertama, kita akan memakai method bernama `level` yang satu-satunya
parameternya adalah *reference* ke `self` dan return valuenya berupa
`i32`, yang bukan *reference* ke apa pun:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

Deklarasi parameter *lifetime* setelah `impl` dan pemakaiannya setelah nama
type itu wajib, tetapi karena aturan elision pertama, kita tidak wajib
menganotasi *lifetime* *reference* ke `self`.

Berikut contoh ketika aturan elision *lifetime* ketiga berlaku:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

Ada dua *lifetime* input, jadi Rust menerapkan aturan elision *lifetime*
pertama dan memberikan *lifetime* masing-masing kepada `&self` dan
`announcement`. Kemudian, karena salah satu parameternya adalah `&self`,
return typenya mendapatkan *lifetime* `&self`, dan semua *lifetime* telah
terhitung.

### Lifetime Static

Satu *lifetime* khusus yang perlu kita bahas adalah `'static`, yang
menandakan bahwa *reference* yang terdampak _bisa_ hidup selama keseluruhan
durasi program. Semua *string literal* memiliki *lifetime* `'static`, yang bisa
kita anotasi sebagai berikut:

```rust
let s: &'static str = "I have a static lifetime.";
```

Teks string ini disimpan langsung di binary program, yang selalu tersedia.
Karena itu, *lifetime* semua *string literal* adalah `'static`.

Anda mungkin melihat saran di pesan error untuk memakai *lifetime* `'static`.
Namun, sebelum menentukan `'static` sebagai *lifetime* untuk sebuah
*reference*, pikirkan apakah *reference* yang Anda miliki benar-benar hidup
selama seluruh masa program Anda, dan apakah Anda menginginkannya. Sebagian
besar waktu, pesan error yang menyarankan *lifetime* `'static` muncul akibat
percobaan membuat *reference* *dangling* atau ketidakcocokan *lifetime* yang
tersedia. Dalam kasus seperti itu, solusinya adalah memperbaiki masalah
tersebut, bukan menentukan *lifetime* `'static`.

<!-- Old headings. Do not remove or links may break. -->

<a id="generic-type-parameters-trait-bounds-and-lifetimes-together"></a>

## Parameter Type Generik, Trait Bound, dan Lifetime

Mari kita lihat sekilas sintaks menentukan type parameter generik, *trait*
bound, dan *lifetime* semuanya dalam satu fungsi!

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

Ini adalah fungsi `longest` dari Listing 10-21 yang mengembalikan yang
lebih panjang dari dua string *slice*. Namun, sekarang ia memiliki parameter
tambahan bernama `ann` typed generik `T`, yang bisa diisi oleh type apa
pun yang mengimplementasikan *trait* `Display` seperti yang ditentukan oleh
klausa `where`. Parameter tambahan ini akan dicetak memakai `{}`, dan
itulah alasan *trait bound* `Display` diperlukan. Karena *lifetime* adalah
salah satu jenis generik, deklarasi parameter *lifetime* `'a` dan parameter
generic type `T` berada di daftar yang sama di dalam kurung sudut setelah
nama fungsi.

## Ringkasan

Banyak yang telah kita bahas dalam bab ini! Sekarang setelah Anda tahu
tentang type parameter generik, *trait* dan *trait bound*, serta parameter
*lifetime* generik, Anda siap menulis kode tanpa pengulangan yang berfungsi
dalam banyak situasi berbeda. Parameter generic type memungkinkan Anda
menerapkan kode ke berbagai type. *Trait* dan *trait bound* memastikan bahwa
meskipun type-typenya generik, mereka akan memiliki perilaku yang
dibutuhkan kode. Anda telah mempelajari cara memakai anotasi *lifetime* untuk
memastikan bahwa kode fleksibel ini tidak memiliki *reference* *dangling*.
Dan semua analisis ini terjadi pada waktu kompilasi, yang tidak memengaruhi
kinerja *runtime*!

Percaya atau tidak, masih banyak yang harus dipelajari tentang topik yang
kita bahas di bab ini: Bab 18 membahas *trait object* (objek *trait*), yang
merupakan cara lain untuk memakai *trait*. Ada juga skenario yang lebih
kompleks yang melibatkan anotasi *lifetime* yang hanya Anda perlukan dalam
skenario yang sangat lanjut; untuk itu, Anda sebaiknya membaca [Rust
*Reference*][reference]. Namun selanjutnya, Anda akan mempelajari cara
menulis test di Rust supaya Anda bisa memastikan bahwa kode Anda
berjalan sebagaimana mestinya.

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[string-slices-as-parameters]: ch04-03-slices.html#string-slices-as-parameters
[reference]: ../reference/trait-bounds.html
