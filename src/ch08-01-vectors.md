## Menyimpan Daftar Nilai dengan Vector

Type collection pertama yang akan kita lihat adalah `Vec<T>`, yang juga dikenal
sebagai vector. Vector memungkinkan Anda menyimpan lebih dari satu nilai di
dalam satu struktur data yang menempatkan semua nilainya bersebelahan di
memori. Vector hanya dapat menyimpan nilai dengan type yang sama. Vector
berguna ketika Anda memiliki daftar item, seperti baris-baris teks di sebuah
file atau harga-harga barang di keranjang belanja.

### Membuat Vector Baru

Untuk membuat vector kosong yang baru, kita memanggil fungsi `Vec::new`,
seperti yang ditunjukkan di Listing 8-1.

<Listing number="8-1" caption="Membuat vector kosong yang baru untuk menampung nilai typed `i32`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-01/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa kita menambahkan type annotation di sini. Karena kita belum
memasukkan nilai apa pun ke dalam vector ini, Rust tidak tahu elemen typed
apa yang ingin kita simpan. Ini poin yang penting. Vector diimplementasikan
memakai *generics* (tipe generik); kita akan membahas cara memakai *generics*
dengan type Anda sendiri di Bab 10. Untuk saat ini, ketahuilah bahwa type
`Vec<T>` yang disediakan standard library dapat menampung type apa pun. Ketika
kita membuat vector untuk menampung type tertentu, kita dapat menyebutkan
typenya di dalam kurung sudut. Di Listing 8-1, kita telah memberi tahu Rust
bahwa `Vec<T>` di `v` akan menampung elemen typed `i32`.

Lebih sering, Anda akan membuat `Vec<T>` dengan nilai awal, dan Rust akan
mengtype inference nilai yang ingin Anda simpan, sehingga Anda jarang perlu
melakukan type annotation ini. Rust dengan mudah menyediakan *macro* (makro)
`vec!`, yang akan membuat vector baru yang menampung nilai-nilai yang Anda
berikan. Listing 8-2 membuat `Vec<i32>` baru yang menampung nilai `1`, `2`,
dan `3`. Type bilangannya adalah `i32` karena itu adalah type bilangan bulat
default, seperti yang kita bahas di bagian [“Type Data”][data-types]<!--
ignore --> di Bab 3.

<Listing number="8-2" caption="Membuat vector baru yang berisi nilai-nilai">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-02/src/main.rs:here}}
```

</Listing>

Karena kita telah memberikan nilai awal `i32`, Rust dapat menginferensi
bahwa type `v` adalah `Vec<i32>`, dan type annotation tidak diperlukan.
Berikutnya, kita akan melihat cara memodifikasi vector.

### Memperbarui Vector

Untuk membuat vector lalu menambahkan elemen ke dalamnya, kita dapat memakai
method `push`, seperti yang ditunjukkan di Listing 8-3.

<Listing number="8-3" caption="Memakai method `push` untuk menambahkan nilai ke vector">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-03/src/main.rs:here}}
```

</Listing>

Seperti variable mana pun, jika kita ingin dapat mengubah nilainya, kita
perlu menjadikannya *mutable* (dapat diubah) memakai kata kunci `mut`, seperti
yang dibahas di Bab 3. Angka-angka yang kita tempatkan di dalamnya semuanya
typed `i32`, dan Rust menginferensi hal ini dari datanya, jadi kita tidak
perlu anotasi `Vec<i32>`.

### Membaca Elemen-Elemen Vector

Ada dua cara untuk merujuk nilai yang tersimpan di vector: lewat pengindeksan
atau dengan memakai method `get`. Pada contoh-contoh berikut, kita
mengtype annotation nilai yang dikembalikan dari fungsi-fungsi ini demi
kejelasan ekstra.

Listing 8-4 menunjukkan kedua method untuk mengakses nilai di vector, dengan
sintaks pengindeksan dan method `get`.

<Listing number="8-4" caption="Memakai sintaks pengindeksan dan memakai method `get` untuk mengakses item di vector">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-04/src/main.rs:here}}
```

</Listing>

Perhatikan beberapa detail di sini. Kita memakai nilai indeks `2` untuk
mendapatkan elemen ketiga karena vector diindeks berdasarkan angka, dimulai
dari nol. Memakai `&` dan `[]` memberi kita sebuah *reference* (referensi) ke
elemen pada nilai indeks tersebut. Ketika kita memakai method `get` dengan
indeks yang diteruskan sebagai argumen, kita mendapat `Option<&T>` yang dapat
kita pakai dengan `match`.

Rust menyediakan dua cara untuk merujuk elemen ini supaya Anda dapat memilih
bagaimana program berperilaku ketika Anda mencoba memakai nilai indeks di
luar jangkauan elemen yang ada. Sebagai contoh, mari kita lihat apa yang
terjadi ketika kita memiliki vector berisi lima elemen lalu mencoba mengakses
elemen pada indeks 100 dengan masing-masing teknik, seperti yang ditunjukkan
di Listing 8-5.

<Listing number="8-5" caption="Mencoba mengakses elemen pada indeks 100 di vector yang berisi lima elemen">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-05/src/main.rs:here}}
```

