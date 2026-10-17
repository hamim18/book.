<!-- Old headings. Do not remove or links may break. -->

<a id="digging-into-the-traits-for-async"></a>

## Menelaah Lebih Dekat Trait-Trait untuk Async

Sepanjang bab ini, kita telah memakai *trait* `Future`, `Stream`, dan
`StreamExt` dengan berbagai cara. Namun, sejauh ini kita menghindari masuk
terlalu jauh ke detail cara kerja *trait*-trait itu atau bagaimana mereka saling
berkaitan, yang sebagian besar waktu tidak masalah untuk pekerjaan Rust
sehari-hari Anda. Akan tetapi, terkadang Anda akan menghadapi situasi yang
mengharuskan Anda memahami beberapa detail tambahan dari *trait*-trait ini,
bersama tipe `Pin` dan *trait* `Unpin`. Pada bagian ini, kita akan menggali
secukupnya untuk membantu dalam skenario-skenario itu, sambil tetap
menyerahkan penyelaman yang _benar-benar_ dalam ke dokumentasi lain.

<!-- Old headings. Do not remove or links may break. -->

<a id="future"></a>

### Trait `Future`

Mari mulai dengan menelaah lebih dekat cara kerja *trait* `Future`. Berikut cara
Rust mendefinisikannya:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Definisi *trait* itu memuat sejumlah tipe baru dan juga beberapa sintaks yang
belum pernah kita lihat, jadi mari kita telusuri definisinya bagian demi
bagian.

Pertama, tipe asosiasi `Output` dari `Future` menyatakan apa yang dihasilkan
*future* itu. Ini serupa dengan tipe asosiasi `Item` untuk *trait* `Iterator`.
Kedua, `Future` memiliki metode `poll`, yang menerima *reference* `Pin` khusus
untuk parameter `self`-nya dan *reference* *mutable* ke tipe `Context`, lalu
mengembalikan `Poll<Self::Output>`. Sebentar lagi kita akan membahas lebih
banyak tentang `Pin` dan `Context`. Untuk saat ini, mari kita fokus pada apa
yang dikembalikan metode itu, yaitu tipe `Poll`:

