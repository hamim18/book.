<!-- Old headings. Do not remove or links may break. -->

<a id="defining-modules-to-control-scope-and-privacy"></a>

## Mengontrol Scope dan Privasi dengan Module

Di bagian ini, kita akan membahas *module* dan bagian-bagian lain dari *module*
system, yaitu *path*, yang memungkinkan Anda memberi nama item; *keyword*
`use` yang membawa sebuah *path* ke dalam *scope*; dan *keyword* `pub` untuk
menjadikan item publik. Kita juga akan membahas *keyword* `as`, *package*
eksternal, dan operator *glob*.

### Lembar Contekan Module

Sebelum masuk ke detail *module* dan *path*, di sini kita menyediakan rujukan
cepat tentang cara kerja *module*, *path*, *keyword* `use`, dan *keyword* `pub`
di dalam *compiler*, serta cara sebagian besar pengembang mengatur kode mereka.
Kita akan menelusuri contoh dari masing-masing aturan ini di sepanjang bab
ini, tetapi bagian ini adalah tempat yang bagus untuk dirujuk sebagai
pengingat cara kerja *module*.

- **Mulai dari crate root**: Saat mengompilasi sebuah *crate*, *compiler*
  pertama-tama mencari kode untuk dikompilasi di file *crate root* (biasanya
  _src/lib.rs_ untuk *crate* library dan _src/main.rs_ untuk *crate* binary).
- **Mendeklarasikan module**: Di file *crate root*, Anda dapat mendeklarasikan
  *module*-module baru; katakanlah Anda mendeklarasikan *module* “garden” dengan
  `mod garden;`. *Compiler* akan mencari kode *module* tersebut di tempat-tempat
  berikut:
  - Inline, di dalam kurung kurawal yang menggantikan titik koma setelah `mod
    garden`
  - Di file _src/garden.rs_
  - Di file _src/garden/mod.rs_
- **Mendeklarasikan submodule**: Di file mana pun selain *crate root*, Anda
  dapat mendeklarasikan submodule. Misalnya, Anda dapat mendeklarasikan `mod
  vegetables;` di _src/garden.rs_. *Compiler* akan mencari kode submodule
  tersebut di dalam direktori yang diberi nama sesuai *module* induknya, di
  tempat-tempat berikut:
  - Inline, tepat setelah `mod vegetables`, di dalam kurung kurawal, bukan
    titik koma
  - Di file _src/garden/vegetables.rs_
  - Di file _src/garden/vegetables/mod.rs_
- **Path menuju kode di dalam module**: Begitu sebuah *module* menjadi bagian
  dari *crate* Anda, Anda dapat merujuk kode di *module* tersebut dari tempat lain
  mana pun di *crate* yang sama, selama aturan privasi mengizinkannya, dengan
  memakai *path* menuju kode tersebut. Misalnya, type `Asparagus` di *module*
  garden vegetables akan ditemukan di
  `crate::garden::vegetables::Asparagus`.
- **Privat vs. publik**: Kode di dalam sebuah *module* bersifat privat dari
  *module*-module induknya secara default. Untuk menjadikan sebuah *module*
  publik, deklarasikan dengan `pub mod`, bukan `mod`. Untuk menjadikan
  item-item di dalam *module* publik ikut publik, pakai `pub` sebelum
  deklarasinya.
- ***keyword* `use`**: Di dalam sebuah *scope*, *keyword* `use` membuat
  pintasan menuju item untuk mengurangi pengulangan *path* yang panjang. Di
  *scope* mana pun yang dapat merujuk ke
  `crate::garden::vegetables::Asparagus`, Anda dapat membuat pintasan dengan
  `use
  crate::garden::vegetables::Asparagus;`, dan sejak saat itu Anda cukup
  menulis `Asparagus` untuk memakai type tersebut di dalam *scope*.

Di sini, kita membuat sebuah *crate* binary bernama `backyard` yang
mengilustrasikan aturan-aturan ini. Direktori *crate* tersebut, yang juga
bernama _backyard_, berisi file dan direktori berikut:

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

File *crate root* dalam kasus ini adalah _src/main.rs_, dan isinya:

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

Baris `pub mod garden;` memberi tahu *compiler* untuk menyertakan kode yang
ditemukannya di _src/garden.rs_, yang isinya:

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

Di sini, `pub mod vegetables;` berarti kode di _src/garden/vegetables.rs_ ikut
disertakan. Kode itu adalah:

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

Sekarang mari kita masuk ke detail aturan-aturan ini dan menunjukkannya
beraksi!

### Mengelompokkan Kode yang Berkaitan di dalam Module

_Modules_ memungkinkan kita mengatur kode di dalam sebuah *crate* demi
keterbacaan dan kemudahan pemakaian ulang. *Module* juga memungkinkan kita
mengontrol *privacy* (privasi) item, karena kode di dalam sebuah *module*
bersifat privat secara default. Item privat adalah detail implementasi
internal yang tidak tersedia untuk dipakai dari luar. Kita dapat memilih untuk
menjadikan *module* dan item-item di dalamnya publik, yang mengeksposnya agar
kode eksternal dapat memakai dan bergantung padanya.

Sebagai contoh, mari kita tulis sebuah *crate* library yang menyediakan
fungsionalitas sebuah restoran. Kita akan mendefinisikan *signature*
fungsi-fungsinya tetapi membiarkan badannya kosong supaya kita berkonsentrasi
pada pengaturan kode, bukan pada implementasi sebuah restoran.

Di industri restoran, sebagian bagian sebuah restoran disebut sebagai front of
house dan sebagian lain disebut back of house. *Front of house* (area depan)
adalah tempat pelanggan berada; ini mencakup tempat host mendudukkan
pelanggan, pelayan menerima pesanan dan pembayaran, serta bartender membuat
minuman. *Back of house* (area belakang) adalah tempat koki dan juru masak
bekerja di dapur, tukang cuci piring membersihkan, dan manajer melakukan
pekerjaan administratif.

Untuk menyusun *crate* kita dengan cara ini, kita dapat mengatur
fungsi-fungsinya ke dalam *module* bersarang. Buat library baru bernama
`restaurant` dengan menjalankan `cargo new restaurant --lib`. Lalu, masukkan
kode di Listing 7-1 ke _src/lib.rs_ untuk mendefinisikan beberapa *module* dan
*signature* fungsi; kode ini adalah bagian front of house.

<Listing number="7-1" file-name="src/lib.rs" caption="Sebuah module `front_of_house` yang berisi module-module lain yang kemudian berisi fungsi-fungsi">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

Kita mendefinisikan sebuah *module* dengan *keyword* `mod` yang diikuti nama
*module* (dalam kasus ini, `front_of_house`). Badan *module* kemudian diletakkan
di dalam kurung kurawal. Di dalam *module*, kita dapat menempatkan *module* lain,
seperti dalam kasus ini dengan *module* `hosting` dan `serving`. *Module* juga
dapat memuat definisi untuk item lain, seperti *struct*, *enum*, constant, *trait*,
dan seperti di Listing 7-1, fungsi.

Dengan memakai *module*, kita dapat mengelompokkan definisi-definisi yang
berkaitan dan memberi nama alasan keterkaitannya. Programmer yang memakai kode
ini dapat menavigasi kode berdasarkan kelompok-kelompok tersebut alih-alih
harus membaca semua definisi, sehingga lebih mudah menemukan definisi yang
relevan bagi mereka. Programmer yang menambahkan fungsionalitas baru ke kode
ini akan tahu tempat menempatkan kodenya agar program tetap teratur.

Sebelumnya, kita menyebutkan bahwa _src/main.rs_ dan _src/lib.rs_ disebut
*crate root* (akar *crate*). Alasan penamaannya adalah bahwa isi salah satu dari
kedua file tersebut membentuk sebuah *module* bernama `crate` di akar struktur
*module* *crate*, yang dikenal sebagai *module tree* (pohon modul).

Listing 7-2 menunjukkan *module tree* untuk struktur di Listing 7-1.

<Listing number="7-2" caption="Module tree untuk kode di Listing 7-1">

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

</Listing>

Pohon ini menunjukkan bagaimana sebagian *module* bersarang di dalam *module*
lain; misalnya, `hosting` bersarang di dalam `front_of_house`. Pohon ini juga
menunjukkan bahwa sebagian *module* adalah *sibling* (saudara), artinya
*module*-module tersebut didefinisikan di dalam *module* yang sama; `hosting` dan
`serving` adalah sibling yang didefinisikan di dalam `front_of_house`. Jika
*module* A berada di dalam *module* B, kita katakan bahwa *module* A adalah *child*
(anak) dari *module* B dan *module* B adalah *parent* (induk) dari *module* A.
Perhatikan bahwa seluruh *module tree* berakar di bawah *module* implisit bernama
`crate`.

*Module tree* mungkin mengingatkan Anda pada pohon direktori sistem file di
komputer Anda; ini perbandingan yang sangat tepat! Sama seperti direktori di
dalam sistem file, Anda memakai *module* untuk mengatur kode Anda. Dan sama
seperti file di dalam direktori, kita memerlukan cara untuk menemukan *module*
kita.