</Listing>

Ketika kita menjalankan kode ini, method `[]` yang pertama akan menyebabkan
program panic karena ia merujuk elemen yang tidak ada. Method ini paling baik
dipakai ketika Anda ingin program Anda crash jika ada upaya mengakses elemen
melewati ujung vector.

Ketika method `get` diberi indeks yang berada di luar vector, ia
mengembalikan `None` tanpa panic. Anda akan memakai method ini jika mengakses
elemen di luar jangkauan vector sesekali dapat terjadi dalam keadaan normal.
Kode Anda kemudian akan memiliki logika untuk menangani `Some(&element)`
atau `None`, seperti yang dibahas di Bab 6. Misalnya, indeks bisa berasal
dari seseorang yang memasukkan angka. Jika mereka tidak sengaja memasukkan
angka yang terlalu besar dan program mendapat nilai `None`, Anda dapat
memberi tahu pengguna berapa banyak item yang ada di vector saat ini dan
memberi mereka kesempatan lagi untuk memasukkan nilai yang valid. Itu akan
lebih ramah pengguna daripada membuat program crash gara-gara salah ketik!

Ketika program memiliki *reference* yang valid, *borrow checker* menegakkan
aturan *ownership* dan *borrowing* (peminjaman) (yang dibahas di Bab 4) untuk
memastikan bahwa *reference* ini dan *reference* lain mana pun ke isi vector
tetap valid. Ingat aturan yang menyatakan bahwa Anda tidak dapat memiliki
*reference* *mutable* dan *immutable* di *scope* yang sama. Aturan itu berlaku di
Listing 8-6, ketika kita memegang *reference* *immutable* ke elemen pertama di
vector dan mencoba menambahkan elemen ke ujungnya. Program ini tidak akan
bekerja jika kita juga mencoba merujuk elemen itu di bagian selanjutnya dari
fungsi.