```rust
pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

Tipe `Poll` ini mirip dengan `Option`. Ia memiliki satu varian yang memuat
nilai, `Ready(T)`, dan satu yang tidak, `Pending`. Akan tetapi, `Poll`
berarti sesuatu yang cukup berbeda dari `Option`! Varian `Pending` menandakan
bahwa *future* itu masih punya pekerjaan yang harus dilakukan, jadi pemanggil
perlu mengecek lagi nanti. Varian `Ready` menandakan bahwa `Future` itu telah
menyelesaikan pekerjaannya dan nilai `T` sudah tersedia.

> Catatan: Jarang ada kebutuhan untuk memanggil `poll` secara langsung, tetapi
> jika Anda memang perlu, ingat bahwa pada kebanyakan *future*, pemanggil
> seharusnya tidak memanggil `poll` lagi setelah *future* itu mengembalikan
> `Ready`. Banyak *future* akan panic jika di-polling lagi setelah menjadi
> ready. *Future* yang aman untuk di-polling lagi akan menyatakannya secara
> eksplisit di dokumentasinya. Ini mirip dengan perilaku `Iterator::next`.

Ketika Anda melihat kode yang memakai `await`, Rust mengompilasinya di balik
layar menjadi kode yang memanggil `poll`. Jika Anda melihat kembali Listing
17-4, tempat kita mencetak judul halaman untuk satu URL begitu judul itu
berhasil didapat, Rust mengompilasinya menjadi sesuatu yang semacam (meskipun
tidak persis) seperti ini:

```rust,ignore
match page_title(url).poll() {
    Ready(page_title) => match page_title {
        Some(title) => println!("The title for {url} was {title}"),
        None => println!("{url} had no title"),
    }
    Pending => {
        // But what goes here?
    }
}
```

Apa yang harus kita lakukan saat *future* masih `Pending`? Kita perlu semacam
cara untuk mencoba lagi, dan lagi, dan lagi, sampai *future* itu akhirnya siap.
Dengan kata lain, kita butuh perulangan:

```rust,ignore
let mut page_title_fut = page_title(url);
loop {
    match page_title_fut.poll() {
        Ready(value) => match page_title {
            Some(title) => println!("The title for {url} was {title}"),
            None => println!("{url} had no title"),
        }
        Pending => {
            // continue
        }
    }
}
```

Namun, jika Rust mengompilasinya menjadi persis kode itu, setiap `await` akan
memblokir—justru kebalikan dari tujuan kita! Sebagai gantinya, Rust
memastikan bahwa perulangan itu bisa menyerahkan kontrol kepada sesuatu yang
bisa menjeda pekerjaan pada *future* ini untuk mengerjakan *future*-future lain,
lalu mengecek yang ini lagi nanti. Seperti yang telah kita lihat, sesuatu itu
adalah runtime async, dan pekerjaan penjadwalan serta koordinasi ini adalah
salah satu tugas utamanya.

Di bagian [“Mengirim Data antara Dua *Task* Menggunakan Message
Passing”][message-passing]<!-- ignore -->, kita membahas penungguan pada
`rx.recv`. Pemanggilan `recv` mengembalikan sebuah *future*, dan menunggu *future*
itu berarti melakukan polling padanya. Kita mencatat bahwa runtime akan
menjeda *future* itu sampai ia siap dengan `Some(message)` atau `None` ketika
*channel* ditutup. Dengan pemahaman yang lebih dalam tentang *trait* `Future`, dan
khususnya `Future::poll`, kita bisa melihat cara kerjanya. Runtime tahu *future*
itu belum siap ketika ia mengembalikan `Poll::Pending`. Sebaliknya, runtime
tahu *future* itu _sudah_ siap dan memajukannya ketika `poll` mengembalikan
`Poll::Ready(Some(message))` atau `Poll::Ready(None)`.

Detail persis cara sebuah runtime melakukannya berada di luar cakupan buku
ini, tetapi kuncinya adalah melihat mekanika dasar *future*: sebuah runtime
melakukan _polling_ pada setiap *future* yang menjadi tanggung jawabnya, lalu
membuat *future* itu kembali tidur ketika ia belum siap.

<!-- Old headings. Do not remove or links may break. -->

<a id="pinning-and-the-pin-and-unpin-traits"></a>
<a id="the-pin-and-unpin-traits"></a>

### Tipe `Pin` dan Trait `Unpin`

Kembali di Listing 17-13, kita memakai *macro* `trpl::join!` untuk menunggu
tiga *future*. Akan tetapi, lazim untuk memiliki koleksi seperti vektor yang
memuat sejumlah *future* yang jumlahnya tidak akan diketahui sampai runtime.
Mari kita ubah Listing 17-13 menjadi kode di Listing 17-23 yang menaruh ketiga
*future* itu ke dalam vektor dan memanggil fungsi `trpl::join_all`, yang belum
bisa terkompilasi.

<Listing number="17-23" caption="Menunggu future-future di dalam koleksi"  file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-23/src/main.rs:here}}
```

</Listing>

Kita menaruh setiap *future* di dalam `Box` untuk menjadikannya _trait object_,
sama seperti yang kita lakukan di bagian “Mengembalikan Error dari `run`” di
Bab 12. (Kita akan membahas *trait object* secara mendetail di Bab 18.) Memakai
*trait object* memungkinkan kita memperlakukan setiap *future* anonim yang
dihasilkan tipe-tipe ini sebagai tipe yang sama, karena semuanya
mengimplementasikan *trait* `Future`.

Ini mungkin mengejutkan. Toh, tidak ada satu pun blok async itu yang
mengembalikan apa pun, jadi setiap blok menghasilkan `Future<Output = ()>`.
Namun, ingat bahwa `Future` adalah *trait*, dan kompilator menciptakan *enum* unik
untuk setiap blok async, bahkan ketika tipe outputnya identik. Sama seperti
Anda tidak bisa menaruh dua *struct* tulisan tangan yang berbeda di dalam
`Vec`, Anda tidak bisa mencampur *enum* hasil kompilator.

Kemudian kita meneruskan koleksi *future* itu ke fungsi `trpl::join_all` dan
menunggu hasilnya. Namun, ini tidak terkompilasi; berikut bagian yang relevan
dari pesan errornya.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-23
cargo build
copy *only* the final `error` block from the errors
-->

```text
error[E0277]: `dyn Future<Output = ()>` cannot be unpinned
  --> src/main.rs:48:33
   |
48 |         trpl::join_all(futures).await;
   |                                 ^^^^^ the trait `Unpin` is not implemented for `dyn Future<Output = ()>`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
   = note: required for `Box<dyn Future<Output = ()>>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
   |
