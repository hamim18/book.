## Mengimplementasikan Pattern Desain Berorientasi Objek

_State pattern_ (state pattern) adalah pattern desain berorientasi objek. Inti dari
pattern ini adalah kita mendefinisikan sekumpulan state yang bisa dimiliki sebuah
nilai secara internal. State-state itu direpresentasikan oleh sekumpulan
_state object_ (objek state), dan perilaku nilai itu berubah berdasarkan
state-nya. Kita akan menelusuri contoh *struct* post blog yang memiliki *field*
untuk menampung state-nya, yang akan berupa *state object* dari kumpulan
“draf”, “review”, atau “diterbitkan”.

*State object* berbagi fungsionalitas: di Rust, tentu saja, kita memakai *struct*
dan *trait* alih-alih objek dan *inheritance*. Setiap *state object* bertanggung
jawab atas perilakunya sendiri dan untuk mengatur kapan ia harus berubah
menjadi state lain. Nilai yang menampung *state object* tidak tahu apa-apa
tentang perilaku yang berbeda dari state-state itu atau kapan harus
bertransisi di antara state-state.

Keuntungan memakai state pattern adalah bahwa ketika persyaratan bisnis program
berubah, kita tidak perlu mengubah kode nilai yang menampung state atau kode
yang memakai nilai itu. Kita hanya perlu memperbarui kode di dalam salah satu
*state object* untuk mengubah aturannya atau mungkin menambahkan lebih banyak
*state object*.

Pertama, kita akan mengimplementasikan state pattern dengan cara yang lebih
tradisional dan berorientasi objek. Kemudian, kita akan memakai pendekatan
yang sedikit lebih alami di Rust. Mari kita mulai dengan mengimplementasikan
alur kerja post blog secara bertahap menggunakan state pattern.

Fungsionalitas akhirnya akan terlihat seperti ini:

1. Sebuah post blog dimulai sebagai draf kosong.
1. Ketika drafnya selesai, review terhadap post itu diminta.
1. Ketika post itu disetujui, post itu diterbitkan.
1. Hanya post blog yang diterbitkan yang mengembalikan konten untuk dicetak
   supaya post yang belum disetujui tidak bisa diterbitkan secara tidak
   sengaja.

Perubahan lain apa pun yang dicoba pada sebuah post seharusnya tidak
berpengaruh. Contohnya, jika kita mencoba menyetujui post blog draf sebelum
kita meminta review, post itu harus tetap menjadi draf yang belum
diterbitkan.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-traditional-object-oriented-attempt"></a>

### Mencoba Gaya Berorientasi Objek Tradisional

Ada banyak cara tak terbatas untuk menstrukturkan kode guna memecahkan masalah
yang sama, masing-masing dengan kompromi yang berbeda. Implementasi bagian
ini lebih bergaya berorientasi objek tradisional, yang mungkin untuk ditulis
di Rust, tetapi tidak memanfaatkan sebagian kekuatan Rust. Nanti, kita akan
mendemonstrasikan solusi berbeda yang tetap memakai pattern desain berorientasi
objek tetapi terstruktur dengan cara yang mungkin terlihat kurang familier
bagi pemrogram berpengalaman berorientasi objek. Kita akan membandingkan
kedua solusi itu untuk merasakan kompromi merancang kode Rust secara berbeda
dari kode di bahasa lain.

Listing 18-11 menunjukkan alur kerja ini dalam bentuk kode: ini adalah contoh
pemakaian API yang akan kita implementasikan di *crate* library bernama `blog`.
Ini belum bisa terkompilasi karena kita belum mengimplementasikan *crate*
`blog`.

<Listing number="18-11" file-name="src/main.rs" caption="Kode yang mendemonstrasikan perilaku yang kita inginkan dari crate `blog` kita">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

