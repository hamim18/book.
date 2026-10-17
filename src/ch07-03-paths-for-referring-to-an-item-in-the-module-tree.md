## Path untuk Merujuk Item di dalam Pohon Modul

Untuk menunjukkan kepada Rust tempat menemukan sebuah item di dalam *module*
*tree*, kita memakai *path* dengan cara yang sama seperti kita memakai *path* saat
menavigasi sistem file. Untuk memanggil sebuah fungsi, kita perlu tahu
*path*-nya.

Sebuah *path* dapat berbentuk salah satu dari dua bentuk berikut:

- Sebuah *absolute path* (*path* absolut) adalah *path* lengkap yang dimulai dari
  *crate root*; untuk kode dari *crate* eksternal, *path* absolut dimulai dengan
  nama *crate*, dan untuk kode dari *crate* saat ini, *path* itu dimulai dengan
  literal `crate`.
- Sebuah *relative path* (*path* relatif) dimulai dari *module* saat ini dan
  memakai `self`, `super`, atau sebuah *identifier* (pengidentifikasi) di
  *module* saat ini.

Baik *path* absolut maupun relatif diikuti oleh satu identifier atau lebih yang
dipisahkan oleh titik dua ganda (`::`).

Kembali ke Listing 7-1, katakanlah kita ingin memanggil fungsi
`add_to_waitlist`. Ini sama dengan bertanya: Apa *path* dari fungsi
`add_to_waitlist`? Listing 7-3 berisi Listing 7-1 dengan sebagian *module* dan
fungsinya dihilangkan.

Kita akan menunjukkan dua cara memanggil fungsi `add_to_waitlist` dari sebuah
fungsi baru, `eat_at_restaurant`, yang didefinisikan di *crate root*. *Path*-path
ini benar, tetapi masih ada satu masalah lain yang tersisa yang akan mencegah
contoh ini terkompilasi apa adanya. Kami akan menjelaskan alasannya sebentar
lagi.

Fungsi `eat_at_restaurant` adalah bagian dari API publik *crate* library kita,
jadi kita menandainya dengan *keyword* `pub`. Di bagian [“Mengekspos *Path*
dengan Kata Kunci `pub`”][pub]<!-- ignore -->, kita akan membahas `pub` lebih
detail.

<Listing number="7-3" file-name="src/lib.rs" caption="Memanggil fungsi `add_to_waitlist` memakai path absolut dan relatif">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

Pertama kali kita memanggil fungsi `add_to_waitlist` di `eat_at_restaurant`,
kita memakai *path* absolut. Fungsi `add_to_waitlist` didefinisikan di *crate*
yang sama dengan `eat_at_restaurant`, yang berarti kita dapat memakai kata
kunci `crate` untuk memulai sebuah *path* absolut. Kita lalu menyertakan setiap
*module* berikutnya hingga kita sampai di `add_to_waitlist`. Anda dapat
membayangkan sebuah sistem file dengan struktur yang sama: kita akan
menuliskan *path* `/front_of_house/hosting/add_to_waitlist` untuk menjalankan
program `add_to_waitlist`; memakai nama `crate` untuk memulai dari *crate root*
seperti memakai `/` untuk memulai dari akar sistem file di shell Anda.

Kedua kalinya kita memanggil `add_to_waitlist` di `eat_at_restaurant`, kita
memakai *path* relatif. *Path* dimulai dengan `front_of_house`, nama *module* yang
didefinisikan di tingkat yang sama pada *module tree* dengan
`eat_at_restaurant`. Di sini padanan sistem filenya adalah memakai *path*
`front_of_house/hosting/add_to_waitlist`. Memulai dengan nama *module* berarti
*path* tersebut relatif.

Memilih apakah memakai *path* relatif atau absolut adalah keputusan yang akan
Anda buat berdasarkan proyek Anda, dan itu bergantung pada apakah Anda lebih
mungkin memindahkan kode definisi item terpisah dari atau bersama-sama dengan
kode yang memakai item tersebut. Misalnya, jika kita memindahkan *module*
`front_of_house` dan fungsi `eat_at_restaurant` ke dalam sebuah *module*
bernama `customer_experience`, kita perlu memperbarui *path* absolut menuju
`add_to_waitlist`, tetapi *path* relatifnya akan tetap berlaku. Namun, jika
kita memindahkan fungsi `eat_at_restaurant` secara terpisah ke dalam sebuah
*module* bernama `dining`, *path* absolut menuju pemanggilan `add_to_waitlist`
akan tetap sama, tetapi *path* relatifnya perlu diperbarui. Preferensi kita
secara umum adalah menuliskan *path* absolut karena kemungkinan besar kita
ingin memindahkan definisi kode dan pemanggilan item secara independen satu
sama lain.

Mari kita coba mengompilasi Listing 7-3 dan mencari tahu mengapa listing itu
belum bisa dikompilasi! Error yang kita dapatkan ditunjukkan di Listing 7-4.

<Listing number="7-4" caption="Error compiler dari membangun kode di Listing 7-3">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

Pesan errornya mengatakan bahwa *module* `hosting` bersifat privat. Dengan kata
lain, kita memiliki *path* yang benar untuk *module* `hosting` dan fungsi
`add_to_waitlist`, tetapi Rust tidak mengizinkan kita memakainya karena Rust
tidak memiliki akses ke bagian-bagian privat tersebut. Di Rust, semua item
(fungsi, method, *struct*, *enum*, *module*, dan constant) bersifat privat
terhadap *module* induknya secara default. Jika Anda ingin menjadikan item
seperti fungsi atau *struct* privat, Anda menempatkannya di dalam sebuah
*module*.

Item di *module* induk tidak dapat memakai item privat di dalam *module* anak,
tetapi item di *module* anak dapat memakai item di *module*-module leluhurnya.
Ini karena *module* anak membungkus dan menyembunyikan detail implementasinya,
tetapi *module* anak dapat melihat konteks tempat mereka didefinisikan.
Melanjutkan metafora kita, bayangkan aturan privasi seperti kantor belakang
sebuah restoran: apa yang terjadi di sana bersifat privat bagi pelanggan
restoran, tetapi manajer kantor dapat melihat dan melakukan apa pun di
restoran yang mereka operasikan.

Rust memilih untuk membuat *module system* berfungsi seperti ini supaya
menyembunyikan detail implementasi bagian dalam menjadi default. Dengan
begitu, Anda tahu bagian mana dari kode bagian dalam yang dapat Anda ubah
tanpa merusak kode bagian luar. Namun, Rust memang memberi Anda opsi untuk
mengekspos bagian dalam kode *module* anak ke *module* leluhur di luarnya dengan
memakai *keyword* `pub` untuk menjadikan sebuah item publik.

<a id="exposing-paths-with-the-pub-keyword"></a>
### Mengekspos Path dengan Kata Kunci `pub`

Mari kita kembali ke error di Listing 7-4 yang memberi tahu kita bahwa *module*
`hosting` bersifat privat. Kita ingin fungsi `eat_at_restaurant` di *module*
induk memiliki akses ke fungsi `add_to_waitlist` di *module* anak, jadi kita
menandai *module* `hosting` dengan *keyword* `pub`, seperti yang ditunjukkan
di Listing 7-5.

<Listing number="7-5" file-name="src/lib.rs" caption="Mendeklarasikan module `hosting` sebagai `pub` untuk memakainya dari `eat_at_restaurant`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

Sayangnya, kode di Listing 7-5 tetap menghasilkan error *compiler*, seperti
yang ditunjukkan di Listing 7-6.

<Listing number="7-6" caption="Error compiler dari membangun kode di Listing 7-5">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

Apa yang terjadi? Menambahkan *keyword* `pub` di depan `mod hosting`
menjadikan *module* tersebut publik. Dengan perubahan ini, jika kita dapat
mengakses `front_of_house`, kita dapat mengakses `hosting`. Tetapi _isi_ dari
`hosting` masih privat; menjadikan *module* publik tidak menjadikan isinya
publik. *keyword* `pub` pada sebuah *module* hanya mengizinkan kode di
*module*-module leluhurnya untuk merujuk kepadanya, bukan untuk mengakses kode
bagian dalamnya. Karena *module* adalah kontainer, tidak banyak yang bisa kita
lakukan hanya dengan menjadikan *module* publik; kita perlu melangkah lebih
jauh dan memilih untuk menjadikan satu item atau lebih di dalam *module* ikut
publik.

Error di Listing 7-6 mengatakan bahwa fungsi `add_to_waitlist` bersifat
privat. Aturan privasi berlaku untuk *struct*, *enum*, fungsi, dan method, juga
*module*.

Mari kita jadikan fungsi `add_to_waitlist` publik dengan menambahkan kata
kunci `pub` sebelum definisinya, seperti di Listing 7-7.

<Listing number="7-7" file-name="src/lib.rs" caption="Menambahkan *keyword* `pub` ke `mod hosting` dan `fn add_to_waitlist` memungkinkan kita memanggil fungsi tersebut dari `eat_at_restaurant`.">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

Kini kode tersebut akan terkompilasi! Untuk melihat mengapa menambahkan kata
kunci `pub` memungkinkan kita memakai *path*-path ini di `eat_at_restaurant`
menurut aturan privasi, mari kita lihat *path* absolut dan *path* relatifnya.

Pada *path* absolut, kita memulai dengan `crate`, akar *module tree* *crate* kita.
*Module* `front_of_house` didefinisikan di *crate root*. Meskipun
`front_of_house` tidak publik, karena fungsi `eat_at_restaurant`
didefinisikan di *module* yang sama dengan `front_of_house` (artinya,
`eat_at_restaurant` dan `front_of_house` adalah sibling), kita dapat merujuk
`front_of_house` dari `eat_at_restaurant`. Berikutnya adalah *module*
`hosting` yang ditandai dengan `pub`. Kita dapat mengakses *module* induk dari
`hosting`, jadi kita dapat mengakses `hosting`. Terakhir, fungsi
`add_to_waitlist` ditandai dengan `pub`, dan kita dapat mengakses *module*
induknya, jadi pemanggilan fungsi ini berhasil!

Pada *path* relatif, logikanya sama dengan *path* absolut kecuali pada langkah
pertama: alih-alih memulai dari *crate root*, *path* dimulai dari
`front_of_house`. *Module* `front_of_house` didefinisikan di dalam *module* yang
sama dengan `eat_at_restaurant`, jadi *path* relatif yang dimulai dari *module*
tempat `eat_at_restaurant` didefinisikan bekerja. Lalu, karena `hosting` dan
`add_to_waitlist` ditandai dengan `pub`, sisa *path* bekerja, dan pemanggilan
fungsi ini valid!

Jika Anda berencana membagikan *crate* library Anda supaya proyek lain dapat
memakai kode Anda, API publik Anda adalah kontrak Anda dengan para pengguna
*crate* Anda yang menentukan bagaimana mereka dapat berinteraksi dengan kode
Anda. Ada banyak pertimbangan seputar pengelolaan perubahan pada API publik
Anda untuk memudahkan orang bergantung pada *crate* Anda.
Pertimbangan-pertimbangan ini berada di luar coverage buku ini; jika Anda
tertarik pada topik ini, lihat [Rust API Guidelines][api-guidelines].

> #### Praktik Terbaik untuk Package dengan Binary dan Library
>
> Kita telah menyebutkan bahwa sebuah *package* dapat berisi _src/main.rs_
> sebagai *crate root* binary dan juga _src/lib.rs_ sebagai *crate root* library,
> dan kedua *crate* tersebut akan memiliki nama *package* secara default.
> Biasanya, *package* dengan pattern berisi library dan *crate* binary seperti ini
> akan memiliki kode yang cukup sedikit di *crate* binary untuk memulai sebuah
> file yang dapat dieksekusi yang memanggil kode yang didefinisikan di *crate*
> library. Ini memungkinkan proyek lain menikmati fungsionalitas terbanyak
> yang disediakan *package* karena kode *crate* library dapat dibagikan.
>
> *Module tree* harus didefinisikan di _src/lib.rs_. Lalu, item publik mana pun
> dapat dipakai di *crate* binary dengan memulai *path* dengan nama *package*.
> *Crate* binary menjadi pengguna *crate* library sama seperti *crate* yang
> sepenuhnya eksternal akan memakai *crate* library tersebut: ia hanya dapat
> memakai API publik. Ini membantu Anda merancang API yang baik; Anda bukan
> hanya penulis, tetapi juga klien!
>
> Di [Bab 12][ch12]<!-- ignore -->, kita akan mendemonstrasikan praktik
> pengaturan ini dengan sebuah program command line yang akan berisi *crate*
> binary dan *crate* library.

### Memulai Path Relatif dengan `super`

Kita dapat menyusun *path* relatif yang dimulai di *module* induk, alih-alih
*module* saat ini atau *crate root*, dengan memakai `super` di awal *path*. Ini
seperti memulai *path* sistem file dengan sintaks `..` yang berarti pergi ke
direktori induk. Memakai `super` memungkinkan kita merujuk sebuah item yang
kita tahu berada di *module* induk, yang dapat mempermudah penataan ulang
*module tree* ketika *module* tersebut berkaitan erat dengan induknya tetapi
induknya mungkin dipindahkan ke tempat lain di *module tree* suatu hari nanti.

Perhatikan kode di Listing 7-8 yang memodelkan situasi ketika seorang koki
memperbaiki pesanan yang salah dan secara pribadi membawanya keluar kepada
pelanggan. Fungsi `fix_incorrect_order` yang didefinisikan di *module*
`back_of_house` memanggil fungsi `deliver_order` yang didefinisikan di *module*
induk dengan menuliskan *path* menuju `deliver_order`, dimulai dengan `super`.

<Listing number="7-8" file-name="src/lib.rs" caption="Memanggil sebuah fungsi memakai path relatif yang dimulai dengan `super`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

Fungsi `fix_incorrect_order` berada di *module* `back_of_house`, jadi kita
dapat memakai `super` untuk pergi ke *module* induk dari `back_of_house`, yang
dalam kasus ini adalah `crate`, sang akar. Dari sana, kita mencari
`deliver_order` dan menemukannya. Berhasil! Kami rasa *module* `back_of_house`
dan fungsi `deliver_order` kemungkinan akan tetap dalam hubungan yang sama
satu sama lain dan ikut pindah bersama-sama seandainya kita memutuskan untuk
mengatur ulang *module tree* *crate*. Karena itu, kita memakai `super` supaya
kita punya lebih sedikit tempat untuk memperbarui kode di masa depan jika
kode ini dipindahkan ke *module* lain.

### Menjadikan Struct dan Enum Publik

Kita juga dapat memakai `pub` untuk menetapkan *struct* dan *enum* sebagai
publik, tetapi ada beberapa detail tambahan pada pemakaian `pub` dengan
*struct* dan *enum*. Jika kita memakai `pub` sebelum definisi *struct*, kita
menjadikan *struct* publik, tetapi *field*-field *struct* akan tetap privat. Kita
dapat menjadikan setiap *field* publik atau tidak, satu per satu. Di Listing
7-9, kita telah mendefinisikan *struct* publik `back_of_house::Breakfast`
dengan *field* `toast` yang publik tetapi *field* `seasonal_fruit` yang privat.
Ini memodelkan kasus di sebuah restoran ketika pelanggan dapat memilih jenis
roti yang menyertai hidangan, tetapi koki yang menentukan buah apa yang
menyertai hidangan berdasarkan apa yang sedang musim dan tersedia di stok.
Buah yang tersedia berubah dengan cepat, jadi pelanggan tidak dapat memilih
buahnya atau bahkan melihat buah apa yang akan mereka dapatkan.

<Listing number="7-9" file-name="src/lib.rs" caption="Sebuah struct dengan sebagian field publik dan sebagian field privat">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

Karena *field* `toast` di *struct* `back_of_house::Breakfast` publik, di
`eat_at_restaurant` kita dapat menulis dan membaca *field* `toast` memakai
notasi titik. Perhatikan bahwa kita tidak dapat memakai *field*
`seasonal_fruit` di `eat_at_restaurant`, karena `seasonal_fruit` privat. Coba
batalkan komentar pada baris yang mengubah nilai *field* `seasonal_fruit` untuk
melihat error apa yang Anda dapatkan!

Juga, perhatikan bahwa karena `back_of_house::Breakfast` memiliki *field*
privat, *struct* tersebut perlu menyediakan *associated function* (fungsi
asosiasi) publik yang mengonstruksi sebuah instance `Breakfast` (di sini kita
menamainya `summer`). Jika `Breakfast` tidak memiliki fungsi seperti itu,
kita tidak dapat membuat instance `Breakfast` di `eat_at_restaurant`, karena
kita tidak dapat menetapkan nilai *field* privat `seasonal_fruit` di
`eat_at_restaurant`.

Sebaliknya, jika kita menjadikan sebuah *enum* publik, semua *variant*
(varian)-nya ikut publik. Kita hanya perlu `pub` sebelum *keyword* `enum`,
seperti yang ditunjukkan di Listing 7-10.

<Listing number="7-10" file-name="src/lib.rs" caption="Menetapkan sebuah enum sebagai publik menjadikan semua variant-nya publik.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

Karena kita menjadikan *enum* `Appetizer` publik, kita dapat memakai variant
`Soup` dan `Salad` di `eat_at_restaurant`.

*Enum* tidak terlalu berguna kecuali variant-nya publik; akan menyebalkan jika
harus menganotasi semua variant *enum* dengan `pub` di setiap kasus, jadi
default untuk variant *enum* adalah publik. *Struct* sering berguna tanpa
*field*-fieldnya publik, jadi *field* *struct* mengikuti aturan umum bahwa
semuanya privat secara default kecuali dianotasi dengan `pub`.

Ada satu situasi lagi yang melibatkan `pub` yang belum kita bahas, dan itu
adalah fitur *module system* terakhir kita: *keyword* `use`. Kita akan
membahas `use` sendiri terlebih dahulu, lalu kita akan menunjukkan cara
menggabungkan `pub` dan `use`.

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html