27 | pub struct JoinAll<F>
   |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`
```

Catatan dalam pesan error ini memberi tahu kita bahwa kita sebaiknya memakai
*macro* `pin!` untuk mem-_pin_ nilai-nilai itu, yang berarti menaruhnya di dalam
tipe `Pin` yang menjamin nilai-nilai itu tidak akan dipindahkan di memori.
Pesan error itu mengatakan pinning diperlukan karena `dyn Future<Output = ()>`
perlu mengimplementasikan *trait* `Unpin` dan saat ini belum
mengimplementasikannya.

Fungsi `trpl::join_all` mengembalikan sebuah *struct* bernama `JoinAll`. *Struct*
itu generik atas tipe `F`, yang dibatasi agar mengimplementasikan *trait*
`Future`. Menunggu sebuah *future* secara langsung dengan `await` akan mem-pin
*future* itu secara implisit. Itulah sebabnya kita tidak perlu memakai `pin!` di
setiap tempat kita ingin menunggu *future*.

Akan tetapi, di sini kita tidak menunggu sebuah *future* secara langsung.
Sebaliknya, kita membangun *future* baru, JoinAll, dengan meneruskan koleksi
*future* ke fungsi `join_all`. Tanda tangan untuk `join_all` mensyaratkan bahwa
tipe item-item di koleksi itu semuanya mengimplementasikan *trait* `Future`, dan
`Box<T>` mengimplementasikan `Future` hanya jika `T` yang dibungkusnya adalah
*future* yang mengimplementasikan *trait* `Unpin`.

Banyak sekali yang harus diserap! Untuk benar-benar memahaminya, mari kita
menyelam sedikit lebih jauh ke cara kerja *trait* `Future`, khususnya seputar
pinning. Lihat lagi definisi *trait* `Future`:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    // Required method
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Parameter `cx` dan tipenya, `Context`, adalah kunci dari cara sebuah runtime
benar-benar tahu kapan harus mengecek sebuah *future* tertentu sambil tetap
bersifat malas. Sekali lagi, detail cara kerjanya berada di luar cakupan bab
ini, dan Anda umumnya hanya perlu memikirkannya saat menulis implementasi
`Future` kustom. Kita akan berfokus pada tipe untuk `self`, karena ini kali
pertama kita melihat metode yang `self`-nya punya anotasi tipe. Anotasi tipe
untuk `self` bekerja seperti anotasi tipe untuk parameter fungsi lain, tetapi
dengan dua perbedaan kunci:

- Anotasi itu memberi tahu Rust tipe `self` yang harus dipenuhi agar metode
  itu bisa dipanggil.
- Anotasi itu tidak bisa berupa tipe sembarang. Anotasi ini dibatasi pada tipe
  tempat metode itu diimplementasikan, *reference* atau *smart pointer* ke tipe
  itu, atau `Pin` yang membungkus *reference* ke tipe itu.

Kita akan melihat lebih banyak sintaks ini di [Bab 18][ch-18]<!-- ignore -->.
Untuk saat ini, cukup untuk mengetahui bahwa jika kita ingin melakukan polling
pada sebuah *future* untuk mengecek apakah ia `Pending` atau `Ready(Output)`,
kita butuh *reference* *mutable* yang terbungkus `Pin` ke tipe itu.

`Pin` adalah wrapper untuk tipe-tipe yang mirip *pointer* seperti `&`, `&mut`,
`Box`, dan `Rc`. (Secara teknis, `Pin` bekerja dengan tipe yang
mengimplementasikan *trait* `Deref` atau `DerefMut`, tetapi ini secara efektif
setara dengan bekerja hanya dengan *reference* dan *smart pointer*.) `Pin`
bukanlah *pointer* itu sendiri dan tidak punya perilaku sendiri seperti yang
dimiliki `Rc` dan `Arc` dengan penghitungan referensi; `Pin` murni alat yang
bisa dipakai kompilator untuk menegakkan batasan pada pemakaian *pointer*.

Mengingat bahwa `await` diimplementasikan dalam bentuk pemanggilan `poll`
mulai menjelaskan pesan error yang kita lihat sebelumnya, tetapi itu dalam
bentuk `Unpin`, bukan `Pin`. Jadi, bagaimana persisnya hubungan `Pin` dengan
`Unpin`, dan mengapa `Future` membutuhkan `self` berada di dalam tipe `Pin`
untuk memanggil `poll`?

