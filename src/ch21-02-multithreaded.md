<!-- Old headings. Do not remove or links may break. -->

<a id="turning-our-single-threaded-server-into-a-multithreaded-server"></a>
<a id="from-single-threaded-to-multithreaded-server"></a>

## Dari Server Single-Threaded Menjadi Multithreaded

Saat ini, server akan memproses setiap permintaan secara bergiliran, yang
berarti ia tidak akan memproses koneksi kedua sampai koneksi pertama
selesai diproses. Jika server menerima permintaan yang semakin banyak,
eksekusi serial ini akan semakin tidak optimal. Jika server menerima
permintaan yang butuh waktu lama untuk diproses, permintaan-permintaan
berikutnya harus menunggu sampai permintaan yang lama itu selesai, bahkan
jika permintaan-permintaan baru itu bisa diproses dengan cepat. Kita perlu
memperbaikinya, tetapi pertama-tama mari kita lihat masalahnya secara
langsung.

<!-- Old headings. Do not remove or links may break. -->

<a id="simulating-a-slow-request-in-the-current-server-implementation"></a>

### Menyimulasikan Permintaan yang Lambat

Kita akan melihat bagaimana permintaan yang diproses dengan lambat bisa
memengaruhi permintaan lain yang dibuat ke implementasi server kita saat
ini. Listing 21-10 mengimplementasikan penanganan permintaan ke _/sleep_
dengan respons lambat yang disimulasikan yang akan membuat server tidur
selama lima detik sebelum merespons.

<Listing number="21-10" file-name="src/main.rs" caption="Menyimulasikan permintaan yang lambat dengan tidur selama lima detik">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```

</Listing>

Kita beralih dari `if` ke `match` sekarang setelah kita punya tiga kasus.
Kita perlu mencocokkan secara eksplisit terhadap *slice* dari `request_line`
untuk mencocokkan pattern dengan nilai string literalnya; `match` tidak
melakukan referencing dan dereferencing otomatis, seperti yang dilakukan
method kesamaan.

Arm pertama sama dengan blok `if` dari Listing 21-9. Arm kedua mencocokkan
permintaan ke _/sleep_. Ketika permintaan itu diterima, server akan tidur
selama lima detik sebelum merender halaman HTML sukses. Arm ketiga sama
dengan blok `else` dari Listing 21-9.

Anda bisa melihat betapa primitifnya server kita: Library sungguhan akan
menangani pengenalan banyak permintaan dengan cara yang jauh lebih ringkas!

Mulai server dengan memakai `cargo run`. Lalu, buka dua jendela peramban:
satu untuk _http://127.0.0.1:7878_ dan satu lagi untuk
_http://127.0.0.1:7878/sleep_. Jika Anda memasukkan URI _/_ beberapa kali,
seperti sebelumnya, Anda akan melihat ia merespons dengan cepat. Tetapi
jika Anda memasukkan _/sleep_ lalu memuat _/_, Anda akan melihat bahwa _/_
menunggu sampai `sleep` tidur selama lima detik penuh sebelum dimuat.

Ada banyak teknik yang bisa kita pakai untuk menghindari permintaan yang
menumpuk di belakang permintaan yang lambat, termasuk memakai async seperti
yang kita lakukan di Bab 17; yang akan kita implementasikan adalah thread
pool.

### Meningkatkan Throughput dengan Thread Pool

_Thread pool_ adalah sekelompok thread yang telah dibuat dan sedang siap
menunggu untuk menangani tugas. Ketika program menerima tugas baru, ia
menugaskan salah satu thread di pool itu ke tugas tersebut, dan thread itu
akan memproses tugasnya. Thread-thread tersisa di pool tersedia untuk
menangani tugas lain apa pun yang masuk sementara thread pertama sedang
memproses. Ketika thread pertama selesai memproses tugasnya, ia
dikembalikan ke kumpulan thread yang menganggur, siap menangani tugas baru.
*Thread pool* memungkinkan Anda memproses koneksi secara konkuren, sehingga
throughput server Anda meningkat.

Kita akan membatasi jumlah thread di pool menjadi angka kecil untuk
melindungi kita dari serangan DoS; jika program kita membuat thread baru
untuk setiap permintaan yang masuk, seseorang yang membuat 10 juta
permintaan ke server kita bisa membuat kekacauan dengan menghabiskan semua
sumber daya server kita dan membuat pemrosesan permintaan berhenti total.

Jadi, alih-alih membuat thread tanpa batas, kita akan punya sejumlah tetap
thread yang menunggu di pool. Permintaan yang masuk dikirim ke pool untuk
diproses. Pool akan memelihara antrean permintaan yang masuk. Setiap thread
di pool akan mengambil sebuah permintaan dari antrean ini, menangani
permintaan itu, lalu meminta permintaan lain dari antrean. Dengan desain
ini, kita bisa memproses hingga _`N`_ permintaan secara konkuren, dengan
_`N`_ adalah jumlah thread. Jika setiap thread sedang merespons permintaan
yang berjalan lama, permintaan-permintaan berikutnya tetap bisa menumpuk di
antrean, tetapi kita telah meningkatkan jumlah permintaan berjalan lama
yang bisa kita tangani sebelum mencapai titik itu.

Teknik ini hanyalah salah satu dari banyak cara untuk meningkatkan
throughput server web. Pilihan lain yang mungkin Anda jelajahi adalah model
fork/join, model I/O async single-threaded, dan model I/O async
multithreaded. Jika Anda tertarik dengan topik ini, Anda bisa membaca lebih
banyak tentang solusi-solusi lain dan mencoba mengimplementasikannya;
dengan low-level language seperti Rust, semua pilihan ini dimungkinkan.

Sebelum kita mulai mengimplementasikan *thread pool*, mari kita bicarakan
seperti apa pemakaian pool itu seharusnya. Saat Anda mencoba mendesain
kode, menulis antarmuka client terlebih dahulu bisa membantu memandu desain
Anda. Tulis API kodenya supaya terstruktur sesuai cara Anda ingin
memanggilnya; kemudian, implementasikan fungsionalitasnya di dalam struktur
itu, alih-alih mengimplementasikan fungsionalitasnya lalu mendesain API
publiknya.

Mirip dengan cara kita memakai pengembangan yang digerakkan oleh pengujian
di proyek Bab 12, di sini kita akan memakai *compiler-driven development*
(pengembangan yang digerakkan oleh *compiler*). Kita akan menulis kode yang
memanggil fungsi-fungsi yang kita inginkan, lalu kita akan melihat error
dari *compiler* untuk menentukan apa yang harus kita ubah berikutnya agar
kodenya bekerja. Namun, sebelum kita melakukannya, kita akan mengeksplorasi
teknik yang tidak akan kita pakai sebagai titik awal.

<!-- Old headings. Do not remove or links may break. -->

<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>

#### Membuat Thread untuk Setiap Permintaan

Pertama, mari kita telusuri bagaimana kode kita akan tampak jika ia memang
membuat thread baru untuk setiap koneksi. Seperti yang disebutkan
sebelumnya, ini bukan rencana akhir kita karena ada masalah dengan
kemungkinan membuat thread dalam jumlah tak terbatas, tetapi ini adalah
titik awal untuk mendapatkan server multithreaded yang bekerja terlebih
dahulu. Lalu, kita akan menambahkan *thread pool* sebagai penyempurnaan, dan
membandingkan kedua solusi itu akan menjadi lebih mudah.

Listing 21-11 menunjukkan perubahan yang harus dilakukan pada `main` untuk
membuat thread baru yang menangani setiap *stream* di dalam loop `for`.

<Listing number="21-11" file-name="src/main.rs" caption="Membuat thread baru untuk setiap stream">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```

</Listing>

Seperti yang Anda pelajari di Bab 16, `thread::spawn` akan membuat thread
baru lalu menjalankan kode di *closure* itu di thread baru. Jika Anda
menjalankan kode ini dan memuat _/sleep_ di peramban Anda, lalu _/_ di dua
tab peramban lagi, Anda memang akan melihat bahwa permintaan ke _/_ tidak
harus menunggu _/sleep_ selesai. Akan tetapi, seperti yang kita sebutkan,
ini pada akhirnya akan membebani sistem karena Anda membuat thread baru
tanpa batas.

Anda mungkin juga ingat dari Bab 17 bahwa ini persis jenis situasi di mana
async dan await benar-benar bersinar! Ingatlah itu sambil kita membangun
*thread pool* dan pikirkan bagaimana semuanya akan tampak berbeda atau sama
dengan async.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>

<a id="creating-a-finite-number-of-threads"></a>
#### Membuat Thread dalam Jumlah Terbatas

Kita ingin *thread pool* kita bekerja dengan cara yang serupa dan familier
sehingga peralihan dari thread ke *thread pool* tidak memerlukan perubahan
besar pada kode yang memakai API kita. Listing 21-12 menunjukkan antarmuka
hipotetis untuk *struct* `ThreadPool` yang ingin kita pakai alih-alih
`thread::spawn`.

<Listing number="21-12" file-name="src/main.rs" caption="Antarmuka `ThreadPool` ideal kita">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

Kita memakai `ThreadPool::new` untuk membuat *thread pool* baru dengan jumlah
thread yang dapat dikonfigurasi, dalam kasus ini empat. Lalu, di loop `for`,
`pool.execute` memiliki antarmuka yang mirip dengan `thread::spawn`, yaitu
menerima *closure* yang harus dijalankan pool untuk setiap *stream*. Kita perlu
mengimplementasikan `pool.execute` supaya ia menerima *closure* itu dan
memberikannya kepada thread di pool untuk dijalankan. Kode ini belum akan
terkompilasi, tetapi kita akan mencobanya supaya *compiler* bisa memandu
kita dalam memperbaikinya.

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>

#### Membangun `ThreadPool` dengan Compiler-Driven Development

Buat perubahan di Listing 21-12 pada _src/main.rs_, lalu mari kita pakai
error *compiler* dari `cargo check` untuk mendorong pengembangan kita.
Berikut error pertama yang kita dapat:

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```

Bagus! Error ini memberi tahu kita bahwa kita memerlukan type atau *module*
`ThreadPool`, jadi sekarang kita akan membangunnya. Implementasi
`ThreadPool` kita akan tidak bergantung pada jenis pekerjaan yang dilakukan
server web kita. Jadi, mari kita alihkan *crate* `hello` dari *crate* binary
menjadi *crate* library untuk menampung implementasi `ThreadPool` kita.
Setelah kita mengubahnya menjadi *crate* library, kita juga bisa memakai
library *thread pool* terpisah itu untuk pekerjaan apa pun yang ingin kita
lakukan dengan *thread pool*, bukan hanya untuk melayani permintaan web.

Buat file _src/lib.rs_ yang berisi hal berikut, yaitu definisi paling
sederhana dari *struct* `ThreadPool` yang bisa kita miliki untuk saat ini:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```

</Listing>


Lalu, sunting file _main.rs_ untuk membawa `ThreadPool` ke dalam *scope* dari
*crate* library dengan menambahkan kode berikut ke bagian atas
_src/main.rs_:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```

</Listing>

Kode ini tetap belum akan bekerja, tetapi mari kita periksa lagi untuk
mendapatkan error berikutnya yang perlu kita tangani:

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```

Error ini menunjukkan bahwa berikutnya kita perlu membuat associated
function bernama `new` untuk `ThreadPool`. Kita juga tahu bahwa `new` perlu
memiliki satu parameter yang bisa menerima `4` sebagai argumen dan
seharusnya mengembalikan instance `ThreadPool`. Mari kita implementasikan
fungsi `new` paling sederhana yang akan memiliki karakteristik itu:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```

</Listing>

Kita memilih `usize` sebagai type parameter `size` karena kita tahu bahwa
jumlah thread negatif tidak masuk akal. Kita juga tahu kita akan memakai
`4` ini sebagai jumlah elemen dalam collection thread, yang memang merupakan
kegunaan type `usize`, seperti yang dibahas di seksi [“Type
Integer”][integer-types]<!-- ignore --> pada Bab 3.

Mari kita periksa kodenya lagi:

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```

Sekarang errornya muncul karena kita tidak punya method `execute` pada
`ThreadPool`. Ingat kembali dari seksi [“Membuat Thread dalam Jumlah
Terbatas”](#creating-a-finite-number-of-threads)<!-- ignore --> bahwa kita
memutuskan *thread pool* kita seharusnya memiliki antarmuka yang mirip dengan
`thread::spawn`. Selain itu, kita akan mengimplementasikan fungsi `execute`
supaya ia menerima *closure* yang diberikan kepadanya dan memberikannya
kepada thread yang menganggur di pool untuk dijalankan.

Kita akan mendefinisikan method `execute` pada `ThreadPool` untuk menerima
*closure* sebagai parameter. Ingat kembali dari [“Memindahkan Nilai yang
Ditangkap Keluar dari *Closure*”][moving-out-of-closures]<!-- ignore --> pada
Bab 13 bahwa kita bisa menerima *closure* sebagai parameter dengan tiga *trait*
yang berbeda: `Fn`, `FnMut`, dan `FnOnce`. Kita perlu memutuskan jenis
*closure* mana yang dipakai di sini. Kita tahu pada akhirnya kita akan
melakukan sesuatu yang mirip dengan implementasi `thread::spawn` di
pustaka standar, jadi kita bisa melihat bound apa yang dimiliki tanda
tangan `thread::spawn` pada parameternya. Dokumentasinya menunjukkan hal
berikut kepada kita:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Parameter type `F` adalah yang menjadi perhatian kita di sini; parameter
type `T` berkaitan dengan return value, dan itu bukan perhatian kita.
Kita bisa melihat bahwa `spawn` memakai `FnOnce` sebagai *trait bound* pada
`F`. Kemungkinan besar ini juga yang kita inginkan, karena pada akhirnya
kita akan meneruskan argumen yang kita dapat di `execute` ke `spawn`. Kita
bisa semakin yakin bahwa `FnOnce` adalah *trait* yang ingin kita pakai karena
thread untuk menjalankan sebuah permintaan hanya akan mengeksekusi *closure*
permintaan itu satu kali, yang cocok dengan `Once` pada `FnOnce`.

Parameter type `F` juga memiliki *trait bound* `Send` dan bound *lifetime*
`'static`, yang berguna dalam situasi kita: Kita memerlukan `Send` untuk
mentransfer *closure* dari satu thread ke thread lain dan `'static` karena
kita tidak tahu berapa lama thread itu akan butuh untuk mengeksekusi. Mari
kita buat method `execute` pada `ThreadPool` yang akan menerima parameter
generik typed `F` dengan bound-bound ini:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```

</Listing>

Kita tetap memakai `()` setelah `FnOnce` karena `FnOnce` ini mewakili
*closure* yang tidak menerima parameter dan mengembalikan type unit `()`.
Sama seperti definisi fungsi, return type boleh dihilangkan dari tanda
tangannya, tetapi meskipun kita tidak punya parameter, kita tetap
memerlukan tanda kurungnya.

Sekali lagi, ini adalah implementasi paling sederhana dari method
`execute`: Ia tidak melakukan apa pun, tetapi kita hanya berusaha membuat
kode kita terkompilasi. Mari kita periksa lagi:

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```

Ia terkompilasi! Tetapi perhatikan bahwa jika Anda mencoba `cargo run` dan
membuat permintaan di peramban, Anda akan melihat error-error di peramban
yang kita lihat di awal bab ini. Library kita belum benar-benar memanggil
*closure* yang diberikan ke `execute`!

> Catatan: Pepatah yang mungkin Anda dengar tentang bahasa dengan
> *compiler* yang ketat, seperti Haskell dan Rust, adalah “Jika kodenya
> terkompilasi, ia bekerja.” Tetapi pepatah ini tidak berlaku secara
> universal. Proyek kita terkompilasi, tetapi ia sama sekali tidak
> melakukan apa pun! Jika kita sedang membangun proyek yang nyata dan
> lengkap, ini adalah saat yang tepat untuk mulai menulis pengujian unit
> untuk memeriksa bahwa kode terkompilasi _dan_ memiliki perilaku yang kita
> inginkan.

Pertimbangkan: Apa yang akan berbeda di sini jika kita akan mengeksekusi
*future* alih-alih *closure*?

#### Memvalidasi Jumlah Thread di `new`

Kita belum melakukan apa pun dengan parameter-parameter `new` dan
`execute`. Mari kita implementasikan tubuh fungsi-fungsi ini dengan
perilaku yang kita inginkan. Untuk memulai, mari kita pikirkan `new`.
Sebelumnya kita memilih type tak bertanda untuk parameter `size` karena
pool dengan jumlah thread negatif tidak masuk akal. Akan tetapi, pool
dengan nol thread juga tidak masuk akal, padahal nol adalah `usize` yang
sah sepenuhnya. Kita akan menambahkan kode untuk memeriksa bahwa `size`
lebih besar daripada nol sebelum kita mengembalikan instance `ThreadPool`,
dan kita akan membuat program panic jika ia menerima nol dengan memakai
*macro* `assert!`, seperti yang ditunjukkan di Listing 21-13.

<Listing number="21-13" file-name="src/lib.rs" caption="Mengimplementasikan `ThreadPool::new` untuk panic jika `size` adalah nol">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```

</Listing>

Kita juga telah menambahkan sebagian dokumentasi untuk `ThreadPool` kita
dengan komentar dok. Perhatikan bahwa kita mengikuti praktik dokumentasi
yang baik dengan menambahkan seksi yang menyebutkan situasi-situasi di mana
fungsi kita bisa panic, seperti yang dibahas di Bab 14. Coba jalankan
`cargo doc --open` dan klik *struct* `ThreadPool` untuk melihat seperti apa
dokumentasi yang dihasilkan untuk `new`!

Alih-alih menambahkan *macro* `assert!` seperti yang kita lakukan di sini,
kita bisa mengubah `new` menjadi `build` dan mengembalikan `Result` seperti
yang kita lakukan dengan `Config::build` di proyek I/O pada Listing 12-9.
Tetapi dalam kasus ini kita memutuskan bahwa mencoba membuat *thread pool*
tanpa thread apa pun seharusnya merupakan error yang tidak dapat
dipulihkan. Jika Anda merasa tertantang, cobalah menulis fungsi bernama
`build` dengan *signature* berikut untuk dibandingkan dengan fungsi `new`:

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### Membuat Ruang untuk Menyimpan Thread

Sekarang setelah kita punya cara untuk mengetahui bahwa kita punya jumlah
thread yang valid untuk disimpan di pool, kita bisa membuat thread-thread
itu dan menyimpannya di *struct* `ThreadPool` sebelum mengembalikan *struct*
itu. Tetapi bagaimana cara kita “menyimpan” thread? Mari kita lihat lagi
*signature* `thread::spawn`:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Fungsi `spawn` mengembalikan `JoinHandle<T>`, dengan `T` adalah type yang
dikembalikan *closure* itu. Mari kita coba memakai `JoinHandle` juga dan
lihat apa yang terjadi. Dalam kasus kita, *closure* yang kita berikan ke
*thread pool* akan menangani koneksi dan tidak mengembalikan apa pun, jadi
`T` akan menjadi type unit `()`.

Kode di Listing 21-14 akan terkompilasi, tetapi ia belum membuat thread
apa pun. Kita telah mengubah definisi `ThreadPool` untuk menampung vector
instance `thread::JoinHandle<()>`, menginisialisasi vector itu dengan
kapasitas `size`, menyiapkan loop `for` yang akan menjalankan sebagian kode
untuk membuat thread-thread itu, dan mengembalikan instance `ThreadPool`
yang memuatnya.

<Listing number="21-14" file-name="src/lib.rs" caption="Membuat vector untuk `ThreadPool` agar menampung thread-threadnya">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```

</Listing>

Kita telah membawa `std::thread` ke dalam *scope* di *crate* library karena
kita memakai `thread::JoinHandle` sebagai type item-item di vector pada
`ThreadPool`.

Setelah ukuran yang valid diterima, `ThreadPool` kita membuat vector baru
yang bisa menampung `size` item. Fungsi `with_capacity` melakukan tugas
yang sama dengan `Vec::new` tetapi dengan satu perbedaan penting: Ia
mengalokasikan ruang di vector di muka. Karena kita tahu kita perlu
menyimpan `size` elemen di vector itu, melakukan *allocation* ini di muka
sedikit lebih efisien daripada memakai `Vec::new`, yang mengubah ukurannya
sendiri saat elemen-elemen dimasukkan.

Ketika Anda menjalankan `cargo check` lagi, ia seharusnya sukses.

<!-- Old headings. Do not remove or links may break. -->
<a id ="a-worker-struct-responsible-for-sending-code-from-the-threadpool-to-a-thread"></a>

#### Mengirim Kode dari `ThreadPool` ke Thread

Kita meninggalkan sebuah komentar di loop `for` pada Listing 21-14 tentang
pembuatan thread. Di sini, kita akan melihat bagaimana kita benar-benar
membuat thread. Pustaka standar menyediakan `thread::spawn` sebagai cara
membuat thread, dan `thread::spawn` mengharapkan untuk menerima sebagian
kode yang harus dijalankan thread itu segera setelah thread itu dibuat.
Akan tetapi, dalam kasus kita, kita ingin membuat thread-thread itu dan
membuat mereka _menunggu_ kode yang akan kita kirim nanti. Implementasi
thread di pustaka standar tidak menyertakan cara untuk melakukan itu; kita
harus mengimplementasikannya secara manual.

Kita akan mengimplementasikan perilaku ini dengan memperkenalkan struktur
data baru di antara `ThreadPool` dan thread-threadnya yang akan mengelola
perilaku baru ini. Kita akan menyebut struktur data ini _Worker_, istilah
yang umum dalam implementasi pooling. `Worker` mengambil kode yang perlu
dijalankan dan menjalankan kode itu di thread-nya.

Bayangkan orang-orang yang bekerja di dapur sebuah restoran: Para pekerja
menunggu sampai pesanan masuk dari pelanggan, lalu mereka bertanggung jawab
mengambil pesanan-pesanan itu dan memenuhinya.

Alih-alih menyimpan vector instance `JoinHandle<()>` di *thread pool*, kita
akan menyimpan instance *struct* `Worker`. Setiap `Worker` akan menyimpan
satu instance `JoinHandle<()>`. Lalu, kita akan mengimplementasikan method
pada `Worker` yang akan menerima *closure* berisi kode untuk dijalankan dan
mengirimnya ke thread yang sudah berjalan untuk dieksekusi. Kita juga akan
memberi setiap `Worker` sebuah `id` supaya kita bisa membedakan antara
instance-instance `Worker` yang berbeda di pool saat logging atau
debugging.

Berikut proses baru yang akan terjadi ketika kita membuat `ThreadPool`.
Kita akan mengimplementasikan kode yang mengirim *closure* ke thread setelah
kita menyiapkan `Worker` dengan cara ini:

1. Mendefinisikan *struct* `Worker` yang menampung `id` dan
   `JoinHandle<()>`.
2. Mengubah `ThreadPool` untuk menampung vector instance `Worker`.
3. Mendefinisikan fungsi `Worker::new` yang menerima nomor `id` dan
   mengembalikan instance `Worker` yang menampung `id` itu dan sebuah
   thread yang dibuat dengan *closure* kosong.
4. Di `ThreadPool::new`, memakai pencacah loop `for` untuk menghasilkan
   `id`, membuat `Worker` baru dengan `id` itu, dan menyimpan `Worker`
   tersebut di vector.

Jika Anda siap untuk tantangan, cobalah mengimplementasikan perubahan ini
sendiri sebelum melihat kode di Listing 21-15.

Siap? Berikut Listing 21-15 dengan salah satu cara untuk membuat
modifikasi-modifikasi sebelumnya.

<Listing number="21-15" file-name="src/lib.rs" caption="Mengubah `ThreadPool` untuk menampung instance `Worker`, bukan menampung thread secara langsung">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```

</Listing>

Kita telah mengubah nama *field* pada `ThreadPool` dari `threads` menjadi
`workers` karena sekarang ia menampung instance `Worker`, bukan instance
`JoinHandle<()>`. Kita memakai pencacah di loop `for` sebagai argumen
untuk `Worker::new`, dan kita menyimpan setiap `Worker` baru di vector
bernama `workers`.

Kode eksternal (seperti server kita di _src/main.rs_) tidak perlu tahu
detail implementasi tentang pemakaian *struct* `Worker` di dalam
`ThreadPool`, jadi kita membuat *struct* `Worker` dan fungsi `new`-nya
privat. Fungsi `Worker::new` memakai `id` yang kita berikan dan menyimpan
instance `JoinHandle<()>` yang dibuat dengan membuat thread baru memakai
*closure* kosong.

> Catatan: Jika sistem operasi tidak bisa membuat thread karena tidak ada
> cukup sumber daya sistem, `thread::spawn` akan panic. Itu akan membuat
> seluruh server kita panic, meskipun pembuatan sebagian thread mungkin
> berhasil. Demi kesederhanaan, perilaku ini tidak apa-apa, tetapi dalam
> implementasi *thread pool* produksi, kemungkinan besar Anda ingin memakai
> [`std::thread::Builder`][builder]<!-- ignore --> dan method
> [`spawn`][builder-spawn]<!-- ignore -->-nya yang mengembalikan `Result`.

Kode ini akan terkompilasi dan akan menyimpan jumlah instance `Worker`
yang kita tentukan sebagai argumen untuk `ThreadPool::new`. Tetapi kita
_masih_ belum memproses *closure* yang kita dapat di `execute`. Mari kita
lihat cara melakukannya berikutnya.

#### Mengirim Permintaan ke Thread melalui Channel

Masalah berikutnya yang akan kita tangani adalah *closure* yang diberikan ke
`thread::spawn` sama sekali tidak melakukan apa pun. Saat ini, kita
mendapatkan *closure* yang ingin kita eksekusi di method `execute`. Tetapi
kita perlu memberikan *closure* kepada `thread::spawn` untuk dijalankan saat
kita membuat setiap `Worker` selama pembuatan `ThreadPool`.

Kita ingin *struct* `Worker` yang baru kita buat mengambil kode yang akan
dijalankan dari antrean yang dipegang `ThreadPool` dan mengirim kode itu ke
thread-nya untuk dijalankan.

*Channel* yang kita pelajari di Bab 16—cara sederhana untuk berkomunikasi
antara dua thread—akan sempurna untuk kasus pemakaian ini. Kita akan
memakai *channel* untuk berfungsi sebagai antrean pekerjaan, dan `execute`
akan mengirim sebuah pekerjaan dari `ThreadPool` ke instance `Worker`,
yang akan mengirim pekerjaan itu ke thread-nya. Berikut rencananya:

1. `ThreadPool` akan membuat *channel* dan memegang pengirimnya.
2. Setiap `Worker` akan memegang penerimanya.
3. Kita akan membuat *struct* `Job` baru yang akan menampung *closure* yang
   ingin kita kirim melalui *channel*.
4. Method `execute` akan mengirim pekerjaan yang ingin ia eksekusi melalui
   pengirim.
5. Di thread-nya, `Worker` akan melakukan loop pada penerimanya dan
   mengeksekusi *closure* dari pekerjaan apa pun yang ia terima.

Mari kita mulai dengan membuat *channel* di `ThreadPool::new` dan memegang
pengirimnya di instance `ThreadPool`, seperti yang ditunjukkan di Listing
21-16. *Struct* `Job` tidak menampung apa pun untuk saat ini, tetapi ia akan
menjadi type item yang kita kirim melalui *channel*.

<Listing number="21-16" file-name="src/lib.rs" caption="Mengubah `ThreadPool` untuk menyimpan pengirim channel yang mentransmisikan instance `Job`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```

</Listing>

Di `ThreadPool::new`, kita membuat *channel* baru kita dan membuat pool itu
memegang pengirimnya. Ini akan terkompilasi dengan sukses.

Mari kita coba memberikan penerima *channel* itu ke setiap `Worker` saat
*thread pool* membuat *channel*-nya. Kita tahu kita ingin memakai penerima itu
di thread yang dibuat instance `Worker`, jadi kita akan mereferensikan
parameter `receiver` di *closure* itu. Kode di Listing 21-17 belum akan
terkompilasi.

<Listing number="21-17" file-name="src/lib.rs" caption="Memberikan penerima ke setiap `Worker`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```

</Listing>

Kita telah membuat beberapa perubahan kecil dan langsung: Kita memberikan
penerima itu ke `Worker::new`, lalu kita memakainya di dalam *closure*.

Ketika kita mencoba memeriksa kode ini, kita mendapat error ini:

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```

Kode itu sedang mencoba memberikan `receiver` ke banyak instance `Worker`.
Ini tidak akan bekerja, seperti yang Anda ingat dari Bab 16: Implementasi
*channel* yang disediakan Rust adalah banyak _produsen_, satu _konsumen_.
Ini berarti kita tidak bisa sekadar mengklon ujung konsumsi dari *channel*
untuk memperbaiki kode ini. Kita juga tidak ingin mengirim pesan berkali-
kali ke banyak konsumen; kita ingin satu daftar pesan dengan banyak
instance `Worker` sedemikian rupa sehingga setiap pesan diproses satu kali.

Selain itu, mengambil sebuah pekerjaan dari antrean *channel* melibatkan
pengubahan `receiver`, jadi thread-thread itu memerlukan cara yang aman
untuk berbagi dan mengubah `receiver`; jika tidak, kita mungkin mendapat
race condition (seperti yang dibahas di Bab 16).

Ingat kembali *smart pointer* yang thread-safe yang dibahas di Bab 16: Untuk
berbagi *ownership* lintas banyak thread dan memungkinkan thread-thread itu
mengubah nilainya, kita perlu memakai `Arc<Mutex<T>>`. Type `Arc` akan
memungkinkan banyak instance `Worker` memiliki *receiver*, dan `Mutex` akan
memastikan bahwa hanya satu `Worker` yang mendapat pekerjaan dari *receiver*
pada satu waktu. Listing 21-18 menunjukkan perubahan yang perlu kita buat.

<Listing number="21-18" file-name="src/lib.rs" caption="Berbagi receiver di antara instance `Worker` dengan memakai `Arc` dan `Mutex`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```

</Listing>

Di `ThreadPool::new`, kita meletakkan *receiver* di dalam `Arc` dan `Mutex`.
Untuk setiap `Worker` baru, kita mengklon `Arc` itu untuk menaikkan
hitungan *reference*nya supaya instance `Worker` bisa berbagi *ownership* atas
*receiver* itu.

Dengan perubahan ini, kodenya terkompilasi! Kita sudah hampir sampai!

#### Mengimplementasikan Method `execute`

Akhirnya, mari kita implementasikan method `execute` pada `ThreadPool`.
Kita juga akan mengubah `Job` dari *struct* menjadi type alias untuk *trait*
object yang menampung jenis *closure* yang diterima `execute`. Seperti yang
dibahas di seksi [“Sinonim Type dan Alias Type”][type-aliases]<!-- ignore -->
pada Bab 20, type alias memungkinkan kita memendekkan type yang panjang
demi kemudahan pemakaian. Lihat Listing 21-19.

<Listing number="21-19" file-name="src/lib.rs" caption="Membuat type alias `Job` untuk `Box` yang menampung setiap closure lalu mengirim pekerjaan itu melalui channel">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```

</Listing>

Setelah membuat instance `Job` baru dengan memakai *closure* yang kita dapat
di `execute`, kita mengirim pekerjaan itu melalui ujung pengiriman *channel*.
Kita memanggil `unwrap` pada `send` untuk kasus pengiriman gagal. Ini bisa
terjadi jika, misalnya, kita menghentikan semua thread kita dari
mengeksekusi, yang berarti ujung penerimaan berhenti menerima pesan baru.
Saat ini, kita tidak bisa menghentikan thread-thread kita dari
mengeksekusi: Thread-thread kita terus mengeksekusi selama pool itu ada.
Alasan kita memakai `unwrap` adalah kita tahu kasus kegagalan itu tidak
akan terjadi, tetapi *compiler* tidak mengetahuinya.

Tetapi kita belum selesai! Di `Worker`, *closure* yang kita berikan ke
`thread::spawn` masih hanya _mereferensikan_ ujung penerimaan *channel*.
Sebaliknya, kita perlu *closure* itu melakukan loop selamanya, meminta
pekerjaan dari ujung penerimaan *channel* dan menjalankan pekerjaan itu saat
ia mendapatkannya. Mari kita buat perubahan yang ditunjukkan di Listing
21-20 pada `Worker::new`.

<Listing number="21-20" file-name="src/lib.rs" caption="Menerima dan mengeksekusi pekerjaan-pekerjaan di thread instance `Worker`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```

</Listing>

Di sini, pertama-tama kita memanggil `lock` pada `receiver` untuk
memperoleh mutex-nya, lalu kita memanggil `unwrap` untuk panic pada error
apa pun. Memperoleh kunci bisa gagal jika mutex berada dalam keadaan
*poisoned* (teracuni), yang bisa terjadi jika thread lain panic saat masih
memegang kunci alih-alih melepaskan kuncinya. Dalam situasi ini, memanggil
`unwrap` untuk membuat thread ini panic adalah tindakan yang tepat.
Silakan mengubah `unwrap` ini menjadi `expect` dengan pesan error yang
bermakna bagi Anda.

Jika kita mendapatkan kunci pada mutex itu, kita memanggil `recv` untuk
menerima `Job` dari *channel*. `unwrap` terakhir melewati error apa pun di
sini juga, yang bisa terjadi jika thread yang memegang pengirim telah
berhenti, mirip dengan cara method `send` mengembalikan `Err` jika
penerimanya berhenti.

Pemanggilan `recv` memblokir, jadi jika belum ada pekerjaan, thread saat
ini akan menunggu sampai ada pekerjaan yang tersedia. `Mutex<T>` memastikan
bahwa hanya satu thread `Worker` pada satu waktu yang sedang mencoba
meminta pekerjaan.

*Thread pool* kita sekarang dalam keadaan bekerja! Jalankan `cargo run` dan
buat beberapa permintaan:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

Sukses! Sekarang kita punya *thread pool* yang mengeksekusi koneksi secara
asinkron. Tidak pernah ada lebih dari empat thread yang dibuat, jadi sistem
kita tidak akan kelebihan beban jika server menerima banyak permintaan.
Jika kita membuat permintaan ke _/sleep_, server akan bisa melayani
permintaan lain dengan meminta thread lain menjalankannya.

> Catatan: Jika Anda membuka _/sleep_ di banyak jendela peramban secara
> bersamaan, halaman-halaman itu mungkin dimuat satu per satu dengan jeda
> lima detik. Sebagian peramban web mengeksekusi banyak instance dari
> permintaan yang sama secara berurutan karena alasan caching. Batasan ini
> bukan disebabkan oleh server web kita.

Ini saat yang tepat untuk berhenti sejenak dan mempertimbangkan bagaimana
kode di Listing 21-18, 21-19, dan 21-20 akan berbeda jika kita memakai
*future* alih-alih *closure* untuk pekerjaan yang akan dilakukan. Type apa yang
akan berubah? Bagaimana *signature* methodnya akan berbeda, jika ada?
Bagian kode mana yang akan tetap sama?

Setelah mempelajari loop `while let` di Bab 17 dan Bab 19, Anda mungkin
bertanya-tanya mengapa kita tidak menulis kode thread `Worker` seperti yang
ditunjukkan di Listing 21-21.

<Listing number="21-21" file-name="src/lib.rs" caption="Implementasi alternatif `Worker::new` yang memakai `while let`">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```

</Listing>

Kode ini terkompilasi dan berjalan, tetapi tidak menghasilkan perilaku
threading yang diinginkan: Permintaan yang lambat tetap akan membuat
permintaan lain menunggu untuk diproses. Alasannya agak tidak kentara:
*Struct* `Mutex` tidak memiliki method `unlock` publik karena *ownership* atas
kuncinya didasarkan pada *lifetime* `MutexGuard<T>` di dalam
`LockResult<MutexGuard<T>>` yang dikembalikan method `lock`. Pada waktu
kompilasi, *borrow checker* kemudian bisa menegakkan aturan bahwa sumber
daya yang dijaga oleh `Mutex` tidak bisa diakses kecuali kita memegang
kuncinya. Akan tetapi, implementasi ini juga bisa mengakibatkan kuncinya
dipegang lebih lama daripada yang dimaksudkan jika kita tidak memerhatikan
*lifetime* `MutexGuard<T>` itu.

Kode di Listing 21-20 yang memakai `let job =
receiver.lock().unwrap().recv().unwrap();` bekerja karena dengan `let`,
nilai-nilai temporer apa pun yang dipakai di expression pada sisi kanan tanda
sama dengan segera dibebaskan saat statement `let` itu berakhir. Akan
tetapi, `while let` (dan `if let` dan `match`) tidak membebaskan nilai
temporer sampai akhir blok terkait. Di Listing 21-21, kuncinya tetap
dipegang selama pemanggilan `job()`, yang berarti instance `Worker` lain
tidak bisa menerima pekerjaan.

[type-aliases]: ch20-03-advanced-types.html#type-synonyms-and-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[moving-out-of-closures]: ch13-01-closures.html#moving-captured-values-out-of-closures
[builder]: ../std/thread/struct.Builder.html
[builder-spawn]: ../std/thread/struct.Builder.html#method.spawn
