<a id="macros"></a>
## Macro

Kita sudah memakai *macro* seperti `println!` di sepanjang buku ini, tetapi
kita belum sepenuhnya mengeksplorasi apa itu *macro* dan bagaimana ia bekerja.
Istilah *macro* (makro) merujuk pada satu keluarga fitur di Rust—*macro*
deklaratif dengan `macro_rules!` dan tiga jenis *macro* prosedural:

- *Macro* `#[derive]` kustom yang menentukan kode yang ditambahkan dengan
  atribut `derive` yang dipakai pada *struct* dan *enum*
- *Macro* mirip atribut yang mendefinisikan atribut kustom yang bisa dipakai
  pada item apa pun
- *Macro* mirip fungsi yang tampak seperti pemanggilan fungsi tetapi bekerja
  pada token yang ditentukan sebagai argumennya

Kita akan membahas semuanya satu per satu, tetapi pertama-tama, mari kita
lihat mengapa kita membutuhkan *macro* padahal kita sudah punya fungsi.

### Perbedaan antara Macro dan Fungsi

Pada dasarnya, *macro* adalah cara menulis kode yang menulis kode lain, yang
dikenal sebagai *metaprogramming* (metapemrograman). Di Lampiran C, kita
membahas atribut `derive`, yang menghasilkan implementasi berbagai *trait*
untuk Anda. Kita juga sudah memakai *macro* `println!` dan `vec!` di sepanjang
buku ini. Semua *macro* ini *diekspansi* untuk menghasilkan lebih banyak kode
daripada kode yang Anda tulis secara manual.

*Metaprogramming* berguna untuk mengurangi jumlah kode yang harus Anda tulis
dan pelihara, yang juga merupakan salah satu peran fungsi. Akan tetapi,
*macro* memiliki beberapa kekuatan tambahan yang tidak dimiliki fungsi.

Tanda tangan fungsi harus mendeklarasikan jumlah dan tipe parameter yang
dimiliki fungsi itu. Sebaliknya, *macro* bisa menerima jumlah parameter yang
bervariasi: Kita bisa memanggil `println!("hello")` dengan satu argumen atau
`println!("hello {}", name)` dengan dua argumen. Selain itu, *macro*
diekspansi sebelum kompilator menafsirkan makna kodenya, jadi sebuah *macro*
bisa, misalnya, mengimplementasikan *trait* pada tipe tertentu. Fungsi tidak
bisa, karena ia dipanggil pada runtime dan *trait* perlu diimplementasikan
pada waktu kompilasi.

Kelemahan mengimplementasikan *macro* alih-alih fungsi adalah definisi *macro*
lebih kompleks daripada definisi fungsi karena Anda menulis kode Rust yang
menulis kode Rust. Karena indireksi ini, definisi *macro* umumnya lebih sulit
dibaca, dipahami, dan dipelihara daripada definisi fungsi.

Perbedaan penting lainnya antara *macro* dan fungsi adalah Anda harus
mendefinisikan *macro* atau membawanya ke dalam *scope* *sebelum* Anda
memanggilnya di sebuah file, berbeda dengan fungsi yang bisa Anda
definisikan di mana saja dan panggil di mana saja.

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>

### Macro Deklaratif untuk Metaprogramming Umum

Bentuk *macro* yang paling banyak dipakai di Rust adalah *declarative macro*
(macro deklaratif). Macro ini kadang juga disebut “macros by example,”
“*macro* `macro_rules!`,” atau sekadar “*macro*.” Pada intinya, *macro*
deklaratif memungkinkan Anda menulis sesuatu yang mirip dengan ekspresi
`match` di Rust. Seperti yang dibahas di Bab 6, ekspresi `match` adalah
struktur kontrol yang menerima sebuah ekspresi, membandingkan nilai yang
dihasilkan ekspresi itu dengan pola-pola, lalu menjalankan kode yang
dikaitkan dengan pola yang cocok. *Macro* juga membandingkan sebuah nilai
dengan pola-pola yang dikaitkan dengan kode tertentu: Dalam situasi ini,
nilainya adalah kode sumber Rust literal yang diberikan ke *macro*;
pola-polanya dibandingkan dengan struktur kode sumber itu; dan kode yang
dikaitkan dengan setiap pola, saat cocok, menggantikan kode yang diberikan
ke *macro*. Semua ini terjadi selama kompilasi.

