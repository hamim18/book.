<a id="control-flow"></a>
## Alur Kontrol

Kemampuan untuk menjalankan sebagian kode bergantung pada apakah sebuah
kondisi bernilai `true`, dan kemampuan untuk menjalankan sebagian kode secara
berulang selama sebuah kondisi bernilai `true`, adalah blok penyusun dasar
pada sebagian besar bahasa pemrograman. Konstruk paling umum yang memungkinkan
Anda mengendalikan alur eksekusi kode Rust adalah ekspresi `if` dan
perulangan.

### Ekspresi `if`

Ekspresi `if` memungkinkan Anda membuat percabangan kode bergantung pada
kondisinya. Anda memberikan sebuah kondisi lalu menyatakan, “Jika kondisi ini
terpenuhi, jalankan blok kode ini. Jika kondisinya tidak terpenuhi, jangan
jalankan blok kode ini.”

Buat proyek baru bernama _branches_ di direktori _projects_ Anda untuk
mengeksplorasi ekspresi `if`. Di file _src/main.rs_, masukkan kode berikut:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

Semua ekspresi `if` dimulai dengan keyword `if`, yang diikuti sebuah kondisi.
Pada kasus ini, kondisinya memeriksa apakah variabel `number` memiliki nilai
kurang dari 5 atau tidak. Kita meletakkan blok kode yang dieksekusi jika
kondisinya `true` tepat setelah kondisi, di dalam kurung kurawal. Blok kode
yang terkait dengan kondisi pada ekspresi `if` kadang-kadang disebut *arm*
(lengan), sama seperti arm pada ekspresi `match` yang kita bahas di bagian
[“Membandingkan Tebakan dengan Angka
Rahasia”][comparing-the-guess-to-the-secret-number]<!--
ignore --> pada Bab 2.

Secara opsional, kita juga dapat menyertakan ekspresi `else`, yang kita pilih
untuk dilakukan di sini, untuk memberi program blok kode alternatif yang
dieksekusi seandainya kondisi mengevaluasi menjadi `false`. Jika Anda tidak
memberikan ekspresi `else` dan kondisinya `false`, program akan melewati blok
`if` dan melanjutkan ke bagian kode berikutnya.

Coba jalankan kode ini; Anda seharusnya melihat keluaran berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Mari kita coba mengubah nilai `number` menjadi nilai yang membuat kondisinya
`false` untuk melihat apa yang terjadi:

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Jalankan programnya lagi, dan lihat keluarannya:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

Perlu dicatat juga bahwa kondisi pada kode ini _harus_ berupa `bool`. Jika
kondisinya bukan `bool`, kita akan mendapatkan error. Contohnya, coba jalankan
kode berikut:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

Kondisi `if` mengevaluasi menjadi nilai `3` kali ini, dan Rust melemparkan
error:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

Error tersebut menandakan bahwa Rust mengharapkan `bool` tetapi mendapatkan
integer. Tidak seperti bahasa seperti Ruby dan JavaScript, Rust tidak akan
otomatis mencoba mengonversi tipe non-Boolean menjadi Boolean. Anda harus
eksplisit dan selalu memberikan `if` sebuah Boolean sebagai kondisinya. Jika
kita ingin blok kode `if` berjalan hanya ketika sebuah angka tidak sama dengan
`0`, misalnya, kita dapat mengubah ekspresi `if` menjadi seperti berikut:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

Menjalankan kode ini akan mencetak `number was something other than zero`.

#### Menangani Banyak Kondisi dengan `else if`

Anda dapat memakai banyak kondisi dengan menggabungkan `if` dan `else` dalam
sebuah ekspresi `else if`. Contohnya:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

Program ini memiliki empat jalur yang mungkin dapat diambilnya. Setelah
menjalankannya, Anda seharusnya melihat keluaran berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

Ketika program ini dieksekusi, ia memeriksa setiap ekspresi `if` secara
bergiliran dan mengeksekusi badan pertama yang kondisinya mengevaluasi menjadi
`true`. Perhatikan bahwa meskipun 6 habis dibagi 2, kita tidak melihat keluaran
`number is divisible by 2`, dan kita juga tidak melihat teks
`number is not divisible by 4, 3, or 2` dari blok `else`. Itu karena Rust hanya
mengeksekusi blok untuk kondisi `true` yang pertama, dan begitu menemukannya,
ia bahkan tidak memeriksa sisanya.

