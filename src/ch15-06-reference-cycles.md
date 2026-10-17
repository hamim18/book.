## Reference Cycle Dapat Membocorkan Memori

Jaminan keamanan memori Rust membuat penciptaan memori yang tidak pernah
dibersihkan secara tidak sengaja (dikenal sebagai _memory leak_ atau kebocoran
memori) menjadi sulit, tetapi bukan mustahil. Mencegah kebocoran memori
sepenuhnya bukanlah salah satu jaminan Rust, artinya kebocoran memori tidak
melanggar keamanan memori di Rust. Kita bisa melihat bahwa Rust mengizinkan kebocoran
memori dengan memakai `Rc<T>` dan `RefCell<T>`: Ada kemungkinan membuat
*reference* di mana item-item saling merujuk dalam sebuah siklus. Ini
menciptakan kebocoran memori karena jumlah referensi setiap item dalam siklus
itu tidak akan pernah mencapai 0, dan nilainya tidak akan pernah dibebaskan.

### Membuat Reference Cycle

Mari kita lihat bagaimana *reference cycle* bisa terjadi dan bagaimana
mencegahnya, dimulai dengan definisi *enum* `List` dan metode `tail` di Listing
15-25.

<Listing number="15-25" file-name="src/main.rs" caption="Definisi cons list yang menampung `RefCell<T>` supaya kita dapat memodifikasi apa yang dirujuk variant `Cons`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-25/src/main.rs:here}}
```

</Listing>

Kita memakai variasi lain dari definisi `List` di Listing 15-5. Elemen kedua
di variant `Cons` sekarang adalah `RefCell<Rc<List>>`, artinya alih-alih
memiliki kemampuan memodifikasi nilai `i32` seperti yang kita lakukan di
Listing 15-24, kita ingin memodifikasi nilai `List` yang ditunjuk variant
`Cons`. Kita juga menambahkan metode `tail` untuk memudahkan kita mengakses
item kedua jika kita memiliki variant `Cons`.

Di Listing 15-26, kita menambahkan fungsi `main` yang memakai definisi di
Listing 15-25. Kode ini membuat list di `a` dan list di `b` yang menunjuk ke
list di `a`. Kemudian, kode itu memodifikasi list di `a` untuk menunjuk ke
`b`, menciptakan *reference cycle*. Ada statement `println!` di sepanjang
jalan untuk menunjukkan jumlah referensi pada berbagai titik dalam proses ini.

<Listing number="15-26" file-name="src/main.rs" caption="Membuat reference cycle dari dua nilai `List` yang saling menunjuk">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-26/src/main.rs:here}}
```

</Listing>

Kita membuat instance `Rc<List>` yang menampung nilai `List` di variable `a`
dengan list awal `5, Nil`. Kita kemudian membuat instance `Rc<List>` yang
menampung nilai `List` lain di variable `b` yang memuat nilai `10` dan
menunjuk ke list di `a`.

Kita memodifikasi `a` supaya menunjuk ke `b` alih-alih `Nil`, menciptakan
sebuah siklus. Kita melakukannya dengan memakai metode `tail` untuk
mendapatkan *reference* ke `RefCell<Rc<List>>` di `a`, yang kita letakkan di
variable `link`. Kemudian, kita memakai metode `borrow_mut` pada
`RefCell<Rc<List>>` untuk mengubah nilai di dalamnya dari `Rc<List>` yang
menampung nilai `Nil` menjadi `Rc<List>` di `b`.

