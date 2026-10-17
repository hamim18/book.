## Alur Kontrol yang Ringkas dengan `if let` dan `let...else`

Sintaks `if let` memungkinkan Anda menggabungkan `if` dan `let` menjadi cara
yang lebih ringkas untuk menangani nilai yang cocok dengan satu pattern sambil
mengabaikan sisanya. Perhatikan program pada Listing 6-6 yang melakukan match
pada nilai `Option<u8>` di variable `config_max` tetapi hanya ingin
mengeksekusi kode jika nilainya adalah *variant* (varian) `Some`.

<Listing number="6-6" caption="`match` yang hanya peduli mengeksekusi kode ketika nilainya `Some`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Listing>

Jika nilainya `Some`, kita mencetak nilai di dalam *variant* `Some` dengan
mengikat nilai itu ke variable `max` di dalam pattern. Kita tidak ingin melakukan
apa pun dengan nilai `None`. Untuk memenuhi expression `match`, kita harus
menambahkan `_ => ()` setelah memproses satu *variant* saja, yang merupakan
kode boilerplate yang menjengkelkan untuk ditulis.

Sebagai gantinya, kita dapat menuliskannya dengan cara yang lebih pendek
memakai `if let`. Kode berikut berperilaku sama seperti `match` pada Listing
6-6:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

Sintaks `if let` menerima sebuah pattern dan sebuah expression yang dipisahkan
tanda sama dengan. Ia bekerja sama seperti `match`, ketika expressionnya
diberikan ke `match` dan patternnya adalah *arm* (lengan) pertamanya. Pada kasus
ini, patternnya adalah `Some(max)`, dan `max` mengikat nilai di dalam `Some`.
Kita kemudian dapat memakai `max` di badan blok `if let` dengan cara yang sama
seperti kita memakai `max` pada *arm* `match` yang bersesuaian. Kode di blok
`if let` hanya berjalan jika nilainya cocok dengan patternnya.

Memakai `if let` berarti lebih sedikit mengetik, lebih sedikit indentasi, dan
lebih sedikit kode boilerplate. Namun, Anda kehilangan pemeriksaan *exhaustive* (ekshaustif)
yang ditegakkan `match`, yang memastikan Anda tidak lupa menangani kasus apa
pun. Memilih antara `match` dan `if let` bergantung pada apa yang Anda lakukan
dalam situasi Anda dan apakah memperoleh keringkasan adalah pengorbanan yang
sepadan untuk kehilangan pemeriksaan *exhaustive*.

Dengan kata lain, Anda dapat menganggap `if let` sebagai gula sintaks untuk
`match` yang menjalankan kode ketika nilainya cocok dengan satu pattern, lalu
mengabaikan semua nilai lain.

Kita dapat menyertakan `else` bersama `if let`. Blok kode yang menyertai
`else` sama dengan blok kode yang akan menyertai kasus `_` pada expression
`match` yang setara dengan `if let` dan `else` tersebut. Ingat definisi *enum*
`Coin` pada Listing 6-4, di mana *variant* `Quarter` juga menampung nilai
`UsState`. Jika kita ingin menghitung semua koin selain quarter yang kita
lihat sambil mengumumkan negara bagian pada koin-koin quarter, kita dapat
melakukannya dengan expression `match`, seperti ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

Atau kita dapat memakai expression `if let` dan `else`, seperti ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```

## Tetap di “Happy Path” dengan `let...else`

Pattern yang umum adalah melakukan suatu perhitungan ketika ada nilai dan
mengembalikan nilai bawaan jika tidak. Melanjutkan contoh koin dengan nilai
`UsState`, jika kita ingin mengatakan sesuatu yang lucu bergantung pada
seberapa tua negara bagian pada quarter itu, kita dapat menambahkan sebuah
method pada `UsState` untuk memeriksa usia sebuah negara bagian, seperti ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

Lalu, kita dapat memakai `if let` untuk melakukan match pada jenis koinnya,
dengan memperkenalkan variable `state` di dalam badan kondisinya, seperti
pada Listing 6-7.

<Listing number="6-7" caption="Memeriksa apakah sebuah negara bagian sudah ada pada tahun 1900 dengan memakai kondisional bersarang di dalam `if let`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Listing>

Itu menyelesaikan pekerjaannya, tetapi ia mendorong pekerjaannya ke badan
statement `if let`, dan jika pekerjaan yang dilakukan lebih rumit, mungkin
sulit untuk mengikuti dengan tepat bagaimana cabang-cabang tingkat atas
saling berhubungan. Kita juga dapat memanfaatkan fakta bahwa expression
menghasilkan nilai, entah untuk menghasilkan `state` dari `if let` atau untuk
keluar lebih awal, seperti pada Listing 6-8. (Anda juga dapat melakukan hal
serupa dengan `match`.)

<Listing number="6-8" caption="Memakai `if let` untuk menghasilkan nilai atau keluar lebih awal">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Listing>

Namun, cara ini juga agak menjengkelkan untuk diikuti! Satu cabang `if let`
menghasilkan nilai, dan yang lainnya keluar dari fungsi sepenuhnya.

Untuk membuat pattern umum ini lebih enak dinyatakan, Rust memiliki `let...else`.
Sintaks `let...else` menerima pattern di sisi kiri dan expression di sisi kanan,
sangat mirip dengan `if let`, tetapi ia tidak memiliki cabang `if`, hanya
cabang `else`. Jika patternnya cocok, ia akan mengikat nilai dari pattern di *scope* (cakupan)
luar. Jika patternnya _tidak_ cocok, program akan mengalir ke *arm* `else`, yang
harus keluar dari fungsi.

Pada Listing 6-9, Anda dapat melihat bagaimana tampilan Listing 6-8 ketika
memakai `let...else` menggantikan `if let`.

<Listing number="6-9" caption="Memakai `let...else` untuk memperjelas alur di dalam fungsi">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Listing>

Perhatikan bahwa dengan cara ini ia tetap berada di “happy path” pada badan
utama fungsi, tanpa memiliki control flow yang berbeda secara signifikan
untuk dua cabang seperti yang dilakukan `if let`.

Jika Anda berada dalam situasi ketika program Anda memiliki logika yang
terlalu bertele-tele untuk dinyatakan dengan `match`, ingatlah bahwa `if let`
dan `let...else` juga ada di kotak peralatan Rust Anda.

## Ringkasan

Kini kita telah membahas cara memakai *enum* untuk membuat custom type yang
dapat menjadi salah satu dari sekumpulan nilai yang dienumerasikan. Kita telah
menunjukkan bagaimana type `Option<T>` milik pustaka standar membantu Anda
memakai type system untuk mencegah error. Ketika nilai *enum* memiliki data di
dalamnya, Anda dapat memakai `match` atau `if let` untuk mengekstrak dan
memakai nilai-nilai itu, bergantung pada seberapa banyak kasus yang perlu Anda
tangani.

Program Rust Anda kini dapat menyatakan konsep-konsep di domain Anda dengan
memakai *struct* dan *enum*. Membuat custom type untuk dipakai di API Anda
menjamin keamanan type: *compiler* (kompilator) akan memastikan fungsi-fungsi
Anda hanya mendapatkan nilai dengan type yang diharapkan setiap fungsi.

Untuk menyediakan API yang tertata baik kepada pengguna Anda, yang mudah
dipakai dan hanya mengekspos persis apa yang dibutuhkan pengguna Anda, mari
kita beralih ke *module* (modul) milik Rust.
