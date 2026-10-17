<a id="how-to-write-tests"></a>
## Cara Menulis Pengujian

*Test* (pengujian) adalah fungsi Rust yang memverifikasi bahwa kode
non-pengujian berfungsi sebagaimana yang diharapkan. Badan fungsi pengujian
biasanya melakukan tiga tindakan berikut:

- Menyiapkan data atau state yang diperlukan.
- Menjalankan kode yang ingin Anda uji.
- Menegaskan bahwa hasilnya sesuai dengan yang Anda harapkan.

Mari kita lihat fitur-fitur yang disediakan Rust secara khusus untuk
menulis pengujian yang melakukan tindakan-tindakan tersebut, yang meliputi
atribut `test`, beberapa macro, dan atribut `should_panic`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-anatomy-of-a-test-function"></a>

### Menyusun Fungsi Pengujian

Dalam bentuknya yang paling sederhana, sebuah pengujian di Rust adalah
fungsi yang dianotasi dengan atribut `test`. Atribut adalah metadata
tentang potongan-potongan kode Rust; salah satu contohnya adalah atribut
`derive` yang kita pakai bersama *struct* di Bab 5. Untuk mengubah sebuah
fungsi menjadi fungsi pengujian, tambahkan `#[test]` pada baris sebelum
`fn`. Ketika Anda menjalankan pengujian dengan perintah `cargo test`, Rust
membangun sebuah binary test runner yang menjalankan fungsi-fungsi yang
dianotasi dan melaporkan apakah setiap fungsi pengujian lulus atau gagal.

Setiap kali kita membuat proyek library baru dengan Cargo, sebuah *module*
(modul) pengujian dengan fungsi pengujian di dalamnya otomatis dibuatkan
untuk kita. Modul ini memberi Anda templat untuk menulis pengujian sehingga
Anda tidak perlu mencari tahu struktur dan sintaks persisnya setiap kali
memulai proyek baru. Anda bisa menambahkan fungsi pengujian dan modul
pengujian tambahan sebanyak yang Anda mau!

Kita akan mengeksplorasi beberapa aspek tentang cara kerja pengujian dengan
bereksperimen dengan pengujian templat itu sebelum kita benar-benar menguji
kode apa pun. Kemudian, kita akan menulis beberapa pengujian dunia nyata
yang memanggil kode yang telah kita tulis dan menegaskan bahwa perilakunya
benar.

Mari kita buat proyek library baru bernama `adder` yang akan menambahkan
dua angka:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

Isi file _src/lib.rs_ di library `adder` Anda seharusnya terlihat seperti
Listing 11-1.

<Listing number="11-1" file-name="src/lib.rs" caption="Kode yang dibuat otomatis oleh `cargo new`">

<!-- manual-regeneration
cd listings/ch11-writing-automated-tests
rm -rf listing-11-01
cargo new listing-11-01 --lib --name adder
cd listing-11-01
echo "$ cargo test" > output.txt
RUSTFLAGS="-A unused_variables -A dead_code" RUST_TEST_THREADS=1 cargo test >> output.txt 2>&1
git diff output.txt # commit any relevant changes; discard irrelevant ones
cd ../../..
-->

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

File ini dimulai dengan contoh fungsi `add` supaya kita punya sesuatu untuk
diuji.

Untuk saat ini, mari kita fokus hanya pada fungsi `it_works`. Perhatikan
anotasi `#[test]`: atribut ini menandakan bahwa ini adalah fungsi
pengujian, sehingga test runner tahu untuk memperlakukan fungsi ini sebagai
pengujian. Kita mungkin juga memiliki fungsi non-pengujian di modul `tests`
untuk membantu menyiapkan skenario umum atau melakukan operasi umum, jadi
kita selalu perlu menandai fungsi mana yang merupakan pengujian.

Badan fungsi contoh ini memakai macro `assert_eq!` untuk menegaskan bahwa
`result`, yang berisi hasil pemanggilan `add` dengan 2 dan 2, sama dengan 4.
Asersi ini berfungsi sebagai contoh format pengujian yang khas. Mari kita
jalankan untuk melihat bahwa pengujian ini lulus.

Perintah `cargo test` menjalankan semua pengujian dalam proyek kita,
seperti yang ditunjukkan di Listing 11-2.

<Listing number="11-2" caption="Keluaran dari menjalankan pengujian yang dibuat otomatis">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo mengompilasi dan menjalankan pengujian itu. Kita melihat baris
`running 1 test`. Baris berikutnya menunjukkan nama fungsi pengujian yang
dibuat, yaitu `tests::it_works`, dan bahwa hasil menjalankan pengujian
tersebut adalah `ok`. Ringkasan keseluruhan `test result: ok.` berarti
semua pengujian lulus, dan bagian yang berbunyi `1 passed; 0 failed`
menjumlahkan banyaknya pengujian yang lulus atau gagal.

Kita bisa menandai sebuah pengujian sebagai diabaikan supaya tidak
dijalankan dalam kasus tertentu; kita akan membahasnya di bagian
[“Mengabaikan Pengujian Kecuali Diminta Secara
Spesifik”][ignoring]<!-- ignore --> nanti di bab ini. Karena kita belum
melakukannya di sini, ringkasannya menunjukkan `0 ignored`. Kita juga bisa
meneruskan sebuah argumen ke perintah `cargo test` untuk menjalankan hanya
pengujian yang namanya cocok dengan sebuah string; ini disebut *filtering*
(penyaringan), dan kita akan membahasnya di bagian [“Menjalankan Sebagian
Pengujian Berdasarkan Nama”][subset]<!-- ignore -->. Di sini, kita belum
menyaring pengujian yang dijalankan, jadi di akhir ringkasan tertulis `0
filtered out`.

Statistik `0 measured` adalah untuk test benchmark yang mengukur kinerja.
Test benchmark, hingga tulisan ini dibuat, hanya tersedia di Rust nightly.
Lihat [dokumentasi tentang test benchmark][bench] untuk mempelajari lebih
lanjut.

Bagian keluaran pengujian berikutnya, yang dimulai dari `Doc-tests adder`,
adalah untuk hasil dari *documentation test* (test dokumentasi) mana pun.
Kita belum memiliki documentation test apa pun, tetapi Rust bisa
mengompilasi contoh kode mana pun yang muncul di dokumentasi API kita.
Fitur ini membantu menjaga dokumen dan kode Anda tetap sinkron! Kita akan
membahas cara menulis documentation test di bagian [“Komentar Dokumentasi
sebagai Pengujian”][doc-comments]<!-- ignore --> pada Bab 14. Untuk saat
ini, kita akan mengabaikan keluaran `Doc-tests`.

Mari kita mulai menyesuaikan pengujian itu dengan kebutuhan kita sendiri.
Pertama, ubah nama fungsi `it_works` menjadi nama yang berbeda, misalnya
`exploration`, seperti ini:

<span class="filename">Nama File: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Lalu, jalankan `cargo test` lagi. Keluarannya sekarang menunjukkan
`exploration`, bukan `it_works`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Sekarang kita akan menambahkan pengujian lain, tetapi kali ini kita akan
membuat pengujian yang gagal! Sebuah pengujian gagal ketika ada sesuatu di
fungsi pengujian yang panic. Setiap pengujian dijalankan dalam thread baru,
dan ketika thread utama melihat bahwa thread pengujian telah mati,
pengujian itu ditandai sebagai gagal. Di Bab 9, kita membahas bahwa cara
paling sederhana untuk panic adalah memanggil macro `panic!`. Masukkan
pengujian baru itu sebagai fungsi bernama `another`, sehingga file
_src/lib.rs_ Anda terlihat seperti Listing 11-3.

<Listing number="11-3" file-name="src/lib.rs" caption="Menambahkan pengujian kedua yang akan gagal karena kita memanggil macro `panic!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Jalankan pengujian lagi memakai `cargo test`. Keluarannya seharusnya
terlihat seperti Listing 11-4, yang menunjukkan bahwa pengujian
`exploration` kita lulus dan `another` gagal.

<Listing number="11-4" caption="Hasil pengujian ketika satu pengujian lulus dan satu pengujian gagal">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
 -->

Alih-alih `ok`, baris `test tests::another` menunjukkan `FAILED`. Dua
bagian baru muncul di antara hasil individual dan ringkasannya: yang
pertama menampilkan alasan detail dari setiap kegagalan pengujian. Dalam
kasus ini, kita mendapatkan detail bahwa `tests::another` gagal karena ia
panic dengan pesan `Make this test fail` pada baris 17 di file _src/lib.rs_.
Bagian berikutnya mendaftarkan nama semua pengujian yang gagal, yang
berguna ketika ada banyak pengujian dan banyak keluaran detail pengujian
yang gagal. Kita bisa memakai nama pengujian yang gagal untuk menjalankan
pengujian itu saja supaya lebih mudah men-debug-nya; kita akan membahas
lebih lanjut cara-cara menjalankan pengujian di bagian [“Mengontrol Cara
Pengujian Dijalankan”][controlling-how-tests-are-run]<!-- ignore -->.

