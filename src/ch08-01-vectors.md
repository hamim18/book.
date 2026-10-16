## Menyimpan Daftar Nilai dengan Vektor

Tipe koleksi pertama yang akan kita lihat adalah `Vec<T>`, yang juga dikenal
sebagai vektor. Vektor memungkinkan Anda menyimpan lebih dari satu nilai di
dalam satu struktur data yang menempatkan semua nilainya bersebelahan di
memori. Vektor hanya dapat menyimpan nilai dengan tipe yang sama. Vektor
berguna ketika Anda memiliki daftar item, seperti baris-baris teks di sebuah
file atau harga-harga barang di keranjang belanja.

### Membuat Vektor Baru

Untuk membuat vektor kosong yang baru, kita memanggil fungsi `Vec::new`,
seperti yang ditunjukkan di Listing 8-1.

<Listing number="8-1" caption="Membuat vektor kosong yang baru untuk menampung nilai bertipe `i32`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-01/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa kita menambahkan anotasi tipe di sini. Karena kita belum
memasukkan nilai apa pun ke dalam vektor ini, Rust tidak tahu elemen bertipe
apa yang ingin kita simpan. Ini poin yang penting. Vektor diimplementasikan
memakai *generics* (tipe generik); kita akan membahas cara memakai generics
dengan tipe Anda sendiri di Bab 10. Untuk saat ini, ketahuilah bahwa tipe
`Vec<T>` yang disediakan pustaka standar dapat menampung tipe apa pun. Ketika
kita membuat vektor untuk menampung tipe tertentu, kita dapat menyebutkan
tipenya di dalam kurung sudut. Di Listing 8-1, kita telah memberi tahu Rust
bahwa `Vec<T>` di `v` akan menampung elemen bertipe `i32`.

Lebih sering, Anda akan membuat `Vec<T>` dengan nilai awal, dan Rust akan
menginferensi tipe nilai yang ingin Anda simpan, sehingga Anda jarang perlu
melakukan anotasi tipe ini. Rust dengan mudah menyediakan *macro* (makro)
`vec!`, yang akan membuat vektor baru yang menampung nilai-nilai yang Anda
berikan. Listing 8-2 membuat `Vec<i32>` baru yang menampung nilai `1`, `2`,
dan `3`. Tipe bilangannya adalah `i32` karena itu adalah tipe bilangan bulat
default, seperti yang kita bahas di bagian [“Tipe Data”][data-types]<!--
ignore --> di Bab 3.

<Listing number="8-2" caption="Membuat vektor baru yang berisi nilai-nilai">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-02/src/main.rs:here}}
```

</Listing>

Karena kita telah memberikan nilai awal `i32`, Rust dapat menginferensi
bahwa tipe `v` adalah `Vec<i32>`, dan anotasi tipe tidak diperlukan.
Berikutnya, kita akan melihat cara memodifikasi vektor.

### Memperbarui Vektor

Untuk membuat vektor lalu menambahkan elemen ke dalamnya, kita dapat memakai
metode `push`, seperti yang ditunjukkan di Listing 8-3.

<Listing number="8-3" caption="Memakai metode `push` untuk menambahkan nilai ke vektor">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-03/src/main.rs:here}}
```

</Listing>

Seperti variabel mana pun, jika kita ingin dapat mengubah nilainya, kita
perlu menjadikannya *mutable* (dapat diubah) memakai kata kunci `mut`, seperti
yang dibahas di Bab 3. Angka-angka yang kita tempatkan di dalamnya semuanya
bertipe `i32`, dan Rust menginferensi hal ini dari datanya, jadi kita tidak
perlu anotasi `Vec<i32>`.

### Membaca Elemen-Elemen Vektor

Ada dua cara untuk merujuk nilai yang tersimpan di vektor: lewat pengindeksan
atau dengan memakai metode `get`. Pada contoh-contoh berikut, kita
menganotasi tipe nilai yang dikembalikan dari fungsi-fungsi ini demi
kejelasan ekstra.

Listing 8-4 menunjukkan kedua metode untuk mengakses nilai di vektor, dengan
sintaks pengindeksan dan metode `get`.

