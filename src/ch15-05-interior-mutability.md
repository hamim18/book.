## `RefCell<T>` dan Pola Interior Mutability

_Interior mutability_ (mutabilitas internal) adalah pola desain di Rust yang
memungkinkan Anda mengubah data meskipun ada *immutable* *reference* ke data itu;
biasanya, tindakan ini dilarang oleh aturan *borrowing*. Untuk mengubah data,
pola ini memakai kode `unsafe` di dalam struktur data untuk melenturkan aturan
Rust yang biasa mengatur perubahan dan peminjaman. Kode *unsafe* memberi tahu
kompilator bahwa kitalah yang memeriksa aturannya secara manual alih-alih
mengandalkan kompilator untuk memeriksanya bagi kita; kita akan membahas kode
*unsafe* lebih jauh di Bab 20.

Kita dapat memakai tipe yang menggunakan pola *interior mutability* hanya ketika
kita dapat memastikan bahwa aturan *borrowing* akan diikuti pada runtime,
meskipun kompilator tidak bisa menjaminnya. Kode `unsafe` yang terlibat
kemudian dibungkus dalam API yang aman, dan tipe luarnya tetap *immutable*.

Mari kita jelajahi konsep ini dengan melihat tipe `RefCell<T>` yang mengikuti
pola *interior mutability*.

<!-- Old headings. Do not remove or links may break. -->

<a id="enforcing-borrowing-rules-at-runtime-with-refcellt"></a>

### Menegakkan Aturan Borrowing pada Runtime

Tidak seperti `Rc<T>`, tipe `RefCell<T>` merepresentasikan *ownership* tunggal
atas data yang ditampungnya. Jadi, apa yang membuat `RefCell<T>` berbeda dari
tipe seperti `Box<T>`? Ingat kembali aturan *borrowing* yang Anda pelajari di
Bab 4:

- Pada waktu kapan pun, Anda dapat memiliki _salah satu_: satu *mutable*
  *reference* atau sejumlah *immutable* *reference* (tetapi tidak keduanya).
- *Reference* harus selalu valid.

Dengan *reference* dan `Box<T>`, invarian aturan *borrowing* ditegakkan pada waktu
kompilasi. Dengan `RefCell<T>`, invarian ini ditegakkan _pada runtime_. Dengan
*reference*, jika Anda melanggar aturan ini, Anda akan mendapat galat kompilator.
Dengan `RefCell<T>`, jika Anda melanggar aturan ini, program Anda akan panic
dan keluar.

Keuntungan memeriksa aturan *borrowing* pada waktu kompilasi adalah galat akan
tertangkap lebih awal dalam proses pengembangan, dan tidak ada dampak pada
performa runtime karena seluruh analisis diselesaikan sebelumnya. Karena
alasan-alasan itu, memeriksa aturan *borrowing* pada waktu kompilasi adalah
pilihan terbaik pada sebagian besar kasus, itulah sebabnya ini menjadi
default Rust.

Keuntungan memeriksa aturan *borrowing* pada runtime adalah beberapa skenario
yang aman terhadap memori menjadi diizinkan, padahal skenario itu akan ditolak
oleh pemeriksaan waktu kompilasi. Analisis statis, seperti kompilator Rust,
pada dasarnya bersifat konservatif. Beberapa sifat kode tidak mungkin
dideteksi dengan menganalisis kodenya: Contoh paling terkenal adalah Masalah
Halting, yang berada di luar cakupan buku ini tetapi merupakan topik yang
menarik untuk diteliti.

Karena sebagian analisis tidak mungkin dilakukan, jika kompilator Rust tidak
bisa memastikan kode mematuhi aturan *ownership*, ia mungkin menolak program
yang sebenarnya benar; dalam hal ini, ia bersifat konservatif. Jika Rust
menerima program yang salah, pengguna tidak akan bisa memercayai jaminan yang
dibuat Rust. Namun, jika Rust menolak program yang benar, pemrogram akan
kerepotan, tetapi tidak ada hal fatal yang dapat terjadi. Tipe `RefCell<T>`
berguna ketika Anda yakin kode Anda mengikuti aturan *borrowing* tetapi
kompilator tidak mampu memahami dan menjamin hal itu.

