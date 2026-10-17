## Fungsi dan Closure Lanjutan

Seksi ini mengeksplorasi beberapa fitur lanjutan yang berkaitan dengan fungsi
dan *closure*, termasuk *pointer* fungsi dan mengembalikan *closure*.

### Pointer Fungsi

Kita sudah membahas cara memberikan *closure* ke fungsi; Anda juga bisa
memberikan fungsi biasa ke fungsi! Teknik ini berguna ketika Anda ingin
memberikan fungsi yang sudah Anda definisikan alih-alih mendefinisikan
*closure* baru. Fungsi terkoersi menjadi type `fn` (dengan huruf *f* kecil),
jangan tertukar dengan *trait* *closure* `Fn`. Type `fn` disebut *function
pointer* (*pointer* fungsi). Memberikan fungsi dengan *pointer* fungsi akan
memungkinkan Anda memakai fungsi sebagai argumen untuk fungsi lain.

Sintaks untuk menentukan bahwa sebuah parameter adalah *pointer* fungsi mirip
dengan sintaks *closure*, seperti yang ditunjukkan di Listing 20-28, tempat
kita mendefinisikan fungsi `add_one` yang menambahkan 1 ke parameternya.
Fungsi `do_twice` menerima dua parameter: sebuah *pointer* fungsi ke fungsi apa
pun yang menerima parameter `i32` dan mengembalikan `i32`, dan satu nilai
`i32`. Fungsi `do_twice` memanggil fungsi `f` dua kali, memberikannya nilai
`arg`, lalu menjumlahkan hasil kedua pemanggilan fungsi itu. Fungsi `main`
memanggil `do_twice` dengan argumen `add_one` dan `5`.

<Listing number="20-28" file-name="src/main.rs" caption="Memakai type `fn` untuk menerima pointer fungsi sebagai argumen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

Kode ini mencetak `The answer is: 12`. Kita menentukan bahwa parameter `f`
di `do_twice` adalah `fn` yang menerima satu parameter typed `i32` dan
mengembalikan `i32`. Kita kemudian bisa memanggil `f` di tubuh `do_twice`.
Di `main`, kita bisa memberikan nama fungsi `add_one` sebagai argumen pertama
ke `do_twice`.

Tidak seperti *closure*, `fn` adalah type, bukan *trait*, jadi kita menuliskan
`fn` langsung sebagai type parameter alih-alih mendeklarasikan type parameter
generik dengan salah satu *trait* `Fn` sebagai *trait bound*.

*Pointer* fungsi mengimplementasikan ketiga *trait* *closure* (`Fn`, `FnMut`, dan
`FnOnce`), artinya Anda selalu bisa memberikan *pointer* fungsi sebagai argumen
untuk fungsi yang mengharapkan *closure*. Sebaiknya tulis fungsi dengan memakai
generic type dan salah satu *trait* *closure* supaya fungsi Anda bisa menerima
fungsi ataupun *closure*.

Meskipun begitu, satu contoh situasi di mana Anda hanya ingin menerima `fn`
dan bukan *closure* adalah saat berinteraksi dengan kode eksternal yang tidak
memiliki *closure*: Fungsi C bisa menerima fungsi sebagai argumen, tetapi C
tidak memiliki *closure*.

Sebagai contoh situasi di mana Anda bisa memakai *closure* yang didefinisikan
secara inline ataupun fungsi bernama, mari kita lihat pemakaian method `map`
yang disediakan *trait* `Iterator` di standard library. Untuk memakai method
`map` guna mengubah vector berisi angka menjadi vector berisi string, kita
bisa memakai *closure*, seperti di Listing 20-29.

<Listing number="20-29" caption="Memakai closure dengan method `map` untuk mengubah angka menjadi string">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

Atau kita bisa memberikan fungsi bernama sebagai argumen `map`, bukan
*closure*. Listing 20-30 menunjukkan tampilannya.

<Listing number="20-30" caption="Memakai fungsi `String::to_string` dengan method `map` untuk mengubah angka menjadi string">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa kita harus memakai sintaks fully qualified yang kita bahas
di seksi [“Trait Lanjutan”][advanced-traits]<!-- ignore --> karena ada banyak
fungsi bernama `to_string` yang tersedia.

Di sini, kita memakai fungsi `to_string` yang didefinisikan di *trait*
`ToString`, yang telah diimplementasikan standard library untuk type apa pun
yang mengimplementasikan `Display`.

Ingat kembali dari seksi [“Nilai Enum”][enum-values]<!-- ignore --> di Bab 6
bahwa nama setiap varian *enum* yang kita definisikan juga menjadi fungsi
penginisialisasi. Kita bisa memakai fungsi-fungsi penginisialisasi ini
sebagai *pointer* fungsi yang mengimplementasikan *trait*-trait *closure*, yang
berarti kita bisa memberikan fungsi-fungsi penginisialisasi itu sebagai
argumen untuk method yang menerima *closure*, seperti terlihat di Listing
20-31.

<Listing number="20-31" caption="Memakai penginisialisasi enum dengan method `map` untuk membuat instance `Status` dari angka">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

Di sini, kita membuat instance `Status::Value` dengan memakai setiap nilai
`u32` di range tempat `map` dipanggil, yaitu dengan memakai fungsi
penginisialisasi `Status::Value`. Sebagian orang lebih menyukai gaya ini dan
sebagian lagi lebih suka memakai *closure*. Keduanya terkompilasi menjadi kode
yang sama, jadi pakailah gaya mana pun yang lebih jelas bagi Anda.

### Mengembalikan Closure

*Closure* direpresentasikan oleh *trait*, yang berarti Anda tidak bisa
mengembalikan *closure* secara langsung. Pada sebagian besar kasus ketika Anda
ingin mengembalikan sebuah *trait*, Anda bisa memakai type konkret yang
mengimplementasikan *trait* itu sebagai return value fungsi. Akan tetapi,
biasanya Anda tidak bisa melakukan itu dengan *closure* karena *closure* tidak
memiliki type konkret yang bisa dikembalikan; misalnya, Anda tidak diizinkan
memakai *pointer* fungsi `fn` sebagai return type jika *closure* itu menangkap
nilai apa pun dari *scope*-nya.

Sebagai gantinya, biasanya Anda akan memakai sintaks `impl Trait` yang kita
pelajari di Bab 10. Anda bisa mengembalikan type fungsi apa pun, dengan
memakai `Fn`, `FnOnce`, dan `FnMut`. Misalnya, kode di Listing 20-32 akan
terkompilasi dengan baik.

<Listing number="20-32" caption="Mengembalikan closure dari fungsi dengan memakai sintaks `impl Trait`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

Akan tetapi, seperti yang kita catat di seksi [“Menginferensi dan
Menganotasi Type *Closure*”][*closure*-types]<!-- ignore --> pada Bab 13, setiap
*closure* juga merupakan typenya sendiri yang berbeda. Jika Anda perlu bekerja
dengan banyak fungsi yang memiliki *signature* yang sama tetapi implementasi
yang berbeda, Anda perlu memakai *trait object* untuk fungsi-fungsi itu.
Perhatikan apa yang terjadi jika Anda menulis kode seperti yang ditunjukkan
di Listing 20-33.

<Listing file-name="src/main.rs" number="20-33" caption="Membuat `Vec<T>` berisi closure yang didefinisikan oleh fungsi-fungsi yang mengembalikan type `impl Fn`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

Di sini kita punya dua fungsi, `returns_closure` dan
`returns_initialized_closure`, yang sama-sama mengembalikan `impl Fn(i32) ->
i32`. Perhatikan bahwa *closure* yang mereka kembalikan berbeda, meskipun
keduanya mengimplementasikan type yang sama. Jika kita mencoba
mengompilasinya, Rust memberi tahu kita bahwa itu tidak akan bekerja:

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

Pesan error itu memberi tahu kita bahwa setiap kali kita mengembalikan `impl
Trait`, Rust membuat *opaque type* (tipe opak) yang unik, yaitu type yang
detailnya tidak bisa kita lihat dari apa yang Rust bangun untuk kita, dan
kita juga tidak bisa menebak type yang akan dihasilkan Rust untuk kita tulis
sendiri. Jadi, meskipun fungsi-fungsi ini mengembalikan *closure* yang
mengimplementasikan *trait* yang sama, `Fn(i32) -> i32`, type opak yang
dihasilkan Rust untuk masing-masing fungsi berbeda. (Ini mirip dengan cara
Rust menghasilkan type konkret yang berbeda untuk blok async yang berbeda
meskipun type outputnya sama, seperti yang kita lihat di [“Type `Pin` dan
*Trait* `Unpin`”][*future*-types]<!-- ignore --> pada Bab 17.) Kita sudah melihat
solusi untuk masalah ini beberapa kali: Kita bisa memakai *trait object*,
seperti di Listing 20-34.

<Listing number="20-34" caption="Membuat `Vec<T>` berisi closure yang didefinisikan oleh fungsi-fungsi yang mengembalikan `Box<dyn Fn>` sehingga semuanya typed sama">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

Kode ini akan terkompilasi dengan baik. Untuk lebih lanjut tentang *trait*
object, lihat seksi [“Memakai *Trait Object* untuk Mengabstraksi Perilaku
Bersama”][*trait*-objects]<!-- ignore --> pada Bab 18.

Selanjutnya, mari kita lihat *macro*!

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[future-types]: ch17-03-more-futures.html
[trait-objects]: ch18-02-trait-objects.html
