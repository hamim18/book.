<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

## Menerapkan Konkurensi dengan Async

Pada bagian ini, kita akan menerapkan async pada sebagian tantangan konkurensi
yang sama dengan yang kita tangani dengan thread di Bab 16. Karena kita sudah
membahas banyak gagasan kuncinya di sana, pada bagian ini kita akan berfokus
pada hal-hal yang berbeda antara thread dan *future*.

Dalam banyak kasus, API untuk bekerja dengan konkurensi menggunakan async
sangat mirip dengan yang menggunakan thread. Di kasus lain, keduanya akhirnya
cukup berbeda. Bahkan ketika API thread dan async _terlihat_ mirip, keduanya
sering kali punya perilaku yang berbeda—dan karakteristik performanya hampir
selalu berbeda.

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>

### Membuat Task Baru dengan `spawn_task`

Operasi pertama yang kita tangani di bagian [“Membuat Thread Baru dengan
`spawn`”][thread-spawn]<!-- ignore --> di Bab 16 adalah menghitung naik pada
dua thread terpisah. Mari kita lakukan hal yang sama menggunakan async. *Crate*
`trpl` menyediakan fungsi `spawn_task` yang terlihat sangat mirip dengan API
`thread::spawn`, serta fungsi `sleep` yang merupakan versi async dari API
`thread::sleep`. Kita bisa memakai keduanya bersama-sama untuk
mengimplementasikan contoh penghitungan, seperti yang ditunjukkan di Listing
17-6.

<Listing number="17-6" caption="Membuat task baru untuk mencetak satu hal sementara task utama mencetak hal lain" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

Sebagai titik awal, kita menyiapkan fungsi `main` dengan `trpl::block_on`
supaya fungsi tingkat atas kita bisa bersifat async.

> Catatan: Mulai dari titik ini, setiap contoh di bab ini akan menyertakan kode
> pembungkus yang persis sama dengan `trpl::block_on` di `main`, jadi kita akan
> sering melewatkannya sama seperti kita melewatkan `main`. Ingat untuk
> menyertakannya di kode Anda!

Kemudian kita menulis dua loop di dalam blok tersebut, masing-masing
memuat sebuah pemanggilan `trpl::sleep`, yang menunggu selama setengah detik
(500 milidetik) sebelum mengirim pesan berikutnya. Kita menaruh satu
loop di badan `trpl::spawn_task` dan yang lainnya di loop `for`
tingkat atas. Kita juga menambahkan `await` setelah pemanggilan `sleep`.

Kode ini berperilaku mirip dengan implementasi berbasis thread—termasuk
kenyataan bahwa Anda mungkin melihat pesan-pesan muncul dalam urutan berbeda
di terminal Anda sendiri saat menjalankannya:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

Versi ini berhenti begitu loop `for` di badan blok async utama selesai,
karena *task* yang dibuat oleh `spawn_task` dimatikan saat fungsi `main`
berakhir. Jika Anda ingin *task* itu berjalan sampai tuntas, Anda perlu memakai
join handle untuk menunggu *task* pertama selesai. Dengan thread, kita memakai
metode `join` untuk “memblokir” sampai thread itu selesai berjalan. Di Listing
17-7, kita bisa memakai `await` untuk melakukan hal yang sama, karena *task*
handle itu sendiri adalah sebuah *future*. Type `Output`-nya adalah `Result`,
jadi kita juga melakukan unwrap padanya setelah menunggunya.

<Listing number="17-7" caption="Memakai `await` dengan join handle untuk menjalankan sebuah task sampai tuntas" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

Versi yang diperbarui ini berjalan sampai _kedua_ loop selesai:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Sejauh ini, tampaknya async dan thread memberi kita hasil yang serupa, hanya
dengan sintaks yang berbeda: memakai `await` alih-alih memanggil `join` pada
join handle, dan menunggu pemanggilan `sleep`.