Serupa dengan `Rc<T>`, `RefCell<T>` hanya untuk dipakai dalam skenario
single-threaded dan akan memberi Anda galat waktu kompilasi jika Anda mencoba
memakainya dalam konteks multithreaded. Kita akan membahas cara mendapatkan
fungsionalitas `RefCell<T>` di program multithreaded di Bab 16.

Berikut rekap alasan memilih `Box<T>`, `Rc<T>`, atau `RefCell<T>`:

- `Rc<T>` memungkinkan beberapa pemilik atas data yang sama; `Box<T>` dan
  `RefCell<T>` memiliki pemilik tunggal.
- `Box<T>` mengizinkan pinjaman *immutable* atau *mutable* yang diperiksa pada
  waktu kompilasi; `Rc<T>` hanya mengizinkan pinjaman *immutable* yang diperiksa
  pada waktu kompilasi; `RefCell<T>` mengizinkan pinjaman *immutable* atau
  *mutable* yang diperiksa pada runtime.
- Karena `RefCell<T>` mengizinkan pinjaman *mutable* yang diperiksa pada
  runtime, Anda dapat mengubah nilai di dalam `RefCell<T>` bahkan ketika
  `RefCell<T>` itu *immutable*.

Mengubah nilai di dalam nilai yang *immutable* adalah pola *interior mutability*.
Mari kita lihat situasi ketika *interior mutability* berguna dan periksa
bagaimana hal itu mungkin.

<!-- Old headings. Do not remove or links may break. -->

<a id="interior-mutability-a-mutable-borrow-to-an-immutable-value"></a>

### Memakai Interior Mutability

