## Menerbitkan Crate ke Crates.io

Kita telah memakai *package* (paket) dari
[crates.io](https://crates.io/)<!-- ignore --> sebagai dependency proyek kita,
tetapi Anda juga dapat membagikan kode Anda kepada orang lain dengan
menerbitkan *package* Anda sendiri. *Crate registry* (registri *crate*) di
[crates.io](https://crates.io/)<!-- ignore --> mendistribusikan kode sumber
*package* Anda, jadi situs itu utamanya menampung kode yang bersifat open source.

Rust dan Cargo memiliki fitur-fitur yang membuat *package* terbitan Anda lebih
mudah ditemukan dan dipakai orang. Selanjutnya, kita akan membahas beberapa
fitur tersebut, lalu menjelaskan cara menerbitkan sebuah *package*.

### Membuat Komentar Dokumentasi yang Berguna

Mendokumentasikan *package* Anda secara akurat akan membantu pengguna lain
mengetahui cara dan waktu memakainya, jadi ada baiknya Anda meluangkan waktu
untuk menulis dokumentasi. Di Bab 3, kita membahas cara memberi komentar pada
kode Rust dengan dua garis miring, `//`. Rust juga memiliki jenis komentar
khusus untuk dokumentasi, yang dengan tepat disebut _documentation comment_
(komentar dokumentasi), yang akan menghasilkan dokumentasi HTML. HTML itu
menampilkan isi komentar dokumentasi untuk item API publik yang ditujukan bagi
programmer yang tertarik mengetahui cara _memakai_ *crate* Anda, bukan cara *crate*
Anda _diimplementasikan_.

Komentar dokumentasi memakai tiga garis miring, `///`, alih-alih dua, dan
mendukung notasi Markdown untuk memformat teks. Tempatkan komentar dokumentasi
tepat sebelum item yang didokumentasikannya. Listing 14-1 menampilkan komentar
dokumentasi untuk fungsi `add_one` di dalam *crate* bernama `my_crate`.

<Listing number="14-1" file-name="src/lib.rs" caption="Komentar dokumentasi untuk sebuah fungsi">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-01/src/lib.rs}}
```

</Listing>

Di sini, kita memberikan deskripsi tentang apa yang dilakukan fungsi
`add_one`, memulai sebuah seksi dengan heading `Examples`, lalu menyediakan
kode yang menunjukkan cara memakai fungsi `add_one`. Kita dapat menghasilkan
dokumentasi HTML dari komentar dokumentasi ini dengan menjalankan `cargo doc`.
Perintah ini menjalankan tool `rustdoc` yang didistribusikan bersama Rust dan
meletakkan dokumentasi HTML yang dihasilkan di direktori _target/doc_.

Demi kemudahan, menjalankan `cargo doc --open` akan membangun HTML untuk
dokumentasi *crate* Anda saat ini (serta dokumentasi untuk semua dependency
*crate* Anda) dan membuka hasilnya di web browser. Buka fungsi `add_one` dan
Anda akan melihat bagaimana teks di komentar dokumentasi itu dirender, seperti
ditunjukkan pada Gambar 14-1.

<img alt="Dokumentasi HTML yang dirender untuk fungsi `add_one` dari `my_crate`" src="img/trpl14-01.png" class="center" />

<span class="caption">Gambar 14-1: Dokumentasi HTML untuk fungsi
`add_one`</span>

#### Seksi yang Lazim Dipakai

Kita memakai heading Markdown `# Examples` di Listing 14-1 untuk membuat
sebuah seksi di HTML dengan judul “Examples.” Berikut beberapa seksi lain yang
lazim dipakai penulis *crate* di dokumentasi mereka:

- **Panics**: Ini adalah skenario ketika fungsi yang didokumentasikan bisa
  panic. Pemanggil fungsi yang tidak ingin programnya panic harus memastikan
  mereka tidak memanggil fungsi itu dalam situasi-situasi tersebut.
- **Errors**: Jika fungsi mengembalikan `Result`, menjelaskan jenis error yang
  mungkin terjadi dan kondisi apa yang mungkin menyebabkan error tersebut
  dikembalikan dapat membantu pemanggil sehingga mereka bisa menulis kode
  untuk menangani berbagai jenis error dengan cara yang berbeda-beda.
- **Safety**: Jika fungsi itu tidak aman (`unsafe`) untuk dipanggil (kita
  membahas ketidakamanan di Bab 20), seharusnya ada seksi yang menjelaskan
  mengapa fungsi itu `unsafe` dan mencakup invarian yang diharapkan fungsi
  untuk dipertahankan oleh pemanggilnya.

Sebagian besar komentar dokumentasi tidak membutuhkan semua seksi ini, tetapi
ini adalah daftar periksa yang baik untuk mengingatkan Anda tentang
aspek-aspek kode yang ingin diketahui pengguna Anda.

<a id="documentation-comments-as-tests"></a>
#### Komentar Dokumentasi sebagai Test

Menambahkan blok kode contoh di komentar dokumentasi Anda dapat membantu
menunjukkan cara memakai library Anda dan memberi bonus tambahan: menjalankan
`cargo test` akan menjalankan contoh kode di dokumentasi Anda sebagai test!
Tidak ada yang lebih baik daripada dokumentasi dengan contoh. Tetapi tidak ada
yang lebih buruk daripada contoh yang tidak berfungsi karena kode telah
berubah sejak dokumentasi ditulis. Jika kita menjalankan `cargo test` dengan
dokumentasi untuk fungsi `add_one` dari Listing 14-1, kita akan melihat sebuah
seksi di hasil test yang tampak seperti ini:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-01/
cargo test
copy just the doc-tests section below
-->

```text
   Doc-tests my_crate

running 1 test
test src/lib.rs - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
```

Sekarang, jika kita mengubah fungsinya atau contohnya sehingga `assert_eq!` di
contoh itu panic, lalu menjalankan `cargo test` lagi, kita akan melihat bahwa
doc test menangkap ketidaksinkronan antara contoh dan kode!

<!-- Old headings. Do not remove or links may break. -->

<a id="commenting-contained-items"></a>

#### Komentar pada Item yang Memuatnya

Gaya komentar dok `//!` menambahkan dokumentasi ke item yang _memuat_ komentar
itu, bukan ke item yang _mengikuti_ komentar itu. Kita biasanya memakai
komentar dok ini di dalam file akar *crate* (_src/lib.rs_ menurut konvensi) atau
di dalam sebuah modul untuk mendokumentasikan *crate* atau modul itu secara
keseluruhan.

Sebagai contoh, untuk menambahkan dokumentasi yang menjelaskan tujuan *crate*
`my_crate` yang memuat fungsi `add_one`, kita menambahkan komentar dokumentasi
yang diawali `//!` ke awal file _src/lib.rs_, seperti ditunjukkan pada Listing
14-2.

<Listing number="14-2" file-name="src/lib.rs" caption="Dokumentasi untuk crate `my_crate` secara keseluruhan">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-02/src/lib.rs:here}}
```

</Listing>

Perhatikan bahwa tidak ada kode apa pun setelah baris terakhir yang diawali
`//!`. Karena kita memulai komentarnya dengan `//!` alih-alih `///`, kita
mendokumentasikan item yang memuat komentar ini, bukan item yang mengikuti
komentar ini. Dalam kasus ini, item itu adalah file _src/lib.rs_, yang
merupakan *crate root* (akar *crate*). Komentar-komentar ini menjelaskan
keseluruhan *crate*.

Ketika kita menjalankan `cargo doc --open`, komentar ini akan tampil di
halaman depan dokumentasi untuk `my_crate`, di atas daftar item publik di
*crate* tersebut, seperti ditunjukkan pada Gambar 14-2.

Komentar dokumentasi di dalam item berguna terutama untuk menjelaskan *crate*
dan modul. Pakailah komentar itu untuk menjelaskan tujuan keseluruhan wadah
tersebut guna membantu pengguna memahami organisasi *crate* Anda.

<img alt="Dokumentasi HTML yang dirender dengan komentar untuk crate secara keseluruhan" src="img/trpl14-02.png" class="center" />

<span class="caption">Gambar 14-2: Dokumentasi yang dirender untuk `my_crate`,
termasuk komentar yang menjelaskan *crate* secara keseluruhan</span>

<!-- Old headings. Do not remove or links may break. -->

<a id="exporting-a-convenient-public-api-with-pub-use"></a>

<a id="exporting-a-convenient-public-api"></a>
### Mengekspor API Publik yang Mudah Dipakai

Struktur API publik Anda merupakan pertimbangan utama ketika menerbitkan sebuah
*crate*. Orang yang memakai *crate* Anda kurang mengenal strukturnya dibandingkan Anda dan
mungkin kesulitan menemukan bagian yang ingin mereka pakai jika *crate* Anda
memiliki hierarki modul yang besar.

Di Bab 7, kita membahas cara membuat item menjadi publik dengan kata kunci
`pub`, dan cara membawa item ke dalam sebuah *scope* dengan kata kunci `use`.
Namun, struktur yang masuk akal bagi Anda ketika mengembangkan *crate* mungkin
tidak begitu nyaman bagi pengguna Anda. Anda mungkin ingin mengorganisasi
*struct* Anda dalam hierarki yang memuat beberapa tingkat, tetapi orang yang
ingin memakai type yang Anda definisikan di kedalaman hierarki mungkin
kesulitan mengetahui bahwa type itu ada. Mereka mungkin juga jengkel karena
harus menulis `use my_crate::some_module::another_module::UsefulType;`
alih-alih `use my_crate::UsefulType;`.

Kabar baiknya adalah jika struktur itu _tidak_ nyaman dipakai orang lain dari
library lain, Anda tidak perlu menyusun ulang organisasi internal Anda.
Sebagai gantinya, Anda dapat mengekspor ulang item untuk membuat struktur
publik yang berbeda dari struktur privat Anda dengan memakai `pub use`.
*Re-exporting* (mengekspor ulang) mengambil sebuah item publik di satu lokasi
dan menjadikannya publik di lokasi lain, seolah-olah item itu justru
didefinisikan di lokasi yang lain itu.

Sebagai contoh, anggaplah kita membuat sebuah library bernama `art` untuk
memodelkan konsep artistik. Di dalam library ini ada dua modul: modul `kinds`
yang memuat dua *enum* bernama `PrimaryColor` dan `SecondaryColor`, serta modul
`utils` yang memuat sebuah fungsi bernama `mix`, seperti ditunjukkan pada
Listing 14-3.

<Listing number="14-3" file-name="src/lib.rs" caption="Library `art` dengan item yang diorganisasi ke dalam modul `kinds` dan `utils`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-03/src/lib.rs:here}}
```

</Listing>

Gambar 14-3 menunjukkan seperti apa tampilan halaman depan dokumentasi untuk
*crate* ini yang dihasilkan oleh `cargo doc`.

<img alt="Dokumentasi yang dirender untuk crate `art` yang mendaftarkan modul `kinds` dan `utils`" src="img/trpl14-03.png" class="center" />

<span class="caption">Gambar 14-3: Halaman depan dokumentasi untuk `art`
yang mendaftarkan modul `kinds` dan `utils`</span>

Perhatikan bahwa type `PrimaryColor` dan `SecondaryColor` tidak terdaftar di
halaman depan, begitu pula fungsi `mix`. Kita harus mengeklik `kinds` dan
`utils` untuk melihatnya.

*Crate* lain yang bergantung pada library ini akan membutuhkan statement `use`
yang membawa item dari `art` ke dalam *scope*, dengan menyebutkan struktur modul
yang saat ini didefinisikan. Listing 14-4 menunjukkan contoh sebuah *crate* yang
memakai item `PrimaryColor` dan `mix` dari *crate* `art`.

<Listing number="14-4" file-name="src/main.rs" caption="Sebuah crate yang memakai item crate `art` dengan struktur internalnya yang diekspor">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-04/src/main.rs}}
```

</Listing>

Penulis kode di Listing 14-4, yang memakai *crate* `art`, harus mencari tahu
sendiri bahwa `PrimaryColor` ada di modul `kinds` dan `mix` ada di modul
`utils`. Struktur modul *crate* `art` lebih relevan bagi pengembang yang
mengerjakan *crate* `art` daripada bagi mereka yang memakainya. Struktur
internal itu tidak memuat informasi berguna apa pun bagi orang yang mencoba
memahami cara memakai *crate* `art`, melainkan menimbulkan kebingungan karena
pengembang yang memakainya harus mencari tahu ke mana harus melihat, dan harus
menyebutkan nama modul di statement `use`.

