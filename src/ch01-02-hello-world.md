## Hello, World!

Setelah Rust terpasang, sekarang saatnya menulis program Rust pertama Anda.
Ketika mempelajari bahasa baru, tradisinya adalah menulis program kecil yang
mencetak teks `Hello, world!` ke layar, jadi kita akan melakukan hal yang
sama di sini!

> Catatan: Buku ini mengasumsikan Anda cukup familier dengan baris perintah.
> Rust tidak menuntut hal khusus tentang cara Anda menyunting atau perangkat yang Anda
> pakai ataupun lokasi kode Anda, jadi jika Anda lebih suka memakai IDE
> alih-alih baris perintah, silakan memakai IDE favorit Anda. Banyak IDE kini
> memiliki dukungan Rust sampai taraf tertentu; periksa dokumentasi IDE
> tersebut untuk detailnya. Tim Rust selama ini berfokus menghadirkan
> dukungan IDE yang hebat melalui `rust-analyzer`. Lihat
> [Lampiran D][devtools]<!-- ignore --> untuk detail lebih lanjut.

<!-- Old headings. Do not remove or links may break. -->
<a id="creating-a-project-directory"></a>

### Menyiapkan Direktori Proyek

Anda akan memulai dengan membuat direktori untuk menyimpan kode Rust Anda.
Bagi Rust, lokasi kode Anda tidak menjadi soal, tetapi untuk latihan dan
proyek dalam buku ini, kita menyarankan Anda membuat direktori _projects_ di
direktori home Anda dan menyimpan semua proyek Anda di sana.

Buka terminal dan masukkan perintah-perintah berikut untuk membuat direktori
_projects_ dan sebuah direktori untuk proyek “Hello, world!” di dalam
direktori _projects_ tersebut.

Untuk Linux, macOS, dan PowerShell di Windows, masukkan ini:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

Untuk Windows CMD, masukkan ini:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-and-running-a-rust-program"></a>

<a id="rust-program-basics"></a>
### Dasar-Dasar Program Rust

Berikutnya, buat file sumber baru dan beri nama _main.rs_. File Rust selalu
diakhiri dengan ekstensi _.rs_. Jika Anda memakai lebih dari satu kata dalam
nama file, konvensinya adalah memakai garis bawah sebagai pemisah.
Misalnya, gunakan _hello_world.rs_ alih-alih _helloworld.rs_.

Sekarang buka file _main.rs_ yang baru saja Anda buat dan masukkan kode di
Listing 1-1.

<Listing number="1-1" file-name="main.rs" caption="Sebuah program yang mencetak `Hello, world!`">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

Simpan file tersebut dan kembali ke jendela terminal di direktori
_~/projects/hello_world_. Di Linux atau macOS, masukkan perintah-perintah
berikut untuk mengompilasi dan menjalankan file tersebut:

```console
$ rustc main.rs
$ ./main
Hello, world!
```

Di Windows, masukkan perintah `.\main` alih-alih `./main`:

```powershell
> rustc main.rs
> .\main
Hello, world!
```

Apa pun sistem operasi Anda, string `Hello, world!` seharusnya tercetak ke
terminal. Jika Anda tidak melihat keluaran ini, lihat kembali bagian
[“Pemecahan Masalah”][troubleshooting]<!-- ignore --> dari bagian Instalasi
untuk cara meminta bantuan.

Jika `Hello, world!` tercetak, selamat! Anda telah resmi menulis program
Rust. Itu menjadikan Anda seorang pemrogram Rust—selamat datang!

<!-- Old headings. Do not remove or links may break. -->

<a id="anatomy-of-a-rust-program"></a>

### Anatomi Program Rust

Mari kita telaah program “Hello, world!” ini secara detail. Berikut potongan
pertama dari teka-tekinya:

```rust
fn main() {

}
```

Baris-baris ini mendefinisikan fungsi bernama `main`. Fungsi `main` itu
istimewa: fungsi ini selalu menjadi kode pertama yang dijalankan di setiap
program Rust yang dapat dieksekusi. Di sini, baris pertama mendeklarasikan
sebuah fungsi bernama `main` yang tidak memiliki parameter dan tidak
mengembalikan apa pun. Jika ada parameter, parameter itu akan berada di
dalam tanda kurung (`()`).

Badan fungsi dibungkus dalam `{}`. Rust mewajibkan kurung kurawal di
sekeliling semua badan fungsi. Merupakan gaya yang baik untuk menempatkan
kurung kurawal pembuka di baris yang sama dengan deklarasi fungsi, dengan
satu spasi di antaranya.

> Catatan: Jika Anda ingin mempertahankan gaya yang standar di seluruh
> proyek Rust, Anda dapat memakai alat pemformat otomatis bernama `rustfmt`
> untuk memformat kode Anda dalam gaya tertentu (lebih lanjut tentang
> `rustfmt` di [Lampiran D][devtools]<!-- ignore -->). Tim Rust telah
> menyertakan alat ini dalam distribusi standar Rust, sama seperti `rustc`,
> jadi alat ini seharusnya sudah terpasang di komputer Anda!

Badan fungsi `main` memuat kode berikut:

```rust
println!("Hello, world!");
```

Baris ini melakukan semua pekerjaan dalam program kecil ini: baris ini
mencetak teks ke layar. Ada tiga detail penting yang perlu diperhatikan di
sini.

Pertama, `println!` memanggil sebuah *macro* (makro) Rust. Jika yang
dipanggil adalah fungsi, penulisannya adalah `println` (tanpa `!`). Makro
Rust adalah cara menulis kode yang menghasilkan kode untuk memperluas
sintaks Rust, dan kita akan membahasnya lebih detail di
[Bab 20][ch20-macros]<!-- ignore -->. Untuk saat ini, Anda cukup tahu bahwa
memakai `!` berarti Anda memanggil makro alih-alih fungsi biasa, dan bahwa
makro tidak selalu mengikuti aturan yang sama seperti fungsi.

Kedua, Anda melihat string `"Hello, world!"`. Kita meneruskan string ini
sebagai argumen ke `println!`, lalu string tersebut dicetak ke layar.

Ketiga, kita mengakhiri baris dengan titik koma (`;`), yang menandakan
bahwa ekspresi ini telah selesai dan ekspresi berikutnya siap dimulai.
Sebagian besar baris kode Rust diakhiri dengan titik koma.

<!-- Old headings. Do not remove or links may break. -->
<a id="compiling-and-running-are-separate-steps"></a>

### Kompilasi dan Eksekusi

Anda baru saja menjalankan program yang baru dibuat, jadi mari kita periksa
setiap langkah dalam prosesnya.

Sebelum menjalankan program Rust, Anda harus mengompilasinya menggunakan
*compiler* (kompilator) Rust dengan memasukkan perintah `rustc` dan
memberikan nama file sumber Anda kepadanya, seperti ini:

```console
$ rustc main.rs
```

Jika Anda berlatar belakang C atau C++, Anda akan menyadari bahwa ini mirip
dengan `gcc` atau `clang`. Setelah berhasil dikompilasi, Rust menghasilkan
file biner yang dapat dieksekusi.

Di Linux, macOS, dan PowerShell di Windows, Anda dapat melihat file
eksekutabelnya dengan memasukkan perintah `ls` di shell Anda:

```console
$ ls
main  main.rs
```

Di Linux dan macOS, Anda akan melihat dua file. Dengan PowerShell di
Windows, Anda akan melihat tiga file yang sama seperti yang Anda lihat
dengan CMD. Dengan CMD di Windows, Anda perlu memasukkan perintah berikut:

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

Ini menampilkan file kode sumber dengan ekstensi _.rs_, file eksekutabelnya
(_main.exe_ di Windows, tetapi _main_ di semua platform lain), dan, ketika
memakai Windows, sebuah file yang berisi informasi debugging dengan
ekstensi _.pdb_. Dari sini, Anda menjalankan file _main_ atau _main.exe_,
seperti ini:

```console
$ ./main # or .\main on Windows
```

Jika _main.rs_ Anda adalah program “Hello, world!” Anda, baris ini mencetak
`Hello, world!` ke terminal Anda.

Jika Anda lebih familier dengan bahasa dinamis, seperti Ruby, Python, atau
JavaScript, Anda mungkin tidak terbiasa mengompilasi dan menjalankan
program sebagai langkah yang terpisah. Rust adalah bahasa yang
_ahead-of-time compiled_ (dikompilasi lebih awal), artinya Anda dapat
mengompilasi program dan memberikan file eksekutabelnya kepada orang lain,
dan mereka dapat menjalankannya bahkan tanpa memasang Rust. Jika Anda
memberikan file _.rb_, _.py_, atau _.js_ kepada seseorang, mereka harus
memasang implementasi Ruby, Python, atau JavaScript (sesuai urutannya).
Namun, pada bahasa-bahasa itu, Anda hanya butuh satu perintah untuk
mengompilasi dan menjalankan program. Segala sesuatu adalah kompromi dalam
desain bahasa.

Mengompilasi hanya dengan `rustc` sudah cukup untuk program sederhana,
tetapi seiring berkembangnya proyek Anda, Anda akan ingin mengelola semua
opsinya dan mempermudah berbagi kode. Berikutnya, kita akan memperkenalkan
Anda pada alat Cargo, yang akan membantu Anda menulis program Rust untuk
dunia nyata.

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html
