<a id="how-to-write-tests"></a>
## Cara Menulis Test

*Test* (test) adalah fungsi Rust yang memverifikasi bahwa kode
non-test berfungsi sebagaimana yang diharapkan. Badan fungsi test
biasanya melakukan tiga tindakan berikut:

- Menyiapkan data atau state yang diperlukan.
- Menjalankan kode yang ingin Anda uji.
- Menegaskan bahwa hasilnya sesuai dengan yang Anda harapkan.

Mari kita lihat fitur-fitur yang disediakan Rust secara khusus untuk
menulis test yang melakukan tindakan-tindakan tersebut, yang meliputi
atribut `test`, beberapa *macro*, dan atribut `should_panic`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-anatomy-of-a-test-function"></a>

### Menyusun Fungsi Test

Dalam bentuknya yang paling sederhana, sebuah test di Rust adalah
fungsi yang dianotasi dengan atribut `test`. Atribut adalah metadata
tentang potongan-potongan kode Rust; salah satu contohnya adalah atribut
`derive` yang kita pakai bersama *struct* di Bab 5. Untuk mengubah sebuah
fungsi menjadi fungsi test, tambahkan `#[test]` pada baris sebelum
`fn`. Ketika Anda menjalankan test dengan perintah `cargo test`, Rust
membangun sebuah binary test runner yang menjalankan fungsi-fungsi yang
dianotasi dan melaporkan apakah setiap fungsi test lulus atau gagal.

Setiap kali kita membuat proyek library baru dengan Cargo, sebuah *module*
(modul) test dengan fungsi test di dalamnya otomatis dibuatkan
untuk kita. Modul ini memberi Anda templat untuk menulis test sehingga
Anda tidak perlu mencari tahu struktur dan sintaks persisnya setiap kali
memulai proyek baru. Anda bisa menambahkan fungsi test dan modul
test tambahan sebanyak yang Anda mau!

Kita akan mengeksplorasi beberapa aspek tentang cara kerja test dengan
bereksperimen dengan test templat itu sebelum kita benar-benar menguji
kode apa pun. Kemudian, kita akan menulis beberapa test dunia nyata
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
test, sehingga test runner tahu untuk memperlakukan fungsi ini sebagai
test. Kita mungkin juga memiliki fungsi non-test di modul `tests`
untuk membantu menyiapkan skenario umum atau melakukan operasi umum, jadi
kita selalu perlu menandai fungsi mana yang merupakan test.

Badan fungsi contoh ini memakai *macro* `assert_eq!` untuk menegaskan bahwa
`result`, yang berisi hasil pemanggilan `add` dengan 2 dan 2, sama dengan 4.
Asersi ini berfungsi sebagai contoh format test yang khas. Mari kita
jalankan untuk melihat bahwa test ini lulus.

Perintah `cargo test` menjalankan semua test dalam proyek kita,
seperti yang ditunjukkan di Listing 11-2.

<Listing number="11-2" caption="Output dari menjalankan test yang dibuat otomatis">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo mengompilasi dan menjalankan test itu. Kita melihat baris
`running 1 test`. Baris berikutnya menunjukkan nama fungsi test yang
dibuat, yaitu `tests::it_works`, dan bahwa hasil menjalankan test
tersebut adalah `ok`. Ringkasan keseluruhan `test result: ok.` berarti
semua test lulus, dan bagian yang berbunyi `1 passed; 0 failed`
menjumlahkan banyaknya test yang lulus atau gagal.

Kita bisa menandai sebuah test sebagai diabaikan supaya tidak
dijalankan dalam kasus tertentu; kita akan membahasnya di bagian
[“Mengabaikan Test Kecuali Diminta Secara
Spesifik”][ignoring]<!-- ignore --> nanti di bab ini. Karena kita belum
melakukannya di sini, ringkasannya menunjukkan `0 ignored`. Kita juga bisa
meneruskan sebuah argumen ke perintah `cargo test` untuk menjalankan hanya
test yang namanya cocok dengan sebuah string; ini disebut *filtering*
(filtering), dan kita akan membahasnya di bagian [“Menjalankan Sebagian
Test Berdasarkan Nama”][subset]<!-- ignore -->. Di sini, kita belum
menyaring test yang dijalankan, jadi di akhir ringkasan tertulis `0
filtered out`.

