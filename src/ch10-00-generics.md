# Type Generik, Trait, dan Lifetime

Setiap bahasa pemrograman memiliki alat untuk menangani duplikasi konsep
secara efektif. Di Rust, salah satu alat tersebut adalah *generics* (tipe
generik): pengganti abstrak untuk type konkret atau properti lain. Kita bisa
mengekspresikan perilaku *generics* atau bagaimana mereka berhubungan dengan
*generics* lain tanpa mengetahui apa yang akan berada di tempatnya saat kode
dikompilasi dan dijalankan.

Fungsi dapat menerima parameter typed generik, alih-alih type konkret
seperti `i32` atau `String`, sama seperti mereka menerima parameter dengan
nilai yang tidak diketahui untuk menjalankan kode yang sama pada banyak nilai
konkret. Nyatanya, kita sudah memakai *generics* di Bab 6 dengan `Option<T>`,
di Bab 8 dengan `Vec<T>` dan `HashMap<K, V>`, serta di Bab 9 dengan
`Result<T, E>`. Di bab ini, Anda akan mengeksplorasi cara mendefinisikan
type, fungsi, dan metode Anda sendiri dengan *generics*!

Pertama, kita akan meninjau cara mengekstrak fungsi untuk mengurangi
duplikasi kode. Kemudian, kita akan memakai teknik yang sama untuk membuat
fungsi generik dari dua fungsi yang hanya berbeda pada type parameternya.
Kita juga akan menjelaskan cara memakai generic type dalam definisi *struct*
dan *enum*.

Kemudian, Anda akan mempelajari cara memakai *trait* untuk mendefinisikan
perilaku secara generik. Anda bisa menggabungkan *trait* dengan generic type
untuk membatasi generic type agar hanya menerima type-type yang memiliki
perilaku tertentu, alih-alih sembarang type.

Terakhir, kita akan membahas *lifetime* (masa hidup): sejenis *generics* yang
memberi *compiler* (kompilator) informasi tentang bagaimana *reference*
(referensi) berhubungan satu sama lain. *Lifetime* memungkinkan kita memberi
*compiler* informasi yang cukup tentang nilai yang dipinjam sehingga ia bisa
memastikan bahwa *reference* akan tetap valid dalam lebih banyak situasi
daripada yang bisa ia lakukan tanpa bantuan kita.

## Menghilangkan Duplikasi dengan Mengekstrak Fungsi

*Generics* memungkinkan kita mengganti type spesifik dengan placeholder yang
mewakili banyak type untuk menghilangkan duplikasi kode. Sebelum menyelami
sintaks *generics*, mari kita lihat dulu cara menghilangkan duplikasi dengan
cara yang tidak melibatkan generic type, yaitu dengan mengekstrak fungsi yang
mengganti nilai spesifik dengan placeholder yang mewakili banyak nilai.
Kemudian, kita akan menerapkan teknik yang sama untuk mengekstrak fungsi
generik! Dengan melihat cara mengenali kode duplikat yang bisa Anda ekstrak
menjadi sebuah fungsi, Anda akan mulai mengenali kode duplikat yang bisa
memakai *generics*.

Kita akan mulai dengan program pendek di Listing 10-1 yang menemukan angka
terbesar dalam sebuah daftar.

<Listing number="10-1" file-name="src/main.rs" caption="Menemukan angka terbesar dalam sebuah daftar angka">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-01/src/main.rs:here}}
```

</Listing>

Kita menyimpan daftar bilangan bulat dalam variable `number_list` dan
menempatkan *reference* ke angka pertama dalam daftar itu pada variable
bernama `largest`. Kita kemudian mengiterasi seluruh angka dalam daftar itu,
dan jika angka saat ini lebih besar daripada angka yang tersimpan di
`largest`, kita mengganti *reference* di variable tersebut. Akan tetapi, jika
angka saat ini lebih kecil dari atau sama dengan angka terbesar yang sudah
terlihat sejauh ini, variable itu tidak berubah dan kode melanjutkan ke angka
berikutnya dalam daftar. Setelah mempertimbangkan semua angka dalam daftar,
`largest` seharusnya merujuk ke angka terbesar, yang dalam kasus ini adalah
100.

Sekarang kita ditugasi untuk menemukan angka terbesar dalam dua daftar angka
yang berbeda. Untuk melakukannya, kita bisa memilih untuk menduplikasi kode
di Listing 10-1 dan memakai logika yang sama di dua tempat berbeda dalam
program, seperti yang ditunjukkan di Listing 10-2.

<Listing number="10-2" file-name="src/main.rs" caption="Kode untuk menemukan angka terbesar dalam *dua* daftar angka">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-02/src/main.rs}}
```

</Listing>

Meskipun kode ini berfungsi, menduplikasi kode itu melelahkan dan rawan
error. Kita juga harus ingat untuk memperbarui kode di banyak tempat ketika
kita ingin mengubahnya.

Untuk menghilangkan duplikasi ini, kita akan membuat sebuah abstraksi dengan
mendefinisikan fungsi yang beroperasi pada daftar bilangan bulat mana pun yang
dimasukkan sebagai parameter. Solusi ini membuat kode kita lebih jelas dan
memungkinkan kita mengekspresikan konsep menemukan angka terbesar dalam
sebuah daftar secara abstrak.

Di Listing 10-3, kita mengekstrak kode yang menemukan angka terbesar menjadi
sebuah fungsi bernama `largest`. Lalu, kita memanggil fungsi itu untuk
menemukan angka terbesar dalam dua daftar dari Listing 10-2. Kita juga bisa
memakai fungsi ini pada daftar nilai `i32` lain mana pun yang mungkin kita
miliki di masa depan.

<Listing number="10-3" file-name="src/main.rs" caption="Kode yang diabstraksikan untuk menemukan angka terbesar dalam dua daftar">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-03/src/main.rs:here}}
```

</Listing>

Fungsi `largest` memiliki parameter bernama `list`, yang mewakili *slice*
konkret berisi nilai `i32` mana pun yang mungkin kita teruskan ke fungsi
tersebut. Alhasil, ketika kita memanggil fungsi itu, kodenya berjalan pada
nilai-nilai spesifik yang kita teruskan.

Ringkasnya, berikut langkah-langkah yang kita ambil untuk mengubah kode dari
Listing 10-2 menjadi Listing 10-3:

1. Identifikasi kode duplikat.
1. Ekstrak kode duplikat itu ke dalam badan fungsi, dan tentukan input serta
   return value kode itu di tanda tangan fungsi.
1. Perbarui dua instance kode duplikat itu agar memanggil fungsi tersebut.

Selanjutnya, kita akan memakai langkah-langkah yang sama dengan *generics*
untuk mengurangi duplikasi kode. Sama seperti badan fungsi yang dapat
beroperasi pada `list` yang abstrak alih-alih nilai-nilai spesifik, *generics*
memungkinkan kode beroperasi pada type-type abstrak.

Sebagai contoh, katakanlah kita memiliki dua fungsi: satu yang menemukan item
terbesar dalam sebuah *slice* berisi nilai `i32` dan satu yang menemukan item
terbesar dalam sebuah *slice* berisi nilai `char`. Bagaimana kita
menghilangkan duplikasi itu? Mari kita cari tahu!