Ketika kita menjalankan kode ini, dengan `println!` terakhir tetap
dikomentari untuk sementara, kita akan mendapat output ini:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-26/output.txt}}
```

Jumlah referensi instance `Rc<List>` di `a` dan `b` adalah 2 setelah kita
mengubah list di `a` untuk menunjuk ke `b`. Di akhir `main`, Rust membebaskan
variable `b`, yang mengurangi jumlah referensi instance `Rc<List>` `b` dari 2
menjadi 1. Memori yang dimiliki `Rc<List>` di *heap* tidak akan dibebaskan pada
titik ini karena jumlah referensinya 1, bukan 0. Kemudian, Rust membebaskan
`a`, yang juga mengurangi jumlah referensi instance `Rc<List>` `a` dari 2
menjadi 1. Memori instance ini juga tidak bisa dibebaskan, karena instance
`Rc<List>` yang lain masih merujuk padanya. Memori yang dialokasikan untuk
list itu tidak akan pernah diklaim kembali. Untuk memvisualisasikan
*reference cycle* ini, kita telah membuat diagram pada Gambar 15-4.

<img alt="Persegi panjang berlabel 'a' yang menunjuk ke persegi panjang yang memuat integer 5. Persegi panjang berlabel 'b' yang menunjuk ke persegi panjang yang memuat integer 10. Persegi panjang yang memuat 5 menunjuk ke persegi panjang yang memuat 10, dan persegi panjang yang memuat 10 menunjuk balik ke persegi panjang yang memuat 5, menciptakan sebuah siklus." src="img/trpl15-04.svg" class="center" />

<span class="caption">Gambar 15-4: *Reference cycle* dari list `a` dan `b`
yang saling menunjuk</span>

Jika Anda membuka tanda komentar pada `println!` terakhir dan menjalankan
programnya, Rust akan mencoba mencetak siklus ini dengan `a` menunjuk ke `b`
menunjuk ke `a` dan seterusnya sampai terjadi luapan *stack*.

Dibandingkan dengan program di dunia nyata, konsekuensi menciptakan *reference*
cycle dalam contoh ini tidak terlalu parah: Tepat setelah kita membuat
*reference cycle* itu, programnya berakhir. Namun, jika program yang lebih
kompleks mengalokasikan banyak memori dalam sebuah siklus dan menahannya dalam
waktu lama, program itu akan memakai lebih banyak memori daripada yang
dibutuhkannya dan bisa membebani sistem, menyebabkannya kehabisan memori yang
tersedia.

Membuat *reference cycle* tidak mudah dilakukan, tetapi juga bukan mustahil.
Jika Anda memiliki nilai `RefCell<T>` yang memuat nilai `Rc<T>` atau kombinasi
bersarang serupa dari type dengan *interior mutability* dan penghitungan
referensi, Anda harus memastikan Anda tidak menciptakan siklus; Anda tidak
bisa mengandalkan Rust untuk menangkapnya. Membuat *reference cycle* akan
menjadi bug logika dalam program Anda yang harus Anda minimalisasi dengan
pengujian terotomatisasi, code review, dan praktik pengembangan perangkat
lunak lainnya.

Solusi lain untuk menghindari *reference cycle* adalah menata ulang struktur
data Anda sehingga sebagian *reference* menyatakan *ownership* dan sebagian tidak.
Akibatnya, Anda dapat memiliki siklus yang tersusun dari sebagian hubungan
*ownership* dan sebagian hubungan non-ownership, dan hanya hubungan *ownership*
yang memengaruhi apakah sebuah nilai dapat dibebaskan atau tidak. Di Listing
15-25, kita selalu ingin variant `Cons` memiliki listnya, jadi menata ulang
struktur datanya tidak mungkin. Mari kita lihat contoh yang memakai graf yang
tersusun dari *node* parent dan *node* child untuk melihat kapan hubungan
non-ownership merupakan cara yang tepat untuk mencegah *reference cycle*.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-reference-cycles-turning-an-rct-into-a-weakt"></a>

### Mencegah Reference Cycle Menggunakan `Weak<T>`

Sejauh ini, kita telah menunjukkan bahwa memanggil `Rc::clone` menambah
`strong_count` sebuah instance `Rc<T>`, dan instance `Rc<T>` hanya dibersihkan
jika `strong_count`-nya 0. Anda juga dapat membuat *weak reference* ke nilai di
dalam instance `Rc<T>` dengan memanggil `Rc::downgrade` dan memberikan
*reference* ke `Rc<T>` itu. _Strong reference_ (*reference* kuat) adalah cara
Anda berbagi *ownership* atas instance `Rc<T>`. _Weak reference_ (*reference*
lemah) tidak menyatakan hubungan *ownership*, dan jumlahnya tidak memengaruhi
kapan instance `Rc<T>` dibersihkan. *Weak reference* tidak akan menyebabkan
*reference cycle*, karena siklus apa pun yang melibatkan beberapa *weak reference*
akan putus begitu jumlah *strong reference* dari nilai-nilai yang terlibat
mencapai 0.

Ketika Anda memanggil `Rc::downgrade`, Anda mendapat *smart pointer* typed
`Weak<T>`. Alih-alih menambah `strong_count` di instance `Rc<T>` sebesar 1,
memanggil `Rc::downgrade` menambah `weak_count` sebesar 1. Type `Rc<T>`
memakai `weak_count` untuk melacak berapa banyak *reference* `Weak<T>` yang
ada, serupa dengan `strong_count`. Bedanya adalah `weak_count` tidak perlu
menjadi 0 agar instance `Rc<T>` dibersihkan.

Karena nilai yang dirujuk `Weak<T>` mungkin telah dibebaskan, untuk melakukan
apa pun dengan nilai yang ditunjuk `Weak<T>` Anda harus memastikan nilai itu
masih ada. Lakukan ini dengan memanggil metode `upgrade` pada instance
`Weak<T>`, yang akan mengembalikan `Option<Rc<T>>`. Anda akan mendapat hasil
`Some` jika nilai `Rc<T>` belum dibebaskan dan hasil `None` jika nilai
`Rc<T>` telah dibebaskan. Karena `upgrade` mengembalikan `Option<Rc<T>>`,
Rust akan memastikan kasus `Some` dan kasus `None` ditangani, dan tidak akan
ada *pointer* yang tidak valid.

Sebagai contoh, alih-alih memakai list yang item-itemnya hanya tahu tentang
item berikutnya, kita akan membuat *tree* (pohon) yang item-itemnya tahu
tentang item-item child _dan_ item parent mereka.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-tree-data-structure-a-node-with-child-nodes"></a>

#### Membuat Struktur Data Tree

Untuk memulai, kita akan membangun *tree* dengan *node*-node yang tahu tentang
*node* child mereka. Kita akan membuat *struct* bernama `Node` yang menampung
nilai `i32`-nya sendiri serta *reference* ke nilai `Node` child-nya:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:here}}
```

