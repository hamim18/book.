## Membangun Web Server Single-Threaded

Kita akan mulai dengan membuat web server single-threaded bekerja. Sebelum
kita mulai, mari kita lihat sekilas protocol-protocol yang terlibat dalam
pembangunan web server. Detail protocol-protocol ini berada di luar *scope*
buku ini, tetapi ringkasan singkat akan memberi Anda informasi yang Anda
butuhkan.

Dua protocol utama yang terlibat dalam web server adalah *Hypertext Transfer
Protocol* *(HTTP)* dan *Transmission Control Protocol* *(TCP)*. Kedua
protocol itu adalah protocol *request-response*, yang berarti sebuah
*client* (klien) memulai request dan sebuah *server* mendengarkan
request itu serta memberikan response kepada client. Isi request dan
response itu ditentukan oleh protokolnya.

TCP adalah protocol tingkat yang lebih rendah yang menjelaskan detail
tentang bagaimana informasi berpindah dari satu server ke server lain,
tetapi tidak menentukan apa informasi itu. HTTP dibangun di atas TCP dengan
mendefinisikan isi request dan responsnya. Secara teknis, HTTP bisa
dipakai dengan protocol lain, tetapi pada sebagian besar kasus, HTTP
mengirim datanya melalui TCP. Kita akan bekerja dengan byte mentah dari
request dan response TCP dan HTTP.

### Mendengarkan Connection TCP

Server web kita perlu mendengarkan connection TCP, jadi itulah bagian pertama
yang akan kita kerjakan. Pustaka standar menyediakan *module* `std::net` yang
memungkinkan kita melakukannya. Mari kita buat proyek baru dengan cara yang
biasa:

```console
$ cargo new hello
     Created binary (application) `hello` project
$ cd hello
```

Sekarang masukkan kode di Listing 21-1 ke _src/main.rs_ untuk memulai. Kode
ini akan mendengarkan alamat lokal `127.0.0.1:7878` untuk *stream* TCP yang
masuk. Ketika ia menerima *stream* yang masuk, ia akan mencetak `Connection
established!`.

<Listing number="21-1" file-name="src/main.rs" caption="Mendengarkan stream yang masuk dan mencetak pesan saat kita menerima stream">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-01/src/main.rs}}
```

</Listing>

Dengan memakai `TcpListener`, kita bisa mendengarkan connection TCP pada
alamat `127.0.0.1:7878`. Pada alamat itu, bagian sebelum titik dua adalah
alamat IP yang mewakili komputer Anda (alamat ini sama di setiap komputer
dan tidak mewakili komputer para penulis secara khusus), dan `7878` adalah
portnya. Kami memilih port ini karena dua alasan: HTTP biasanya tidak
diterima pada port ini, jadi server kita kemungkinan besar tidak akan
bentrok dengan web server lain yang mungkin sedang berjalan di mesin Anda,
dan 7878 adalah _rust_ jika diketik pada telepon.

Fungsi `bind` dalam skenario ini bekerja seperti fungsi `new`, yaitu
mengembalikan instance `TcpListener` baru. Fungsi ini disebut `bind` karena,
dalam jaringan, menghubungkan diri ke sebuah port untuk mendengarkannya
dikenal sebagai “mengikat ke sebuah port.”

Fungsi `bind` mengembalikan `Result<T, E>`, yang menunjukkan bahwa
pengikatan bisa saja gagal, misalnya, jika kita menjalankan dua instance
program kita sehingga ada dua program yang mendengarkan port yang sama.
Karena kita menulis server dasar hanya untuk tujuan belajar, kita tidak
akan memusingkan penanganan error semacam ini; sebagai gantinya, kita
memakai `unwrap` untuk menghentikan program jika terjadi error.

Method `incoming` pada `TcpListener` mengembalikan *iterator* yang memberi
kita urutan *stream* (lebih tepatnya, *stream* bertipe `TcpStream`). Sebuah
_stream_ tunggal mewakili connection terbuka antara client dan server.
_Koneksi_ adalah nama untuk seluruh proses request dan response di mana
client terhubung ke server, server menghasilkan response, dan server menutup
koneksinya. Dengan demikian, kita akan membaca dari `TcpStream` untuk
melihat apa yang dikirim client lalu menulis response kita ke *stream* itu
untuk mengirim data kembali ke client. Secara keseluruhan, loop `for` ini
akan memproses setiap connection secara bergiliran dan menghasilkan
serangkaian *stream* untuk kita tangani.

Untuk saat ini, penanganan *stream* kita terdiri dari memanggil `unwrap`
untuk mengakhiri program kita jika *stream* itu memiliki error; jika tidak
ada error, program akan mencetak pesan. Kita akan menambahkan lebih banyak
fungsionalitas untuk kasus sukses di listing berikutnya. Alasan kita
mungkin menerima error dari method `incoming` saat client terhubung ke
server adalah bahwa kita sebenarnya tidak mengiterasi connection. Sebaliknya,
kita mengiterasi *connection attempt*. Connection itu mungkin tidak berhasil
karena sejumlah alasan, banyak di antaranya spesifik untuk sistem operasi.
Misalnya, banyak sistem operasi memiliki batas jumlah connection terbuka
serentak yang bisa mereka dukung; connection attempt baru di luar jumlah itu
akan menghasilkan error sampai sebagian connection yang terbuka ditutup.

Mari kita coba menjalankan kode ini! Jalankan `cargo run` di terminal lalu
muat _127.0.0.1:7878_ di web browser. Peramban seharusnya menampilkan
pesan error seperti “Connection reset” karena server saat ini tidak
mengirimkan data apa pun kembali. Tetapi saat Anda melihat terminal Anda,
Anda seharusnya melihat beberapa pesan yang dicetak saat peramban terhubung
ke server!

```text
     Running `target/debug/hello`
Connection established!
Connection established!
Connection established!
```

Terkadang Anda akan melihat banyak pesan dicetak untuk satu request
peramban; alasannya mungkin peramban membuat request untuk halamannya
sekaligus request untuk sumber lain, seperti ikon _favicon.ico_ yang
muncul di tab peramban.

Bisa juga peramban sedang mencoba terhubung ke server berkali-kali karena
server tidak merespons dengan data apa pun. Ketika `stream` keluar dari
*scope* dan dibebaskan di akhir loop, koneksinya ditutup sebagai bagian dari
implementasi `drop`. Peramban terkadang menangani connection yang tertutup
dengan mencoba ulang, karena masalahnya mungkin hanya sementara.

Peramban juga terkadang membuka banyak connection ke server tanpa mengirim
request apa pun supaya jika mereka *memang* mengirim request nanti,
request itu bisa terjadi lebih cepat. Ketika ini terjadi, server kita
akan melihat setiap connection, terlepas dari ada atau tidaknya request
pada connection itu. Banyak versi peramban berbasis Chrome melakukan ini,
misalnya; Anda bisa menonaktifkan optimasi itu dengan memakai mode
penjelajahan privat atau memakai peramban lain.

Faktor pentingnya adalah kita telah berhasil mendapatkan handle ke connection
TCP!

Ingatlah untuk menghentikan program dengan menekan <kbd>ctrl</kbd>-<kbd>C</kbd>
saat Anda selesai menjalankan versi kode tertentu. Lalu, mulai ulang
program dengan menjalankan perintah `cargo run` setelah Anda membuat
setiap rangkaian perubahan kode untuk memastikan Anda menjalankan kode
terbaru.

### Membaca Request

Mari kita implementasikan fungsionalitas untuk membaca request dari
peramban! Untuk memisahkan tanggung jawab antara mendapatkan connection
terlebih dahulu lalu mengambil tindakan dengan connection itu, kita akan
memulai fungsi baru untuk memproses connection. Di fungsi `handle_connection`
yang baru ini, kita akan membaca data dari *stream* TCP dan mencetaknya
supaya kita bisa melihat data yang dikirim dari peramban. Ubah kodenya agar
tampak seperti Listing 21-2.

<Listing number="21-2" file-name="src/main.rs" caption="Membaca dari `TcpStream` dan mencetak datanya">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-02/src/main.rs}}
```

