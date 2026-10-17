## Merangkai Semuanya: Futures, Tasks, dan Threads

Seperti yang kita lihat di [Bab 16][ch16]<!-- ignore -->, thread menyediakan
satu pendekatan terhadap konkurensi. Kita telah melihat pendekatan lain di bab
ini: memakai async dengan *future* dan *stream*. Jika Anda bertanya-tanya kapan
memilih satu metode alih-alih yang lain, jawabannya adalah: tergantung! Dan
dalam banyak kasus, pilihannya bukan thread _atau_ async, melainkan thread
_dan_ async.

Banyak sistem operasi telah menyediakan model konkurensi berbasis threading
selama puluhan tahun, dan karena itu banyak bahasa pemrograman mendukungnya.
Akan tetapi, model-model ini bukan tanpa kompromi. Di banyak sistem operasi,
model ini memakai memori yang cukup banyak untuk setiap thread. Thread juga
hanya menjadi opsi ketika sistem operasi dan perangkat keras Anda
mendukungnya. Tidak seperti komputer desktop dan ponsel arus utama, sebagian
sistem tertanam tidak punya OS sama sekali, jadi mereka juga tidak punya
thread.

Model async menyediakan sekumpulan kompromi yang berbeda—dan pada akhirnya
saling melengkapi. Dalam model async, operasi konkuren tidak memerlukan
thread-nya sendiri. Sebagai gantinya, operasi itu bisa berjalan pada *task*,
seperti saat kita memakai `trpl::spawn_task` untuk memulai pekerjaan dari
fungsi sinkron di bagian *streams*. Sebuah *task* mirip dengan thread, tetapi
alih-alih dikelola oleh sistem operasi, *task* dikelola oleh kode tingkat
library: runtime.

Ada alasan mengapa API untuk membuat thread dan membuat *task* sangat mirip.
Thread berlaku sebagai batas untuk kumpulan operasi sinkron; konkurensi
dimungkinkan _antar_-thread. *Task* berlaku sebagai batas untuk kumpulan operasi
_asinkron_; konkurensi dimungkinkan baik _antar_- maupun _di dalam_ *task*,
karena sebuah *task* bisa beralih di antara *future*-future di badannya.
Terakhir, *future* adalah satuan konkurensi Rust yang paling halus, dan setiap
*future* bisa merepresentasikan pohon dari *future*-future lain. Runtime—secara
khusus, executor-nya—mengelola *task*, dan *task* mengelola *future*. Dalam hal itu,
*task* mirip dengan thread ringan yang dikelola runtime, dengan kemampuan
tambahan yang berasal dari dikelola oleh runtime alih-alih oleh sistem
operasi.

Ini tidak berarti *task* async selalu lebih baik daripada thread (atau
sebaliknya). Konkurensi dengan thread dalam beberapa hal adalah model
pemrograman yang lebih sederhana daripada konkurensi dengan `async`. Itu bisa
menjadi kekuatan atau kelemahan. Thread agak “fire and forget” (dilepas dan
dibiarkan); mereka tidak punya padanan native untuk *future*, jadi mereka
langsung berjalan sampai selesai tanpa diinterupsi kecuali oleh sistem operasi
itu sendiri.

Dan ternyata thread dan *task* sering bekerja sangat baik bersama-sama, karena
*task* bisa (setidaknya di beberapa runtime)
dipindahkan antar-thread. Bahkan, di balik layar, runtime yang kita pakai
selama ini—termasuk fungsi `spawn_blocking` dan `spawn_task`—bersifat
multithreaded secara bawaan! Banyak runtime memakai pendekatan yang disebut
_work stealing_ (pencurian pekerjaan) untuk memindahkan *task* antar-thread
secara transparan, berdasarkan cara thread-thread itu sedang dimanfaatkan,
untuk meningkatkan performa keseluruhan sistem. Pendekatan itu sebenarnya
memerlukan thread _dan_ *task*, dan karena itu juga *future*.

Saat memikirkan metode mana yang dipakai untuk situasi mana, pertimbangkan
aturan praktis ini:

- Jika pekerjaannya _sangat dapat diparalelkan_ (artinya, terikat CPU),
  seperti memproses sekumpulan data yang setiap bagiannya bisa diproses
  terpisah, thread adalah pilihan yang lebih baik.
- Jika pekerjaannya _sangat konkuren_ (artinya, terikat I/O), seperti
  menangani pesan dari banyak sumber berbeda yang bisa datang pada selang atau
  laju yang berbeda, async adalah pilihan yang lebih baik.

Dan jika Anda butuh paralelisme sekaligus konkurensi, Anda tidak harus memilih
antara thread dan async. Anda bisa memakai keduanya secara bebas, membiarkan
masing-masing memainkan peran yang paling dikuasainya. Contohnya, Listing
17-25 menunjukkan contoh yang cukup umum dari campuran semacam ini di kode
Rust dunia nyata.

<Listing number="17-25" caption="Mengirim pesan dengan kode pemblokiran di dalam thread dan menunggu pesan-pesan itu di dalam blok async" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:all}}
```

</Listing>

Kita mulai dengan membuat *channel* async, lalu membuat sebuah thread yang
mengambil kepemilikan sisi pengirim *channel* dengan memakai kata kunci `move`.
Di dalam thread itu, kita mengirim angka 1 sampai 10, tidur selama satu detik
di antara setiap angka. Terakhir, kita menjalankan sebuah *future* yang dibuat
dengan blok async yang diteruskan ke `trpl::block_on`, sama seperti yang kita
lakukan di sepanjang bab ini. Di dalam *future* itu, kita menunggu pesan-pesan
tersebut, sama seperti contoh-contoh *message passing* lain yang telah kita
lihat.

Untuk kembali ke skenario pembuka bab ini, bayangkan menjalankan sekumpulan
tugas pengodean video menggunakan thread khusus (karena pengodean video
terikat komputasi), tetapi memberi tahu UI bahwa operasi-operasi itu selesai
dengan *channel* async. Ada contoh yang tak terhitung jumlahnya untuk kombinasi
semacam ini di kasus pemakaian dunia nyata.

## Ringkasan

Ini bukan terakhir kalinya Anda melihat konkurensi di buku ini. Proyek di
[Bab 21][ch21]<!-- ignore --> akan menerapkan konsep-konsep ini dalam situasi
yang lebih realistis daripada contoh-contoh sederhana yang dibahas di sini,
dan membandingkan pemecahan masalah dengan threading versus *task* dan *future*
secara lebih langsung.

Apa pun pendekatan yang Anda pilih di antara ini, Rust memberi Anda alat yang
Anda butuhkan untuk menulis kode konkuren yang aman dan cepat—baik untuk
server web berdaya tampung tinggi maupun sistem operasi tertanam.

Berikutnya, kita akan membahas cara-cara yang idiomatis untuk memodelkan
masalah dan menstrukturkan solusi seiring program Rust Anda membesar. Selain
itu, kita akan membahas bagaimana idiom Rust berhubungan dengan idiom yang
mungkin Anda kenal dari pemrograman berorientasi objek.

[ch16]: ch16-00-concurrency.html
[combining-futures]: ch17-03-more-futures.html#building-our-own-async-abstractions
[streams]: ch17-04-streams.html#composing-streams
[ch21]: ch21-00-final-project-a-web-server.html