Kita ingin sebuah `Node` memiliki child-childnya, dan kita ingin berbagi
*ownership* itu dengan variable supaya kita dapat mengakses setiap `Node` di
*tree* secara langsung. Untuk melakukan ini, kita mendefinisikan item-item
`Vec<T>` sebagai nilai typed `Rc<Node>`. Kita juga ingin memodifikasi *node*
mana yang menjadi child dari *node* lain, jadi kita memiliki `RefCell<T>` di
`children` di sekeliling `Vec<Rc<Node>>`.

Selanjutnya, kita akan memakai definisi *struct* kita dan membuat satu instance
`Node` bernama `leaf` dengan nilai `3` dan tanpa child, serta instance lain
bernama `branch` dengan nilai `5` dan `leaf` sebagai salah satu child-nya,
seperti ditunjukkan pada Listing 15-27.

<Listing number="15-27" file-name="src/main.rs" caption="Membuat node `leaf` tanpa child dan node `branch` dengan `leaf` sebagai salah satu child-nya">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:there}}
```

</Listing>

Kita mengklon `Rc<Node>` di `leaf` dan menyimpannya di `branch`, artinya
`Node` di `leaf` sekarang memiliki dua pemilik: `leaf` dan `branch`. Kita
dapat bergerak dari `branch` ke `leaf` melalui `branch.children`, tetapi
tidak ada cara bergerak dari `leaf` ke `branch`. Alasannya adalah `leaf`
tidak memiliki *reference* ke `branch` dan tidak tahu bahwa keduanya saling
berhubungan. Kita ingin `leaf` tahu bahwa `branch` adalah parent-nya. Kita
akan melakukannya berikutnya.

#### Menambahkan Reference dari Child ke Parent-nya

Untuk membuat *node* child sadar akan parent-nya, kita perlu menambahkan *field*
`parent` ke definisi *struct* `Node` kita. Kesulitannya adalah memutuskan type
`parent` seharusnya apa. Kita tahu ia tidak bisa memuat `Rc<T>`, karena itu
akan menciptakan *reference cycle* dengan `leaf.parent` menunjuk ke `branch`
dan `branch.children` menunjuk ke `leaf`, yang akan menyebabkan nilai
`strong_count` mereka tidak pernah menjadi 0.

Memikirkan hubungan ini dari sisi lain, sebuah *node* parent harus memiliki
child-childnya: Jika *node* parent dibebaskan, *node* child-nya juga harus
dibebaskan. Namun, sebuah child tidak boleh memiliki parent-nya: Jika kita
membebaskan *node* child, parent-nya harus tetap ada. Ini adalah kasus untuk
*weak reference*!

Jadi, alih-alih `Rc<T>`, kita akan membuat type `parent` memakai `Weak<T>`,
khususnya `RefCell<Weak<Node>>`. Sekarang definisi *struct* `Node` kita tampak
seperti ini:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:here}}
```

