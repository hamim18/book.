## Menyimpan Teks Terenkode UTF-8 dengan String

Kita telah membicarakan string di Bab 4, tetapi sekarang kita akan
melihatnya lebih mendalam. Rustacean baru biasanya tersangkut pada string
karena kombinasi tiga alasan: kecenderungan Rust untuk mengekspos
kemungkinan galat, string sebagai struktur data yang lebih rumit daripada
perkiraan banyak pemrogram, dan UTF-8. Faktor-faktor ini berpadu dengan cara
yang bisa terasa sulit ketika Anda datang dari bahasa pemrograman lain.

Kita membahas string dalam konteks koleksi karena string diimplementasikan
sebagai koleksi byte, ditambah beberapa metode untuk menyediakan
fungsionalitas yang berguna ketika byte-byte itu ditafsirkan sebagai teks.
Di bagian ini, kita akan membicarakan operasi-operasi pada `String` yang
dimiliki setiap tipe koleksi, seperti membuat, memperbarui, dan membaca.
Kita juga akan membahas cara-cara `String` berbeda dari koleksi lainnya,
yaitu bagaimana pengindeksan ke dalam `String` menjadi rumit karena
perbedaan antara cara manusia dan komputer menafsirkan data `String`.

<!-- Old headings. Do not remove or links may break. -->

<a id="what-is-a-string"></a>

### Mendefinisikan String

Pertama-tama, kita akan mendefinisikan apa yang kita maksud dengan istilah
*string*. Rust hanya memiliki satu tipe string di bahasa intinya, yaitu
string slice `str` yang biasanya terlihat dalam bentuk pinjamannya, `&str`.
Di Bab 4, kita membicarakan string slice, yang merupakan reference ke
sebagian data string terenkode UTF-8 yang tersimpan di tempat lain. String
literal, misalnya, tersimpan di binary program dan karena itu adalah string
slice.

Tipe `String`, yang disediakan oleh pustaka standar Rust alih-alih
dikodekan ke dalam bahasa inti, adalah tipe string yang dapat membesar,
mutable, dimiliki, dan terenkode UTF-8. Ketika para Rustacean merujuk
“string” di Rust, mereka mungkin merujuk ke tipe `String` atau string slice
`&str`, bukan hanya salah satu dari tipe-tipe itu. Meskipun bagian ini
sebagian besar tentang `String`, kedua tipe dipakai secara besar-besaran di
pustaka standar Rust, dan baik `String` maupun string slice sama-sama
terenkode UTF-8.

### Membuat String Baru

Banyak operasi yang sama yang tersedia pada `Vec<T>` juga tersedia pada
`String`, karena `String` sebenarnya diimplementasikan sebagai *wrapper*
(pembungkus) di sekitar vektor byte dengan beberapa jaminan, pembatasan, dan
kemampuan ekstra. Contoh fungsi yang bekerja dengan cara yang sama pada
`Vec<T>` dan `String` adalah fungsi `new` untuk membuat sebuah instance,
yang ditunjukkan di Listing 8-11.

<Listing number="8-11" caption="Membuat `String` kosong yang baru">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

Baris ini membuat string kosong baru bernama `s`, yang kemudian dapat kita
isi dengan data. Sering kali, kita akan memiliki data awal yang ingin kita
pakai untuk memulai string. Untuk itu, kita memakai metode `to_string`, yang
tersedia pada tipe apa pun yang mengimplementasikan *trait* `Display`,
seperti halnya string literal. Listing 8-12 menunjukkan dua contoh.

<Listing number="8-12" caption="Memakai metode `to_string` untuk membuat `String` dari string literal">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

Kode ini membuat string berisi `initial contents`.

Kita juga dapat memakai fungsi `String::from` untuk membuat `String` dari
string literal. Kode di Listing 8-13 setara dengan kode di Listing 8-12 yang
memakai `to_string`.

<Listing number="8-13" caption="Memakai fungsi `String::from` untuk membuat `String` dari string literal">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

Karena string dipakai untuk begitu banyak hal, kita dapat memakai banyak API
generik yang berbeda untuk string, yang memberi kita banyak pilihan.
Sebagian di antaranya bisa terlihat mubazir, tetapi semuanya punya
tempatnya masing-masing! Dalam kasus ini, `String::from` dan `to_string`
melakukan hal yang sama, jadi pilihan Anda adalah soal gaya dan
keterbacaan.

Ingat bahwa string terenkode UTF-8, jadi kita dapat menyertakan data apa pun
yang terenkode dengan benar di dalamnya, seperti yang ditunjukkan di Listing
8-14.

<Listing number="8-14" caption="Menyimpan sapaan dalam berbagai bahasa di dalam string">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

Semua nilai ini adalah nilai `String` yang valid.

### Memperbarui String

