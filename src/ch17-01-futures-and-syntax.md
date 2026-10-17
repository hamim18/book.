## Futures dan Sintaks Async

Elemen kunci dari pemrograman asinkron di Rust adalah _future_ dan kata kunci
`async` serta `await` dari Rust.

Sebuah _future_ adalah nilai yang mungkin belum siap sekarang, tetapi akan siap
pada suatu titik di masa depan. (Konsep yang sama ini muncul di banyak bahasa,
terkadang dengan nama lain seperti _task_ atau _promise_.) Rust menyediakan
trait `Future` sebagai batu penyusun supaya berbagai operasi async bisa
diimplementasikan dengan struktur data yang berbeda-beda, tetapi dengan
antarmuka yang sama. Di Rust, future adalah tipe yang mengimplementasikan trait
`Future`. Setiap future menyimpan informasinya sendiri tentang kemajuan yang
telah dibuat dan apa arti “siap”.

Anda bisa menerapkan kata kunci `async` pada blok dan fungsi untuk menentukan
bahwa keduanya bisa diinterupsi dan dilanjutkan kembali. Di dalam blok async
atau fungsi async, Anda bisa memakai kata kunci `await` untuk _menunggu sebuah
future_ (artinya, menunggu future itu menjadi siap). Setiap titik tempat Anda
menunggu sebuah future di dalam blok atau fungsi async adalah titik yang
berpotensi membuat blok atau fungsi tersebut berhenti sejenak dan dilanjutkan
kembali. Proses mengecek sebuah future untuk melihat apakah nilainya sudah
tersedia disebut _polling_.

Beberapa bahasa lain, seperti C# dan JavaScript, juga memakai kata kunci
`async` dan `await` untuk pemrograman asinkron. Jika Anda familier dengan
bahasa-bahasa itu, Anda mungkin akan melihat beberapa perbedaan yang cukup
besar dalam cara Rust menangani sintaks ini. Ada alasan kuat di baliknya,
seperti yang akan kita lihat nanti!

Saat menulis kode async di Rust, kita memakai kata kunci `async` dan `await`
hampir setiap saat. Rust mengompilasinya menjadi kode yang setara dengan
memakai trait `Future`, sebagaimana Rust mengompilasi perulangan `for` menjadi
kode yang setara dengan memakai trait `Iterator`. Akan tetapi, karena Rust
menyediakan trait `Future`, Anda juga bisa mengimplementasikannya untuk tipe
data Anda sendiri saat dibutuhkan. Banyak fungsi yang akan kita lihat di bab
ini mengembalikan tipe dengan implementasi `Future` mereka sendiri. Kita akan
kembali ke definisi trait itu di akhir bab dan menggali lebih dalam cara
kerjanya, tetapi detail sejauh ini sudah cukup untuk membuat kita terus
melaju.

Semua ini mungkin terasa agak abstrak, jadi mari kita tulis program async
pertama kita: sebuah _web scraper_ kecil. Kita akan meneruskan dua URL dari
baris perintah, mengambil keduanya secara konkuren, dan mengembalikan hasil
dari URL mana pun yang selesai lebih dulu. Contoh ini akan memuat cukup banyak
sintaks baru, tetapi jangan khawatir—kami akan menjelaskan semua yang perlu
Anda ketahui seiring kita berjalan.

## Program Async Pertama Kita

Untuk menjaga fokus bab ini pada mempelajari async alih-alih menyulap berbagai
bagian ekosistem, kami telah membuat crate `trpl` (`trpl` adalah singkatan dari
“The Rust Programming Language”). Crate ini mengekspor ulang semua tipe,
trait, dan fungsi yang Anda perlukan, terutama dari crate
[`futures`][futures-crate]<!-- ignore --> dan [`tokio`][tokio]<!-- ignore -->.
Crate `futures` adalah rumah resmi eksperimen Rust untuk kode async, dan
sebenarnya di situlah trait `Future` awalnya dirancang. Tokio adalah runtime
async yang paling banyak dipakai di Rust saat ini, terutama untuk aplikasi
web. Ada runtime-runtime hebat lain di luar sana, dan barangkali lebih cocok
untuk keperluan Anda. Kami memakai crate `tokio` di balik layar untuk `trpl`
karena crate ini teruji dengan baik dan dipakai secara luas.

Dalam beberapa kasus, `trpl` juga mengganti nama atau membungkus API aslinya
agar Anda tetap fokus pada detail yang relevan dengan bab ini. Jika Anda ingin
memahami apa yang dilakukan crate ini, kami menganjurkan Anda melihat [kode
sumbernya][crate-source]. Anda bisa melihat dari crate mana setiap
re-export berasal, dan kami telah meninggalkan komentar yang ekstensif untuk
menjelaskan apa yang dilakukan crate ini.

Buat proyek binary baru bernama `hello-async` dan tambahkan crate `trpl`
sebagai dependensi:

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

Sekarang kita bisa memakai berbagai bagian yang disediakan `trpl` untuk
menulis program async pertama kita. Kita akan membangun sebuah alat baris
perintah kecil yang mengambil dua halaman web, menarik elemen `<title>` dari
masing-masing halaman, dan mencetak judul dari halaman mana pun yang
menyelesaikan seluruh proses itu lebih dulu.

### Mendefinisikan Fungsi page_title

Mari mulai dengan menulis sebuah fungsi yang menerima satu URL halaman sebagai
parameter, membuat permintaan ke URL itu, dan mengembalikan teks dari elemen
`<title>` (lihat Listing 17-1).

<Listing number="17-1" file-name="src/main.rs" caption="Mendefinisikan sebuah fungsi async untuk mendapatkan elemen title dari sebuah halaman HTML">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

Pertama, kita mendefinisikan sebuah fungsi bernama `page_title` dan menandainya
dengan kata kunci `async`. Kemudian kita memakai fungsi `trpl::get` untuk
mengambil URL apa pun yang diteruskan, lalu menambahkan kata kunci `await`
untuk menunggu responsnya. Untuk mendapatkan teks dari `response`, kita
memanggil metode `text`-nya dan sekali lagi menunggunya dengan kata kunci
`await`. Kedua langkah ini asinkron. Untuk fungsi `get`, kita harus menunggu
server mengirim balik bagian pertama dari responsnya, yang akan mencakup
header HTTP, cookie, dan seterusnya, dan bisa dikirim terpisah dari badan
respons. Apalagi jika badannya sangat besar, semuanya bisa butuh waktu untuk
tiba. Karena kita harus menunggu _keseluruhan_ respons tiba, metode `text` juga
bersifat async.

Kita harus menunggu kedua future ini secara eksplisit, karena future di Rust
bersifat _lazy_: future tidak melakukan apa pun sampai Anda memintanya dengan
kata kunci `await`. (Bahkan, Rust akan menampilkan peringatan kompilator jika
Anda tidak memakai sebuah future.) Ini mungkin mengingatkan Anda pada
pembahasan iterator di bagian [“Memproses Serangkaian Item dengan
Iterator”][iterators-lazy]<!-- ignore --> di Bab 13. Iterator tidak melakukan
apa pun kecuali Anda memanggil metode `next`-nya—baik secara langsung maupun
dengan memakai perulangan `for` atau metode seperti `map` yang memakai `next`
di balik layar. Begitu pula, future tidak melakukan apa pun kecuali Anda
memintanya secara eksplisit. Sifat malas ini memungkinkan Rust menghindari
menjalankan kode async sampai kode itu benar-benar dibutuhkan.

> Catatan: Ini berbeda dari perilaku yang kita lihat saat memakai
> `thread::spawn` di bagian [“Membuat Thread Baru dengan `spawn`”][thread-spawn]<!-- ignore -->
> di Bab 16, tempat closure yang kita berikan kepada thread lain langsung
> mulai berjalan. Ini juga berbeda dari pendekatan banyak bahasa lain terhadap
> async. Namun, ini penting supaya Rust bisa memberikan jaminan performanya,
> sama seperti halnya iterator.

Setelah kita mendapatkan `response_text`, kita bisa melakukan parsing pada
teks itu menjadi sebuah instance bertipe `Html` dengan memakai `Html::parse`.
Alih-alih string mentah, sekarang kita punya tipe data yang bisa kita pakai
untuk mengolah HTML sebagai struktur data yang lebih kaya. Khususnya, kita
bisa memakai metode `select_first` untuk menemukan instance pertama dari
sebuah selector CSS tertentu. Dengan meneruskan string `"title"`, kita akan
mendapatkan elemen `<title>` pertama di dalam dokumen, jika ada. Karena
mungkin saja tidak ada elemen yang cocok, `select_first` mengembalikan sebuah
`Option<ElementRef>`. Terakhir, kita memakai metode `Option::map`, yang
memungkinkan kita mengolah item di dalam `Option` jika item itu ada, dan tidak
melakukan apa pun jika tidak ada. (Di sini kita juga bisa memakai ekspresi
`match`, tetapi `map` lebih idiomatis.) Di dalam badan fungsi yang kita
berikan kepada `map`, kita memanggil `inner_html` pada `title` untuk
mendapatkan isinya, yang berupa `String`. Pada akhirnya, kita memiliki sebuah
`Option<String>`.

Perhatikan bahwa kata kunci `await` dari Rust berada _setelah_ ekspresi yang
Anda tunggu, bukan sebelumnya. Artinya, kata kunci ini bersifat _postfix_. Ini
mungkin berbeda dari yang biasa Anda lihat jika Anda pernah memakai `async` di
bahasa lain, tetapi di Rust ini membuat rantai metode jauh lebih nyaman
dipakai. Hasilnya, kita bisa mengubah badan `page_title` untuk merantaikan
pemanggilan fungsi `trpl::get` dan `text` dengan `await` di antaranya, seperti
yang ditunjukkan di Listing 17-2.

<Listing number="17-2" file-name="src/main.rs" caption="Merantaikan dengan kata kunci `await`">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

Dengan itu, kita berhasil menulis fungsi async pertama kita! Sebelum
menambahkan beberapa kode di `main` untuk memanggilnya, mari kita bahas
sedikit lagi apa yang telah kita tulis dan apa artinya.

Ketika Rust melihat sebuah _blok_ yang ditandai dengan kata kunci `async`,
Rust mengompilasinya menjadi sebuah tipe data anonim yang unik yang
mengimplementasikan trait `Future`. Ketika Rust melihat sebuah _fungsi_ yang
ditandai dengan `async`, Rust mengompilasinya menjadi sebuah fungsi non-async
yang badannya adalah blok async. Tipe kembalian sebuah fungsi async adalah
tipe dari tipe data anonim yang dibuat kompilator untuk blok async tersebut.

Dengan demikian, menulis `async fn` setara dengan menulis sebuah fungsi yang
mengembalikan _future_ dari tipe kembaliannya. Bagi kompilator, definisi
fungsi seperti `async fn page_title` di Listing 17-1 kira-kira setara dengan
fungsi non-async yang didefinisikan seperti ini:

```rust
# extern crate trpl; // required for mdbook test
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

Mari kita telusuri setiap bagian dari versi yang ditransformasi ini:

- Kode ini memakai sintaks `impl Trait` yang kita bahas di Bab 10 pada bagian
  [“Memakai Trait sebagai Parameter”][impl-trait]<!-- ignore -->.
- Nilai yang dikembalikan mengimplementasikan trait `Future` dengan tipe
  asosiasi `Output`. Perhatikan bahwa tipe `Output`-nya adalah
  `Option<String>`, sama dengan tipe kembalian asli dari `page_title` versi
  `async fn`.
- Semua kode yang dipanggil di badan fungsi asli terbungkus di dalam blok
  `async move`. Ingat bahwa blok adalah ekspresi. Seluruh blok ini adalah
  ekspresi yang dikembalikan dari fungsi tersebut.
- Blok async ini menghasilkan sebuah nilai bertipe `Option<String>`, seperti
  yang baru saja dijelaskan. Nilai itu cocok dengan tipe `Output` pada tipe
  kembaliannya. Ini sama saja dengan blok-blok lain yang pernah Anda lihat.
- Badan fungsi yang baru adalah blok `async move` karena cara ia memakai
  parameter `url`. (Kita akan membahas lebih jauh tentang `async` versus
  `async move` nanti di bab ini.)

Sekarang kita bisa memanggil `page_title` di `main`.

<!-- Old headings. Do not remove or links may break. -->

<a id ="determining-a-single-pages-title"></a>

### Menjalankan Fungsi Async dengan Runtime

Untuk memulai, kita akan mendapatkan judul untuk satu halaman, seperti yang
ditunjukkan di Listing 17-3. Sayangnya, kode ini belum terkompilasi.

<Listing number="17-3" file-name="src/main.rs" caption="Memanggil fungsi `page_title` dari `main` dengan sebuah argumen dari pengguna">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

Kita mengikuti pola yang sama dengan yang kita pakai untuk mendapatkan
argumen baris perintah di bagian [“Menerima Argumen Baris
Perintah”][cli-args]<!-- ignore --> di Bab 12. Kemudian kita meneruskan argumen
URL itu ke `page_title` dan menunggu hasilnya. Karena nilai yang dihasilkan
future itu adalah `Option<String>`, kita memakai ekspresi `match` untuk
mencetak pesan yang berbeda sesuai ada atau tidaknya `<title>` di halaman
tersebut.

Satu-satunya tempat kita bisa memakai kata kunci `await` adalah di fungsi atau
blok async, dan Rust tidak mengizinkan kita menandai fungsi khusus `main`
sebagai `async`.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-03
cargo build
copy just the compiler error
-->

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

Alasan `main` tidak boleh ditandai `async` adalah karena kode async
membutuhkan sebuah _runtime_: sebuah crate Rust yang mengelola detail eksekusi
kode asinkron. Fungsi `main` sebuah program bisa _menginisialisasi_ sebuah
runtime, tetapi `main` bukanlah runtime _itu sendiri_. (Sebentar lagi kita
akan melihat lebih jauh alasan kondisi ini.) Setiap program Rust yang
menjalankan kode async punya setidaknya satu tempat yang menyiapkan runtime
untuk menjalankan future-future tersebut.

Kebanyakan bahasa yang mendukung async membundel sebuah runtime, tetapi Rust
tidak. Sebagai gantinya, tersedia banyak runtime async yang berbeda,
masing-masing dengan pilihan kompromi yang sesuai untuk kasus pemakaian yang
dibidiknya. Contohnya, sebuah server web berdaya tampung tinggi dengan banyak
inti CPU dan RAM besar punya kebutuhan yang sangat berbeda dari sebuah
mikrokontroler dengan satu inti, RAM kecil, dan tanpa kemampuan alokasi heap.
Crate-crate yang menyediakan runtime itu juga sering menyediakan versi async
dari fungsionalitas umum seperti I/O file atau jaringan.

Di sini, dan di sepanjang sisa bab ini, kita akan memakai fungsi `block_on`
dari crate `trpl`, yang menerima sebuah future sebagai argumen dan memblokir
thread saat ini sampai future itu berjalan tuntas. Di belakang layar,
pemanggilan `block_on` menyiapkan sebuah runtime memakai crate `tokio` yang
dipakai untuk menjalankan future yang diteruskan (perilaku `block_on` dari
crate `trpl` mirip dengan fungsi `block_on` dari crate-crate runtime lain).
Begitu future itu selesai, `block_on` mengembalikan nilai apa pun yang
dihasilkan future tersebut.

Kita bisa meneruskan future yang dikembalikan `page_title` langsung ke
`block_on` dan, begitu selesai, kita bisa melakukan `match` pada
`Option<String>` yang dihasilkan seperti yang kita coba lakukan di Listing
17-3. Akan tetapi, untuk sebagian besar contoh di bab ini (dan sebagian besar
kode async di dunia nyata), kita akan melakukan lebih dari sekadar satu
pemanggilan fungsi async, jadi sebagai gantinya kita akan meneruskan sebuah
blok `async` dan menunggu hasil pemanggilan `page_title` secara eksplisit,
seperti di Listing 17-4.

<Listing number="17-4" caption="Menunggu sebuah blok async dengan `trpl::block_on`" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

Ketika kita menjalankan kode ini, kita mendapatkan perilaku yang kita
harapkan sejak awal:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run -- "https://www.rust-lang.org"
# copy the output here
-->

```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

Fiuh—akhirnya kita punya kode async yang berfungsi! Namun, sebelum
menambahkan kode untuk mempertandingkan dua situs satu sama lain, mari kita
alihkan perhatian sejenak kembali ke cara kerja future.

Setiap _await point_—artinya, setiap tempat yang memakai kata kunci
`await`—merepresentasikan tempat kontrol diserahkan kembali ke runtime. Untuk
membuatnya bekerja, Rust perlu melacak state yang terlibat dalam blok async
sehingga runtime bisa memulai pekerjaan lain lalu kembali ketika siap mencoba
memajukan yang pertama lagi. Ini adalah state machine yang tak terlihat,
seolah-olah Anda menulis sebuah enum seperti ini untuk menyimpan state saat
ini di setiap await point:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

Akan tetapi, menulis kode transisi antar-state secara manual akan melelahkan
dan rawan galat, apalagi ketika nanti Anda perlu menambahkan fungsionalitas
dan state lain ke kode tersebut. Untungnya, kompilator Rust membuat dan
mengelola struktur data state machine untuk kode async secara otomatis. Aturan
peminjaman dan kepemilikan yang biasa pada struktur data tetap berlaku
seluruhnya, dan syukurlah, kompilator juga menangani pemeriksaannya untuk kita
serta memberikan pesan galat yang bermanfaat. Kita akan menelusuri beberapa di
antaranya nanti di bab ini.

Pada akhirnya, ada sesuatu yang harus menjalankan state machine ini, dan
sesuatu itu adalah runtime. (Inilah sebabnya Anda mungkin menemukan sebutan
_executor_ saat menelusuri runtime: executor adalah bagian runtime yang
bertanggung jawab menjalankan kode async.)

Sekarang Anda bisa melihat alasan kompilator menghentikan kita dari membuat
`main` menjadi fungsi async di Listing 17-3. Jika `main` adalah fungsi async,
harus ada hal lain yang mengelola state machine untuk future apa pun yang
dikembalikan `main`, padahal `main` adalah titik awal program! Sebagai
gantinya, kita memanggil fungsi `trpl::block_on` di `main` untuk menyiapkan
sebuah runtime dan menjalankan future yang dikembalikan blok `async` itu
sampai selesai.

> Catatan: Beberapa runtime menyediakan macro sehingga Anda _bisa_ menulis
> fungsi `main` yang async. Macro itu menulis ulang `async fn main() { ... }`
> menjadi `fn main` biasa, yang melakukan hal yang sama dengan yang kita
> lakukan secara manual di Listing 17-4: memanggil sebuah fungsi yang
> menjalankan future sampai tuntas sebagaimana `trpl::block_on`.

Sekarang mari kita rangkai semua bagian ini dan melihat bagaimana kita bisa
menulis kode konkuren.

<!-- Old headings. Do not remove or links may break. -->

<a id="racing-our-two-urls-against-each-other"></a>

### Mempertandingkan Dua URL Secara Konkuren

Di Listing 17-5, kita memanggil `page_title` dengan dua URL berbeda yang
diteruskan dari baris perintah dan mempertandingkannya dengan memilih future
mana pun yang selesai lebih dulu.

<Listing number="17-5" caption="Memanggil `page_title` untuk dua URL untuk melihat mana yang kembali lebih dulu" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

Kita mulai dengan memanggil `page_title` untuk setiap URL dari pengguna. Kita
menyimpan future yang dihasilkan sebagai `title_fut_1` dan `title_fut_2`.
Ingat, keduanya belum melakukan apa pun, karena future bersifat lazy dan kita
belum menunggunya. Kemudian kita meneruskan kedua future itu ke `trpl::select`,
yang mengembalikan sebuah nilai untuk menunjukkan mana di antara future yang
diteruskan padanya yang selesai lebih dulu.

> Catatan: Di balik layar, `trpl::select` dibangun di atas fungsi `select`
> yang lebih umum yang didefinisikan di crate `futures`. Fungsi `select` dari
> crate `futures` bisa melakukan banyak hal yang tidak bisa dilakukan fungsi
> `trpl::select`, tetapi fungsi itu juga punya kerumitan tambahan yang bisa
> kita lewati untuk saat ini.

Future mana pun bisa “menang” secara sah, jadi tidak masuk akal untuk
mengembalikan `Result`. Sebagai gantinya, `trpl::select` mengembalikan tipe
yang belum pernah kita lihat, `trpl::Either`. Tipe `Either` agak mirip
`Result` karena sama-sama punya dua kasus. Namun, tidak seperti `Result`,
tidak ada gagasan sukses atau gagal yang tertanam di dalam `Either`.
Sebaliknya, tipe ini memakai `Left` dan `Right` untuk menunjukkan “salah satu
atau yang lain”:

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

Fungsi `select` mengembalikan `Left` beserta output future pertama jika
argumen pertama menang, dan `Right` beserta output argumen future kedua jika
future _itu_ yang menang. Ini cocok dengan urutan argumen saat pemanggilan
fungsi: argumen pertama berada di kiri argumen kedua.

Kita juga memperbarui `page_title` untuk mengembalikan URL yang sama dengan
yang diteruskan. Dengan begitu, jika halaman yang kembali lebih dulu tidak
memiliki `<title>` yang bisa kita olah, kita tetap bisa mencetak pesan yang
bermakna. Dengan informasi itu tersedia, kita menutupnya dengan memperbarui
output `println!` kita untuk menunjukkan URL mana yang selesai lebih dulu dan
apa `<title>` halaman web di URL itu, jika ada.

Sekarang Anda telah membangun sebuah web scraper kecil yang berfungsi! Pilih
beberapa URL dan jalankan alat baris perintah itu. Anda mungkin menemukan
bahwa beberapa situs secara konsisten lebih cepat daripada yang lain, sementara
di kasus lain situs yang lebih cepat berubah-ubah dari satu kali jalankan ke
jalankan berikutnya. Yang lebih penting, Anda telah mempelajari dasar-dasar
bekerja dengan future, jadi sekarang kita bisa menggali lebih dalam apa yang
bisa kita lakukan dengan async.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs
