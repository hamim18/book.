<a id="references-and-borrowing"></a>
## References dan Borrowing

Masalah dengan kode *tuple* pada Listing 4-5 adalah kita harus mengembalikan
`String` ke fungsi pemanggil supaya kita masih bisa menggunakan `String`
tersebut setelah pemanggilan `calculate_length`, karena `String` itu telah
dipindahkan ke dalam `calculate_length`. Sebagai gantinya, kita dapat
memberikan sebuah *reference* ke nilai `String` tersebut. *Reference* mirip
dengan *pointer* karena ia adalah sebuah alamat yang dapat kita ikuti untuk
mengakses data yang tersimpan di alamat tersebut; data itu dimiliki oleh
variable lain. Tidak seperti *pointer*, *reference* dijamin menunjuk ke nilai
yang valid dari type tertentu selama *lifetime* *reference* tersebut.

Berikut cara Anda mendefinisikan dan menggunakan fungsi `calculate_length`
yang memiliki sebuah *reference* ke sebuah objek sebagai parameter, alih-alih
mengambil *ownership* dari nilai tersebut:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:all}}
```

</Listing>

Pertama, perhatikan bahwa semua kode *tuple* dalam deklarasi variable dan
return value fungsi sudah tidak ada. Kedua, perhatikan bahwa kita
meneruskan `&s1` ke dalam `calculate_length` dan, pada definisinya, kita
menerima `&String`, bukan `String`. Tanda ampersand ini merepresentasikan
*reference*, dan memungkinkan Anda merujuk ke suatu nilai tanpa mengambil
*ownership*-nya. Gambar 4-6 menggambarkan konsep ini.

<img alt="Tiga tabel: tabel untuk s hanya memuat sebuah pointer ke tabel
untuk s1. Tabel untuk s1 memuat data stack untuk s1 dan menunjuk ke data
string di heap." src="img/trpl04-06.svg" class="center" />

<span class="caption">Gambar 4-6: Diagram `&String` `s` yang menunjuk ke
`String` `s1`</span>

> Catatan: Kebalikan dari membuat *reference* menggunakan `&` adalah
> *dereferencing* (dereferensi), yang dilakukan dengan operator dereferensi,
> `*`. Kita akan melihat beberapa penggunaan operator dereferensi di Bab 8 dan
> membahas detail *dereferencing* di Bab 15.

Mari kita cermati pemanggilan fungsi di sini:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:here}}
```

Sintaks `&s1` memungkinkan kita membuat sebuah *reference* yang _merujuk_ ke
nilai `s1` tetapi tidak memilikinya. Karena *reference* tersebut tidak
memilikinya, nilai yang ditunjuknya tidak akan dibuang ketika *reference* itu
berhenti digunakan.

Demikian pula, *signature* (tanda tangan) fungsi menggunakan `&` untuk
menunjukkan bahwa type parameter `s` adalah sebuah *reference*. Mari kita
tambahkan beberapa anotasi penjelas:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-08-reference-with-annotations/src/main.rs:here}}
```

*Scope* tempat variable `s` berlaku sama dengan *scope* parameter fungsi mana
pun, tetapi nilai yang ditunjuk oleh *reference* tidak dibuang ketika `s`
berhenti digunakan, karena `s` tidak memiliki *ownership*. Ketika fungsi
menerima *reference* sebagai parameter alih-alih nilai sebenarnya, kita tidak
perlu mengembalikan nilai-nilai tersebut untuk menyerahkan kembali
*ownership*, karena sejak awal kita tidak pernah memilikinya.

Kita menyebut tindakan membuat sebuah *reference* sebagai *borrowing*
(peminjaman). Seperti dalam kehidupan nyata, jika seseorang memiliki sesuatu,
Anda dapat meminjamnya dari mereka. Setelah selesai, Anda harus
mengembalikannya. Anda tidak memilikinya.

Jadi, apa yang terjadi jika kita mencoba mengubah sesuatu yang sedang kita
pinjam? Cobalah kode pada Listing 4-6. Peringatan spoiler: kode ini tidak
akan berhasil!

<Listing number="4-6" file-name="src/main.rs" caption="Mencoba mengubah nilai yang dipinjam">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-06/src/main.rs}}
```

</Listing>

Berikut errornya:

```console
{{#include ../listings/ch04-understanding-ownership/listing-04-06/output.txt}}
```

Sama seperti variable yang bersifat *immutable* secara bawaan, *reference*
juga demikian. Kita tidak diizinkan mengubah sesuatu yang kita miliki
*reference*-nya.

### Mutable References

Kita dapat memperbaiki kode dari Listing 4-6 agar kita diizinkan mengubah
nilai yang dipinjam hanya dengan beberapa penyesuaian kecil, yaitu dengan
menggunakan *mutable reference* (*reference* yang *mutable*):

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-09-fixes-listing-04-06/src/main.rs}}
```

</Listing>

Pertama, kita mengubah `s` menjadi `mut`. Lalu, kita membuat *mutable
reference* dengan `&mut s` di tempat kita memanggil fungsi `change`, dan
memperbarui *signature* fungsi agar menerima *mutable reference* dengan
`some_string: &mut String`. Ini memperjelas bahwa fungsi `change` akan
mengubah nilai yang dipinjamnya.

*Mutable reference* memiliki satu pembatasan besar: jika Anda memiliki
*mutable reference* ke sebuah nilai, Anda tidak boleh memiliki *reference*
lain ke nilai tersebut. Kode berikut yang mencoba membuat dua *mutable
reference* ke `s` akan gagal:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/src/main.rs:here}}
```

</Listing>

Berikut errornya:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/output.txt}}
```

Error ini menyatakan bahwa kode ini tidak valid karena kita tidak boleh
meminjam `s` sebagai *mutable* lebih dari sekali pada satu waktu. Pinjaman
*mutable* pertama ada di `r1` dan harus bertahan sampai ia digunakan di dalam
`println!`, tetapi di antara pembuatan *mutable reference* itu dan
penggunaannya, kita mencoba membuat *mutable reference* lain di `r2` yang
meminjam data yang sama seperti `r1`.

Pembatasan yang mencegah beberapa *mutable reference* ke data yang sama pada
waktu yang sama tetap mengizinkan mutasi, tetapi dengan cara yang sangat
terkendali. Ini adalah hal yang sulit bagi Rustaceans baru karena sebagian
besar bahasa mengizinkan Anda mengubah data kapan pun Anda mau. Manfaat dari
pembatasan ini adalah Rust dapat mencegah *data race* pada saat kompilasi.
*Data race* mirip dengan *race condition* dan terjadi ketika tiga perilaku
berikut muncul:

- Dua *pointer* atau lebih mengakses data yang sama pada waktu yang sama.
- Setidaknya satu dari *pointer* tersebut digunakan untuk menulis ke data
  itu.
- Tidak ada mekanisme yang dipakai untuk menyinkronkan akses ke data
  tersebut.

*Data race* menyebabkan *undefined behavior* (*undefined behavior*) dan
bisa sulit didiagnosis serta diperbaiki ketika Anda mencoba melacaknya pada
saat *runtime*; Rust mencegah masalah ini dengan menolak mengompilasi kode
yang memiliki *data race*!

Seperti biasa, kita dapat menggunakan kurung kurawal untuk membuat *scope*
baru, sehingga memungkinkan beberapa *mutable reference*, hanya saja tidak
_bersamaan_:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-11-muts-in-separate-scopes/src/main.rs:here}}
```

Rust memberlakukan aturan serupa untuk penggabungan *mutable reference* dan
*immutable reference*. Kode ini menghasilkan error:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/src/main.rs:here}}
```

Berikut errornya:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/output.txt}}
```

Fiuh! Kita _juga_ tidak boleh memiliki *mutable reference* selagi kita
memiliki *immutable reference* ke nilai yang sama.

Pengguna *immutable reference* tidak menduga nilainya akan tiba-tiba berubah
di bawah mereka! Namun, beberapa *immutable reference* diizinkan karena tidak
ada satu pun orang yang sekadar membaca data yang memiliki kemampuan untuk
memengaruhi pembacaan data oleh orang lain.

Perhatikan bahwa *scope* sebuah *reference* dimulai dari tempat *reference*
itu diperkenalkan dan berlanjut sampai terakhir kali *reference* tersebut
digunakan. Misalnya, kode ini akan terkompilasi karena penggunaan terakhir
dari *immutable reference* ada di dalam `println!`, sebelum *mutable
reference* diperkenalkan:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-13-reference-scope-ends/src/main.rs:here}}
```

*Scope* dari *immutable reference* `r1` dan `r2` berakhir setelah `println!`
tempat keduanya terakhir digunakan, yaitu sebelum *mutable reference* `r3`
dibuat. Kedua *scope* ini tidak saling tumpang tindih, jadi kode ini
diizinkan: *compiler* dapat mengetahui bahwa *reference* tersebut tidak lagi
digunakan pada titik sebelum akhir *scope*.

Meskipun error *borrowing* kadang membuat frustrasi, ingatlah bahwa
*compiler* Rust sedang menunjukkan potensi bug sejak dini (pada saat
kompilasi, bukan pada saat *runtime*) dan menunjukkan dengan tepat di mana
letak masalahnya. Dengan begitu, Anda tidak perlu melacak mengapa data Anda
tidak seperti yang Anda kira.

### Dangling References

Pada bahasa yang memiliki *pointer*, mudah untuk secara keliru membuat
*dangling pointer* (*pointer* *dangling*)—yaitu *pointer* yang merujuk ke
lokasi di dalam memori yang mungkin sudah diberikan kepada pihak lain—dengan
membebaskan sebagian memori sambil tetap menyimpan *pointer* ke memori
tersebut. Sebaliknya, di Rust, *compiler* menjamin bahwa *reference* tidak
akan pernah menjadi *dangling reference*: jika Anda memiliki *reference* ke
suatu data, *compiler* akan memastikan bahwa data tersebut tidak akan keluar
dari *scope* sebelum *reference* ke data itu keluar.

Mari kita coba membuat *dangling reference* untuk melihat bagaimana Rust
mencegahnya dengan error waktu kompilasi:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/src/main.rs}}
```

</Listing>

Berikut errornya:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/output.txt}}
```

Pesan error ini merujuk pada sebuah fitur yang belum kita bahas: *lifetime*
(masa hidup). Kita akan membahas *lifetime* secara mendetail di Bab 10.
Namun, jika Anda mengabaikan bagian-bagian tentang *lifetime*, pesan ini
memang memuat kunci mengapa kode ini bermasalah:

```text
this function's return type contains a borrowed value, but there is no value
for it to be borrowed from
```

Mari kita cermati dengan saksama apa yang terjadi pada setiap tahap kode
`dangle` kita:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-15-dangling-reference-annotated/src/main.rs:here}}
```

</Listing>

Karena `s` dibuat di dalam `dangle`, ketika kode `dangle` selesai, `s` akan
didealokasikan. Namun, kita mencoba mengembalikan sebuah *reference* ke
variable itu. Artinya, *reference* ini akan menunjuk ke `String` yang tidak
valid. Itu tidak bagus! Rust tidak akan mengizinkan kita melakukannya.

Solusinya di sini adalah mengembalikan `String`-nya secara langsung:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-16-no-dangle/src/main.rs:here}}
```

Kode ini bekerja tanpa masalah apa pun. *Ownership* dipindahkan ke luar, dan
tidak ada yang didealokasikan.

### Aturan References

Mari kita rangkum apa yang telah kita bahas tentang *reference*:

- Pada satu waktu tertentu, Anda dapat memiliki _salah satu_: satu
  *mutable reference* _atau_ sejumlah *immutable reference*.
- *Reference* harus selalu valid.

Selanjutnya, kita akan melihat jenis *reference* yang berbeda: *slice*.