<Listing number="8-4" caption="Memakai sintaks pengindeksan dan memakai metode `get` untuk mengakses item di vektor">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-04/src/main.rs:here}}
```

</Listing>

Perhatikan beberapa detail di sini. Kita memakai nilai indeks `2` untuk
mendapatkan elemen ketiga karena vektor diindeks berdasarkan angka, dimulai
dari nol. Memakai `&` dan `[]` memberi kita sebuah *reference* (referensi) ke
elemen pada nilai indeks tersebut. Ketika kita memakai metode `get` dengan
indeks yang diteruskan sebagai argumen, kita mendapat `Option<&T>` yang dapat
kita pakai dengan `match`.

Rust menyediakan dua cara untuk merujuk elemen ini supaya Anda dapat memilih
bagaimana program berperilaku ketika Anda mencoba memakai nilai indeks di
luar jangkauan elemen yang ada. Sebagai contoh, mari kita lihat apa yang
terjadi ketika kita memiliki vektor berisi lima elemen lalu mencoba mengakses
elemen pada indeks 100 dengan masing-masing teknik, seperti yang ditunjukkan
di Listing 8-5.

<Listing number="8-5" caption="Mencoba mengakses elemen pada indeks 100 di vektor yang berisi lima elemen">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-05/src/main.rs:here}}
```

</Listing>

Ketika kita menjalankan kode ini, metode `[]` yang pertama akan menyebabkan
program panic karena ia merujuk elemen yang tidak ada. Metode ini paling baik
dipakai ketika Anda ingin program Anda crash jika ada upaya mengakses elemen
melewati ujung vektor.

Ketika metode `get` diberi indeks yang berada di luar vektor, ia
mengembalikan `None` tanpa panic. Anda akan memakai metode ini jika mengakses
elemen di luar jangkauan vektor sesekali dapat terjadi dalam keadaan normal.
Kode Anda kemudian akan memiliki logika untuk menangani `Some(&element)`
atau `None`, seperti yang dibahas di Bab 6. Misalnya, indeks bisa berasal
dari seseorang yang memasukkan angka. Jika mereka tidak sengaja memasukkan
angka yang terlalu besar dan program mendapat nilai `None`, Anda dapat
memberi tahu pengguna berapa banyak item yang ada di vektor saat ini dan
memberi mereka kesempatan lagi untuk memasukkan nilai yang valid. Itu akan
lebih ramah pengguna daripada membuat program crash gara-gara salah ketik!

Ketika program memiliki reference yang valid, borrow checker menegakkan
aturan ownership dan *borrowing* (peminjaman) (yang dibahas di Bab 4) untuk
memastikan bahwa reference ini dan reference lain mana pun ke isi vektor
tetap valid. Ingat aturan yang menyatakan bahwa Anda tidak dapat memiliki
reference mutable dan immutable di scope yang sama. Aturan itu berlaku di
Listing 8-6, ketika kita memegang reference immutable ke elemen pertama di
vektor dan mencoba menambahkan elemen ke ujungnya. Program ini tidak akan
bekerja jika kita juga mencoba merujuk elemen itu di bagian selanjutnya dari
fungsi.

<Listing number="8-6" caption="Mencoba menambahkan elemen ke vektor sambil memegang reference ke sebuah item">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-06/src/main.rs:here}}
```

</Listing>

Mengompilasi kode ini akan menghasilkan galat berikut:

```console
{{#include ../listings/ch08-common-collections/listing-08-06/output.txt}}
```

Kode di Listing 8-6 mungkin terlihat seharusnya bekerja: mengapa reference
ke elemen pertama harus peduli dengan perubahan di ujung vektor? Galat ini
disebabkan oleh cara kerja vektor: karena vektor menempatkan nilai-nilai
bersebelahan di memori, menambahkan elemen baru ke ujung vektor mungkin
mengharuskan pengalokasian memori baru dan penyalinan elemen-elemen lama ke
ruang yang baru, jika tidak ada cukup ruang untuk menempatkan semua elemen
bersebelahan di tempat vektor saat ini disimpan. Dalam kasus itu, reference
ke elemen pertama akan menunjuk ke memori yang telah dibebaskan. Aturan
borrowing mencegah program berakhir di situasi semacam itu.

> Catatan: Untuk lebih lanjut tentang detail implementasi tipe `Vec<T>`,
> lihat [“The Rustonomicon”][nomicon].

### Mengiterasi Nilai-Nilai di dalam Vektor

Untuk mengakses setiap elemen di vektor secara bergantian, kita akan
mengiterasi semua elemen alih-alih memakai indeks untuk mengakses satu per
satu. Listing 8-7 menunjukkan cara memakai perulangan `for` untuk
mendapatkan reference immutable ke setiap elemen di vektor berisi nilai
`i32` dan mencetaknya.

<Listing number="8-7" caption="Mencetak setiap elemen di vektor dengan mengiterasi elemen-elemennya memakai perulangan `for`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-07/src/main.rs:here}}
```

</Listing>

Kita juga dapat mengiterasi reference mutable ke setiap elemen di vektor
mutable untuk membuat perubahan pada semua elemen. Perulangan `for` di
Listing 8-8 akan menambahkan `50` ke setiap elemen.

<Listing number="8-8" caption="Mengiterasi reference mutable ke elemen-elemen di vektor">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-08/src/main.rs:here}}
```

</Listing>

Untuk mengubah nilai yang dirujuk reference mutable, kita harus memakai
operator dereferensi `*` untuk sampai ke nilai di `i` sebelum kita dapat
memakai operator `+=`. Kita akan membahas lebih lanjut operator dereferensi
di bagian [“Mengikuti Reference Menuju Nilai”][deref]<!-- ignore --> di Bab
15.

Mengiterasi vektor, baik secara immutable maupun mutable, aman karena aturan
borrow checker. Jika kita mencoba memasukkan atau menghapus item di badan
perulangan `for` di Listing 8-7 dan Listing 8-8, kita akan mendapat galat
compiler yang mirip dengan yang kita dapatkan pada kode di Listing 8-6.
Reference ke vektor yang dipegang perulangan `for` mencegah modifikasi
seluruh vektor secara bersamaan.

### Memakai Enum untuk Menyimpan Beberapa Tipe

Vektor hanya dapat menyimpan nilai yang bertipe sama. Ini bisa merepotkan;
pasti ada kasus penggunaan yang membutuhkan penyimpanan daftar item dengan
tipe berbeda. Untungnya, variant-variant sebuah enum didefinisikan di bawah
tipe enum yang sama, jadi ketika kita membutuhkan satu tipe untuk
merepresentasikan elemen-elemen dengan tipe berbeda, kita dapat
mendefinisikan dan memakai enum!

Misalnya, katakanlah kita ingin mengambil nilai dari sebuah baris di
spreadsheet yang sebagian kolomnya berisi bilangan bulat, sebagian berisi
angka titik mengambang, dan sebagian berisi string. Kita dapat mendefinisikan
enum yang variant-nya akan menampung tipe nilai yang berbeda, dan semua
variant enum akan dianggap sebagai tipe yang sama: tipe enum itu. Lalu, kita
dapat membuat vektor untuk menampung enum itu dan, pada akhirnya, menampung
tipe-tipe yang berbeda. Kita telah mendemonstrasikannya di Listing 8-9.

<Listing number="8-9" caption="Mendefinisikan enum untuk menyimpan nilai dengan tipe berbeda di satu vektor">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-09/src/main.rs:here}}
```

</Listing>

Rust perlu tahu tipe apa saja yang akan berada di vektor pada waktu
kompilasi supaya ia tahu persis berapa banyak memori di heap yang akan
dibutuhkan untuk menyimpan setiap elemen. Kita juga harus eksplisit tentang
tipe apa saja yang diperbolehkan di vektor ini. Jika Rust mengizinkan vektor
menampung tipe apa pun, ada kemungkinan satu tipe atau lebih menyebabkan
galat pada operasi yang dilakukan terhadap elemen-elemen vektor. Memakai
enum ditambah ekspresi `match` berarti Rust akan memastikan pada waktu
kompilasi bahwa setiap kasus yang mungkin tertangani, seperti yang dibahas
di Bab 6.

Jika Anda tidak tahu himpunan tipe yang lengkap yang akan diterima program
pada runtime untuk disimpan di vektor, teknik enum tidak akan bekerja.
Sebagai gantinya, Anda dapat memakai *trait object* (objek trait), yang akan
kita bahas di Bab 18.

Setelah kita membahas beberapa cara paling umum untuk memakai vektor,
pastikan untuk meninjau [dokumentasi API][vec-api]<!-- ignore --> untuk semua
metode bermanfaat yang banyak jumlahnya yang didefinisikan pada `Vec<T>` oleh
pustaka standar. Misalnya, selain `push`, metode `pop` menghapus dan
mengembalikan elemen terakhir.

### Membebaskan Vektor Ikut Membebaskan Elemen-Elemennya

Seperti `struct` lainnya, sebuah vektor dibebaskan ketika keluar dari scope,
seperti yang dianotasi di Listing 8-10.

<Listing number="8-10" caption="Menunjukkan tempat vektor dan elemen-elemennya dibebaskan">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-10/src/main.rs:here}}
```

</Listing>

Ketika vektor dibebaskan, semua isinya juga ikut dibebaskan, yang berarti
bilangan bulat yang ditampungnya akan dibersihkan. Borrow checker memastikan
bahwa reference mana pun ke isi vektor hanya dipakai selama vektornya
sendiri masih valid.

Mari kita lanjut ke tipe koleksi berikutnya: `String`!

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: ../nomicon/vec/vec.html
[vec-api]: ../std/vec/struct.Vec.html
[deref]: ch15-02-deref.html#following-the-pointer-to-the-value-with-the-dereference-operator