Sebuah `String` dapat membesar ukurannya dan isinya dapat berubah, sama
seperti isi `Vec<T>`, jika Anda memasukkan lebih banyak data ke dalamnya.
Selain itu, Anda dapat dengan mudah memakai operator `+` atau *macro*
(makro) `format!` untuk menggabungkan nilai-nilai `String`.

<!-- Old headings. Do not remove or links may break. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### Menambahkan dengan `push_str` atau `push`

Kita dapat memperbesar `String` dengan memakai metode `push_str` untuk
menambahkan sebuah string slice, seperti yang ditunjukkan di Listing 8-15.

<Listing number="8-15" caption="Menambahkan sebuah string slice ke `String` memakai metode `push_str`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

Setelah dua baris ini, `s` akan berisi `foobar`. Metode `push_str` menerima
string slice karena kita belum tentu ingin mengambil ownership parameter.
Misalnya, pada kode di Listing 8-16, kita ingin dapat memakai `s2` setelah
menambahkan isinya ke `s1`.

<Listing number="8-16" caption="Memakai string slice setelah menambahkan isinya ke `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

Jika metode `push_str` mengambil ownership `s2`, kita tidak akan dapat
mencetak nilainya di baris terakhir. Namun, kode ini bekerja seperti yang
kita harapkan!

Metode `push` menerima satu karakter sebagai parameter dan menambahkannya ke
`String`. Listing 8-17 menambahkan huruf _l_ ke sebuah `String` memakai
metode `push`.

<Listing number="8-17" caption="Menambahkan satu karakter ke nilai `String` memakai `push`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

Akibatnya, `s` akan berisi `lol`.

<!-- Old headings. Do not remove or links may break. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

#### Menggabungkan dengan `+` atau `format!`

Sering kali, Anda ingin menggabungkan dua string yang ada. Salah satu
caranya adalah memakai operator `+`, seperti yang ditunjukkan di Listing
8-18.

<Listing number="8-18" caption="Memakai operator `+` untuk menggabungkan dua nilai `String` menjadi nilai `String` baru">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

String `s3` akan berisi `Hello, world!`. Alasan `s1` tidak lagi valid
setelah penambahan, dan alasan kita memakai reference ke `s2`, berkaitan
dengan tanda tangan metode yang dipanggil ketika kita memakai operator `+`.
Operator `+` memakai metode `add`, yang tanda tangannya terlihat seperti
ini:

```rust,ignore
fn add(self, s: &str) -> String {
```

Di pustaka standar, Anda akan melihat `add` didefinisikan memakai generics
dan tipe asosiasi. Di sini, kita telah menggantinya dengan tipe konkret,
yang memang terjadi ketika kita memanggil metode ini dengan nilai `String`.
Kita akan membahas generics di Bab 10. Tanda tangan ini memberi kita
petunjuk yang kita perlukan untuk memahami bagian-bagian rumit dari operator
`+`.

Pertama, `s2` memiliki `&`, yang berarti kita menambahkan sebuah reference
ke string kedua ke string pertama. Ini karena parameter `s` di fungsi
`add`: kita hanya dapat menambahkan string slice ke `String`; kita tidak
dapat menjumlahkan dua nilai `String`. Tapi tunggu—tipe `&s2` adalah
`&String`, bukan `&str`, seperti yang disebutkan di parameter kedua `add`.
Jadi, mengapa Listing 8-18 bisa dikompilasi?

Alasan kita dapat memakai `&s2` di pemanggilan `add` adalah bahwa compiler
dapat mengoersi argumen `&String` menjadi `&str`. Ketika kita memanggil
metode `add`, Rust memakai deref coercion, yang di sini mengubah `&s2`
menjadi `&s2[..]`. Kita akan membahas deref coercion lebih mendalam di Bab
15. Karena `add` tidak mengambil ownership parameter `s`, `s2` akan tetap
menjadi `String` yang valid setelah operasi ini.

Kedua, kita dapat melihat di tanda tangan bahwa `add` mengambil ownership
`self` karena `self` _tidak_ memiliki `&`. Ini berarti `s1` di Listing 8-18
akan dipindahkan ke dalam pemanggilan `add` dan tidak lagi valid setelahnya.
Jadi, meskipun `let s3 = s1 + &s2;` terlihat seperti menyalin kedua string
dan membuat yang baru, pernyataan ini sebenarnya mengambil ownership `s1`,
menambahkan salinan isi `s2`, lalu mengembalikan ownership hasilnya. Dengan
kata lain, ia terlihat membuat banyak salinan, tetapi tidak;
implementasinya lebih efisien daripada menyalin.

Jika kita perlu menggabungkan banyak string, perilaku operator `+` menjadi
sulit dikendalikan:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