Kita ingin memungkinkan pengguna membuat post blog draf baru dengan
`Post::new`. Kita ingin memungkinkan teks ditambahkan ke post blog itu. Jika
kita mencoba mendapatkan konten post itu segera, sebelum disetujui, kita
seharusnya tidak mendapat teks apa pun karena post itu masih draf. Kami telah
menambahkan `assert_eq!` di kode untuk tujuan demonstrasi. Pengujian unit
yang bagus untuk ini adalah menegaskan bahwa post blog draf mengembalikan
string kosong dari method `content`, tetapi kita tidak akan menulis pengujian
untuk contoh ini.

Berikutnya, kita ingin mengaktifkan permintaan review terhadap post itu, dan
kita ingin `content` mengembalikan string kosong selagi menunggu review.
Ketika post itu menerima persetujuan, post itu seharusnya diterbitkan,
artinya teks post itu akan dikembalikan saat `content` dipanggil.

Perhatikan bahwa satu-satunya type dari *crate* itu yang
kita gunakan adalah type `Post`. Type ini akan memakai state pattern dan akan menampung
nilai yang berupa salah satu dari tiga *state object* yang merepresentasikan
berbagai state yang bisa dialami sebuah post—draf, review, atau diterbitkan.
Perubahan dari satu state ke state lain akan dikelola secara internal di dalam
type `Post`. State-state itu berubah sebagai respons terhadap method yang
dipanggil pengguna library kita pada instance `Post`, tetapi mereka tidak
harus mengelola perubahan state secara langsung. Selain itu, pengguna tidak
bisa membuat kesalahan dengan state-state itu, seperti menerbitkan post
sebelum post itu di-review.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-post-and-creating-a-new-instance-in-the-draft-state"></a>

#### Mendefinisikan `Post` dan Membuat Instance Baru

Mari kita mulai implementasi library-nya! Kita tahu kita butuh *struct* `Post`
publik yang menampung sejumlah konten, jadi kita akan mulai dengan definisi
*struct* itu dan fungsi asosiasi publik `new` untuk membuat instance `Post`,
seperti yang ditunjukkan di Listing 18-12. Kita juga akan membuat *trait*
`State` privat yang akan mendefinisikan perilaku yang harus dimiliki semua
*state object* untuk sebuah `Post`.

Kemudian, `Post` akan menampung *trait object* `Box<dyn State>` di dalam
`Option<T>` pada *field* privat bernama `state` untuk menampung *state object*
itu. Sebentar lagi Anda akan melihat mengapa `Option<T>` itu diperlukan.

<Listing number="18-12" file-name="src/lib.rs" caption="Definisi struct `Post` dan fungsi `new` yang membuat instance `Post` baru, trait `State`, dan struct `Draft`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

*Trait* `State` mendefinisikan perilaku yang dibagikan oleh berbagai state
post. *State object*-nya adalah `Draft`, `PendingReview`, dan `Published`, dan
semuanya akan mengimplementasikan *trait* `State`. Untuk saat ini, *trait* itu
belum memiliki method, dan kita akan mulai dengan mendefinisikan state
`Draft` saja karena itulah state tempat sebuah post dimulai.

Ketika kita membuat `Post` baru, kita menetapkan *field* `state`-nya ke nilai
`Some` yang menampung `Box`. `Box` ini menunjuk ke instance baru *struct*
`Draft`. Ini memastikan bahwa setiap kali kita membuat instance baru `Post`,
instance itu akan dimulai sebagai draf. Karena *field* `state` dari `Post`
privat, tidak ada cara untuk membuat `Post` dalam state lain! Di fungsi
`Post::new`, kita menetapkan *field* `content` ke `String` baru yang kosong.

#### Menyimpan Teks Konten Post

Kita melihat di Listing 18-11 bahwa kita ingin bisa memanggil method bernama
`add_text` dan memberinya `&str` yang kemudian ditambahkan sebagai konten
teks post blog. Kita mengimplementasikan ini sebagai method, alih-alih
mengekspos *field* `content` sebagai `pub`, supaya nanti kita bisa
mengimplementasikan method yang akan mengontrol cara data *field* `content`
dibaca. Method `add_text` cukup sederhana, jadi mari kita tambahkan
implementasi di Listing 18-13 ke blok `impl Post`.