Untuk mendefinisikan *macro*, Anda memakai konstruk `macro_rules!`. Mari kita
telusuri cara memakai `macro_rules!` dengan melihat bagaimana *macro* `vec!`
didefinisikan. Bab 8 membahas cara kita memakai *macro* `vec!` untuk membuat
vektor baru dengan nilai-nilai tertentu. Misalnya, *macro* berikut membuat
vektor baru berisi tiga integer:

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

Kita juga bisa memakai *macro* `vec!` untuk membuat vektor berisi dua integer
atau vektor berisi lima string *slice*. Kita tidak akan bisa memakai fungsi
untuk melakukan hal yang sama karena kita tidak tahu jumlah atau tipe
nilainya di muka.

Listing 20-35 menunjukkan definisi *macro* `vec!` yang sedikit disederhanakan.

<Listing number="20-35" file-name="src/lib.rs" caption="Versi sederhana dari definisi macro `vec!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-35/src/lib.rs}}
```

</Listing>

> Catatan: Definisi asli *macro* `vec!` di pustaka standar menyertakan kode
> untuk mengalokasikan jumlah memori yang tepat di muka. Kode itu adalah
> optimasi yang tidak kita sertakan di sini, supaya contohnya lebih
> sederhana.

Anotasi `#[macro_export]` menunjukkan bahwa *macro* ini harus tersedia setiap
kali *crate* tempat *macro* itu didefinisikan dibawa ke dalam *scope*. Tanpa
anotasi ini, *macro* itu tidak bisa dibawa ke dalam *scope*.

Kita kemudian memulai definisi *macro* dengan `macro_rules!` dan nama *macro*
yang kita definisikan *tanpa* tanda seru. Nama itu, dalam kasus ini `vec`,
diikuti oleh kurung kurawal yang menandakan tubuh definisi *macro*.

Struktur di tubuh `vec!` mirip dengan struktur ekspresi `match`. Di sini
kita punya satu arm dengan pola `( $( $x:expr ),* )`, diikuti oleh `=>` dan
blok kode yang dikaitkan dengan pola ini. Jika polanya cocok, blok kode yang
terkait akan dihasilkan. Mengingat ini satu-satunya pola di *macro* ini, hanya
ada satu cara pencocokan yang valid; pola lain mana pun akan menghasilkan
galat. *Macro* yang lebih kompleks akan memiliki lebih dari satu arm.

Sintaks pola yang valid dalam definisi *macro* berbeda dari sintaks pola yang
dibahas di Bab 19 karena pola *macro* dicocokkan dengan struktur kode Rust,
bukan dengan nilai. Mari kita telusuri arti bagian-bagian pola di Listing
20-29; untuk sintaks pola *macro* selengkapnya, lihat [Rust *Reference*][ref].

Pertama, kita memakai sepasang tanda kurung untuk melingkupi seluruh pola.
Kita memakai tanda dolar (`$`) untuk mendeklarasikan variabel di sistem
*macro* yang akan memuat kode Rust yang cocok dengan polanya. Tanda dolar
memperjelas bahwa ini adalah variabel *macro*, bukan variabel Rust biasa.
Berikutnya ada sepasang tanda kurung yang menangkap nilai-nilai yang cocok
dengan pola di dalam tanda kurung itu untuk dipakai di kode penggantinya.
Di dalam `$()` ada `$x:expr`, yang mencocokkan ekspresi Rust mana pun dan
memberi ekspresi itu nama `$x`.

Koma yang mengikuti `$()` menunjukkan bahwa karakter koma pemisah literal
harus muncul di antara setiap instance kode yang cocok dengan kode di dalam
`$()`. `*` menentukan bahwa pola itu mencocokkan nol atau lebih dari apa pun
yang mendahului `*`.

Saat kita memanggil *macro* ini dengan `vec![1, 2, 3];`, pola `$x` cocok tiga
kali dengan tiga ekspresi `1`, `2`, dan `3`.