Salah satu konsekuensi aturan *borrowing* adalah ketika Anda memiliki nilai
*immutable*, Anda tidak bisa meminjamnya secara *mutable*. Sebagai contoh, kode
ini tidak akan terkompilasi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/src/main.rs}}
```

Jika Anda mencoba mengompilasi kode ini, Anda akan mendapat galat berikut:

```console
{{#include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/output.txt}}
```

Namun, ada situasi ketika akan berguna bagi sebuah nilai untuk mengubah
dirinya sendiri di dalam metodenya tetapi tampak *immutable* bagi kode lain.
Kode di luar metode nilai itu tidak akan bisa mengubah nilai itu. Memakai
`RefCell<T>` adalah salah satu cara untuk memperoleh kemampuan memiliki
*interior mutability*, tetapi `RefCell<T>` tidak sepenuhnya menghindari aturan
*borrowing*: *Borrow checker* di kompilator mengizinkan *interior mutability* ini,
dan aturan *borrowing* diperiksa pada runtime sebagai gantinya. Jika Anda
melanggar aturannya, Anda akan mendapat `panic!` alih-alih galat kompilator.

Mari kita kerjakan contoh praktis ketika kita dapat memakai `RefCell<T>`
untuk mengubah nilai *immutable* dan melihat mengapa hal itu berguna.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-use-case-for-interior-mutability-mock-objects"></a>

#### Menguji dengan Mock Object

Terkadang selama pengujian seorang pemrogram memakai suatu tipe sebagai
pengganti tipe lain, untuk mengamati perilaku tertentu dan menegaskan bahwa
perilaku itu diimplementasikan dengan benar. Tipe pengganti ini disebut
_test double_ (pengganti dalam pengujian). Bayangkan ini seperti pemeran
pengganti dalam pembuatan film, ketika seseorang maju menggantikan seorang
aktor untuk melakukan adegan yang sangat rumit. *Test double* menggantikan tipe
lain ketika kita menjalankan test. _Mock object_ (objek tiruan) adalah jenis
*test double* khusus yang mencatat apa yang terjadi selama test sehingga Anda
dapat menegaskan bahwa tindakan yang benar telah terjadi.

Rust tidak memiliki objek dalam pengertian yang sama seperti objek di
bahasa-bahasa lain, dan Rust tidak memiliki fungsionalitas *mock object* yang
tertanam di pustaka standar seperti yang dimiliki beberapa bahasa lain. Namun,
Anda pasti bisa membuat *struct* yang akan menjalankan tujuan yang sama dengan
*mock object*.

Berikut skenario yang akan kita uji: Kita akan membuat sebuah library yang
melacak sebuah nilai terhadap nilai maksimum dan mengirim pesan berdasarkan
seberapa dekat nilai saat ini dengan nilai maksimum itu. Library ini, misalnya,
bisa dipakai untuk melacak kuota pengguna atas jumlah panggilan API yang
diizinkan untuk mereka buat.

Library kita hanya akan menyediakan fungsionalitas melacak seberapa dekat
sebuah nilai dengan maksimumnya dan pesan apa yang seharusnya muncul pada
waktu apa. Aplikasi yang memakai library kita diharapkan menyediakan mekanisme
pengiriman pesannya: Aplikasi bisa menampilkan pesan itu langsung kepada
pengguna, mengirim email, mengirim pesan teks, atau melakukan hal lain.
Library tidak perlu tahu detail itu. Yang dibutuhkannya hanyalah sesuatu yang
mengimplementasikan *trait* yang akan kita sediakan, bernama `Messenger`.
Listing 15-20 menunjukkan kode library itu.

<Listing number="15-20" file-name="src/lib.rs" caption="Library untuk melacak seberapa dekat sebuah nilai dengan nilai maksimum dan memperingatkan ketika nilai itu berada pada tingkat tertentu">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-20/src/lib.rs}}
```

</Listing>

Satu bagian penting dari kode ini adalah bahwa *trait* `Messenger` memiliki satu
metode bernama `send` yang menerima *immutable* *reference* ke `self` dan teks
pesannya. *Trait* ini adalah antarmuka yang perlu diimplementasikan *mock object*
kita supaya mock itu dapat dipakai dengan cara yang sama seperti objek asli.
Bagian penting lainnya adalah bahwa kita ingin menguji perilaku metode
`set_value` pada `LimitTracker`. Kita dapat mengubah apa yang kita berikan
untuk parameter `value`, tetapi `set_value` tidak mengembalikan apa pun untuk
kita buat asersi. Kita ingin bisa menyatakan bahwa jika kita membuat
`LimitTracker` dengan sesuatu yang mengimplementasikan *trait* `Messenger` dan
nilai tertentu untuk `max`, messenger itu diperintahkan untuk mengirim pesan
yang sesuai ketika kita memberikan angka yang berbeda untuk `value`.

Kita membutuhkan *mock object* yang, alih-alih mengirim email atau pesan teks
ketika kita memanggil `send`, hanya akan melacak pesan yang diperintahkan
untuk dikirim. Kita dapat membuat instance baru dari *mock object*, membuat
`LimitTracker` yang memakai *mock object* itu, memanggil metode `set_value` pada
`LimitTracker`, lalu memeriksa bahwa *mock object* itu memiliki pesan yang kita
harapkan. Listing 15-21 menunjukkan upaya mengimplementasikan *mock object*
untuk melakukan hal itu, tetapi *borrow checker* tidak mengizinkannya.

<Listing number="15-21" file-name="src/lib.rs" caption="Upaya mengimplementasikan `MockMessenger` yang tidak diizinkan oleh borrow checker">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-21/src/lib.rs:here}}
```

</Listing>

Kode test ini mendefinisikan *struct* `MockMessenger` yang memiliki *field*
`sent_messages` berisi `Vec` nilai `String` untuk melacak pesan yang
diperintahkan untuk dikirim. Kita juga mendefinisikan *associated function*
`new` untuk memudahkan pembuatan nilai `MockMessenger` baru yang dimulai
dengan daftar pesan kosong. Kita kemudian mengimplementasikan *trait*
`Messenger` untuk `MockMessenger` supaya kita dapat memberikan
`MockMessenger` kepada `LimitTracker`. Dalam definisi metode `send`, kita
mengambil pesan yang diberikan sebagai parameter dan menyimpannya di daftar
`sent_messages` milik `MockMessenger`.

Dalam test itu, kita menguji apa yang terjadi ketika `LimitTracker`
diperintahkan untuk menetapkan `value` menjadi sesuatu yang lebih dari 75
persen nilai `max`. Pertama, kita membuat `MockMessenger` baru, yang akan
dimulai dengan daftar pesan kosong. Kemudian, kita membuat `LimitTracker` baru
dan memberinya *reference* ke `MockMessenger` baru itu dan nilai `max` sebesar
`100`. Kita memanggil metode `set_value` pada `LimitTracker` dengan nilai
`80`, yang lebih dari 75 persen dari 100. Lalu, kita menegaskan bahwa daftar
pesan yang dilacak `MockMessenger` sekarang seharusnya memuat satu pesan.

Namun, ada satu masalah dengan test ini, seperti ditunjukkan di sini:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-21/output.txt}}
```

Kita tidak bisa memodifikasi `MockMessenger` untuk melacak pesan-pesan itu,
karena metode `send` menerima *immutable* *reference* ke `self`. Kita juga tidak
bisa mengambil saran dari teks galat itu untuk memakai `&mut self` di metode
`impl` sekaligus definisi *trait*. Kita tidak ingin mengubah *trait* `Messenger`
semata-mata demi pengujian. Sebagai gantinya, kita perlu mencari cara membuat
kode test kita bekerja dengan benar dengan desain yang sudah ada.

Ini adalah situasi ketika *interior mutability* dapat membantu! Kita akan
menyimpan `sent_messages` di dalam `RefCell<T>`, dan kemudian metode `send`
akan bisa memodifikasi `sent_messages` untuk menyimpan pesan yang telah kita
lihat. Listing 15-22 menunjukkan seperti apa tampilannya.

<Listing number="15-22" file-name="src/lib.rs" caption="Memakai `RefCell<T>` untuk mengubah nilai bagian dalam sementara nilai luarnya dianggap immutable">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-22/src/lib.rs:here}}
```

</Listing>

*Field* `sent_messages` sekarang bertipe `RefCell<Vec<String>>` alih-alih
`Vec<String>`. Di fungsi `new`, kita membuat instance `RefCell<Vec<String>>`
baru di sekeliling vektor kosong itu.

Untuk implementasi metode `send`, parameter pertamanya tetap pinjaman
*immutable* atas `self`, yang cocok dengan definisi *trait*. Kita memanggil
`borrow_mut` pada `RefCell<Vec<String>>` di `self.sent_messages` untuk
mendapatkan *mutable* *reference* ke nilai di dalam `RefCell<Vec<String>>`, yaitu
vektor itu. Kemudian, kita dapat memanggil `push` pada *mutable* *reference* ke
vektor itu untuk melacak pesan yang dikirim selama test.

Perubahan terakhir yang harus kita buat ada di asersi: Untuk melihat berapa
banyak item di dalam vektor bagian dalam, kita memanggil `borrow` pada
`RefCell<Vec<String>>` untuk mendapatkan *immutable* *reference* ke vektor itu.

Sekarang setelah Anda melihat cara memakai `RefCell<T>`, mari kita selami cara
kerjanya!

<!-- Old headings. Do not remove or links may break. -->

<a id="keeping-track-of-borrows-at-runtime-with-refcellt"></a>

#### Melacak Borrows pada Runtime

Ketika membuat *immutable* dan *mutable* *reference*, kita memakai sintaks `&` dan
`&mut`. Dengan `RefCell<T>`, kita memakai metode `borrow` dan `borrow_mut`,
yang merupakan bagian dari API aman milik `RefCell<T>`. Metode `borrow`
mengembalikan tipe *smart pointer* `Ref<T>`, dan `borrow_mut` mengembalikan
tipe *smart pointer* `RefMut<T>`. Kedua tipe mengimplementasikan `Deref`, jadi
kita dapat memperlakukannya seperti *reference* biasa.

`RefCell<T>` melacak berapa banyak *smart pointer* `Ref<T>` dan `RefMut<T>`
yang sedang aktif. Setiap kali kita memanggil `borrow`, `RefCell<T>` menambah
jumlah pinjaman *immutable* yang aktif. Ketika sebuah nilai `Ref<T>` keluar dari
*scope*, jumlah pinjaman *immutable* turun 1. Sama seperti aturan *borrowing* waktu
kompilasi, `RefCell<T>` mengizinkan kita memiliki banyak pinjaman *immutable*
atau satu pinjaman *mutable* pada titik waktu mana pun.

Jika kita mencoba melanggar aturan ini, alih-alih mendapat galat kompilator
seperti yang terjadi dengan *reference*, implementasi `RefCell<T>` akan panic
pada runtime. Listing 15-23 menunjukkan modifikasi implementasi `send` di
Listing 15-22. Kita sengaja mencoba membuat dua pinjaman *mutable* yang aktif
untuk *scope* yang sama untuk menggambarkan bahwa `RefCell<T>` mencegah kita
melakukan ini pada runtime.

<Listing number="15-23" file-name="src/lib.rs" caption="Membuat dua mutable reference di scope yang sama untuk melihat bahwa `RefCell<T>` akan panic">

```rust,ignore,panics
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-23/src/lib.rs:here}}
```

</Listing>

Kita membuat variabel `one_borrow` untuk *smart pointer* `RefMut<T>` yang
dikembalikan dari `borrow_mut`. Kemudian, kita membuat pinjaman *mutable* lain
dengan cara yang sama di variabel `two_borrow`. Ini membuat dua *mutable*
*reference* di *scope* yang sama, yang tidak diizinkan. Ketika kita menjalankan
test untuk library kita, kode di Listing 15-23 akan terkompilasi tanpa galat,
tetapi testnya akan gagal:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-23/output.txt}}
```