Perbedaan yang lebih besar adalah kita tidak perlu membuat thread sistem
operasi lain untuk melakukan ini. Bahkan, di sini kita tidak perlu membuat
*task* sama sekali. Karena blok async terkompilasi menjadi *future* anonim, kita
bisa menaruh setiap loop di blok async dan meminta runtime menjalankan
keduanya sampai tuntas menggunakan fungsi `trpl::join`.

Di bagian [“Menunggu Semua Thread Selesai”][join-handles]<!-- ignore --> di
Bab 16, kita menunjukkan cara memakai metode `join` pada type `JoinHandle`
yang dikembalikan saat Anda memanggil `std::thread::spawn`. Fungsi
`trpl::join` serupa, tetapi untuk *future*. Saat Anda memberinya dua *future*,
fungsi itu menghasilkan satu *future* baru yang output-nya adalah *tuple* berisi
output dari setiap *future* yang Anda teruskan begitu _keduanya_ selesai.
Dengan demikian, di Listing 17-8, kita memakai `trpl::join` untuk menunggu
`fut1` dan `fut2` selesai. Kita _tidak_ menunggu `fut1` dan `fut2`, melainkan
*future* baru yang dihasilkan `trpl::join`. Kita mengabaikan output-nya, karena
output itu hanya *tuple* berisi dua nilai unit.

<Listing number="17-8" caption="Memakai `trpl::join` untuk menunggu dua future anonim" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

Saat kita menjalankan ini, kita melihat kedua *future* berjalan sampai tuntas:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Nah, Anda akan melihat urutan yang persis sama setiap kali, sangat berbeda
dari yang kita lihat dengan thread dan dengan `trpl::spawn_task` di Listing
17-7. Itu karena fungsi `trpl::join` bersifat _fair_ (adil), artinya fungsi
itu mengecek setiap *future* sesering yang sama, bergantian di antara keduanya,
dan tidak pernah membiarkan salah satunya melaju lebih dulu ketika yang lain
sudah siap. Dengan thread, sistem operasi yang memutuskan thread mana yang
dicek dan berapa lama ia dibiarkan berjalan. Dengan async Rust, runtime yang
memutuskan *task* mana yang dicek. (Dalam praktiknya, detailnya menjadi rumit
karena sebuah runtime async mungkin memakai thread sistem operasi di balik
layar sebagai bagian dari cara ia mengelola konkurensi, sehingga menjamin
fairness bisa menjadi pekerjaan lebih bagi sebuah runtime—tetapi itu tetap
mungkin!) Runtime tidak harus menjamin fairness untuk operasi tertentu, dan
runtime sering kali menawarkan API yang berbeda untuk memilih apakah Anda
menginginkan fairness atau tidak.

Cobalah beberapa variasi penungguan *future* berikut ini dan lihat hasilnya:

- Hapus blok async di sekeliling salah satu atau kedua loop.
- Tunggu setiap blok async segera setelah mendefinisikannya.
- Bungkus hanya loop pertama dalam blok async, dan tunggu *future* yang
  dihasilkan setelah badan loop kedua.

Sebagai tantangan tambahan, lihat apakah Anda bisa menebak output pada setiap
kasus _sebelum_ menjalankan kodenya!

<!-- Old headings. Do not remove or links may break. -->

<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>

### Mengirim Data antara Dua Task Menggunakan Message Passing

Berbagi data antar-future juga akan terasa familier: kita akan memakai message
passing lagi, tetapi kali ini dengan versi async dari type-type dan
fungsi-fungsinya. Kita akan menempuh jalan yang sedikit berbeda dari bagian
[“Mentransfer Data Antar-Thread dengan Message Passing”][message-passing-threads]<!-- ignore -->
di Bab 16 untuk mengilustrasikan sebagian perbedaan kunci antara konkurensi
berbasis thread dan berbasis *future*. Di Listing 17-9, kita akan mulai dengan
satu blok async saja—_bukan_ membuat *task* terpisah sebagaimana kita membuat
thread terpisah.

