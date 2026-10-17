## Unsafe Rust

Semua kode yang kita bahas sejauh ini memiliki jaminan keamanan memori Rust
yang ditegakkan pada waktu kompilasi. Akan tetapi, Rust memiliki bahasa kedua
yang tersembunyi di dalamnya yang tidak menegakkan jaminan keamanan memori
ini: Bahasa itu disebut *unsafe Rust* dan bekerja persis seperti Rust biasa,
tetapi memberi kita kekuatan super ekstra.

*Unsafe* Rust ada karena, secara kodrat, analisis statis bersifat konservatif.
Ketika kompilator berusaha menentukan apakah suatu kode menegakkan
jaminan-jaminan itu atau tidak, lebih baik ia menolak beberapa program yang
valid daripada menerima beberapa program yang tidak valid. Meskipun kode itu
*mungkin* tidak masalah, jika kompilator Rust tidak memiliki cukup informasi
untuk yakin, ia akan menolak kode itu. Dalam kasus seperti ini, Anda bisa
memakai kode *unsafe* untuk memberi tahu kompilator, “Percayalah, saya tahu apa
yang saya lakukan.” Namun, ingatlah bahwa Anda memakai *unsafe* Rust dengan
risiko ditanggung sendiri: Jika Anda memakai kode *unsafe* secara tidak benar,
masalah bisa terjadi karena ketidakamanan memori, seperti dereferensi *pointer*
null.

Alasan lain mengapa Rust memiliki alter ego yang *unsafe* adalah karena
perangkat keras komputer yang mendasarinya pada dasarnya tidak aman. Jika
Rust tidak mengizinkan Anda melakukan operasi *unsafe*, Anda tidak bisa
mengerjakan tugas-tugas tertentu. Rust perlu mengizinkan Anda melakukan
pemrograman sistem tingkat rendah, seperti berinteraksi langsung dengan
sistem operasi atau bahkan menulis sistem operasi Anda sendiri. Mengerjakan
pemrograman sistem tingkat rendah adalah salah satu tujuan bahasa ini. Mari
kita telusuri apa saja yang bisa kita lakukan dengan *unsafe* Rust dan bagaimana
melakukannya.

<!-- Old headings. Do not remove or links may break. -->

<a id="unsafe-superpowers"></a>

### Menjalankan Unsafe Superpowers

Untuk beralih ke *unsafe* Rust, pakailah kata kunci `unsafe` lalu bukalah blok
baru yang memuat kode *unsafe* itu. Anda bisa melakukan lima tindakan di *unsafe*
Rust yang tidak bisa Anda lakukan di Rust yang aman, yang kita sebut *unsafe
superpowers* (kekuatan super *unsafe*). Kekuatan super itu mencakup kemampuan
untuk:

1. Melakukan dereferensi terhadap sebuah *raw pointer*.
1. Memanggil fungsi atau metode *unsafe*.
1. Mengakses atau mengubah variabel static yang *mutable*.
1. Mengimplementasikan *trait* yang *unsafe*.
1. Mengakses *field* dari `union`.

Penting untuk dipahami bahwa `unsafe` tidak mematikan *borrow checker* atau
menonaktifkan pemeriksaan keamanan Rust lainnya: Jika Anda memakai sebuah
*reference* di dalam kode *unsafe*, *reference* itu tetap akan diperiksa. Kata
kunci `unsafe` hanya memberi Anda akses ke lima fitur ini, yang kemudian tidak
diperiksa oleh kompilator untuk keamanan memori. Anda tetap mendapatkan
keamanan dalam tingkat tertentu di dalam blok *unsafe*.

Selain itu, `unsafe` tidak berarti kode di dalam bloknya pasti berbahaya atau
pasti akan memiliki masalah keamanan memori: Maksudnya adalah, sebagai
pemrogram, Andalah yang akan memastikan bahwa kode di dalam blok `unsafe`
mengakses memori dengan cara yang valid.

Manusia bisa salah dan kesalahan pasti akan terjadi, tetapi dengan
mengharuskan lima operasi *unsafe* ini berada di dalam blok yang ditandai
dengan `unsafe`, Anda akan tahu bahwa error apa pun yang berkaitan dengan
keamanan memori pasti berada di dalam blok `unsafe`. Buatlah blok `unsafe`
sekecil mungkin; Anda akan bersyukur nanti saat menyelidiki bug memori.