Ingat dari awal bab ini bahwa serangkaian await point di dalam sebuah *future*
terkompilasi menjadi state machine, dan kompilator memastikan state machine
itu mematuhi semua aturan normal Rust seputar keamanan, termasuk peminjaman
dan kepemilikan. Untuk membuatnya bekerja, Rust melihat data apa yang
dibutuhkan antara satu await point dan await point berikutnya atau akhir blok
async. Rust lalu menciptakan varian yang sesuai di state machine hasil
kompilasi. Setiap varian mendapat akses yang dibutuhkannya ke data yang akan
dipakai di bagian kode sumber itu, entah dengan mengambil kepemilikan data itu
atau dengan mendapatkan *reference* *mutable* atau *immutable* ke sana.

Sejauh ini semuanya baik-baik saja: jika ada yang keliru tentang
kepemilikan atau *reference* di blok async tertentu, *borrow checker* akan
memberi tahu kita. Ketika kita ingin memindahkan *future* yang sesuai dengan
blok itu—misalnya memindahkannya ke dalam `Vec` untuk diteruskan ke
`join_all`—semuanya menjadi lebih rumit.

Ketika kita memindahkan sebuah *future*—entah dengan mendorongnya ke dalam
struktur data untuk dipakai sebagai *iterator* dengan `join_all`, atau dengan
mengembalikannya dari fungsi—itu sebenarnya berarti memindahkan state machine
yang dibuat Rust untuk kita. Dan tidak seperti kebanyakan tipe lain di Rust,
*future* yang dibuat Rust untuk blok async bisa berakhir dengan *reference* ke
dirinya sendiri di *field* dari varian mana pun, seperti yang ditunjukkan
ilustrasi sederhana di Gambar 17-4.

<figure>

<img alt="Tabel satu kolom tiga baris yang merepresentasikan sebuah future, fut1, yang memiliki nilai data 0 dan 1 pada dua baris pertama dan sebuah panah yang menunjuk dari baris ketiga kembali ke baris kedua, merepresentasikan reference internal di dalam future tersebut." src="img/trpl17-04.svg" class="center" />

<figcaption>Gambar 17-4: Tipe data yang mengacu ke dirinya sendiri</figcaption>

</figure>

Namun, secara bawaan, objek apa pun yang punya *reference* ke dirinya sendiri
tidak aman untuk dipindahkan, karena *reference* selalu menunjuk ke alamat
memori aktual dari apa yang diacunya (lihat Gambar 17-5). Jika Anda
memindahkan struktur datanya itu sendiri, *reference* internal itu akan
tertinggal menunjuk ke lokasi lama. Akan tetapi, lokasi memori itu kini tidak
valid lagi. Pertama, nilainya tidak akan diperbarui ketika Anda membuat
perubahan pada struktur data itu. Kedua—yang lebih penting—komputer kini
bebas memakai ulang memori itu untuk keperluan lain! Anda bisa berakhir
membaca data yang sama sekali tidak berkaitan di kemudian hari.

<figure>

<img alt="Dua tabel, menggambarkan dua future, fut1 dan fut2, masing-masing memiliki satu kolom dan tiga baris, merepresentasikan hasil pemindahan sebuah future dari fut1 ke fut2. Tabel pertama, fut1, berwarna abu-abu, dengan tanda tanya di setiap indeks, merepresentasikan memori yang tidak diketahui. Tabel kedua, fut2, memiliki 0 dan 1 pada baris pertama dan kedua, dan sebuah panah yang menunjuk dari baris ketiganya kembali ke baris kedua fut1, merepresentasikan sebuah pointer yang mengacu ke lokasi lama future itu di memori sebelum dipindahkan." src="img/trpl17-05.svg" class="center" />

<figcaption>Gambar 17-5: Hasil tidak aman dari memindahkan tipe data yang mengacu ke dirinya sendiri</figcaption>

</figure>

Secara teoretis, kompilator Rust bisa mencoba memperbarui setiap *reference* ke
sebuah objek setiap kali objek itu dipindahkan, tetapi itu bisa menambah
banyak overhead performa, apalagi jika seluruh jaringan *reference* perlu
diperbarui. Jika sebagai gantinya kita bisa memastikan struktur data yang
dimaksud _tidak berpindah di memori_, kita tidak perlu memperbarui *reference*
mana pun. Inilah tepatnya kegunaan *borrow checker* Rust: dalam kode yang aman,
*borrow checker* mencegah Anda memindahkan item mana pun yang memiliki
*reference* aktif ke sana.

`Pin` dibangun di atas itu untuk memberi kita jaminan yang persis kita
butuhkan. Ketika kita mem-_pin_ sebuah nilai dengan membungkus *pointer* ke
nilai itu di dalam `Pin`, nilai itu tidak bisa lagi berpindah. Dengan
demikian, jika Anda punya `Pin<Box<SomeType>>`, Anda sebenarnya mem-pin nilai
`SomeType`, _bukan_ *pointer* `Box`-nya. Gambar 17-6 mengilustrasikan proses
ini.

<figure>

<img alt="Tiga kotak tersusun bersebelahan. Kotak pertama diberi label “Pin”, yang kedua “b1”, dan yang ketiga “pinned”. Di dalam “pinned” terdapat tabel berlabel “fut”, dengan satu kolom; tabel itu merepresentasikan sebuah future dengan sel untuk setiap bagian struktur datanya. Sel pertamanya berisi nilai “0”, sel keduanya memiliki panah yang keluar darinya dan menunjuk ke sel keempat sekaligus terakhir, yang berisi nilai “1”, dan sel ketiga memiliki garis putus-putus serta elipsis untuk menunjukkan bahwa mungkin ada bagian lain dari struktur data itu. Secara keseluruhan, tabel “fut” merepresentasikan sebuah future yang mengacu ke dirinya sendiri. Sebuah panah keluar dari kotak berlabel “Pin”, melewati kotak berlabel “b1”, dan berakhir di dalam kotak “pinned” pada tabel “fut”." src="img/trpl17-06.svg" class="center" />

<figcaption>Gambar 17-6: Mem-pin sebuah `Box` yang menunjuk ke tipe *future* yang mengacu ke dirinya sendiri</figcaption>

</figure>

Bahkan, *pointer* `Box` itu tetap bisa berpindah-pindah dengan bebas. Ingat:
yang kita pedulikan adalah memastikan data yang pada akhirnya diacu tetap
berada di tempatnya. Jika sebuah *pointer* berpindah-pindah, _tetapi data yang
ditunjuknya_ berada di tempat yang sama, seperti di Gambar 17-7, tidak ada
masalah potensial. (Sebagai latihan mandiri, lihat dokumentasi tipe-tipe itu
serta modul `std::pin` dan cobalah mencari tahu cara Anda melakukannya dengan
`Pin` yang membungkus sebuah `Box`.) Kuncinya adalah tipe yang mengacu ke
dirinya sendiri itu tidak bisa berpindah, karena ia tetap ter-pin.

<figure>

<img alt="Empat kotak tersusun dalam tiga kolom kasar, identik dengan diagram sebelumnya dengan satu perubahan pada kolom kedua. Sekarang ada dua kotak di kolom kedua, berlabel “b1” dan “b2”; “b1” berwarna abu-abu, dan panah dari “Pin” melewati “b2” alih-alih “b1”, menunjukkan bahwa pointer telah berpindah dari “b1” ke “b2”, tetapi data di “pinned” tidak berpindah." src="img/trpl17-07.svg" class="center" />

<figcaption>Gambar 17-7: Memindahkan sebuah `Box` yang menunjuk ke tipe *future* yang mengacu ke dirinya sendiri</figcaption>

</figure>

Akan tetapi, kebanyakan tipe sepenuhnya aman untuk dipindahkan, bahkan jika
mereka kebetulan berada di balik *pointer* `Pin`. Kita hanya perlu memikirkan
pinning ketika item punya *reference* internal. Nilai primitif seperti angka dan
Boolean aman karena jelas tidak punya *reference* internal. Kebanyakan tipe yang
biasa Anda pakai di Rust juga tidak. Anda bisa memindahkan `Vec`, contohnya,
tanpa khawatir. Mengingat apa yang telah kita lihat sejauh ini, jika Anda
punya `Pin<Vec<String>>`, Anda harus melakukan semuanya melalui API yang aman
tetapi membatasi yang disediakan `Pin`, meskipun `Vec<String>` selalu aman
untuk dipindahkan jika tidak ada *reference* lain ke sana. Kita butuh cara untuk
memberi tahu kompilator bahwa tidak apa-apa memindahkan item pada kasus
seperti ini—dan di situlah `Unpin` berperan.