<Listing number="17-9" caption="Membuat channel async dan menetapkan kedua belahannya ke `tx` dan `rx`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

Di sini, kita memakai `trpl::channel`, versi async dari API *channel*
banyak-produsen, satu-konsumen yang kita pakai dengan thread di Bab 16. Versi
async dari API ini hanya sedikit berbeda dari versi berbasis threadnya: versi
ini memakai `rx` yang *mutable* alih-alih *immutable*, dan metode `recv`-nya
menghasilkan sebuah *future* yang perlu kita tunggu alih-alih langsung
menghasilkan nilainya. Sekarang kita bisa mengirim pesan dari pengirim ke
penerima. Perhatikan bahwa kita tidak perlu membuat thread terpisah atau
bahkan *task*; kita cukup menunggu pemanggilan `rx.recv`.

Metode `Receiver::recv` yang sinkron di `std::mpsc::channel` memblokir sampai
ia menerima sebuah pesan. Metode `trpl::Receiver::recv` tidak, karena metode
itu async. Alih-alih memblokir, metode itu menyerahkan kontrol kembali ke
runtime sampai sebuah pesan diterima atau sisi pengirim *channel* ditutup.
Sebaliknya, kita tidak menunggu pemanggilan `send`, karena pemanggilan itu
tidak memblokir. Memang tidak perlu, karena *channel* yang menjadi tujuan
pengirimannya tidak terbatas.

> Catatan: Karena semua kode async ini berjalan di dalam blok async dalam
> pemanggilan `trpl::block_on`, semua yang ada di dalamnya bisa menghindari
> pemblokiran. Namun, kode di _luar_ itu akan memblokir menunggu fungsi
> `block_on` kembali. Itulah inti dari fungsi `trpl::block_on`: fungsi itu
> memungkinkan Anda _memilih_ tempat untuk memblokir pada sekumpulan kode
> async, dan dengan demikian tempat transisi antara kode sinkron dan async.

Perhatikan dua hal tentang contoh ini. Pertama, pesan akan langsung tiba.
Kedua, meskipun kita memakai *future* di sini, belum ada konkurensi. Semua yang
ada di listing ini terjadi secara berurutan, sama seperti jika tidak ada
*future* yang terlibat.

Mari kita tangani bagian pertama dengan mengirim serangkaian pesan dan tidur
di antaranya, seperti yang ditunjukkan di Listing 17-10.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Mengirim dan menerima banyak pesan melalui channel async dan tidur dengan `await` di antara setiap pesan" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

Selain mengirim pesan, kita juga perlu menerimanya. Dalam kasus ini, karena
kita tahu berapa banyak pesan yang akan datang, kita bisa melakukannya secara
manual dengan memanggil `rx.recv().await` empat kali. Namun, di dunia nyata,
kita umumnya menunggu sejumlah pesan yang _tidak diketahui_, jadi kita perlu
terus menunggu sampai kita menentukan bahwa tidak ada pesan lagi.

Di Listing 16-10, kita memakai loop `for` untuk memproses semua item
yang diterima dari *channel* sinkron. Namun, Rust belum punya cara untuk memakai
loop `for` dengan serangkaian item yang _dihasilkan secara asinkron_,
jadi kita perlu memakai loop yang belum pernah kita lihat: loop
kondisional `while let`. Ini adalah versi loop dari konstruksi `if let`
yang kita lihat di bagian [“Alur Kontrol yang Ringkas dengan `if let` dan
`let...else`”][if-let]<!-- ignore --> di Bab 6. Loop ini akan terus
berjalan selama pola yang ditentukannya terus cocok dengan nilainya.

Pemanggilan `rx.recv` menghasilkan sebuah *future*, yang kita tunggu. Runtime
akan menjeda *future* itu sampai ia siap. Begitu sebuah pesan tiba, *future* itu
akan menghasilkan `Some(message)` sebanyak jumlah pesan yang tiba. Ketika
*channel* ditutup, terlepas dari apakah _ada_ pesan yang pernah tiba, *future* itu
akan menghasilkan `None` untuk menandakan bahwa tidak ada nilai lagi sehingga
kita harus berhenti melakukan polling—artinya, berhenti menunggu.

Loop `while let` merangkum semua ini. Jika hasil pemanggilan
`rx.recv().await` adalah `Some(message)`, kita mendapat akses ke pesan
tersebut dan bisa memakainya di badan loop, sama seperti yang bisa kita
lakukan dengan `if let`. Jika hasilnya `None`, loop berakhir. Setiap
kali loop selesai, ia kembali mencapai await point, sehingga runtime
menjedanya lagi sampai pesan lain tiba.

Sekarang kode ini berhasil mengirim dan menerima semua pesan. Sayangnya,
masih ada beberapa masalah. Pertama, pesan-pesan tidak tiba dalam selang
setengah detik. Semuanya tiba sekaligus, 2 detik (2.000 milidetik) setelah
kita memulai program. Kedua, program ini juga tidak pernah keluar! Sebaliknya,
program menunggu pesan baru selamanya. Anda harus mematikannya menggunakan
<kbd>ctrl</kbd>-<kbd>C</kbd>.

#### Kode di dalam Satu Blok Async Berjalan secara Linear

Mari mulai dengan memeriksa mengapa pesan-pesan itu datang sekaligus setelah
seluruh penundaan, alih-alih datang dengan penundaan di antara setiap pesan.
Di dalam sebuah blok async tertentu, urutan kemunculan kata kunci `await` di
kode juga merupakan urutan eksekusinya saat program berjalan.

Hanya ada satu blok async di Listing 17-10, jadi semua yang ada di dalamnya
berjalan secara linear. Masih belum ada konkurensi. Semua pemanggilan
`tx.send` terjadi, diselingi semua pemanggilan `trpl::sleep` dan await point
terkaitnya. Baru setelah itu loop `while let` sempat melewati
await point mana pun pada pemanggilan `recv`.

Untuk mendapatkan perilaku yang kita inginkan, yaitu penundaan tidur terjadi
di antara setiap pesan, kita perlu menaruh operasi `tx` dan `rx` di blok async
masing-masing, seperti yang ditunjukkan di Listing 17-11. Dengan begitu,
runtime bisa menjalankan keduanya secara terpisah menggunakan `trpl::join`,
sama seperti di Listing 17-8. Sekali lagi, kita menunggu hasil pemanggilan
`trpl::join`, bukan *future* masing-masing. Jika kita menunggu *future*
masing-masing secara berurutan, kita akan kembali berakhir di alur
sekuensial—justru hal yang sedang kita usahakan untuk _tidak_ dilakukan.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="Memisahkan `send` dan `recv` ke blok `async` masing-masing dan menunggu future dari blok-blok itu" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

Dengan kode yang diperbarui di Listing 17-11, pesan-pesan dicetak dengan
selang 500 milidetik, alih-alih berhamburan sekaligus setelah 2 detik.

#### Memindahkan Ownership ke dalam Blok Async

Namun, program ini masih tidak pernah keluar, karena cara loop `while
let` berinteraksi dengan `trpl::join`:

- *Future* yang dikembalikan `trpl::join` hanya selesai ketika _kedua_ *future*
  yang diteruskan padanya telah selesai.
- *Future* `tx_fut` selesai begitu ia selesai tidur setelah mengirim pesan
  terakhir di `vals`.
- *Future* `rx_fut` tidak akan selesai sampai loop `while let` berakhir.
- Loop `while let` tidak akan berakhir sampai menunggu `rx.recv`
  menghasilkan `None`.
- Menunggu `rx.recv` akan mengembalikan `None` hanya ketika ujung lain
  *channel* ditutup.
- *Channel* akan ditutup hanya jika kita memanggil `rx.close` atau ketika sisi
  pengirimnya, `tx`, di-drop.
