## Apa Itu Ownership?

*Ownership* adalah seperangkat aturan yang mengatur cara program Rust
mengelola memori. Semua program harus mengelola cara mereka menggunakan
memori komputer selama berjalan. Sebagian bahasa memiliki *garbage collection*
(pengumpulan sampah) yang secara berkala mencari memori yang tidak lagi
dipakai selama program berjalan; pada bahasa lain, pemrogram harus secara
eksplisit mengalokasikan dan membebaskan memori. Rust memakai pendekatan
ketiga: memori dikelola melalui sistem *ownership* dengan seperangkat aturan
yang diperiksa oleh *compiler* (kompilator). Jika salah satu aturan
dilanggar, program tidak akan terkompilasi. Tidak satu pun fitur *ownership*
akan memperlambat program Anda selama program itu berjalan.

Karena *ownership* adalah konsep baru bagi banyak pemrogram, memang perlu
waktu untuk membiasakan diri. Kabar baiknya, semakin berpengalaman Anda
dengan Rust dan aturan-aturan sistem *ownership*, semakin mudah bagi Anda
untuk secara alami mengembangkan kode yang aman dan efisien. Teruslah
berlatih!

Ketika Anda memahami *ownership*, Anda akan memiliki fondasi yang kokoh untuk
memahami fitur-fitur yang membuat Rust unik. Dalam bab ini, Anda akan
mempelajari *ownership* dengan menelusuri beberapa contoh yang berfokus pada
satu struktur data yang sangat umum: string.

<a id="the-stack-and-the-heap"></a>
> ### Stack dan Heap
>
> Banyak bahasa pemrograman tidak mengharuskan Anda untuk terlalu sering
> memikirkan *stack* (tumpukan) dan *heap* (timbunan). Namun, dalam bahasa
> pemrograman sistem seperti Rust, apakah sebuah nilai berada di *stack* atau
> di *heap* memengaruhi perilaku bahasa tersebut dan alasan Anda harus
> membuat keputusan tertentu. Bagian-bagian *ownership* akan dijelaskan dalam
> kaitannya dengan *stack* dan *heap* nanti di bab ini, jadi berikut
> penjelasan singkatnya sebagai persiapan.
>
> *Stack* maupun *heap* adalah bagian dari memori yang tersedia untuk
> digunakan kode Anda pada saat *runtime*, tetapi keduanya terstruktur dengan
> cara yang berbeda. *Stack* menyimpan nilai sesuai urutan masuknya dan
> menghapus nilai dalam urutan sebaliknya. Ini disebut *last in, first out*
> (LIFO, yang terakhir masuk adalah yang pertama keluar). Bayangkan tumpukan
> piring: ketika Anda menambah piring, Anda meletakkannya di atas tumpukan,
> dan ketika Anda membutuhkan piring, Anda mengambil yang paling atas.
> Menambah atau mengambil piring dari tengah atau bawah tumpukan tidak akan
> berjalan sebaik itu! Menambah data disebut *pushing onto the stack*
> (mendorong ke *stack*), dan menghapus data disebut *popping off the stack*
> (mengambil dari *stack*). Semua data yang tersimpan di *stack* harus
> memiliki ukuran yang pasti dan tetap. Data yang ukurannya tidak diketahui
> pada saat kompilasi atau yang ukurannya dapat berubah harus disimpan di
> *heap*.
>
> *Heap* tidak seteratur itu: ketika Anda meletakkan data di *heap*, Anda
> meminta sejumlah ruang tertentu. *Memory allocator* (pengalokasi memori)
> mencari tempat kosong di *heap* yang cukup besar, menandainya sebagai
> sedang digunakan, lalu mengembalikan sebuah *pointer* (penunjuk), yaitu
> alamat dari lokasi tersebut. Proses ini disebut *allocating on the heap*
> (mengalokasikan di *heap*) dan kadang disingkat menjadi *allocating* saja
> (mendorong nilai ke *stack* tidak dianggap sebagai *allocating*). Karena
> *pointer* ke *heap* memiliki ukuran yang pasti dan tetap, Anda dapat
> menyimpan *pointer* tersebut di *stack*, tetapi ketika Anda menginginkan
> data yang sebenarnya, Anda harus mengikuti *pointer* tersebut. Bayangkan
> ketika Anda dicarikan tempat duduk di sebuah restoran. Saat masuk, Anda
> menyebutkan jumlah orang dalam rombongan Anda, lalu pelayan menemukan meja
> kosong yang cukup untuk semua orang dan mengantar Anda ke sana. Jika ada
> anggota rombongan yang datang terlambat, mereka dapat menanyakan di mana
> Anda duduk untuk menemukan Anda.
>
> Mendorong data ke *stack* lebih cepat daripada mengalokasikan di *heap*
> karena *allocator* tidak perlu mencari tempat untuk menyimpan data baru;
> lokasinya selalu berada di puncak *stack*. Sebagai perbandingan,
> mengalokasikan ruang di *heap* membutuhkan lebih banyak kerja karena
> *allocator* harus lebih dulu menemukan ruang yang cukup besar untuk
> menampung data, lalu melakukan pembukuan untuk menyiapkan alokasi
> berikutnya.
>
> Mengakses data di *heap* umumnya lebih lambat daripada mengakses data di
> *stack* karena Anda harus mengikuti *pointer* untuk sampai ke sana.
> Prosesor masa kini bekerja lebih cepat jika lebih sedikit melompat-lompat
> di dalam memori. Melanjutkan analogi tadi, bayangkan seorang pelayan di
> restoran yang menerima pesanan dari banyak meja. Cara yang paling efisien
> adalah mengambil semua pesanan di satu meja sebelum pindah ke meja
> berikutnya. Mengambil pesanan dari meja A, lalu pesanan dari meja B, lalu
> dari A lagi, kemudian dari B lagi, akan menjadi proses yang jauh lebih
> lambat. Dengan alasan yang sama, prosesor biasanya dapat bekerja lebih baik
> jika mengolah data yang berdekatan dengan data lain (seperti di *stack*)
> daripada data yang berjauhan (seperti yang mungkin terjadi di *heap*).
>
> Ketika kode Anda memanggil sebuah fungsi, nilai-nilai yang diteruskan ke
> fungsi tersebut (termasuk, mungkin, *pointer* ke data di *heap*) dan
> variable-variable lokal fungsi itu didorong ke *stack*. Ketika fungsi
> selesai, nilai-nilai tersebut dikeluarkan dari *stack*.
>
> Melacak bagian kode mana yang menggunakan data apa di *heap*, meminimalkan
> jumlah data duplikat di *heap*, dan membersihkan data yang tidak terpakai
> di *heap* supaya Anda tidak kehabisan ruang, semuanya adalah masalah yang
> ditangani oleh *ownership*. Begitu Anda memahami *ownership*, Anda tidak
> akan perlu memikirkan *stack* dan *heap* terlalu sering. Namun, mengetahui
> bahwa tujuan utama *ownership* adalah mengelola data di *heap* dapat
> membantu menjelaskan mengapa *ownership* bekerja seperti itu.

### Aturan Ownership

Pertama, mari kita lihat aturan-aturan *ownership*. Ingatlah aturan-aturan
ini saat kita menelusuri contoh-contoh yang mengilustrasikannya:

- Setiap nilai di Rust memiliki sebuah *owner* (pemilik).
- Hanya boleh ada satu *owner* pada satu waktu.
- Ketika *owner* keluar dari *scope* (cakupan), nilai tersebut akan dibuang.

### Scope Variable

Karena kita sudah melewati sintaks dasar Rust, kita tidak akan menyertakan
semua kode `fn main() {` dalam contoh-contohnya. Jadi, jika Anda mengikuti
buku ini, pastikan untuk meletakkan contoh-contoh berikutnya di dalam sebuah
fungsi `main` secara manual. Hasilnya, contoh-contoh kita akan sedikit lebih
ringkas, sehingga kita bisa berfokus pada detail yang sebenarnya, bukan pada
kode boilerplate.

Sebagai contoh pertama dari *ownership*, kita akan melihat *scope* dari
beberapa variable. *Scope* adalah rentang di dalam program tempat sebuah item
berlaku. Perhatikan variable berikut:

```rust
let s = "hello";
```

Variable `s` merujuk pada sebuah *string literal*, yaitu nilai *string* yang
ditulis langsung ke dalam teks program kita. Variable ini berlaku mulai dari
titik ketika ia dideklarasikan sampai akhir *scope* saat ini. Listing 4-1
menampilkan sebuah program dengan komentar yang memberi keterangan di bagian
mana variable `s` berlaku.

<Listing number="4-1" caption="Sebuah variable dan scope tempat ia berlaku">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-01/src/main.rs:here}}
```

</Listing>

Dengan kata lain, ada dua titik waktu penting di sini:

- Ketika `s` masuk _ke dalam_ *scope*, ia berlaku.
- Ia tetap berlaku sampai keluar _dari_ *scope*.

Sejauh ini, hubungan antara *scope* dan masa berlaku variable mirip dengan
bahasa pemrograman lain. Sekarang kita akan membangun pemahaman ini dengan
memperkenalkan type `String`.

### Type `String`

Untuk mengilustrasikan aturan-aturan *ownership*, kita membutuhkan data type
yang lebih kompleks daripada type yang kita bahas di bagian [“Type
Data”][data-types]<!-- ignore --> pada Bab 3. Type-type yang telah dibahas
sebelumnya memiliki ukuran yang diketahui, dapat disimpan di *stack* dan
dikeluarkan dari *stack* ketika *scope*-nya berakhir, serta dapat disalin
dengan cepat dan sepele untuk membuat instans baru yang mandiri jika bagian
kode lain perlu menggunakan nilai yang sama di *scope* yang berbeda. Namun,
kita ingin melihat data yang disimpan di *heap* dan mengeksplorasi bagaimana
Rust mengetahui kapan harus membersihkan data tersebut, dan type `String`
adalah contoh yang bagus.

Kita akan berkonsentrasi pada bagian-bagian `String` yang berkaitan dengan
*ownership*. Aspek-aspek ini juga berlaku untuk data type kompleks lainnya,
baik yang disediakan oleh *standard library* (pustaka standar) maupun yang
Anda buat sendiri. Kita akan membahas aspek-aspek `String` yang tidak
berkaitan dengan *ownership* di [Bab 8][ch8]<!-- ignore -->.

Kita sudah pernah melihat *string literal*, yaitu nilai *string* yang ditulis
langsung di dalam program kita. *String literal* praktis, tetapi tidak cocok
untuk setiap situasi ketika kita ingin menggunakan teks. Salah satu alasannya
adalah *string literal* bersifat *immutable* (tidak dapat diubah). Alasan
lainnya, tidak semua nilai *string* dapat diketahui ketika kita menulis kode:
contohnya, bagaimana jika kita ingin mengambil input dari pengguna dan
menyimpannya? Untuk situasi-situasi seperti inilah Rust memiliki type
`String`. Type ini mengelola data yang dialokasikan di *heap* sehingga mampu
menyimpan sejumlah teks yang ukurannya belum kita ketahui pada saat
kompilasi. Anda dapat membuat `String` dari sebuah *string literal* dengan
menggunakan fungsi `from`, seperti berikut:

```rust
let s = String::from("hello");
```

Operator titik dua ganda `::` memungkinkan kita menaruh fungsi `from` khusus
ini ke dalam *namespace* (ruang nama) dari type `String`, alih-alih
menggunakan semacam nama seperti `string_from`. Kita akan membahas sintaks
ini lebih lanjut di bagian [“Metode”][methods]<!-- ignore --> pada Bab 5,
serta ketika kita membicarakan ruang nama dengan *module* (modul) di bagian
[“*Path* untuk Merujuk Item di dalam Pohon
Modul”][*paths*-module-tree]<!-- ignore --> pada Bab 7.

String jenis ini _dapat_ diubah:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-01-can-mutate-string/src/main.rs:here}}
```

Jadi, apa bedanya di sini? Mengapa `String` bisa diubah sementara *string
literal* tidak bisa? Perbedaannya terletak pada cara kedua type ini
memperlakukan memori.

### Memori dan Alokasi

Dalam kasus *string literal*, kita sudah mengetahui isinya pada saat
kompilasi, sehingga teksnya ditulis langsung ke dalam berkas eksekutabel
akhir. Inilah mengapa *string literal* cepat dan efisien. Namun, sifat-sifat
ini hanya muncul karena *string literal* bersifat *immutable*. Sayangnya,
kita tidak bisa memasukkan seonggok memori ke dalam biner untuk setiap
potongan teks yang ukurannya tidak diketahui pada saat kompilasi dan yang
ukurannya mungkin berubah selama program berjalan.

Dengan type `String`, untuk mendukung potongan teks yang *mutable* (dapat
diubah) dan dapat bertumbuh, kita perlu mengalokasikan sejumlah memori di
*heap* — yang jumlahnya tidak diketahui pada saat kompilasi — untuk menampung
isinya. Artinya:

- Memori tersebut harus diminta dari *memory allocator* pada saat *runtime*.
- Kita memerlukan cara untuk mengembalikan memori ini kepada *allocator*
  setelah selesai menggunakan `String` kita.

Bagian pertama dilakukan oleh kita: ketika kita memanggil `String::from`,
implementasinya meminta memori yang dibutuhkannya. Hal ini berlaku hampir di
semua bahasa pemrograman.

Namun, bagian kedua berbeda. Pada bahasa yang memiliki *garbage collector*
(GC), GC melacak dan membersihkan memori yang tidak lagi digunakan, dan kita
tidak perlu memikirkannya. Pada sebagian besar bahasa tanpa GC, kita
bertanggung jawab untuk mengenali kapan memori tidak lagi digunakan dan
memanggil kode untuk membebaskannya secara eksplisit, sama seperti saat kita
memintanya. Melakukan hal ini dengan benar secara historis merupakan masalah
pemrograman yang sulit. Jika kita lupa, kita akan membuang-buang memori. Jika
kita melakukannya terlalu dini, kita akan mendapatkan variable yang tidak
valid. Jika kita melakukannya dua kali, itu juga sebuah bug. Kita harus
memasangkan tepat satu `allocate` dengan tepat satu `free`.

Rust mengambil jalan yang berbeda: memori dikembalikan secara otomatis
begitu variable yang memilikinya keluar dari *scope*. Berikut versi contoh
*scope* dari Listing 4-1 dengan menggunakan `String`, bukan *string literal*:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-02-string-scope/src/main.rs:here}}
```

Ada satu titik yang alami di mana kita dapat mengembalikan memori yang
dibutuhkan `String` kita kepada *allocator*: ketika `s` keluar dari *scope*.
Ketika sebuah variable keluar dari *scope*, Rust memanggil sebuah fungsi
khusus untuk kita. Fungsi ini bernama `drop`, dan di sinilah penulis `String`
dapat meletakkan kode untuk mengembalikan memorinya. Rust memanggil `drop`
secara otomatis pada kurung kurawal penutup.

> Catatan: Di C++, pola pembebasan sumber daya pada akhir *lifetime* (masa
> hidup) suatu item ini kadang disebut *Resource Acquisition Is
> Initialization* (RAII). Fungsi `drop` di Rust akan terasa familier bagi Anda
> jika pernah menggunakan pola RAII.

Pola ini berdampak besar pada cara penulisan kode Rust. Saat ini pola ini
mungkin tampak sederhana, tetapi perilaku kode bisa jadi tidak terduga dalam
situasi yang lebih rumit, yaitu ketika kita ingin beberapa variable
menggunakan data yang telah kita alokasikan di *heap*. Mari kita telusuri
beberapa situasi tersebut sekarang.

<!-- Old headings. Do not remove or links may break. -->

<a id="ways-variables-and-data-interact-move"></a>

<a id="variables-and-data-interacting-with-move"></a>
#### Variable dan Data yang Berinteraksi dengan Move

Beberapa variable dapat berinteraksi dengan data yang sama dengan berbagai
cara di Rust. Listing 4-2 menampilkan contoh yang menggunakan sebuah bilangan
bulat.

<Listing number="4-2" caption="Menetapkan nilai bilangan bulat dari variable `x` ke `y`">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-02/src/main.rs:here}}
```

</Listing>

Kita mungkin bisa menebak apa yang dilakukan kode ini: “ikat nilai `5` ke
`x`; lalu buat salinan nilai di `x` dan ikat ke `y`.” Sekarang kita punya dua
variable, `x` dan `y`, dan keduanya bernilai `5`. Inilah yang memang terjadi,
karena bilangan bulat adalah nilai sederhana dengan ukuran yang pasti dan
tetap, dan kedua nilai `5` ini didorong ke *stack*.

Sekarang mari kita lihat versi `String`-nya:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-03-string-move/src/main.rs:here}}
```

Kode ini tampak sangat mirip, sehingga kita mungkin mengira cara kerjanya
akan sama: yaitu, baris kedua akan membuat salinan dari nilai di `s1` dan
mengikatnya ke `s2`. Namun, bukan itu yang terjadi.

Lihatlah Gambar 4-1 untuk mengetahui apa yang terjadi pada `String` di balik
layar. Sebuah `String` terdiri atas tiga bagian, seperti yang ditunjukkan di
sebelah kiri: sebuah *pointer* ke memori yang menampung isi *string*, sebuah
panjang (*length*), dan sebuah kapasitas (*capacity*). Kumpulan data ini
disimpan di *stack*. Di sebelah kanan adalah memori di *heap* yang menampung
isinya.

<img alt="Dua tabel: tabel pertama memuat representasi dari s1 di stack, yang
terdiri atas panjangnya (5), kapasitasnya (5), dan sebuah pointer yang menunjuk
ke nilai pertama pada tabel kedua. Tabel kedua memuat representasi data string
di heap, byte demi byte." src="img/trpl04-01.svg" class="center"
style="width: 50%;" />

<span class="caption">Gambar 4-1: Representasi di dalam memori dari sebuah
`String` yang memuat nilai `"hello"` dan terikat ke `s1`</span>

Panjang adalah seberapa banyak memori, dalam satuan *byte*, yang sedang
digunakan oleh isi `String` tersebut. Kapasitas adalah jumlah total memori,
dalam satuan *byte*, yang telah diterima `String` tersebut dari *allocator*.
Perbedaan antara panjang dan kapasitas itu penting, tetapi tidak dalam
konteks ini, jadi untuk sekarang tidak apa-apa mengabaikan kapasitas.

Ketika kita menetapkan `s1` ke `s2`, data `String`-nya disalin, artinya kita
menyalin *pointer*, panjang, dan kapasitas yang berada di *stack*. Kita tidak
menyalin data di *heap* yang dirujuk oleh *pointer* tersebut. Dengan kata
lain, representasi data di dalam memori tampak seperti pada Gambar 4-2.

<img alt="Tiga tabel: tabel s1 dan s2 yang masing-masing merepresentasikan
kedua string di stack, dan keduanya menunjuk ke data string yang sama di
heap." src="img/trpl04-02.svg" class="center" style="width: 50%;" />

<span class="caption">Gambar 4-2: Representasi di dalam memori dari variable
`s2` yang memiliki salinan *pointer*, panjang, dan kapasitas dari `s1`</span>

Representasi ini _tidak_ tampak seperti Gambar 4-3, yang merupakan bentuk
memori jika Rust ikut menyalin data di *heap*. Jika Rust melakukan itu,
operasi `s2 = s1` bisa sangat mahal dari segi kinerja saat *runtime* jika
data di *heap*-nya besar.

<img alt="Empat tabel: dua tabel yang merepresentasikan data stack untuk s1
dan s2, dan masing-masing menunjuk ke salinan data string miliknya sendiri di
heap." src="img/trpl04-03.svg" class="center" style="width: 50%;" />

<span class="caption">Gambar 4-3: Kemungkinan lain dari apa yang mungkin
dilakukan `s2 = s1` jika Rust ikut menyalin data *heap*</span>

Sebelumnya kita telah mengatakan bahwa ketika sebuah variable keluar dari
*scope*, Rust secara otomatis memanggil fungsi `drop` dan membersihkan memori
*heap* untuk variable tersebut. Namun, Gambar 4-2 menunjukkan kedua *pointer*
data menunjuk ke lokasi yang sama. Ini adalah sebuah masalah: ketika `s2` dan
`s1` keluar dari *scope*, keduanya akan mencoba membebaskan memori yang sama.
Ini dikenal sebagai error *double free* dan merupakan salah satu *bug*
keamanan memori yang kita sebutkan sebelumnya. Membebaskan memori dua kali
dapat menyebabkan korupsi memori, yang berpotensi mengarah pada celah
keamanan.

Untuk menjamin keamanan memori, setelah baris `let s2 = s1;`, Rust
menganggap `s1` tidak lagi valid. Karena itu, Rust tidak perlu membebaskan
apa pun ketika `s1` keluar dari *scope*. Lihatlah apa yang terjadi ketika
Anda mencoba menggunakan `s1` setelah `s2` dibuat; ini tidak akan berhasil:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-04-cant-use-after-move/src/main.rs:here}}
```