Untuk mengisolasi kode *unsafe* sebisa mungkin, sebaiknya kode semacam itu
dibungkus di dalam abstraksi yang aman dan menyediakan API yang aman, yang
akan kita bahas nanti di bab ini saat kita menelaah fungsi dan metode *unsafe*.
Sebagian pustaka standar diimplementasikan sebagai abstraksi yang aman di
atas kode *unsafe* yang telah diaudit. Membungkus kode *unsafe* di dalam
abstraksi yang aman mencegah pemakaian `unsafe` bocor ke semua tempat di mana
Anda atau pengguna Anda mungkin ingin memakai fungsionalitas yang
diimplementasikan dengan kode `unsafe`, karena memakai abstraksi yang aman
itu aman.

Mari kita lihat kelima kekuatan super *unsafe* itu satu per satu. Kita juga
akan melihat beberapa abstraksi yang menyediakan antarmuka yang aman untuk
kode *unsafe*.

### Melakukan Dereferensi pada Raw Pointer

Di Bab 4, pada seksi [“Dangling References”][dangling-references]<!-- ignore
-->, kita menyebutkan bahwa kompilator memastikan *reference* selalu valid.
*Unsafe* Rust memiliki dua tipe baru yang disebut *raw pointer* (*pointer*
mentah) yang mirip dengan *reference*. Seperti halnya *reference*, *raw pointer*
bisa *immutable* (tidak dapat diubah) atau *mutable* (dapat diubah) dan
ditulis sebagai `*const T` dan `*mut T` berturut-turut. Tanda bintang itu
bukan operator dereferensi; ia adalah bagian dari nama tipenya. Dalam konteks
*raw pointer*, *immutable* berarti *pointer* itu tidak bisa langsung diberi nilai
setelah didereferensi.

Berbeda dari *reference* dan *smart pointer*, *raw pointer*:

- Diizinkan untuk mengabaikan aturan *borrowing* dengan memiliki *pointer*
  *immutable* dan *mutable* sekaligus, atau banyak *pointer* *mutable*, ke lokasi
  yang sama
- Tidak dijamin menunjuk ke memori yang valid
- Diizinkan untuk bernilai null
- Tidak mengimplementasikan pembersihan otomatis apa pun

Dengan memilih untuk tidak memakai penegakan jaminan-jaminan ini oleh Rust,
Anda bisa melepaskan keamanan yang terjamin dengan imbalan performa yang
lebih besar atau kemampuan untuk berinteraksi dengan bahasa atau perangkat
keras lain tempat jaminan Rust tidak berlaku.

Listing 20-1 menunjukkan cara membuat *raw pointer* *immutable* dan *mutable*.

<Listing number="20-1" caption="Membuat raw pointer dengan operator borrow mentah">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-01/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa kita tidak menyertakan kata kunci `unsafe` di kode ini.
Kita bisa membuat *raw pointer* di kode yang aman; kita hanya tidak bisa
melakukan dereferensi *raw pointer* di luar blok *unsafe*, seperti yang akan Anda
lihat sebentar lagi.

Kita telah membuat *raw pointer* dengan memakai operator borrow mentah:
`&raw const num` membuat *raw pointer* *immutable* `*const i32`, dan `&raw mut
num` membuat raw pointer mutable `*mut i32`. Karena kita membuatnya langsung
dari sebuah variabel lokal, kita tahu raw pointer khusus ini valid, tetapi
kita tidak bisa membuat asumsi itu terhadap sembarang raw pointer.

Untuk menunjukkan hal ini, berikutnya kita akan membuat sebuah raw pointer
yang validitasnya tidak begitu bisa kita pastikan, dengan memakai kata kunci
`as` untuk melakukan cast pada sebuah nilai alih-alih memakai operator borrow
mentah. Listing 20-2 menunjukkan cara membuat raw pointer ke lokasi memori
yang sembarang. Berusaha memakai memori sembarang adalah perilaku tak
terdefinisi: Mungkin ada data di alamat itu atau mungkin tidak, kompilator
mungkin mengoptimasi kodenya sehingga tidak ada akses memori, atau programnya
mungkin berakhir dengan segmentation fault. Biasanya, tidak ada alasan bagus
untuk menulis kode seperti ini, terutama pada kasus di mana Anda bisa memakai
operator borrow mentah, tetapi itu memang mungkin.

<Listing number="20-2" caption="Membuat raw pointer ke alamat memori sembarang">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-02/src/main.rs:here}}
```

</Listing>

Ingat kembali bahwa kita bisa membuat raw pointer di kode yang aman, tetapi
kita tidak bisa melakukan dereferensi raw pointer dan membaca data yang
ditunjuknya. Di Listing 20-3, kita memakai operator dereferensi `*` pada
sebuah *raw pointer* yang memerlukan blok `unsafe`.

<Listing number="20-3" caption="Melakukan dereferensi raw pointer di dalam blok `unsafe`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-03/src/main.rs:here}}
```

</Listing>

Membuat sebuah *pointer* tidak menimbulkan bahaya; hanya ketika kita berusaha
mengakses nilai yang ditunjuknya, kita mungkin berakhir berurusan dengan
nilai yang tidak valid.

Perhatikan juga bahwa di Listing 20-1 dan 20-3, kita membuat *raw pointer*
`*const i32` dan `*mut i32` yang sama-sama menunjuk ke lokasi memori yang
sama, tempat `num` disimpan. Jika kita justru berusaha membuat *reference*
*immutable* dan *mutable* ke `num`, kode itu tidak akan terkompilasi karena
aturan *ownership* Rust tidak mengizinkan sebuah *reference* *mutable* pada saat
yang sama dengan *reference* *immutable* mana pun. Dengan *raw pointer*, kita bisa
membuat *pointer* *mutable* dan *pointer* *immutable* ke lokasi yang sama dan
mengubah data melalui *pointer* *mutable* itu, yang berpotensi menimbulkan data
race. Berhati-hatilah!

Dengan segala bahaya ini, mengapa Anda perlu memakai *raw pointer*? Salah satu
kasus pemakaian utamanya adalah saat berinteraksi dengan kode C, seperti yang
akan Anda lihat di seksi berikutnya. Kasus lainnya adalah saat membangun
abstraksi yang aman yang tidak dipahami oleh *borrow checker*. Kita akan
memperkenalkan fungsi *unsafe* lalu melihat contoh abstraksi yang aman yang
memakai kode *unsafe*.

### Memanggil Fungsi atau Metode Unsafe

Jenis operasi kedua yang bisa Anda lakukan di dalam blok *unsafe* adalah
memanggil fungsi *unsafe*. Fungsi dan metode *unsafe* tampak persis seperti
fungsi dan metode biasa, tetapi mereka memiliki tambahan `unsafe` sebelum
bagian definisi lainnya. Kata kunci `unsafe` dalam konteks ini menandakan
bahwa fungsi itu memiliki persyaratan yang perlu kita tegakkan saat
memanggilnya, karena Rust tidak bisa menjamin bahwa kita telah memenuhi
persyaratan-persyaratan itu. Dengan memanggil fungsi *unsafe* di dalam blok
`unsafe`, kita menyatakan bahwa kita telah membaca dokumentasi fungsi itu dan
kita bertanggung jawab untuk menegakkan kontrak-kontraknya.

Berikut adalah fungsi *unsafe* bernama `dangerous` yang tidak melakukan apa pun
di tubuhnya:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-01-unsafe-fn/src/main.rs:here}}
```

Kita harus memanggil fungsi `dangerous` di dalam blok `unsafe` yang terpisah.
Jika kita berusaha memanggil `dangerous` tanpa blok `unsafe`, kita akan
mendapat error:

```console
{{#include ../listings/ch20-advanced-features/output-only-01-missing-unsafe/output.txt}}
```

Dengan blok `unsafe`, kita menegaskan kepada Rust bahwa kita telah membaca
dokumentasi fungsi itu, kita memahami cara memakainya dengan benar, dan kita
telah memverifikasi bahwa kita memenuhi kontrak fungsi itu.

Untuk melakukan operasi *unsafe* di tubuh sebuah fungsi `unsafe`, Anda tetap
perlu memakai blok `unsafe`, sama seperti di dalam fungsi biasa, dan
kompilator akan memperingatkan Anda jika Anda lupa. Ini membantu kita
menjaga blok `unsafe` sekecil mungkin, karena operasi *unsafe* mungkin tidak
diperlukan di seluruh tubuh fungsi.

#### Membuat Abstraksi yang Aman di atas Kode Unsafe

Hanya karena sebuah fungsi memuat kode *unsafe* bukan berarti kita perlu
menandai seluruh fungsi itu sebagai *unsafe*. Bahkan, membungkus kode *unsafe* di
dalam fungsi yang aman adalah abstraksi yang umum. Sebagai contoh, mari kita
pelajari fungsi `split_at_mut` dari pustaka standar, yang memerlukan sedikit
kode *unsafe*. Kita akan menelusuri bagaimana kita bisa mengimplementasikannya.
Metode yang aman ini didefinisikan pada *slice* *mutable*: Metode ini mengambil
satu *slice* dan menjadikannya dua dengan membelah *slice* itu pada indeks yang
diberikan sebagai argumen. Listing 20-4 menunjukkan cara memakai
`split_at_mut`.

<Listing number="20-4" caption="Memakai fungsi `split_at_mut` yang aman">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-04/src/main.rs:here}}
```

</Listing>

Kita tidak bisa mengimplementasikan fungsi ini hanya dengan memakai Rust
yang aman. Suatu percobaan mungkin tampak seperti Listing 20-5, yang tidak
akan terkompilasi. Demi kesederhanaan, kita akan mengimplementasikan
`split_at_mut` sebagai fungsi alih-alih metode dan hanya untuk *slice* berisi
nilai `i32` alih-alih untuk tipe generik `T`.

<Listing number="20-5" caption="Percobaan implementasi `split_at_mut` hanya dengan memakai Rust yang aman">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-05/src/main.rs:here}}
```

</Listing>

Fungsi ini pertama-tama mengambil panjang total *slice*. Lalu, fungsi ini
menegaskan bahwa indeks yang diberikan sebagai parameter berada di dalam
*slice* dengan memeriksa apakah indeks itu kurang dari atau sama dengan
panjangnya. Asersi itu berarti jika kita memberikan indeks yang lebih besar
daripada panjangnya untuk membelah *slice*, fungsi itu akan panic sebelum ia
berusaha memakai indeks tersebut.

Kemudian, kita mengembalikan dua *slice* *mutable* di dalam sebuah *tuple*: satu
dari awal *slice* asli sampai indeks `mid`, dan satu lagi dari `mid` sampai
akhir *slice*.

Saat kita berusaha mengompilasi kode di Listing 20-5, kita akan mendapat
error:

```console
{{#include ../listings/ch20-advanced-features/listing-20-05/output.txt}}
```

*Borrow checker* Rust tidak bisa memahami bahwa kita meminjam bagian-bagian
*slice* yang berbeda; ia hanya tahu bahwa kita meminjam dari *slice* yang sama
sebanyak dua kali. Meminjam bagian-bagian *slice* yang berbeda pada dasarnya
tidak masalah karena kedua *slice* itu tidak saling tumpang tindih, tetapi
Rust tidak cukup cerdas untuk mengetahui hal ini. Saat kita tahu kode itu
tidak masalah tetapi Rust tidak mengetahuinya, sudah saatnya memakai kode
*unsafe*.

Listing 20-6 menunjukkan cara memakai blok `unsafe`, sebuah *raw pointer*, dan
beberapa pemanggilan fungsi *unsafe* untuk membuat implementasi `split_at_mut`
bekerja.

<Listing number="20-6" caption="Memakai kode unsafe dalam implementasi fungsi `split_at_mut`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-06/src/main.rs:here}}
```

</Listing>

Ingat kembali dari seksi [“Tipe Slice”][the-slice-type]<!-- ignore --> di Bab
4 bahwa *slice* adalah *pointer* ke sejumlah data beserta panjang *slice* itu. Kita
memakai metode `len` untuk mendapatkan panjang sebuah *slice* dan metode
`as_mut_ptr` untuk mengakses *raw pointer* dari sebuah *slice*. Dalam kasus ini,
karena kita memiliki *slice* *mutable* ke nilai `i32`, `as_mut_ptr` mengembalikan
*raw pointer* dengan tipe `*mut i32`, yang kita simpan di variabel `ptr`.

Kita mempertahankan asersi bahwa indeks `mid` berada di dalam *slice*. Lalu,
kita sampai pada kode *unsafe*-nya: Fungsi `slice::from_raw_parts_mut`
menerima sebuah *raw pointer* dan sebuah panjang, lalu ia membuat sebuah *slice*.
Kita memakai fungsi ini untuk membuat *slice* yang dimulai dari `ptr` dan
panjangnya `mid` item. Kemudian, kita memanggil metode `add` pada `ptr`
dengan `mid` sebagai argumen untuk mendapatkan *raw pointer* yang dimulai di
`mid`, dan kita membuat *slice* dengan memakai *pointer* itu serta sisa jumlah
item setelah `mid` sebagai panjangnya.

Fungsi `slice::from_raw_parts_mut` bersifat *unsafe* karena ia menerima raw
*pointer* dan harus percaya bahwa *pointer* itu valid. Metode `add` pada raw
*pointer* juga *unsafe* karena ia harus percaya bahwa lokasi offsetnya juga
merupakan *pointer* yang valid. Karena itu, kita harus meletakkan blok `unsafe`
di sekeliling pemanggilan kita terhadap `slice::from_raw_parts_mut` dan `add`
supaya kita bisa memanggilnya. Dengan melihat kodenya dan dengan menambahkan
asersi bahwa `mid` harus kurang dari atau sama dengan `len`, kita bisa tahu
bahwa semua *raw pointer* yang dipakai di dalam blok `unsafe` akan menjadi
*pointer* yang valid ke data di dalam *slice*. Ini adalah pemakaian `unsafe` yang
dapat diterima dan tepat.

Perhatikan bahwa kita tidak perlu menandai fungsi `split_at_mut` yang
dihasilkan sebagai `unsafe`, dan kita bisa memanggil fungsi ini dari Rust
yang aman. Kita telah membuat abstraksi yang aman atas kode *unsafe* itu dengan
implementasi fungsi yang memakai kode `unsafe` dengan cara yang aman, karena
ia hanya membuat *pointer*-pointer yang valid dari data yang dapat diakses
fungsi ini.

Sebaliknya, pemakaian `slice::from_raw_parts_mut` di Listing 20-7 kemungkinan
besar akan crash saat *slice* itu dipakai. Kode ini mengambil lokasi memori
sembarang dan membuat *slice* sepanjang 10.000 item.

<Listing number="20-7" caption="Membuat slice dari lokasi memori sembarang">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-07/src/main.rs:here}}
```

</Listing>

Kita tidak memiliki memori di lokasi sembarang ini, dan tidak ada jaminan
bahwa *slice* yang dibuat kode ini berisi nilai `i32` yang valid. Berusaha
memakai `values` seolah-olah ia *slice* yang valid menghasilkan perilaku tak
terdefinisi.

#### Memakai Fungsi `extern` untuk Memanggil Kode Eksternal

Terkadang kode Rust Anda mungkin perlu berinteraksi dengan kode yang ditulis
dalam bahasa lain. Untuk ini, Rust memiliki kata kunci `extern` yang
memfasilitasi pembuatan dan pemakaian *Foreign Function Interface* (FFI,
Antarmuka Fungsi Asing), yaitu cara bagi sebuah bahasa pemrograman untuk
mendefinisikan fungsi dan memungkinkan bahasa pemrograman lain (asing) untuk
memanggil fungsi-fungsi itu.

Listing 20-8 menunjukkan cara menyiapkan integrasi dengan fungsi `abs` dari
pustaka standar C. Fungsi yang dideklarasikan di dalam blok `extern` umumnya
tidak aman untuk dipanggil dari kode Rust, jadi blok `extern` juga harus
ditandai `unsafe`. Alasannya, bahasa lain tidak menegakkan aturan dan jaminan
Rust, dan Rust tidak bisa memeriksanya, sehingga tanggung jawab untuk
memastikan keamanan jatuh pada pemrogram.

<Listing number="20-8" file-name="src/main.rs" caption="Mendeklarasikan dan memanggil fungsi `extern` yang didefinisikan dalam bahasa lain">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Listing>

Di dalam blok `unsafe extern "C"`, kita mendaftarkan nama dan tanda tangan
fungsi-fungsi eksternal dari bahasa lain yang ingin kita panggil. Bagian
`"C"` mendefinisikan *application binary interface* (ABI, antarmuka biner
aplikasi) mana yang dipakai fungsi eksternal itu: ABI mendefinisikan cara
memanggil fungsi itu pada tingkat assembly. ABI `"C"` adalah yang paling
umum dan mengikuti ABI bahasa pemrograman C. Informasi tentang semua ABI
yang didukung Rust tersedia di [Rust *Reference*][ABI].

Setiap item yang dideklarasikan di dalam blok `unsafe extern` secara implisit
bersifat *unsafe*. Akan tetapi, beberapa fungsi FFI *memang* aman untuk
dipanggil. Misalnya, fungsi `abs` dari pustaka standar C tidak memiliki
pertimbangan keamanan memori apa pun, dan kita tahu ia bisa dipanggil dengan
`i32` apa pun. Dalam kasus seperti ini, kita bisa memakai kata kunci `safe`
untuk menyatakan bahwa fungsi khusus ini aman untuk dipanggil meskipun ia
berada di dalam blok `unsafe extern`. Setelah kita membuat perubahan itu,
memanggilnya tidak lagi memerlukan blok `unsafe`, seperti yang ditunjukkan di
Listing 20-9.

<Listing number="20-9" file-name="src/main.rs" caption="Menandai fungsi secara eksplisit sebagai `safe` di dalam blok `unsafe extern` dan memanggilnya dengan aman">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Listing>

Menandai sebuah fungsi sebagai `safe` tidak serta-merta membuatnya aman!
Sebaliknya, itu seperti janji yang Anda buat kepada Rust bahwa fungsi itu
aman. Tanggung jawab untuk memastikan janji itu ditepati tetap ada pada
Anda!

#### Memanggil Fungsi Rust dari Bahasa Lain

Kita juga bisa memakai `extern` untuk membuat antarmuka yang memungkinkan
bahasa lain memanggil fungsi Rust. Alih-alih membuat satu blok `extern` utuh,
kita menambahkan kata kunci `extern` dan menentukan ABI yang akan dipakai
tepat sebelum kata kunci `fn` untuk fungsi yang bersangkutan. Kita juga perlu
menambahkan anotasi `#[unsafe(no_mangle)]` untuk memberi tahu kompilator Rust
agar tidak melakukan mangling pada nama fungsi ini. *Mangling* adalah ketika
sebuah kompilator mengubah nama yang kita berikan kepada sebuah fungsi
menjadi nama lain yang memuat lebih banyak informasi untuk dipakai bagian
lain proses kompilasi, tetapi kurang mudah dibaca manusia. Setiap kompilator
bahasa pemrograman melakukan mangling pada nama dengan cara yang sedikit
berbeda, jadi agar fungsi Rust bisa diberi nama oleh bahasa lain, kita harus
menonaktifkan name mangling milik kompilator Rust. Ini *unsafe* karena mungkin
ada bentrokan nama antarlibrary tanpa adanya mangling bawaan itu, jadi
menjadi tanggung jawab kita untuk memastikan nama yang kita pilih aman untuk
diekspor tanpa mangling.

Pada contoh berikut, kita membuat fungsi `call_from_c` dapat diakses dari
kode C, setelah ia dikompilasi menjadi library bersama dan di-link dari C:

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

Pemakaian `extern` ini memerlukan `unsafe` hanya pada atributnya, bukan pada
blok `extern`.

### Mengakses atau Mengubah Variabel Static yang Mutable

Di buku ini, kita belum membicarakan variabel global, yang memang didukung
Rust tetapi bisa bermasalah dengan aturan *ownership* Rust. Jika dua thread
mengakses variabel global *mutable* yang sama, itu bisa menimbulkan data race.

Di Rust, variabel global disebut variabel *static*. Listing 20-10 menunjukkan
contoh deklarasi dan pemakaian variabel static dengan string *slice* sebagai
nilainya.

<Listing number="20-10" file-name="src/main.rs" caption="Mendefinisikan dan memakai variabel static yang immutable">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-10/src/main.rs}}
```

</Listing>

Variabel static mirip dengan konstanta, yang kita bahas di seksi
[“Mendeklarasikan Konstanta”][constants]<!-- ignore --> di Bab 3. Nama
variabel static memakai `SCREAMING_SNAKE_CASE` berdasarkan konvensi. Variabel
static hanya bisa menyimpan *reference* dengan *lifetime* `'static`, yang berarti
kompilator Rust bisa menentukan *lifetime*-nya dan kita tidak diharuskan
menganotasinya secara eksplisit. Mengakses variabel static yang *immutable* itu
aman.

Perbedaan halus antara konstanta dan variabel static yang *immutable* adalah
bahwa nilai dalam variabel static memiliki alamat yang tetap di memori.
Memakai nilainya akan selalu mengakses data yang sama. Sebaliknya, konstanta
diizinkan untuk menduplikasi datanya setiap kali ia dipakai. Perbedaan
lainnya adalah variabel static bisa dibuat *mutable*. Mengakses dan mengubah
variabel static yang *mutable* itu *unsafe*. Listing 20-11 menunjukkan cara
mendeklarasikan, mengakses, dan mengubah variabel static *mutable* bernama
`COUNTER`.

<Listing number="20-11" file-name="src/main.rs" caption="Membaca atau menulis variabel static yang mutable itu unsafe.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-11/src/main.rs}}
```

</Listing>

Sama seperti variabel biasa, kita menentukan mutabilitas dengan memakai kata
kunci `mut`. Kode apa pun yang membaca atau menulis `COUNTER` harus berada di
dalam blok `unsafe`. Kode di Listing 20-11 terkompilasi dan mencetak
`COUNTER: 3` seperti yang kita harapkan karena kode ini single-threaded.
Memiliki banyak thread yang mengakses `COUNTER` kemungkinan besar akan
menghasilkan data race, sehingga itu adalah perilaku tak terdefinisi. Karena
itu, kita perlu menandai seluruh fungsi sebagai `unsafe` dan mendokumentasikan
batasan keamanannya supaya siapa pun yang memanggil fungsi itu tahu apa yang
boleh dan tidak boleh mereka lakukan dengan aman.

Kapan pun kita menulis fungsi *unsafe*, sudah menjadi kebiasaan idiomatis untuk
menulis komentar yang diawali dengan `SAFETY` dan menjelaskan apa yang perlu
dilakukan pemanggil agar bisa memanggil fungsi itu dengan aman. Demikian
pula, kapan pun kita melakukan operasi *unsafe*, sudah menjadi kebiasaan
idiomatis untuk menulis komentar yang diawali dengan `SAFETY` untuk
menjelaskan bagaimana aturan keamanannya ditegakkan.

Selain itu, secara bawaan kompilator akan menolak percobaan apa pun untuk
membuat *reference* ke variabel static yang *mutable* melalui sebuah lint
kompilator. Anda harus memilih untuk tidak memakai perlindungan lint itu
secara eksplisit dengan menambahkan anotasi `#[allow(static_mut_refs)]`,
atau mengakses variabel static *mutable* itu melalui *raw pointer* yang dibuat
dengan salah satu operator borrow mentah. Itu termasuk kasus ketika *reference*
dibuat secara tak terlihat, seperti saat ia dipakai di dalam `println!` pada
listing kode ini. Mengharuskan *reference* ke variabel static *mutable* dibuat
melalui *raw pointer* membantu membuat persyaratan keamanan untuk memakainya
lebih jelas.

Dengan data *mutable* yang dapat diakses secara global, sulit untuk memastikan
tidak ada data race, dan itulah sebabnya Rust menganggap variabel static yang
*mutable* sebagai *unsafe*. Jika memungkinkan, lebih baik memakai teknik
konkurensi dan *smart pointer* yang thread-safe yang kita bahas di Bab 16,
supaya kompilator memeriksa bahwa akses data dari thread yang berbeda
dilakukan dengan aman.

### Mengimplementasikan Trait yang Unsafe

Kita bisa memakai `unsafe` untuk mengimplementasikan *trait* yang *unsafe*.
Sebuah *trait* bersifat *unsafe* ketika setidaknya satu dari metodenya memiliki
suatu invarian yang tidak bisa diverifikasi oleh kompilator. Kita
mendeklarasikan bahwa sebuah *trait* adalah `unsafe` dengan menambahkan kata
kunci `unsafe` sebelum `trait` dan menandai implementasi *trait* itu sebagai
`unsafe` juga, seperti yang ditunjukkan di Listing 20-12.

<Listing number="20-12" caption="Mendefinisikan dan mengimplementasikan trait yang unsafe">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-12/src/main.rs:here}}
```

</Listing>

Dengan memakai `unsafe impl`, kita berjanji bahwa kita akan menegakkan
invarian-invarian yang tidak bisa diverifikasi kompilator.

Sebagai contoh, ingat kembali *marker trait* `Send` dan `Sync` yang kita bahas
di seksi [“Konkurensi yang Dapat Diperluas dengan `Send` dan `Sync`”][send-and-sync]<!-- ignore
--> di Bab 16: Kompilator mengimplementasikan *trait*-trait ini secara otomatis
jika tipe-tipe kita seluruhnya tersusun dari tipe-tipe lain yang
mengimplementasikan `Send` dan `Sync`. Jika kita mengimplementasikan sebuah
tipe yang memuat tipe yang tidak mengimplementasikan `Send` atau `Sync`,
seperti *raw pointer*, dan kita ingin menandai tipe itu sebagai `Send` atau
`Sync`, kita harus memakai `unsafe`. Rust tidak bisa memverifikasi bahwa tipe
kita menegakkan jaminan bahwa ia bisa dikirim lintas thread atau diakses dari
banyak thread dengan aman; karena itu, kita perlu melakukan
pemeriksaan-pemeriksaan itu secara manual dan menandainya dengan `unsafe`.

### Mengakses Field dari Union

Tindakan terakhir yang hanya bekerja dengan `unsafe` adalah mengakses *field*
dari sebuah *union*. *Union* mirip dengan `struct`, tetapi hanya satu *field*
yang dideklarasikan yang dipakai pada instance tertentu dalam satu waktu.
*Union* terutama dipakai untuk berinteraksi dengan *union* di kode C. Mengakses
*field* *union* itu *unsafe* karena Rust tidak bisa menjamin tipe data yang sedang
disimpan di dalam instance *union* itu. Anda bisa mempelajari lebih lanjut
tentang *union* di [Rust *Reference*][unions].

### Memakai Miri untuk Memeriksa Kode Unsafe

Saat menulis kode *unsafe*, Anda mungkin ingin memeriksa bahwa apa yang Anda
tulis benar-benar aman dan tepat. Salah satu cara terbaik untuk melakukannya
adalah memakai Miri, alat resmi Rust untuk mendeteksi perilaku tak
terdefinisi. Sementara *borrow checker* adalah alat *statis* yang bekerja pada
waktu kompilasi, Miri adalah alat *dinamis* yang bekerja pada runtime. Miri
memeriksa kode Anda dengan menjalankan program Anda, atau test suite-nya, dan
mendeteksi saat Anda melanggar aturan-aturan yang dipahaminya tentang cara
Rust seharusnya bekerja.

Memakai Miri memerlukan build nightly dari Rust (yang akan kita bahas lebih
lanjut di [Lampiran G: Bagaimana Rust Dibuat dan “Nightly Rust”][nightly]<!-- ignore -->).
Anda bisa memasang versi nightly dari Rust sekaligus alat Miri dengan
mengetik `rustup +nightly component add miri`. Ini tidak mengubah versi Rust
yang dipakai proyek Anda; ini hanya menambahkan alat itu ke sistem Anda
supaya bisa Anda pakai kapan pun Anda mau. Anda bisa menjalankan Miri pada
sebuah proyek dengan mengetik `cargo +nightly miri run` atau `cargo +nightly
miri test`.

Sebagai contoh betapa bermanfaatnya ini, perhatikan apa yang terjadi saat
kita menjalankannya terhadap Listing 20-7.

```console
{{#include ../listings/ch20-advanced-features/listing-20-07/output.txt}}
```

Miri memperingatkan kita dengan benar bahwa kita melakukan cast pada sebuah
integer menjadi *pointer*, yang mungkin bermasalah, tetapi Miri tidak bisa
menentukan apakah masalah itu benar ada karena ia tidak tahu bagaimana
*pointer* itu berasal. Lalu, Miri mengembalikan error di bagian Listing 20-7
yang memiliki perilaku tak terdefinisi karena kita memiliki *pointer*
menggantung. Berkat Miri, sekarang kita tahu ada risiko perilaku tak
terdefinisi, dan kita bisa memikirkan cara membuat kodenya aman. Dalam
beberapa kasus, Miri bahkan bisa memberikan rekomendasi tentang cara
memperbaiki error.

Miri tidak menangkap semua hal yang mungkin Anda lakukan salah saat menulis
kode *unsafe*. Miri adalah alat analisis dinamis, jadi ia hanya menangkap
masalah pada kode yang benar-benar dijalankan. Itu berarti Anda perlu
memakainya bersamaan dengan teknik pengujian yang baik untuk meningkatkan
keyakinan Anda terhadap kode *unsafe* yang telah Anda tulis. Miri juga tidak
mencakup semua kemungkinan cara kode Anda menjadi tidak sound.

Dengan kata lain: Jika Miri *memang* menangkap suatu masalah, Anda tahu ada
bug, tetapi hanya karena Miri *tidak* menangkap sebuah bug bukan berarti
tidak ada masalah. Meskipun begitu, ia bisa menangkap banyak hal. Cobalah
menjalankannya pada contoh-contoh kode *unsafe* lain di bab ini dan lihat apa
yang dikatakannya!

Anda bisa mempelajari lebih lanjut tentang Miri di [repositori
GitHub-nya][miri].

<!-- Old headings. Do not remove or links may break. -->

<a id="when-to-use-unsafe-code"></a>

### Memakai Kode Unsafe dengan Benar

Memakai `unsafe` untuk memakai salah satu dari lima kekuatan super yang baru
saja dibahas tidaklah salah, bahkan tidak dipandang buruk, tetapi membuat
kode `unsafe` menjadi benar itu lebih sulit karena kompilator tidak bisa
membantu menegakkan keamanan memori. Ketika Anda memiliki alasan untuk
memakai kode `unsafe`, Anda boleh melakukannya, dan adanya anotasi `unsafe`
yang eksplisit membuat sumber masalah lebih mudah dilacak saat masalah itu
terjadi. Kapan pun Anda menulis kode *unsafe*, Anda bisa memakai Miri untuk
membantu Anda lebih yakin bahwa kode yang Anda tulis menegakkan aturan-aturan
Rust.

Untuk penjelajahan yang jauh lebih mendalam tentang cara bekerja secara
efektif dengan *unsafe* Rust, bacalah panduan resmi Rust untuk `unsafe`,
[The Rustonomicon][nomicon].

[dangling-references]: ch04-02-references-and-borrowing.html#dangling-references
[ABI]: ../reference/items/external-blocks.html#abi
[constants]: ch03-01-variables-and-mutability.html#declaring-constants
[send-and-sync]: ch16-04-extensible-concurrency-sync-and-send.html
[the-slice-type]: ch04-03-slices.html#the-slice-type
[unions]: ../reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: appendix-05-editions.html
[nightly]: appendix-07-nightly-rust.html
[nomicon]: https://doc.rust-lang.org/nomicon/