- Kita tidak memanggil `rx.close` di mana pun, dan `tx` tidak akan di-drop
  sampai blok async terluar yang diteruskan ke `trpl::block_on` berakhir.
- Blok itu tidak bisa berakhir karena ia terblokir menunggu `trpl::join`
  selesai, yang membawa kita kembali ke awal daftar ini.

Saat ini, blok async tempat kita mengirim pesan hanya _meminjam_ `tx` karena
mengirim pesan tidak memerlukan *ownership*, tetapi jika kita bisa _memindahkan_
`tx` ke dalam blok async itu, `tx` akan di-drop begitu blok itu berakhir. Di
bagian [“Menangkap *Reference* atau Memindahkan
*Ownership*”][capture-or-move]<!-- ignore --> di Bab 13, Anda belajar cara
memakai kata kunci `move` dengan *closure*, dan seperti yang dibahas di bagian
[“Memakai Closure `move` dengan Thread”][move-threads]<!-- ignore --> di Bab
16, kita sering perlu memindahkan data ke dalam *closure* saat bekerja dengan
thread. Dinamika dasar yang sama berlaku pada blok async, jadi kata kunci
`move` bekerja dengan blok async sama seperti dengan *closure*.

Di Listing 17-12, kita mengubah blok yang dipakai untuk mengirim pesan dari
`async` menjadi `async move`.

<Listing number="17-12" caption="Revisi kode dari Listing 17-11 yang berhenti dengan benar saat selesai" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

Saat kita menjalankan versi kode _ini_, program berhenti dengan mulus setelah
pesan terakhir dikirim dan diterima. Berikutnya, mari kita lihat apa yang
perlu diubah untuk mengirim data dari lebih dari satu *future*.

#### Menggabungkan Sejumlah Future dengan Macro `join!`

*Channel* async ini juga merupakan *channel* banyak-produsen, jadi kita bisa
memanggil `clone` pada `tx` jika ingin mengirim pesan dari beberapa *future*,
seperti yang ditunjukkan di Listing 17-13.

<Listing number="17-13" caption="Memakai banyak produsen dengan blok async" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

Pertama, kita mengklon `tx`, menciptakan `tx1` di luar blok async pertama.
Kita memindahkan `tx1` ke dalam blok itu sama seperti yang kita lakukan
sebelumnya dengan `tx`. Kemudian, nanti, kita memindahkan `tx` yang asli ke
dalam blok async yang _baru_, tempat kita mengirim lebih banyak pesan dengan
penundaan yang sedikit lebih lambat. Kebetulan kita menaruh blok async baru
ini setelah blok async untuk menerima pesan, tetapi blok itu bisa saja
ditaruh sebelumnya. Kuncinya adalah urutan *future* di-tunggu, bukan urutan
*future* dibuat.

Kedua blok async untuk mengirim pesan harus menjadi blok `async move` supaya
`tx` dan `tx1` di-drop saat blok-blok itu selesai. Jika tidak, kita akan
kembali berakhir di infinite loop yang sama dengan saat kita mulai.

Terakhir, kita beralih dari `trpl::join` ke `trpl::join!` untuk menangani
*future* tambahan: *macro* `join!` menunggu sejumlah *future* sembarang yang
jumlahnya kita ketahui pada waktu kompilasi. Kita akan membahas penungguan
koleksi *future* dengan jumlah yang tidak diketahui nanti di bab ini.

Sekarang kita melihat semua pesan dari kedua *future* pengirim, dan karena
*future*-future pengirim itu memakai penundaan yang sedikit berbeda setelah
mengirim, pesan-pesan juga diterima pada selang yang berbeda:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

Kita telah mengeksplorasi cara memakai *message passing* untuk mengirim data
antar-future, cara kode di dalam blok async berjalan secara sekuensial, cara
memindahkan *ownership* ke dalam blok async, dan cara menggabungkan banyak
*future*. Berikutnya, mari kita bahas bagaimana dan mengapa memberi tahu runtime
bahwa ia bisa beralih ke *task* lain.

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads
