## Memperbaiki Proyek I/O Kita

Dengan pengetahuan baru tentang *iterator* ini, kita dapat memperbaiki proyek
I/O di Bab 12 dengan memakai *iterator* untuk membuat beberapa bagian kode
menjadi lebih jelas dan lebih ringkas. Mari kita lihat bagaimana *iterator*
dapat memperbaiki implementasi fungsi `Config::build` dan fungsi `search`
kita.

### Menghapus `clone` Menggunakan Iterator

Di Listing 12-6, kita menambahkan kode yang mengambil sebuah *slice* berisi
nilai `String` dan membuat instance *struct* `Config` dengan mengindeks ke dalam
*slice* dan meng-clone nilai-nilainya, sehingga *struct* `Config` dapat memiliki
nilai-nilai itu. Di Listing 13-17, kita telah menampilkan ulang implementasi
fungsi `Config::build` sebagaimana adanya di Listing 12-23.

<Listing number="13-17" file-name="src/main.rs" caption="Reproduksi fungsi `Config::build` dari Listing 12-23">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/main.rs:ch13}}
```

</Listing>

Pada saat itu, kita berkata untuk tidak mengkhawatirkan pemanggilan `clone`
yang tidak efisien karena kita akan menghapusnya di masa depan. Nah, saatnya
adalah sekarang!

Kita memerlukan `clone` di sini karena kita memiliki sebuah *slice* dengan
elemen-elemen `String` di parameter `args`, tetapi fungsi `build` tidak
memiliki `args`. Untuk mengembalikan *ownership* atas sebuah instance
`Config`, kita harus meng-clone nilai dari *field* `query` dan `file_path` pada
`Config` sehingga instance `Config` dapat memiliki nilai-nilainya.

Dengan pengetahuan baru kita tentang *iterator*, kita dapat mengubah fungsi
`build` untuk mengambil *ownership* atas sebuah *iterator* sebagai
argumennya alih-alih meminjam sebuah *slice*. Kita akan memakai fungsionalitas
*iterator* alih-alih kode yang memeriksa panjang *slice* dan mengindeks ke
lokasi-lokasi tertentu. Ini akan memperjelas apa yang dilakukan fungsi
`Config::build` karena *iterator*-lah yang akan mengakses nilai-nilainya.

Setelah `Config::build` mengambil *ownership* atas *iterator* dan berhenti
memakai operasi pengindeksan yang meminjam, kita dapat memindahkan nilai-nilai
`String` dari *iterator* ke dalam `Config` alih-alih memanggil `clone` dan
membuat alokasi baru.

#### Memakai Iterator yang Dikembalikan Secara Langsung

Buka file _src/main.rs_ proyek I/O Anda, yang seharusnya tampak seperti ini:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

Pertama, kita akan mengubah awal fungsi `main` yang kita miliki di Listing
12-24 menjadi kode di Listing 13-18, yang kali ini memakai sebuah *iterator*.
Ini tidak akan terkompilasi sampai kita memperbarui `Config::build` juga.

<Listing number="13-18" file-name="src/main.rs" caption="Meneruskan nilai kembalian `env::args` ke `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Listing>

Fungsi `env::args` mengembalikan sebuah *iterator*! Alih-alih mengumpulkan
nilai-nilai *iterator* ke dalam sebuah vektor lalu meneruskan *slice* ke
`Config::build`, sekarang kita meneruskan *ownership* atas *iterator* yang
dikembalikan dari `env::args` ke `Config::build` secara langsung.

Selanjutnya, kita perlu memperbarui definisi `Config::build`. Mari kita ubah
tanda tangan `Config::build` agar tampak seperti Listing 13-19. Ini masih
belum akan terkompilasi, karena kita perlu memperbarui badan fungsinya.

<Listing number="13-19" file-name="src/main.rs" caption="Memperbarui tanda tangan `Config::build` agar menerima sebuah iterator">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```

</Listing>

Dokumentasi pustaka standar untuk fungsi `env::args` menunjukkan bahwa type
*iterator* yang dikembalikannya adalah `std::env::Args`, dan type itu
mengimplementasikan *trait* `Iterator` serta mengembalikan nilai `String`.

Kita telah memperbarui tanda tangan fungsi `Config::build` sehingga parameter
`args` memiliki generic type dengan *trait bound* `impl Iterator<Item =
String>` alih-alih `&[String]`. Pemakaian sintaks `impl Trait` yang kita
bahas di bagian [“Memakai Trait sebagai Parameter”][impl-trait]<!-- ignore -->
pada Bab 10 ini berarti `args` dapat berupa type apa pun yang
mengimplementasikan *trait* `Iterator` dan mengembalikan item `String`.

Karena kita mengambil *ownership* atas `args` dan kita akan mengubah `args`
dengan melakukan iterasi atasnya, kita dapat menambahkan kata kunci `mut` ke
dalam spesifikasi parameter `args` untuk membuatnya *mutable*.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### Memakai Metode Trait `Iterator`

Selanjutnya, kita akan memperbaiki badan `Config::build`. Karena `args`
mengimplementasikan *trait* `Iterator`, kita tahu bahwa kita dapat memanggil
metode `next` padanya! Listing 13-20 memperbarui kode dari Listing 12-23
untuk memakai metode `next`.

<Listing number="13-20" file-name="src/main.rs" caption="Mengubah badan `Config::build` untuk memakai metode iterator">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```

</Listing>

Ingat bahwa nilai pertama di dalam nilai kembalian `env::args` adalah nama
programnya. Kita ingin mengabaikannya dan lanjut ke nilai berikutnya, jadi
pertama kita memanggil `next` dan tidak melakukan apa pun dengan nilai
kembaliannya. Lalu, kita memanggil `next` untuk mendapat nilai yang ingin
kita taruh di *field* `query` pada `Config`. Jika `next` mengembalikan `Some`,
kita memakai `match` untuk mengekstrak nilainya. Jika ia mengembalikan `None`,
itu berarti argumen yang diberikan tidak cukup, dan kita melakukan return dini
dengan nilai `Err`. Kita melakukan hal yang sama untuk nilai `file_path`.

<!-- Old headings. Do not remove or links may break. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### Memperjelas Kode dengan Iterator Adapter

Kita juga dapat memanfaatkan *iterator* di fungsi `search` pada proyek I/O
kita, yang ditampilkan ulang di sini pada Listing 13-21 sebagaimana adanya di
Listing 12-19.

<Listing number="13-21" file-name="src/lib.rs" caption="Implementasi fungsi `search` dari Listing 12-19">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Listing>

Kita dapat menulis kode ini dengan cara yang lebih ringkas memakai
metode-metode *iterator adapter*. Melakukannya juga memungkinkan kita
menghindari vektor `results` *mutable* perantara. Gaya pemrograman fungsional
lebih suka meminimalkan jumlah keadaan *mutable* untuk membuat kode lebih
jelas. Menghapus keadaan *mutable* mungkin memungkinkan penyempurnaan di masa
depan untuk membuat pencarian berjalan secara paralel karena kita tidak harus
mengelola akses konkuren ke vektor `results`. Listing 13-22 menunjukkan
perubahan ini.

<Listing number="13-22" file-name="src/lib.rs" caption="Memakai metode iterator adapter di dalam implementasi fungsi `search`">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Listing>

Ingat bahwa tujuan fungsi `search` adalah mengembalikan semua baris di
`contents` yang memuat `query`. Mirip dengan contoh `filter` di Listing 13-16,
kode ini memakai adapter `filter` untuk menyimpan hanya baris-baris yang
membuat `line.contains(query)` mengembalikan `true`. Kita lalu mengumpulkan
baris-baris yang cocok ke dalam vektor lain dengan `collect`. Jauh lebih
sederhana! Silakan membuat perubahan yang sama untuk memakai metode *iterator*
di fungsi `search_case_insensitive` juga.

Untuk penyempurnaan lebih lanjut, kembalikan sebuah *iterator* dari fungsi
`search` dengan menghapus pemanggilan `collect` dan mengubah return typenya
menjadi `impl Iterator<Item = &'a str>` sehingga fungsi itu menjadi sebuah
*iterator adapter*. Perhatikan bahwa Anda juga perlu memperbarui
pengujian-pengujiannya! Cari di file yang besar memakai alat `minigrep` Anda
sebelum dan sesudah melakukan perubahan ini untuk mengamati perbedaan
perilakunya. Sebelum perubahan ini, program tidak akan mencetak hasil apa pun
sampai ia mengumpulkan semua hasilnya, tetapi setelah perubahan ini,
hasil-hasilnya akan dicetak begitu setiap baris yang cocok ditemukan karena
perulangan `for` di fungsi `run` dapat memanfaatkan sifat *lazy* (kemalasan) *iterator*.

<!-- Old headings. Do not remove or links may break. -->

<a id="choosing-between-loops-or-iterators"></a>

### Memilih antara Perulangan atau Iterator

Pertanyaan logis berikutnya adalah gaya mana yang sebaiknya Anda pilih di
kode Anda sendiri dan mengapa: implementasi asli di Listing 13-21 atau versi
yang memakai *iterator* di Listing 13-22 (dengan asumsi kita mengumpulkan
semua hasilnya sebelum mengembalikannya, alih-alih mengembalikan
*iterator*-nya). Sebagian besar pemrogram Rust lebih suka memakai gaya
*iterator*. Sedikit lebih sulit untuk membiasakan diri pada awalnya, tetapi
begitu Anda mendapat pemahaman tentang berbagai *iterator adapter* dan apa yang
mereka lakukan, *iterator* bisa jadi lebih mudah dipahami. Alih-alih
mengutak-atik berbagai bagian perulangan dan membangun vektor-vektor baru,
kode berfokus pada tujuan tingkat tinggi dari perulangan tersebut. Ini
mengabstraksikan sebagian kode yang umum dijumpai sehingga lebih mudah
melihat konsep-konsep yang unik untuk kode ini, seperti kondisi penyaringan
yang harus dilewati setiap elemen di dalam *iterator*.

Tetapi apakah kedua implementasi itu benar-benar setara? Asumsi intuitifnya
mungkin adalah bahwa perulangan tingkat rendah akan lebih cepat. Mari kita
bicarakan performa.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