Pada titik ini, `s` akan menjadi `tic-tac-toe`. Dengan semua karakter `+`
dan `"`, sulit untuk melihat apa yang sedang terjadi. Untuk menggabungkan
string dengan cara yang lebih rumit, kita dapat memakai macro `format!`:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

Kode ini juga menetapkan `s` menjadi `tic-tac-toe`. Macro `format!` bekerja
seperti `println!`, tetapi alih-alih mencetak output ke layar, ia
mengembalikan `String` berisi kontennya. Versi kode yang memakai `format!`
jauh lebih mudah dibaca, dan kode yang dihasilkan macro `format!` memakai
reference sehingga pemanggilan ini tidak mengambil ownership parameter mana
pun.

### Mengindeks ke dalam String

Di banyak bahasa pemrograman lain, mengakses karakter individual di string
dengan merujuknya lewat indeks adalah operasi yang valid dan umum. Namun,
jika Anda mencoba mengakses bagian-bagian `String` memakai sintaks
pengindeksan di Rust, Anda akan mendapat galat. Perhatikan kode tidak valid
di Listing 8-19.

<Listing number="8-19" caption="Mencoba memakai sintaks pengindeksan dengan `String`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

Kode ini akan menghasilkan galat berikut:

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

Galat ini menceritakan semuanya: string Rust tidak mendukung pengindeksan.
Tetapi mengapa tidak? Untuk menjawab pertanyaan itu, kita perlu membahas
cara Rust menyimpan string di memori.

#### Representasi Internal

Sebuah `String` adalah wrapper di atas `Vec<u8>`. Mari kita lihat sebagian
contoh string UTF-8 yang terenkode dengan benar dari Listing 8-14. Pertama,
yang ini:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

Dalam kasus ini, `len` akan menjadi `4`, yang berarti vektor yang menyimpan
string `"Hola"` panjangnya 4 byte. Setiap huruf ini memakan 1 byte ketika
dienkode dalam UTF-8. Namun, baris berikut mungkin mengejutkan Anda
(perhatikan bahwa string ini dimulai dengan huruf kapital Sirilik _Ze_,
bukan angka 3):

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

Jika Anda ditanya berapa panjang string tersebut, Anda mungkin menjawab 12.
Kenyataannya, jawaban Rust adalah 24: itulah jumlah byte yang dibutuhkan
untuk mengodekan “Здравствуйте” dalam UTF-8, karena setiap nilai skalar
Unicode di string itu memakan 2 byte penyimpanan. Karena itu, sebuah indeks
ke dalam byte-byte string tidak selalu berkorelasi dengan nilai skalar
Unicode yang valid. Untuk mendemonstrasikannya, perhatikan kode Rust tidak
valid ini:

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

Anda sudah tahu bahwa `answer` tidak akan menjadi `З`, huruf pertama.
Ketika dienkode dalam UTF-8, byte pertama `З` adalah `208` dan yang kedua
`151`, jadi sepertinya `answer` seharusnya menjadi `208`, tetapi `208`
sendiri bukan karakter yang valid. Mengembalikan `208` kemungkinan besar
bukan yang diinginkan pengguna jika mereka meminta huruf pertama string ini;
namun, itulah satu-satunya data yang dimiliki Rust pada indeks byte 0.
Pengguna umumnya tidak ingin nilai byte dikembalikan, bahkan jika stringnya
hanya berisi huruf Latin: jika `&"hi"[0]` adalah kode valid yang
mengembalikan nilai byte, ia akan mengembalikan `104`, bukan `h`.

Jawabannya, dengan demikian, adalah bahwa untuk menghindari pengembalian
nilai yang tidak diharapkan dan menyebabkan bug yang mungkin tidak segera
ditemukan, Rust sama sekali tidak mengompilasi kode ini dan mencegah
kesalahpahaman sejak awal proses pengembangan.

<!-- Old headings. Do not remove or links may break. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### Byte, Nilai Skalar, dan Grapheme Cluster

Poin lain tentang UTF-8 adalah bahwa sebenarnya ada tiga cara relevan untuk
melihat string dari sudut pandang Rust: sebagai byte, nilai skalar, dan
*grapheme cluster* (klaster grafem) (hal yang paling dekat dengan apa yang
kita sebut _huruf_).

Jika kita melihat kata Hindi “नमस्ते” yang ditulis dalam aksara Devanagari,
kata itu tersimpan sebagai vektor berisi nilai `u8` yang terlihat seperti
ini:

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

Itu 18 byte dan itulah cara komputer pada akhirnya menyimpan data ini. Jika
kita melihatnya sebagai nilai skalar Unicode, yang merupakan tipe `char`
Rust, byte-byte itu terlihat seperti ini:

```text
['न', 'म', 'स', '्', 'त', 'े']
```