Memakai terlalu banyak ekspresi `else if` dapat membuat kode Anda berantakan,
jadi jika Anda memiliki lebih dari satu, Anda mungkin ingin melakukan
refactoring pada kode Anda. Bab 6 menjelaskan konstruk percabangan Rust yang
tangguh bernama `match` untuk kasus-kasus seperti ini.

#### Memakai `if` dalam Pernyataan `let`

Karena `if` adalah ekspresi, kita dapat memakainya di sisi kanan pernyataan
`let` untuk menetapkan hasilnya ke sebuah variabel, seperti pada Listing 3-2.

<Listing number="3-2" file-name="src/main.rs" caption="Menetapkan hasil ekspresi `if` ke sebuah variabel">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

Variabel `number` akan terikat pada sebuah nilai berdasarkan hasil ekspresi
`if`. Jalankan kode ini untuk melihat apa yang terjadi:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

Ingat bahwa blok kode mengevaluasi menjadi ekspresi terakhir di dalamnya, dan
angka itu sendiri juga merupakan ekspresi. Pada kasus ini, nilai keseluruhan
ekspresi `if` bergantung pada blok kode mana yang dieksekusi. Ini berarti
nilai-nilai yang berpotensi menjadi hasil dari setiap arm `if` harus bertipe
sama; pada Listing 3-2, hasil dari arm `if` maupun arm `else` sama-sama
integer `i32`. Jika tipenya tidak cocok, seperti pada contoh berikut, kita akan
mendapatkan error:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

Ketika kita mencoba mengompilasi kode ini, kita akan mendapatkan error. Arm
`if` dan `else` memiliki tipe nilai yang tidak kompatibel, dan Rust menunjukkan
dengan tepat di mana letak masalahnya di dalam program:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

Ekspresi di dalam blok `if` mengevaluasi menjadi integer, dan ekspresi di
dalam blok `else` mengevaluasi menjadi string. Ini tidak akan berhasil, karena
variabel harus memiliki satu tipe, dan Rust perlu tahu secara pasti pada waktu
kompilasi tipe apa variabel `number` itu. Mengetahui tipe `number`
memungkinkan *compiler* memverifikasi bahwa tipenya valid di semua tempat kita
memakai `number`. Rust tidak akan mampu melakukannya jika tipe `number` hanya
ditentukan pada saat runtime; *compiler* akan menjadi lebih rumit dan memberikan
jaminan yang lebih sedikit tentang kodenya jika ia harus melacak beberapa tipe
hipotetis untuk setiap variabel.

### Perulangan

Sering kali berguna untuk mengeksekusi blok kode lebih dari sekali. Untuk
tugas ini, Rust menyediakan beberapa perulangan, yang akan menjalankan kode di
dalam badan perulangan sampai selesai, lalu segera mulai lagi dari awal. Untuk
bereksperimen dengan perulangan, mari kita buat proyek baru bernama _loops_.

Rust memiliki tiga jenis perulangan: `loop`, `while`, dan `for`. Mari kita
coba satu per satu.

#### Mengulang Kode dengan `loop`

Keyword `loop` memberi tahu Rust untuk mengeksekusi blok kode berulang-ulang,
entah selamanya atau sampai Anda secara eksplisit menyuruhnya berhenti.

Sebagai contoh, ubah file _src/main.rs_ di direktori _loops_ Anda menjadi
seperti ini:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

Ketika kita menjalankan program ini, kita akan melihat `again!` dicetak
terus-menerus berulang-ulang sampai kita menghentikan programnya secara
manual. Sebagian besar terminal mendukung pintasan keyboard
<kbd>ctrl</kbd>-<kbd>C</kbd> untuk menginterupsi program yang terjebak dalam
perulangan terus-menerus. Cobalah:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

Simbol `^C` merepresentasikan posisi ketika Anda menekan
<kbd>ctrl</kbd>-<kbd>C</kbd>.

Anda mungkin melihat atau tidak melihat kata `again!` dicetak setelah `^C`,
bergantung pada posisi kode di dalam perulangan ketika menerima sinyal
interupsi.

Untungnya, Rust juga menyediakan cara untuk keluar dari perulangan lewat kode.
Anda dapat meletakkan keyword `break` di dalam perulangan untuk memberi tahu
program kapan harus berhenti mengeksekusi perulangan. Ingat bahwa kita
melakukannya dalam permainan tebak angka di bagian [“Berhenti Setelah Tebakan
Benar”][quitting-after-a-correct-guess]<!-- ignore
--> pada Bab 2 untuk keluar dari program ketika pengguna memenangkan permainan
dengan menebak angka yang benar.

Kita juga memakai `continue` dalam permainan tebak angka, yang di dalam
perulangan memberi tahu program untuk melewati sisa kode pada iterasi
perulangan kali ini dan langsung menuju iterasi berikutnya.

#### Mengembalikan Nilai dari Perulangan

Salah satu kegunaan `loop` adalah mengulangi operasi yang Anda tahu mungkin
gagal, seperti memeriksa apakah sebuah thread telah menyelesaikan pekerjaannya.
Anda mungkin juga perlu meneruskan hasil operasi itu keluar dari perulangan ke
bagian lain kode Anda. Untuk melakukannya, Anda dapat menambahkan nilai yang
ingin Anda kembalikan setelah ekspresi `break` yang Anda pakai untuk
menghentikan perulangan; nilai itu akan dikembalikan keluar dari perulangan
sehingga Anda dapat memakainya, seperti yang ditunjukkan di sini:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

Sebelum perulangan, kita mendeklarasikan variabel bernama `counter` dan
menginisialisasinya ke `0`. Lalu, kita mendeklarasikan variabel bernama
`result` untuk menampung nilai yang dikembalikan dari perulangan. Pada setiap
iterasi perulangan, kita menambahkan `1` ke variabel `counter`, lalu memeriksa
apakah `counter` sama dengan `10`. Ketika ya, kita memakai keyword `break`
dengan nilai `counter * 2`. Setelah perulangan, kita memakai titik koma untuk
mengakhiri pernyataan yang menetapkan nilai ke `result`. Terakhir, kita
mencetak nilai di dalam `result`, yang pada kasus ini adalah `20`.

Anda juga dapat melakukan `return` dari dalam perulangan. Sementara `break`
hanya keluar dari perulangan saat ini, `return` selalu keluar dari fungsi saat
ini.

<!-- Old headings. Do not remove or links may break. -->
<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### Menghilangkan Ambiguitas dengan Label Perulangan

Jika Anda memiliki perulangan di dalam perulangan, `break` dan `continue`
berlaku pada perulangan paling dalam pada titik itu. Anda secara opsional
dapat menentukan label perulangan pada sebuah perulangan, yang kemudian dapat
Anda pakai bersama `break` atau `continue` untuk menyatakan bahwa keyword
tersebut berlaku pada perulangan yang berlabel alih-alih perulangan paling
dalam. Label perulangan harus diawali dengan tanda kutip tunggal. Berikut
contoh dengan dua perulangan bersarang:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

Perulangan luar memiliki label `'counting_up`, dan ia akan menghitung naik
dari 0 sampai 2. Perulangan dalam tanpa label menghitung turun dari 10 ke 9.
`break` pertama yang tidak menyebutkan label hanya akan keluar dari perulangan
dalam. Pernyataan `break 'counting_up;` akan keluar dari perulangan luar.
Kode ini mencetak:

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

<!-- Old headings. Do not remove or links may break. -->
<a id="conditional-loops-with-while"></a>

#### Menyederhanakan Perulangan Kondisional dengan while

Sebuah program sering kali perlu mengevaluasi sebuah kondisi di dalam
perulangan. Selama kondisinya `true`, perulangan berjalan. Ketika kondisinya
tidak lagi `true`, program memanggil `break`, menghentikan perulangan. Perilaku
seperti ini mungkin diimplementasikan memakai kombinasi `loop`, `if`, `else`,
dan `break`; Anda boleh mencobanya sekarang dalam sebuah program, jika mau.
Akan tetapi, pola ini sangat umum sehingga Rust memiliki konstruk bahasa
bawaan untuk itu, yang disebut perulangan `while`. Pada Listing 3-3, kita
memakai `while` untuk membuat program berulang tiga kali, menghitung mundur
setiap kali, lalu setelah perulangan, mencetak sebuah pesan dan keluar.

<Listing number="3-3" file-name="src/main.rs" caption="Memakai perulangan `while` untuk menjalankan kode selama sebuah kondisi mengevaluasi menjadi `true`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

Konstruk ini menghilangkan banyak penumpukan yang akan diperlukan jika Anda
memakai `loop`, `if`, `else`, dan `break`, dan ia pun lebih jelas. Selama
sebuah kondisi mengevaluasi menjadi `true`, kodenya berjalan; jika tidak,
program keluar dari perulangan.

<a id="looping-through-a-collection-with-for"></a>
#### Melakukan Perulangan pada Koleksi dengan `for`

Anda dapat memilih memakai konstruk `while` untuk melakukan perulangan pada
elemen-elemen sebuah koleksi, seperti array. Contohnya, perulangan pada
Listing 3-4 mencetak setiap elemen di dalam array `a`.

<Listing number="3-4" file-name="src/main.rs" caption="Melakukan perulangan pada setiap elemen koleksi dengan perulangan `while`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Di sini, kode menghitung naik menelusuri elemen-elemen dalam array. Ia mulai
dari indeks `0`, lalu berulang sampai mencapai indeks terakhir dalam array
(yaitu, ketika `index < 5` tidak lagi `true`). Menjalankan kode ini akan
mencetak setiap elemen dalam array:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

Kelima nilai array muncul di terminal, seperti yang diharapkan. Meskipun
`index` akan mencapai nilai `5` pada suatu titik, perulangan berhenti
mengeksekusi sebelum mencoba mengambil nilai keenam dari array.

Akan tetapi, pendekatan ini rawan error; kita dapat membuat program panic jika
nilai indeks atau kondisi pengujiannya salah. Contohnya, jika Anda mengubah
definisi array `a` menjadi empat elemen tetapi lupa memperbarui kondisinya
menjadi `while index < 4`, kodenya akan panic. Pendekatan ini juga lambat,
karena compiler menambahkan kode runtime untuk melakukan pemeriksaan
kondisional apakah indeks berada di dalam batas array pada setiap iterasi
perulangan.

Sebagai alternatif yang lebih ringkas, Anda dapat memakai perulangan `for` dan
mengeksekusi beberapa kode untuk setiap item dalam sebuah koleksi. Perulangan
`for` terlihat seperti kode pada Listing 3-5.

<Listing number="3-5" file-name="src/main.rs" caption="Melakukan perulangan pada setiap elemen koleksi dengan perulangan `for`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

Ketika kita menjalankan kode ini, kita akan melihat keluaran yang sama seperti
pada Listing 3-4. Yang lebih penting, kita kini telah meningkatkan keamanan
kode dan menghilangkan peluang munculnya bug yang mungkin timbul akibat
melampaui ujung array atau tidak melangkah cukup jauh sehingga melewatkan
beberapa item. Kode mesin yang dihasilkan dari perulangan `for` juga bisa
lebih efisien karena indeks tidak perlu dibandingkan dengan panjang array pada
setiap iterasi.

Dengan memakai perulangan `for`, Anda tidak perlu ingat untuk mengubah kode
lain jika Anda mengubah jumlah nilai dalam array, tidak seperti pada metode
yang dipakai di Listing 3-4.

Keamanan dan keringkasan perulangan `for` menjadikannya konstruk perulangan
yang paling sering dipakai di Rust. Bahkan pada situasi ketika Anda ingin
menjalankan kode sebanyak beberapa kali tertentu, seperti contoh hitung mundur
yang memakai perulangan `while` pada Listing 3-3, sebagian besar Rustacean
akan memakai perulangan `for`. Caranya adalah memakai `Range`, yang disediakan
oleh pustaka standar, yang membangkitkan semua angka secara berurutan mulai
dari satu angka dan berakhir sebelum angka lain.

Berikut tampilan hitung mundurnya jika memakai perulangan `for` dan metode
lain yang belum kita bahas, `rev`, untuk membalikkan range:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

Kode ini sedikit lebih bagus, bukan?

## Ringkasan

Anda berhasil! Ini adalah bab yang cukup panjang: Anda telah mempelajari
variabel, tipe data skalar dan majemuk, fungsi, komentar, ekspresi `if`, dan
perulangan! Untuk berlatih dengan konsep-konsep yang dibahas dalam bab ini,
cobalah membuat program yang melakukan hal-hal berikut:

- Mengonversi suhu antara Fahrenheit dan Celsius.
- Membangkitkan bilangan Fibonacci ke-*n*.
- Mencetak lirik lagu Natal “The Twelve Days of Christmas,” dengan
  memanfaatkan pengulangan dalam lagunya.

Ketika Anda siap melangkah, kita akan membahas sebuah konsep di Rust yang
_tidak_ umum ada di bahasa pemrograman lain: *ownership* (kepemilikan).

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess
