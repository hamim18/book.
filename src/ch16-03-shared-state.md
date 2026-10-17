## Konkurensi Shared-State

*Message passing* adalah cara yang baik untuk menangani konkurensi, tetapi itu
bukan satu-satunya cara. Metode lain adalah membiarkan beberapa thread
mengakses data bersama yang sama. Perhatikan kembali bagian slogan dari
dokumentasi bahasa Go ini: “Do not communicate by sharing memory.”

Seperti apa rupa komunikasi dengan berbagi memori? Selain itu, mengapa para
penggemar *message passing* mengingatkan agar tidak memakai pembagian memori?

Dengan satu cara, *channel* dalam bahasa pemrograman mana pun mirip dengan
*ownership* tunggal karena begitu Anda mentransfer nilai melalui *channel*, Anda
tidak boleh lagi memakai nilai itu. Konkurensi shared-memory seperti
*ownership* ganda: Beberapa thread dapat mengakses lokasi memori yang sama pada
saat yang sama. Seperti yang Anda lihat di Bab 15, ketika *smart pointer*
memungkinkan *ownership* ganda, *ownership* ganda dapat menambah kompleksitas
karena pemilik-pemilik yang berbeda ini perlu dikelola. Sistem tipe dan
aturan *ownership* Rust sangat membantu dalam menangani pengelolaan ini dengan
benar. Sebagai contoh, mari kita lihat mutex, salah satu primitif konkurensi
yang lebih umum untuk memori bersama.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-mutexes-to-allow-access-to-data-from-one-thread-at-a-time"></a>

### Mengontrol Akses dengan Mutex

_Mutex_ adalah singkatan dari _mutual exclusion_ (eksklusi mutual), yang
artinya mutex hanya mengizinkan satu thread mengakses sejumlah data pada satu
waktu. Untuk mengakses data dalam sebuah mutex, sebuah thread pertama-tama
harus memberi sinyal bahwa ia ingin mengaksesnya dengan meminta memperoleh
lock mutex itu. _Lock_ (kunci) adalah struktur data yang merupakan bagian
dari mutex yang melacak siapa yang saat ini memiliki akses eksklusif ke data
itu. Karena itu, mutex digambarkan sebagai yang _menjaga_ data yang
ditampungnya melalui sistem penguncian.

Mutex terkenal sulit dipakai karena Anda harus mengingat dua aturan:

1. Anda harus mencoba memperoleh lock sebelum memakai datanya.
2. Ketika Anda selesai dengan data yang dijaga mutex, Anda harus membuka kunci
   data itu supaya thread lain dapat memperoleh lock.

Untuk metafora mutex di dunia nyata, bayangkan diskusi panel di sebuah
konferensi yang hanya memiliki satu mikrofon. Sebelum seorang panelis dapat
berbicara, mereka harus meminta atau memberi sinyal bahwa mereka ingin memakai
mikrofon itu. Ketika mereka mendapat mikrofon, mereka dapat berbicara selama
yang mereka mau, lalu menyerahkan mikrofon itu kepada panelis berikutnya yang
meminta untuk berbicara. Jika seorang panelis lupa menyerahkan mikrofon ketika
selesai memakainya, tidak ada orang lain yang bisa berbicara. Jika pengelolaan
mikrofon bersama itu kacau, panel tidak akan berjalan sesuai rencana!

Pengelolaan mutex bisa sangat rumit untuk dilakukan dengan benar, yang menjadi
alasan begitu banyak orang antusias dengan *channel*. Namun, berkat sistem tipe
dan aturan *ownership* Rust, Anda tidak bisa salah dalam mengunci dan membuka
kunci.

#### API dari `Mutex<T>`

Sebagai contoh cara memakai mutex, mari kita mulai dengan memakai mutex dalam
konteks single-threaded, seperti ditunjukkan pada Listing 16-12.

<Listing number="16-12" file-name="src/main.rs" caption="Menjelajahi API `Mutex<T>` dalam konteks single-threaded demi kesederhanaan">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-12/src/main.rs}}
```

</Listing>

Seperti banyak tipe lain, kita membuat `Mutex<T>` menggunakan associated
function `new`. Untuk mengakses data di dalam mutex, kita memakai metode
`lock` untuk memperoleh lock. Panggilan ini akan memblokir thread saat ini
sehingga ia tidak bisa melakukan pekerjaan apa pun sampai giliran kita
memiliki lock.

Panggilan ke `lock` akan gagal jika thread lain yang memegang lock itu panic.
Dalam kasus itu, tidak akan pernah ada yang bisa mendapat lock, jadi kita
memilih untuk `unwrap` dan membuat thread ini panic jika kita berada dalam
situasi itu.

Setelah kita memperoleh lock, kita dapat memperlakukan nilai kembaliannya,
yang bernama `num` dalam kasus ini, sebagai *mutable* *reference* ke data di
dalamnya. Sistem tipe memastikan bahwa kita memperoleh lock sebelum memakai
nilai di dalam `m`. Tipe `m` adalah `Mutex<i32>`, bukan `i32`, jadi kita
_harus_ memanggil `lock` untuk bisa memakai nilai `i32` itu. Kita tidak bisa
lupa; sistem tipe tidak akan mengizinkan kita mengakses `i32` bagian dalam
jika tidak.

Panggilan ke `lock` mengembalikan tipe bernama `MutexGuard`, yang dibungkus
dalam `LockResult` yang kita tangani dengan panggilan ke `unwrap`. Tipe
`MutexGuard` mengimplementasikan `Deref` untuk menunjuk ke data bagian dalam
kita; tipe itu juga memiliki implementasi `Drop` yang melepas lock secara
otomatis ketika sebuah `MutexGuard` keluar dari *scope*, yang terjadi di akhir
*scope* dalam. Akibatnya, kita tidak berisiko lupa melepas lock dan menghalangi
mutex dipakai thread lain karena pelepasan lock terjadi secara otomatis.

Setelah melepas lock, kita dapat mencetak nilai mutex dan melihat bahwa kita
berhasil mengubah `i32` bagian dalam menjadi `6`.

<!-- Old headings. Do not remove or links may break. -->

<a id="sharing-a-mutext-between-multiple-threads"></a>

<a id="shared-access-to-mutext"></a>
#### Akses Bersama ke `Mutex<T>`

Sekarang mari kita coba berbagi nilai di antara beberapa thread menggunakan
`Mutex<T>`. Kita akan menjalankan 10 thread dan menyuruh masing-masing
menambah nilai pencacah sebesar 1, sehingga pencacahnya bergerak dari 0 ke
10. Contoh di Listing 16-13 akan menghasilkan galat kompilator, dan kita akan
memakai galat itu untuk belajar lebih banyak tentang pemakaian `Mutex<T>` dan
bagaimana Rust membantu kita memakainya dengan benar.

<Listing number="16-13" file-name="src/main.rs" caption="Sepuluh thread, masing-masing menambah pencacah yang dijaga oleh `Mutex<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-13/src/main.rs}}
```

</Listing>

Kita membuat variabel `counter` untuk menampung `i32` di dalam `Mutex<T>`,
seperti yang kita lakukan di Listing 16-12. Selanjutnya, kita membuat 10
thread dengan mengiterasi range angka. Kita memakai `thread::spawn` dan
memberikan *closure* yang sama kepada semua thread: *closure* yang memindahkan
counter ke dalam thread, memperoleh lock pada `Mutex<T>` dengan memanggil
metode `lock`, lalu menambahkan 1 ke nilai di dalam mutex. Ketika sebuah
thread selesai menjalankan *closure*-nya, `num` akan keluar dari *scope* dan
melepas lock sehingga thread lain dapat memperolehnya.

Di thread utama, kita mengumpulkan semua handle join. Kemudian, seperti yang
kita lakukan di Listing 16-2, kita memanggil `join` pada setiap handle untuk
memastikan semua thread selesai. Pada titik itu, thread utama akan memperoleh
lock dan mencetak hasil program ini.

Kita telah memberi petunjuk bahwa contoh ini tidak akan terkompilasi. Sekarang
mari kita cari tahu alasannya!

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-13/output.txt}}
```

Pesan galat itu menyatakan bahwa nilai `counter` telah dipindahkan pada
iterasi perulangan sebelumnya. Rust memberi tahu kita bahwa kita tidak bisa
memindahkan *ownership* lock `counter` ke banyak thread. Mari kita perbaiki
galat kompilator itu dengan metode *ownership* ganda yang kita bahas di Bab 15.

#### Kepemilikan Ganda dengan Banyak Thread

Di Bab 15, kita memberikan nilai kepada beberapa pemilik dengan memakai smart
*pointer* `Rc<T>` untuk membuat nilai dengan penghitungan referensi. Mari kita
lakukan hal yang sama di sini dan lihat apa yang terjadi. Kita akan membungkus
`Mutex<T>` di dalam `Rc<T>` di Listing 16-14 dan mengklon `Rc<T>` itu sebelum
memindahkan *ownership* ke thread.

<Listing number="16-14" file-name="src/main.rs" caption="Mencoba memakai `Rc<T>` untuk mengizinkan beberapa thread memiliki `Mutex<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-14/src/main.rs}}
```

</Listing>

Sekali lagi, kita mengompilasi dan mendapat... galat yang berbeda! Kompilator
sedang mengajari kita banyak hal:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-14/output.txt}}
```

Wah, pesan galat itu panjang lebar sekali! Berikut bagian penting yang perlu
difokuskan: `` `Rc<Mutex<i32>>` cannot be sent between threads safely ``.
Kompilator juga memberi tahu alasannya: `` the *trait* `Send` is not implemented
for `Rc<Mutex<i32>>` ``. Kita akan membahas `Send` di seksi berikutnya: Ini
adalah salah satu *trait* yang memastikan bahwa tipe yang kita pakai dengan
thread memang dimaksudkan untuk dipakai dalam situasi konkuren.

Sayangnya, `Rc<T>` tidak aman untuk dibagikan antar-thread. Ketika `Rc<T>`
mengelola jumlah referensi, ia menambah jumlah itu untuk setiap panggilan ke
`clone` dan menguranginya ketika setiap klon dibebaskan. Tetapi ia tidak
memakai primitif konkurensi apa pun untuk memastikan perubahan pada jumlah itu
tidak bisa disela thread lain. Ini bisa menyebabkan jumlah yang salah—bug
samar yang pada gilirannya bisa menyebabkan kebocoran memori atau nilai yang
dibebaskan sebelum kita selesai memakainya. Yang kita butuhkan adalah tipe
yang persis seperti `Rc<T>`, tetapi mengubah jumlah referensi dengan cara yang
thread-safe.

#### Penghitungan Referensi Atomik dengan `Arc<T>`

Untungnya, `Arc<T>` _adalah_ tipe seperti `Rc<T>` yang aman dipakai dalam
situasi konkuren. Huruf _a_ berarti _atomic_ (atomik), yang berarti tipe itu
adalah tipe yang _dihitung referensinya secara atomik_. Atomik adalah jenis
primitif konkurensi tambahan yang tidak akan kita bahas secara mendetail di
sini: Lihat dokumentasi pustaka standar untuk [`std::sync::atomic`][atomic]<!--
ignore --> untuk detail lebih lanjut. Pada titik ini, Anda cukup tahu bahwa
atomik bekerja seperti tipe primitif tetapi aman dibagikan antar-thread.

Anda mungkin lalu bertanya-tanya mengapa semua tipe primitif tidak atomik dan
mengapa tipe-tipe pustaka standar tidak diimplementasikan memakai `Arc<T>`
secara default. Alasannya adalah thread safety datang dengan denda performa
yang hanya ingin Anda bayar ketika benar-benar membutuhkannya. Jika Anda hanya
melakukan operasi pada nilai di dalam satu thread, kode Anda dapat berjalan
lebih cepat jika ia tidak harus menegakkan jaminan yang disediakan atomik.

Mari kita kembali ke contoh kita: `Arc<T>` dan `Rc<T>` memiliki API yang sama,
jadi kita memperbaiki program kita dengan mengubah baris `use`, panggilan ke
`new`, dan panggilan ke `clone`. Kode di Listing 16-15 akhirnya akan
terkompilasi dan berjalan.

<Listing number="16-15" file-name="src/main.rs" caption="Memakai `Arc<T>` untuk membungkus `Mutex<T>` agar dapat berbagi ownership lintas thread">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-15/src/main.rs}}
```

</Listing>

Kode ini akan mencetak hal berikut:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Result: 10
```

Kita berhasil! Kita menghitung dari 0 sampai 10, yang mungkin tidak tampak
begitu mengesankan, tetapi itu memang mengajari kita banyak tentang `Mutex<T>`
dan thread safety. Anda juga bisa memakai struktur program ini untuk melakukan
operasi yang lebih rumit daripada sekadar menambah pencacah. Dengan strategi
ini, Anda dapat membagi perhitungan menjadi bagian-bagian independen,
memecah bagian-bagian itu lintas thread, lalu memakai `Mutex<T>` agar setiap
thread memperbarui hasil akhir dengan bagiannya.

Perhatikan bahwa jika Anda melakukan operasi numerik sederhana, ada tipe yang
lebih sederhana daripada tipe `Mutex<T>` yang disediakan oleh [modul
`std::sync::atomic` pada pustaka standar][atomic]<!-- ignore -->. Tipe-tipe
ini menyediakan akses atomik, konkuren, dan aman ke tipe primitif. Kita
memilih memakai `Mutex<T>` dengan tipe primitif untuk contoh ini supaya kita
dapat berkonsentrasi pada cara kerja `Mutex<T>`.

<!-- Old headings. Do not remove or links may break. -->

<a id="similarities-between-refcelltrct-and-mutextarct"></a>

### Membandingkan `RefCell<T>`/`Rc<T>` dan `Mutex<T>`/`Arc<T>`

Anda mungkin menyadari bahwa `counter` bersifat *immutable* tetapi kita bisa
mendapat *mutable* *reference* ke nilai di dalamnya; ini berarti `Mutex<T>`
menyediakan *interior mutability*, seperti yang dilakukan keluarga `Cell`.
Dengan cara yang sama ketika kita memakai `RefCell<T>` di Bab 15 untuk
mengizinkan kita mengubah isi di dalam `Rc<T>`, kita memakai `Mutex<T>` untuk
mengubah isi di dalam `Arc<T>`.

Detail lain yang perlu dicatat adalah bahwa Rust tidak bisa melindungi Anda
dari semua jenis galat logika ketika Anda memakai `Mutex<T>`. Ingat dari Bab
15 bahwa memakai `Rc<T>` datang dengan risiko menciptakan *reference cycle*,
ketika dua nilai `Rc<T>` saling merujuk, menyebabkan kebocoran memori.
Demikian pula, `Mutex<T>` datang dengan risiko menciptakan deadlock. Ini
terjadi ketika sebuah operasi perlu mengunci dua resource dan dua thread
masing-masing telah memperoleh salah satu lock, menyebabkan keduanya saling
menunggu selamanya. Jika Anda tertarik pada deadlock, cobalah membuat program
Rust yang memiliki deadlock; lalu, teliti strategi mitigasi deadlock untuk
mutex dalam bahasa apa pun dan cobalah mengimplementasikannya di Rust.
Dokumentasi API pustaka standar untuk `Mutex<T>` dan `MutexGuard` menawarkan
informasi yang berguna.

Kita akan menutup bab ini dengan membicarakan *trait* `Send` dan `Sync` serta
cara kita dapat memakainya dengan tipe buatan sendiri.

[atomic]: ../std/sync/atomic/index.html