Statistik `0 measured` adalah untuk test benchmark yang mengukur kinerja.
Test benchmark, hingga tulisan ini dibuat, hanya tersedia di Rust nightly.
Lihat [dokumentasi tentang test benchmark][bench] untuk mempelajari lebih
lanjut.

Bagian output test berikutnya, yang dimulai dari `Doc-tests adder`,
adalah untuk hasil dari *documentation test* (test dokumentasi) mana pun.
Kita belum memiliki *documentation test* apa pun, tetapi Rust bisa
mengompilasi contoh kode mana pun yang muncul di dokumentasi API kita.
Fitur ini membantu menjaga dokumen dan kode Anda tetap sinkron! Kita akan
membahas cara menulis *documentation test* di bagian [“Komentar Dokumentasi
sebagai Test”][doc-comments]<!-- ignore --> pada Bab 14. Untuk saat
ini, kita akan mengabaikan output `Doc-tests`.

Mari kita mulai menyesuaikan test itu dengan kebutuhan kita sendiri.
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

Sekarang kita akan menambahkan test lain, tetapi kali ini kita akan
membuat test yang gagal! Sebuah test gagal ketika ada sesuatu di
fungsi test yang panic. Setiap test dijalankan dalam thread baru,
dan ketika thread utama melihat bahwa thread test telah mati,
test itu ditandai sebagai gagal. Di Bab 9, kita membahas bahwa cara
paling sederhana untuk panic adalah memanggil *macro* `panic!`. Masukkan
test baru itu sebagai fungsi bernama `another`, sehingga file
_src/lib.rs_ Anda terlihat seperti Listing 11-3.

<Listing number="11-3" file-name="src/lib.rs" caption="Menambahkan test kedua yang akan gagal karena kita memanggil macro `panic!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Jalankan test lagi memakai `cargo test`. Keluarannya seharusnya
terlihat seperti Listing 11-4, yang menunjukkan bahwa test
`exploration` kita lulus dan `another` gagal.

<Listing number="11-4" caption="Hasil test ketika satu test lulus dan satu test gagal">

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
pertama menampilkan alasan detail dari setiap kegagalan test. Dalam
kasus ini, kita mendapatkan detail bahwa `tests::another` gagal karena ia
panic dengan pesan `Make this test fail` pada baris 17 di file _src/lib.rs_.
Bagian berikutnya mendaftarkan nama semua test yang gagal, yang
berguna ketika ada banyak test dan banyak output detail test
yang gagal. Kita bisa memakai nama test yang gagal untuk menjalankan
test itu saja supaya lebih mudah men-debug-nya; kita akan membahas
lebih lanjut cara-cara menjalankan test di bagian [“Mengontrol Cara
Test Dijalankan”][controlling-how-tests-are-run]<!-- ignore -->.

Baris ringkasan muncul di akhir: secara keseluruhan, hasil test kita
adalah `FAILED`. Kita memiliki satu test yang lulus dan satu yang
gagal.

Sekarang setelah Anda melihat seperti apa hasil test dalam berbagai
skenario, mari kita lihat beberapa *macro* selain `panic!` yang berguna
dalam test.

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>

### Memeriksa Hasil dengan `assert!`

*Macro* `assert!`, yang disediakan standard library, berguna ketika Anda ingin
memastikan bahwa sebuah kondisi dalam test bernilai `true`. Kita
memberi *macro* `assert!` sebuah argumen yang bernilai Boolean. Jika nilainya
`true`, tidak ada yang terjadi dan test lulus. Jika nilainya `false`,
*macro* `assert!` memanggil `panic!` untuk membuat test gagal. Memakai
*macro* `assert!` membantu kita memeriksa bahwa kode kita berfungsi sesuai
yang kita maksudkan.

Di Bab 5, Listing 5-15, kita memakai *struct* `Rectangle` dan method
`can_hold`, yang diulang di sini di Listing 11-5. Mari kita letakkan kode
ini di file _src/lib.rs_, lalu menulis beberapa test untuknya memakai
*macro* `assert!`.

<Listing number="11-5" file-name="src/lib.rs" caption="Struct `Rectangle` dan method `can_hold`-nya dari Bab 5">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

Method `can_hold` mengembalikan sebuah Boolean, yang berarti ini adalah
kasus pemakaian yang sempurna untuk *macro* `assert!`. Di Listing 11-6, kita
menulis test yang melatih method `can_hold` dengan membuat instance
`Rectangle` yang memiliki lebar 8 dan tinggi 7, lalu menegaskan bahwa ia
bisa menampung instance `Rectangle` lain yang memiliki lebar 5 dan tinggi 1.

<Listing number="11-6" file-name="src/lib.rs" caption="Test untuk `can_hold` yang memeriksa apakah persegi panjang yang lebih besar memang bisa menampung persegi panjang yang lebih kecil">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Perhatikan baris `use super::*;` di dalam modul `tests`. Modul `tests`
adalah modul biasa yang mengikuti aturan visibilitas yang kita bahas di Bab
7 pada bagian [“*Path* untuk Merujuk Item di dalam Pohon
Modul”][*paths*-for-referring-to-an-item-in-the-module-tree]<!-- ignore -->.
Karena modul `tests` adalah modul dalam, kita perlu membawa kode yang
sedang diuji di modul luar ke dalam *scope* modul dalam. Kita memakai glob di
sini, sehingga apa pun yang kita definisikan di modul luar tersedia untuk
modul `tests` ini.

Kita telah menamai test kita `larger_can_hold_smaller`, dan kita telah
membuat dua instance `Rectangle` yang kita perlukan. Kemudian, kita
memanggil *macro* `assert!` dan meneruskan kepadanya hasil pemanggilan
`larger.can_hold(&smaller)`. Expression ini seharusnya mengembalikan `true`,
jadi test kita seharusnya lulus. Mari kita cari tahu!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Ternyata memang lulus! Mari kita tambahkan test lain, kali ini
menegaskan bahwa persegi panjang yang lebih kecil tidak bisa menampung
persegi panjang yang lebih besar:

<span class="filename">Nama File: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Karena hasil yang benar dari fungsi `can_hold` dalam kasus ini adalah
`false`, kita perlu menegasikan hasil itu sebelum meneruskannya ke *macro*
`assert!`. Alhasil, test kita akan lulus jika `can_hold` mengembalikan
`false`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Dua test lulus! Sekarang mari kita lihat apa yang terjadi pada hasil
test kita ketika kita memasukkan bug ke dalam kode kita. Kita akan
mengubah implementasi method `can_hold` dengan mengganti tanda lebih besar
dari (`>`) menjadi tanda lebih kecil dari (`<`) ketika ia membandingkan
lebarnya:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

Menjalankan test sekarang menghasilkan hal berikut:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

Test kita menangkap bug itu! Karena `larger.width` adalah `8` dan
`smaller.width` adalah `5`, perbandingan lebar di `can_hold` sekarang
mengembalikan `false`: 8 tidak lebih kecil dari 5.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-equality-with-the-assert_eq-and-assert_ne-macros"></a>

### Menguji Kesamaan dengan `assert_eq!` dan `assert_ne!`

