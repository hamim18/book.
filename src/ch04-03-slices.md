## Tipe Slice

*Slice* memungkinkan Anda merujuk pada urutan elemen yang berkesinambungan di
dalam sebuah [koleksi](ch08-00-common-collections.md)<!-- ignore -->. *Slice*
adalah salah satu jenis *reference*, jadi ia tidak memiliki *ownership*.

Berikut sebuah soal pemrograman kecil: tulis sebuah fungsi yang menerima
*string* berisi kata-kata yang dipisahkan spasi dan mengembalikan kata
pertama yang ditemukannya dalam *string* tersebut. Jika fungsi tidak
menemukan spasi di dalam *string*, seluruh *string* itu pasti satu kata, jadi
seluruh *string* harus dikembalikan.

> Catatan: Demi memperkenalkan *slice*, pada bagian ini kita hanya
> mengasumsikan ASCII; pembahasan yang lebih menyeluruh tentang penanganan
> UTF-8 ada di bagian [“Menyimpan Teks Terenkode UTF-8 dengan
> String”][strings]<!-- ignore --> pada Bab 8.

Mari kita telusuri bagaimana kita menulis *signature* fungsi ini tanpa
menggunakan *slice*, untuk memahami masalah yang akan dipecahkan oleh
*slice*:

```rust,ignore
fn first_word(s: &String) -> ?
```

Fungsi `first_word` memiliki parameter bertipe `&String`. Kita tidak
membutuhkan *ownership*, jadi ini tidak masalah. (Dalam Rust yang idiomatis,
fungsi tidak mengambil *ownership* dari argumennya kecuali memang perlu, dan
alasannya akan menjadi jelas seiring perjalanan kita.) Tetapi apa yang harus
kita kembalikan? Kita sebenarnya tidak punya cara untuk membicarakan
*sebagian* dari sebuah *string*. Namun, kita bisa mengembalikan indeks akhir
kata, yang ditandai oleh spasi. Mari kita coba, seperti ditunjukkan pada
Listing 4-7.

<Listing number="4-7" file-name="src/main.rs" caption="Fungsi `first_word` yang mengembalikan nilai indeks byte ke dalam parameter `String`">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:here}}
```

</Listing>

Karena kita perlu menelusuri `String` elemen demi elemen dan memeriksa apakah
suatu nilai adalah spasi, kita akan mengonversi `String` kita menjadi array
berisi byte menggunakan metode `as_bytes`.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:as_bytes}}
```

Selanjutnya, kita membuat sebuah *iterator* untuk array byte tersebut
menggunakan metode `iter`:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:iter}}
```

Kita akan membahas *iterator* secara lebih mendetail di [Bab
13][ch13]<!-- ignore -->. Untuk sekarang, ketahuilah bahwa `iter` adalah
metode yang mengembalikan setiap elemen dalam sebuah koleksi, dan bahwa
`enumerate` membungkus hasil dari `iter` dan mengembalikan setiap elemen
sebagai bagian dari sebuah *tuple*. Elemen pertama dari *tuple* yang
dikembalikan `enumerate` adalah indeksnya, dan elemen kedua adalah
*reference* ke elemen tersebut. Ini sedikit lebih praktis daripada
menghitung indeksnya sendiri.

Karena metode `enumerate` mengembalikan sebuah *tuple*, kita dapat
menggunakan pola untuk mendestrukturisasi *tuple* tersebut. Kita akan
membahas pola lebih lanjut di [Bab 6][ch6]<!-- ignore -->. Di dalam
perulangan `for`, kita menentukan sebuah pola yang memuat `i` untuk indeks
dalam *tuple* dan `&item` untuk byte tunggal dalam *tuple*. Karena kita
mendapatkan *reference* ke elemen dari `.iter().enumerate()`, kita
menggunakan `&` di dalam pola tersebut.

Di dalam perulangan `for`, kita mencari byte yang merepresentasikan spasi
menggunakan sintaks literal byte. Jika kita menemukan spasi, kita
mengembalikan posisinya. Jika tidak, kita mengembalikan panjang *string*
menggunakan `s.len()`.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:inside_for}}
```

Sekarang kita punya cara untuk menemukan indeks akhir kata pertama di dalam
*string*, tetapi ada masalahnya. Kita mengembalikan `usize` begitu saja,
padahal angka itu hanya bermakna dalam konteks `&String`-nya. Dengan kata
lain, karena ia adalah nilai yang terpisah dari `String`, tidak ada jaminan
bahwa ia akan tetap valid di masa mendatang. Perhatikan program pada Listing
4-8 yang menggunakan fungsi `first_word` dari Listing 4-7.

<Listing number="4-8" file-name="src/main.rs" caption="Menyimpan hasil pemanggilan fungsi `first_word` lalu mengubah isi `String`">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-08/src/main.rs:here}}
```

</Listing>

Program ini terkompilasi tanpa galat apa pun, dan tetap akan terkompilasi
jika kita menggunakan `word` setelah memanggil `s.clear()`. Karena `word`
sama sekali tidak terhubung dengan keadaan `s`, `word` tetap berisi nilai
`5`. Kita bisa menggunakan nilai `5` itu bersama variabel `s` untuk mencoba
mengekstrak kata pertama, tetapi ini akan menjadi sebuah bug karena isi `s`
telah berubah sejak kita menyimpan `5` di `word`.

Harus mengkhawatirkan indeks di `word` yang bisa tidak sinkron dengan data di
`s` itu melelahkan dan rawan galat! Mengelola indeks-indeks ini bahkan lebih
rapuh jika kita menulis fungsi `second_word`. *Signature*-nya harus terlihat
seperti ini:

```rust,ignore
fn second_word(s: &String) -> (usize, usize) {
```

Sekarang kita melacak indeks awal _dan_ indeks akhir, dan kita memiliki lebih
banyak lagi nilai yang dihitung dari data pada keadaan tertentu tetapi sama
sekali tidak terikat pada keadaan itu. Ada tiga variabel yang tidak saling
berhubungan bertebaran yang harus dijaga agar tetap sinkron.

Untungnya, Rust memiliki solusi untuk masalah ini: *string slice*.

### Slice String

Sebuah *string slice* adalah *reference* ke urutan elemen yang
berkesinambungan dari sebuah `String`, dan tampilannya seperti ini:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-17-slice/src/main.rs:here}}
```

Alih-alih *reference* ke seluruh `String`, `hello` adalah *reference* ke
sebagian dari `String`, yang ditentukan oleh tambahan `[0..5]` itu. Kita
membuat *slice* menggunakan rentang di dalam kurung siku dengan menentukan
`[starting_index..ending_index]`, dengan _`starting_index`_ sebagai posisi
pertama dalam *slice* dan _`ending_index`_ satu lebih banyak dari posisi
terakhir dalam *slice*. Di dalam, struktur data *slice* menyimpan posisi awal
dan panjang *slice*, yang sama dengan _`ending_index`_ dikurangi
_`starting_index`_. Jadi, dalam kasus `let world = &s[6..11];`, `world` akan
menjadi *slice* yang memuat *pointer* ke byte pada indeks 6 dari `s` dengan
nilai panjang `5`.

Gambar 4-7 menunjukkannya dalam sebuah diagram.

<img alt="Tiga tabel: sebuah tabel yang merepresentasikan data stack dari s,
yang menunjuk ke byte pada indeks 0 di tabel data string
&quot;hello world&quot; di heap. Tabel ketiga merepresentasikan data stack dari
slice world, yang memiliki nilai panjang 5 dan menunjuk ke byte 6 dari tabel
data heap." src="img/trpl04-07.svg" class="center" style="width: 50%;" />

<span class="caption">Gambar 4-7: Sebuah string slice yang merujuk ke sebagian
dari `String`</span>

Dengan sintaks rentang `..` milik Rust, jika Anda ingin memulai dari indeks
0, Anda dapat menghilangkan nilai sebelum dua titik. Dengan kata lain,
keduanya sama:

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

Dengan alasan yang sama, jika *slice* Anda mencakup byte terakhir dari
`String`, Anda dapat menghilangkan angka di belakangnya. Artinya, keduanya
sama:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

Anda juga dapat menghilangkan kedua nilai untuk mengambil *slice* dari
seluruh *string*. Jadi, keduanya sama:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> Catatan: Indeks rentang *string slice* harus berada pada batas karakter
> UTF-8 yang valid. Jika Anda mencoba membuat *string slice* di tengah-tengah
> karakter multibyte, program Anda akan keluar dengan galat.

Dengan semua informasi ini, mari kita tulis ulang `first_word` agar
mengembalikan sebuah *slice*. Tipe yang menandakan “string slice” ditulis
sebagai `&str`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-18-first-word-slice/src/main.rs:here}}
```

</Listing>

Kita mendapatkan indeks akhir kata dengan cara yang sama seperti pada
Listing 4-7, yaitu dengan mencari kemunculan pertama spasi. Ketika menemukan
spasi, kita mengembalikan *string slice* menggunakan awal *string* dan indeks
spasi sebagai indeks awal dan indeks akhir.

Sekarang ketika kita memanggil `first_word`, kita mendapatkan kembali satu
nilai tunggal yang terikat pada data yang mendasarinya. Nilai itu terdiri
atas sebuah *reference* ke titik awal *slice* dan jumlah elemen dalam
*slice*.

Mengembalikan *slice* juga akan berhasil untuk fungsi `second_word`:

```rust,ignore
fn second_word(s: &String) -> &str {
```

Sekarang kita memiliki API yang lugas dan jauh lebih sulit untuk dikacaukan,
karena *compiler* akan memastikan bahwa *reference* ke dalam `String` tetap
valid. Masih ingat bug pada program di Listing 4-8, ketika kita mendapatkan
indeks akhir kata pertama tetapi lalu mengosongkan *string* sehingga indeks
kita menjadi tidak valid? Kode itu salah secara logika tetapi tidak langsung
menunjukkan galat. Masalahnya baru akan muncul belakangan jika kita terus
mencoba menggunakan indeks kata pertama dengan *string* yang telah
dikosongkan. *Slice* membuat bug ini mustahil terjadi dan memberi tahu kita
jauh lebih cepat bahwa ada masalah pada kode kita. Versi *slice* dari
`first_word` akan melemparkan galat waktu kompilasi:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/src/main.rs:here}}
```

</Listing>

Berikut galat dari *compiler*:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/output.txt}}
```

Ingatlah aturan *borrowing* bahwa jika kita memiliki *immutable reference* ke
sesuatu, kita tidak boleh juga mengambil *mutable reference*. Karena `clear`
perlu memotong `String`, ia perlu mendapatkan *mutable reference*. `println!`
setelah pemanggilan `clear` menggunakan *reference* di dalam `word`, jadi
*immutable reference* itu harus tetap aktif pada titik tersebut. Rust
melarang *mutable reference* di `clear` dan *immutable reference* di `word`
untuk ada pada saat yang sama, dan kompilasi pun gagal. Rust tidak hanya
membuat API kita lebih mudah digunakan, tetapi juga telah menghilangkan
seluruh golongan galat pada saat kompilasi!

<!-- Old headings. Do not remove or links may break. -->

<a id="string-literals-are-slices"></a>

#### String Literal sebagai Slice

Ingat bahwa kita pernah membahas tentang *string literal* yang disimpan di
dalam biner. Sekarang setelah kita mengenal *slice*, kita dapat memahami
*string literal* dengan benar:

```rust
let s = "Hello, world!";
```

Tipe `s` di sini adalah `&str`: ia adalah sebuah *slice* yang menunjuk ke
titik tertentu di dalam biner. Inilah juga mengapa *string literal* bersifat
*immutable*; `&str` adalah *immutable reference*.

#### Slice String sebagai Parameter

Mengetahui bahwa Anda dapat mengambil *slice* dari *literal* maupun nilai
`String` membawa kita pada satu penyempurnaan lagi untuk `first_word`, yaitu
*signature*-nya:

```rust,ignore
fn first_word(s: &String) -> &str {
```

Rustacean yang lebih berpengalaman akan menulis *signature* seperti yang
ditunjukkan pada Listing 4-9, karena ini memungkinkan kita menggunakan fungsi
yang sama untuk nilai `&String` maupun nilai `&str`.

<Listing number="4-9" caption="Menyempurnakan fungsi `first_word` dengan menggunakan string slice sebagai tipe parameter `s`">

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:here}}
```

</Listing>

Jika kita memiliki *string slice*, kita dapat meneruskannya secara langsung.
Jika kita memiliki `String`, kita dapat meneruskan *slice* dari `String`
tersebut atau *reference* ke `String` tersebut. Fleksibilitas ini
memanfaatkan *deref coercion*, sebuah fitur yang akan kita bahas di bagian
[“Menggunakan Deref Coercions di dalam Fungsi dan
Metode”][deref-coercions]<!-- ignore --> pada Bab 15.

Mendefinisikan fungsi yang menerima *string slice* alih-alih *reference* ke
`String` membuat API kita lebih umum dan berguna tanpa kehilangan
fungsionalitas apa pun:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:usage}}
```

</Listing>

### Slice Lainnya

*String slice*, seperti yang dapat Anda bayangkan, khusus untuk *string*.
Tetapi ada juga tipe *slice* yang lebih umum. Perhatikan array ini:

```rust
let a = [1, 2, 3, 4, 5];
```

Sama seperti kita mungkin ingin merujuk ke sebagian dari sebuah *string*,
kita mungkin ingin merujuk ke sebagian dari sebuah array. Caranya seperti
ini:

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

*Slice* ini bertipe `&[i32]`. Cara kerjanya sama dengan *string slice*, yaitu
dengan menyimpan *reference* ke elemen pertama dan sebuah panjang. Anda akan
menggunakan *slice* semacam ini untuk berbagai jenis koleksi lainnya. Kita
akan membahas koleksi-koleksi ini secara mendetail ketika kita membicarakan
vektor di Bab 8.

## Ringkasan

Konsep *ownership*, *borrowing*, dan *slice* menjamin keamanan memori dalam
program Rust pada saat kompilasi. Bahasa Rust memberi Anda kendali atas
penggunaan memori Anda, sama seperti bahasa pemrograman sistem lainnya.
Namun, dengan adanya *owner* data yang membersihkan data itu secara otomatis
ketika *owner*-nya keluar dari *scope*, Anda tidak perlu menulis dan
men-debug kode tambahan untuk mendapatkan kendali ini.

*Ownership* memengaruhi cara kerja banyak bagian lain dari Rust, jadi kita
akan membahas konsep-konsep ini lebih lanjut di sepanjang sisa buku. Mari
kita lanjut ke Bab 5 dan melihat bagaimana mengelompokkan potongan-potongan
data di dalam sebuah `struct`.

[ch13]: ch13-02-iterators.html
[ch6]: ch06-02-match.html#patterns-that-bind-to-values
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[deref-coercions]: ch15-02-deref.html#using-deref-coercions-in-functions-and-methods