<Listing number="18-13" file-name="src/lib.rs" caption="Mengimplementasikan method `add_text` untuk menambahkan teks ke `content` post">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

Method `add_text` menerima *reference* *mutable* ke `self` karena kita mengubah
instance `Post` yang kita panggil `add_text`-nya. Kita kemudian memanggil
`push_str` pada `String` di `content` dan meneruskan argumen `text` untuk
ditambahkan ke `content` yang tersimpan. Perilaku ini tidak bergantung pada
state post itu, jadi ini bukan bagian dari state pattern. Method `add_text`
tidak berinteraksi dengan *field* `state` sama sekali, tetapi ia bagian dari
perilaku yang ingin kita dukung.

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-the-content-of-a-draft-post-is-empty"></a>

#### Memastikan Konten Post Draf Kosong

Bahkan setelah kita memanggil `add_text` dan menambahkan sejumlah konten ke
post kita, kita tetap ingin method `content` mengembalikan string *slice*
kosong karena post itu masih dalam state draf, seperti yang ditunjukkan
`assert_eq!` pertama di Listing 18-11. Untuk saat ini, mari kita
implementasikan method `content` dengan hal paling sederhana yang akan
memenuhi persyaratan ini: selalu mengembalikan string *slice* kosong. Kita
akan mengubahnya nanti setelah kita mengimplementasikan kemampuan mengubah
state post supaya post itu bisa diterbitkan. Sejauh ini, post hanya bisa
berada di state draf, jadi konten post harus selalu kosong. Listing 18-14
menunjukkan implementasi placeholder ini.

<Listing number="18-14" file-name="src/lib.rs" caption="Menambahkan implementasi placeholder untuk method `content` pada `Post` yang selalu mengembalikan string slice kosong">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

Dengan method `content` yang ditambahkan ini, semua yang ada di Listing 18-11
sampai `assert_eq!` pertama bekerja sebagaimana dimaksudkan.

<!-- Old headings. Do not remove or links may break. -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>
<a id="requesting-a-review-changes-the-posts-state"></a>

#### Meminta Review, yang Mengubah State Post

Berikutnya, kita perlu menambahkan fungsionalitas untuk meminta review
terhadap sebuah post, yang seharusnya mengubah state-nya dari `Draft` menjadi
`PendingReview`. Listing 18-15 menunjukkan kode ini.

<Listing number="18-15" file-name="src/lib.rs" caption="Mengimplementasikan method `request_review` pada `Post` dan trait `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

Kita memberi `Post` method publik bernama `request_review` yang menerima
*reference* *mutable* ke `self`. Kemudian, kita memanggil method internal
`request_review` pada state `Post` saat ini, dan method `request_review`
kedua ini mengonsumsi state saat ini dan mengembalikan state baru.

Kita menambahkan method `request_review` ke *trait* `State`; semua type yang
mengimplementasikan *trait* itu sekarang harus mengimplementasikan method
`request_review`. Perhatikan bahwa alih-alih memiliki `self`, `&self`, atau
`&mut self` sebagai parameter pertama method itu, kita memiliki
`self: Box<Self>`. Sintaks ini berarti method itu hanya valid ketika
dipanggil pada `Box` yang menampung type itu. Sintaks ini mengambil
*ownership* `Box<Self>`, meniadakan state lama sehingga nilai state dari
`Post` bisa berubah menjadi state baru.

Untuk mengonsumsi state lama, method `request_review` perlu mengambil
*ownership* nilai state itu. Di sinilah `Option` pada *field* `state` dari
`Post` berperan: kita memanggil method `take` untuk mengambil nilai `Some`
dari *field* `state` dan meninggalkan `None` di tempatnya karena Rust tidak
mengizinkan kita memiliki *field* yang tidak terisi di dalam *struct*. Ini
memungkinkan kita memindahkan nilai `state` keluar dari `Post` alih-alih
meminjamnya. Kemudian, kita akan menetapkan nilai `state` post itu ke hasil
operasi ini.

Kita perlu menetapkan `state` ke `None` sementara alih-alih menetapkannya
langsung dengan kode seperti `self.state = self.state.request_review();`
untuk mendapatkan *ownership* nilai `state`. Ini memastikan `Post` tidak bisa
memakai nilai `state` lama setelah kita mengubahnya menjadi state baru.

Method `request_review` pada `Draft` mengembalikan instance baru yang
ter-box dari *struct* `PendingReview` baru, yang merepresentasikan state ketika
sebuah post menunggu review. *Struct* `PendingReview` juga mengimplementasikan
method `request_review` tetapi tidak melakukan transformasi apa pun.
Sebaliknya, ia mengembalikan dirinya sendiri karena ketika kita meminta
review pada post yang sudah berada di state `PendingReview`, post itu harus
tetap berada di state `PendingReview`.

Sekarang kita mulai melihat keuntungan state pattern: method `request_review`
pada `Post` tetap sama apa pun nilai `state`-nya. Setiap state bertanggung
jawab atas aturannya sendiri.

Kita akan membiarkan method `content` pada `Post` apa adanya, mengembalikan
string *slice* kosong. Sekarang kita bisa memiliki `Post` di state
`PendingReview` maupun di state `Draft`, tetapi kita menginginkan perilaku
yang sama di state `PendingReview`. Listing 18-11 sekarang bekerja sampai
pemanggilan `assert_eq!` kedua!

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>
<a id="adding-approve-to-change-the-behavior-of-content"></a>

#### Menambahkan `approve` untuk Mengubah Perilaku `content`

Method `approve` akan serupa dengan method `request_review`: method itu akan
menetapkan `state` ke nilai yang menurut state saat ini seharusnya dimiliki
ketika state itu disetujui, seperti yang ditunjukkan di Listing 18-16.

<Listing number="18-16" file-name="src/lib.rs" caption="Mengimplementasikan method `approve` pada `Post` dan trait `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

Kita menambahkan method `approve` ke *trait* `State` dan menambahkan *struct*
baru yang mengimplementasikan `State`, yaitu state `Published`.

Serupa dengan cara kerja `request_review` pada `PendingReview`, jika kita
memanggil method `approve` pada `Draft`, itu tidak akan berpengaruh karena
`approve` akan mengembalikan `self`. Ketika kita memanggil `approve` pada
`PendingReview`, method itu mengembalikan instance baru yang ter-box dari
*struct* `Published`. *Struct* `Published` mengimplementasikan *trait* `State`, dan
untuk method `request_review` maupun method `approve`, ia mengembalikan
dirinya sendiri karena post harus tetap berada di state `Published` dalam
kasus-kasus itu.

Sekarang kita perlu memperbarui method `content` pada `Post`. Kita ingin
nilai yang dikembalikan `content` bergantung pada state `Post` saat ini, jadi
kita akan membuat `Post` mendelegasikan ke method `content` yang
didefinisikan pada `state`-nya, seperti yang ditunjukkan di Listing 18-17.

<Listing number="18-17" file-name="src/lib.rs" caption="Memperbarui method `content` pada `Post` untuk mendelegasikan ke method `content` pada `State`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

Karena tujuannya adalah menjaga semua aturan ini di dalam *struct* yang
mengimplementasikan `State`, kita memanggil method `content` pada nilai di
`state` dan meneruskan instance post (yaitu, `self`) sebagai argumen.
Kemudian, kita mengembalikan nilai yang dikembalikan dari pemakaian method
`content` pada nilai `state` itu.

Kita memanggil method `as_ref` pada `Option` karena kita menginginkan
*reference* ke nilai di dalam `Option` alih-alih *ownership* nilainya. Karena
`state` adalah `Option<Box<dyn State>>`, ketika kita memanggil `as_ref`,
sebuah `Option<&Box<dyn State>>` dikembalikan. Jika kita tidak memanggil
`as_ref`, kita akan mendapat error karena kita tidak bisa memindahkan `state`
keluar dari `&self` yang dipinjam dari parameter fungsi.

Kita kemudian memanggil method `unwrap`, yang kita tahu tidak akan pernah
panic karena kita tahu method-method pada `Post` memastikan `state` akan
selalu memuat nilai `Some` ketika method-method itu selesai. Ini salah satu
kasus yang kita bicarakan di bagian [“Ketika Anda Memiliki Lebih Banyak
Informasi daripada *Compiler*”][more-info-than-rustc]<!-- ignore --> di Bab 9,
ketika kita tahu nilai `None` tidak mungkin terjadi, meskipun *compiler*
tidak bisa memahaminya.

Pada titik ini, ketika kita memanggil `content` pada `&Box<dyn State>`, deref
coercion akan berlaku pada `&` dan `Box` sehingga method `content` pada
akhirnya dipanggil pada type yang mengimplementasikan *trait* `State`. Artinya,
kita perlu menambahkan `content` ke definisi *trait* `State`, dan di situlah
kita akan menaruh logika konten apa yang dikembalikan bergantung pada state
mana yang kita miliki, seperti yang ditunjukkan di Listing 18-18.

<Listing number="18-18" file-name="src/lib.rs" caption="Menambahkan method `content` ke trait `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

Kita menambahkan implementasi bawaan untuk method `content` yang
mengembalikan string *slice* kosong. Artinya, kita tidak perlu
mengimplementasikan `content` pada *struct* `Draft` dan `PendingReview`. *Struct*
`Published` akan menimpa method `content` dan mengembalikan nilai di
`post.content`. Meskipun nyaman, membuat method `content` pada `State`
menentukan konten `Post` mengaburkan batas antara tanggung jawab `State` dan
tanggung jawab `Post`.

Perhatikan bahwa kita butuh anotasi *lifetime* pada method ini, seperti yang
kita bahas di Bab 10. Kita menerima *reference* ke `post` sebagai argumen dan
mengembalikan *reference* ke bagian dari `post` itu, jadi *lifetime* *reference*
yang dikembalikan berkaitan dengan *lifetime* argumen `post`.

Dan selesai—semua Listing 18-11 sekarang bekerja! Kita telah
mengimplementasikan state pattern dengan aturan alur kerja post blog. Logika
yang berkaitan dengan aturan-aturan itu hidup di *state object* alih-alih
tersebar di seluruh `Post`.

> ### Mengapa Tidak Enum?
>
> Anda mungkin bertanya-tanya mengapa kita tidak memakai *enum* dengan berbagai
> kemungkinan state post sebagai varian. Itu tentu solusi yang mungkin; coba
> saja dan bandingkan hasil akhirnya untuk melihat mana yang Anda sukai! Salah
> satu kekurangan memakai *enum* adalah setiap tempat yang mengecek nilai *enum*
> itu akan membutuhkan expression `match` atau yang serupa untuk menangani
> setiap varian yang mungkin. Ini bisa menjadi lebih berulang daripada solusi
> *trait object* ini.

<!-- Old headings. Do not remove or links may break. -->

<a id="trade-offs-of-the-state-pattern"></a>

#### Mengevaluasi Pattern State

Kita telah menunjukkan bahwa Rust mampu mengimplementasikan state pattern
berorientasi objek untuk mengenkapsulasi berbagai jenis perilaku yang harus
dimiliki sebuah post di setiap state. Method-method pada `Post` tidak tahu
apa-apa tentang berbagai perilaku itu. Karena cara kita mengatur kode, kita
hanya perlu melihat satu tempat untuk mengetahui berbagai cara post yang
diterbitkan bisa berperilaku: implementasi *trait* `State` pada *struct*
`Published`.

Jika kita membuat implementasi alternatif yang tidak memakai state pattern, kita
mungkin memakai expression `match` di method-method pada `Post` atau bahkan di
kode `main` yang mengecek state post dan mengubah perilaku di tempat-tempat
itu. Itu berarti kita harus melihat di beberapa tempat untuk memahami semua
implikasi post yang berada di state diterbitkan.

Dengan state pattern, method-method `Post` dan tempat-tempat kita memakai `Post`
tidak membutuhkan expression `match`, dan untuk menambahkan state baru, kita
hanya perlu menambahkan *struct* baru dan mengimplementasikan method *trait* pada
satu *struct* itu di satu lokasi.

Implementasi yang memakai state pattern mudah diperluas untuk menambahkan lebih
banyak fungsionalitas. Untuk melihat kesederhanaan memelihara kode yang
memakai state pattern, coba beberapa saran ini:

- Tambahkan method `reject` yang mengubah state post dari `PendingReview`
  kembali ke `Draft`.
- Mewajibkan dua pemanggilan `approve` sebelum state bisa diubah menjadi
  `Published`.
- Izinkan pengguna menambahkan konten teks hanya ketika post berada di state
  `Draft`. Petunjuk: buat *state object* bertanggung jawab atas apa yang mungkin
  berubah pada konten, tetapi tidak bertanggung jawab mengubah `Post`.

Salah satu sisi negatif state pattern adalah, karena state mengimplementasikan
transisi antar-state, sebagian state saling terkait satu sama lain. Jika kita
menambahkan state lain di antara `PendingReview` dan `Published`, seperti
`Scheduled`, kita harus mengubah kode di `PendingReview` untuk bertransisi ke
`Scheduled` sebagai gantinya. Akan lebih sedikit pekerjaan jika `PendingReview` tidak perlu
berubah dengan penambahan state baru, tetapi itu berarti beralih ke pattern
desain lain.

Sisi negatif lainnya adalah kita telah menduplikasi sebagian logika. Untuk
menghilangkan sebagian duplikasi, kita bisa mencoba membuat implementasi
bawaan untuk method `request_review` dan `approve` pada *trait* `State` yang
mengembalikan `self`. Namun, ini tidak akan bekerja: ketika memakai `State`
sebagai *trait object*, *trait* itu tidak tahu apa persisnya `self` yang konkret,
jadi return typenya tidak diketahui pada waktu kompilasi. (Ini salah satu
aturan kompatibilitas dyn yang disebutkan sebelumnya.)

Duplikasi lain mencakup implementasi serupa dari method `request_review` dan
`approve` pada `Post`. Kedua method memakai `Option::take` dengan *field*
`state` dari `Post`, dan jika `state` adalah `Some`, mereka mendelegasikan ke
implementasi method yang sama dari nilai yang terbungkus dan menetapkan nilai
baru *field* `state` ke hasilnya. Jika kita punya banyak method pada `Post`
yang mengikuti pattern ini, kita bisa mempertimbangkan mendefinisikan *macro*
untuk menghilangkan pengulangannya (lihat bagian [“Macro”][macros]<!-- ignore -->
di Bab 20).

Dengan mengimplementasikan state pattern persis seperti yang didefinisikan untuk
bahasa berorientasi objek, kita tidak memanfaatkan kekuatan Rust sepenuh yang
kita bisa. Mari kita lihat beberapa perubahan yang bisa kita buat pada *crate*
`blog` yang bisa menjadikan state dan transisi yang tidak valid sebagai error
waktu kompilasi.

<a id="encoding-states-and-behavior-as-types"></a>
### Menyandikan State dan Perilaku sebagai Type

Kami akan menunjukkan cara memikirkan ulang state pattern untuk mendapatkan
sekumpulan kompromi yang berbeda. Alih-alih mengenkapsulasi state dan
transisi sepenuhnya sehingga kode luar tidak mengetahuinya, kita akan
menyandikan state ke dalam type yang berbeda. Akibatnya, sistem pemeriksaan
type Rust akan mencegah upaya memakai post draf di tempat yang hanya
mengizinkan post yang diterbitkan dengan mengeluarkan error *compiler*.

Mari kita pertimbangkan bagian pertama `main` di Listing 18-11:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

Kita tetap mengaktifkan pembuatan post baru di state draf menggunakan
`Post::new` dan kemampuan menambahkan teks ke konten post. Tetapi alih-alih
memiliki method `content` pada post draf yang mengembalikan string kosong,
kita akan membuatnya sedemikian rupa sehingga post draf tidak memiliki method
`content` sama sekali. Dengan begitu, jika kita mencoba mendapatkan konten
post draf, kita akan mendapat error *compiler* yang memberi tahu kita method
itu tidak ada. Hasilnya, mustahil bagi kita untuk secara tidak sengaja
menampilkan konten post draf di produksi karena kode itu bahkan tidak akan
terkompilasi. Listing 18-19 menunjukkan definisi *struct* `Post` dan *struct*
`DraftPost`, beserta method pada masing-masing.

<Listing number="18-19" file-name="src/lib.rs" caption="`Post` dengan method `content` dan `DraftPost` tanpa method `content`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

Baik *struct* `Post` maupun `DraftPost` memiliki *field* privat `content` yang
menyimpan teks post blog. Kedua *struct* tidak lagi memiliki *field* `state`
karena kita memindahkan penyandian state ke type *struct*-nya. *Struct* `Post`
akan merepresentasikan post yang diterbitkan, dan ia memiliki method
`content` yang mengembalikan `content` itu.

Kita masih memiliki fungsi `Post::new`, tetapi alih-alih mengembalikan
instance `Post`, fungsi itu mengembalikan instance `DraftPost`. Karena
`content` privat dan tidak ada fungsi yang mengembalikan `Post`, mustahil
untuk membuat instance `Post` saat ini.

*Struct* `DraftPost` memiliki method `add_text`, jadi kita bisa menambahkan teks
ke `content` seperti sebelumnya, tetapi perhatikan bahwa `DraftPost` tidak
memiliki method `content` yang terdefinisi! Jadi sekarang program memastikan
semua post dimulai sebagai post draf, dan post draf tidak memiliki konten yang
tersedia untuk ditampilkan. Upaya apa pun untuk mengakali batasan-batasan ini
akan menghasilkan error *compiler*.

<!-- Old headings. Do not remove or links may break. -->

<a id="implementing-transitions-as-transformations-into-different-types"></a>

Jadi, bagaimana kita mendapatkan post yang diterbitkan? Kita ingin menegakkan
aturan bahwa post draf harus di-review dan disetujui sebelum bisa
diterbitkan. Post di state menunggu review tetap tidak boleh menampilkan
konten apa pun. Mari kita implementasikan batasan-batasan ini dengan
menambahkan *struct* lain, `PendingReviewPost`, mendefinisikan method
`request_review` pada `DraftPost` untuk mengembalikan `PendingReviewPost`,
dan mendefinisikan method `approve` pada `PendingReviewPost` untuk
mengembalikan `Post`, seperti yang ditunjukkan di Listing 18-20.

<Listing number="18-20" file-name="src/lib.rs" caption="`PendingReviewPost` yang dibuat dengan memanggil `request_review` pada `DraftPost` dan method `approve` yang mengubah `PendingReviewPost` menjadi `Post` yang diterbitkan">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

Method `request_review` dan `approve` mengambil *ownership* `self`, sehingga
mengonsumsi instance `DraftPost` dan `PendingReviewPost` dan mengubahnya
masing-masing menjadi `PendingReviewPost` dan `Post` yang diterbitkan. Dengan cara ini,
kita tidak akan punya instance `DraftPost` yang tersisa setelah kita memanggil
`request_review` padanya, dan seterusnya. *Struct* `PendingReviewPost` tidak
memiliki method `content` yang terdefinisi padanya, jadi mencoba membaca
kontennya menghasilkan error *compiler*, sama seperti `DraftPost`. Karena
satu-satunya cara mendapatkan instance `Post` yang diterbitkan—yang memang
memiliki method `content`—adalah memanggil method `approve` pada
`PendingReviewPost`, dan satu-satunya cara mendapatkan `PendingReviewPost`
adalah memanggil method `request_review` pada `DraftPost`, kita kini telah
menyandikan alur kerja post blog ke dalam type system.

Tetapi kita juga harus membuat beberapa perubahan kecil pada `main`. Method
`request_review` dan `approve` mengembalikan instance baru alih-alih mengubah
*struct* yang dipanggil, jadi kita perlu menambahkan lebih banyak assignment
shadowing `let post =` untuk menyimpan instance yang dikembalikan. Kita juga
tidak bisa lagi memiliki asersi bahwa konten post draf dan post menunggu
review adalah string kosong, dan kita juga tidak memerlukannya: kita tidak
bisa mengompilasi kode yang mencoba memakai konten post pada state-state itu.
Kode yang diperbarui di `main` ditunjukkan di Listing 18-21.

<Listing number="18-21" file-name="src/main.rs" caption="Modifikasi pada `main` untuk memakai implementasi baru alur kerja post blog">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

Perubahan yang harus kita buat pada `main` untuk menetapkan ulang `post`
berarti implementasi ini tidak lagi sepenuhnya mengikuti state pattern
berorientasi objek: transformasi antar-state tidak lagi terenkapsulasi
seluruhnya di dalam implementasi `Post`. Namun, keuntungan kita adalah state
yang tidak valid kini mustahil karena type system dan pemeriksaan type yang
terjadi pada waktu kompilasi! Ini memastikan bug tertentu, seperti penampilan
konten post yang belum diterbitkan, akan ditemukan sebelum sempat masuk ke
produksi.

Coba tugas-tugas yang disarankan di awal bagian ini pada *crate* `blog` dalam
kondisinya setelah Listing 18-21 untuk melihat pendapat Anda tentang desain
versi kode ini. Perhatikan bahwa sebagian tugas itu mungkin sudah selesai di
desain ini.

Kita telah melihat bahwa meskipun Rust mampu mengimplementasikan pattern desain
berorientasi objek, pattern lain, seperti menyandikan state ke dalam sistem
type, juga tersedia di Rust. Pattern-pattern ini punya kompromi yang berbeda.
Meskipun Anda mungkin sangat familier dengan pattern berorientasi objek,
memikirkan ulang masalah untuk memanfaatkan fitur-fitur Rust bisa memberikan
manfaat, seperti mencegah sebagian bug pada waktu kompilasi. Pattern
berorientasi objek tidak selalu menjadi solusi terbaik di Rust karena
fitur-fitur tertentu, seperti *ownership*, yang tidak dimiliki bahasa
berorientasi objek.

## Ringkasan

Terlepas dari apakah Anda menganggap Rust bahasa berorientasi objek setelah
membaca bab ini, kini Anda tahu bahwa Anda bisa memakai *trait object* untuk
mendapatkan sebagian fitur berorientasi objek di Rust. *Dynamic dispatch* bisa
memberi kode Anda sedikit fleksibilitas dengan imbalan sedikit performa
runtime. Anda bisa memakai fleksibilitas ini untuk mengimplementasikan pattern
berorientasi objek yang bisa membantu kemudahan pemeliharaan kode Anda. Rust
juga punya fitur lain, seperti *ownership*, yang tidak dimiliki bahasa
berorientasi objek. Pattern berorientasi objek tidak selalu menjadi cara terbaik
untuk memanfaatkan kekuatan Rust, tetapi ia opsi yang tersedia.

Berikutnya, kita akan melihat pattern, fitur Rust lain yang memungkinkan banyak
fleksibilitas. Kita telah melihatnya sekilas di sepanjang buku tetapi belum
melihat kemampuan penuhnya. Ayo!

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros
