## Refutabilitas: Apakah Sebuah Pattern Mungkin Gagal Cocok

Pattern hadir dalam dua bentuk: *refutable* dan *irrefutable*. Pattern yang akan cocok
untuk nilai apa pun yang diteruskan bersifat _irrefutable_ (tidak dapat
dibantah). Contohnya adalah `x` pada statement `let x = 5;` karena `x`
cocok dengan apa pun dan karena itu tidak mungkin gagal cocok. Pattern yang bisa
gagal cocok untuk beberapa nilai yang mungkin bersifat _refutable_ (dapat
dibantah). Contohnya adalah `Some(x)` pada expression `if let Some(x) =
a_value` karena jika nilai pada variable `a_value` adalah `None` alih-alih
`Some`, pattern `Some(x)` tidak akan cocok.

Parameter fungsi, statement `let`, dan loop `for` hanya bisa menerima
pattern *irrefutable* karena program tidak bisa melakukan apa pun yang bermakna
ketika nilai-nilainya tidak cocok. Expression `if let` dan `while let` serta
statement `let...else` menerima pattern *refutable* dan *irrefutable*, tetapi
*compiler* memperingatkan kita terhadap pattern *irrefutable* karena, menurut
definisi, konstruksi kondisional itulah yang dimaksudkan untuk menangani kemungkinan kegagalan:
fungsionalitas sebuah kondisional terletak pada kemampuannya untuk berperilaku
berbeda bergantung pada keberhasilan atau kegagalan.

Secara umum, Anda tidak perlu khawatir tentang perbedaan antara pattern
*refutable* dan *irrefutable*; tetapi, Anda perlu familier dengan konsep
refutabilitas supaya bisa merespons ketika Anda melihatnya di pesan error.
Dalam kasus-kasus itu, Anda perlu mengubah pattern atau konstruksi yang Anda
pakai bersama patternnya, bergantung pada perilaku kode yang dimaksudkan.

Mari kita lihat contoh apa yang terjadi ketika kita mencoba memakai pattern
*refutable* di tempat Rust mensyaratkan pattern *irrefutable*, dan sebaliknya.
Listing 19-8 menunjukkan statement `let`, tetapi untuk patternnya, kita
menentukan `Some(x)`, sebuah pattern *refutable*. Seperti yang mungkin Anda duga,
kode ini tidak akan terkompilasi.

<Listing number="19-8" caption="Mencoba memakai pattern refutable dengan `let`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

Jika `some_option_value` adalah nilai `None`, ia akan gagal cocok dengan pattern
`Some(x)`, yang berarti patternnya *refutable*. Namun, statement `let` hanya bisa
menerima pattern *irrefutable* karena tidak ada yang valid yang bisa dilakukan kode
itu dengan nilai `None`. Pada waktu kompilasi, Rust akan mengeluh bahwa kita
telah mencoba memakai pattern *refutable* di tempat pattern *irrefutable* dibutuhkan:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

Karena kita tidak mencakup (dan tidak bisa mencakup!) setiap nilai yang valid
dengan pattern `Some(x)`, Rust dengan benar menghasilkan error *compiler*.

Jika kita memiliki pattern *refutable* di tempat pattern *irrefutable* dibutuhkan, kita
bisa memperbaikinya dengan mengubah kode yang memakai pattern itu: alih-alih
memakai `let`, kita bisa memakai `let...else`. Dengan begitu, jika patternnya
tidak cocok, kode di dalam kurung kurawal akan menangani nilainya. Listing
19-9 menunjukkan cara memperbaiki kode di Listing 19-8.

<Listing number="19-9" caption="Memakai `let...else` dan blok dengan pattern refutable alih-alih `let`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

Kita telah memberi jalan keluar untuk kode ini! Kode ini sepenuhnya valid,
meskipun itu berarti kita tidak bisa memakai pattern *irrefutable* tanpa menerima
peringatan. Jika kita memberi `let...else` pattern yang akan selalu cocok,
seperti `x`, seperti yang ditunjukkan di Listing 19-10, *compiler* akan
memberikan peringatan.

<Listing number="19-10" caption="Mencoba memakai pattern irrefutable dengan `let...else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

Rust mengeluh bahwa tidak masuk akal memakai `let...else` dengan pattern
*irrefutable* karena `else`-nya tidak akan pernah tercapai:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

Karena alasan ini, arm match harus memakai pattern *refutable*, kecuali arm
terakhir, yang seharusnya mencocokkan semua nilai yang tersisa dengan pattern
*irrefutable*. Rust mengizinkan kita memakai pattern *irrefutable* di `match` dengan
hanya satu arm, tetapi sintaks ini tidak terlalu berguna dan bisa diganti
dengan statement `let` yang lebih sederhana.

Sekarang setelah Anda tahu tempat memakai pattern dan perbedaan antara pattern
*refutable* dan *irrefutable*, mari kita bahas semua sintaks yang bisa kita pakai
untuk membuat pattern.
