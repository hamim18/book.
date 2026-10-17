## Bekerja dengan Variable Lingkungan

Kita akan memperbaiki binary `minigrep` dengan menambahkan fitur tambahan:
sebuah opsi untuk pencarian *case-insensitive* (tanpa membedakan huruf
besar-kecil) yang dapat diaktifkan pengguna melalui sebuah variable
lingkungan. Kita bisa menjadikan fitur ini sebuah opsi baris perintah dan
mengharuskan pengguna memasukkannya setiap kali mereka ingin fitur itu
berlaku, tetapi dengan menjadikannya environment variable, kita mengizinkan
pengguna menetapkan environment variable itu sekali dan membuat semua
pencarian mereka menjadi case-insensitive di sesi terminal itu.

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-a-failing-test-for-the-case-insensitive-search-function"></a>

### Menulis Pengujian yang Gagal untuk Pencarian Case-Insensitive

Pertama, kita menambahkan fungsi baru `search_case_insensitive` ke pustaka
`minigrep` yang akan dipanggil ketika environment variable itu memiliki nilai.
Kita akan terus mengikuti proses TDD, jadi langkah pertama kembali adalah
menulis sebuah pengujian yang gagal. Kita akan menambahkan pengujian baru
untuk fungsi `search_case_insensitive` yang baru itu dan mengganti nama
pengujian lama kita dari `one_result` menjadi `case_sensitive` untuk
memperjelas perbedaan antara kedua pengujian tersebut, seperti yang
ditunjukkan di Listing 12-20.

<Listing number="12-20" file-name="src/lib.rs" caption="Menambahkan pengujian gagal yang baru untuk fungsi case-insensitive yang akan segera kita tambahkan">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

Perhatikan bahwa kita juga telah mengedit `contents` pada pengujian lama.
Kita telah menambahkan sebuah baris baru dengan teks `"Duct tape."` memakai
huruf kapital _D_ yang seharusnya tidak cocok dengan kueri `"duct"` ketika
kita mencari secara case-sensitive. Mengubah pengujian lama dengan cara ini
membantu memastikan bahwa kita tidak secara tidak sengaja merusak
fungsionalitas pencarian case-sensitive yang telah kita implementasikan.
Pengujian ini seharusnya lulus sekarang dan seharusnya terus lulus saat kita
mengerjakan pencarian case-insensitive.

Pengujian baru untuk pencarian case-_insensitive_ memakai `"rUsT"` sebagai
kuerinya. Di fungsi `search_case_insensitive` yang akan segera kita tambahkan,
kueri `"rUsT"` seharusnya cocok dengan baris yang memuat `"Rust:"` dengan
huruf kapital _R_ dan cocok dengan baris `"Trust me."` meskipun keduanya
memiliki kapitalisasi yang berbeda dari kuerinya. Ini adalah pengujian kita
yang gagal, dan ia akan gagal terkompilasi karena kita belum mendefinisikan
fungsi `search_case_insensitive`. Silakan tambahkan implementasi kerangka yang
selalu mengembalikan vector kosong, mirip dengan yang kita lakukan untuk
fungsi `search` di Listing 12-16, untuk melihat pengujiannya terkompilasi lalu
gagal.

### Mengimplementasikan Fungsi `search_case_insensitive`

Fungsi `search_case_insensitive`, yang ditunjukkan di Listing 12-21, akan
hampir sama dengan fungsi `search`. Satu-satunya perbedaan adalah kita akan
mengubah `query` dan setiap `line` menjadi huruf kecil sehingga apa pun
kapitalisasi argumen inputnya, mereka akan memiliki kapitalisasi yang sama
ketika kita memeriksa apakah baris itu memuat kuerinya.

<Listing number="12-21" file-name="src/lib.rs" caption="Mendefinisikan fungsi `search_case_insensitive` untuk mengubah kueri dan baris menjadi huruf kecil sebelum membandingkannya">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

Pertama, kita mengubah string `query` menjadi huruf kecil dan menyimpannya di
sebuah variable baru dengan nama yang sama, melakukan *shadowing* terhadap
`query` yang asli. Memanggil `to_lowercase` pada kueri itu perlu agar apa pun
kueri pengguna—`"rust"`, `"RUST"`, `"Rust"`, ataupun `"rUsT"`—kita akan
memperlakukan kuerinya seolah-olah ia adalah `"rust"` dan menjadi tidak peka
terhadap huruf besar-kecil. Meskipun `to_lowercase` akan menangani Unicode
dasar, ia tidak akan akurat 100 persen. Jika kita menulis aplikasi sungguhan,
kita akan melakukan sedikit lebih banyak pekerjaan di sini, tetapi bagian ini
membahas environment variable, bukan Unicode, jadi kita biarkan saja seperti
ini.

Perhatikan bahwa `query` kini adalah sebuah `String`, bukan string *slice*,
karena memanggil `to_lowercase` menciptakan data baru, bukan mereferensikan
data yang sudah ada. Misalnya kuerinya adalah `"rUsT"`: String *slice* itu tidak
memuat huruf kecil `u` atau `t` yang dapat kita pakai, jadi kita harus
mengalokasikan sebuah `String` baru yang memuat `"rust"`. Ketika kita
meneruskan `query` sebagai argumen ke method `contains` sekarang, kita perlu
menambahkan ampersand karena tanda tangan `contains` didefinisikan untuk
menerima sebuah string *slice*.

Selanjutnya, kita menambahkan pemanggilan `to_lowercase` pada setiap `line`
untuk mengubah semua karakter menjadi huruf kecil. Sekarang setelah kita
mengonversi `line` dan `query` menjadi huruf kecil, kita akan menemukan
kecocokan apa pun huruf besar-kecil kuerinya.

Mari kita lihat apakah implementasi ini meloloskan pengujian-pengujiannya:

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

Hebat! Mereka lulus. Sekarang mari kita panggil fungsi
`search_case_insensitive` yang baru itu dari fungsi `run`. Pertama, kita akan
menambahkan sebuah opsi konfigurasi ke *struct* `Config` untuk berpindah antara
pencarian case-sensitive dan case-insensitive. Menambahkan *field* ini akan
menyebabkan error kompilasi karena kita belum menginisialisasi *field* ini di
mana pun:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```

Kita telah menambahkan *field* `ignore_case` yang menampung sebuah Boolean.
Selanjutnya, kita perlu membuat fungsi `run` memeriksa nilai *field*
`ignore_case` dan memakainya untuk memutuskan apakah akan memanggil fungsi
`search` atau fungsi `search_case_insensitive`, seperti yang ditunjukkan di
Listing 12-22. Ini masih belum akan terkompilasi.

<Listing number="12-22" file-name="src/main.rs" caption="Memanggil `search` atau `search_case_insensitive` berdasarkan nilai di `config.ignore_case`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```

</Listing>

Akhirnya, kita perlu memeriksa environment variablenya. Fungsi-fungsi untuk
bekerja dengan environment variable berada di modul `env` dalam pustaka
standar, yang sudah berada di dalam *scope* di bagian atas _src/main.rs_.
Kita akan memakai fungsi `var` dari modul `env` untuk memeriksa apakah ada
nilai yang ditetapkan untuk sebuah environment variable bernama `IGNORE_CASE`,
seperti yang ditunjukkan di Listing 12-23.

<Listing number="12-23" file-name="src/main.rs" caption="Memeriksa apakah ada nilai apa pun di environment variable bernama `IGNORE_CASE`">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```

</Listing>

Di sini, kita membuat sebuah variable baru, `ignore_case`. Untuk menetapkan
nilainya, kita memanggil fungsi `env::var` dan meneruskan nama variable
lingkungan `IGNORE_CASE` kepadanya. Fungsi `env::var` mengembalikan sebuah
`Result` yang akan berupa *variant* `Ok` yang berhasil dan memuat nilai
environment variable itu jika environment variablenya ditetapkan ke nilai apa
pun. Fungsi itu akan mengembalikan *variant* `Err` jika variable
lingkungannya tidak ditetapkan.

Kita memakai method `is_ok` pada `Result` untuk memeriksa apakah variable
lingkungan itu ditetapkan, yang berarti program seharusnya melakukan
pencarian case-insensitive. Jika environment variable `IGNORE_CASE` tidak
ditetapkan ke apa pun, `is_ok` akan mengembalikan `false` dan program akan
melakukan pencarian case-sensitive. Kita tidak peduli pada _nilai_ variable
lingkungan itu, hanya apakah ia ditetapkan atau tidak, jadi kita memeriksa
`is_ok` alih-alih memakai `unwrap`, `expect`, atau method-method lain yang
telah kita lihat pada `Result`.

Kita meneruskan nilai di variable `ignore_case` ke instance `Config` sehingga
fungsi `run` dapat membaca nilai itu dan memutuskan apakah akan memanggil
`search_case_insensitive` atau `search`, seperti yang kita implementasikan di
Listing 12-22.

Mari kita coba! Pertama, kita akan menjalankan program kita tanpa variable
lingkungan yang ditetapkan dan dengan kueri `to`, yang seharusnya cocok dengan
semua baris yang memuat kata _to_ dengan huruf kecil semua:

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

Tampaknya itu masih bekerja! Sekarang mari kita jalankan programnya dengan
`IGNORE_CASE` ditetapkan ke `1` tetapi dengan kueri yang sama `to`:

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

Jika Anda memakai PowerShell, Anda perlu menetapkan environment variable dan
menjalankan programnya sebagai perintah-perintah terpisah:

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

Ini akan membuat `IGNORE_CASE` bertahan selama sisa sesi shell Anda. Variable
itu dapat dibatalkan dengan cmdlet `Remove-Item`:

```console
PS> Remove-Item Env:IGNORE_CASE
```

Kita seharusnya mendapat baris-baris yang memuat _to_ yang mungkin memiliki
huruf kapital:

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

Luar biasa, kita juga mendapat baris-baris yang memuat _To_! Program
`minigrep` kita kini dapat melakukan pencarian case-insensitive yang
dikendalikan oleh sebuah environment variable. Sekarang Anda tahu cara
mengelola opsi yang ditetapkan menggunakan argumen baris perintah ataupun
environment variable.

Beberapa program mengizinkan argumen _dan_ environment variable untuk
konfigurasi yang sama. Dalam kasus-kasus itu, program menentukan bahwa salah
satu di antaranya yang didahulukan. Untuk latihan lain secara mandiri, cobalah
mengendalikan kepekaan huruf besar-kecil melalui argumen baris perintah
ataupun environment variable. Putuskan apakah argumen baris perintah atau
environment variable yang seharusnya didahulukan jika program dijalankan dengan
yang satu ditetapkan untuk membedakan huruf besar-kecil dan yang satu lagi
untuk mengabaikan huruf besar-kecil.

Modul `std::env` memuat lebih banyak fitur berguna untuk menangani variable
lingkungan: Lihat dokumentasinya untuk mengetahui apa saja yang tersedia.