`Unpin` adalah *marker trait*, mirip dengan *trait* `Send` dan `Sync` yang kita
lihat di Bab 16, sehingga tidak punya fungsionalitas sendiri. *Marker trait*
ada hanya untuk memberi tahu kompilator bahwa aman memakai tipe yang
mengimplementasikan *trait* tertentu dalam konteks tertentu. `Unpin`
memberitahukan kompilator bahwa tipe tertentu _tidak_ perlu mempertahankan
jaminan apa pun tentang apakah nilai yang dimaksud bisa dipindahkan dengan
aman.

<!--
  The inline `<code>` in the next block is to allow the inline `<em>` inside it,
  matching what NoStarch does style-wise, and emphasizing within the text here
  that it is something distinct from a normal type.
-->

Sama seperti `Send` dan `Sync`, kompilator mengimplementasikan `Unpin` secara
otomatis untuk semua tipe yang bisa dibuktikan aman olehnya. Kasus khususnya,
lagi-lagi mirip dengan `Send` dan `Sync`, adalah ketika `Unpin` _tidak_
diimplementasikan untuk sebuah tipe. Notasi untuk ini adalah
<code>impl !Unpin for <em>SomeType</em></code>, dengan
<code><em>SomeType</em></code> adalah nama tipe yang _memang_ perlu
mempertahankan jaminan-jaminan itu agar aman setiap kali *pointer* ke tipe itu
dipakai di dalam `Pin`.

Dengan kata lain, ada dua hal yang perlu diingat tentang hubungan antara `Pin`
dan `Unpin`. Pertama, `Unpin` adalah kasus yang “normal”, dan `!Unpin` adalah
kasus khusus. Kedua, apakah sebuah tipe mengimplementasikan `Unpin` atau
`!Unpin` _hanya_ penting ketika Anda memakai *pointer* ter-pin ke tipe itu
seperti <code>Pin<&mut <em>SomeType</em>></code>.

Untuk membuatnya konkret, pikirkan sebuah `String`: ia punya panjang dan
karakter-karakter Unicode yang menyusunnya. Kita bisa membungkus `String` di
dalam `Pin`, seperti terlihat di Gambar 17-8. Namun, `String` secara otomatis
mengimplementasikan `Unpin`, begitu pula kebanyakan tipe lain di Rust.

<figure>

<img alt="Sebuah kotak berlabel “Pin” di kiri dengan panah darinya menuju kotak berlabel “String” di kanan. Kotak “String” berisi data 5usize, yang merepresentasikan panjang string, dan huruf-huruf “h”, “e”, “l”, “l”, dan “o” yang merepresentasikan karakter string “hello” yang tersimpan di instance String ini. Sebuah persegi panjang putus-putus mengelilingi kotak “String” beserta labelnya, tetapi bukan kotak “Pin”." src="img/trpl17-08.svg" class="center" />

<figcaption>Gambar 17-8: Mem-pin sebuah `String`; garis putus-putus menunjukkan bahwa `String` mengimplementasikan *trait* `Unpin` sehingga ia tidak ter-pin</figcaption>

</figure>

Hasilnya, kita bisa melakukan hal-hal yang akan menjadi tidak sah jika
`String` mengimplementasikan `!Unpin`, seperti mengganti satu string dengan
string lain di lokasi memori yang persis sama seperti di Gambar 17-9. Ini
tidak melanggar kontrak `Pin`, karena `String` tidak punya *reference* internal
yang membuatnya tidak aman untuk dipindahkan. Justru itulah alasan ia
mengimplementasikan `Unpin` alih-alih `!Unpin`.

<figure>

<img alt="Data string “hello” yang sama dari contoh sebelumnya, kini berlabel “s1” dan berwarna abu-abu. Kotak “Pin” dari contoh sebelumnya kini menunjuk ke instance String yang berbeda, yang berlabel “s2”, valid, memiliki panjang 7usize, dan berisi karakter string “goodbye”. s2 dikelilingi persegi panjang putus-putus karena ia juga mengimplementasikan trait Unpin." src="img/trpl17-09.svg" class="center" />

<figcaption>Gambar 17-9: Mengganti `String` itu dengan `String` yang sepenuhnya berbeda di memori</figcaption>

</figure>

Sekarang kita cukup tahu untuk memahami error yang dilaporkan untuk
pemanggilan `join_all` dari Listing 17-23. Awalnya kita mencoba memindahkan
future yang dihasilkan blok async ke dalam `Vec<Box<dyn Future<Output =
()>>>`, tetapi seperti yang telah kita lihat, future-future itu mungkin punya
*reference* internal, jadi mereka tidak otomatis mengimplementasikan `Unpin`.
Begitu kita mem-pin mereka, kita bisa meneruskan tipe `Pin` yang dihasilkan ke
dalam `Vec`, yakin bahwa data yang mendasari *future*-future itu _tidak_ akan
dipindahkan. Listing 17-24 menunjukkan cara memperbaiki kodenya dengan
memanggil *macro* `pin!` di tempat ketiga *future* itu didefinisikan dan
menyesuaikan tipe *trait object*-nya.

<Listing number="17-24" caption="Mem-pin future-future itu agar bisa dipindahkan ke dalam vektor">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-24/src/main.rs:here}}
```

</Listing>

Contoh ini sekarang terkompilasi dan berjalan, dan kita bisa menambahkan atau
menghapus *future* dari vektor pada saat runtime dan menggabungkan semuanya.

`Pin` dan `Unpin` kebanyakan penting untuk membangun library tingkat yang
lebih rendah, atau ketika Anda membangun runtime itu sendiri, alih-alih untuk
kode Rust sehari-hari. Akan tetapi, saat Anda melihat *trait*-trait ini di pesan
error, sekarang Anda akan punya gambaran yang lebih baik tentang cara
memperbaiki kode Anda!

> Catatan: Kombinasi `Pin` dan `Unpin` ini memungkinkan implementasi yang aman
> untuk seluruh kelas tipe kompleks di Rust yang jika tidak akan terbukti
> menantang karena mereka mengacu ke dirinya sendiri. Tipe yang memerlukan
> `Pin` paling sering muncul di Rust async saat ini, tetapi sesekali Anda
> mungkin melihatnya di konteks lain juga.
>
> Kekhususan cara kerja `Pin` dan `Unpin`, serta aturan-aturan yang harus
> mereka pertahankan, dibahas secara ekstensif di dokumentasi API untuk
> `std::pin`, jadi jika Anda tertarik mempelajari lebih lanjut, itu tempat
> yang bagus untuk memulai.
>
> Jika Anda ingin memahami cara kerja di balik layar dengan detail yang lebih
> dalam lagi, lihat Bab [2][under-the-hood]<!-- ignore --> dan
> [4][pinning]<!-- ignore --> dari
> [_Asynchronous Programming in Rust_][async-book].

### Trait `Stream`

Sekarang setelah Anda punya pemahaman yang lebih dalam tentang *trait*
`Future`, `Pin`, dan `Unpin`, kita bisa mengalihkan perhatian ke *trait*
`Stream`. Seperti yang Anda pelajari di awal bab ini, *stream* mirip dengan
*iterator* asinkron. Akan tetapi, tidak seperti `Iterator` dan `Future`,
`Stream` belum punya definisi di pustaka standar saat tulisan ini dibuat,
tetapi _ada_ definisi yang sangat umum dari *crate* `futures` yang dipakai di
seluruh ekosistem.

Mari kita tinjau definisi *trait* `Iterator` dan `Future` sebelum melihat
bagaimana *trait* `Stream` menggabungkan keduanya. Dari `Iterator`, kita punya
gagasan tentang urutan: metode `next`-nya menyediakan `Option<Self::Item>`.
Dari `Future`, kita punya gagasan tentang kesiapan seiring waktu: metode
`poll`-nya menyediakan `Poll<Self::Output>`. Untuk merepresentasikan urutan
item yang menjadi siap seiring waktu, kita mendefinisikan *trait* `Stream` yang
menggabungkan kedua fitur itu:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

trait Stream {
    type Item;

    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>
    ) -> Poll<Option<Self::Item>>;
}
```

*Trait* `Stream` mendefinisikan tipe asosiasi bernama `Item` untuk tipe item
yang dihasilkan *stream* itu. Ini mirip dengan `Iterator`, yang itemnya bisa
nol hingga banyak, dan tidak seperti `Future`, yang selalu punya satu
`Output`, bahkan jika itu tipe unit `()`.

`Stream` juga mendefinisikan metode untuk mendapatkan item-item itu. Kita
menamainya `poll_next`, untuk memperjelas bahwa metode itu melakukan polling
dengan cara yang sama seperti `Future::poll` dan menghasilkan urutan item
dengan cara yang sama seperti `Iterator::next`. Tipe kembaliannya
menggabungkan `Poll` dengan `Option`. Tipe luarnya adalah `Poll`, karena ia
harus dicek kesiapannya, sama seperti *future*. Tipe dalamnya adalah `Option`,
karena ia perlu memberi sinyal apakah masih ada pesan lagi, sama seperti
*iterator*.

Sesuatu yang sangat mirip dengan definisi ini kemungkinan besar akan berakhir
menjadi bagian dari pustaka standar Rust. Sementara itu, definisi ini menjadi
bagian dari perangkat kebanyakan runtime, jadi Anda bisa mengandalkannya, dan
semua yang kita bahas berikutnya secara umum seharusnya berlaku!

Akan tetapi, pada contoh yang kita lihat di bagian [“*Streams*: *Future* dalam
Urutan”][streams]<!-- ignore -->, kita tidak memakai `poll_next` _atau_
`Stream`, melainkan `next` dan `StreamExt`. Tentu saja, kita _bisa_ bekerja
langsung dalam bentuk API `poll_next` dengan menulis sendiri state machine
`Stream` kita, sama seperti kita _bisa_ bekerja dengan *future* secara langsung
melalui metode `poll` mereka. Akan tetapi, memakai `await` jauh lebih nyaman,
dan *trait* `StreamExt` menyediakan metode `next` supaya kita bisa melakukan
persis itu:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-stream-ext/src/lib.rs:here}}
```

<!--
TODO: update this if/when tokio/etc. update their MSRV and switch to using async functions
in traits, since the lack thereof is the reason they do not yet have this.
-->

> Catatan: Definisi aktual yang kita pakai di awal bab ini terlihat sedikit
> berbeda dari ini, karena definisi itu mendukung versi Rust yang belum
> mendukung pemakaian fungsi async di dalam *trait*. Hasilnya, definisi itu
> terlihat seperti ini:
>
> ```rust,ignore
> fn next(&mut self) -> Next<'_, Self> where Self: Unpin;
> ```
>
> Tipe `Next` itu adalah `struct` yang mengimplementasikan `Future` dan
> memungkinkan kita menamai *lifetime* *reference* ke `self` dengan
> `Next<'_, Self>`, sehingga `await` bisa bekerja dengan metode ini.

*Trait* `StreamExt` juga merupakan rumah bagi semua metode menarik yang tersedia
untuk dipakai dengan *stream*. `StreamExt` diimplementasikan secara otomatis
untuk setiap tipe yang mengimplementasikan `Stream`, tetapi *trait*-trait ini
didefinisikan terpisah untuk memungkinkan komunitas mengembangkan API
kenyamanan secara iteratif tanpa memengaruhi *trait* dasarnya.

Pada versi `StreamExt` yang dipakai *crate* `trpl`, *trait* itu tidak hanya
mendefinisikan metode `next`, tetapi juga menyediakan implementasi bawaan
`next` yang menangani detail pemanggilan `Stream::poll_next` dengan benar.
Artinya, bahkan ketika Anda perlu menulis tipe data streaming Anda sendiri,
Anda _hanya_ perlu mengimplementasikan `Stream`, lalu siapa pun yang memakai
tipe data Anda bisa memakai `StreamExt` dan metode-metodenya secara otomatis.

Itu saja yang akan kita bahas untuk detail tingkat rendah dari *trait*-trait
ini. Sebagai penutup, mari kita pertimbangkan bagaimana *future* (termasuk
*stream*), *task*, dan thread saling berkaitan!

[message-passing]: ch17-02-concurrency-with-async.md#sending-data-between-two-tasks-using-message-passing
[ch-18]: ch18-00-oop.html
[async-book]: https://rust-lang.github.io/async-book/
[under-the-hood]: https://rust-lang.github.io/async-book/02_execution/01_chapter.html
[pinning]: https://rust-lang.github.io/async-book/04_pinning/01_chapter.html
[first-async]: ch17-01-futures-and-syntax.html#our-first-async-program
[any-number-futures]: ch17-03-more-futures.html#working-with-any-number-of-futures
[streams]: ch17-04-streams.html