Perhatikan bahwa kode itu panic dengan pesan `already borrowed:
BorrowMutError`. Beginilah `RefCell<T>` menangani pelanggaran aturan
*borrowing* pada runtime.

Memilih untuk menangkap galat *borrowing* pada runtime alih-alih pada waktu
kompilasi, seperti yang kita lakukan di sini, berarti Anda berpotensi
menemukan kesalahan dalam kode Anda lebih lambat dalam proses pengembangan:
bisa jadi baru ketahuan ketika kode Anda sudah di-deploy ke produksi. Selain
itu, kode Anda akan menanggung denda performa runtime yang kecil sebagai
akibat melacak peminjaman pada runtime alih-alih pada waktu kompilasi. Namun,
memakai `RefCell<T>` memungkinkan penulisan *mock object* yang dapat memodifikasi
dirinya sendiri untuk melacak pesan yang telah dilihatnya selagi Anda
memakainya dalam konteks yang hanya mengizinkan nilai *immutable*. Anda dapat
memakai `RefCell<T>` terlepas dari komprominya untuk mendapatkan lebih banyak
fungsionalitas daripada yang disediakan *reference* biasa.

<!-- Old headings. Do not remove or links may break. -->

<a id="having-multiple-owners-of-mutable-data-by-combining-rc-t-and-ref-cell-t"></a>
<a id="allowing-multiple-owners-of-mutable-data-with-rct-and-refcellt"></a>