Sekarang mari kita lihat pola di tubuh kode yang dikaitkan dengan arm ini:
`temp_vec.push()` di dalam `$()*` dihasilkan untuk setiap bagian yang cocok
dengan `$()` di polanya, nol kali atau lebih, bergantung pada berapa kali
pola itu cocok. `$x` diganti dengan setiap ekspresi yang cocok. Saat kita
memanggil *macro* ini dengan `vec![1, 2, 3];`, kode yang dihasilkan untuk
menggantikan pemanggilan *macro* ini adalah sebagai berikut:

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

Kita telah mendefinisikan *macro* yang bisa menerima sejumlah argumen dengan
tipe apa pun dan bisa menghasilkan kode untuk membuat vektor berisi
elemen-elemen yang ditentukan.

Untuk mempelajari lebih lanjut cara menulis *macro*, lihat dokumentasi daring
atau sumber lain, seperti [“The Little Book of Rust Macros”][tlborm] yang
dimulai oleh Daniel Keep dan dilanjutkan oleh Lukas Wirth.

### Macro Prosedural untuk Menghasilkan Kode dari Atribut

Bentuk *macro* yang kedua adalah *macro* prosedural, yang bertindak lebih
seperti fungsi (dan merupakan jenis prosedur). *Procedural macro* (*macro*
prosedural) menerima sejumlah kode sebagai masukan, bekerja pada kode itu,
dan menghasilkan sejumlah kode sebagai keluaran, alih-alih mencocokkan
dengan pola dan mengganti kode itu dengan kode lain seperti yang dilakukan
*macro* deklaratif. Tiga jenis *macro* prosedural adalah `derive` kustom, mirip
atribut, dan mirip fungsi, dan semuanya bekerja dengan cara yang serupa.

Saat membuat *macro* prosedural, definisinya harus berada di *crate*-nya sendiri
dengan tipe *crate* khusus. Hal ini karena alasan teknis yang rumit yang kita
harap bisa dihilangkan di masa depan. Di Listing 20-36, kita menunjukkan
cara mendefinisikan *macro* prosedural, dengan `some_attribute` sebagai
placeholder untuk memakai jenis *macro* tertentu.

<Listing number="20-36" file-name="src/lib.rs" caption="Contoh pendefinisian macro prosedural">

```rust,ignore
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

Fungsi yang mendefinisikan *macro* prosedural menerima `TokenStream` sebagai
masukan dan menghasilkan `TokenStream` sebagai keluaran. Tipe `TokenStream`
didefinisikan oleh *crate* `proc_macro` yang disertakan bersama Rust dan
mewakili urutan token. Inilah inti dari *macro*: Kode sumber yang sedang
diolah *macro* membentuk `TokenStream` masukan, dan kode yang dihasilkan *macro*
adalah `TokenStream` keluaran. Fungsi itu juga memiliki atribut yang melekat
padanya yang menentukan jenis *macro* prosedural mana yang kita buat. Kita
bisa memiliki banyak jenis *macro* prosedural di *crate* yang sama.

Mari kita lihat berbagai jenis *macro* prosedural. Kita akan mulai dengan
*macro* `derive` kustom, lalu menjelaskan perbedaan-perbedaan kecil yang
membuat bentuk lainnya berbeda.

<!-- Old headings. Do not remove or links may break. -->

<a id="how-to-write-a-custom-derive-macro"></a>

<a id="custom-derive-macros"></a>
### Macro `derive` Kustom

Mari kita buat *crate* bernama `hello_macro` yang mendefinisikan *trait*
bernama `HelloMacro` dengan satu fungsi asosiasi bernama `hello_macro`.
Alih-alih membuat pengguna kita mengimplementasikan *trait* `HelloMacro`
untuk setiap tipe mereka, kita akan menyediakan *macro* prosedural sehingga
pengguna bisa menganotasi tipe mereka dengan `#[derive(HelloMacro)]` untuk
mendapatkan implementasi bawaan dari fungsi `hello_macro`. Implementasi
bawaan itu akan mencetak `Hello, Macro! My name is TypeName!` dengan
`TypeName` adalah nama tipe tempat *trait* ini didefinisikan. Dengan kata
lain, kita akan menulis *crate* yang memungkinkan pemrogram lain menulis kode
seperti Listing 20-37 dengan memakai *crate* kita.

<Listing number="20-37" file-name="src/main.rs" caption="Kode yang akan bisa ditulis oleh pengguna crate kita saat memakai macro prosedural kita">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-37/src/main.rs}}
```

</Listing>

Kode ini akan mencetak `Hello, Macro! My name is Pancakes!` saat kita
selesai. Langkah pertama adalah membuat *crate* library baru, seperti ini:

```console
$ cargo new hello_macro --lib
```

Selanjutnya, di Listing 20-38, kita akan mendefinisikan *trait* `HelloMacro`
dan fungsi asosiasinya.

<Listing file-name="src/lib.rs" number="20-38" caption="Trait sederhana yang akan kita pakai dengan macro `derive`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-38/hello_macro/src/lib.rs}}
```

</Listing>

Sekarang kita punya *trait* beserta fungsinya. Pada titik ini, pengguna *crate*
kita bisa mengimplementasikan *trait* itu untuk mencapai fungsionalitas yang
diinginkan, seperti di Listing 20-39.

<Listing number="20-39" file-name="src/main.rs" caption="Tampilannya jika pengguna menulis implementasi manual trait `HelloMacro`">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-39/pancakes/src/main.rs}}
```

</Listing>

Akan tetapi, mereka harus menulis blok implementasi untuk setiap tipe yang
ingin mereka pakai dengan `hello_macro`; kita ingin membebaskan mereka dari
keharusan melakukan pekerjaan ini.

Selain itu, kita belum bisa memberikan implementasi bawaan kepada fungsi
`hello_macro` yang akan mencetak nama tipe tempat *trait* itu
diimplementasikan: Rust tidak memiliki kemampuan refleksi, jadi ia tidak
bisa mencari nama tipe itu pada runtime. Kita butuh *macro* untuk
menghasilkan kode pada waktu kompilasi.

Langkah berikutnya adalah mendefinisikan *macro* prosedural itu. Pada saat
buku ini ditulis, *macro* prosedural harus berada di *crate*-nya sendiri. Pada
akhirnya, batasan ini mungkin akan dicabut. Konvensi untuk menyusun *crate*
dan *crate* *macro* adalah sebagai berikut: Untuk *crate* bernama `foo`, *crate*
*macro* prosedural `derive` kustomnya disebut `foo_derive`. Mari kita buat
*crate* baru bernama `hello_macro_derive` di dalam proyek `hello_macro` kita:

```console
$ cargo new hello_macro_derive --lib
```

Kedua *crate* kita saling terkait erat, jadi kita membuat *crate* *macro*
prosedural itu di dalam direktori *crate* `hello_macro`. Jika kita mengubah
definisi *trait* di `hello_macro`, kita juga harus mengubah implementasi
*macro* prosedural di `hello_macro_derive`. Kedua *crate* itu harus diterbitkan
secara terpisah, dan pemrogram yang memakai *crate*-crate ini harus
menambahkan keduanya sebagai dependensi dan membawa keduanya ke dalam *scope*.
Sebagai gantinya, kita bisa membuat *crate* `hello_macro` memakai
`hello_macro_derive` sebagai dependensi dan mengekspor ulang kode *macro*
prosedural itu. Akan tetapi, cara kita menyusun proyek ini memungkinkan
pemrogram memakai `hello_macro` meskipun mereka tidak menginginkan
fungsionalitas `derive`.

Kita perlu mendeklarasikan *crate* `hello_macro_derive` sebagai *crate* *macro*
prosedural. Kita juga akan membutuhkan fungsionalitas dari *crate* `syn` dan
`quote`, seperti yang akan Anda lihat sebentar lagi, jadi kita perlu
menambahkan keduanya sebagai dependensi. Tambahkan yang berikut ini ke file
_Cargo.toml_ untuk `hello_macro_derive`:

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</Listing>

Untuk mulai mendefinisikan *macro* prosedural, letakkan kode di Listing 20-40
ke file _src/lib.rs_ Anda untuk *crate* `hello_macro_derive`. Perhatikan
bahwa kode ini tidak akan terkompilasi sampai kita menambahkan definisi
untuk fungsi `impl_hello_macro`.

<Listing number="20-40" file-name="hello_macro_derive/src/lib.rs" caption="Kode yang dibutuhkan sebagian besar crate macro prosedural untuk memproses kode Rust">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/src/lib.rs}}
```

</Listing>

Perhatikan bahwa kita membagi kodenya menjadi fungsi `hello_macro_derive`,
yang bertanggung jawab melakukan parsing pada `TokenStream`, dan fungsi
`impl_hello_macro`, yang bertanggung jawab mentransformasi pohon sintaks:
Ini membuat penulisan *macro* prosedural lebih nyaman. Kode di fungsi luar
(`hello_macro_derive` dalam kasus ini) akan sama untuk hampir semua *crate*
*macro* prosedural yang Anda lihat atau buat. Kode yang Anda tulis di tubuh
fungsi dalam (`impl_hello_macro` dalam kasus ini) akan berbeda bergantung
pada tujuan *macro* prosedural Anda.

Kita telah memperkenalkan tiga *crate* baru: `proc_macro`,
[`syn`][syn]<!-- ignore -->, dan [`quote`][quote]<!-- ignore -->. *Crate*
`proc_macro` ikut disertakan bersama Rust, jadi kita tidak perlu
menambahkannya ke dependensi di _Cargo.toml_. *Crate* `proc_macro` adalah API
kompilator yang memungkinkan kita membaca dan memanipulasi kode Rust dari
kode kita.

*Crate* `syn` melakukan parsing kode Rust dari sebuah string menjadi struktur
data yang bisa kita olah. *Crate* `quote` mengubah struktur data `syn` kembali
menjadi kode Rust. *Crate*-crate ini membuat parsing kode Rust jenis apa pun
yang mungkin ingin kita tangani menjadi jauh lebih sederhana: Menulis parser
lengkap untuk kode Rust bukanlah tugas yang ringan.

Fungsi `hello_macro_derive` akan dipanggil ketika pengguna library kita
menuliskan `#[derive(HelloMacro)]` pada sebuah tipe. Ini dimungkinkan
karena di sini kita menganotasi fungsi `hello_macro_derive` dengan
`proc_macro_derive` dan menentukan nama `HelloMacro`, yang cocok dengan nama
*trait* kita; ini adalah konvensi yang diikuti sebagian besar *macro*
prosedural.

Fungsi `hello_macro_derive` pertama-tama mengubah `input` dari
`TokenStream` menjadi struktur data yang kemudian bisa kita tafsirkan dan
olah. Di sinilah `syn` berperan. Fungsi `parse` di `syn` menerima
`TokenStream` dan mengembalikan *struct* `DeriveInput` yang mewakili kode
Rust yang telah di-parse. Listing 20-41 menunjukkan bagian-bagian yang
relevan dari *struct* `DeriveInput` yang kita dapatkan dari parsing string
`struct Pancakes;`.

<Listing number="20-41" caption="Instance `DeriveInput` yang kita dapatkan saat melakukan parsing pada kode yang memiliki atribut macro di Listing 20-37">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</Listing>

*Field*-field *struct* ini menunjukkan bahwa kode Rust yang kita parse adalah
unit *struct* dengan `ident` (*identifier*, pengidentifikasi, yang berarti
namanya) berupa `Pancakes`. Ada lebih banyak *field* pada *struct* ini untuk
menggambarkan segala jenis kode Rust; lihat [dokumentasi `syn` untuk
`DeriveInput`][syn-docs] untuk informasi lebih lanjut.

Sebentar lagi kita akan mendefinisikan fungsi `impl_hello_macro`, tempat
kita membangun kode Rust baru yang ingin kita sertakan. Tetapi sebelum itu,
perhatikan bahwa keluaran *macro* `derive` kita juga berupa `TokenStream`.
`TokenStream` yang dikembalikan ditambahkan ke kode yang ditulis pengguna
*crate* kita, sehingga saat mereka mengompilasi *crate* mereka, mereka akan
mendapatkan fungsionalitas tambahan yang kita sediakan di `TokenStream`
yang dimodifikasi itu.

Anda mungkin menyadari bahwa di sini kita memanggil `unwrap` untuk membuat
fungsi `hello_macro_derive` panic jika pemanggilan fungsi `syn::parse`
gagal. *Macro* prosedural kita perlu panic saat terjadi galat karena fungsi
`proc_macro_derive` harus mengembalikan `TokenStream`, bukan `Result`, agar
sesuai dengan API *macro* prosedural. Kami menyederhanakan contoh ini dengan
memakai `unwrap`; di kode produksi, Anda sebaiknya memberikan pesan galat
yang lebih spesifik tentang apa yang salah dengan memakai `panic!` atau
`expect`.

Sekarang setelah kita punya kode untuk mengubah kode Rust yang dianotasi
dari `TokenStream` menjadi instance `DeriveInput`, mari kita hasilkan kode
yang mengimplementasikan *trait* `HelloMacro` pada tipe yang dianotasi,
seperti yang ditunjukkan di Listing 20-42.

<Listing number="20-42" file-name="hello_macro_derive/src/lib.rs" caption="Mengimplementasikan trait `HelloMacro` dengan memakai kode Rust yang telah di-parse">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-42/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</Listing>

Kita mendapatkan instance *struct* `Ident` yang berisi nama (identifier) tipe
yang dianotasi dengan memakai `ast.ident`. *Struct* di Listing 20-41
menunjukkan bahwa saat kita menjalankan fungsi `impl_hello_macro` pada kode
di Listing 20-37, `ident` yang kita dapatkan akan memiliki *field* `ident`
dengan nilai `"Pancakes"`. Jadi, variabel `name` di Listing 20-42 akan
berisi instance *struct* `Ident` yang, saat dicetak, menjadi string
`"Pancakes"`, yaitu nama *struct* di Listing 20-37.

*Macro* `quote!` memungkinkan kita mendefinisikan kode Rust yang ingin kita
kembalikan. Kompilator mengharapkan sesuatu yang berbeda dari hasil
langsung eksekusi *macro* `quote!`, jadi kita perlu mengonversinya menjadi
`TokenStream`. Kita melakukannya dengan memanggil metode `into`, yang
mengonsumsi representasi perantara ini dan mengembalikan nilai bertipe
`TokenStream` yang diwajibkan.

*Macro* `quote!` juga menyediakan mekanisme templating yang sangat keren:
Kita bisa menulis `#name`, dan `quote!` akan menggantinya dengan nilai di
variabel `name`. Anda bahkan bisa melakukan pengulangan yang mirip dengan
cara kerja *macro* biasa. Lihat [dokumentasi *crate* `quote`][quote-docs] untuk
pengenalan yang menyeluruh.

Kita ingin *macro* prosedural kita menghasilkan implementasi *trait*
`HelloMacro` untuk tipe yang dianotasi pengguna, yang bisa kita dapatkan
dengan memakai `#name`. Implementasi *trait* itu memiliki satu fungsi
`hello_macro`, yang tubuhnya berisi fungsionalitas yang ingin kita
sediakan: mencetak `Hello, Macro! My name is` lalu nama tipe yang dianotasi.

*Macro* `stringify!` yang dipakai di sini sudah terpasang di dalam Rust. Ia
menerima ekspresi Rust, seperti `1 + 2`, dan pada waktu kompilasi mengubah
ekspresi itu menjadi *string literal*, seperti `"1 + 2"`. Ini berbeda dari
`format!` atau `println!`, yang merupakan *macro* yang mengevaluasi ekspresi
lalu mengubah hasilnya menjadi `String`. Ada kemungkinan masukan `#name`
adalah ekspresi yang harus dicetak secara literal, jadi kita memakai
`stringify!`. Memakai `stringify!` juga menghemat satu alokasi dengan
mengubah `#name` menjadi *string literal* pada waktu kompilasi.

Pada titik ini, `cargo build` seharusnya selesai dengan sukses di
`hello_macro` maupun `hello_macro_derive`. Mari kita hubungkan *crate*-crate
ini dengan kode di Listing 20-37 untuk melihat *macro* prosedural itu
bekerja! Buat proyek binary baru di direktori _projects_ Anda dengan
`cargo new pancakes`. Kita perlu menambahkan `hello_macro` dan
`hello_macro_derive` sebagai dependensi di _Cargo.toml_ *crate* `pancakes`.
Jika Anda menerbitkan versi `hello_macro` dan `hello_macro_derive` Anda ke
[crates.io](https://crates.io/)<!-- ignore -->, keduanya akan menjadi
dependensi biasa; jika tidak, Anda bisa menentukannya sebagai dependensi
`path` seperti berikut:

```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:6:8}}
```

Letakkan kode di Listing 20-37 ke _src/main.rs_, lalu jalankan `cargo
run`: Ia seharusnya mencetak `Hello, Macro! My name is Pancakes!`.
Implementasi *trait* `HelloMacro` dari *macro* prosedural itu sudah disertakan
tanpa *crate* `pancakes` perlu mengimplementasikannya;
`#[derive(HelloMacro)]` menambahkan implementasi *trait* itu.

Selanjutnya, mari kita telusuri bagaimana jenis *macro* prosedural lainnya
berbeda dari *macro* `derive` kustom.

### Macro Mirip Atribut

*Macro* mirip atribut serupa dengan *macro* `derive` kustom, tetapi alih-alih
menghasilkan kode untuk atribut `derive`, *macro* ini memungkinkan Anda
membuat atribut baru. *Macro* ini juga lebih fleksibel: `derive` hanya bekerja
untuk *struct* dan *enum*; atribut bisa diterapkan ke item-item lain juga,
seperti fungsi. Berikut contoh pemakaian *macro* mirip atribut. Katakanlah
Anda memiliki atribut bernama `route` yang menganotasi fungsi saat memakai
framework aplikasi web:

```rust,ignore
#[route(GET, "/")]
fn index() {
```

Atribut `#[route]` ini akan didefinisikan oleh framework itu sebagai *macro*
prosedural. Tanda tangan fungsi definisi *macro*-nya akan tampak seperti ini:

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

Di sini, kita punya dua parameter bertipe `TokenStream`. Yang pertama untuk
isi atribut: bagian `GET, "/"`. Yang kedua adalah tubuh item tempat atribut
itu melekat: dalam kasus ini, `fn index() {}` dan sisa tubuh fungsinya.

Selain itu, *macro* mirip atribut bekerja dengan cara yang sama seperti *macro*
`derive` kustom: Anda membuat *crate* dengan tipe *crate* `proc-macro` dan
mengimplementasikan fungsi yang menghasilkan kode yang Anda inginkan!

### Macro Mirip Fungsi

*Macro* mirip fungsi mendefinisikan *macro* yang tampak seperti pemanggilan
fungsi. Sama seperti *macro* `macro_rules!`, *macro* ini lebih fleksibel
daripada fungsi; misalnya, *macro* ini bisa menerima jumlah argumen yang
tidak diketahui. Akan tetapi, *macro* `macro_rules!` hanya bisa didefinisikan
dengan memakai sintaks mirip match yang kita bahas di seksi [“*Macro*
Deklaratif untuk *Metaprogramming* Umum”][decl]<!-- ignore --> sebelumnya.
*Macro* mirip fungsi menerima parameter `TokenStream`, dan definisinya
memanipulasi `TokenStream` itu dengan memakai kode Rust, sama seperti yang
dilakukan dua jenis *macro* prosedural lainnya. Contoh *macro* mirip fungsi
adalah *macro* `sql!` yang bisa dipanggil seperti berikut:

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

*Macro* ini akan melakukan parsing pernyataan SQL di dalamnya dan memeriksa
bahwa pernyataan itu benar secara sintaksis, pemrosesan yang jauh lebih
kompleks daripada yang bisa dilakukan *macro* `macro_rules!`. *Macro* `sql!`
akan didefinisikan seperti ini:

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

Definisi ini mirip dengan tanda tangan *macro* `derive` kustom: Kita menerima
token yang berada di dalam tanda kurung dan mengembalikan kode yang ingin
kita hasilkan.

## Ringkasan

Fiuh! Sekarang Anda memiliki beberapa fitur Rust di kotak perkakas Anda
yang mungkin tidak akan sering Anda pakai, tetapi Anda akan tahu bahwa
fitur-fitur itu tersedia dalam keadaan yang sangat khusus. Kami telah
memperkenalkan beberapa topik yang rumit supaya saat Anda menemukannya
dalam saran pesan galat atau di kode orang lain, Anda bisa mengenali
konsep dan sintaks ini. Pakailah bab ini sebagai rujukan untuk memandu Anda
menuju solusi.

Selanjutnya, kita akan mempraktikkan semua yang telah kita bahas di
sepanjang buku ini dan mengerjakan satu proyek lagi!

[ref]: ../reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[syn]: https://crates.io/crates/syn
[quote]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming
