## Fungsi

Fungsi ada di mana-mana dalam kode Rust. Anda telah melihat salah satu fungsi
terpenting dalam bahasa ini: fungsi `main`, yang merupakan titik masuk banyak
program. Anda juga telah melihat keyword `fn`, yang memungkinkan Anda
mendeklarasikan fungsi baru.

Kode Rust memakai _snake case_ sebagai gaya konvensional untuk nama fungsi dan
variabel, yaitu semua hurufnya ditulis kecil dan kata-katanya dipisahkan garis
bawah. Berikut program yang berisi contoh definisi fungsi:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

Kita mendefinisikan fungsi di Rust dengan menuliskan `fn` yang diikuti nama
fungsi dan sepasang tanda kurung. Kurung kurawalnya memberi tahu *compiler* di
mana badan fungsi dimulai dan diakhiri.

Kita dapat memanggil fungsi apa pun yang telah kita definisikan dengan
menuliskan namanya yang diikuti sepasang tanda kurung. Karena
`another_function` sudah didefinisikan di dalam program, ia dapat dipanggil
dari dalam fungsi `main`. Perhatikan bahwa kita mendefinisikan
`another_function` _setelah_ fungsi `main` di kode sumber; kita juga bisa
mendefinisikannya sebelumnya. Rust tidak peduli di mana Anda mendefinisikan
fungsi Anda, yang penting fungsi itu didefinisikan di suatu tempat dalam
*scope* (cakupan) yang dapat dilihat oleh pemanggilnya.

Mari kita mulai proyek binary baru bernama _functions_ untuk mengeksplorasi
fungsi lebih jauh. Letakkan contoh `another_function` di _src/main.rs_ dan
jalankan. Anda seharusnya melihat keluaran berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

Baris-baris itu dieksekusi sesuai urutan kemunculannya di dalam fungsi `main`.
Pertama, pesan “Hello, world!” dicetak, lalu `another_function` dipanggil dan
pesannya dicetak.

### Parameter

Kita dapat mendefinisikan fungsi agar memiliki parameter, yaitu variabel khusus
yang menjadi bagian dari tanda tangan sebuah fungsi. Ketika sebuah fungsi
memiliki parameter, Anda dapat memberikannya nilai konkret untuk
parameter-parameter tersebut. Secara teknis, nilai konkret itu disebut
argumen, tetapi dalam percakapan sehari-hari, orang cenderung memakai kata
parameter dan argumen secara bergantian, baik untuk variabel di dalam definisi
fungsi maupun nilai konkret yang diberikan ketika Anda memanggil fungsi.

Pada versi `another_function` ini kita menambahkan sebuah parameter:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

Coba jalankan program ini; Anda seharusnya mendapatkan keluaran berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

Deklarasi `another_function` memiliki satu parameter bernama `x`. Tipe `x`
ditentukan sebagai `i32`. Ketika kita meneruskan `5` ke `another_function`,
*macro* (makro) `println!` meletakkan `5` pada posisi pasangan kurung kurawal
berisi `x` di dalam string format.

Dalam tanda tangan fungsi, Anda _harus_ mendeklarasikan tipe setiap parameter.
Ini adalah keputusan yang disengaja dalam desain Rust: mewajibkan anotasi tipe
dalam definisi fungsi berarti *compiler* hampir tidak pernah meminta Anda
memakainya di bagian lain kode untuk mengetahui tipe yang Anda maksud.
*Compiler* juga mampu memberikan pesan error yang lebih membantu jika ia tahu
tipe apa yang diharapkan fungsi tersebut.

Ketika mendefinisikan beberapa parameter, pisahkan deklarasi parameternya
dengan koma, seperti ini:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

Contoh ini membuat fungsi bernama `print_labeled_measurement` dengan dua
parameter. Parameter pertama bernama `value` dan bertipe `i32`. Parameter
kedua bernama `unit_label` dan bertipe `char`. Fungsi itu lalu mencetak teks
yang berisi `value` maupun `unit_label`.

Mari kita coba menjalankan kode ini. Ganti program yang saat ini ada di file
_src/main.rs_ proyek _functions_ Anda dengan contoh sebelumnya, lalu jalankan
dengan `cargo run`:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

Karena kita memanggil fungsi itu dengan `5` sebagai nilai untuk `value` dan
`'h'` sebagai nilai untuk `unit_label`, keluaran program memuat nilai-nilai
tersebut.

### Pernyataan dan Ekspresi

Badan fungsi tersusun dari serangkaian pernyataan yang secara opsional diakhiri
sebuah ekspresi. Sejauh ini, fungsi-fungsi yang telah kita bahas tidak
menyertakan ekspresi penutup, tetapi Anda telah melihat ekspresi sebagai bagian
dari sebuah pernyataan. Karena Rust adalah bahasa berbasis ekspresi, ini adalah
pembedaan penting untuk dipahami. Bahasa lain tidak memiliki pembedaan yang
sama, jadi mari kita lihat apa itu pernyataan dan ekspresi serta bagaimana
perbedaan keduanya memengaruhi badan fungsi.

- _Pernyataan_ adalah instruksi yang melakukan suatu tindakan dan tidak
  mengembalikan nilai.
- _Ekspresi_ mengevaluasi menjadi sebuah nilai hasil.

Mari kita lihat beberapa contoh.

Sebenarnya kita sudah memakai pernyataan dan ekspresi. Membuat variabel dan
menetapkan nilai padanya dengan keyword `let` adalah sebuah pernyataan. Pada
Listing 3-1, `let y = 6;` adalah sebuah pernyataan.