Untuk menghilangkan organisasi internal dari API publik, kita dapat mengubah
kode *crate* `art` di Listing 14-3 untuk menambahkan statement `pub use` guna
mengekspor ulang item-item itu di tingkat teratas, seperti ditunjukkan pada
Listing 14-5.

<Listing number="14-5" file-name="src/lib.rs" caption="Menambahkan statement `pub use` untuk mengekspor ulang item">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-05/src/lib.rs:here}}
```

</Listing>

Dokumentasi API yang dihasilkan `cargo doc` untuk *crate* ini sekarang akan
mendaftarkan dan menautkan hasil ekspor ulang di halaman depan, seperti
ditunjukkan pada Gambar 14-4, sehingga type `PrimaryColor` dan
`SecondaryColor` serta fungsi `mix` lebih mudah ditemukan.

<img alt="Dokumentasi yang dirender untuk crate `art` dengan hasil ekspor ulang di halaman depan" src="img/trpl14-04.png" class="center" />

<span class="caption">Gambar 14-4: Halaman depan dokumentasi untuk `art`
yang mendaftarkan hasil ekspor ulang</span>

Pengguna *crate* `art` tetap dapat melihat dan memakai struktur internal dari
Listing 14-3 seperti yang ditunjukkan pada Listing 14-4, atau mereka dapat
memakai struktur yang lebih nyaman di Listing 14-5, seperti ditunjukkan pada
Listing 14-6.

<Listing number="14-6" file-name="src/main.rs" caption="Program yang memakai item hasil ekspor ulang dari crate `art`">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-06/src/main.rs:here}}
```

</Listing>

Dalam kasus di mana ada banyak modul bersarang, mengekspor ulang type-type di
tingkat teratas dengan `pub use` dapat membuat perbedaan yang berarti dalam
pengalaman orang yang memakai *crate* itu. Kegunaan umum lain dari `pub use`
adalah mengekspor ulang definisi sebuah dependency di *crate* saat ini untuk
menjadikan definisi *crate* tersebut bagian dari API publik *crate* Anda.

Membuat struktur API publik yang berguna lebih merupakan seni daripada ilmu,
dan Anda dapat beriterasi untuk menemukan API yang paling cocok bagi pengguna
Anda. Memilih `pub use` memberi Anda fleksibilitas dalam menyusun *crate* Anda
secara internal dan melepaskan struktur internal itu dari apa yang Anda
tampilkan kepada pengguna Anda. Lihatlah sebagian kode *crate* yang telah Anda
pasang untuk melihat apakah struktur internalnya berbeda dari API publiknya.

### Menyiapkan Akun Crates.io

