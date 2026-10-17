## Semua Tempat Pola Bisa Dipakai

Pola muncul di sejumlah tempat di Rust, dan Anda telah memakainya secara luas
tanpa menyadarinya! Bagian ini membahas semua tempat pola valid.

### Arm `match`

Seperti yang dibahas di Bab 6, kita memakai pola di arm ekspresi `match`.
Secara formal, ekspresi `match` didefinisikan sebagai kata kunci `match`,
sebuah nilai untuk dicocokkan, dan satu atau lebih arm match yang terdiri dari
sebuah pola dan ekspresi yang dijalankan jika nilainya cocok dengan pola arm
itu, seperti ini:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre><code>match <em>VALUE</em> {
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
}</code></pre>

Contohnya, berikut ekspresi `match` dari Listing 6-5 yang mencocokkan nilai
`Option<i32>` pada variabel `x`:

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

Pola pada ekspresi `match` ini adalah `None` dan `Some(i)` di sebelah kiri
setiap panah.

Salah satu persyaratan ekspresi `match` adalah ia harus ekshaustif, dalam arti
semua kemungkinan nilai pada ekspresi `match` harus diperhitungkan. Salah satu
cara memastikan Anda telah mencakup semua kemungkinan adalah dengan memiliki
pola catch-all untuk arm terakhir: contohnya, nama variabel yang cocok dengan
nilai apa pun tidak akan pernah gagal dan dengan demikian mencakup semua kasus
yang tersisa.

Pola khusus `_` akan cocok dengan apa pun, tetapi ia tidak pernah mengikat ke
variabel, jadi ia sering dipakai di arm match terakhir. Pola `_` bisa berguna
ketika Anda ingin mengabaikan nilai apa pun yang tidak ditentukan, misalnya.
Kita akan membahas pola `_` secara lebih mendetail di [“Mengabaikan Nilai
dalam Pola”][ignoring-values-in-a-pattern]<!-- ignore --> nanti di bab ini.

### Pernyataan `let`

Sebelum bab ini, kita hanya secara eksplisit membahas pemakaian pola dengan
`match` dan `if let`, tetapi sebenarnya kita telah memakai pola di tempat lain
juga, termasuk pada pernyataan `let`. Contohnya, perhatikan penetapan variabel
sederhana dengan `let` ini:

```rust
let x = 5;
```

Setiap kali Anda memakai pernyataan `let` seperti ini, Anda telah memakai
pola, meskipun Anda mungkin tidak menyadarinya! Secara lebih formal,
pernyataan `let` terlihat seperti ini:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

Pada pernyataan seperti `let x = 5;` dengan nama variabel di slot PATTERN,
nama variabel itu hanyalah bentuk pola yang sangat sederhana. Rust
membandingkan ekspresi dengan polanya dan menetapkan nama apa pun yang
ditemukannya. Jadi, pada contoh `let x = 5;`, `x` adalah pola yang berarti
“ikat apa yang cocok di sini ke variabel `x`.” Karena nama `x` adalah
keseluruhan polanya, pola ini secara efektif berarti “ikat semuanya ke
variabel `x`, apa pun nilainya.”

Untuk melihat aspek pencocokan pola dari `let` dengan lebih jelas,
perhatikan Listing 19-1, yang memakai pola dengan `let` untuk
mendestrukturisasi sebuah *tuple*.

<Listing number="19-1" caption="Memakai pola untuk mendestrukturisasi tuple dan membuat tiga variabel sekaligus">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs:here}}
```

</Listing>

Di sini, kita mencocokkan sebuah *tuple* terhadap sebuah pola. Rust
membandingkan nilai `(1, 2, 3)` dengan pola `(x, y, z)` dan melihat bahwa
nilai itu cocok dengan polanya—artinya, ia melihat bahwa jumlah elemen
keduanya sama—jadi Rust mengikat `1` ke `x`, `2` ke `y`, dan `3` ke `z`. Anda
bisa menganggap pola *tuple* ini sebagai tiga pola variabel individual yang
bersarang di dalamnya.

Jika jumlah elemen pada pola tidak cocok dengan jumlah elemen pada *tuple*,
tipe keseluruhannya tidak akan cocok dan kita akan mendapat error kompilator.
Contohnya, Listing 19-2 menunjukkan upaya mendestrukturisasi *tuple* dengan
tiga elemen menjadi dua variabel, yang tidak akan berhasil.

<Listing number="19-2" caption="Membuat pola secara keliru dengan variabel yang jumlahnya tidak cocok dengan jumlah elemen pada tuple">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

Upaya mengompilasi kode ini menghasilkan error tipe berikut:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-02/output.txt}}
```

