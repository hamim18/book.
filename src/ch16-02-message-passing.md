<!-- Old headings. Do not remove or links may break. -->

<a id="using-message-passing-to-transfer-data-between-threads"></a>

## Mentransfer Data Antar-Thread dengan Message Passing

Salah satu pendekatan yang semakin populer untuk menjamin concurrency yang aman
adalah *message passing* (message passing), ketika thread atau aktor
berkomunikasi dengan saling mengirim pesan yang memuat data. Berikut gagasan
itu dalam sebuah slogan dari [dokumentasi bahasa Go](https://golang.org/doc/effective_go.html#concurrency):
“Do not communicate by sharing memory; instead, share memory by communicating.”

Untuk mewujudkan concurrency message passing, standard library Rust menyediakan
implementasi *channel*. Sebuah _channel_ (*channel*) adalah konsep pemrograman
umum untuk mengirim data dari satu thread ke thread lain.

Anda dapat membayangkan *channel* dalam pemrograman seperti *channel* air
berarah, misalnya anak sungai atau sungai. Jika Anda meletakkan sesuatu
seperti bebek karet ke sebuah sungai, benda itu akan hanyut ke hilir sampai
ujung aliran air.

Sebuah *channel* memiliki dua bagian: *transmitter* dan *receiver*. Bagian
*transmitter* adalah lokasi di hulu tempat Anda meletakkan bebek karet ke
sungai, dan bagian *receiver* adalah tempat bebek karet itu berakhir di hilir.
Satu bagian kode Anda memanggil method pada *transmitter* dengan data yang ingin
Anda kirim, dan bagian lain memeriksa ujung *receiver* untuk pesan yang datang.
Sebuah *channel* dikatakan _closed_ (tertutup) jika bagian *transmitter* atau
*receiver*-nya dibebaskan.

Di sini, kita akan menyusun program yang memiliki satu thread untuk
menghasilkan nilai dan mengirimkannya lewat sebuah *channel*, serta thread lain
yang akan menerima nilai-nilai itu dan mencetaknya. Kita akan mengirim nilai
sederhana antar-thread memakai *channel* untuk menggambarkan fiturnya. Begitu
Anda terbiasa dengan teknik ini, Anda dapat memakai *channel* untuk thread mana
pun yang perlu saling berkomunikasi, seperti sistem obrolan atau sistem ketika
banyak thread mengerjakan bagian-bagian sebuah perhitungan dan mengirim
bagian-bagian itu ke satu thread yang menggabungkan hasilnya.

Pertama, di Listing 16-6, kita akan membuat *channel* tetapi tidak melakukan
apa pun dengannya. Perhatikan bahwa ini belum akan terkompilasi karena Rust
tidak bisa tahu type nilai apa yang ingin kita kirim melalui *channel* itu.

<Listing number="16-6" file-name="src/main.rs" caption="Membuat channel dan menetapkan kedua bagiannya ke `tx` dan `rx`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-06/src/main.rs}}
```

</Listing>

Kita membuat *channel* baru menggunakan fungsi `mpsc::channel`; `mpsc` adalah
singkatan dari _multiple producer, single consumer_ (banyak produsen, satu
konsumen). Singkatnya, cara standard library Rust mengimplementasikan *channel*
berarti sebuah *channel* dapat memiliki beberapa ujung _pengirim_ yang
menghasilkan nilai tetapi hanya satu ujung _penerima_ yang mengonsumsi
nilai-nilai itu. Bayangkan beberapa anak sungai mengalir bersama menjadi satu
sungai besar: Semua yang dikirim melalui anak sungai mana pun akan berakhir di
satu sungai di ujungnya. Untuk sekarang kita akan mulai dengan satu produsen,
tetapi kita akan menambahkan banyak produsen ketika contoh ini sudah
berfungsi.

Fungsi `mpsc::channel` mengembalikan sebuah *tuple*, elemen pertamanya adalah
ujung *transmitter*—*transmitter*—dan elemen keduanya adalah ujung *receiver*—*receiver*.
Singkatan `tx` dan `rx` secara tradisional dipakai di banyak bidang untuk
_transmitter_ (*transmitter*) dan _receiver_ (*receiver*), jadi kita menamai variable
kita seperti itu untuk menandai masing-masing ujung. Kita memakai statement
`let` dengan pattern yang mendestrukturisasi *tuple*; kita akan membahas pemakaian
pattern dalam statement `let` dan destrukturisasi di Bab 19. Untuk sekarang,
cukup ketahui bahwa memakai statement `let` dengan cara ini adalah pendekatan
praktis untuk mengekstrak bagian-bagian *tuple* yang dikembalikan
`mpsc::channel`.

Mari kita pindahkan ujung *transmitter* ke thread yang dibuat dan menyuruhnya
mengirim satu string supaya thread yang dibuat itu berkomunikasi dengan thread
utama, seperti ditunjukkan pada Listing 16-7. Ini seperti meletakkan bebek
karet di hulu sungai atau mengirim pesan obrolan dari satu thread ke thread
lain.

<Listing number="16-7" file-name="src/main.rs" caption='Memindahkan `tx` ke thread yang dibuat dan mengirim `"hi"`'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-07/src/main.rs}}
```

</Listing>

Sekali lagi, kita memakai `thread::spawn` untuk membuat thread baru, lalu
memakai `move` untuk memindahkan `tx` ke *closure* supaya thread yang dibuat
memiliki `tx`. Thread yang dibuat perlu memiliki *transmitter* untuk bisa
mengirim pesan melalui *channel*.

*Transmitter* memiliki method `send` yang menerima nilai yang ingin kita kirim.
Method `send` mengembalikan type `Result<T, E>`, jadi jika *receiver* telah
dibebaskan dan tidak ada tempat untuk mengirim nilai, operasi pengiriman akan
mengembalikan error. Dalam contoh ini, kita memanggil `unwrap` untuk panic
jika terjadi error. Tetapi dalam aplikasi nyata, kita akan menanganinya dengan
benar: Kembalilah ke Bab 9 untuk mengulas strategi penanganan error yang
tepat.

Di Listing 16-8, kita akan mengambil nilai dari *receiver* di thread utama. Ini
seperti mengambil bebek karet dari air di ujung sungai atau menerima pesan
obrolan.

<Listing number="16-8" file-name="src/main.rs" caption='Menerima nilai `"hi"` di thread utama dan mencetaknya'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-08/src/main.rs}}
```

</Listing>

*Receiver* memiliki dua method yang berguna: `recv` dan `try_recv`. Kita
memakai `recv`, singkatan dari _receive_ (menerima), yang akan memblokir
eksekusi thread utama dan menunggu sampai sebuah nilai dikirim melalui
*channel*. Begitu sebuah nilai terkirim, `recv` akan mengembalikannya dalam
`Result<T, E>`. Ketika *transmitter* tertutup, `recv` akan mengembalikan error
untuk menandakan bahwa tidak akan ada nilai lagi yang datang.

Method `try_recv` tidak memblokir, tetapi langsung mengembalikan
`Result<T, E>`: nilai `Ok` yang menampung pesan jika ada yang tersedia dan
nilai `Err` jika kali ini tidak ada pesan. Memakai `try_recv` berguna jika
thread ini memiliki pekerjaan lain selagi menunggu pesan: Kita bisa menulis
loop yang memanggil `try_recv` sesekali, menangani pesan jika ada, dan
selain itu mengerjakan pekerjaan lain sebentar sampai memeriksa lagi.

Kita memakai `recv` di contoh ini demi kesederhanaan; kita tidak punya
pekerjaan lain untuk thread utama selain menunggu pesan, jadi memblokir
thread utama adalah pilihan yang tepat.

Ketika kita menjalankan kode di Listing 16-8, kita akan melihat nilai yang
dicetak dari thread utama:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
```

Sempurna!

<!-- Old headings. Do not remove or links may break. -->

<a id="channels-and-ownership-transference"></a>

### Mentransfer Ownership Melalui Channel

Aturan *ownership* memainkan peran penting dalam message passing karena
aturan itu membantu Anda menulis kode concurrent yang aman. Mencegah error
dalam concurrent programming adalah keuntungan memikirkan *ownership* di seluruh
program Rust Anda. Mari kita lakukan eksperimen untuk menunjukkan bagaimana
*channel* dan *ownership* bekerja sama mencegah masalah: Kita akan mencoba memakai
nilai `val` di thread yang dibuat _setelah_ kita mengirimkannya melalui
*channel*. Coba kompilasi kode di Listing 16-9 untuk melihat mengapa kode ini
tidak diizinkan.

<Listing number="16-9" file-name="src/main.rs" caption="Mencoba memakai `val` setelah kita mengirimkannya melalui channel">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-09/src/main.rs}}
```

</Listing>

Di sini, kita mencoba mencetak `val` setelah mengirimkannya melalui *channel*
lewat `tx.send`. Mengizinkan hal ini adalah ide yang buruk: Begitu nilai itu
dikirim ke thread lain, thread itu bisa memodifikasi atau membebaskannya
sebelum kita mencoba memakai nilai itu lagi. Berpotensi, modifikasi thread
lain itu bisa menyebabkan error atau hasil yang tidak terduga karena data yang
tidak konsisten atau tidak ada. Namun, Rust memberi kita error jika kita
mencoba mengompilasi kode di Listing 16-9:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-09/output.txt}}
```

Kesalahan concurrency kita telah menyebabkan error waktu kompilasi. Fungsi
`send` mengambil *ownership* atas parameternya, dan ketika nilainya dipindahkan,
*receiver* mengambil *ownership* atasnya. Ini mencegah kita tanpa sengaja memakai
nilai itu lagi setelah mengirimkannya; sistem *ownership* memeriksa bahwa
semuanya baik-baik saja.

<!-- Old headings. Do not remove or links may break. -->

<a id="sending-multiple-values-and-seeing-the-receiver-waiting"></a>

### Mengirim Banyak Nilai

Kode di Listing 16-8 terkompilasi dan berjalan, tetapi kode itu tidak
menunjukkan dengan jelas kepada kita bahwa dua thread terpisah sedang saling
berbicara melalui *channel*.

Di Listing 16-10, kita telah membuat beberapa modifikasi yang akan
membuktikan bahwa kode di Listing 16-8 berjalan secara concurrent: Thread yang
dibuat sekarang akan mengirim banyak pesan dan berhenti sejenak selama satu
detik di antara setiap pesan.

<Listing number="16-10" file-name="src/main.rs" caption="Mengirim banyak pesan dan berhenti sejenak di antara setiap pesan">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-10/src/main.rs}}
```

</Listing>

Kali ini, thread yang dibuat memiliki vector berisi string yang ingin kita
kirim ke thread utama. Kita mengiterasinya, mengirim masing-masing satu per
satu, dan berhenti sejenak di antara setiap pengiriman dengan memanggil fungsi
`thread::sleep` dengan nilai `Duration` satu detik.

Di thread utama, kita tidak lagi memanggil fungsi `recv` secara eksplisit:
Sebagai gantinya, kita memperlakukan `rx` sebagai *iterator*. Untuk setiap nilai
yang diterima, kita mencetaknya. Ketika *channel* tertutup, iterasi akan
berakhir.

Ketika menjalankan kode di Listing 16-10, Anda seharusnya melihat output
berikut dengan jeda satu detik di antara setiap baris:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: from
Got: the
Got: thread
```

Karena kita tidak memiliki kode yang berhenti atau menunda di loop `for`
di thread utama, kita dapat memastikan bahwa thread utama sedang menunggu
untuk menerima nilai dari thread yang dibuat.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-multiple-producers-by-cloning-the-transmitter"></a>

### Membuat Banyak Produsen

Sebelumnya kita menyebutkan bahwa `mpsc` adalah akronim dari _multiple
producer, single consumer_. Mari kita pakai `mpsc` dan perluas kode di Listing
16-10 untuk membuat banyak thread yang semuanya mengirim nilai ke *receiver*
yang sama. Kita dapat melakukannya dengan mengklon *transmitter*, seperti
ditunjukkan pada Listing 16-11.

<Listing number="16-11" file-name="src/main.rs" caption="Mengirim banyak pesan dari banyak produsen">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-11/src/main.rs:here}}
```

</Listing>

Kali ini, sebelum kita membuat thread pertama, kita memanggil `clone` pada
*transmitter*. Ini akan memberi kita *transmitter* baru yang dapat kita berikan
ke thread pertama. Kita memberikan *transmitter* asli ke thread kedua. Ini
memberi kita dua thread, masing-masing mengirim pesan berbeda ke satu
*receiver*.

Ketika Anda menjalankan kodenya, output Anda seharusnya tampak seperti ini:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: more
Got: from
Got: messages
Got: for
Got: the
Got: thread
Got: you
```

Anda mungkin melihat nilai-nilai itu dalam urutan lain, tergantung sistem
Anda. Inilah yang membuat concurrency menarik sekaligus sulit. Jika Anda
bereksperimen dengan `thread::sleep`, memberinya berbagai nilai di thread yang
berbeda, setiap penjalanan akan semakin nondeterministik dan menghasilkan
output yang berbeda setiap kali.

Sekarang setelah kita melihat cara kerja *channel*, mari kita lihat method
concurrency yang berbeda.
