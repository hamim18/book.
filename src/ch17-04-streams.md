<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

## Streams: Future dalam Urutan

Ingat kembali cara kita memakai receiver untuk channel async kita di awal bab
ini pada bagian [“Message Passing”][17-02-messages]<!-- ignore -->. Metode
async `recv` menghasilkan serangkaian item seiring waktu. Ini adalah instance
dari pola yang jauh lebih umum yang dikenal sebagai _stream_. Banyak konsep
yang secara alami direpresentasikan sebagai stream: item yang tersedia di
antrean, potongan-potongan data yang ditarik sedikit demi sedikit dari sistem
file ketika kumpulan datanya terlalu besar untuk memori komputer, atau data
yang tiba melalui jaringan seiring waktu. Karena stream adalah future, kita
bisa memakainya dengan future jenis apa pun dan menggabungkannya dengan
cara-cara yang menarik. Contohnya, kita bisa mengelompokkan event untuk
menghindari terlalu banyak panggilan jaringan, memasang timeout pada urutan
operasi yang berjalan lama, atau membatasi laju event antarmuka pengguna untuk
menghindari pekerjaan yang sia-sia.

Kita pernah melihat serangkaian item di Bab 13, ketika kita menelaah trait
Iterator di bagian [“Trait `Iterator` dan Metode `next`”][iterator-trait]<!--
ignore -->, tetapi ada dua perbedaan antara iterator dan receiver channel
async. Perbedaan pertama adalah waktu: iterator bersifat sinkron, sementara
receiver channel bersifat asinkron. Perbedaan kedua adalah API-nya. Saat
bekerja langsung dengan `Iterator`, kita memanggil metode sinkronnya, `next`.
Khusus pada stream `trpl::Receiver`, kita memanggil metode asinkron `recv`.
Selain itu, kedua API ini terasa sangat mirip, dan kemiripan itu bukanlah
kebetulan. Stream itu seperti bentuk iterasi yang asinkron. Akan tetapi,
sementara `trpl::Receiver` secara khusus menunggu untuk menerima pesan, API
stream serbaguna jauh lebih luas: API ini menyediakan item berikutnya
sebagaimana `Iterator`, tetapi secara asinkron.

Kemiripan antara iterator dan stream di Rust berarti kita benar-benar bisa
membuat sebuah stream dari iterator mana pun. Seperti halnya iterator, kita
bisa bekerja dengan stream dengan memanggil metode `next`-nya lalu menunggu
output-nya, seperti di Listing 17-21, yang belum bisa terkompilasi.

<Listing number="17-21" caption="Membuat stream dari iterator dan mencetak nilainya" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```

</Listing>

Kita mulai dengan array angka, yang kita ubah menjadi iterator lalu kita
panggil `map` padanya untuk menggandakan semua nilainya. Kemudian kita ubah
iterator itu menjadi stream menggunakan fungsi `trpl::stream_from_iter`.
Berikutnya, kita melakukan perulangan atas item-item di stream itu saat
mereka tiba dengan perulangan `while let`.

Sayangnya, saat kita mencoba menjalankan kodenya, kode itu tidak
terkompilasi, melainkan melaporkan bahwa tidak ada metode `next` yang
tersedia:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->

```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

Seperti yang dijelaskan output ini, alasan galat kompilatornya adalah kita
perlu trait yang tepat berada di scope untuk bisa memakai metode `next`.
Mengingat pembahasan kita sejauh ini, wajar jika Anda menduga trait itu adalah
`Stream`, tetapi sebenarnya `StreamExt`. Singkatan dari _extension_ (ekstensi),
`Ext` adalah pola umum di komunitas Rust untuk memperluas satu trait dengan
trait lain.

Trait `Stream` mendefinisikan antarmuka tingkat rendah yang secara efektif
menggabungkan trait `Iterator` dan `Future`. `StreamExt` menyediakan
sekumpulan API tingkat yang lebih tinggi di atas `Stream`, termasuk metode
`next` serta metode-metode utilitas lain yang serupa dengan yang disediakan
trait `Iterator`. `Stream` dan `StreamExt` belum menjadi bagian dari pustaka
standar Rust, tetapi sebagian besar crate ekosistem memakai definisi yang
serupa.

Perbaikan untuk galat kompilator itu adalah menambahkan pernyataan `use`
untuk `trpl::StreamExt`, seperti di Listing 17-22.

<Listing number="17-22" caption="Berhasil memakai iterator sebagai dasar sebuah stream" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```

</Listing>

Dengan semua bagian itu dirangkai, kode ini bekerja sesuai keinginan kita!
Terlebih lagi, sekarang setelah `StreamExt` berada di scope, kita bisa memakai
semua metode utilitasnya, sama seperti halnya iterator.

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method