Sebuah *node* akan dapat merujuk *node* parent-nya tetapi tidak memiliki
parent-nya. Di Listing 15-28, kita memperbarui `main` untuk memakai definisi
baru ini supaya *node* `leaf` memiliki cara untuk merujuk parent-nya, `branch`.

<Listing number="15-28" file-name="src/main.rs" caption="Node `leaf` dengan weak reference ke node parent-nya, `branch`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:there}}
```

</Listing>

Membuat *node* `leaf` tampak serupa dengan Listing 15-27 kecuali *field*
`parent`: `leaf` awalnya tidak memiliki parent, jadi kita membuat instance
*reference* `Weak<Node>` baru yang kosong.

Pada titik ini, ketika kita mencoba mendapatkan *reference* ke parent `leaf`
dengan memakai metode `upgrade`, kita mendapat nilai `None`. Kita melihat ini
di output dari statement `println!` pertama:

```text
leaf parent = None
```

Ketika kita membuat *node* `branch`, ia juga akan memiliki *reference*
`Weak<Node>` baru di *field* `parent` karena `branch` tidak memiliki *node*
parent. Kita tetap memiliki `leaf` sebagai salah satu child dari `branch`.
Begitu kita memiliki instance `Node` di `branch`, kita dapat memodifikasi
`leaf` untuk memberinya *reference* `Weak<Node>` ke parent-nya. Kita memakai
metode `borrow_mut` pada `RefCell<Weak<Node>>` di *field* `parent` milik
`leaf`, lalu kita memakai fungsi `Rc::downgrade` untuk membuat *reference*
`Weak<Node>` ke `branch` dari `Rc<Node>` di `branch`.

Ketika kita mencetak parent `leaf` lagi, kali ini kita akan mendapat variant
`Some` yang menampung `branch`: Sekarang `leaf` dapat mengakses parent-nya!
Ketika kita mencetak `leaf`, kita juga menghindari siklus yang akhirnya
berujung pada *stack* overflow seperti yang kita alami di Listing 15-26;
*reference* `Weak<Node>` dicetak sebagai `(Weak)`:

```text
leaf parent = Some(Node { value: 5, parent: RefCell { value: (Weak) },
children: RefCell { value: [Node { value: 3, parent: RefCell { value: (Weak) },
children: RefCell { value: [] } }] } })
```

Tidak adanya output tak terhingga menunjukkan bahwa kode ini tidak
menciptakan *reference cycle*. Kita juga dapat mengetahuinya dengan melihat
nilai yang kita dapat dari memanggil `Rc::strong_count` dan `Rc::weak_count`.

#### Memvisualisasikan Perubahan `strong_count` dan `weak_count`

Mari kita lihat bagaimana nilai `strong_count` dan `weak_count` dari instance
`Rc<Node>` berubah dengan membuat *scope* dalam baru dan memindahkan pembuatan
`branch` ke *scope* itu. Dengan melakukannya, kita dapat melihat apa yang
terjadi ketika `branch` dibuat lalu dibebaskan ketika ia keluar dari *scope*.
Modifikasinya ditunjukkan pada Listing 15-29.

<Listing number="15-29" file-name="src/main.rs" caption="Membuat `branch` di scope dalam dan memeriksa jumlah strong reference dan weak reference">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-29/src/main.rs:here}}
```

</Listing>

Setelah `leaf` dibuat, `Rc<Node>`-nya memiliki strong count 1 dan weak count
0. Di *scope* dalam, kita membuat `branch` dan mengasosiasikannya dengan `leaf`;
pada titik itu, ketika kita mencetak jumlahnya, `Rc<Node>` di `branch` akan
memiliki strong count 1 dan weak count 1 (untuk `leaf.parent` yang menunjuk
ke `branch` dengan `Weak<Node>`). Ketika kita mencetak jumlah di `leaf`, kita
akan melihat ia memiliki strong count 2 karena `branch` sekarang memiliki
klon `Rc<Node>` dari `leaf` yang tersimpan di `branch.children`, tetapi tetap
memiliki weak count 0.

Ketika *scope* dalam berakhir, `branch` keluar dari *scope* dan strong count dari
`Rc<Node>` berkurang menjadi 0, jadi `Node`-nya dibebaskan. Weak count 1 dari
`leaf.parent` tidak berpengaruh pada dibebaskan atau tidaknya `Node`, jadi
kita tidak mendapat kebocoran memori apa pun!

Jika kita mencoba mengakses parent `leaf` setelah akhir *scope* itu, kita akan
mendapat `None` lagi. Di akhir program, `Rc<Node>` di `leaf` memiliki strong
count 1 dan weak count 0 karena variable `leaf` kini menjadi satu-satunya
*reference* ke `Rc<Node>` itu lagi.

Semua logika yang mengelola jumlah dan pembebasan nilai sudah tertanam di
`Rc<T>` dan `Weak<T>` beserta implementasi *trait* `Drop` mereka. Dengan
menyatakan bahwa hubungan dari child ke parent-nya harus berupa *reference*
`Weak<T>` dalam definisi `Node`, Anda dapat membuat *node* parent menunjuk ke
*node* child dan sebaliknya tanpa menciptakan *reference cycle* dan kebocoran
memori.

## Ringkasan

Bab ini membahas cara memakai *smart pointer* untuk membuat jaminan dan
kompromi yang berbeda dari yang dibuat Rust secara default dengan *reference*
biasa. Type `Box<T>` memiliki ukuran yang diketahui dan menunjuk ke data yang
dialokasikan di *heap*. Type `Rc<T>` melacak jumlah referensi ke data di *heap*
sehingga data itu dapat memiliki beberapa pemilik. Type `RefCell<T>` dengan
*interior mutability*-nya memberi kita type yang dapat kita pakai ketika kita
membutuhkan type *immutable* tetapi perlu mengubah nilai bagian dalam type itu;
ia juga menegakkan aturan *borrowing* pada runtime alih-alih pada waktu
kompilasi.

Juga dibahas *trait* `Deref` dan `Drop`, yang mengaktifkan banyak fungsionalitas
*smart pointer*. Kita mengeksplorasi *reference cycle* yang dapat menyebabkan
kebocoran memori dan cara mencegahnya menggunakan `Weak<T>`.

Jika bab ini telah menggugah minat Anda dan Anda ingin mengimplementasikan
*smart pointer* Anda sendiri, lihat [“The Rustonomicon”][nomicon] untuk
informasi yang lebih berguna.

Selanjutnya, kita akan membicarakan konkurensi di Rust. Anda bahkan akan
belajar tentang beberapa *smart pointer* baru.

[nomicon]: ../nomicon/index.html