Untuk memperbaiki errornya, kita bisa mengabaikan satu atau beberapa nilai di
*tuple* itu menggunakan `_` atau `..`, seperti yang akan Anda lihat di bagian
[“Mengabaikan Nilai dalam Pola”][ignoring-values-in-a-pattern]<!-- ignore -->.
Jika masalahnya adalah kita punya terlalu banyak variabel di pola, solusinya
adalah membuat tipe-tipenya cocok dengan menghapus variabel sehingga jumlah
variabel sama dengan jumlah elemen di *tuple*.

### Ekspresi Kondisional `if let`

Di Bab 6, kita membahas cara memakai ekspresi `if let` terutama sebagai cara
yang lebih singkat untuk menulis yang setara dengan `match` yang hanya
mencocokkan satu kasus. Secara opsional, `if let` bisa memiliki `else` yang
sesuai dan berisi kode untuk dijalankan jika pola di `if let` tidak cocok.

Listing 19-3 menunjukkan bahwa kita juga bisa mencampur dan mencocokkan
ekspresi `if let`, `else if`, dan `else if let`. Melakukannya memberi kita
lebih banyak fleksibilitas daripada ekspresi `match`, yang dengannya kita
hanya bisa mengekspresikan satu nilai untuk dibandingkan dengan pola-pola
itu. Selain itu, Rust tidak mengharuskan kondisi-kondisi pada rangkaian arm
`if let`, `else if`, dan `else if let` saling berkaitan.

Kode di Listing 19-3 menentukan warna apa yang akan dijadikan latar belakang
Anda berdasarkan serangkaian pemeriksaan untuk beberapa kondisi. Untuk contoh
ini, kita telah membuat variabel dengan nilai yang ditulis langsung (hardcoded) yang mungkin diterima
program sungguhan dari masukan pengguna.

<Listing number="19-3" file-name="src/main.rs" caption="Mencampur `if let`, `else if`, `else if let`, dan `else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-03/src/main.rs}}
```

</Listing>

Jika pengguna menentukan warna favorit, warna itu dipakai sebagai latar
belakang. Jika tidak ada warna favorit yang ditentukan dan hari ini Selasa,
warna latar belakangnya hijau. Jika tidak, jika pengguna menentukan usia
mereka sebagai string dan kita berhasil melakukan parsing menjadi angka, warna
latar belakangnya ungu atau oranye bergantung pada nilai angka itu. Jika tidak
ada satu pun kondisi ini yang berlaku, warna latar belakangnya biru.

Struktur kondisional ini memungkinkan kita mendukung persyaratan yang
kompleks. Dengan nilai yang ditulis langsung (hardcoded) yang kita punya di sini, contoh ini akan
mencetak `Using purple as the background color`.

Anda bisa melihat bahwa `if let` juga bisa memperkenalkan variabel baru yang
melakukan shadowing terhadap variabel yang sudah ada dengan cara yang sama
seperti yang bisa dilakukan arm `match`: baris `if let Ok(age) = age`
memperkenalkan variabel `age` baru yang memuat nilai di dalam varian `Ok`,
melakukan shadowing terhadap variabel `age` yang sudah ada. Ini berarti kita
perlu menaruh kondisi `if age > 30` di dalam blok itu: kita tidak bisa
menggabungkan dua kondisi ini menjadi `if let Ok(age) = age && age > 30`.
`age` baru yang ingin kita bandingkan dengan 30 tidak valid sampai *scope* baru
dimulai dengan kurung kurawal.

Kekurangan memakai ekspresi `if let` adalah kompilator tidak memeriksa
ekshaustivitas, sedangkan pada ekspresi `match` ia memeriksanya. Jika kita
menghilangkan blok `else` terakhir dan karenanya melewatkan penanganan
beberapa kasus, kompilator tidak akan memperingatkan kita tentang kemungkinan
bug logika itu.

### Perulangan Kondisional `while let`

Serupa konstruksinya dengan `if let`, perulangan kondisional `while let`
memungkinkan perulangan `while` berjalan selama sebuah pola terus cocok. Di
Listing 19-4, kita menunjukkan perulangan `while let` yang menunggu pesan yang
dikirim antar-thread, tetapi dalam kasus ini memeriksa `Result` alih-alih
`Option`.

<Listing number="19-4" caption="Memakai perulangan `while let` untuk mencetak nilai selama `rx.recv()` mengembalikan `Ok`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

Contoh ini mencetak `1`, `2`, lalu `3`. Metode `recv` mengambil pesan pertama
dari sisi penerima *channel* dan mengembalikan `Ok(value)`. Ketika pertama kali
kita melihat `recv` di Bab 16, kita melakukan unwrap pada errornya secara
langsung, atau kita berinteraksi dengannya sebagai *iterator* menggunakan
perulangan `for`. Akan tetapi, seperti yang ditunjukkan Listing 19-4, kita
juga bisa memakai `while let`, karena metode `recv` mengembalikan `Ok` setiap
kali pesan tiba, selama pengirimnya ada, dan kemudian menghasilkan `Err`
begitu sisi pengirim terputus.

### Perulangan `for`

Pada perulangan `for`, nilai yang langsung mengikuti kata kunci `for` adalah
sebuah pola. Contohnya, pada `for x in y`, `x` adalah polanya. Listing 19-5
mendemonstrasikan cara memakai pola di perulangan `for` untuk
mendestrukturisasi, atau memecah, sebuah *tuple* sebagai bagian dari perulangan
`for`.

<Listing number="19-5" caption="Memakai pola di perulangan `for` untuk mendestrukturisasi tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

Kode di Listing 19-5 akan mencetak hal berikut:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

Kita mengadaptasi sebuah *iterator* menggunakan metode `enumerate` sehingga ia
menghasilkan sebuah nilai dan indeks untuk nilai itu, ditempatkan ke dalam
sebuah *tuple*. Nilai pertama yang dihasilkan adalah *tuple* `(0, 'a')`. Ketika
nilai ini dicocokkan dengan pola `(index, value)`, index akan menjadi `0` dan
value akan menjadi `'a'`, mencetak baris pertama dari keluaran.

### Parameter Fungsi

Parameter fungsi juga bisa menjadi pola. Kode di Listing 19-6, yang
mendeklarasikan fungsi bernama `foo` yang menerima satu parameter bernama `x`
bertipe `i32`, sekarang seharusnya terasa familier.

<Listing number="19-6" caption="Tanda tangan fungsi yang memakai pola di parameter-parameternya">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

Bagian `x` adalah sebuah pola! Seperti yang kita lakukan dengan `let`, kita
bisa mencocokkan *tuple* pada argumen fungsi terhadap polanya. Listing 19-7
memecah nilai-nilai pada sebuah *tuple* saat kita meneruskannya ke fungsi.

<Listing number="19-7" file-name="src/main.rs" caption="Fungsi dengan parameter yang mendestrukturisasi tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

Kode ini mencetak `Current location: (3, 5)`. Nilai `&(3, 5)` cocok dengan
pola `&(x, y)`, jadi `x` adalah nilai `3` dan `y` adalah nilai `5`.

Kita juga bisa memakai pola di daftar parameter *closure* dengan cara yang sama
seperti di daftar parameter fungsi karena *closure* mirip dengan fungsi, seperti
yang dibahas di Bab 13.

Pada titik ini, Anda telah melihat beberapa cara memakai pola, tetapi pola
tidak bekerja dengan cara yang sama di setiap tempat kita bisa memakainya. Di
sebagian tempat, polanya harus *irrefutable*; di kondisi lain, pola boleh
*refutable*. Kita akan membahas dua konsep ini berikutnya.

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern
