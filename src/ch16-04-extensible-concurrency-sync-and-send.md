<!-- Old headings. Do not remove or links may break. -->

<a id="extensible-concurrency-with-the-sync-and-send-traits"></a>
<a id="extensible-concurrency-with-the-send-and-sync-traits"></a>

## Concurrency yang Dapat Diperluas dengan `Send` dan `Sync`

Menariknya, hampir semua fitur concurrency yang sejauh ini kita bicarakan di
bab ini merupakan bagian dari standard library, bukan bahasa. Pilihan Anda
untuk menangani concurrency tidak terbatas pada bahasa atau standard library;
Anda dapat menulis fitur concurrency Anda sendiri atau memakai yang ditulis
orang lain.

Namun, di antara konsep-konsep concurrency kunci yang tertanam di dalam bahasa
alih-alih standard library adalah *trait* `std::marker` `Send` dan `Sync`.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-transference-of-ownership-between-threads-with-send"></a>

### Mentransfer Ownership Antar-Thread

*Marker trait* (*trait* penanda) `Send` menunjukkan bahwa *ownership* nilai
typed yang mengimplementasikan `Send` dapat ditransfer antar-thread. Hampir
semua type Rust mengimplementasikan `Send`, tetapi ada beberapa pengecualian,
termasuk `Rc<T>`: Type ini tidak dapat mengimplementasikan `Send` karena jika
Anda mengklon nilai `Rc<T>` dan mencoba mentransfer *ownership* klon itu ke
thread lain, kedua thread mungkin memperbarui jumlah *reference* pada saat yang
sama. Karena alasan ini, `Rc<T>` diimplementasikan untuk dipakai dalam
situasi single-threaded ketika Anda tidak ingin membayar performance penalty
thread-safe.

Karena itu, type system dan *trait bound* Rust memastikan bahwa Anda tidak
pernah bisa tanpa sengaja mengirim nilai `Rc<T>` lintas thread secara tidak
aman. Ketika kita mencoba melakukan ini di Listing 16-14, kita mendapat error
`` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``. Ketika kita
beralih ke `Arc<T>`, yang memang mengimplementasikan `Send`, kodenya
terkompilasi.

Type apa pun yang tersusun seluruhnya dari type `Send` otomatis ditandai
sebagai `Send` juga. Hampir semua primitive type bersifat `Send`, kecuali raw
*pointer*, yang akan kita bahas di Bab 20.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-access-from-multiple-threads-with-sync"></a>

### Mengakses dari Banyak Thread

*Marker trait* `Sync` menunjukkan bahwa aman bagi type yang
mengimplementasikan `Sync` untuk dirujuk dari banyak thread. Dengan kata lain,
type `T` mana pun mengimplementasikan `Sync` jika `&T` (*immutable* *reference* ke
`T`) mengimplementasikan `Send`, yang berarti *reference* itu dapat dikirim
dengan aman ke thread lain. Serupa dengan `Send`, semua primitive type
mengimplementasikan `Sync`, dan type yang tersusun seluruhnya dari type yang
mengimplementasikan `Sync` juga mengimplementasikan `Sync`.

*Smart pointer* `Rc<T>` juga tidak mengimplementasikan `Sync` karena alasan yang
sama dengan alasan ia tidak mengimplementasikan `Send`. Type `RefCell<T>`
(yang kita bicarakan di Bab 15) dan keluarga type `Cell<T>` yang terkait tidak
mengimplementasikan `Sync`. Implementasi pemeriksaan *borrowing* yang dilakukan
`RefCell<T>` pada runtime tidak thread-safe. *Smart pointer* `Mutex<T>`
mengimplementasikan `Sync` dan dapat dipakai untuk berbagi akses dengan
beberapa thread, seperti yang Anda lihat di [“Akses Bersama ke
`Mutex<T>`”][shared-access]<!-- ignore -->.

### Mengimplementasikan `Send` dan `Sync` Secara Manual Itu Unsafe

Karena type yang tersusun seluruhnya dari type lain yang mengimplementasikan
*trait* `Send` dan `Sync` juga otomatis mengimplementasikan `Send` dan `Sync`,
kita tidak harus mengimplementasikan *trait*-trait itu secara manual. Sebagai
*marker trait*, keduanya bahkan tidak memiliki method untuk diimplementasikan.
Keduanya hanya berguna untuk menegakkan invarian yang terkait dengan
concurrency.

Mengimplementasikan *trait*-trait ini secara manual melibatkan penulisan kode
Rust *unsafe*. Kita akan membahas pemakaian kode Rust *unsafe* di Bab 20; untuk
sekarang, informasi pentingnya adalah bahwa membangun type concurrent baru yang
tidak tersusun dari bagian-bagian `Send` dan `Sync` menuntut pemikiran yang
cermat untuk menegakkan jaminan keamanan. [“The Rustonomicon”][nomicon]
memiliki informasi lebih lanjut tentang jaminan ini dan cara menegakkannya.

## Ringkasan

Ini bukan terakhir kalinya Anda melihat concurrency di buku ini: Bab berikutnya
berfokus pada pemrograman async, dan proyek di Bab 21 akan memakai
konsep-konsep di bab ini dalam situasi yang lebih realistis daripada
contoh-contoh kecil yang dibahas di sini.

Seperti disebutkan sebelumnya, karena sangat sedikit dari cara Rust menangani
concurrency yang merupakan bagian dari bahasa, banyak solusi concurrency
diimplementasikan sebagai *crate*. Solusi-solusi itu berevolusi lebih cepat
daripada standard library, jadi pastikan untuk mencari *crate* terkini yang
mutakhir secara daring untuk dipakai dalam situasi multithreaded.

Pustaka standar Rust menyediakan *channel* untuk *message passing* dan type smart
*pointer*, seperti `Mutex<T>` dan `Arc<T>`, yang aman dipakai dalam konteks
concurrent. Sistem type dan *borrow checker* memastikan bahwa kode yang memakai
solusi-solusi ini tidak akan berakhir dengan data race atau *reference* yang
tidak valid. Begitu kode Anda terkompilasi, Anda bisa yakin bahwa kode itu
akan berjalan dengan senang hati di banyak thread tanpa jenis-jenis bug yang
sulit dilacak seperti yang umum di bahasa lain. Pemrograman concurrent bukan
lagi konsep yang perlu ditakuti: Majulah dan buat program Anda concurrent,
tanpa takut!

[shared-access]: ch16-03-shared-state.html#shared-access-to-mutext
[nomicon]: ../nomicon/index.html
