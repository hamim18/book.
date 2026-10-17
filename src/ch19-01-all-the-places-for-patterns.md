## Semua Tempat Pattern Bisa Dipakai

Pattern muncul di sejumlah tempat di Rust, dan Anda telah memakainya secara luas
tanpa menyadarinya! Bagian ini membahas semua tempat pattern valid.

### Arm `match`

Seperti yang dibahas di Bab 6, kita memakai pattern di arm expression `match`.
Secara formal, expression `match` didefinisikan sebagai *keyword* `match`,
sebuah nilai untuk dicocokkan, dan satu atau lebih arm match yang terdiri dari
sebuah pattern dan expression yang dijalankan jika nilainya cocok dengan pattern arm
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

Contohnya, berikut expression `match` dari Listing 6-5 yang mencocokkan nilai
`Option<i32>` pada variable `x`:

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

Pattern pada expression `match` ini adalah `None` dan `Some(i)` di sebelah kiri
setiap panah.

Salah satu persyaratan expression `match` adalah ia harus ekshaustif, dalam arti
semua kemungkinan nilai pada expression `match` harus diperhitungkan. Salah satu
cara memastikan Anda telah mencakup semua kemungkinan adalah dengan memiliki
pattern catch-all untuk arm terakhir: contohnya, nama variable yang cocok dengan
nilai apa pun tidak akan pernah gagal dan dengan demikian mencakup semua kasus
yang tersisa.

Pattern khusus `_` akan cocok dengan apa pun, tetapi ia tidak pernah mengikat ke
variable, jadi ia sering dipakai di arm match terakhir. Pattern `_` bisa berguna
ketika Anda ingin mengabaikan nilai apa pun yang tidak ditentukan, misalnya.
Kita akan membahas pattern `_` secara lebih mendetail di [“Mengabaikan Nilai
dalam Pattern”][ignoring-values-in-a-pattern]<!-- ignore --> nanti di bab ini.

### Statement `let`

Sebelum bab ini, kita hanya secara eksplisit membahas pemakaian pattern dengan
`match` dan `if let`, tetapi sebenarnya kita telah memakai pattern di tempat lain
juga, termasuk pada statement `let`. Contohnya, perhatikan assignment variable
sederhana dengan `let` ini:

```rust
let x = 5;
```

Setiap kali Anda memakai statement `let` seperti ini, Anda telah memakai
pattern, meskipun Anda mungkin tidak menyadarinya! Secara lebih formal,
statement `let` terlihat seperti ini:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

Pada statement seperti `let x = 5;` dengan nama variable di slot PATTERN,
nama variable itu hanyalah bentuk pattern yang sangat sederhana. Rust
membandingkan expression dengan patternnya dan menetapkan nama apa pun yang
ditemukannya. Jadi, pada contoh `let x = 5;`, `x` adalah pattern yang berarti
“ikat apa yang cocok di sini ke variable `x`.” Karena nama `x` adalah
keseluruhan patternnya, pattern ini secara efektif berarti “ikat semuanya ke
variable `x`, apa pun nilainya.”

Untuk melihat aspek pencocokan pattern dari `let` dengan lebih jelas,
perhatikan Listing 19-1, yang memakai pattern dengan `let` untuk
mendestrukturisasi sebuah *tuple*.

<Listing number="19-1" caption="Memakai pattern untuk mendestrukturisasi tuple dan membuat tiga variable sekaligus">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs:here}}
```

</Listing>

Di sini, kita mencocokkan sebuah *tuple* terhadap sebuah pattern. Rust
membandingkan nilai `(1, 2, 3)` dengan pattern `(x, y, z)` dan melihat bahwa
nilai itu cocok dengan patternnya—artinya, ia melihat bahwa jumlah elemen
keduanya sama—jadi Rust mengikat `1` ke `x`, `2` ke `y`, dan `3` ke `z`. Anda
bisa menganggap pattern *tuple* ini sebagai tiga pattern variable individual yang
bersarang di dalamnya.

Jika jumlah elemen pada pattern tidak cocok dengan jumlah elemen pada *tuple*,
type keseluruhannya tidak akan cocok dan kita akan mendapat error *compiler*.
Contohnya, Listing 19-2 menunjukkan upaya mendestrukturisasi *tuple* dengan
tiga elemen menjadi dua variable, yang tidak akan berhasil.

<Listing number="19-2" caption="Membuat pattern secara keliru dengan variable yang jumlahnya tidak cocok dengan jumlah elemen pada tuple">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

Upaya mengompilasi kode ini menghasilkan error type berikut:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-02/output.txt}}
```

Untuk memperbaiki errornya, kita bisa mengabaikan satu atau beberapa nilai di
*tuple* itu menggunakan `_` atau `..`, seperti yang akan Anda lihat di bagian
[“Mengabaikan Nilai dalam Pattern”][ignoring-values-in-a-pattern]<!-- ignore -->.
Jika masalahnya adalah kita punya terlalu banyak variable di pattern, solusinya
adalah membuat type-typenya cocok dengan menghapus variable sehingga jumlah
variable sama dengan jumlah elemen di *tuple*.

### Expression Kondisional `if let`

Di Bab 6, kita membahas cara memakai expression `if let` terutama sebagai cara
yang lebih singkat untuk menulis yang setara dengan `match` yang hanya
mencocokkan satu kasus. Secara opsional, `if let` bisa memiliki `else` yang
sesuai dan berisi kode untuk dijalankan jika pattern di `if let` tidak cocok.

