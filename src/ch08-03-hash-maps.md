## Menyimpan Kunci dengan Nilai yang Terkait di dalam Hash Map

Yang terakhir dari collection umum kita adalah hash map. Type `HashMap<K, V>`
menyimpan pemetaan dari kunci typed `K` ke nilai typed `V` memakai
*hashing function* (fungsi hashing), yang menentukan cara ia menempatkan
kunci dan nilai tersebut ke dalam memori. Banyak bahasa pemrograman
mendukung struktur data semacam ini, tetapi mereka sering memakai nama yang
berbeda, seperti *hash*, *map*, *object*, *hash table*, *dictionary*, atau
*associative array*, untuk menyebut beberapa saja.

Hash map berguna ketika Anda ingin mencari data bukan dengan memakai indeks,
seperti yang dapat Anda lakukan dengan vector, melainkan dengan memakai
kunci yang dapat typed apa pun. Misalnya, dalam sebuah permainan, Anda
dapat melacak skor setiap tim di dalam hash map yang setiap kuncinya adalah
nama tim dan nilainya adalah skor setiap tim. Dengan diberi nama tim, Anda
dapat mengambil skornya.

Kita akan membahas API dasar hash map di bagian ini, tetapi masih banyak hal
menarik yang tersembunyi di fungsi-fungsi yang didefinisikan pada
`HashMap<K, V>` oleh pustaka standar. Seperti biasa, periksa dokumentasi
pustaka standar untuk informasi lebih lanjut.

### Membuat Hash Map Baru

Salah satu cara membuat hash map kosong adalah memakai `new` dan menambahkan
elemen dengan `insert`. Di Listing 8-20, kita melacak skor dua tim yang
namanya _Blue_ dan _Yellow_. Tim Blue memulai dengan 10 poin, dan tim Yellow
memulai dengan 50.

<Listing number="8-20" caption="Membuat hash map baru dan memasukkan beberapa kunci dan nilai">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-20/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa kita perlu terlebih dahulu `use` `HashMap` dari bagian
collections pustaka standar. Dari tiga collection umum kita, yang satu ini
paling jarang dipakai, jadi ia tidak termasuk dalam fitur-fitur yang dibawa
ke dalam *scope* secara otomatis di *prelude*. Hash map juga mendapat dukungan
lebih sedikit dari pustaka standar; tidak ada *macro* bawaan untuk
mengonstruksinya, misalnya.

Sama seperti vector, hash map menyimpan datanya di *heap*. `HashMap` ini
memiliki kunci typed `String` dan nilai typed `i32`. Seperti vector,
hash map bersifat homogen: semua kunci harus typed sama, dan semua nilai
harus typed sama.

<a id="accessing-values-in-a-hash-map"></a>
### Mengakses Nilai di dalam Hash Map

Kita dapat mengeluarkan sebuah nilai dari hash map dengan memberikan
kuncinya ke method `get`, seperti yang ditunjukkan di Listing 8-21.

<Listing number="8-21" caption="Mengakses skor untuk tim Blue yang tersimpan di hash map">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-21/src/main.rs:here}}
```

</Listing>

Di sini, `score` akan memiliki nilai yang terasosiasi dengan tim Blue, dan
hasilnya adalah `10`. Method `get` mengembalikan `Option<&V>`; jika tidak
ada nilai untuk kunci itu di hash map, `get` akan mengembalikan `None`.
Program ini menangani `Option` dengan memanggil `copied` untuk mendapatkan
`Option<i32>` alih-alih `Option<&i32>`, lalu `unwrap_or` untuk menetapkan
`score` menjadi nol jika `scores` tidak memiliki entri untuk kunci itu.

Kita dapat mengiterasi setiap pasangan kunci-nilai di hash map dengan cara
yang mirip seperti yang kita lakukan dengan vector, memakai loop
`for`:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-03-iterate-over-hashmap/src/main.rs:here}}
```

Kode ini akan mencetak setiap pasangan dalam urutan sembarang:

```text
Yellow: 50
Blue: 10
```

<!-- Old headings. Do not remove or links may break. -->

<a id="hash-maps-and-ownership"></a>

### Mengelola Ownership di dalam Hash Map

Untuk type yang mengimplementasikan *trait* `Copy`, seperti `i32`, nilainya
disalin ke dalam hash map. Untuk nilai yang dimiliki seperti `String`,
nilainya akan dipindahkan dan hash map akan menjadi *owner* nilai-nilai
tersebut, seperti yang didemonstrasikan di Listing 8-22.

<Listing number="8-22" caption="Menunjukkan bahwa kunci dan nilai dimiliki hash map begitu keduanya dimasukkan">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-22/src/main.rs:here}}
```

</Listing>

Kita tidak dapat memakai variable `field_name` dan `field_value` setelah
keduanya dipindahkan ke dalam hash map lewat pemanggilan `insert`.

Jika kita memasukkan *reference* ke nilai ke dalam hash map, nilainya tidak
akan dipindahkan ke dalam hash map. Nilai yang ditunjuk *reference* harus
tetap valid paling tidak selama hash map valid. Kita akan membicarakan
masalah-masalah ini lebih lanjut di [“Memvalidasi *Reference* dengan
*Lifetime*”][validating-references-with-lifetimes]<!-- ignore --> di Bab 10.

### Memperbarui Hash Map

Meskipun jumlah pasangan kunci dan nilai dapat membesar, setiap kunci unik
hanya dapat memiliki satu nilai yang terasosiasi dengannya pada satu waktu
(tetapi tidak sebaliknya: misalnya, baik tim Blue maupun tim Yellow dapat
memiliki nilai `10` yang tersimpan di hash map `scores`).

Ketika Anda ingin mengubah data di hash map, Anda harus memutuskan cara
menangani kasus ketika sebuah kunci sudah memiliki nilai yang ditetapkan.
Anda dapat mengganti nilai lama dengan nilai baru, mengabaikan nilai lama
sepenuhnya. Anda dapat mempertahankan nilai lama dan mengabaikan nilai baru,
hanya menambahkan nilai baru jika kunci _belum_ memiliki nilai. Atau Anda
dapat menggabungkan nilai lama dan nilai baru. Mari kita lihat cara
melakukan masing-masingnya!

#### Menimpa Nilai

Jika kita memasukkan sebuah kunci dan nilai ke dalam hash map, lalu
memasukkan kunci yang sama dengan nilai yang berbeda, nilai yang terasosiasi
dengan kunci itu akan diganti. Meskipun kode di Listing 8-23 memanggil
`insert` dua kali, hash map hanya akan berisi satu pasangan kunci-nilai
karena kita memasukkan nilai untuk kunci tim Blue dua kali.

<Listing number="8-23" caption="Mengganti nilai yang tersimpan pada kunci tertentu">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-23/src/main.rs:here}}
```

</Listing>

Kode ini akan mencetak `{"Blue": 25}`. Nilai awal `10` telah ditimpa.

<!-- Old headings. Do not remove or links may break. -->

<a id="only-inserting-a-value-if-the-key-has-no-value"></a>

#### Menambahkan Kunci dan Nilai Hanya Jika Kunci Belum Ada

Sudah lumrah untuk memeriksa apakah sebuah kunci tertentu sudah ada di hash
map dengan sebuah nilai, lalu mengambil tindakan berikut: jika kunci itu
memang ada di hash map, nilai yang ada harus tetap seperti apa adanya; jika
kunci itu tidak ada, masukkan kunci itu dan sebuah nilai untuknya.

Hash map memiliki API khusus untuk ini yang disebut `entry` yang menerima
kunci yang ingin Anda periksa sebagai parameter. Nilai kembalian method
`entry` adalah *enum* bernama `Entry` yang merepresentasikan nilai yang
mungkin ada atau tidak ada. Katakanlah kita ingin memeriksa apakah kunci
untuk tim Yellow memiliki nilai yang terasosiasi dengannya. Jika tidak, kita
ingin memasukkan nilai `50`, dan begitu pula untuk tim Blue. Memakai API
`entry`, kodenya terlihat seperti Listing 8-24.

<Listing number="8-24" caption="Memakai method `entry` untuk hanya memasukkan jika kuncinya belum memiliki nilai">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-24/src/main.rs:here}}
```

</Listing>

Method `or_insert` pada `Entry` didefinisikan untuk mengembalikan *reference*
*mutable* ke nilai untuk kunci `Entry` yang bersangkutan jika kunci itu ada,
dan jika tidak, ia memasukkan parameter sebagai nilai baru untuk kunci ini
dan mengembalikan *reference* *mutable* ke nilai baru tersebut. Teknik ini jauh
lebih bersih daripada menulis logikanya sendiri dan, selain itu, lebih akur
dengan *borrow checker*.

Menjalankan kode di Listing 8-24 akan mencetak `{"Yellow": 50, "Blue": 10}`.
Pemanggilan `entry` yang pertama akan memasukkan kunci untuk tim Yellow
dengan nilai `50` karena tim Yellow belum memiliki nilai. Pemanggilan
`entry` yang kedua tidak akan mengubah hash map, karena tim Blue sudah
memiliki nilai `10`.

#### Memperbarui Nilai Berdasarkan Nilai Lama

Kasus penggunaan hash map lain yang umum adalah mencari nilai sebuah kunci
lalu memperbaruinya berdasarkan nilai lama. Misalnya, Listing 8-25
menunjukkan kode yang menghitung berapa kali setiap kata muncul di suatu
teks. Kita memakai hash map dengan kata-kata sebagai kunci dan menaikkan
nilainya untuk melacak berapa kali kita telah melihat kata itu. Jika ini
pertama kalinya kita melihat sebuah kata, kita akan memasukkan nilai `0`
terlebih dahulu.

<Listing number="8-25" caption="Menghitung kemunculan kata memakai hash map yang menyimpan kata dan hitungannya">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-25/src/main.rs:here}}
```

</Listing>

Kode ini akan mencetak `{"world": 2, "hello": 1, "wonderful": 1}`. Anda
mungkin melihat pasangan kunci-nilai yang sama dicetak dalam urutan yang
berbeda: ingat dari [“Mengakses Nilai di dalam Hash Map”][access]<!-- ignore
--> bahwa mengiterasi hash map terjadi dalam urutan sembarang.

Method `split_whitespace` mengembalikan sebuah *iterator* atas subslice,
dipisahkan oleh spasi, dari nilai di `text`. Method `or_insert`
mengembalikan *reference* *mutable* (`&mut V`) ke nilai untuk kunci yang
ditentukan. Di sini, kita menyimpan *reference* *mutable* itu di variable
`count`, jadi untuk menetapkan nilai itu, kita harus mendereferensi `count`
terlebih dahulu memakai tanda bintang (`*`). *Reference* *mutable* keluar dari
*scope* di akhir loop `for`, jadi semua perubahan ini aman dan
diperbolehkan oleh aturan *borrowing*.

### Fungsi Hashing

Secara default, `HashMap` memakai hashing function bernama _SipHash_ yang
dapat memberikan ketahanan terhadap serangan denial-of-service (DoS) yang
melibatkan tabel hash[^siphash]<!-- ignore -->. Ini bukan algoritme hashing
tercepat yang tersedia, tetapi kompromi demi keamanan yang lebih baik yang
datang bersama turunnya kinerja itu sepadan. Jika Anda memprofil kode Anda
dan menemukan bahwa hash function default terlalu lambat untuk keperluan
Anda, Anda dapat beralih ke fungsi lain dengan menentukan hasher yang
berbeda. Sebuah *hasher* adalah type yang mengimplementasikan *trait*
`BuildHasher`. Kita akan membicarakan *trait* dan cara mengimplementasikannya
di [Bab 10][traits]<!-- ignore -->. Anda tidak harus mengimplementasikan
hasher Anda sendiri dari nol; [crates.io](https://crates.io/)<!-- ignore -->
memiliki pustaka-pustaka yang dibagikan pengguna Rust lain yang menyediakan
hasher yang mengimplementasikan banyak algoritme hashing yang umum.

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

## Ringkasan

Vector, string, dan hash map akan menyediakan banyak fungsionalitas yang
diperlukan program ketika Anda perlu menyimpan, mengakses, dan memodifikasi
data. Berikut beberapa latihan yang sekarang seharusnya mampu Anda
selesaikan:

1. Diberikan daftar bilangan bulat, pakai vector dan kembalikan median
   (saat diurutkan, nilai pada posisi tengah) dan modus (nilai yang paling
   sering muncul; hash map akan membantu di sini) dari daftar tersebut.
1. Ubah string menjadi Pig Latin. Konsonan pertama setiap kata dipindahkan
   ke akhir kata dan _ay_ ditambahkan, sehingga _first_ menjadi _irst-fay_.
   Kata yang dimulai dengan vokal mendapat tambahan _hay_ di akhirnya
   (_apple_ menjadi _apple-hay_). Ingat-ingat detail tentang enkode UTF-8!
1. Dengan memakai hash map dan vector, buat antarmuka teks untuk
   memungkinkan pengguna menambahkan nama pegawai ke sebuah departemen di
   sebuah perusahaan; misalnya, “Add Sally to Engineering” atau “Add Amir
   to Sales.” Lalu, biarkan pengguna mengambil daftar semua orang di sebuah
   departemen atau semua orang di perusahaan menurut departemen, diurutkan
   menurut abjad.

Dokumentasi API pustaka standar menjelaskan method-method yang dimiliki
vector, string, dan hash map yang akan membantu latihan-latihan ini!

Kita mulai masuk ke program yang lebih kompleks yang operasinya dapat gagal,
jadi ini waktu yang tepat untuk membahas penanganan error. Kita akan
melakukannya selanjutnya!

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: ch10-02-traits.html
