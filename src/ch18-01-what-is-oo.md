## Karakteristik Bahasa Berorientasi Objek

Tidak ada konsensus di komunitas pemrograman tentang fitur apa yang harus
dimiliki sebuah bahasa agar dianggap berorientasi objek. Rust dipengaruhi oleh
banyak paradigma pemrograman, termasuk OOP; contohnya, kita mengeksplorasi
fitur-fitur yang berasal dari pemrograman fungsional di Bab 13. Bisa
dikatakan, bahasa-bahasa OOP memiliki karakteristik umum tertentu—yakni,
objek, enkapsulasi, dan *inheritance*. Mari kita lihat apa arti setiap
karakteristik itu dan apakah Rust mendukungnya.

### Objek Memuat Data dan Perilaku

Buku _Design Patterns: Elements of Reusable Object-Oriented Software_ karya
Erich Gamma, Richard Helm, Ralph Johnson, dan John Vlissides
(Addison-Wesley, 1994), yang dalam bahasa sehari-hari disebut sebagai buku
_The Gang of Four_ (Geng Empat), adalah katalog pola desain berorientasi
objek. Buku itu mendefinisikan OOP sebagai berikut:

> Program berorientasi objek tersusun dari objek. Sebuah **objek** memaketkan
> data dan prosedur yang mengoperasikan data tersebut. Prosedur itu biasanya
> disebut **metode** atau **operasi**.

Menggunakan definisi ini, Rust berorientasi objek: *struct* dan *enum* memiliki
data, dan blok `impl` menyediakan metode pada *struct* dan *enum*. Meskipun *struct*
dan *enum* yang bermetode tidak _disebut_ objek, keduanya menyediakan
fungsionalitas yang sama, menurut definisi objek dari Gang of Four.

<a id="encapsulation-that-hides-implementation-details"></a>
### Enkapsulasi yang Menyembunyikan Detail Implementasi

Aspek lain yang umumnya dikaitkan dengan OOP adalah gagasan tentang
_enkapsulasi_, yang berarti detail implementasi sebuah objek tidak dapat
diakses oleh kode yang memakai objek itu. Karena itu, satu-satunya cara untuk
berinteraksi dengan sebuah objek adalah melalui API publiknya; kode yang
memakai objek itu seharusnya tidak bisa menjangkau bagian dalam objek dan
mengubah data atau perilaku secara langsung. Ini memungkinkan pemrogram
mengubah dan me-refactor bagian dalam sebuah objek tanpa perlu mengubah kode
yang memakai objek itu.

Kita membahas cara mengendalikan enkapsulasi di Bab 7: kita bisa memakai kata
kunci `pub` untuk menentukan *module*, type, fungsi, dan metode mana di kode
kita yang harus bersifat publik, dan secara bawaan semua yang lain bersifat
privat. Contohnya, kita bisa mendefinisikan *struct* `AveragedCollection` yang
memiliki *field* berisi vektor nilai `i32`. *Struct* itu juga bisa memiliki *field*
yang berisi rata-rata dari nilai-nilai di vektor itu, artinya rata-rata tidak
harus dihitung setiap kali seseorang membutuhkannya. Dengan kata lain,
`AveragedCollection` akan menyimpan rata-rata hasil perhitungannya di cache
untuk kita. Listing 18-1 memuat definisi *struct* `AveragedCollection`.

<Listing number="18-1" file-name="src/lib.rs" caption="Struct `AveragedCollection` yang memelihara daftar integer dan rata-rata item-item di dalam koleksinya">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-01/src/lib.rs}}
```

</Listing>

*Struct* itu ditandai `pub` supaya kode lain bisa memakainya, tetapi
*field*-field di dalam *struct* tetap privat. Ini penting dalam kasus ini karena
kita ingin memastikan bahwa setiap kali sebuah nilai ditambahkan atau dihapus
dari daftar, rata-ratanya juga diperbarui. Kita melakukannya dengan
mengimplementasikan metode `add`, `remove`, dan `average` pada *struct* itu,
seperti yang ditunjukkan di Listing 18-2.

<Listing number="18-2" file-name="src/lib.rs" caption="Implementasi metode publik `add`, `remove`, dan `average` pada `AveragedCollection`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-02/src/lib.rs:here}}
```

</Listing>

Metode publik `add`, `remove`, dan `average` adalah satu-satunya cara untuk
mengakses atau mengubah data di instance `AveragedCollection`. Ketika sebuah
item ditambahkan ke `list` menggunakan metode `add` atau dihapus menggunakan
metode `remove`, implementasi masing-masing memanggil metode privat
`update_average` yang menangani pembaruan *field* `average` juga.

Kita membiarkan *field* `list` dan `average` privat supaya tidak ada cara bagi
kode eksternal untuk menambah atau menghapus item langsung ke atau dari *field*
`list`; jika tidak, *field* `average` bisa menjadi tidak sinkron ketika `list`
berubah. Metode `average` mengembalikan nilai di *field* `average`, sehingga
kode eksternal bisa membaca `average` tetapi tidak mengubahnya.

Karena kita telah mengenkapsulasi detail implementasi *struct*
`AveragedCollection`, kita bisa dengan mudah mengubah aspek-aspeknya, seperti
struktur datanya, di masa depan. Misalnya, kita bisa memakai `HashSet<i32>`
alih-alih `Vec<i32>` untuk *field* `list`. Selama tanda tangan metode publik
`add`, `remove`, dan `average` tetap sama, kode yang memakai
`AveragedCollection` tidak perlu berubah. Jika kita membuat `list` publik,
belum tentu demikian halnya: `HashSet<i32>` dan `Vec<i32>` memiliki metode
yang berbeda untuk menambah dan menghapus item, jadi kode eksternal kemungkinan
besar harus berubah jika ia mengubah `list` secara langsung.

Jika enkapsulasi adalah aspek yang diperlukan agar sebuah bahasa dianggap
berorientasi objek, maka Rust memenuhi persyaratan itu. Pilihan untuk memakai
`pub` atau tidak pada berbagai bagian kode memungkinkan enkapsulasi detail
implementasi.

### Inheritance sebagai Sistem Type dan sebagai Berbagi Kode

_Inheritance_ (pewarisan) adalah mekanisme yang dengannya sebuah objek bisa
mewarisi elemen dari definisi objek lain, sehingga memperoleh data dan
perilaku objek induknya tanpa Anda harus mendefinisikannya lagi.

Jika sebuah bahasa harus memiliki *inheritance* untuk dianggap berorientasi
objek, maka Rust bukan bahasa seperti itu. Tidak ada cara untuk
mendefinisikan *struct* yang mewarisi *field* dan implementasi metode *struct*
induknya tanpa memakai *macro*.

Akan tetapi, jika Anda terbiasa memiliki *inheritance* di perangkat pemrograman
Anda, Anda bisa memakai solusi lain di Rust, bergantung pada alasan Anda
mengambil *inheritance* sejak awal.

Anda akan memilih *inheritance* karena dua alasan utama. Salah satunya adalah
pemakaian ulang kode: Anda bisa mengimplementasikan perilaku tertentu untuk
satu type, dan *inheritance* memungkinkan Anda memakai ulang implementasi itu
untuk type yang berbeda. Anda bisa melakukan ini secara terbatas di kode Rust
menggunakan implementasi bawaan metode *trait*, yang Anda lihat di Listing 10-14
ketika kita menambahkan implementasi bawaan metode `summarize` pada *trait*
`Summary`. Type apa pun yang mengimplementasikan *trait* `Summary` akan memiliki
metode `summarize` tersedia padanya tanpa kode lebih lanjut. Ini mirip dengan
kelas induk yang memiliki implementasi sebuah metode dan kelas anak yang
mewarisinya juga memiliki implementasi metode itu. Kita juga bisa menimpa
implementasi bawaan metode `summarize` ketika kita mengimplementasikan *trait*
`Summary`, yang mirip dengan kelas anak yang menimpa implementasi metode yang
diwarisi dari kelas induk.

Alasan lain untuk memakai *inheritance* berkaitan dengan type system: untuk
memungkinkan type anak dipakai di tempat yang sama dengan type induknya. Ini
juga disebut _polymorphism_ (polimorfisme), yang berarti Anda bisa saling
menggantikan beberapa objek pada saat runtime jika mereka memiliki
karakteristik tertentu yang sama.

> ### Polimorfisme
>
> Bagi banyak orang, polimorfisme identik dengan *inheritance*. Tetapi
> sebenarnya ini konsep yang lebih umum yang merujuk pada kode yang bisa
> bekerja dengan data dari berbagai type. Untuk *inheritance*, type-type itu
> umumnya adalah subclass.
>
> Rust justru memakai *generics* untuk mengabstraksi berbagai type yang mungkin
> dan *trait bound* untuk menerapkan batasan pada apa yang harus disediakan
> type-type itu. Ini terkadang disebut _bounded parametric polymorphism_
> (polimorfisme parametrik terbatas).

Rust telah memilih sekumpulan kompromi yang berbeda dengan tidak menawarkan
*inheritance*. *Inheritance* sering kali berisiko berbagi lebih banyak kode
daripada yang diperlukan. Subclass tidak selalu harus berbagi semua
karakteristik kelas induknya, tetapi dengan *inheritance* mereka akan
melakukannya. Ini bisa membuat desain program kurang fleksibel. Ini juga
memunculkan kemungkinan memanggil metode pada subclass yang tidak masuk akal
atau menyebabkan error karena metode itu tidak berlaku untuk subclass
tersebut. Selain itu, beberapa bahasa hanya mengizinkan _single inheritance_
(pewarisan tunggal) (artinya subclass hanya bisa mewarisi dari satu kelas),
yang semakin membatasi fleksibilitas desain program.

Karena alasan-alasan ini, Rust mengambil pendekatan yang berbeda dengan
memakai *trait object* alih-alih *inheritance* untuk mencapai polimorfisme pada
saat runtime. Mari kita lihat cara kerja *trait object*.