<Listing number="3-1" file-name="src/main.rs" caption="Deklarasi fungsi `main` yang berisi satu pernyataan">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

Definisi fungsi juga merupakan pernyataan; keseluruhan contoh sebelumnya itu
sendiri adalah sebuah pernyataan. (Seperti yang akan kita lihat sebentar lagi,
memanggil fungsi bukanlah pernyataan.)

Pernyataan tidak mengembalikan nilai. Karena itu, Anda tidak dapat menetapkan
pernyataan `let` ke variabel lain, seperti yang coba dilakukan kode berikut;
Anda akan mendapatkan error:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

Ketika Anda menjalankan program ini, error yang Anda dapatkan terlihat seperti
ini:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

Pernyataan `let y = 6` tidak mengembalikan nilai, jadi tidak ada apa pun yang
dapat diikat oleh `x`. Ini berbeda dari yang terjadi pada bahasa lain, seperti
C dan Ruby, di mana penetapan mengembalikan nilai dari penetapan tersebut.
Pada bahasa-bahasa itu, Anda dapat menulis `x = y = 6` dan membuat `x` maupun
`y` sama-sama bernilai `6`; hal itu tidak berlaku di Rust.

Ekspresi mengevaluasi menjadi sebuah nilai dan membentuk sebagian besar sisa
kode yang akan Anda tulis di Rust. Perhatikan sebuah operasi matematika,
seperti `5 + 6`, yang merupakan ekspresi yang mengevaluasi menjadi nilai `11`.
Ekspresi dapat menjadi bagian dari pernyataan: Pada Listing 3-1, `6` di dalam
pernyataan `let y = 6;` adalah ekspresi yang mengevaluasi menjadi nilai `6`.
Memanggil fungsi adalah ekspresi. Memanggil *macro* adalah ekspresi. Blok *scope*
baru yang dibuat dengan kurung kurawal adalah ekspresi, contohnya:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

Ekspresi ini:

```rust,ignore
{
    let x = 3;
    x + 1
}
```

adalah sebuah blok yang, pada kasus ini, mengevaluasi menjadi `4`. Nilai itu
diikat ke `y` sebagai bagian dari pernyataan `let`. Perhatikan baris `x + 1`
tanpa titik koma di akhirnya, berbeda dengan sebagian besar baris yang telah
Anda lihat sejauh ini. Ekspresi tidak menyertakan titik koma penutup. Jika
Anda menambahkan titik koma di akhir sebuah ekspresi, Anda mengubahnya menjadi
pernyataan, dan ia pun tidak akan mengembalikan nilai. Ingatlah hal ini ketika
Anda mengeksplorasi nilai kembalian fungsi dan ekspresi berikutnya.

### Fungsi dengan Nilai Kembalian

Fungsi dapat mengembalikan nilai kepada kode yang memanggilnya. Kita tidak
menamai nilai kembalian, tetapi kita harus mendeklarasikan tipenya setelah
tanda panah (`->`). Di Rust, nilai kembalian sebuah fungsi sama artinya dengan
nilai ekspresi terakhir di dalam blok badan fungsi. Anda dapat keluar lebih
awal dari sebuah fungsi dengan memakai keyword `return` dan menyebutkan sebuah
nilai, tetapi sebagian besar fungsi mengembalikan ekspresi terakhirnya secara
implisit. Berikut contoh fungsi yang mengembalikan nilai:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

Tidak ada pemanggilan fungsi, *macro*, ataupun pernyataan `let` di dalam fungsi
`five`—hanya angka `5` itu sendiri. Itu adalah fungsi yang sepenuhnya valid di
Rust. Perhatikan bahwa tipe kembalian fungsinya juga ditentukan, yaitu
`-> i32`. Coba jalankan kode ini; keluarannya seharusnya terlihat seperti ini:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

`5` di dalam `five` adalah nilai kembalian fungsi tersebut, itulah sebabnya
tipe kembaliannya adalah `i32`. Mari kita telaah lebih mendetail. Ada dua hal
penting: Pertama, baris `let x = five();` menunjukkan bahwa kita memakai nilai
kembalian sebuah fungsi untuk menginisialisasi sebuah variabel. Karena fungsi
`five` mengembalikan `5`, baris itu sama dengan berikut ini:

```rust
let x = 5;
```

Kedua, fungsi `five` tidak memiliki parameter dan mendefinisikan tipe nilai
kembaliannya, tetapi badan fungsinya hanyalah `5` sendirian tanpa titik koma
karena ia adalah ekspresi yang nilainya ingin kita kembalikan.

Mari kita lihat contoh lain:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

Menjalankan kode ini akan mencetak `The value of x is: 6`. Tetapi apa yang
terjadi jika kita meletakkan titik koma di akhir baris yang berisi `x + 1`,
mengubahnya dari ekspresi menjadi pernyataan?

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

Mengompilasi kode ini akan menghasilkan error, seperti berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

Pesan error utamanya, `mismatched types`, menyingkap masalah inti kode ini.
Definisi fungsi `plus_one` menyatakan bahwa ia akan mengembalikan `i32`,
tetapi pernyataan tidak mengevaluasi menjadi sebuah nilai, yang dinyatakan
dengan `()`, tipe unit. Karena itu, tidak ada yang dikembalikan, yang
berkontradiksi dengan definisi fungsinya dan menghasilkan error. Pada keluaran
ini, Rust memberikan pesan yang mungkin membantu memperbaiki masalah ini: ia
menyarankan penghapusan titik koma, yang akan memperbaiki errornya.