Sebelum dapat menerbitkan *crate* apa pun, Anda perlu membuat akun di
[crates.io](https://crates.io/)<!-- ignore --> dan mendapatkan token API.
Untuk melakukannya, kunjungi halaman utama di
[crates.io](https://crates.io/)<!-- ignore --> dan masuk lewat akun GitHub.
(Akun GitHub saat ini menjadi syarat, tetapi situs itu mungkin mendukung cara
lain untuk membuat akun di masa depan.) Setelah masuk, kunjungi pengaturan
akun Anda di [https://crates.io/me/](https://crates.io/me/)<!-- ignore --> dan
ambil kunci API Anda. Lalu, jalankan perintah `cargo login` dan tempelkan
kunci API Anda saat diminta, seperti ini:

```console
$ cargo login
abcdefghijklmnopqrstuvwxyz012345
```

Perintah ini akan memberi tahu Cargo token API Anda dan menyimpannya secara
lokal di _~/.cargo/credentials.toml_. Perhatikan bahwa token ini adalah
sebuah rahasia: Jangan membagikannya kepada siapa pun. Jika karena alasan
apa pun Anda membagikannya kepada seseorang, Anda harus mencabutnya dan
membuat token baru di [crates.io](https://crates.io/)<!-- ignore -->.

### Menambahkan Metadata ke Crate Baru

Anggaplah Anda memiliki sebuah *crate* yang ingin diterbitkan. Sebelum
menerbitkan, Anda perlu menambahkan beberapa metadata di seksi `[package]`
pada file _Cargo.toml_ *crate* itu.

*Crate* Anda akan membutuhkan nama yang unik. Selagi mengerjakan *crate* secara
lokal, Anda dapat menamai *crate* sesuka Anda. Namun, nama *crate* di
[crates.io](https://crates.io/)<!-- ignore --> dialokasikan berdasarkan asas
siapa cepat dia dapat. Sekali sebuah nama *crate* telah diambil, tidak ada orang
lain yang dapat menerbitkan *crate* dengan nama itu. Sebelum mencoba
menerbitkan *crate*, carilah nama yang ingin Anda pakai. Jika nama itu sudah
dipakai, Anda perlu mencari nama lain dan mengubah *field* `name` di file
_Cargo.toml_ pada seksi `[package]` untuk memakai nama baru itu saat
menerbitkan, seperti berikut:

<span class="filename">Nama File: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
```

Bahkan jika Anda telah memilih nama yang unik, saat Anda menjalankan `cargo
publish` untuk menerbitkan *crate* pada titik ini, Anda akan mendapat peringatan
lalu sebuah error:

<!-- manual-regeneration
Create a new package with an unregistered name, making no further modifications
  to the generated package, so it is missing the description and license fields.
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
warning: manifest has no description, license, license-file, documentation, homepage or repository.
See https://doc.rust-lang.org/cargo/reference/manifest.html#package-metadata for more info.
--snip--
error: failed to publish to registry at https://crates.io

Caused by:
  the remote server responded with an error (status 400 Bad Request): missing or empty metadata fields: description, license. Please see https://doc.rust-lang.org/cargo/reference/manifest.html for more information on configuring these fields
```

Ini menghasilkan error karena Anda kehilangan beberapa informasi yang penting:
Deskripsi dan lisensi diperlukan supaya orang tahu apa yang dilakukan *crate*
Anda dan dengan ketentuan apa mereka boleh memakainya. Di _Cargo.toml_,
tambahkan deskripsi satu-dua kalimat saja, karena deskripsi itu akan tampil
bersama *crate* Anda di hasil pencarian. Untuk *field* `license`, Anda perlu
memberikan nilai _license identifier_ (pengidentifikasi lisensi). [Software
*Package* Data Exchange (SPDX) milik Linux Foundation][spdx] mendaftarkan
pengidentifikasi yang dapat Anda pakai untuk nilai ini. Sebagai contoh, untuk
menyatakan bahwa Anda melisensikan *crate* Anda dengan Lisensi MIT, tambahkan
pengidentifikasi `MIT`:

<span class="filename">Nama File: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
license = "MIT"
```

Jika Anda ingin memakai lisensi yang tidak tercantum di SPDX, Anda perlu
meletakkan teks lisensi itu di sebuah file, menyertakan file itu di proyek
Anda, lalu memakai `license-file` untuk menyebutkan nama file itu alih-alih
memakai kunci `license`.

Panduan tentang lisensi mana yang sesuai untuk proyek Anda berada di luar
coverage buku ini. Banyak orang di komunitas Rust melisensikan proyek mereka
dengan cara yang sama seperti Rust, yaitu memakai lisensi ganda
`MIT OR Apache-2.0`. Praktik ini menunjukkan bahwa Anda juga dapat
menyebutkan beberapa pengidentifikasi lisensi yang dipisahkan dengan `OR`
untuk memiliki beberapa lisensi pada proyek Anda.

Dengan nama yang unik, versi, deskripsi, dan lisensi yang telah ditambahkan,
file _Cargo.toml_ untuk proyek yang siap diterbitkan mungkin tampak seperti
ini:

<span class="filename">Nama File: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"

[dependencies]
```

[Dokumentasi Cargo](https://doc.rust-lang.org/cargo/) menjelaskan metadata
lain yang dapat Anda sebutkan untuk memastikan orang lain dapat menemukan dan
memakai *crate* Anda dengan lebih mudah.

### Menerbitkan ke Crates.io

Sekarang Anda telah membuat akun, menyimpan token API, memilih nama untuk
*crate* Anda, dan menyebutkan metadata yang diperlukan, Anda siap menerbitkan!
Menerbitkan sebuah *crate* mengunggah versi tertentu ke
[crates.io](https://crates.io/)<!-- ignore --> untuk dipakai orang lain.

Berhati-hatilah, karena sebuah penerbitan bersifat _permanen_. Versinya tidak
pernah bisa ditimpa, dan kodenya tidak dapat dihapus kecuali dalam keadaan
tertentu. Salah satu tujuan utama *Crates*.io adalah menjadi arsip kode permanen
supaya build semua proyek yang bergantung pada *crate* dari
[crates.io](https://crates.io/)<!-- ignore --> akan terus berfungsi.
Mengizinkan penghapusan versi akan membuat tujuan itu mustahil tercapai.
Namun, tidak ada batasan jumlah versi *crate* yang dapat Anda terbitkan.

Jalankan lagi perintah `cargo publish`. Sekarang seharusnya berhasil:

<!-- manual-regeneration
go to some valid crate, publish a new version
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
   Packaging guessing_game v0.1.0 (file:///projects/guessing_game)
    Packaged 6 files, 1.2KiB (895.0B compressed)
   Verifying guessing_game v0.1.0 (file:///projects/guessing_game)
   Compiling guessing_game v0.1.0
(file:///projects/guessing_game/target/package/guessing_game-0.1.0)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0 (file:///projects/guessing_game)
    Uploaded guessing_game v0.1.0 to registry `crates-io`
note: waiting for `guessing_game v0.1.0` to be available at registry
`crates-io`.
You may press ctrl-c to skip waiting; the crate should be available shortly.
   Published guessing_game v0.1.0 at registry `crates-io`
```

Selamat! Anda kini telah membagikan kode Anda dengan komunitas Rust, dan
siapa pun dapat dengan mudah menambahkan *crate* Anda sebagai dependency
proyek mereka.

### Menerbitkan Versi Baru dari Crate yang Sudah Ada

Ketika Anda telah membuat perubahan pada *crate* Anda dan siap merilis versi
baru, Anda mengubah nilai `version` yang disebutkan di file _Cargo.toml_ Anda
dan menerbitkan ulang. Pakailah [aturan Semantic Versioning][semver] untuk
memutuskan nomor versi berikutnya yang sesuai, berdasarkan jenis perubahan
yang telah Anda buat. Lalu, jalankan `cargo publish` untuk mengunggah versi
baru.

<!-- Old headings. Do not remove or links may break. -->

<a id="removing-versions-from-cratesio-with-cargo-yank"></a>
<a id="deprecating-versions-from-cratesio-with-cargo-yank"></a>

### Menandai Versi sebagai Usang di Crates.io

Meskipun Anda tidak dapat menghapus versi lama sebuah *crate*, Anda dapat
mencegah semua proyek mendatang untuk menambahkannya sebagai dependency baru.
Ini berguna ketika sebuah versi *crate* rusak karena satu dan lain hal. Dalam
situasi seperti itu, Cargo mendukung *yanking* (penarikan) sebuah versi *crate*.

_Yanking_ sebuah versi mencegah proyek baru bergantung pada versi itu, tetapi
tetap mengizinkan semua proyek yang sudah bergantung padanya untuk terus
berjalan. Pada dasarnya, sebuah yank berarti semua proyek dengan _Cargo.lock_
tidak akan rusak, dan semua file _Cargo.lock_ yang dihasilkan di masa depan
tidak akan memakai versi yang di-yank.

Untuk menarik sebuah versi *crate*, di direktori *crate* yang sebelumnya telah
Anda terbitkan, jalankan `cargo yank` dan sebutkan versi mana yang ingin Anda
tarik. Sebagai contoh, jika kita telah menerbitkan *crate* bernama
`guessing_game` versi 1.0.1 dan kita ingin menariknya, kita menjalankan
perintah berikut di direktori proyek untuk `guessing_game`:

<!-- manual-regeneration:
cargo yank carol-test --version 2.1.0
cargo yank carol-test --version 2.1.0 --undo
-->

```console
$ cargo yank --vers 1.0.1
    Updating crates.io index
        Yank guessing_game@1.0.1
```

Dengan menambahkan `--undo` ke perintah itu, Anda juga dapat membatalkan
sebuah yank dan mengizinkan proyek untuk mulai bergantung pada versi itu
kembali:

```console
$ cargo yank --vers 1.0.1 --undo
    Updating crates.io index
      Unyank guessing_game@1.0.1
```

Sebuah yank _tidak_ menghapus kode apa pun. Yank, misalnya, tidak dapat
menghapus rahasia yang tidak sengaja terunggah. Jika itu terjadi, Anda harus
segera mengatur ulang rahasia-rahasia itu.

[spdx]: https://spdx.org/licenses/
[semver]: https://semver.org/