Anda akan mendapatkan error seperti ini karena Rust mencegah Anda
menggunakan *reference* (referensi) yang telah dibatalkan validitasnya:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-04-cant-use-after-move/output.txt}}
```

Jika Anda pernah mendengar istilah *shallow copy* (salinan dangkal) dan
*deep copy* (salinan dalam) saat bekerja dengan bahasa lain, konsep menyalin
*pointer*, panjang, dan kapasitas tanpa menyalin datanya mungkin terdengar
seperti membuat salinan dangkal. Namun, karena Rust juga membatalkan
validitas variable pertama, alih-alih disebut salinan dangkal, proses ini
dikenal sebagai *move* (pemindahan). Dalam contoh ini, kita dapat mengatakan
bahwa `s1` telah *moved* (dipindahkan) ke dalam `s2`. Jadi, yang sebenarnya
terjadi ditunjukkan pada Gambar 4-4.

<img alt="Tiga tabel: tabel s1 dan s2 yang masing-masing merepresentasikan
kedua string di stack, dan keduanya menunjuk ke data string yang sama di
heap. Tabel s1 berwarna abu-abu karena s1 tidak lagi valid; hanya s2 yang
dapat digunakan untuk mengakses data heap." src="img/trpl04-04.svg"
class="center" style="width: 50%;" />

<span class="caption">Gambar 4-4: Representasi di dalam memori setelah `s1`
dibatalkan validitasnya</span>

Itu menyelesaikan masalah kita! Dengan hanya `s2` yang valid, ketika ia
keluar dari *scope*, hanya dialah yang akan membebaskan memorinya, dan
selesailah urusan kita.

Selain itu, ada keputusan desain yang tersirat dari sini: Rust tidak akan
pernah membuat salinan “dalam” dari data Anda secara otomatis. Karena itu,
penyalinan _otomatis_ apa pun dapat dianggap murah dari segi kinerja saat
*runtime*.

#### Scope dan Penetapan

Kebalikannya juga berlaku untuk hubungan antara *scope*, *ownership*, dan
memori yang dibebaskan melalui fungsi `drop`. Ketika Anda menetapkan nilai
yang sepenuhnya baru kepada variable yang sudah ada, Rust akan memanggil
`drop` dan segera membebaskan memori nilai aslinya. Perhatikan kode berikut,
misalnya:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-04b-replacement-drop/src/main.rs:here}}
```

Awalnya kita mendeklarasikan variable `s` dan mengikatnya ke sebuah `String`
dengan nilai `"hello"`. Lalu, kita segera membuat `String` baru dengan nilai
`"ahoy"` dan menetapkannya ke `s`. Pada titik ini, tidak ada apa pun yang
merujuk ke nilai asli di *heap*. Gambar 4-5 mengilustrasikan data di *stack*
dan *heap* sekarang:

<img alt="Satu tabel yang merepresentasikan nilai string di stack, menunjuk
ke potongan data string kedua (ahoy) di heap, dengan data string asli (hello)
berwarna abu-abu karena tidak dapat diakses lagi."
src="img/trpl04-05.svg" class="center" style="width: 50%;" />

<span class="caption">Gambar 4-5: Representasi di dalam memori setelah nilai
awal digantikan seluruhnya</span>

Dengan demikian, *string* aslinya segera keluar dari *scope*. Rust akan
menjalankan fungsi `drop` pada *string* tersebut dan memorinya akan langsung
dibebaskan. Ketika kita mencetak nilainya di akhir, hasilnya adalah
`"ahoy, world!"`.

<!-- Old headings. Do not remove or links may break. -->

<a id="ways-variables-and-data-interact-clone"></a>

<a id="variables-and-data-interacting-with-clone"></a>
#### Variable dan Data yang Berinteraksi dengan Clone

Jika kita _memang_ ingin menyalin secara mendalam data *heap* dari `String`,
bukan hanya data *stack*-nya, kita dapat menggunakan sebuah metode yang umum
dipakai bernama `clone`. Kita akan membahas sintaks metode di Bab 5, tetapi
karena metode adalah fitur yang umum di banyak bahasa pemrograman, Anda
mungkin sudah pernah melihatnya.

Berikut contoh metode `clone` yang sedang digunakan:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-05-clone/src/main.rs:here}}
```

Kode ini berjalan dengan baik dan secara eksplisit menghasilkan perilaku yang
ditunjukkan pada Gambar 4-3, yaitu ketika data *heap*-nya _memang_ disalin.

Ketika Anda melihat pemanggilan `clone`, Anda tahu bahwa ada kode arbitrer
yang sedang dieksekusi dan kode tersebut mungkin mahal. Ini adalah penanda
visual bahwa ada sesuatu yang berbeda sedang terjadi.

<a id="stack-only-data-copy"></a>
#### Data yang Hanya Ada di Stack: Copy

Ada satu kerumitan lagi yang belum kita bicarakan. Kode yang menggunakan
bilangan bulat berikut—sebagiannya pernah ditampilkan di Listing 4-2—berjalan
dan valid:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-06-copy/src/main.rs:here}}
```

Namun, kode ini tampak bertentangan dengan apa yang baru saja kita
pelajari: tidak ada pemanggilan `clone`, tetapi `x` tetap valid dan tidak
dipindahkan ke dalam `y`.

Alasannya adalah bahwa type-type seperti bilangan bulat yang ukurannya
diketahui pada saat kompilasi disimpan seluruhnya di *stack*, sehingga
salinan dari nilai sebenarnya cepat dibuat. Artinya, tidak ada alasan bagi
kita untuk mencegah `x` tetap valid setelah kita membuat variable `y`. Dengan
kata lain, tidak ada perbedaan antara penyalinan dalam dan penyalinan dangkal
di sini, sehingga memanggil `clone` tidak akan menghasilkan apa pun yang
berbeda dari penyalinan dangkal biasa, dan kita bisa melewatinya.

Rust memiliki anotasi khusus yang disebut *trait* `Copy` yang dapat kita
pasang pada type-type yang disimpan di *stack*, seperti bilangan bulat (kita
akan membahas *trait* lebih lanjut di [Bab 10][traits]<!-- ignore -->). Jika
sebuah type mengimplementasikan *trait* `Copy`, variable yang memakainya
tidak dipindahkan, melainkan disalin secara sepele, sehingga tetap valid
setelah ditetapkan ke variable lain.

Rust tidak mengizinkan kita memberi anotasi `Copy` pada sebuah type jika
type tersebut, atau bagian mana pun darinya, telah mengimplementasikan
*trait* `Drop`. Jika type tersebut membutuhkan sesuatu yang khusus terjadi
ketika nilainya keluar dari *scope*, dan kita menambahkan anotasi `Copy` ke
type itu, kita akan mendapatkan error waktu kompilasi. Untuk mempelajari cara
menambahkan anotasi `Copy` pada type Anda guna mengimplementasikan *trait*
tersebut, lihat [“Trait yang Dapat Diturunkan”][derivable-traits]<!-- ignore
--> di Lampiran C.

Lalu, type apa saja yang mengimplementasikan *trait* `Copy`? Anda dapat
memeriksa dokumentasi untuk type tertentu demi memastikannya, tetapi sebagai
aturan umum, kelompok nilai skalar sederhana mana pun dapat
mengimplementasikan `Copy`, dan apa pun yang membutuhkan alokasi atau
merupakan suatu bentuk sumber daya tidak dapat mengimplementasikan `Copy`.
Berikut beberapa type yang mengimplementasikan `Copy`:

- Semua type bilangan bulat, seperti `u32`.
- Type Boolean, `bool`, dengan nilai `true` dan `false`.
- Semua type *floating point* (floating point), seperti `f64`.
- Type karakter, `char`.
- *Tuple*, jika hanya berisi type-type yang juga mengimplementasikan `Copy`.
  Misalnya, `(i32, i32)` mengimplementasikan `Copy`, tetapi `(i32, String)`
  tidak.

### Ownership dan Fungsi

Mekanisme penerusan sebuah nilai ke sebuah fungsi serupa dengan mekanisme
penetapan nilai ke sebuah variable. Meneruskan variable ke sebuah fungsi akan
memindahkan atau menyalin, sama seperti penetapan. Listing 4-3 memuat contoh
dengan beberapa anotasi yang menunjukkan di mana variable masuk dan keluar
dari *scope*.

<Listing number="4-3" file-name="src/main.rs" caption="Fungsi-fungsi dengan ownership dan scope yang diberi anotasi">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-03/src/main.rs}}
```

</Listing>

Jika kita mencoba menggunakan `s` setelah pemanggilan `takes_ownership`,
Rust akan melemparkan error waktu kompilasi. Pemeriksaan statis ini
melindungi kita dari kesalahan. Cobalah menambahkan kode ke `main` yang
menggunakan `s` dan `x` untuk melihat di mana Anda dapat memakainya dan di
mana aturan-aturan *ownership* mencegah Anda melakukannya.

### Nilai Kembalian dan Scope

Mengembalikan nilai juga dapat memindahkan *ownership*. Listing 4-4
menampilkan contoh fungsi yang mengembalikan sebuah nilai, dengan anotasi
serupa seperti pada Listing 4-3.

<Listing number="4-4" file-name="src/main.rs" caption="Memindahkan ownership dari nilai-return value">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-04/src/main.rs}}
```

</Listing>

Kepemilikan sebuah variable mengikuti pola yang sama setiap kali: menetapkan
sebuah nilai ke variable lain akan memindahkannya. Ketika sebuah variable
yang memuat data di *heap* keluar dari *scope*, nilainya akan dibersihkan
oleh `drop` kecuali kepemilikan datanya telah dipindahkan ke variable lain.

Meskipun cara ini berhasil, mengambil *ownership* lalu mengembalikannya lagi
pada setiap fungsi agak melelahkan. Bagaimana jika kita ingin membiarkan
sebuah fungsi menggunakan sebuah nilai tanpa mengambil *ownership*-nya?
Cukup menjengkelkan bahwa apa pun yang kita teruskan juga harus dikembalikan
jika kita ingin memakainya lagi, di samping data apa pun yang dihasilkan dari
badan fungsi yang mungkin juga ingin kita kembalikan.

Rust memang mengizinkan kita mengembalikan beberapa nilai menggunakan sebuah
*tuple*, seperti ditunjukkan pada Listing 4-5.

<Listing number="4-5" file-name="src/main.rs" caption="Mengembalikan ownership dari parameter-parameter">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-05/src/main.rs}}
```

</Listing>

Namun, ini terlalu banyak formalitas dan pekerjaan untuk sebuah konsep yang
seharusnya lumrah. Untungnya bagi kita, Rust memiliki fitur untuk
menggunakan sebuah nilai tanpa memindahkan *ownership*-nya: *reference*.

[data-types]: ch03-02-data-types.html#data-types
[ch8]: ch08-02-strings.html
[traits]: ch10-02-traits.html
[derivable-traits]: appendix-03-derivable-traits.html
[methods]: ch05-03-method-syntax.html#methods
[paths-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