Cara umum untuk memverifikasi fungsionalitas adalah menguji kesamaan antara
hasil kode yang sedang diuji dan nilai yang Anda harapkan dikembalikan kode
itu. Anda bisa melakukannya dengan memakai *macro* `assert!` dan meneruskan
kepadanya expression yang memakai operator `==`. Namun, ini adalah test
yang begitu umum sehingga standard library menyediakan sepasang
*macro*—`assert_eq!` dan `assert_ne!`—untuk melakukan test ini dengan
lebih nyaman. *Macro*-macro ini masing-masing membandingkan kesamaan atau
ketidaksamaan dua argumen. Mereka juga akan mencetak kedua nilai itu jika
asersinya gagal, yang memudahkan kita melihat _alasan_ test gagal;
sebaliknya, *macro* `assert!` hanya menandakan bahwa ia mendapatkan nilai
`false` untuk expression `==`, tanpa mencetak nilai-nilai yang menyebabkan
nilai `false` itu.

Di Listing 11-7, kita menulis fungsi bernama `add_two` yang menambahkan `2`
ke parameternya, lalu kita menguji fungsi ini memakai *macro* `assert_eq!`.

<Listing number="11-7" file-name="src/lib.rs" caption="Menguji fungsi `add_two` memakai macro `assert_eq!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Mari kita periksa bahwa ia lulus!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Kita membuat variable bernama `result` yang menampung hasil pemanggilan
`add_two(2)`. Lalu, kita meneruskan `result` dan `4` sebagai argumen ke
*macro* `assert_eq!`. Baris output untuk test ini adalah `test
tests::it_adds_two ... ok`, dan teks `ok` menandakan bahwa test kita
lulus!

Mari kita masukkan bug ke dalam kode kita untuk melihat seperti apa
`assert_eq!` ketika gagal. Ubah implementasi fungsi `add_two` menjadi
menambahkan `3`:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Jalankan test lagi:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

Test kita menangkap bug itu! Test `tests::it_adds_two` gagal, dan
pesannya memberi tahu kita bahwa asersi yang gagal adalah `left == right`
serta berapa nilai `left` dan `right`. Pesan ini membantu kita mulai
men-debug: argumen `left`, tempat kita meletakkan hasil pemanggilan
`add_two(2)`, adalah `5`, tetapi argumen `right` adalah `4`. Anda bisa
membayangkan bahwa ini akan sangat membantu ketika kita memiliki banyak
test yang sedang berjalan.

Perhatikan bahwa di beberapa bahasa dan framework test, parameter
fungsi asersi kesamaan disebut `expected` dan `actual`, dan urutan saat kita
menentukan argumen itu penting. Namun, di Rust, mereka disebut `left` dan
`right`, dan urutan saat kita menentukan nilai yang kita harapkan dan nilai yang
dihasilkan kode tidak penting. Kita bisa menulis asersi di test ini
sebagai `assert_eq!(4, result)`, yang akan menghasilkan pesan kegagalan
yang sama yang menampilkan `` assertion `left == right` failed ``.

*Macro* `assert_ne!` akan lulus jika dua nilai yang kita berikan tidak sama
dan akan gagal jika keduanya sama. *Macro* ini paling berguna untuk kasus
ketika kita tidak yakin nilai apa yang _akan_ dihasilkan, tetapi kita tahu
nilai apa yang pasti _tidak seharusnya_ dihasilkan. Sebagai contoh, jika
kita menguji fungsi yang dijamin mengubah inputnya dengan cara tertentu,
tetapi cara inputnya diubah bergantung pada hari dalam seminggu saat kita
menjalankan test, hal terbaik untuk ditegaskan mungkin adalah bahwa
output fungsinya tidak sama dengan inputnya.

Di balik layar, *macro* `assert_eq!` dan `assert_ne!` masing-masing memakai
operator `==` dan `!=`. Ketika asersinya gagal, *macro*-macro ini mencetak
argumennya memakai pemformatan debug, yang berarti nilai yang dibandingkan
harus mengimplementasikan *trait* `PartialEq` dan `Debug`. Semua type
primitif dan sebagian besar type standard library mengimplementasikan *trait*
ini. Untuk *struct* dan *enum* yang Anda definisikan sendiri, Anda perlu
mengimplementasikan `PartialEq` untuk menegaskan kesamaan type-type itu.
Anda juga perlu mengimplementasikan `Debug` untuk mencetak nilai-nilainya
ketika asersinya gagal. Karena kedua *trait* itu adalah *trait* yang dapat
diturunkan, seperti yang disebutkan di Listing 5-12 pada Bab 5, ini
biasanya semudah menambahkan anotasi `#[derive(PartialEq, Debug)]` ke
definisi *struct* atau *enum* Anda. Lihat Lampiran C, [“*Trait* yang Dapat
Diturunkan,”][derivable-traits]<!-- ignore --> untuk detail lebih lanjut
tentang *trait*-trait yang dapat diturunkan ini dan yang lainnya.

### Menambahkan Pesan Kegagalan Kustom

Anda juga bisa menambahkan pesan kustom untuk dicetak bersama pesan
kegagalan sebagai argumen opsional ke *macro* `assert!`, `assert_eq!`, dan
`assert_ne!`. Argumen apa pun yang ditentukan setelah argumen wajib
diteruskan ke *macro* `format!` (dibahas di [“Menggabungkan dengan `+` atau
`format!`”][concatenating]<!--
ignore --> di Bab 8), jadi Anda bisa meneruskan string format yang berisi
placeholder `{}` dan nilai-nilai untuk mengisi placeholder itu. Pesan
kustom berguna untuk mendokumentasikan makna sebuah asersi; ketika sebuah
test gagal, Anda akan mendapat gambaran yang lebih baik tentang apa
masalahnya dengan kode itu.

Sebagai contoh, katakanlah kita memiliki fungsi yang menyapa orang
berdasarkan nama dan kita ingin menguji bahwa nama yang kita teruskan ke
fungsi itu muncul di outputnya:

<span class="filename">Nama File: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

Persyaratan untuk program ini belum disepakati, dan kita cukup yakin bahwa
teks `Hello` di awal sapaan akan berubah. Kita memutuskan untuk tidak perlu
memperbarui test ketika persyaratannya berubah, jadi alih-alih
memeriksa kesamaan persis dengan nilai yang dikembalikan fungsi `greeting`,
kita hanya menegaskan bahwa outputnya mengandung teks parameter
inputnya.

Sekarang mari kita masukkan bug ke dalam kode ini dengan mengubah
`greeting` agar tidak menyertakan `name` untuk melihat seperti apa kegagalan
test bawaan:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

Menjalankan test ini menghasilkan hal berikut:

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

Sekarang ketika kita menjalankan test, kita akan mendapatkan pesan
error yang lebih informatif:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

Kita bisa melihat nilai yang sebenarnya kita dapatkan di output
test, yang akan membantu kita men-debug apa yang terjadi alih-alih apa
yang kita harapkan terjadi.

### Memeriksa Panic dengan `should_panic`

Selain memeriksa return value, penting untuk memeriksa bahwa kode kita
menangani kondisi error seperti yang kita harapkan. Sebagai contoh,
perhatikan type `Guess` yang kita buat di Bab 9, Listing 9-13. Kode lain
yang memakai `Guess` bergantung pada jaminan bahwa instance `Guess` hanya
akan berisi nilai antara 1 dan 100. Kita bisa menulis test yang
memastikan bahwa percobaan membuat instance `Guess` dengan nilai di luar
rentang itu akan panic.

Kita melakukannya dengan menambahkan atribut `should_panic` ke fungsi
test kita. Test lulus jika kode di dalam fungsi itu panic;
test gagal jika kode di dalam fungsi itu tidak panic.

Listing 11-8 menunjukkan test yang memeriksa bahwa kondisi error
`Guess::new` terjadi ketika kita mengharapkannya.

<Listing number="11-8" file-name="src/lib.rs" caption="Menguji bahwa sebuah kondisi akan menyebabkan `panic!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

Kita menempatkan atribut `#[should_panic]` setelah atribut `#[test]` dan
sebelum fungsi test yang diatributinya. Mari kita lihat hasilnya
ketika test ini lulus:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Terlihat bagus! Sekarang mari kita masukkan bug ke dalam kode kita dengan
menghapus kondisi bahwa fungsi `new` akan panic jika nilainya lebih besar
dari 100:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Ketika kita menjalankan test di Listing 11-8, ia akan gagal:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

Kita tidak mendapatkan pesan yang sangat membantu dalam kasus ini, tetapi
ketika kita melihat fungsi testnya, kita melihat bahwa ia dianotasi
dengan `#[should_panic]`. Kegagalan yang kita dapatkan berarti kode di
fungsi test tidak menyebabkan panic.

Test yang memakai `should_panic` bisa tidak presisi. Test
`should_panic` akan lulus bahkan jika test itu panic karena alasan
yang berbeda dari yang kita harapkan. Untuk membuat test
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

Test ini akan lulus karena nilai yang kita letakkan di parameter
`expected` atribut `should_panic` adalah substring dari pesan yang dipakai
fungsi `Guess::new` untuk panic. Kita bisa saja menentukan seluruh pesan
panic yang kita harapkan, yang dalam kasus ini adalah `Guess value must be
less than or equal to 100, got 200`. Apa yang Anda pilih untuk ditentukan
bergantung pada seberapa unik atau dinamis pesan panic itu dan seberapa
presisi Anda ingin testnya. Dalam kasus ini, substring dari pesan
panic sudah cukup untuk memastikan bahwa kode di fungsi test
mengeksekusi kasus `else if value > 100`.

Untuk melihat apa yang terjadi ketika test `should_panic` dengan pesan
`expected` gagal, mari kita masukkan lagi bug ke dalam kode kita dengan
menukar badan blok `if value < 1` dan blok `else if value > 100`:

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Kali ini ketika kita menjalankan test `should_panic`, ia akan gagal:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

Pesan kegagalannya menandakan bahwa test ini memang panic seperti yang
kita harapkan, tetapi pesan panic-nya tidak menyertakan string yang
diharapkan `less than or equal to 100`. Pesan panic yang sebenarnya kita
dapatkan dalam kasus ini adalah `Guess value must be greater than or equal
to 1, got 200`. Sekarang kita bisa mulai mencari tahu di mana bug kita!

### Memakai `Result<T, E>` dalam Test

Semua test kita sejauh ini panic ketika gagal. Kita juga bisa menulis
test yang memakai `Result<T, E>`! Berikut test dari Listing 11-1,
ditulis ulang untuk memakai `Result<T, E>` dan mengembalikan `Err` alih-alih
panic:

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

Fungsi `it_works` sekarang memiliki return type `Result<(), String>`. Di
badan fungsi, alih-alih memanggil *macro* `assert_eq!`, kita mengembalikan
`Ok(())` ketika test lulus dan `Err` dengan `String` di dalamnya
ketika test gagal.

Menulis test sehingga ia mengembalikan `Result<T, E>` memungkinkan
Anda memakai operator tanda tanya di badan test, yang bisa menjadi
cara yang nyaman untuk menulis test yang seharusnya gagal jika operasi
mana pun di dalamnya mengembalikan varian `Err`.

Anda tidak bisa memakai anotasi `#[should_panic]` pada test yang
memakai `Result<T, E>`. Untuk menegaskan bahwa sebuah operasi mengembalikan
varian `Err`, _jangan_ memakai operator tanda tanya pada nilai `Result<T,
E>` itu. Sebagai gantinya, pakailah `assert!(value.is_err())`.

Sekarang setelah Anda tahu beberapa cara menulis test, mari kita lihat
apa yang terjadi ketika kita menjalankan test kita dan menjelajahi
opsi-opsi berbeda yang bisa kita pakai bersama `cargo test`.

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: ../unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
