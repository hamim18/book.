## Refutabilitas: Apakah Sebuah Pola Mungkin Gagal Cocok

Pola hadir dalam dua bentuk: refutable dan irrefutable. Pola yang akan cocok
untuk nilai apa pun yang diteruskan bersifat _irrefutable_ (tidak dapat
dibantah). Contohnya adalah `x` pada pernyataan `let x = 5;` karena `x`
cocok dengan apa pun dan karena itu tidak mungkin gagal cocok. Pola yang bisa
gagal cocok untuk beberapa nilai yang mungkin bersifat _refutable_ (dapat
dibantah). Contohnya adalah `Some(x)` pada ekspresi `if let Some(x) =
a_value` karena jika nilai pada variabel `a_value` adalah `None` alih-alih
`Some`, pola `Some(x)` tidak akan cocok.

Parameter fungsi, pernyataan `let`, dan perulangan `for` hanya bisa menerima
pola irrefutable karena program tidak bisa melakukan apa pun yang bermakna
ketika nilai-nilainya tidak cocok. Ekspresi `if let` dan `while let` serta
pernyataan `let...else` menerima pola refutable dan irrefutable, tetapi
kompilator memperingatkan kita terhadap pola irrefutable karena, menurut
definisi, pola itu ditujukan untuk menangani kemungkinan kegagalan:
fungsionalitas sebuah kondisional terletak pada kemampuannya untuk berperilaku
berbeda bergantung pada keberhasilan atau kegagalan.

Secara umum, Anda tidak perlu khawatir tentang perbedaan antara pola
refutable dan irrefutable; tetapi, Anda perlu familier dengan konsep
refutabilitas supaya bisa merespons ketika Anda melihatnya di pesan galat.
Dalam kasus-kasus itu, Anda perlu mengubah pola atau konstruksi yang Anda
pakai bersama polanya, bergantung pada perilaku kode yang dimaksudkan.

Mari kita lihat contoh apa yang terjadi ketika kita mencoba memakai pola
refutable di tempat Rust mensyaratkan pola irrefutable, dan sebaliknya.
Listing 19-8 menunjukkan pernyataan `let`, tetapi untuk polanya, kita
menentukan `Some(x)`, sebuah pola refutable. Seperti yang mungkin Anda duga,
kode ini tidak akan terkompilasi.

<Listing number="19-8" caption="Mencoba memakai pola refutable dengan `let`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

Jika `some_option_value` adalah nilai `None`, ia akan gagal cocok dengan pola
`Some(x)`, yang berarti polanya refutable. Namun, pernyataan `let` hanya bisa
menerima pola irrefutable karena tidak ada yang valid yang bisa dilakukan kode
itu dengan nilai `None`. Pada waktu kompilasi, Rust akan mengeluh bahwa kita
telah mencoba memakai pola refutable di tempat pola irrefutable dibutuhkan:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

Karena kita tidak mencakup (dan tidak bisa mencakup!) setiap nilai yang valid
dengan pola `Some(x)`, Rust dengan benar menghasilkan galat kompilator.

Jika kita memiliki pola refutable di tempat pola irrefutable dibutuhkan, kita
bisa memperbaikinya dengan mengubah kode yang memakai pola itu: alih-alih
memakai `let`, kita bisa memakai `let...else`. Dengan begitu, jika polanya
tidak cocok, kode di dalam kurung kurawal akan menangani nilainya. Listing
19-9 menunjukkan cara memperbaiki kode di Listing 19-8.

<Listing number="19-9" caption="Memakai `let...else` dan blok dengan pola refutable alih-alih `let`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

Kita telah memberi jalan keluar untuk kode ini! Kode ini sepenuhnya valid,
meskipun itu berarti kita tidak bisa memakai pola irrefutable tanpa menerima
peringatan. Jika kita memberi `let...else` pola yang akan selalu cocok,
seperti `x`, seperti yang ditunjukkan di Listing 19-10, kompilator akan
memberikan peringatan.

<Listing number="19-10" caption="Mencoba memakai pola irrefutable dengan `let...else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

Rust mengeluh bahwa tidak masuk akal memakai `let...else` dengan pola
irrefutable karena `else`-nya tidak akan pernah tercapai:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

Karena alasan ini, arm match harus memakai pola refutable, kecuali arm
terakhir, yang seharusnya mencocokkan semua nilai yang tersisa dengan pola
irrefutable. Rust mengizinkan kita memakai pola irrefutable di `match` dengan
hanya satu arm, tetapi sintaks ini tidak terlalu berguna dan bisa diganti
dengan pernyataan `let` yang lebih sederhana.

Sekarang setelah Anda tahu tempat memakai pola dan perbedaan antara pola
refutable dan irrefutable, mari kita bahas semua sintaks yang bisa kita pakai
untuk membuat pola.