<Listing number="8-6" caption="Mencoba menambahkan elemen ke vector sambil memegang reference ke sebuah item">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-06/src/main.rs:here}}
```

</Listing>

Mengompilasi kode ini akan menghasilkan error berikut:

```console
{{#include ../listings/ch08-common-collections/listing-08-06/output.txt}}
```

Kode di Listing 8-6 mungkin terlihat seharusnya bekerja: mengapa *reference*
ke elemen pertama harus peduli dengan perubahan di ujung vector? Error ini
disebabkan oleh cara kerja vector: karena vector menempatkan nilai-nilai
bersebelahan di memori, menambahkan elemen baru ke ujung vector mungkin
mengharuskan pengalokasian memori baru dan penyalinan elemen-elemen lama ke
ruang yang baru, jika tidak ada cukup ruang untuk menempatkan semua elemen
bersebelahan di tempat vector saat ini disimpan. Dalam kasus itu, *reference*
ke elemen pertama akan menunjuk ke memori yang telah dibebaskan. Aturan
*borrowing* mencegah program berakhir di situasi semacam itu.

> Catatan: Untuk lebih lanjut tentang detail implementasi type `Vec<T>`,
> lihat [“The Rustonomicon”][nomicon].

### Mengiterasi Nilai-Nilai di dalam Vector

Untuk mengakses setiap elemen di vector secara bergantian, kita akan
mengiterasi semua elemen alih-alih memakai indeks untuk mengakses satu per
satu. Listing 8-7 menunjukkan cara memakai loop `for` untuk
mendapatkan *reference* *immutable* ke setiap elemen di vector berisi nilai
`i32` dan mencetaknya.

<Listing number="8-7" caption="Mencetak setiap elemen di vector dengan mengiterasi elemen-elemennya memakai loop `for`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-07/src/main.rs:here}}
```

</Listing>

Kita juga dapat mengiterasi *reference* *mutable* ke setiap elemen di vector
*mutable* untuk membuat perubahan pada semua elemen. Loop `for` di
Listing 8-8 akan menambahkan `50` ke setiap elemen.

<Listing number="8-8" caption="Mengiterasi reference mutable ke elemen-elemen di vector">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-08/src/main.rs:here}}
```

</Listing>

Untuk mengubah nilai yang dirujuk *reference* *mutable*, kita harus memakai
operator dereferensi `*` untuk sampai ke nilai di `i` sebelum kita dapat
memakai operator `+=`. Kita akan membahas lebih lanjut operator dereferensi
di bagian [“Mengikuti Reference Menuju Nilai”][deref]<!-- ignore --> di Bab
15.

Mengiterasi vector, baik secara *immutable* maupun *mutable*, aman karena aturan
*borrow checker*. Jika kita mencoba memasukkan atau menghapus item di badan
loop `for` di Listing 8-7 dan Listing 8-8, kita akan mendapat error
*compiler* yang mirip dengan yang kita dapatkan pada kode di Listing 8-6.
*Reference* ke vector yang dipegang loop `for` mencegah modifikasi
seluruh vector secara bersamaan.

### Memakai Enum untuk Menyimpan Beberapa Type

Vector hanya dapat menyimpan nilai yang typed sama. Ini bisa merepotkan;
pasti ada kasus penggunaan yang membutuhkan penyimpanan daftar item dengan
type berbeda. Untungnya, variant-variant sebuah *enum* didefinisikan di bawah
type *enum* yang sama, jadi ketika kita membutuhkan satu type untuk
merepresentasikan elemen-elemen dengan type berbeda, kita dapat
mendefinisikan dan memakai *enum*!

Misalnya, katakanlah kita ingin mengambil nilai dari sebuah baris di
spreadsheet yang sebagian kolomnya berisi bilangan bulat, sebagian berisi
angka floating point, dan sebagian berisi string. Kita dapat mendefinisikan
*enum* yang variant-nya akan menampung type nilai yang berbeda, dan semua
variant *enum* akan dianggap sebagai type yang sama: type *enum* itu. Lalu, kita
dapat membuat vector untuk menampung *enum* itu dan, pada akhirnya, menampung
type-type yang berbeda. Kita telah mendemonstrasikannya di Listing 8-9.

<Listing number="8-9" caption="Mendefinisikan enum untuk menyimpan nilai dengan type berbeda di satu vector">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-09/src/main.rs:here}}
```

</Listing>

Rust perlu tahu type apa saja yang akan berada di vector pada waktu
kompilasi supaya ia tahu persis berapa banyak memori di *heap* yang akan
dibutuhkan untuk menyimpan setiap elemen. Kita juga harus eksplisit tentang
type apa saja yang diperbolehkan di vector ini. Jika Rust mengizinkan vector
menampung type apa pun, ada kemungkinan satu type atau lebih menyebabkan
error pada operasi yang dilakukan terhadap elemen-elemen vector. Memakai
*enum* ditambah expression `match` berarti Rust akan memastikan pada waktu
kompilasi bahwa setiap kasus yang mungkin tertangani, seperti yang dibahas
di Bab 6.

Jika Anda tidak tahu himpunan type yang lengkap yang akan diterima program
pada runtime untuk disimpan di vector, teknik *enum* tidak akan bekerja.
Sebagai gantinya, Anda dapat memakai *trait object* (objek *trait*), yang akan
kita bahas di Bab 18.

Setelah kita membahas beberapa cara paling umum untuk memakai vector,
pastikan untuk meninjau [dokumentasi API][vec-api]<!-- ignore --> untuk semua
method bermanfaat yang banyak jumlahnya yang didefinisikan pada `Vec<T>` oleh
standard library. Misalnya, selain `push`, method `pop` menghapus dan
mengembalikan elemen terakhir.

### Membebaskan Vector Ikut Membebaskan Elemen-Elemennya

Seperti `struct` lainnya, sebuah vector dibebaskan ketika keluar dari *scope*,
seperti yang dianotasi di Listing 8-10.

<Listing number="8-10" caption="Menunjukkan tempat vector dan elemen-elemennya dibebaskan">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-10/src/main.rs:here}}
```

</Listing>

Ketika vector dibebaskan, semua isinya juga ikut dibebaskan, yang berarti
bilangan bulat yang ditampungnya akan dibersihkan. *Borrow checker* memastikan
bahwa *reference* mana pun ke isi vector hanya dipakai selama vectornya
sendiri masih valid.

Mari kita lanjut ke type collection berikutnya: `String`!

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: ../nomicon/vec/vec.html
[vec-api]: ../std/vec/struct.Vec.html
[deref]: ch15-02-deref.html#following-the-pointer-to-the-value-with-the-dereference-operator
