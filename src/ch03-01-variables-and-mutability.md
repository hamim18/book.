<a id="variables-and-mutability"></a>
## Variable dan Mutabilitas

Seperti disebutkan di bagian [“Menyimpan Nilai dengan
Variable”][storing-values-with-variables]<!-- ignore -->, secara bawaan
variable bersifat *immutable* (tidak dapat diubah). Ini adalah salah satu dari
sekian banyak dorongan yang diberikan Rust kepada Anda untuk menulis kode
dengan cara yang memanfaatkan keamanan dan kemudahan concurrency yang
ditawarkan Rust. Meski begitu, Anda tetap punya pilihan untuk membuat variable
menjadi *mutable* (dapat diubah). Mari kita lihat bagaimana dan mengapa Rust
mendorong Anda untuk memilih immutability, dan mengapa kadang-kadang Anda
mungkin ingin tidak mengikutinya.

Ketika sebuah variable bersifat *immutable*, begitu sebuah nilai terikat pada
sebuah nama, Anda tidak dapat mengubah nilai itu. Untuk memperlihatkannya,
buat proyek baru bernama _variables_ di direktori _projects_ Anda dengan
memakai `cargo new variables`.

Kemudian, di direktori _variables_ yang baru, buka _src/main.rs_ dan ganti
kodenya dengan kode berikut, yang belum dapat dikompilasi:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

Simpan dan jalankan programnya dengan `cargo run`. Anda seharusnya menerima
pesan error mengenai error immutability, seperti yang ditunjukkan pada
output berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

Contoh ini menunjukkan bagaimana *compiler* (kompilator) membantu Anda
menemukan error dalam program Anda. Error dari *compiler* bisa membuat
frustrasi, tetapi sebenarnya error itu hanya berarti program Anda belum
secara aman melakukan apa yang Anda inginkan; error itu _bukan_ berarti Anda
bukan programmer yang baik! Rustacean yang berpengalaman pun masih mendapatkan
error *compiler*.

Anda menerima pesan error `` cannot assign twice to immutable variable `x` `` karena Anda mencoba menetapkan nilai kedua ke variable `x` yang *immutable*.

Penting bagi kita untuk mendapatkan error pada waktu kompilasi ketika kita
mencoba mengubah nilai yang ditetapkan sebagai *immutable*, karena situasi
seperti ini dapat menimbulkan bug. Jika satu bagian kode kita berjalan dengan
asumsi bahwa sebuah nilai tidak akan pernah berubah dan bagian lain dari kode
kita mengubah nilai itu, mungkin saja bagian pertama kode tidak akan melakukan
apa yang dirancang untuk dilakukannya. Penyebab bug semacam ini bisa sulit
dilacak setelah terjadi, apalagi ketika bagian kode kedua hanya mengubah nilai
itu _kadang-kadang_ saja. *Compiler* Rust menjamin bahwa ketika Anda menyatakan
sebuah nilai tidak akan berubah, nilai itu benar-benar tidak akan berubah,
sehingga Anda tidak perlu melacaknya sendiri. Dengan demikian kode Anda lebih
mudah untuk dinalar.

Tetapi mutabilitas bisa sangat berguna dan dapat membuat kode lebih nyaman
ditulis. Meskipun variable bersifat *immutable* secara bawaan, Anda dapat
membuatnya *mutable* dengan menambahkan `mut` di depan nama variable seperti
yang Anda lakukan di [Bab 2][storing-values-with-variables]<!-- ignore -->.
Menambahkan `mut` juga menyampaikan maksud kepada pembaca kode di masa depan
dengan menandakan bahwa bagian lain dari kode akan mengubah nilai variable
tersebut.

Sebagai contoh, mari kita ubah _src/main.rs_ menjadi seperti berikut:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

Ketika kita menjalankan programnya sekarang, kita mendapatkan hasil seperti
ini:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

Kita diizinkan mengubah nilai yang terikat pada `x` dari `5` menjadi `6`
ketika `mut` digunakan. Pada akhirnya, keputusan untuk memakai mutability
atau tidak ada di tangan Anda dan bergantung pada apa yang menurut Anda
paling jelas dalam situasi tersebut.

<!-- Old headings. Do not remove or links may break. -->
<a id="constants"></a>

<a id="declaring-constants"></a>
### Mendeklarasikan Constant

Seperti variable *immutable*, _konstanta_ adalah nilai yang terikat pada sebuah
nama dan tidak diizinkan untuk berubah, tetapi ada beberapa perbedaan antara
constant dan variable.

Pertama, Anda tidak diizinkan memakai `mut` pada constant. Constant tidak
hanya *immutable* secara bawaan—constant selalu *immutable*. Anda mendeklarasikan
constant dengan memakai keyword `const`, bukan keyword `let`, dan type
nilainya _harus_ diberi anotasi. Kita akan membahas type dan type annotation di
bagian berikutnya, [“Type Data”][data-types]<!-- ignore -->, jadi jangan
khawatir soal detailnya untuk sekarang. Cukup ketahui bahwa Anda harus selalu
memberi anotasi pada typenya.

Constant dapat dideklarasikan di *scope* (cakupan) mana pun, termasuk *scope*
global, yang membuatnya berguna untuk nilai yang perlu diketahui oleh banyak
bagian kode.

Perbedaan terakhir adalah constant hanya boleh diisi dengan expression
constant, bukan hasil dari nilai yang hanya bisa dihitung pada saat runtime.

Berikut adalah contoh deklarasi constant:

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

Nama constantnya adalah `THREE_HOURS_IN_SECONDS`, dan nilainya diisi dengan
hasil perkalian 60 (jumlah detik dalam satu menit) dengan 60 (jumlah menit
dalam satu jam) dengan 3 (jumlah jam yang ingin kita hitung dalam program
ini). Konvensi penamaan Rust untuk constant adalah memakai huruf kapital
semua dengan garis bawah di antara kata. *Compiler* mampu mengevaluasi
sekumpulan operasi terbatas pada waktu kompilasi, sehingga kita dapat memilih
untuk menulis nilai ini dengan cara yang lebih mudah dipahami dan diverifikasi
daripada mengisi constant ini dengan nilai 10.800. Lihat bagian evaluasi
constant di [Rust *Reference*][const-eval] untuk informasi lebih lanjut tentang
operasi apa saja yang dapat dipakai saat mendeklarasikan constant.

Constant berlaku selama program berjalan, di dalam *scope* tempat constant itu
dideklarasikan. Sifat ini membuat constant berguna untuk nilai dalam domain
aplikasi Anda yang mungkin perlu diketahui oleh banyak bagian program, seperti
jumlah poin maksimum yang boleh diperoleh pemain mana pun dalam sebuah
permainan, atau kecepatan cahaya.

Menamai nilai yang ditulis langsung di dalam kode (hardcoded) yang dipakai di
seluruh program Anda sebagai constant berguna untuk menyampaikan makna nilai
tersebut kepada pemelihara kode di masa depan. Hal itu juga membantu karena
hanya ada satu tempat di kode Anda yang perlu diubah jika nilai yang ditulis langsung (hardcoded) itu
perlu diperbarui di masa mendatang.

### Shadowing

Seperti yang Anda lihat dalam tutorial permainan tebak angka di [Bab
2][comparing-the-guess-to-the-secret-number]<!-- ignore -->, Anda dapat
mendeklarasikan variable baru dengan nama yang sama seperti variable
sebelumnya. Para Rustacean mengatakan bahwa variable pertama di-_shadow_ oleh
variable kedua, artinya variable kedualah yang akan dilihat *compiler* ketika
Anda memakai nama variable tersebut. Pada dasarnya, variable kedua menutupi
variable pertama, mengambil semua pemakaian nama variable itu untuk dirinya
sendiri sampai variable kedua itu sendiri di-shadow atau *scope*-nya berakhir.
Kita dapat melakukan shadowing pada sebuah variable dengan memakai nama
variable yang sama dan mengulangi penggunaan keyword `let` seperti berikut:

<span class="filename">Nama File: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

Program ini mula-mula mengikat `x` pada nilai `5`. Lalu, program membuat
variable baru `x` dengan mengulangi `let x =`, mengambil nilai aslinya dan
menambahkan `1` sehingga nilai `x` menjadi `6`. Kemudian, di dalam *scope*
bagian dalam yang dibuat dengan kurung kurawal, statement `let` ketiga juga
melakukan shadowing terhadap `x` dan membuat variable baru, dengan mengalikan
nilai sebelumnya dengan `2` sehingga `x` bernilai `12`. Ketika *scope* itu
berakhir, shadowing bagian dalam pun berakhir dan `x` kembali menjadi `6`.
Ketika kita menjalankan program ini, program akan menampilkan output
berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

Shadowing berbeda dari menandai variable sebagai `mut` karena kita akan
mendapatkan error pada waktu kompilasi jika tanpa sengaja mencoba menetapkan
ulang variable ini tanpa memakai keyword `let`. Dengan memakai `let`, kita
dapat melakukan beberapa transformasi pada sebuah nilai, tetapi variablenya
tetap *immutable* setelah transformasi itu selesai.

Perbedaan lain antara `mut` dan shadowing adalah, karena kita pada dasarnya
membuat variable baru ketika memakai keyword `let` lagi, kita dapat mengubah
type nilainya sambil memakai ulang nama yang sama. Sebagai contoh, misalkan
program kita meminta pengguna menunjukkan berapa banyak spasi yang mereka
inginkan di antara beberapa teks dengan memasukkan karakter spasi, lalu kita
ingin menyimpan input itu sebagai angka:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

Variable `spaces` pertama typed string, dan variable `spaces` kedua typed
angka. Dengan demikian shadowing menyelamatkan kita dari keharusan memikirkan
nama yang berbeda, seperti `spaces_str` dan `spaces_num`; kita cukup memakai
ulang nama `spaces` yang lebih sederhana. Namun, jika kita mencoba memakai
`mut` untuk hal ini, seperti yang ditunjukkan di sini, kita akan mendapatkan
error pada waktu kompilasi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

Error tersebut menyatakan bahwa kita tidak diizinkan mengubah type sebuah
variable:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

Setelah kita mengeksplorasi cara kerja variable, mari kita lihat lebih banyak
data type yang dapat dimiliki variable.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html