</Listing>

Kita membawa `std::io::BufReader` dan `std::io::prelude` ke dalam *scope*
untuk mendapatkan akses ke *trait* dan type yang memungkinkan kita membaca
dari dan menulis ke *stream*. Di loop `for` pada fungsi `main`, alih-alih
mencetak pesan yang menyatakan bahwa kita membuat connection, kita sekarang
memanggil fungsi `handle_connection` yang baru dan memberikan `stream`
kepadanya.

Di fungsi `handle_connection`, kita membuat instance `BufReader` baru yang
membungkus sebuah *reference* ke `stream`. `BufReader` menambahkan buffering
dengan mengelola pemanggilan method-method *trait* `std::io::Read` untuk
kita.

Kita membuat variable bernama `http_request` untuk mengumpulkan
baris-request line yang dikirim peramban ke server kita. Kita
menandakan bahwa kita ingin mengumpulkan baris-baris itu ke dalam vector
dengan menambahkan type annotation `Vec<_>`.

`BufReader` mengimplementasikan *trait* `std::io::BufRead`, yang menyediakan
method `lines`. Method `lines` mengembalikan iterator `Result<String,
std::io::Error>` dengan membelah stream data setiap kali ia melihat byte
newline. Untuk mendapatkan setiap `String`, kita me-`map` dan me-`unwrap`
setiap `Result`. `Result` itu mungkin error jika datanya bukan UTF-8 yang
valid atau jika ada masalah saat membaca dari *stream*. Sekali lagi, program
produksi seharusnya menangani error-error ini dengan lebih baik, tetapi
kita memilih untuk menghentikan program pada kasus error demi
kesederhanaan.

Peramban menandakan akhir sebuah request HTTP dengan mengirim dua
karakter newline berturut-turut, jadi untuk mendapatkan satu request
dari *stream*, kita mengambil baris-baris sampai kita mendapat baris yang
berupa string kosong. Setelah kita mengumpulkan baris-baris itu ke dalam
vector, kita mencetaknya dengan format debug yang rapi supaya kita bisa
melihat instruksi yang dikirim web browser ke server kita.

Mari kita coba kode ini! Mulai programnya dan buat request di peramban
web lagi. Perhatikan bahwa kita tetap akan mendapat halaman error di
peramban, tetapi output program kita di terminal sekarang akan tampak mirip
seperti ini:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-02
cargo run
make a request to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

Bergantung pada peramban Anda, outputnya mungkin sedikit berbeda. Sekarang
setelah kita mencetak data permintaannya, kita bisa melihat mengapa kita
mendapat banyak connection dari satu request peramban dengan melihat *path*
setelah `GET` di baris pertama request. Jika connection yang berulang
semuanya meminta _/_, kita tahu peramban sedang mencoba mengambil _/_
berkali-kali karena ia tidak mendapat response dari program kita.

Mari kita urai data request ini untuk memahami apa yang diminta
peramban dari program kita.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-closer-look-at-an-http-request"></a>
<a id="looking-closer-at-an-http-request"></a>

### Menelaah Request HTTP Lebih Dekat

HTTP adalah protocol berbasis teks, dan sebuah request memakai format
berikut:

```text
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

Baris pertama adalah *request line* yang memuat informasi tentang apa
yang diminta client. Bagian pertama dari request line menunjukkan
method yang dipakai, seperti `GET` atau `POST`, yang menggambarkan
bagaimana client membuat request ini. Client kita memakai request
`GET`, yang berarti ia meminta informasi.

Bagian berikutnya dari request line adalah _/_, yang menunjukkan
*uniform resource identifier* *(URI)* yang diminta client: URI hampir, tetapi
tidak sepenuhnya, sama dengan *uniform resource locator* *(URL)*. Perbedaan
antara URI dan URL tidak penting untuk keperluan kita di bab ini, tetapi
spesifikasi HTTP memakai istilah _URI_, jadi di sini kita bisa saja
mengganti _URI_ dengan _URL_ di pikiran kita.

Bagian terakhir adalah versi HTTP yang dipakai client, lalu baris
request itu berakhir dengan urutan CRLF. (_CRLF_ adalah singkatan dari
_carriage return_ dan _line feed_, istilah dari zaman mesin ketik!) Urutan
CRLF juga bisa ditulis sebagai `\r\n`, dengan `\r` adalah carriage return
dan `\n` adalah line feed. _Urutan CRLF_ memisahkan request line dari
sisa data request. Perhatikan bahwa saat CRLF dicetak, kita melihat
awal baris baru, bukan `\r\n`.

Melihat data request line yang kita terima dari menjalankan program
kita sejauh ini, kita melihat bahwa `GET` adalah methodnya, _/_ adalah URI
permintaannya, dan `HTTP/1.1` adalah versinya.

Setelah request line, baris-baris tersisa mulai dari `Host:` dan
seterusnya adalah header. Request `GET` tidak memiliki body.

Cobalah membuat request dari peramban yang berbeda atau meminta alamat
yang berbeda, seperti _127.0.0.1:7878/test_, untuk melihat bagaimana data
permintaannya berubah.

Sekarang setelah kita tahu apa yang diminta peramban, mari kita kirimkan
balasan berupa data!

### Menulis Response

Kita akan mengimplementasikan pengiriman data sebagai response terhadap
request client. Response memiliki format berikut:

```text
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

Baris pertama adalah *status line* yang memuat versi HTTP yang dipakai
dalam response, status code numerik yang merangkum hasil request, dan
reason phrase yang memberikan deskripsi teks dari status code itu. Setelah
urutan CRLF ada header apa pun, urutan CRLF lagi, dan isi responsnya.

Berikut contoh response yang memakai HTTP versi 1.1 dan memiliki status code
200, reason phrase OK, tanpa header, dan tanpa isi:

```text
HTTP/1.1 200 OK\r\n\r\n
```

Kode status 200 adalah response sukses standar. Teks itu adalah response HTTP
sukses yang kecil. Mari kita tulis ini ke *stream* sebagai response kita
terhadap request yang sukses! Dari fungsi `handle_connection`, hapus
`println!` yang mencetak data request dan ganti dengan kode di Listing
21-3.

<Listing number="21-3" file-name="src/main.rs" caption="Menulis response HTTP sukses yang kecil ke stream">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-03/src/main.rs:here}}
```

</Listing>

Baris baru pertama mendefinisikan variable `response` yang menyimpan data
pesan sukses. Lalu, kita memanggil `as_bytes` pada `response` kita untuk
mengubah data string itu menjadi byte. Method `write_all` pada `stream`
menerima `&[u8]` dan mengirim byte-byte itu langsung melalui connection.
Karena operasi `write_all` bisa gagal, kita memakai `unwrap` pada hasil
error apa pun seperti sebelumnya. Sekali lagi, dalam aplikasi sungguhan,
Anda akan menambahkan penanganan error di sini.

Dengan perubahan ini, mari kita jalankan kode kita dan buat request.
Kita tidak lagi mencetak data apa pun ke terminal, jadi kita tidak akan
melihat output selain output dari Cargo. Saat Anda memuat
_127.0.0.1:7878_ di web browser, Anda seharusnya mendapat halaman kosong,
bukan error. Anda baru saja menulis dengan tangan penerimaan request
HTTP dan pengiriman response!

### Mengembalikan HTML Sungguhan

Mari kita implementasikan fungsionalitas untuk mengembalikan lebih dari
sekadar halaman kosong. Buat file baru _hello.html_ di akar direktori
proyek Anda, bukan di direktori _src_. Anda bisa memasukkan HTML apa pun
yang Anda mau; Listing 21-4 menunjukkan salah satu kemungkinannya.

<Listing number="21-4" file-name="hello.html" caption="Contoh file HTML untuk dikembalikan dalam response">

```html
{{#include ../listings/ch21-web-server/listing-21-05/hello.html}}
```

</Listing>

Ini adalah dokumen HTML5 minimal dengan sebuah heading dan sedikit teks.
Untuk mengembalikan ini dari server saat sebuah request diterima, kita
akan mengubah `handle_connection` seperti yang ditunjukkan di Listing 21-5
untuk membaca file HTML itu, menambahkannya ke response sebagai isinya, dan
mengirimkannya.

<Listing number="21-5" file-name="src/main.rs" caption="Mengirim isi *hello.html* sebagai isi response">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-05/src/main.rs:here}}
```

</Listing>

Kita telah menambahkan `fs` ke statement `use` untuk membawa *module*
filesystem standard library ke dalam *scope*. Kode untuk membaca isi file
menjadi string seharusnya tampak familier; kita memakainya saat membaca isi
file untuk proyek I/O kita di Listing 12-4.

Berikutnya, kita memakai `format!` untuk menambahkan isi file itu sebagai
isi response sukses. Untuk memastikan response HTTP yang valid, kita
menambahkan header `Content-Length`, yang diatur ke ukuran isi response
kita—dalam kasus ini, ukuran `hello.html`.

Jalankan kode ini dengan `cargo run` dan muat _127.0.0.1:7878_ di peramban
Anda; Anda seharusnya melihat HTML Anda dirender!

Saat ini, kita mengabaikan data request di `http_request` dan hanya
mengirim kembali isi file HTML itu tanpa syarat. Itu berarti jika Anda
mencoba meminta _127.0.0.1:7878/something-else_ di peramban Anda, Anda
tetap akan mendapat response HTML yang sama itu. Saat ini, server kita
sangat terbatas dan tidak melakukan apa yang dilakukan sebagian besar
web server. Kita ingin menyesuaikan response kita bergantung pada
permintaannya dan hanya mengirim kembali file HTML itu untuk request
yang *well-formed* ke _/_.

### Memvalidasi Request dan Merespons Secara Selektif

Saat ini, web server kita akan mengembalikan HTML di file itu apa pun yang
diminta client. Mari kita tambahkan fungsionalitas untuk memeriksa bahwa
peramban meminta _/_ sebelum mengembalikan file HTML itu dan untuk
mengembalikan error jika peramban meminta apa pun selain itu. Untuk ini,
kita perlu mengubah `handle_connection`, seperti yang ditunjukkan di
Listing 21-6. Kode baru ini memeriksa isi request yang diterima
dibandingkan dengan apa yang kita tahu tentang tampilan request ke _/_,
dan menambahkan blok `if` dan `else` untuk memperlakukan request secara
berbeda.

<Listing number="21-6" file-name="src/main.rs" caption="Menangani request ke */* secara berbeda dari request lain">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-06/src/main.rs:here}}
```

</Listing>

Kita hanya akan melihat baris pertama dari request HTTP, jadi alih-alih
membaca seluruh request ke dalam vector, kita memanggil `next` untuk
mendapatkan item pertama dari *iterator*. `unwrap` pertama menangani
`Option` itu dan menghentikan program jika *iterator* tidak memiliki item.
`unwrap` kedua menangani `Result` dan memiliki efek yang sama dengan
`unwrap` yang ada di `map` yang ditambahkan di Listing 21-2.

Berikutnya, kita memeriksa `request_line` untuk melihat apakah ia sama
dengan request line dari request GET ke *path* _/_. Jika ya, blok `if`
mengembalikan isi file HTML kita.

Jika `request_line` *tidak* sama dengan request GET ke *path* _/_, itu
berarti kita menerima request lain. Sebentar lagi kita akan menambahkan
kode ke blok `else` untuk merespons semua request lainnya.

Jalankan kode ini sekarang dan minta _127.0.0.1:7878_; Anda seharusnya
mendapat HTML di _hello.html_. Jika Anda membuat request lain, seperti
_127.0.0.1:7878/something-else_, Anda akan mendapat error connection seperti
yang Anda lihat saat menjalankan kode di Listing 21-1 dan Listing 21-2.

Sekarang mari kita tambahkan kode di Listing 21-7 ke blok `else` untuk
mengembalikan response dengan status code 404, yang menandakan bahwa konten
untuk request itu tidak ditemukan. Kita juga akan mengembalikan
sebagian HTML untuk halaman yang dirender di peramban yang menunjukkan
response itu kepada end user.

<Listing number="21-7" file-name="src/main.rs" caption="Merespons dengan status code 404 dan halaman error jika yang diminta bukan */*">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-07/src/main.rs:here}}
```

</Listing>

Di sini, response kita memiliki status line dengan status code 404 dan
reason phrase `NOT FOUND`. Isi responsnya adalah HTML di file _404.html_.
Anda perlu membuat file _404.html_ di samping _hello.html_ untuk halaman
error itu; sekali lagi, silakan memakai HTML apa pun yang Anda mau, atau
pakai contoh HTML di Listing 21-8.

<Listing number="21-8" file-name="404.html" caption="Contoh konten untuk halaman yang dikirim bersama response 404 apa pun">

```html
{{#include ../listings/ch21-web-server/listing-21-07/404.html}}
```

</Listing>

Dengan perubahan ini, jalankan server Anda lagi. Meminta
_127.0.0.1:7878_ seharusnya mengembalikan isi _hello.html_, dan request
lain apa pun, seperti _127.0.0.1:7878/foo_, seharusnya mengembalikan HTML
error dari _404.html_.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-touch-of-refactoring"></a>

### Refactoring

Saat ini, blok `if` dan `else` memiliki banyak pengulangan: Keduanya
membaca file dan menulis isi file itu ke *stream*. Satu-satunya perbedaan
adalah status line dan nama filenya. Mari kita buat kodenya lebih ringkas
dengan menarik perbedaan-perbedaan itu keluar ke baris `if` dan `else`
terpisah yang akan menetapkan nilai status line dan nama file ke
variable; setelah itu, kita bisa memakai variable-variable itu tanpa syarat
di kode untuk membaca file dan menulis response. Listing 21-9 menunjukkan
kode yang dihasilkan setelah mengganti blok `if` dan `else` yang besar itu.

<Listing number="21-9" file-name="src/main.rs" caption="Melakukan refactoring pada blok `if` dan `else` agar hanya memuat kode yang berbeda di antara kedua kasus">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-09/src/main.rs:here}}
```

</Listing>

Sekarang blok `if` dan `else` hanya mengembalikan nilai yang sesuai untuk
status line dan nama file di dalam *tuple*; lalu kita memakai destructuring
untuk menetapkan kedua nilai itu ke `status_line` dan `filename` dengan
memakai pattern di statement `let`, seperti yang dibahas di Bab 19.

Kode yang sebelumnya diduplikasi sekarang berada di luar blok `if` dan
`else` dan memakai variable `status_line` dan `filename`. Ini membuat
perbedaan antara kedua kasus lebih mudah dilihat, dan berarti kita hanya
punya satu tempat untuk memperbarui kode jika kita ingin mengubah cara
pembacaan file dan penulisan response bekerja. Perilaku kode di Listing 21-9
akan sama dengan di Listing 21-7.

Luar biasa! Sekarang kita punya web server sederhana dalam kira-kira 40
baris kode Rust yang merespons satu request dengan halaman berisi
konten dan merespons semua request lainnya dengan response 404.

Saat ini, server kita berjalan di satu thread, yang berarti ia hanya bisa
melayani satu request pada satu waktu. Mari kita telaah bagaimana hal
itu bisa menjadi masalah dengan menyimulasikan beberapa request yang
lambat. Lalu, kita akan memperbaikinya supaya server kita bisa menangani
banyak request sekaligus.
