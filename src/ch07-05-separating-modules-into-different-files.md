## Memisahkan Module ke dalam File yang Berbeda

Sejauh ini, semua contoh di bab ini mendefinisikan beberapa *module* di satu
file. Ketika *module* membesar, Anda mungkin ingin memindahkan definisinya ke
file terpisah untuk membuat kodenya lebih mudah dinavigasi.

Misalnya, mari kita mulai dari kode di Listing 7-17 yang memiliki beberapa
*module* restoran. Kita akan mengekstrak *module* ke dalam file-file, alih-alih
mendefinisikan semua *module* di file *crate root*. Dalam kasus ini, file *crate*
root adalah _src/lib.rs_, tetapi prosedur ini juga berlaku untuk *crate*
binary yang file *crate root*-nya adalah _src/main.rs_.

Pertama, kita akan mengekstrak *module* `front_of_house` ke filenya sendiri.
Hapus kode di dalam kurung kurawal untuk *module* `front_of_house`, sisakan
hanya deklarasi `mod front_of_house;`, sehingga _src/lib.rs_ berisi kode yang
ditunjukkan di Listing 7-21. Perhatikan bahwa ini tidak akan terkompilasi
sampai kita membuat file _src/front_of_house.rs_ di Listing 7-22.

<Listing number="7-21" file-name="src/lib.rs" caption="Mendeklarasikan module `front_of_house` yang badannya akan berada di *src/front_of_house.rs*">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/lib.rs}}
```

</Listing>

Berikutnya, tempatkan kode yang tadinya berada di dalam kurung kurawal ke
dalam file baru bernama _src/front_of_house.rs_, seperti yang ditunjukkan di
Listing 7-22. *Compiler* tahu untuk mencari di file ini karena ia menemukan
deklarasi *module* di *crate root* dengan nama `front_of_house`.

<Listing number="7-22" file-name="src/front_of_house.rs" caption="Definisi-definisi di dalam module `front_of_house` di *src/front_of_house.rs*">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/front_of_house.rs}}
```

</Listing>

Perhatikan bahwa Anda hanya perlu memuat sebuah file memakai deklarasi `mod`
_sekali_ di *module tree* Anda. Begitu *compiler* tahu bahwa file itu adalah
bagian dari proyek (dan tahu di mana letak kode itu di *module tree* karena
posisi pernyataan `mod` yang Anda tulis), file-file lain di proyek Anda harus
merujuk kode file yang dimuat itu memakai *path* menuju tempat ia
dideklarasikan, seperti yang dibahas di bagian [“*Path* untuk Merujuk Item di
dalam Pohon Modul”][paths]<!-- ignore -->. Dengan kata lain, `mod` _bukanlah_
operasi “include” yang mungkin pernah Anda lihat di bahasa pemrograman lain.

Berikutnya, kita akan mengekstrak *module* `hosting` ke filenya sendiri.
Prosesnya sedikit berbeda karena `hosting` adalah *module* anak dari
`front_of_house`, bukan dari *module* akar. Kita akan menempatkan file untuk
`hosting` di direktori baru yang diberi nama sesuai leluhurnya di *module*
*tree*, dalam kasus ini _src/front_of_house_.

Untuk mulai memindahkan `hosting`, kita mengubah _src/front_of_house.rs_
agar hanya berisi deklarasi *module* `hosting`:

<Listing file-name="src/front_of_house.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house.rs}}
```

</Listing>

Lalu, kita membuat direktori _src/front_of_house_ dan file _hosting.rs_ untuk
menampung definisi-definisi yang dibuat di *module* `hosting`:

<Listing file-name="src/front_of_house/hosting.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house/hosting.rs}}
```

</Listing>

Jika alih-alih kita menempatkan _hosting.rs_ di direktori _src_, *compiler*
akan mengharapkan kode _hosting.rs_ berada di *module* `hosting` yang
dideklarasikan di *crate root* dan bukan dideklarasikan sebagai anak dari
*module* `front_of_house`. Aturan *compiler* tentang file mana yang diperiksa
untuk kode *module* mana berarti direktori dan file akan lebih mendekati *module*
*tree*.

<a id="alternate-file-paths"></a>
> ### Path File Alternatif
>
> Sejauh ini kita telah membahas *path* file yang paling idiomatis yang dipakai
> *compiler* Rust, tetapi Rust juga mendukung gaya *path* file yang lebih lama.
> Untuk sebuah *module* bernama `front_of_house` yang dideklarasikan di *crate*
> root, *compiler* akan mencari kode *module* tersebut di:
>
> - _src/front_of_house.rs_ (yang kita bahas)
> - _src/front_of_house/mod.rs_ (gaya lama, *path* yang masih didukung)
>
> Untuk sebuah *module* bernama `hosting` yang merupakan submodule dari
> `front_of_house`, *compiler* akan mencari kode *module* tersebut di:
>
> - _src/front_of_house/hosting.rs_ (yang kita bahas)
> - _src/front_of_house/hosting/mod.rs_ (gaya lama, *path* yang masih didukung)
>
> Jika Anda memakai kedua gaya untuk *module* yang sama, Anda akan mendapat
> galat *compiler*. Memakai campuran kedua gaya untuk *module*-module yang
> berbeda di proyek yang sama diperbolehkan, tetapi mungkin membingungkan
> orang yang menavigasi proyek Anda.
>
> Kelemahan utama gaya yang memakai file bernama _mod.rs_ adalah proyek Anda
> bisa berakhir dengan banyak file bernama _mod.rs_, yang bisa membingungkan
> ketika Anda membukanya di editor secara bersamaan.

Kita telah memindahkan kode setiap *module* ke file terpisah, dan *module tree*
tetap sama. Pemanggilan fungsi di `eat_at_restaurant` akan bekerja tanpa
modifikasi apa pun, meskipun definisinya tinggal di file yang berbeda. Teknik
ini memungkinkan Anda memindahkan *module* ke file baru seiring membesarnya
ukuran *module*.

Perhatikan bahwa pernyataan `pub use crate::front_of_house::hosting` di
_src/lib.rs_ juga tidak berubah, dan `use` tidak memiliki dampak apa pun
terhadap file mana yang dikompilasi sebagai bagian dari *crate*. Kata kunci
`mod` mendeklarasikan *module*, dan Rust mencari di file dengan nama yang sama
dengan *module* untuk kode yang masuk ke *module* itu.

## Ringkasan

Rust memungkinkan Anda membagi sebuah *package* menjadi beberapa *crate* dan
sebuah *crate* menjadi *module* sehingga Anda dapat merujuk item yang
didefinisikan di satu *module* dari *module* lain. Anda dapat melakukannya dengan
menuliskan *path* absolut atau relatif. *Path*-path ini dapat dibawa ke dalam
*scope* dengan pernyataan `use` sehingga Anda dapat memakai *path* yang lebih
pendek untuk beberapa pemakaian item di *scope* itu. Kode *module* bersifat
privat secara default, tetapi Anda dapat menjadikan definisi publik dengan
menambahkan kata kunci `pub`.

Di bab berikutnya, kita akan melihat beberapa struktur data koleksi di
pustaka standar yang dapat Anda pakai di kode yang tertata rapi.

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