Ada enam nilai `char` di sini, tetapi yang keempat dan keenam bukan huruf:
keduanya adalah diakritik yang tidak bermakna jika berdiri sendiri.
Terakhir, jika kita melihatnya sebagai grapheme cluster, kita akan
mendapatkan apa yang orang sebut sebagai empat huruf yang menyusun kata
Hindi itu:

```text
["न", "म", "स्", "ते"]
```

Rust menyediakan berbagai cara menafsirkan data string mentah yang disimpan
komputer sehingga setiap program dapat memilih tafsiran yang dibutuhkannya,
apa pun bahasa manusia yang dipakai data itu.

Alasan terakhir Rust tidak mengizinkan kita mengindeks ke dalam `String`
untuk mendapatkan karakter adalah bahwa operasi pengindeksan diharapkan
selalu memakan waktu konstan (O(1)). Tetapi tidak mungkin menjamin kinerja
itu dengan `String`, karena Rust harus menelusuri isinya dari awal sampai
indeks itu untuk menentukan berapa banyak karakter valid yang ada.

### Membuat Slice pada String

Mengindeks ke dalam string sering kali merupakan ide buruk karena tidak
jelas tipe kembalian operasi pengindeksan string seharusnya apa: nilai
byte, karakter, grapheme cluster, atau string slice. Jika Anda benar-benar
perlu memakai indeks untuk membuat string slice, maka Rust meminta Anda
untuk lebih spesifik.

Alih-alih mengindeks memakai `[]` dengan satu angka, Anda dapat memakai
`[]` dengan sebuah range untuk membuat string slice yang berisi byte-byte
tertentu:

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

Di sini, `s` akan menjadi `&str` yang berisi 4 byte pertama string.
Sebelumnya, kita menyebutkan bahwa setiap karakter ini berukuran 2 byte,
yang berarti `s` akan menjadi `Зд`.

Jika kita mencoba memotong hanya sebagian byte sebuah karakter dengan
sesuatu seperti `&hello[0..1]`, Rust akan panic pada runtime dengan cara
yang sama seperti jika indeks tidak valid diakses di vektor:

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

Anda harus berhati-hati saat membuat string slice dengan range, karena
melakukannya dapat membuat program Anda crash.

<!-- Old headings. Do not remove or links may break. -->

<a id="methods-for-iterating-over-strings"></a>

### Mengiterasi String

Cara terbaik untuk mengoperasikan potongan-potongan string adalah dengan
eksplisit tentang apakah Anda menginginkan karakter atau byte. Untuk nilai
skalar Unicode individual, pakai metode `chars`. Memanggil `chars` pada
“Зд” memisahkan dan mengembalikan dua nilai bertipe `char`, dan Anda dapat
mengiterasi hasilnya untuk mengakses setiap elemen:

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

Kode ini akan mencetak yang berikut:

```text
З
д
```

Sebagai alternatif, metode `bytes` mengembalikan setiap byte mentah, yang
mungkin cocok untuk domain Anda:

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

Kode ini akan mencetak 4 byte yang menyusun string ini:

```text
208
151
208
180
```

Tetapi pastikan untuk mengingat bahwa nilai skalar Unicode yang valid bisa
tersusun dari lebih dari 1 byte.

Mendapatkan grapheme cluster dari string, seperti pada aksara Devanagari,
itu rumit, sehingga fungsionalitas ini tidak disediakan oleh pustaka
standar. Crate-crate tersedia di [crates.io](https://crates.io/)<!-- ignore
--> jika ini fungsionalitas yang Anda butuhkan.

<!-- Old headings. Do not remove or links may break. -->

<a id="strings-are-not-so-simple"></a>

### Menangani Kerumitan String

Ringkasnya, string itu rumit. Bahasa pemrograman yang berbeda membuat
pilihan yang berbeda tentang cara menyajikan kerumitan ini kepada pemrogram.
Rust telah memilih untuk menjadikan penanganan data `String` yang benar
sebagai perilaku default untuk semua program Rust, yang berarti pemrogram
harus lebih banyak berpikir untuk menangani data UTF-8 sejak awal. Kompromi
ini mengekspos lebih banyak kerumitan string daripada yang tampak di bahasa
pemrograman lain, tetapi ia mencegah Anda harus menangani galat yang
melibatkan karakter non-ASCII di kemudian hari dalam siklus hidup
pengembangan Anda.

Kabar baiknya adalah pustaka standar menawarkan banyak fungsionalitas yang
dibangun di atas tipe `String` dan `&str` untuk membantu menangani
situasi-situasi rumit ini dengan benar. Pastikan untuk memeriksa
dokumentasinya untuk metode-metode bermanfaat seperti `contains` untuk
mencari di dalam string dan `replace` untuk mengganti bagian string dengan
string lain.

Mari kita beralih ke sesuatu yang sedikit kurang rumit: hash map!