### Mengizinkan Beberapa Pemilik Data Mutable

Cara umum memakai `RefCell<T>` adalah dengan mengombinasikannya dengan
`Rc<T>`. Ingat bahwa `Rc<T>` memungkinkan Anda memiliki beberapa pemilik atas
sejumlah data, tetapi ia hanya memberi akses *immutable* ke data itu. Jika Anda
memiliki `Rc<T>` yang menampung `RefCell<T>`, Anda bisa mendapat nilai yang
dapat memiliki beberapa pemilik _dan_ yang dapat Anda ubah!

Sebagai contoh, ingat kembali contoh *cons list* di Listing 15-18 ketika kita
memakai `Rc<T>` untuk mengizinkan beberapa list berbagi *ownership* atas list
lain. Karena `Rc<T>` hanya menampung nilai *immutable*, kita tidak bisa mengubah
nilai apa pun di dalam list itu setelah kita membuatnya. Mari kita tambahkan
`RefCell<T>` untuk kemampuannya mengubah nilai di dalam list. Listing 15-24
menunjukkan bahwa dengan memakai `RefCell<T>` di definisi `Cons`, kita dapat
memodifikasi nilai yang tersimpan di semua list.

<Listing number="15-24" file-name="src/main.rs" caption="Memakai `Rc<RefCell<i32>>` untuk membuat `List` yang dapat kita ubah">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-24/src/main.rs}}
```

</Listing>

Kita membuat nilai yang merupakan instance `Rc<RefCell<i32>>` dan
menyimpannya di variabel bernama `value` supaya kita dapat mengaksesnya
langsung nanti. Kemudian, kita membuat `List` di `a` dengan variant `Cons`
yang menampung `value`. Kita perlu mengklon `value` supaya `a` dan `value`
sama-sama memiliki nilai `5` bagian dalam, alih-alih memindahkan *ownership*
dari `value` ke `a` atau membuat `a` meminjam dari `value`.

Kita membungkus list `a` di dalam `Rc<T>` supaya ketika kita membuat list `b`
dan `c`, keduanya dapat merujuk `a`, yang persis kita lakukan di Listing
15-18.

Setelah membuat list di `a`, `b`, dan `c`, kita ingin menambahkan 10 ke nilai
di dalam `value`. Kita melakukan ini dengan memanggil `borrow_mut` pada
`value`, yang memakai fitur dereferensi otomatis yang kita bahas di [“Di Mana
Operator `->`?”][wheres-the---operator]<!-- ignore --> di Bab 5 untuk
melakukan dereferensi `Rc<T>` ke nilai `RefCell<T>` bagian dalam. Metode
`borrow_mut` mengembalikan *smart pointer* `RefMut<T>`, dan kita memakai
operator dereferensi padanya dan mengubah nilai bagian dalam.

Ketika kita mencetak `a`, `b`, dan `c`, kita dapat melihat bahwa semuanya
memiliki nilai yang telah dimodifikasi, `15`, alih-alih `5`:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-24/output.txt}}
```

Teknik ini cukup rapi! Dengan memakai `RefCell<T>`, kita memiliki nilai `List`
yang tampak dari luar *immutable*. Tetapi kita dapat memakai metode-metode pada
`RefCell<T>` yang menyediakan akses ke *interior mutability*-nya sehingga kita
dapat memodifikasi data kita ketika kita perlu. Pemeriksaan aturan *borrowing*
pada runtime melindungi kita dari data race, dan terkadang layak menukar
sedikit kecepatan demi fleksibilitas ini pada struktur data kita. Perhatikan
bahwa `RefCell<T>` tidak bekerja untuk kode multithreaded! `Mutex<T>` adalah
versi thread-safe dari `RefCell<T>`, dan kita akan membahas `Mutex<T>` di
Bab 16.

[wheres-the---operator]: ch05-03-method-syntax.html#wheres-the---operator
