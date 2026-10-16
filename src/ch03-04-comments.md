## Komentar

Semua pemrogram berusaha membuat kode mereka mudah dipahami, tetapi
kadang-kadang penjelasan tambahan memang diperlukan. Pada kasus seperti itu,
pemrogram meninggalkan komentar di kode sumber mereka yang akan diabaikan
compiler tetapi mungkin berguna bagi orang yang membaca kode sumbernya.

Berikut komentar sederhana:

```rust
// hello, world
```

Di Rust, gaya komentar yang idiomatis memulai komentar dengan dua garis
miring, dan komentarnya berlanjut sampai akhir baris. Untuk komentar yang
melebihi satu baris, Anda perlu menyertakan `//` pada setiap baris, seperti
ini:

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

Komentar juga dapat diletakkan di akhir baris yang berisi kode:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

Tetapi Anda akan lebih sering melihat komentar dipakai dalam format ini, yaitu
komentar berada di baris terpisah di atas kode yang dianotasikannya:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

Rust juga memiliki jenis komentar lain, yaitu komentar dokumentasi, yang akan
kita bahas di bagian [“Menerbitkan Crate ke Crates.io”][publishing]<!-- ignore
--> pada Bab 14.

[publishing]: ch14-02-publishing-to-crates-io.html
