<!-- Old headings. Do not remove or links may break. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>
<a id="closures-anonymous-functions-that-capture-their-environment"></a>

## Closure

*Closure* di Rust adalah fungsi anonim yang dapat Anda simpan di sebuah variabel
atau teruskan sebagai argumen ke fungsi lain. Anda dapat membuat *closure* di
satu tempat lalu memanggil *closure* itu di tempat lain untuk mengevaluasinya di
dalam konteks yang berbeda. Tidak seperti fungsi, *closure* dapat menangkap
nilai dari *scope* (cakupan) tempat *closure* itu didefinisikan. Kita akan
mendemonstrasikan bagaimana fitur-fitur *closure* ini memungkinkan pemakaian
ulang kode dan penyesuaian perilaku.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>
<a id="capturing-the-environment-with-closures"></a>

### Menangkap Lingkungan

Pertama-tama, kita akan menelaah bagaimana kita dapat memakai *closure* untuk
menangkap nilai dari lingkungan tempat *closure* itu didefinisikan untuk dipakai
nanti. Begini skenarionya: Sesekali, perusahaan kaos kita memberikan sebuah
kaos edisi terbatas yang eksklusif kepada seseorang di milis kita sebagai
promosi. Orang-orang di milis itu secara opsional dapat menambahkan warna
favorit mereka ke profil mereka. Jika orang yang terpilih untuk mendapat kaos
gratis telah menetapkan warna favoritnya, mereka mendapat kaos dengan warna
itu. Jika orang itu belum menentukan warna favorit, mereka mendapat warna apa
pun yang saat ini paling banyak dimiliki perusahaan.

Ada banyak cara untuk mengimplementasikan ini. Untuk contoh ini, kita akan
memakai sebuah *enum* bernama `ShirtColor` yang memiliki *variant* `Red` dan
`Blue` (membatasi jumlah warna yang tersedia demi kesederhanaan). Kita
merepresentasikan persediaan perusahaan dengan *struct* `Inventory` yang
memiliki sebuah *field* bernama `shirts` berisi `Vec<ShirtColor>` yang
merepresentasikan warna-warna kaos yang saat ini tersedia. Metode `giveaway`
yang didefinisikan pada `Inventory` menerima preferensi warna kaos yang
opsional dari pemenang kaos gratis, dan mengembalikan warna kaos yang akan
didapat orang tersebut. Susunan ini ditunjukkan di Listing 13-1.

<Listing number="13-1" file-name="src/main.rs" caption="Situasi pemberian hadiah kaos perusahaan">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-01/src/main.rs}}
```

</Listing>

`store` yang didefinisikan di `main` memiliki dua kaos biru dan satu kaos
merah tersisa untuk dibagikan dalam promosi edisi terbatas ini. Kita memanggil
metode `giveaway` untuk seorang pengguna dengan preferensi kaos merah dan
seorang pengguna tanpa preferensi apa pun.

Lagi-lagi, kode ini bisa diimplementasikan dengan banyak cara, dan di sini,
untuk berfokus pada *closure*, kita bertahan pada konsep-konsep yang telah Anda
pelajari, kecuali badan metode `giveaway` yang memakai sebuah *closure*. Di
metode `giveaway`, kita menerima preferensi pengguna sebagai parameter
bertipe `Option<ShirtColor>` dan memanggil metode `unwrap_or_else` pada
`user_preference`. [Metode `unwrap_or_else` pada `Option<T>`][unwrap-or-else]<!--
ignore --> didefinisikan oleh pustaka standar. Metode ini menerima satu
argumen: sebuah *closure* tanpa argumen yang mengembalikan nilai `T` (tipe yang
sama dengan yang disimpan di *variant* `Some` dari `Option<T>`, dalam kasus
ini `ShirtColor`). Jika `Option<T>`-nya berupa *variant* `Some`,
`unwrap_or_else` mengembalikan nilai dari dalam `Some`. Jika `Option<T>`-nya
berupa *variant* `None`, `unwrap_or_else` memanggil *closure* itu dan
mengembalikan nilai yang dikembalikan oleh *closure* tersebut.

Kita menentukan ekspresi *closure* `|| self.most_stocked()` sebagai argumen
untuk `unwrap_or_else`. Ini adalah *closure* yang tidak menerima parameter (jika
*closure* itu punya parameter, parameter-parameter itu akan muncul di antara dua
garis vertikal). Badan *closure* itu memanggil `self.most_stocked()`. Di sini
kita sedang mendefinisikan *closure* itu, dan implementasi `unwrap_or_else` akan
mengevaluasi *closure* tersebut nanti jika hasilnya diperlukan.

Menjalankan kode ini mencetak yang berikut:

```console
{{#include ../listings/ch13-functional-features/listing-13-01/output.txt}}
```

Satu aspek menarik di sini adalah kita telah meneruskan sebuah *closure* yang
memanggil `self.most_stocked()` pada instance `Inventory` saat ini. Pustaka
standar tidak perlu mengetahui apa pun tentang tipe `Inventory` atau
`ShirtColor` yang kita definisikan, ataupun logika yang ingin kita pakai dalam
skenario ini. *Closure* itu menangkap sebuah *reference* *immutable* (tidak dapat
diubah) ke instance `Inventory` `self` dan meneruskannya beserta kode yang
kita tentukan ke metode `unwrap_or_else`. Sebaliknya, fungsi tidak mampu
menangkap lingkungannya dengan cara seperti ini.

<!-- Old headings. Do not remove or links may break. -->

<a id="closure-type-inference-and-annotation"></a>

### Menginferensi dan Menganotasi Tipe Closure

Ada lebih banyak perbedaan antara fungsi dan *closure*. *Closure* biasanya tidak
mengharuskan Anda menganotasi tipe-tipe parameter atau nilai kembaliannya
seperti fungsi `fn`. Anotasi tipe diwajibkan pada fungsi karena tipe-tipe itu
adalah bagian dari *interface* (antarmuka) eksplisit yang diekspos kepada
pengguna Anda. Mendefinisikan *interface* ini secara kaku penting untuk
memastikan bahwa semua orang sepakat tentang tipe nilai apa yang dipakai dan
dikembalikan sebuah fungsi. Sebaliknya, *closure* tidak dipakai di dalam
*interface* yang diekspos seperti ini: *Closure* disimpan di dalam variabel, dan
dipakai tanpa menamainya dan mengeksposnya kepada pengguna pustaka kita.

*Closure* biasanya pendek dan hanya relevan di dalam konteks yang sempit, bukan
di skenario yang sembarangan. Di dalam konteks yang terbatas ini, *compiler*
dapat menginferensi tipe-tipe parameter dan tipe kembaliannya, mirip dengan
kemampuannya menginferensi tipe-tipe sebagian besar variabel (ada kasus
langka ketika *compiler* juga memerlukan anotasi tipe *closure*).

Seperti halnya variabel, kita dapat menambahkan anotasi tipe jika ingin
meningkatkan keeksplisitan dan kejelasan dengan biaya menjadi lebih
bertele-tele daripada yang benar-benar diperlukan. Menganotasi tipe-tipe untuk
sebuah *closure* akan tampak seperti definisi yang ditunjukkan di Listing 13-2.
Dalam contoh ini, kita mendefinisikan sebuah *closure* dan menyimpannya di dalam
sebuah variabel alih-alih mendefinisikan *closure* itu di tempat kita
meneruskannya sebagai argumen, seperti yang kita lakukan di Listing 13-1.

<Listing number="13-2" file-name="src/main.rs" caption="Menambahkan anotasi tipe opsional untuk tipe parameter dan nilai kembalian di dalam closure">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-02/src/main.rs:here}}
```

</Listing>

Dengan anotasi tipe yang ditambahkan, sintaks *closure* tampak lebih mirip
dengan sintaks fungsi. Di sini, kita mendefinisikan sebuah fungsi yang
menambahkan 1 ke parameternya dan sebuah *closure* dengan perilaku yang sama,
sebagai perbandingan. Kita telah menambahkan beberapa spasi untuk
menyelaraskan bagian-bagian yang relevan. Ini mengilustrasikan bagaimana
sintaks *closure* mirip dengan sintaks fungsi kecuali dalam pemakaian pipa dan
banyaknya sintaks yang bersifat opsional:

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

Baris pertama menunjukkan definisi fungsi dan baris kedua menunjukkan definisi
*closure* yang dianotasi sepenuhnya. Di baris ketiga, kita menghapus anotasi
tipe dari definisi *closure*. Di baris keempat, kita menghapus kurung
kurawalnya, yang bersifat opsional karena badan *closure* hanya memiliki satu
ekspresi. Semua ini adalah definisi yang valid dan akan menghasilkan perilaku
yang sama ketika dipanggil. Baris `add_one_v3` dan `add_one_v4` mengharuskan
*closure*-closure itu dievaluasi agar dapat terkompilasi karena tipe-tipenya
akan diinferensi dari pemakaiannya. Ini mirip dengan `let v = Vec::new();`
yang memerlukan anotasi tipe ataupun nilai-nilai bertipe tertentu untuk
dimasukkan ke dalam `Vec` agar Rust dapat menginferensi tipenya.

Untuk definisi *closure*, *compiler* akan menginferensi satu tipe konkret untuk
setiap parameternya dan untuk nilai kembaliannya. Misalnya, Listing 13-3
menunjukkan definisi sebuah *closure* pendek yang hanya mengembalikan nilai
yang diterimanya sebagai parameter. *Closure* ini tidak terlalu berguna kecuali
untuk keperluan contoh ini. Perhatikan bahwa kita belum menambahkan anotasi
tipe apa pun ke definisinya. Karena tidak ada anotasi tipe, kita dapat
memanggil *closure* itu dengan tipe apa pun, yang telah kita lakukan di sini
dengan `String` pada pemanggilan pertama. Jika kemudian kita mencoba memanggil
`example_closure` dengan sebuah integer, kita akan mendapat error.

<Listing number="13-3" file-name="src/main.rs" caption="Mencoba memanggil closure yang tipe-tipenya diinferensi dengan dua tipe yang berbeda">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-03/src/main.rs:here}}
```

</Listing>

*Compiler* memberi kita error ini:

```console
{{#include ../listings/ch13-functional-features/listing-13-03/output.txt}}
```

Pertama kali kita memanggil `example_closure` dengan nilai `String`,
*compiler* menginferensi tipe `x` dan tipe kembalian *closure* itu sebagai
`String`. Tipe-tipe itu kemudian dikunci ke dalam *closure* di
`example_closure`, dan kita mendapat error tipe ketika selanjutnya mencoba
memakai tipe yang berbeda dengan *closure* yang sama.

<a id="capturing-references-or-moving-ownership"></a>
### Menangkap Reference atau Memindahkan Ownership

*Closure* dapat menangkap nilai dari lingkungannya dengan tiga cara, yang
berpadanan langsung dengan tiga cara sebuah fungsi menerima parameter:
meminjam secara *immutable*, meminjam secara *mutable* (dapat diubah), dan
mengambil *ownership* (kepemilikan). *Closure* akan memutuskan mana yang dipakai
berdasarkan apa yang dilakukan badan fungsi itu terhadap nilai-nilai yang
ditangkap.

Di Listing 13-4, kita mendefinisikan sebuah *closure* yang menangkap sebuah
*reference* *immutable* ke vektor bernama `list` karena *closure* itu hanya
memerlukan *reference* *immutable* untuk mencetak nilainya.

<Listing number="13-4" file-name="src/main.rs" caption="Mendefinisikan dan memanggil closure yang menangkap reference immutable">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-04/src/main.rs}}
```

</Listing>

Contoh ini juga mengilustrasikan bahwa sebuah variabel dapat terikat ke
definisi *closure*, dan nanti kita dapat memanggil *closure* itu dengan memakai
nama variabel beserta tanda kurung, seolah-olah nama variabel itu adalah nama
fungsi.

Karena kita dapat memiliki banyak *reference* *immutable* ke `list` pada saat
yang sama, `list` tetap dapat diakses dari kode sebelum definisi *closure*,
setelah definisi *closure* tetapi sebelum *closure* dipanggil, dan setelah *closure*
dipanggil. Kode ini terkompilasi, berjalan, dan mencetak:

```console
{{#include ../listings/ch13-functional-features/listing-13-04/output.txt}}
```

Selanjutnya, di Listing 13-5, kita mengubah badan *closure* sehingga *closure* itu
menambahkan sebuah elemen ke vektor `list`. *Closure* itu kini menangkap sebuah
*reference* *mutable*.

<Listing number="13-5" file-name="src/main.rs" caption="Mendefinisikan dan memanggil closure yang menangkap reference mutable">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-05/src/main.rs}}
```

</Listing>

Kode ini terkompilasi, berjalan, dan mencetak:

```console
{{#include ../listings/ch13-functional-features/listing-13-05/output.txt}}
```

Perhatikan bahwa tidak ada lagi `println!` di antara definisi dan pemanggilan
*closure* `borrows_mutably`: Ketika `borrows_mutably` didefinisikan, ia
menangkap sebuah *reference* *mutable* ke `list`. Kita tidak memakai *closure* itu
lagi setelah *closure* itu dipanggil, jadi peminjaman *mutable*-nya berakhir. Di
antara definisi *closure* dan pemanggilan *closure*, peminjaman *immutable* untuk
mencetak tidak diizinkan, karena tidak ada peminjaman lain yang diizinkan
ketika ada peminjaman *mutable*. Coba tambahkan `println!` di sana untuk melihat
pesan error apa yang Anda dapat!

Jika Anda ingin memaksa *closure* mengambil *ownership* atas nilai-nilai yang
dipakainya di lingkungan, meskipun badan *closure* itu tidak benar-benar
memerlukan *ownership*, Anda dapat memakai kata kunci `move` sebelum daftar
parameternya.

Teknik ini paling berguna ketika meneruskan sebuah *closure* ke thread baru
untuk memindahkan data sehingga data itu dimiliki oleh thread baru. Kita akan
membahas thread dan alasan Anda ingin memakainya secara mendetail di Bab 16
ketika kita berbicara tentang konkurensi, tetapi untuk saat ini, mari kita
menelaah secara singkat pembuatan thread baru memakai *closure* yang memerlukan
kata kunci `move`. Listing 13-6 menunjukkan Listing 13-4 yang dimodifikasi
untuk mencetak vektor di thread baru alih-alih di thread utama.

<Listing number="13-6" file-name="src/main.rs" caption="Memakai `move` untuk memaksa closure bagi thread itu mengambil ownership atas `list`">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-06/src/main.rs}}
```

</Listing>

Kita membuat sebuah thread baru, memberikan *closure* untuk dijalankan sebagai
argumen kepada thread itu. Badan *closure* itu mencetak daftarnya. Di Listing
13-4, *closure* hanya menangkap `list` memakai *reference* *immutable* karena
itulah jumlah akses minimum ke `list` yang diperlukan untuk mencetaknya.
Dalam contoh ini, meskipun badan *closure* tetap hanya memerlukan *reference*
*immutable*, kita perlu menyatakan bahwa `list` harus dipindahkan ke dalam
*closure* dengan menaruh kata kunci `move` di awal definisi *closure*. Jika thread
utama melakukan lebih banyak operasi sebelum memanggil `join` pada thread
baru, thread baru itu mungkin selesai sebelum sisa thread utama selesai, atau
thread utama mungkin selesai lebih dulu. Jika thread utama tetap memegang
*ownership* atas `list` tetapi berakhir sebelum thread baru dan membebaskan
`list`, *reference* *immutable* di dalam thread itu akan menjadi tidak valid.
Karena itu, *compiler* mengharuskan `list` dipindahkan ke dalam *closure* yang
diberikan kepada thread baru supaya *reference*-nya tetap valid. Coba hapus kata
kunci `move` atau pakai `list` di thread utama setelah *closure* didefinisikan
untuk melihat error kompilasi apa yang Anda dapat!

<!-- Old headings. Do not remove or links may break. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>
<a id="moving-captured-values-out-of-closures-and-the-fn-traits"></a>

<a id="moving-captured-values-out-of-closures"></a>
### Memindahkan Nilai yang Ditangkap Keluar dari Closure

Setelah sebuah *closure* menangkap *reference* atau menangkap *ownership* atas
sebuah nilai dari lingkungan tempat *closure* itu didefinisikan (sehingga
memengaruhi apa, jika ada, yang dipindahkan _ke dalam_ *closure*), kode di badan
*closure* menentukan apa yang terjadi pada *reference* atau nilai-nilai itu ketika
*closure* dievaluasi nanti (sehingga memengaruhi apa, jika ada, yang dipindahkan
_keluar dari_ *closure*).

Badan *closure* dapat melakukan salah satu dari hal berikut: Memindahkan nilai
yang ditangkap keluar dari *closure*, mengubah nilai yang ditangkap, tidak
memindahkan ataupun mengubah nilai itu, atau sejak awal tidak menangkap apa
pun dari lingkungan.

Cara sebuah *closure* menangkap dan menangani nilai-nilai dari lingkungan
memengaruhi *trait* mana yang diimplementasikan *closure* itu, dan *trait*
adalah cara fungsi dan *struct* menentukan jenis *closure* apa yang dapat mereka
pakai. *Closure* akan secara otomatis mengimplementasikan satu, dua, atau ketiga
*trait* `Fn` ini, secara aditif, bergantung pada bagaimana badan *closure*
menangani nilai-nilainya:

* `FnOnce` berlaku untuk *closure* yang hanya dapat dipanggil sekali. Semua
  *closure* mengimplementasikan setidaknya *trait* ini karena semua *closure*
  dapat dipanggil. *Closure* yang memindahkan nilai-nilai yang ditangkap keluar
  dari badannya hanya akan mengimplementasikan `FnOnce` dan tidak satu pun
  *trait* `Fn` lainnya, karena *closure* itu hanya dapat dipanggil sekali.
* `FnMut` berlaku untuk *closure* yang tidak memindahkan nilai-nilai yang
  ditangkap keluar dari badannya, tetapi mungkin mengubah nilai-nilai yang
  ditangkap. *Closure* ini dapat dipanggil lebih dari sekali.
* `Fn` berlaku untuk *closure* yang tidak memindahkan nilai-nilai yang ditangkap
  keluar dari badannya dan tidak mengubah nilai-nilai yang ditangkap, serta
  *closure* yang tidak menangkap apa pun dari lingkungannya. *Closure* ini dapat
  dipanggil lebih dari sekali tanpa mengubah lingkungannya, yang penting dalam
  kasus seperti memanggil sebuah *closure* berkali-kali secara konkuren.

Mari kita lihat definisi metode `unwrap_or_else` pada `Option<T>` yang kita
pakai di Listing 13-1:

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

Ingat bahwa `T` adalah tipe generik yang merepresentasikan tipe nilai di dalam
*variant* `Some` dari sebuah `Option`. Tipe `T` itu juga merupakan tipe
kembalian fungsi `unwrap_or_else`: Kode yang memanggil `unwrap_or_else` pada
`Option<String>`, misalnya, akan mendapat sebuah `String`.

Selanjutnya, perhatikan bahwa fungsi `unwrap_or_else` memiliki parameter tipe
generik tambahan `F`. Tipe `F` adalah tipe dari parameter bernama `f`, yaitu
*closure* yang kita berikan saat memanggil `unwrap_or_else`.

*Trait bound* (batasan *trait*) yang ditentukan pada tipe generik `F` adalah
`FnOnce() -> T`, yang berarti `F` harus dapat dipanggil sekali, tidak
menerima argumen, dan mengembalikan sebuah `T`. Memakai `FnOnce` di *trait
bound* itu mengekspresikan batasan bahwa `unwrap_or_else` tidak akan memanggil
`f` lebih dari sekali. Di badan `unwrap_or_else`, kita dapat melihat bahwa
jika `Option`-nya berupa `Some`, `f` tidak akan dipanggil. Jika `Option`-nya
berupa `None`, `f` akan dipanggil sekali. Karena semua *closure*
mengimplementasikan `FnOnce`, `unwrap_or_else` menerima ketiga jenis *closure*
dan sefleksibel mungkin.

> Catatan: Jika yang ingin kita lakukan tidak memerlukan penangkapan nilai
> dari lingkungan, kita dapat memakai nama fungsi alih-alih *closure* di tempat
> yang memerlukan sesuatu yang mengimplementasikan salah satu *trait* `Fn`.
> Misalnya, pada nilai `Option<Vec<T>>`, kita dapat memanggil
> `unwrap_or_else(Vec::new)` untuk mendapat vektor baru yang kosong jika
> nilainya `None`. *Compiler* secara otomatis mengimplementasikan *trait* `Fn`
> mana pun yang berlaku untuk sebuah definisi fungsi.

Sekarang mari kita lihat metode pustaka standar `sort_by_key`, yang
didefinisikan pada *slice*, untuk melihat perbedaannya dari `unwrap_or_else` dan
alasan `sort_by_key` memakai `FnMut` alih-alih `FnOnce` untuk *trait bound*-nya.
*Closure* itu menerima satu argumen berupa *reference* ke item saat ini di dalam
*slice* yang sedang dipertimbangkan, dan mengembalikan nilai bertipe `K` yang
dapat diurutkan. Fungsi ini berguna ketika Anda ingin mengurutkan sebuah *slice*
berdasarkan atribut tertentu dari setiap itemnya. Di Listing 13-7, kita
memiliki daftar instance `Rectangle`, dan kita memakai `sort_by_key` untuk
mengurutkannya berdasarkan atribut `width` dari rendah ke tinggi.

<Listing number="13-7" file-name="src/main.rs" caption="Memakai `sort_by_key` untuk mengurutkan persegi panjang berdasarkan lebar">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-07/src/main.rs}}
```

</Listing>

Kode ini mencetak:

```console
{{#include ../listings/ch13-functional-features/listing-13-07/output.txt}}
```

Alasan `sort_by_key` didefinisikan untuk menerima *closure* `FnMut` adalah
karena ia memanggil *closure* itu berkali-kali: sekali untuk setiap item di
dalam *slice*. *Closure* `|r| r.width` tidak menangkap, mengubah, atau
memindahkan apa pun keluar dari lingkungannya, jadi *closure* itu memenuhi
syarat *trait bound*-nya.

Sebaliknya, Listing 13-8 menunjukkan contoh *closure* yang hanya
mengimplementasikan *trait* `FnOnce`, karena *closure* itu memindahkan sebuah
nilai keluar dari lingkungan. *Compiler* tidak akan mengizinkan kita memakai
*closure* ini bersama `sort_by_key`.

<Listing number="13-8" file-name="src/main.rs" caption="Mencoba memakai closure `FnOnce` bersama `sort_by_key`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-08/src/main.rs}}
```

</Listing>

Ini adalah cara yang dibuat-buat dan berbelit (yang tidak bekerja) untuk
mencoba menghitung berapa kali `sort_by_key` memanggil *closure* ketika
mengurutkan `list`. Kode ini berusaha melakukan penghitungan itu dengan
memasukkan `value`—sebuah `String` dari lingkungan *closure*—ke dalam vektor
`sort_operations`. *Closure* itu menangkap `value` lalu memindahkan `value`
keluar dari *closure* dengan mentransfer *ownership* atas `value` ke vektor
`sort_operations`. *Closure* ini hanya dapat dipanggil sekali; mencoba
memanggilnya untuk kedua kalinya tidak akan bekerja, karena `value` tidak lagi
berada di lingkungan untuk dimasukkan ke dalam `sort_operations` lagi! Karena
itu, *closure* ini hanya mengimplementasikan `FnOnce`. Ketika kita mencoba
mengompilasi kode ini, kita mendapat error bahwa `value` tidak dapat
dipindahkan keluar dari *closure* karena *closure* itu harus mengimplementasikan
`FnMut`:

```console
{{#include ../listings/ch13-functional-features/listing-13-08/output.txt}}
```

Error itu menunjuk ke baris di badan *closure* yang memindahkan `value` keluar
dari lingkungan. Untuk memperbaikinya, kita perlu mengubah badan *closure* agar
ia tidak memindahkan nilai keluar dari lingkungan. Menyimpan sebuah penghitung
di lingkungan dan menaikkan nilainya di badan *closure* adalah cara yang lebih
lugas untuk menghitung berapa kali *closure* dipanggil. *Closure* di Listing 13-9
bekerja bersama `sort_by_key` karena ia hanya menangkap sebuah *reference*
*mutable* ke penghitung `num_sort_operations`, dan karena itu dapat dipanggil
lebih dari sekali.

<Listing number="13-9" file-name="src/main.rs" caption="Memakai closure `FnMut` bersama `sort_by_key` diizinkan.">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-09/src/main.rs}}
```

</Listing>

*Trait* `Fn` penting ketika mendefinisikan atau memakai fungsi atau tipe yang
memanfaatkan *closure*. Di bagian berikutnya, kita akan membahas *iterator*.
Banyak metode *iterator* menerima argumen *closure*, jadi ingat-ingat detail
*closure* ini selagi kita melanjutkan!

[unwrap-or-else]: ../std/option/enum.Option.html#method.unwrap_or_else