Listing 19-3 menunjukkan bahwa kita juga bisa mencampur dan mencocokkan
expression `if let`, `else if`, dan `else if let`. Melakukannya memberi kita
lebih banyak fleksibilitas daripada expression `match`, yang dengannya kita
hanya bisa mengekspresikan satu nilai untuk dibandingkan dengan pattern-pattern
itu. Selain itu, Rust tidak mengharuskan kondisi-kondisi pada rangkaian arm
`if let`, `else if`, dan `else if let` saling berkaitan.

Kode di Listing 19-3 menentukan warna apa yang akan dijadikan latar belakang
Anda berdasarkan serangkaian pemeriksaan untuk beberapa kondisi. Untuk contoh
ini, kita telah membuat variable dengan nilai yang ditulis langsung (hardcoded) yang mungkin diterima
program sungguhan dari user input.

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

Anda bisa melihat bahwa `if let` juga bisa memperkenalkan variable baru yang
melakukan shadowing terhadap variable yang sudah ada dengan cara yang sama
seperti yang bisa dilakukan arm `match`: baris `if let Ok(age) = age`
memperkenalkan variable `age` baru yang memuat nilai di dalam varian `Ok`,
melakukan shadowing terhadap variable `age` yang sudah ada. Ini berarti kita
perlu menaruh kondisi `if age > 30` di dalam blok itu: kita tidak bisa
menggabungkan dua kondisi ini menjadi `if let Ok(age) = age && age > 30`.
`age` baru yang ingin kita bandingkan dengan 30 tidak valid sampai *scope* baru
dimulai dengan kurung kurawal.

Kekurangan memakai expression `if let` adalah *compiler* tidak memeriksa
ekshaustivitas, sedangkan pada expression `match` ia memeriksanya. Jika kita
menghilangkan blok `else` terakhir dan karenanya melewatkan penanganan
beberapa kasus, *compiler* tidak akan memperingatkan kita tentang kemungkinan
bug logika itu.

### Loop Kondisional `while let`

Serupa konstruksinya dengan `if let`, loop kondisional `while let`
memungkinkan loop `while` berjalan selama sebuah pattern terus cocok. Di
Listing 19-4, kita menunjukkan loop `while let` yang menunggu pesan yang
dikirim antar-thread, tetapi dalam kasus ini memeriksa `Result` alih-alih
`Option`.

<Listing number="19-4" caption="Memakai loop `while let` untuk mencetak nilai selama `rx.recv()` mengembalikan `Ok`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

Contoh ini mencetak `1`, `2`, lalu `3`. Method `recv` mengambil pesan pertama
dari sisi receiver *channel* dan mengembalikan `Ok(value)`. Ketika pertama kali
kita melihat `recv` di Bab 16, kita melakukan unwrap pada errornya secara
langsung, atau kita berinteraksi dengannya sebagai *iterator* menggunakan
loop `for`. Akan tetapi, seperti yang ditunjukkan Listing 19-4, kita
juga bisa memakai `while let`, karena method `recv` mengembalikan `Ok` setiap
kali pesan tiba, selama sendernya ada, dan kemudian menghasilkan `Err`
begitu sisi sender terputus.

### Loop `for`

Pada loop `for`, nilai yang langsung mengikuti *keyword* `for` adalah
sebuah pattern. Contohnya, pada `for x in y`, `x` adalah patternnya. Listing 19-5
mendemonstrasikan cara memakai pattern di loop `for` untuk
mendestrukturisasi, atau memecah, sebuah *tuple* sebagai bagian dari loop
`for`.

<Listing number="19-5" caption="Memakai pattern di loop `for` untuk mendestrukturisasi tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

Kode di Listing 19-5 akan mencetak hal berikut:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

Kita mengadaptasi sebuah *iterator* menggunakan method `enumerate` sehingga ia
menghasilkan sebuah nilai dan indeks untuk nilai itu, ditempatkan ke dalam
sebuah *tuple*. Nilai pertama yang dihasilkan adalah *tuple* `(0, 'a')`. Ketika
nilai ini dicocokkan dengan pattern `(index, value)`, index akan menjadi `0` dan
value akan menjadi `'a'`, mencetak baris pertama dari output.

### Parameter Fungsi

Parameter fungsi juga bisa menjadi pattern. Kode di Listing 19-6, yang
mendeklarasikan fungsi bernama `foo` yang menerima satu parameter bernama `x`
typed `i32`, sekarang seharusnya terasa familier.

<Listing number="19-6" caption="Tanda tangan fungsi yang memakai pattern di parameter-parameternya">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

Bagian `x` adalah sebuah pattern! Seperti yang kita lakukan dengan `let`, kita
bisa mencocokkan *tuple* pada argumen fungsi terhadap patternnya. Listing 19-7
memecah nilai-nilai pada sebuah *tuple* saat kita meneruskannya ke fungsi.

<Listing number="19-7" file-name="src/main.rs" caption="Fungsi dengan parameter yang mendestrukturisasi tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

Kode ini mencetak `Current location: (3, 5)`. Nilai `&(3, 5)` cocok dengan
pattern `&(x, y)`, jadi `x` adalah nilai `3` dan `y` adalah nilai `5`.

Kita juga bisa memakai pattern di daftar parameter *closure* dengan cara yang sama
seperti di daftar parameter fungsi karena *closure* mirip dengan fungsi, seperti
yang dibahas di Bab 13.

Pada titik ini, Anda telah melihat beberapa cara memakai pattern, tetapi pattern
tidak bekerja dengan cara yang sama di setiap tempat kita bisa memakainya. Di
sebagian tempat, patternnya harus *irrefutable*; di kondisi lain, pattern boleh
*refutable*. Kita akan membahas dua konsep ini berikutnya.

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern
