## Memproses Serangkaian Item dengan Iterator

Pattern *iterator* memungkinkan Anda melakukan suatu tugas pada urutan item
secara bergantian. Sebuah *iterator* bertanggung jawab atas logika iterasi
pada setiap item dan menentukan kapan urutannya berakhir. Ketika Anda memakai
*iterator*, Anda tidak perlu mengimplementasikan ulang logika itu sendiri.

Di Rust, *iterator* bersifat _lazy_ (malas), artinya *iterator* tidak memiliki
efek apa pun sampai Anda memanggil method yang mengonsumsi *iterator* itu
untuk menghabiskannya. Misalnya, kode di Listing 13-10 membuat sebuah
*iterator* atas item-item di dalam vector `v1` dengan memanggil method `iter`
yang didefinisikan pada `Vec<T>`. Kode ini saja tidak melakukan apa pun yang
berguna.

<Listing number="13-10" file-name="src/main.rs" caption="Membuat iterator">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```

</Listing>

*Iterator* itu disimpan di variable `v1_iter`. Setelah membuat sebuah
*iterator*, kita dapat memakainya dengan berbagai cara. Di Listing 3-5, kita
melakukan iterasi atas sebuah array memakai loop `for` untuk menjalankan
sebagian kode pada setiap itemnya. Di balik layar, ini secara implisit
membuat lalu mengonsumsi sebuah *iterator*, tetapi kita melewatkan bagaimana
persisnya itu bekerja sampai sekarang.

Pada contoh di Listing 13-11, kita memisahkan pembuatan *iterator* dari
pemakaian *iterator* di dalam loop `for`. Ketika loop `for`
dipanggil memakai *iterator* di `v1_iter`, setiap elemen di dalam *iterator*
dipakai dalam satu iterasi loop, yang mencetak setiap nilainya.

<Listing number="13-11" file-name="src/main.rs" caption="Memakai iterator di dalam loop `for`">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```

</Listing>

Di bahasa-bahasa yang tidak memiliki *iterator* dari standard librarynya, Anda
kemungkinan akan menulis fungsionalitas yang sama ini dengan memulai sebuah
variable pada indeks 0, memakai variable itu untuk mengindeks ke dalam vector
untuk mendapat sebuah nilai, dan menaikkan nilai variable itu di dalam
loop sampai mencapai jumlah total item di dalam vector.

*Iterator* menangani semua logika itu untuk Anda, mengurangi kode berulang
yang berpotensi Anda kacaukan. *Iterator* memberi Anda lebih banyak
fleksibilitas untuk memakai logika yang sama dengan berbagai jenis urutan,
bukan hanya struktur data yang dapat Anda indeks, seperti vector. Mari kita
telaah bagaimana *iterator* melakukannya.

<a id="the-iterator-trait-and-the-next-method"></a>
### Trait `Iterator` dan Method `next`

Semua *iterator* mengimplementasikan sebuah *trait* bernama `Iterator` yang
didefinisikan di standard library. Definisi *trait* itu tampak seperti ini:

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```

Perhatikan bahwa definisi ini memakai beberapa sintaks baru: `type Item` dan
`Self::Item`, yang mendefinisikan sebuah *associated type* (tipe asosiasi)
pada *trait* ini. Kita akan membahas *associated type* secara mendalam di Bab
20. Untuk saat ini, yang perlu Anda ketahui hanyalah bahwa kode ini menyatakan
bahwa mengimplementasikan *trait* `Iterator` mengharuskan Anda juga
mendefinisikan type `Item`, dan type `Item` ini dipakai di return type
method `next`. Dengan kata lain, type `Item` akan menjadi type yang
dikembalikan dari *iterator*.

*Trait* `Iterator` hanya mengharuskan pengimplementasinya mendefinisikan satu
method: method `next`, yang mengembalikan satu item dari *iterator* setiap
kali dipanggil, terbungkus di dalam `Some`, dan, ketika iterasi selesai,
mengembalikan `None`.

Kita dapat memanggil method `next` pada *iterator* secara langsung; Listing
13-12 mendemonstrasikan nilai-nilai apa yang dikembalikan dari pemanggilan
`next` berulang kali pada *iterator* yang dibuat dari vector.

<Listing number="13-12" file-name="src/lib.rs" caption="Memanggil method `next` pada iterator">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```

</Listing>

Perhatikan bahwa kita perlu membuat `v1_iter` *mutable*: Memanggil method
`next` pada sebuah *iterator* mengubah internal state yang dipakai
*iterator* untuk melacak posisinya di dalam urutan. Dengan kata lain, kode ini
_mengonsumsi_, atau menghabiskan, *iterator* itu. Setiap pemanggilan `next`
memakan satu item dari *iterator*. Kita tidak perlu membuat `v1_iter`
*mutable* ketika memakai loop `for`, karena loop itu mengambil
*ownership* atas `v1_iter` dan membuatnya *mutable* di belakang layar.

Perhatikan juga bahwa nilai-nilai yang kita dapat dari pemanggilan `next`
adalah *reference* *immutable* ke nilai-nilai di dalam vector. Method `iter`
menghasilkan sebuah *iterator* atas *reference*-reference *immutable*. Jika kita
ingin membuat *iterator* yang mengambil *ownership* atas `v1` dan
mengembalikan nilai-nilai yang dimiliki, kita dapat memanggil `into_iter`
alih-alih `iter`. Demikian pula, jika kita ingin melakukan iterasi atas
*reference*-reference *mutable*, kita dapat memanggil `iter_mut` alih-alih
`iter`.

### Method yang Mengonsumsi Iterator

*Trait* `Iterator` memiliki sejumlah method yang berbeda dengan implementasi
bawaan yang disediakan oleh standard library; Anda dapat mengetahui
method-method ini dengan melihat dokumentasi API standard library untuk *trait*
`Iterator`. Sebagian dari method ini memanggil method `next` di dalam
definisinya, itulah sebabnya Anda diharuskan mengimplementasikan method `next`
ketika mengimplementasikan *trait* `Iterator`.

Method-method yang memanggil `next` disebut _consuming adapter_ (adapter yang
mengonsumsi) karena memanggilnya menghabiskan *iterator*. Salah satu contohnya
adalah method `sum`, yang mengambil *ownership* atas *iterator* dan melakukan
iterasi pada item-itemnya dengan memanggil `next` berulang kali, sehingga
mengonsumsi *iterator* itu. Selagi melakukan iterasi, method ini menambahkan
setiap item ke total berjalan dan mengembalikan totalnya ketika iterasi
selesai. Listing 13-13 memiliki sebuah test yang mengilustrasikan
pemakaian method `sum`.

<Listing number="13-13" file-name="src/lib.rs" caption="Memanggil method `sum` untuk mendapat total semua item di dalam iterator">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```

</Listing>

Kita tidak diizinkan memakai `v1_iter` setelah pemanggilan `sum`, karena `sum`
mengambil *ownership* atas *iterator* tempat kita memanggilnya.

### Method yang Menghasilkan Iterator Lain

_Iterator adapter_ adalah method-method yang didefinisikan pada *trait*
`Iterator` yang tidak mengonsumsi *iterator*. Sebaliknya, mereka menghasilkan
*iterator* yang berbeda dengan mengubah sebagian aspek dari *iterator*
aslinya.

Listing 13-14 menunjukkan contoh pemanggilan method adapter *iterator* `map`,
yang menerima sebuah *closure* untuk dipanggil pada setiap item selagi
item-item itu diiterasi. Method `map` mengembalikan sebuah *iterator* baru
yang menghasilkan item-item yang telah dimodifikasi. *Closure* di sini membuat
sebuah *iterator* baru yang di dalamnya setiap item dari vector akan
dinaikkan sebesar 1.

<Listing number="13-14" file-name="src/main.rs" caption="Memanggil adapter iterator `map` untuk membuat iterator baru">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```

</Listing>

Namun, kode ini menghasilkan sebuah peringatan:

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```

Kode di Listing 13-14 tidak melakukan apa pun; *closure* yang kita tentukan
tidak pernah dipanggil. Peringatan itu mengingatkan kita alasannya: *Iterator*
adapter bersifat lazy, dan kita perlu mengonsumsi *iterator*-nya di sini.

Untuk memperbaiki peringatan ini dan mengonsumsi *iterator*-nya, kita akan
memakai method `collect`, yang kita pakai bersama `env::args` di Listing 12-1.
Method ini mengonsumsi *iterator* dan mengumpulkan nilai-nilai hasilnya ke
dalam data type collection.

Di Listing 13-15, kita mengumpulkan hasil iterasi atas *iterator* yang
dikembalikan dari pemanggilan `map` ke dalam sebuah vector. Vector ini pada
akhirnya akan memuat setiap item dari vector aslinya, dinaikkan sebesar 1.

<Listing number="13-15" file-name="src/main.rs" caption="Memanggil method `map` untuk membuat iterator baru, lalu memanggil method `collect` untuk mengonsumsi iterator baru itu dan membuat sebuah vector">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```

</Listing>

Karena `map` menerima sebuah *closure*, kita dapat menentukan operasi apa pun
yang ingin kita lakukan pada setiap item. Ini adalah contoh yang bagus
tentang bagaimana *closure* memungkinkan Anda menyesuaikan sebagian perilaku
sambil memakai ulang perilaku iterasi yang disediakan *trait* `Iterator`.

Anda dapat merantaikan banyak pemanggilan *iterator adapter* untuk melakukan
tindakan yang rumit dengan cara yang mudah dibaca. Tetapi karena semua
*iterator* bersifat lazy, Anda harus memanggil salah satu method consuming
adapter untuk mendapat hasil dari pemanggilan-pemanggilan *iterator adapter*.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-closures-that-capture-their-environment"></a>

### Closure yang Menangkap Lingkungannya

Banyak *iterator adapter* menerima *closure* sebagai argumen, dan umumnya *closure*
yang kita tentukan sebagai argumen untuk *iterator adapter* adalah *closure* yang
menangkap lingkungannya.

Untuk contoh ini, kita akan memakai method `filter` yang menerima sebuah
*closure*. *Closure* itu mendapat sebuah item dari *iterator* dan mengembalikan
sebuah `bool`. Jika *closure* mengembalikan `true`, nilainya akan disertakan di
dalam *iterator* yang dihasilkan oleh `filter`. Jika *closure* mengembalikan
`false`, nilainya tidak akan disertakan.

Di Listing 13-16, kita memakai `filter` dengan sebuah *closure* yang menangkap
variable `shoe_size` dari lingkungannya untuk melakukan iterasi atas collection
instance *struct* `Shoe`. *Closure* itu hanya akan mengembalikan sepatu-sepatu
yang ukurannya sesuai.

<Listing number="13-16" file-name="src/lib.rs" caption="Memakai method `filter` dengan closure yang menangkap `shoe_size`">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```

</Listing>

Fungsi `shoes_in_size` menerima *ownership* atas sebuah vector berisi sepatu
dan sebuah ukuran sepatu sebagai parameter. Fungsi itu mengembalikan sebuah
vector yang hanya memuat sepatu dengan ukuran yang ditentukan.

Di badan `shoes_in_size`, kita memanggil `into_iter` untuk membuat sebuah
*iterator* yang mengambil *ownership* atas vector itu. Lalu, kita memanggil
`filter` untuk mengadaptasi *iterator* itu menjadi *iterator* baru yang hanya
memuat elemen-elemen yang membuat *closure* mengembalikan `true`.

*Closure* itu menangkap parameter `shoe_size` dari lingkungan dan membandingkan
nilainya dengan ukuran setiap sepatu, hanya menyimpan sepatu dengan ukuran
yang ditentukan. Akhirnya, pemanggilan `collect` mengumpulkan nilai-nilai yang
dikembalikan oleh *iterator* yang diadaptasi itu ke dalam sebuah vector yang
dikembalikan oleh fungsi tersebut.

Test itu menunjukkan bahwa ketika kita memanggil `shoes_in_size`, kita
hanya mendapat kembali sepatu-sepatu yang ukurannya sama dengan nilai yang
kita tentukan.
