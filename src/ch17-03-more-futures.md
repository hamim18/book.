<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>

### Menyerahkan Kontrol ke Runtime

Ingat kembali dari bagian [“Program Async Pertama Kita”][async-program]<!-- ignore -->
bahwa di setiap await point, Rust memberi runtime kesempatan untuk menjeda
*task* dan beralih ke *task* lain jika *future* yang sedang ditunggu belum siap.
Kebalikannya juga benar: Rust _hanya_ menjeda blok async dan menyerahkan
kontrol kembali ke runtime di await point. Semua yang berada di antara
await point bersifat sinkron.

Artinya, jika Anda mengerjakan banyak pekerjaan di dalam blok async tanpa
await point, *future* itu akan menghalangi *future*-future lain untuk membuat
kemajuan. Anda mungkin pernah mendengar ini disebut sebagai sebuah *future* yang
membuat *future* lain _kelaparan_. Dalam beberapa kasus, hal itu mungkin bukan
masalah besar. Akan tetapi, jika Anda sedang melakukan semacam persiapan yang
mahal atau pekerjaan yang berjalan lama, atau jika Anda punya *future* yang akan
terus-menerus mengerjakan suatu tugas tanpa henti, Anda perlu memikirkan kapan
dan di mana menyerahkan kontrol kembali ke runtime.

Mari kita simulasikan operasi yang berjalan lama untuk mengilustrasikan
masalah kelaparan itu, lalu mengeksplorasi cara mengatasinya. Listing 17-14
memperkenalkan fungsi `slow`.

<Listing number="17-14" caption="Memakai `thread::sleep` untuk mensimulasikan operasi yang lambat" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:slow}}
```

</Listing>

Kode ini memakai `std::thread::sleep` alih-alih `trpl::sleep` sehingga
pemanggilan `slow` akan memblokir thread saat ini selama beberapa milidetik.
Kita bisa memakai `slow` untuk mewakili operasi dunia nyata yang berjalan lama
sekaligus memblokir.

Di Listing 17-15, kita memakai `slow` untuk menirukan pengerjaan pekerjaan
typed CPU-bound semacam ini pada sepasang *future*.

<Listing number="17-15" caption="Memanggil fungsi `slow` untuk mensimulasikan operasi yang lambat" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:slow-futures}}
```

</Listing>

Setiap *future* menyerahkan kontrol kembali ke runtime hanya _setelah_
melakukan serangkaian operasi lambat. Jika Anda menjalankan kode ini, Anda
akan melihat output berikut:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-15/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

Sama seperti Listing 17-5 tempat kita memakai `trpl::select` untuk
mempertandingkan *future* yang mengambil dua URL, `select` tetap selesai begitu
`a` tuntas. Akan tetapi, tidak ada penyelangan antara pemanggilan `slow` di
kedua *future* itu. *Future* `a` mengerjakan semua pekerjaannya sampai pemanggilan
`trpl::sleep` ditunggu, lalu *future* `b` mengerjakan semua pekerjaannya sampai
pemanggilan `trpl::sleep`-nya sendiri ditunggu, dan akhirnya *future* `a`
selesai. Untuk memungkinkan kedua *future* membuat kemajuan di antara
tugas-tugas lambat mereka, kita butuh await point supaya bisa menyerahkan
kontrol kembali ke runtime. Itu berarti kita butuh sesuatu yang bisa kita
tunggu!

Kita sebenarnya sudah bisa melihat penyerahan semacam ini terjadi di Listing
17-15: jika kita menghapus `trpl::sleep` di akhir *future* `a`, *future* itu akan
selesai tanpa *future* `b` berjalan _sama sekali_. Mari kita coba memakai fungsi
`trpl::sleep` sebagai titik awal untuk membiarkan operasi saling bergantian
membuat kemajuan, seperti yang ditunjukkan di Listing 17-16.

<Listing number="17-16" caption="Memakai `trpl::sleep` untuk membiarkan operasi saling bergantian membuat kemajuan" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</Listing>

Kita telah menambahkan pemanggilan `trpl::sleep` dengan await point di antara
setiap pemanggilan `slow`. Sekarang pekerjaan kedua *future* saling menyelang:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

*Future* `a` tetap berjalan sebentar sebelum menyerahkan kontrol ke `b`, karena
ia memanggil `slow` sebelum pernah memanggil `trpl::sleep`, tetapi setelah itu
kedua *future* saling bergantian setiap kali salah satunya mencapai await point.
Dalam kasus ini, kita melakukannya setelah setiap pemanggilan `slow`, tetapi
kita bisa memecah pekerjaan itu dengan cara apa pun yang paling masuk akal
bagi kita.

Namun, di sini kita sebenarnya tidak ingin _tidur_: kita ingin membuat
kemajuan secepat mungkin. Kita hanya perlu menyerahkan kontrol kembali ke
runtime. Kita bisa melakukannya secara langsung, menggunakan fungsi
`trpl::yield_now`. Di Listing 17-17, kita mengganti semua pemanggilan
`trpl::sleep` itu dengan `trpl::yield_now`.

<Listing number="17-17" caption="Memakai `yield_now` untuk membiarkan operasi saling bergantian membuat kemajuan" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:yields}}
```

</Listing>

Kode ini lebih jelas mengenai maksud yang sesungguhnya dan bisa jauh lebih
cepat daripada memakai `sleep`, karena timer seperti yang dipakai `sleep`
sering kali punya batas seberapa rinci mereka bisa dibuat. Versi `sleep` yang
kita pakai, contohnya, akan selalu tidur setidaknya satu milidetik, bahkan
jika kita memberinya `Duration` satu nanodetik. Sekali lagi, komputer modern
itu _cepat_: mereka bisa melakukan banyak hal dalam satu milidetik!

Artinya, async bisa berguna bahkan untuk tugas-tugas yang terikat komputasi,
bergantung pada apa lagi yang sedang dikerjakan program Anda, karena async
menyediakan alat yang berguna untuk menstrukturkan hubungan antara berbagai
bagian program (tetapi dengan membayar overhead state machine async). Ini
adalah bentuk _cooperative multitasking_ (multitasking kooperatif), tempat
setiap *future* punya kuasa untuk menentukan kapan ia menyerahkan kontrol
melalui await point. Karena itu, setiap *future* juga punya tanggung jawab untuk
menghindari pemblokiran terlalu lama. Di sebagian sistem operasi tertanam
berbasis Rust, ini adalah _satu-satunya_ jenis multitasking!

Tentu saja, dalam kode dunia nyata, Anda biasanya tidak akan menyelingi
pemanggilan fungsi dengan await point pada setiap baris. Meskipun menyerahkan
kontrol dengan cara ini relatif murah, itu tidak gratis. Dalam banyak kasus,
mencoba memecah tugas yang terikat komputasi bisa membuatnya jauh lebih
lambat, jadi terkadang lebih baik bagi performa _keseluruhan_ untuk
membiarkan sebuah operasi memblokir sebentar. Selalu ukur untuk melihat di
mana hambatan performa sesungguhnya dari kode Anda. Meski begitu, dinamika
mendasar ini penting untuk diingat jika Anda _memang_ melihat banyak pekerjaan
berjalan serial padahal Anda mengharapkannya berjalan konkuren!

<a id="building-our-own-async-abstractions"></a>
### Membangun Abstraksi Async Kita Sendiri

Kita juga bisa menyusun *future* bersama-sama untuk menciptakan pattern baru.
Contohnya, kita bisa membangun fungsi `timeout` dengan batu penyusun async
yang sudah kita miliki. Saat selesai, hasilnya akan menjadi batu penyusun lain
yang bisa kita pakai untuk menciptakan lebih banyak abstraksi async.

Listing 17-18 menunjukkan bagaimana kita mengharapkan `timeout` ini bekerja
dengan sebuah *future* yang lambat.

<Listing number="17-18" caption="Memakai `timeout` khayalan kita untuk menjalankan operasi lambat dengan batas waktu" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-18/src/main.rs:here}}
```

</Listing>

Mari kita implementasikan ini! Sebagai permulaan, mari kita pikirkan API
untuk `timeout`:

- Fungsi ini harus berupa fungsi async supaya kita bisa menunggunya.
- Parameter pertamanya harus berupa *future* yang akan dijalankan. Kita bisa
  membuatnya generik supaya bisa bekerja dengan *future* apa pun.
- Parameter keduanya adalah waktu maksimum untuk menunggu. Jika kita memakai
  `Duration`, itu akan memudahkan kita meneruskannya ke `trpl::sleep`.
- Fungsi ini harus mengembalikan `Result`. Jika *future* itu selesai dengan
  sukses, `Result`-nya adalah `Ok` beserta nilai yang dihasilkan *future*
  tersebut. Jika batas waktunya habis lebih dulu, `Result`-nya adalah `Err`
  beserta durasi yang ditunggu timeout itu.

Listing 17-19 menunjukkan deklarasi ini.

<!-- This is not tested because it intentionally does not compile. -->

<Listing number="17-19" caption="Mendefinisikan tanda tangan `timeout`" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-19/src/main.rs:declaration}}
```

</Listing>

Itu memenuhi tujuan kita untuk type-typenya. Sekarang mari kita pikirkan
_perilaku_ yang kita butuhkan: kita ingin mempertandingkan *future* yang
diteruskan melawan durasinya. Kita bisa memakai `trpl::sleep` untuk membuat
sebuah *future* timer dari durasi itu, dan memakai `trpl::select` untuk
menjalankan timer itu bersama *future* yang diteruskan pemanggil.

Di Listing 17-20, kita mengimplementasikan `timeout` dengan melakukan `match`
pada hasil penungguan `trpl::select`.

<Listing number="17-20" caption="Mendefinisikan `timeout` dengan `select` dan `sleep`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-20/src/main.rs:implementation}}
```

</Listing>

Implementasi `trpl::select` tidak adil: implementasi itu selalu melakukan
polling pada argumen sesuai urutan penerusan (implementasi `select` lain akan
memilih secara acak argumen mana yang di-polling lebih dulu). Karena itu, kita
meneruskan `future_to_try` ke `select` lebih dulu supaya ia mendapat
kesempatan untuk selesai bahkan jika `max_time` adalah durasi yang sangat
singkat. Jika `future_to_try` selesai lebih dulu, `select` akan mengembalikan
`Left` beserta output dari `future_to_try`. Jika `timer` selesai lebih dulu,
`select` akan mengembalikan `Right` beserta output `()` dari timer.

Jika `future_to_try` berhasil dan kita mendapat `Left(output)`, kita
mengembalikan `Ok(output)`. Jika timer tidur yang habis lebih dulu dan kita
mendapat `Right(())`, kita mengabaikan `()` itu dengan `_` dan mengembalikan
`Err(max_time)`.

Dengan itu, kita punya `timeout` yang berfungsi, dibangun dari dua pembantu
async lainnya. Jika kita menjalankan kode kita, kode itu akan mencetak mode
kegagalannya setelah batas waktu habis:

```text
Failed after 2 seconds
```

Karena *future* dapat disusun dengan *future* lain, Anda bisa membangun alat yang
benar-benar hebat menggunakan batu penyusun async yang lebih kecil. Contohnya,
Anda bisa memakai pendekatan yang sama ini untuk menggabungkan timeout dengan
percobaan ulang, dan selanjutnya memakai keduanya dengan operasi seperti
pemanggilan jaringan (seperti di Listing 17-5).

Dalam praktiknya, Anda biasanya akan bekerja langsung dengan `async` dan
`await`, dan sebagai pelengkap dengan fungsi seperti `select` serta *macro*
seperti *macro* `join!` untuk mengontrol cara *future*-future terluar dijalankan.

Sekarang kita telah melihat sejumlah cara untuk bekerja dengan banyak *future*
pada saat yang sama. Berikutnya, kita akan melihat cara bekerja dengan banyak
*future* dalam sebuah urutan seiring waktu dengan _stream_.

[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program
