<!-- Old headings. Do not remove or links may break. -->
<a id="developing-the-librarys-functionality-with-test-driven-development"></a>

## Menambahkan Fungsionalitas dengan Test-Driven Development

Sekarang logika pencarian di _src/lib.rs_ terpisah dari fungsi `main`, menulis
pengujian untuk fungsionalitas inti kode kita menjadi jauh lebih mudah. Kita
dapat memanggil fungsi-fungsi secara langsung dengan berbagai argumen dan
memeriksa nilai kembaliannya tanpa harus memanggil binary kita dari baris
perintah.

Di bagian ini, kita akan menambahkan logika pencarian ke program `minigrep`
menggunakan proses *test-driven development* (TDD, pengembangan yang
digerakkan oleh pengujian) dengan langkah-langkah berikut:

1. Tulis sebuah pengujian yang gagal dan jalankan untuk memastikan ia gagal
   karena alasan yang Anda harapkan.
2. Tulis atau ubah kode secukupnya agar pengujian baru itu lulus.
3. Lakukan refactoring pada kode yang baru saja Anda tambahkan atau ubah, dan
   pastikan pengujian-pengujian itu terus lulus.
4. Ulangi dari langkah 1!

Meskipun hanya salah satu dari banyak cara menulis perangkat lunak, TDD dapat
membantu mengarahkan desain kode. Menulis pengujian sebelum menulis kode yang
membuat pengujian itu lulus membantu mempertahankan cakupan pengujian yang
tinggi di sepanjang proses.

Kita akan menulis pengujiannya terlebih dahulu untuk menggerakkan
implementasi fungsionalitas yang benar-benar melakukan pencarian string kueri
di dalam isi file dan menghasilkan daftar baris yang cocok dengan kueri
tersebut. Kita akan menambahkan fungsionalitas ini di dalam sebuah fungsi
bernama `search`.

### Menulis Pengujian yang Gagal

Di _src/lib.rs_, kita akan menambahkan modul `tests` dengan sebuah fungsi
pengujian, seperti yang kita lakukan di [Bab 11][ch11-anatomy]<!-- ignore -->.
Fungsi pengujian itu menentukan perilaku yang kita inginkan dari fungsi
`search`: Fungsi ini akan menerima sebuah kueri dan teks yang akan dicari,
lalu mengembalikan hanya baris-baris dari teks itu yang memuat kueri tersebut.
Listing 12-15 menunjukkan pengujian ini.

<Listing number="12-15" file-name="src/lib.rs" caption="Membuat pengujian yang gagal untuk fungsi `search` demi fungsionalitas yang kita inginkan">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-15/src/lib.rs:here}}
```

</Listing>

Pengujian ini mencari string `"duct"`. Teks yang kita cari terdiri dari tiga
baris, dan hanya satu baris yang memuat `"duct"` (perhatikan bahwa backslash
setelah tanda kutip ganda pembuka memberi tahu Rust untuk tidak menaruh
karakter newline di awal isi *string literal* ini). Kita menegaskan bahwa nilai
yang dikembalikan dari fungsi `search` hanya memuat baris yang kita harapkan.

Jika kita menjalankan pengujian ini, saat ini ia akan gagal karena makro
`unimplemented!` melakukan panic dengan pesan “not implemented”. Sesuai
prinsip TDD, kita akan mengambil langkah kecil dengan menambahkan kode
secukupnya agar pengujian itu tidak panic saat memanggil fungsinya, yaitu
dengan mendefinisikan fungsi `search` agar selalu mengembalikan vektor kosong,
seperti yang ditunjukkan di Listing 12-16. Setelah itu, pengujian ini
seharusnya terkompilasi dan gagal karena vektor kosong tidak cocok dengan
vektor yang memuat baris `"safe, fast, productive."`.

<Listing number="12-16" file-name="src/lib.rs" caption="Mendefinisikan fungsi `search` secukupnya sehingga pemanggilannya tidak akan panic">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-16/src/lib.rs:here}}
```

</Listing>

Sekarang mari kita bahas mengapa kita perlu mendefinisikan *lifetime*
eksplisit `'a` di tanda tangan `search` dan memakai *lifetime* itu bersama
argumen `contents` dan nilai kembaliannya. Ingat kembali di [Bab
10][ch10-lifetimes]<!-- ignore --> bahwa parameter *lifetime* menentukan
*lifetime* argumen mana yang terhubung dengan *lifetime* nilai kembalian.
Dalam kasus ini, kita menunjukkan bahwa vektor yang dikembalikan harus memuat
string *slice* yang mereferensikan *slice*-slice dari argumen `contents` (bukan
argumen `query`).

Dengan kata lain, kita memberi tahu Rust bahwa data yang dikembalikan oleh
fungsi `search` akan hidup selama data yang diteruskan ke fungsi `search`
melalui argumen `contents`. Ini penting! Data yang direferensikan _oleh_
sebuah *slice* harus tetap valid agar *reference*-nya valid; jika *compiler*
mengasumsikan kita membuat string *slice* dari `query` dan bukan `contents`, ia
akan melakukan pemeriksaan keamanannya secara keliru.

Jika kita lupa anotasi *lifetime*-nya dan mencoba mengompilasi fungsi ini,
kita akan mendapat galat ini:

```console
{{#include ../listings/ch12-an-io-project/output-only-02-missing-lifetimes/output.txt}}
```

Rust tidak dapat mengetahui mana dari kedua parameter itu yang kita perlukan
untuk keluarannya, jadi kita perlu memberi tahunya secara eksplisit.
Perhatikan bahwa teks bantuan itu menyarankan untuk menentukan parameter
*lifetime* yang sama untuk semua parameter dan tipe keluarannya, dan itu tidak
tepat! Karena `contents` adalah parameter yang memuat seluruh teks kita dan
kita ingin mengembalikan bagian-bagian teks itu yang cocok, kita tahu bahwa
`contents` adalah satu-satunya parameter yang seharusnya terhubung dengan
nilai kembalian menggunakan sintaks *lifetime*.

Bahasa-bahasa pemrograman lain tidak mengharuskan Anda menghubungkan argumen
dengan nilai kembalian di tanda tangan, tetapi praktik ini akan menjadi lebih
mudah seiring waktu. Anda mungkin ingin membandingkan contoh ini dengan
contoh-contoh di bagian [“Memvalidasi *Reference* dengan
Lifetime”][validating-references-with-lifetimes]<!-- ignore --> di Bab 10.

### Menulis Kode agar Pengujian Lulus

Saat ini, pengujian kita gagal karena kita selalu mengembalikan vektor
kosong. Untuk memperbaikinya dan mengimplementasikan `search`, program kita
perlu mengikuti langkah-langkah ini:

1. Melakukan iterasi pada setiap baris dari contents.
2. Memeriksa apakah baris itu memuat string kueri kita.
3. Jika ya, menambahkan baris itu ke daftar nilai yang kita kembalikan.
4. Jika tidak, tidak melakukan apa-apa.
5. Mengembalikan daftar hasil yang cocok.

Mari kita kerjakan setiap langkah, dimulai dari melakukan iterasi pada
baris-baris.

#### Melakukan Iterasi pada Baris-Baris dengan Metode `lines`

Rust memiliki sebuah metode yang membantu untuk menangani iterasi string baris
demi baris, yang dengan tepat dinamai `lines`, dan bekerja seperti yang
ditunjukkan di Listing 12-17. Perhatikan bahwa ini belum akan terkompilasi.

<Listing number="12-17" file-name="src/lib.rs" caption="Melakukan iterasi pada setiap baris di dalam `contents`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-17/src/lib.rs:here}}
```

</Listing>

Metode `lines` mengembalikan sebuah *iterator*. Kita akan membahas *iterator*
secara mendalam di [Bab 13][ch13-iterators]<!-- ignore -->. Tetapi ingat
bahwa Anda pernah melihat cara memakai *iterator* seperti ini di [Listing
3-5][ch3-iter]<!-- ignore -->, tempat kita memakai perulangan `for` dengan
sebuah *iterator* untuk menjalankan sebagian kode pada setiap item di dalam
sebuah koleksi.

#### Mencari Kueri di Setiap Baris

Selanjutnya, kita akan memeriksa apakah baris saat ini memuat string kueri
kita. Untungnya, string memiliki metode yang membantu bernama `contains` yang
melakukan ini untuk kita! Tambahkan pemanggilan metode `contains` di fungsi
`search`, seperti yang ditunjukkan di Listing 12-18. Perhatikan bahwa ini
masih belum akan terkompilasi.

<Listing number="12-18" file-name="src/lib.rs" caption="Menambahkan fungsionalitas untuk melihat apakah baris itu memuat string di dalam `query`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-18/src/lib.rs:here}}
```

</Listing>

Saat ini, kita sedang membangun fungsionalitasnya. Agar kode ini terkompilasi,
kita perlu mengembalikan sebuah nilai dari badan fungsi seperti yang kita
nyatakan di tanda tangan fungsi.

#### Menyimpan Baris yang Cocok

Untuk menyelesaikan fungsi ini, kita perlu sebuah cara untuk menyimpan
baris-baris yang cocok dan ingin kita kembalikan. Untuk itu, kita dapat
membuat sebuah vektor *mutable* sebelum perulangan `for` dan memanggil metode
`push` untuk menyimpan sebuah `line` di dalam vektor. Setelah perulangan
`for`, kita mengembalikan vektor tersebut, seperti yang ditunjukkan di Listing
12-19.

<Listing number="12-19" file-name="src/lib.rs" caption="Menyimpan baris-baris yang cocok agar kita dapat mengembalikannya">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:here}}
```

</Listing>

Sekarang fungsi `search` seharusnya mengembalikan hanya baris-baris yang
memuat `query`, dan pengujian kita seharusnya lulus. Mari kita jalankan
pengujiannya:

```console
{{#include ../listings/ch12-an-io-project/listing-12-19/output.txt}}
```

Pengujian kita lulus, jadi kita tahu ia bekerja!

Pada titik ini, kita dapat mempertimbangkan peluang untuk melakukan
refactoring pada implementasi fungsi pencarian sambil tetap menjaga
pengujian-pengujiannya lulus untuk mempertahankan fungsionalitas yang sama.
Kode di fungsi pencarian tidak terlalu buruk, tetapi ia belum memanfaatkan
beberapa fitur *iterator* yang berguna. Kita akan kembali ke contoh ini di
[Bab 13][ch13-iterators]<!-- ignore -->, tempat kita akan menjelajahi
*iterator* secara mendetail dan melihat cara memperbaikinya.

Sekarang seluruh program seharusnya bekerja! Mari kita coba, pertama dengan
sebuah kata yang seharusnya mengembalikan tepat satu baris dari puisi Emily
Dickinson: _frog_.

```console
{{#include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/output.txt}}
```

Keren! Sekarang mari kita coba sebuah kata yang akan cocok dengan beberapa
baris, seperti _body_:

```console
{{#include ../listings/ch12-an-io-project/output-only-03-multiple-matches/output.txt}}
```

Dan terakhir, mari kita pastikan bahwa kita tidak mendapat baris apa pun
ketika mencari sebuah kata yang tidak ada di mana pun di dalam puisi itu,
seperti _monomorphization_:

```console
{{#include ../listings/ch12-an-io-project/output-only-04-no-matches/output.txt}}
```

Luar biasa! Kita telah membangun versi mini kita sendiri dari sebuah alat
klasik dan belajar banyak tentang cara menyusun aplikasi. Kita juga telah
belajar sedikit tentang masukan dan keluaran file, *lifetime*, pengujian, dan
parsing baris perintah.

Untuk melengkapi proyek ini, kita akan mendemonstrasikan secara singkat cara
bekerja dengan variabel lingkungan dan cara mencetak ke standard error, yang
keduanya berguna ketika Anda menulis program baris perintah.

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html