Baris ringkasan muncul di akhir: secara keseluruhan, hasil pengujian kita
adalah `FAILED`. Kita memiliki satu pengujian yang lulus dan satu yang
gagal.

Sekarang setelah Anda melihat seperti apa hasil pengujian dalam berbagai
skenario, mari kita lihat beberapa macro selain `panic!` yang berguna
dalam pengujian.

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>

### Memeriksa Hasil dengan `assert!`

Macro `assert!`, yang disediakan pustaka standar, berguna ketika Anda ingin
memastikan bahwa sebuah kondisi dalam pengujian bernilai `true`. Kita
memberi macro `assert!` sebuah argumen yang bernilai Boolean. Jika nilainya
`true`, tidak ada yang terjadi dan pengujian lulus. Jika nilainya `false`,
macro `assert!` memanggil `panic!` untuk membuat pengujian gagal. Memakai
macro `assert!` membantu kita memeriksa bahwa kode kita berfungsi sesuai
yang kita maksudkan.

Di Bab 5, Listing 5-15, kita memakai struct `Rectangle` dan metode
`can_hold`, yang diulang di sini di Listing 11-5. Mari kita letakkan kode
ini di file _src/lib.rs_, lalu menulis beberapa pengujian untuknya memakai
macro `assert!`.

<Listing number="11-5" file-name="src/lib.rs" caption="Struct `Rectangle` dan metode `can_hold`-nya dari Bab 5">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

Metode `can_hold` mengembalikan sebuah Boolean, yang berarti ini adalah
kasus pemakaian yang sempurna untuk macro `assert!`. Di Listing 11-6, kita
menulis pengujian yang melatih metode `can_hold` dengan membuat instance
`Rectangle` yang memiliki lebar 8 dan tinggi 7, lalu menegaskan bahwa ia
bisa menampung instance `Rectangle` lain yang memiliki lebar 5 dan tinggi 1.

<Listing number="11-6" file-name="src/lib.rs" caption="Pengujian untuk `can_hold` yang memeriksa apakah persegi panjang yang lebih besar memang bisa menampung persegi panjang yang lebih kecil">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Perhatikan baris `use super::*;` di dalam modul `tests`. Modul `tests`
adalah modul biasa yang mengikuti aturan visibilitas yang kita bahas di Bab
7 pada bagian [“Path untuk Merujuk Item di dalam Pohon
Modul”][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore -->.
Karena modul `tests` adalah modul dalam, kita perlu membawa kode yang
sedang diuji di modul luar ke dalam scope modul dalam. Kita memakai glob di
sini, sehingga apa pun yang kita definisikan di modul luar tersedia untuk
modul `tests` ini.

Kita telah menamai pengujian kita `larger_can_hold_smaller`, dan kita telah
membuat dua instance `Rectangle` yang kita perlukan. Kemudian, kita
memanggil macro `assert!` dan meneruskan kepadanya hasil pemanggilan
`larger.can_hold(&smaller)`. Ekspresi ini seharusnya mengembalikan `true`,
jadi pengujian kita seharusnya lulus. Mari kita cari tahu!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Ternyata memang lulus! Mari kita tambahkan pengujian lain, kali ini
menegaskan bahwa persegi panjang yang lebih kecil tidak bisa menampung
persegi panjang yang lebih besar:

<span class="filename">Nama File: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Karena hasil yang benar dari fungsi `can_hold` dalam kasus ini adalah
`false`, kita perlu menegasikan hasil itu sebelum meneruskannya ke macro
`assert!`. Alhasil, pengujian kita akan lulus jika `can_hold` mengembalikan
`false`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Dua pengujian lulus! Sekarang mari kita lihat apa yang terjadi pada hasil
pengujian kita ketika kita memasukkan bug ke dalam kode kita. Kita akan
mengubah implementasi metode `can_hold` dengan mengganti tanda lebih besar
dari (`>`) menjadi tanda lebih kecil dari (`<`) ketika ia membandingkan
lebarnya:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

Menjalankan pengujian sekarang menghasilkan hal berikut:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

Pengujian kita menangkap bug itu! Karena `larger.width` adalah `8` dan
`smaller.width` adalah `5`, perbandingan lebar di `can_hold` sekarang
mengembalikan `false`: 8 tidak lebih kecil dari 5.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-equality-with-the-assert_eq-and-assert_ne-macros"></a>

### Menguji Kesamaan dengan `assert_eq!` dan `assert_ne!`

Cara umum untuk memverifikasi fungsionalitas adalah menguji kesamaan antara
hasil kode yang sedang diuji dan nilai yang Anda harapkan dikembalikan kode
itu. Anda bisa melakukannya dengan memakai macro `assert!` dan meneruskan
kepadanya ekspresi yang memakai operator `==`. Namun, ini adalah pengujian
yang begitu umum sehingga pustaka standar menyediakan sepasang
macro—`assert_eq!` dan `assert_ne!`—untuk melakukan pengujian ini dengan
lebih nyaman. Macro-macro ini masing-masing membandingkan kesamaan atau
ketidaksamaan dua argumen. Mereka juga akan mencetak kedua nilai itu jika
asersinya gagal, yang memudahkan kita melihat _alasan_ pengujian gagal;
sebaliknya, macro `assert!` hanya menandakan bahwa ia mendapatkan nilai
`false` untuk ekspresi `==`, tanpa mencetak nilai-nilai yang menyebabkan
nilai `false` itu.

Di Listing 11-7, kita menulis fungsi bernama `add_two` yang menambahkan `2`
ke parameternya, lalu kita menguji fungsi ini memakai macro `assert_eq!`.

<Listing number="11-7" file-name="src/lib.rs" caption="Menguji fungsi `add_two` memakai macro `assert_eq!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Mari kita periksa bahwa ia lulus!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Kita membuat variabel bernama `result` yang menampung hasil pemanggilan
`add_two(2)`. Lalu, kita meneruskan `result` dan `4` sebagai argumen ke
macro `assert_eq!`. Baris keluaran untuk pengujian ini adalah `test
tests::it_adds_two ... ok`, dan teks `ok` menandakan bahwa pengujian kita
lulus!

Mari kita masukkan bug ke dalam kode kita untuk melihat seperti apa
`assert_eq!` ketika gagal. Ubah implementasi fungsi `add_two` menjadi
menambahkan `3`:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Jalankan pengujian lagi:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

Pengujian kita menangkap bug itu! Pengujian `tests::it_adds_two` gagal, dan
pesannya memberi tahu kita bahwa asersi yang gagal adalah `left == right`
serta berapa nilai `left` dan `right`. Pesan ini membantu kita mulai
men-debug: argumen `left`, tempat kita meletakkan hasil pemanggilan
`add_two(2)`, adalah `5`, tetapi argumen `right` adalah `4`. Anda bisa
membayangkan bahwa ini akan sangat membantu ketika kita memiliki banyak
pengujian yang sedang berjalan.

Perhatikan bahwa di beberapa bahasa dan framework pengujian, parameter
fungsi asersi kesamaan disebut `expected` dan `actual`, dan urutan kita
menentukan argumen itu penting. Namun, di Rust, mereka disebut `left` dan
`right`, dan urutan kita menentukan nilai yang kita harapkan dan nilai yang
dihasilkan kode tidak penting. Kita bisa menulis asersi di pengujian ini
sebagai `assert_eq!(4, result)`, yang akan menghasilkan pesan kegagalan
yang sama yang menampilkan `` assertion `left == right` failed ``.

Macro `assert_ne!` akan lulus jika dua nilai yang kita berikan tidak sama
dan akan gagal jika keduanya sama. Macro ini paling berguna untuk kasus
ketika kita tidak yakin nilai apa yang _akan_ dihasilkan, tetapi kita tahu
nilai apa yang pasti _tidak seharusnya_ dihasilkan. Sebagai contoh, jika
kita menguji fungsi yang dijamin mengubah masukannya dengan cara tertentu,
tetapi cara masukannya diubah bergantung pada hari dalam seminggu saat kita
menjalankan pengujian, hal terbaik untuk ditegaskan mungkin adalah bahwa
keluaran fungsinya tidak sama dengan masukannya.

Di balik layar, macro `assert_eq!` dan `assert_ne!` masing-masing memakai
operator `==` dan `!=`. Ketika asersinya gagal, macro-macro ini mencetak
argumennya memakai pemformatan debug, yang berarti nilai yang dibandingkan
harus mengimplementasikan *trait* `PartialEq` dan `Debug`. Semua tipe
primitif dan sebagian besar tipe pustaka standar mengimplementasikan trait
ini. Untuk struct dan *enum* yang Anda definisikan sendiri, Anda perlu
mengimplementasikan `PartialEq` untuk menegaskan kesamaan tipe-tipe itu.
Anda juga perlu mengimplementasikan `Debug` untuk mencetak nilai-nilainya
ketika asersinya gagal. Karena kedua trait itu adalah trait yang dapat
diturunkan, seperti yang disebutkan di Listing 5-12 pada Bab 5, ini
biasanya semudah menambahkan anotasi `#[derive(PartialEq, Debug)]` ke
definisi struct atau enum Anda. Lihat Lampiran C, [“Trait yang Dapat
Diturunkan,”][derivable-traits]<!-- ignore --> untuk detail lebih lanjut
tentang trait-trait yang dapat diturunkan ini dan yang lainnya.

### Menambahkan Pesan Kegagalan Kustom

Anda juga bisa menambahkan pesan kustom untuk dicetak bersama pesan
kegagalan sebagai argumen opsional ke macro `assert!`, `assert_eq!`, dan
`assert_ne!`. Argumen apa pun yang ditentukan setelah argumen wajib
diteruskan ke macro `format!` (dibahas di [“Menggabungkan dengan `+` atau
`format!`”][concatenating]<!--
ignore --> di Bab 8), jadi Anda bisa meneruskan string format yang berisi
placeholder `{}` dan nilai-nilai untuk mengisi placeholder itu. Pesan
kustom berguna untuk mendokumentasikan makna sebuah asersi; ketika sebuah
pengujian gagal, Anda akan mendapat gambaran yang lebih baik tentang apa
masalahnya dengan kode itu.

Sebagai contoh, katakanlah kita memiliki fungsi yang menyapa orang
berdasarkan nama dan kita ingin menguji bahwa nama yang kita teruskankan ke
fungsi itu muncul di keluarannya:

<span class="filename">Nama File: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

Persyaratan untuk program ini belum disepakati, dan kita cukup yakin bahwa
teks `Hello` di awal sapaan akan berubah. Kita memutuskan untuk tidak perlu
memperbarui pengujian ketika persyaratannya berubah, jadi alih-alih
memeriksa kesamaan persis dengan nilai yang dikembalikan fungsi `greeting`,
kita hanya menegaskan bahwa keluarannya mengandung teks parameter
masukannya.

Sekarang mari kita masukkan bug ke dalam kode ini dengan mengubah
`greeting` agar tidak menyertakan `name` untuk melihat seperti apa kegagalan
pengujian bawaan:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

Menjalankan pengujian ini menghasilkan hal berikut:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

Hasil ini hanya menandakan bahwa asersinya gagal dan di baris mana asersi
itu berada. Pesan kegagalan yang lebih berguna akan mencetak nilai dari
fungsi `greeting`. Mari kita tambahkan pesan kegagalan kustom yang terdiri
atas string format dengan placeholder yang diisi dengan nilai aktual yang
kita dapatkan dari fungsi `greeting`:

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

Sekarang ketika kita menjalankan pengujian, kita akan mendapatkan pesan
galat yang lebih informatif:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

Kita bisa melihat nilai yang sebenarnya kita dapatkan di keluaran
pengujian, yang akan membantu kita men-debug apa yang terjadi alih-alih apa
yang kita harapkan terjadi.

### Memeriksa Panic dengan `should_panic`

Selain memeriksa nilai kembalian, penting untuk memeriksa bahwa kode kita
menangani kondisi galat seperti yang kita harapkan. Sebagai contoh,
perhatikan tipe `Guess` yang kita buat di Bab 9, Listing 9-13. Kode lain
yang memakai `Guess` bergantung pada jaminan bahwa instance `Guess` hanya
akan berisi nilai antara 1 dan 100. Kita bisa menulis pengujian yang
memastikan bahwa percobaan membuat instance `Guess` dengan nilai di luar
rentang itu akan panic.

Kita melakukannya dengan menambahkan atribut `should_panic` ke fungsi
pengujian kita. Pengujian lulus jika kode di dalam fungsi itu panic;
pengujian gagal jika kode di dalam fungsi itu tidak panic.

Listing 11-8 menunjukkan pengujian yang memeriksa bahwa kondisi galat
`Guess::new` terjadi ketika kita mengharapkannya.

<Listing number="11-8" file-name="src/lib.rs" caption="Menguji bahwa sebuah kondisi akan menyebabkan `panic!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

Kita menempatkan atribut `#[should_panic]` setelah atribut `#[test]` dan
sebelum fungsi pengujian yang diatributinya. Mari kita lihat hasilnya
ketika pengujian ini lulus:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Terlihat bagus! Sekarang mari kita masukkan bug ke dalam kode kita dengan
menghapus kondisi bahwa fungsi `new` akan panic jika nilainya lebih besar
dari 100:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Ketika kita menjalankan pengujian di Listing 11-8, ia akan gagal:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

Kita tidak mendapatkan pesan yang sangat membantu dalam kasus ini, tetapi
ketika kita melihat fungsi pengujiannya, kita melihat bahwa ia dianotasi
dengan `#[should_panic]`. Kegagalan yang kita dapatkan berarti kode di
fungsi pengujian tidak menyebabkan panic.

Pengujian yang memakai `should_panic` bisa tidak presisi. Pengujian
`should_panic` akan lulus bahkan jika pengujian itu panic karena alasan
yang berbeda dari yang kita harapkan. Untuk membuat pengujian
`should_panic` lebih presisi, kita bisa menambahkan parameter opsional
`expected` ke atribut `should_panic`. Test harness akan memastikan bahwa
pesan kegagalannya mengandung teks yang diberikan. Sebagai contoh,
perhatikan kode `Guess` yang dimodifikasi di Listing 11-9, ketika fungsi
`new` panic dengan pesan yang berbeda tergantung pada apakah nilainya
terlalu kecil atau terlalu besar.

<Listing number="11-9" file-name="src/lib.rs" caption="Menguji `panic!` dengan pesan panic yang mengandung substring tertentu">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

Pengujian ini akan lulus karena nilai yang kita letakkan di parameter
`expected` atribut `should_panic` adalah substring dari pesan yang dipakai
fungsi `Guess::new` untuk panic. Kita bisa saja menentukan seluruh pesan
panic yang kita harapkan, yang dalam kasus ini adalah `Guess value must be
less than or equal to 100, got 200`. Apa yang Anda pilih untuk ditentukan
bergantung pada seberapa unik atau dinamis pesan panic itu dan seberapa
presisi Anda ingin pengujiannya. Dalam kasus ini, substring dari pesan
panic sudah cukup untuk memastikan bahwa kode di fungsi pengujian
mengeksekusi kasus `else if value > 100`.

Untuk melihat apa yang terjadi ketika pengujian `should_panic` dengan pesan
`expected` gagal, mari kita masukkan lagi bug ke dalam kode kita dengan
menukar badan blok `if value < 1` dan blok `else if value > 100`:

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Kali ini ketika kita menjalankan pengujian `should_panic`, ia akan gagal:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

Pesan kegagalannya menandakan bahwa pengujian ini memang panic seperti yang
kita harapkan, tetapi pesan panic-nya tidak menyertakan string yang
diharapkan `less than or equal to 100`. Pesan panic yang sebenarnya kita
dapatkan dalam kasus ini adalah `Guess value must be greater than or equal
to 1, got 200`. Sekarang kita bisa mulai mencari tahu di mana bug kita!

### Memakai `Result<T, E>` dalam Pengujian

Semua pengujian kita sejauh ini panic ketika gagal. Kita juga bisa menulis
pengujian yang memakai `Result<T, E>`! Berikut pengujian dari Listing 11-1,
ditulis ulang untuk memakai `Result<T, E>` dan mengembalikan `Err` alih-alih
panic:

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

Fungsi `it_works` sekarang memiliki tipe kembalian `Result<(), String>`. Di
badan fungsi, alih-alih memanggil macro `assert_eq!`, kita mengembalikan
`Ok(())` ketika pengujian lulus dan `Err` dengan `String` di dalamnya
ketika pengujian gagal.

Menulis pengujian sehingga ia mengembalikan `Result<T, E>` memungkinkan
Anda memakai operator tanda tanya di badan pengujian, yang bisa menjadi
cara yang nyaman untuk menulis pengujian yang seharusnya gagal jika operasi
mana pun di dalamnya mengembalikan varian `Err`.

Anda tidak bisa memakai anotasi `#[should_panic]` pada pengujian yang
memakai `Result<T, E>`. Untuk menegaskan bahwa sebuah operasi mengembalikan
varian `Err`, _jangan_ memakai operator tanda tanya pada nilai `Result<T,
E>` itu. Sebagai gantinya, pakailah `assert!(value.is_err())`.

Sekarang setelah Anda tahu beberapa cara menulis pengujian, mari kita lihat
apa yang terjadi ketika kita menjalankan pengujian kita dan menjelajahi
opsi-opsi berbeda yang bisa kita pakai bersama `cargo test`.

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: ../unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
