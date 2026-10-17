## Penghentian yang Rapi dan Pembersihan

Kode di Listing 21-20 merespons permintaan secara asinkron melalui
pemakaian *thread pool*, seperti yang kita maksudkan. Kita mendapat beberapa
peringatan tentang *field* `workers`, `id`, dan `thread` yang tidak kita
pakai secara langsung yang mengingatkan kita bahwa kita belum membersihkan
apa pun. Saat kita memakai metode <kbd>ctrl</kbd>-<kbd>C</kbd> yang kurang
elegan untuk menghentikan thread utama, semua thread lain juga langsung
dihentikan, bahkan jika mereka sedang berada di tengah-tengah melayani
sebuah permintaan.

Maka, berikutnya kita akan mengimplementasikan *trait* `Drop` untuk memanggil
`join` pada setiap thread di pool supaya mereka bisa menyelesaikan
permintaan yang sedang mereka kerjakan sebelum menutup. Lalu, kita akan
mengimplementasikan cara untuk memberi tahu thread-thread itu bahwa mereka
harus berhenti menerima permintaan baru dan menghentikan diri. Untuk
melihat kode ini bekerja, kita akan mengubah server kita untuk hanya
menerima dua permintaan sebelum menghentikan *thread pool*-nya dengan rapi.

Satu hal yang perlu diperhatikan selama kita melakukannya: Tidak satu pun
dari ini memengaruhi bagian kode yang menangani eksekusi *closure*, jadi
semua yang ada di sini akan sama jika kita memakai *thread pool* untuk
runtime async.

### Mengimplementasikan Trait `Drop` pada `ThreadPool`

Mari kita mulai dengan mengimplementasikan `Drop` pada *thread pool* kita.
Ketika pool itu dibebaskan, thread-thread kita seharusnya semuanya melakukan
join untuk memastikan mereka menyelesaikan pekerjaan mereka. Listing 21-22
menunjukkan percobaan pertama implementasi `Drop`; kode ini belum akan
bekerja.

<Listing number="21-22" file-name="src/lib.rs" caption="Melakukan join pada setiap thread ketika thread pool keluar dari scope">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

Pertama, kita melakukan loop melalui setiap `workers` pada *thread pool*.
Kita memakai `&mut` untuk ini karena `self` adalah *reference* *mutable*, dan
kita juga perlu bisa mengubah `worker`. Untuk setiap `worker`, kita
mencetak pesan yang menyatakan bahwa instance `Worker` tertentu ini sedang
menghentikan diri, lalu kita memanggil `join` pada thread instance
`Worker` itu. Jika pemanggilan `join` gagal, kita memakai `unwrap` untuk
membuat Rust panic dan melakukan penghentian yang tidak rapi.

Berikut galat yang kita dapat saat mengompilasi kode ini:

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

Galat itu memberi tahu kita bahwa kita tidak bisa memanggil `join` karena
kita hanya punya peminjaman *mutable* untuk setiap `worker` dan `join`
mengambil *ownership* atas argumennya. Untuk menyelesaikan masalah ini, kita
perlu memindahkan thread keluar dari instance `Worker` yang memiliki
`thread` supaya `join` bisa mengonsumsi thread itu. Salah satu caranya
adalah mengambil pendekatan yang sama seperti yang kita ambil di Listing
18-15. Jika `Worker` menampung `Option<thread::JoinHandle<()>>`, kita bisa
memanggil metode `take` pada `Option` itu untuk memindahkan nilainya keluar
dari varian `Some` dan meninggalkan varian `None` di tempatnya. Dengan kata
lain, `Worker` yang sedang berjalan akan memiliki varian `Some` di
`thread`, dan saat kita ingin membersihkan `Worker`, kita mengganti `Some`
dengan `None` supaya `Worker` itu tidak memiliki thread untuk dijalankan.

Akan tetapi, satu-satunya saat hal ini muncul hanyalah ketika membebaskan
`Worker`. Sebagai imbalannya, kita harus berurusan dengan
`Option<thread::JoinHandle<()>>` di mana pun kita mengakses
`worker.thread`. Rust yang idiomatis memang cukup sering memakai `Option`,
tetapi ketika Anda mendapati diri Anda membungkus sesuatu yang Anda tahu
pasti selalu ada di dalam `Option` sebagai jalan keluar seperti ini, ada
baiknya mencari pendekatan alternatif untuk membuat kode Anda lebih bersih
dan tidak terlalu rawan galat.

Dalam kasus ini, ada alternatif yang lebih baik: metode `Vec::drain`.
Metode ini menerima parameter range untuk menentukan item-item mana yang
akan dihapus dari vektor dan mengembalikan *iterator* berisi item-item itu.
Memberikan sintaks range `..` akan menghapus *semua* nilai dari vektor.

Jadi, kita perlu memperbarui implementasi `drop` pada `ThreadPool` menjadi
seperti ini:

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

Ini menyelesaikan galat kompilator dan tidak memerlukan perubahan lain
pada kode kita. Perhatikan bahwa, karena drop bisa dipanggil saat sedang
panic, unwrap itu juga bisa panic dan menyebabkan panic ganda, yang
langsung membuat program crash dan mengakhiri pembersihan apa pun yang
sedang berlangsung. Ini tidak apa-apa untuk program contoh, tetapi tidak
direkomendasikan untuk kode produksi.

### Memberi Sinyal kepada Thread untuk Berhenti Mendengarkan Pekerjaan

Dengan semua perubahan yang kita buat, kode kita terkompilasi tanpa
peringatan apa pun. Akan tetapi, kabar buruknya adalah kode ini belum
berfungsi seperti yang kita inginkan. Kuncinya adalah logika di *closure*
yang dijalankan oleh thread-thread dari instance `Worker`: Saat ini, kita
memanggil `join`, tetapi itu tidak akan menghentikan thread-thread itu,
karena mereka melakukan `loop` selamanya mencari pekerjaan. Jika kita
mencoba membebaskan `ThreadPool` kita dengan implementasi `drop` saat ini,
thread utama akan memblokir selamanya, menunggu thread pertama selesai.

Untuk memperbaiki masalah ini, kita perlu mengubah implementasi `drop` pada
`ThreadPool` lalu mengubah loop `Worker`.

Pertama, kita akan mengubah implementasi `drop` pada `ThreadPool` untuk
membebaskan `sender` secara eksplisit sebelum menunggu thread-thread
selesai. Listing 21-23 menunjukkan perubahan pada `ThreadPool` untuk
membebaskan `sender` secara eksplisit. Tidak seperti dengan thread, di sini
kita *memang* perlu memakai `Option` untuk bisa memindahkan `sender` keluar
dari `ThreadPool` dengan `Option::take`.

<Listing number="21-23" file-name="src/lib.rs" caption="Membebaskan `sender` secara eksplisit sebelum melakukan join pada thread `Worker`">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

Membebaskan `sender` menutup *channel*, yang menandakan bahwa tidak akan ada
lagi pesan yang dikirim. Ketika itu terjadi, semua pemanggilan `recv` yang
dilakukan instance `Worker` di loop tak berujung itu akan mengembalikan
galat. Di Listing 21-24, kita mengubah loop `Worker` untuk keluar dari loop
dengan rapi pada kasus itu, yang berarti thread-thread itu akan selesai
saat implementasi `drop` pada `ThreadPool` memanggil `join` pada mereka.

<Listing number="21-24" file-name="src/lib.rs" caption="Keluar dari loop secara eksplisit ketika `recv` mengembalikan galat">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

Untuk melihat kode ini bekerja, mari kita ubah `main` untuk hanya menerima
dua permintaan sebelum menghentikan server dengan rapi, seperti yang
ditunjukkan di Listing 21-25.

<Listing number="21-25" file-name="src/main.rs" caption="Menghentikan server setelah melayani dua permintaan dengan keluar dari loop">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

Anda tidak akan ingin server web di dunia nyata berhenti setelah melayani
hanya dua permintaan. Kode ini hanya menunjukkan bahwa penghentian yang
rapi dan pembersihannya bekerja dengan baik.

Metode `take` didefinisikan di *trait* `Iterator` dan membatasi iterasi
paling banyak ke dua item pertama. `ThreadPool` akan keluar dari *scope* di
akhir `main`, dan implementasi `drop` akan berjalan.

Mulai server dengan `cargo run` dan buat tiga permintaan. Permintaan ketiga
seharusnya galat, dan di terminal Anda, Anda seharusnya melihat output yang
mirip dengan ini:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-25
cargo run
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
third request will error because server will have shut down
copy output below
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

Anda mungkin melihat urutan ID `Worker` dan pesan yang berbeda. Kita bisa
melihat bagaimana kode ini bekerja dari pesan-pesannya: Instance `Worker` 0
dan 3 mendapat dua permintaan pertama. Server berhenti menerima koneksi
setelah koneksi kedua, dan implementasi `Drop` pada `ThreadPool` mulai
dieksekusi bahkan sebelum `Worker 3` memulai pekerjaannya. Membebaskan
`sender` memutuskan semua instance `Worker` dan memberi tahu mereka untuk
menghentikan diri. Setiap instance `Worker` mencetak pesan saat mereka
terputus, lalu *thread pool* memanggil `join` untuk menunggu setiap thread
`Worker` selesai.

Perhatikan satu aspek menarik dari eksekusi khusus ini: `ThreadPool`
membebaskan `sender`, dan sebelum ada `Worker` yang menerima galat, kita
mencoba melakukan join pada `Worker 0`. `Worker 0` belum mendapat galat
dari `recv`, jadi thread utama memblokir, menunggu `Worker 0` selesai.
Sementara itu, `Worker 3` menerima pekerjaan lalu semua thread menerima
galat. Ketika `Worker 0` selesai, thread utama menunggu sisa instance
`Worker` untuk selesai. Pada titik itu, mereka semua telah keluar dari
loop-nya dan berhenti.

Selamat! Sekarang kita telah menyelesaikan proyek kita; kita punya server
web dasar yang memakai *thread pool* untuk merespons secara asinkron. Kita
bisa melakukan penghentian server yang rapi, yang membersihkan semua thread
di pool.

Berikut kode lengkapnya sebagai rujukan:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/main.rs}}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/lib.rs}}
```

</Listing>

Kita masih bisa melakukan lebih banyak hal di sini! Jika Anda ingin terus
menyempurnakan proyek ini, berikut beberapa gagasan:

- Menambahkan lebih banyak dokumentasi ke `ThreadPool` dan metode-metode
  publiknya.
- Menambahkan pengujian untuk fungsionalitas library itu.
- Mengubah pemanggilan `unwrap` menjadi penanganan galat yang lebih
  tangguh.
- Memakai `ThreadPool` untuk melakukan tugas lain selain melayani
  permintaan web.
- Menemukan *crate* *thread pool* di [crates.io](https://crates.io/)<!-- ignore -->
  dan mengimplementasikan server web yang serupa dengan memakai *crate* itu.
  Lalu, bandingkan API dan ketangguhannya dengan *thread pool* yang kita
  implementasikan.

## Ringkasan

Kerja bagus! Anda telah sampai di akhir buku! Kami ingin berterima kasih
karena telah bergabung dengan kita dalam tur Rust ini. Anda sekarang siap
untuk mengimplementasikan proyek-proyek Rust Anda sendiri dan membantu
proyek orang lain. Ingatlah bahwa ada komunitas Rustacean lain yang ramah
yang akan senang membantu Anda menghadapi tantangan apa pun yang Anda temui
dalam perjalanan Rust Anda.
