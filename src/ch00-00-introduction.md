# Pendahuluan

> Catatan: Edition buku ini sama dengan [The Rust Programming Language][nsprust]
> yang tersedia dalam format cetak dan ebook dari [No Starch Press][nsp].

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

Selamat datang di _The Rust Programming Language_, sebuah buku pengantar
tentang Rust. Bahasa pemrograman Rust membantu Anda menulis perangkat lunak
yang lebih cepat dan lebih andal. Ergonomi tingkat tinggi dan kendali tingkat
rendah sering kali saling bertentangan dalam desain bahasa pemrograman; Rust
menantang pertentangan itu. Dengan menyeimbangkan capacity teknis yang kuat
dan pengalaman pengembang yang hebat, Rust memberi Anda pilihan untuk
mengendalikan detail-detail tingkat rendah (seperti penggunaan memori) tanpa
semua kerepotan yang biasanya melekat pada kendali semacam itu.

## Untuk Siapa Rust Ditujukan

Rust ideal untuk banyak orang karena berbagai alasan. Mari kita lihat
beberapa kelompok yang paling penting.

### Tim Pengembang

Rust terbukti menjadi tool yang produktif untuk berkolaborasi dalam tim
besar pengembang dengan tingkat pengetahuan pemrograman sistem yang beragam.
Kode tingkat rendah rentan terhadap berbagai bug yang halus, yang di sebagian
besar bahasa lain hanya dapat ditemukan melalui test yang ekstensif dan
peninjauan kode yang cermat oleh pengembang berpengalaman. Di Rust, *compiler*
(*compiler*) berperan sebagai penjaga gerbang dengan menolak mengompilasi
kode yang mengandung bug-bug yang sulit ditemukan ini, termasuk bug
concurrency. Dengan bekerja berdampingan dengan *compiler*, tim dapat
menghabiskan waktunya untuk berfokus pada logika program alih-alih mengejar
bug.

Rust juga membawa tool-tool pengembang yang modern ke dunia pemrograman
sistem:

- Cargo, dependency manager dan tool build bawaan, membuat proses
  menambah, mengompilasi, dan mengelola dependency menjadi mudah dan
  konsisten di seluruh ekosistem Rust.
- Tool pemformatan `rustfmt` menjamin gaya penulisan kode yang konsisten
  di antara para pengembang.
- Rust Language Server mendukung integrasi lingkungan pengembangan terpadu
  (IDE) untuk pelengkapan kode dan pesan error sebaris.

Dengan menggunakan tool-tool ini dan tool-tool lain di ekosistem Rust, para
pengembang dapat tetap produktif saat menulis kode tingkat sistem.

### Pelajar

Rust ditujukan bagi para pelajar dan mereka yang tertarik mempelajari
konsep-konsep sistem. Dengan memakai Rust, banyak orang telah mempelajari
topik seperti pengembangan sistem operasi. Komunitasnya sangat ramah dan
senang menjawab pertanyaan para pelajar. Melalui berbagai upaya seperti buku
ini, tim-tim Rust ingin membuat konsep-konsep sistem lebih mudah diakses oleh
lebih banyak orang, terutama mereka yang baru mengenal pemrograman.

### Perusahaan

Ratusan perusahaan, besar maupun kecil, menggunakan Rust di lingkungan
produksi untuk berbagai macam tugas, termasuk tool command line, layanan
web, perangkat DevOps, perangkat tertanam, analisis dan transkode audio dan
video, mata uang kripto, bioinformatika, mesin pencari, aplikasi Internet of
Things, machine learning, dan bahkan bagian-bagian utama web browser Firefox.

### Pengembang Open Source

Rust ditujukan bagi orang-orang yang ingin membangun bahasa pemrograman Rust,
komunitas, tool pengembang, dan pustakanya. Kami akan sangat senang jika Anda
berkontribusi pada bahasa Rust.

### Orang yang Menghargai Kecepatan dan Stabilitas

Rust ditujukan bagi orang-orang yang mendambakan kecepatan dan stabilitas
dalam sebuah bahasa. Yang kita maksud dengan kecepatan adalah seberapa cepat
kode Rust dapat berjalan sekaligus seberapa cepat Rust memungkinkan Anda
menulis program. Pemeriksaan *compiler* Rust menjamin stabilitas ketika
fitur-fitur ditambahkan dan ketika dilakukan refactoring. Hal ini bertolak
belakang dengan kode warisan yang rapuh pada bahasa-bahasa tanpa pemeriksaan
semacam itu, yang sering kali ditakuti para pengembang untuk dimodifikasi.
Dengan mengupayakan *zero-cost abstraction* (abstraksi tanpa biaya)—fitur
tingkat tinggi yang dikompilasi menjadi kode tingkat rendah secepat kode yang
ditulis secara manual—Rust berusaha menjadikan kode yang aman sekaligus kode
yang cepat.

Bahasa Rust juga berharap dapat mendukung banyak pengguna lainnya; mereka
yang disebutkan di sini hanyalah sebagian dari pemangku kepentingan
terbesar. Secara keseluruhan, ambisi terbesar Rust adalah menghilangkan
kompromi-kompromi yang telah diterima para programmer selama puluhan tahun
dengan menyediakan keamanan _dan_ produktivitas, kecepatan _dan_ ergonomi.
Cobalah Rust, dan lihat apakah pilihan-pilihannya cocok untuk Anda.

## Untuk Siapa Buku Ini Ditujukan

Buku ini mengasumsikan bahwa Anda pernah menulis kode dalam bahasa
pemrograman lain, tetapi tidak mengasumsikan bahasa yang mana. Kami berusaha
membuat materi ini mudah diakses secara luas oleh orang-orang dari berbagai
macam latar belakang pemrograman. Kami tidak menghabiskan banyak waktu untuk
membahas apa itu pemrograman atau bagaimana cara memikirkannya. Jika Anda
benar-benar baru dalam dunia pemrograman, akan lebih baik bagi Anda untuk
membaca buku yang secara khusus memberikan pengantar pemrograman.

## Cara Menggunakan Buku Ini

Secara umum, buku ini mengasumsikan bahwa Anda membacanya secara berurutan
dari depan ke belakang. Bab-bab selanjutnya dibangun di atas konsep-konsep
dari bab-bab sebelumnya, dan bab-bab awal mungkin tidak mendalami detail
suatu topik tertentu, tetapi topik tersebut akan ditinjau kembali di bab
selanjutnya.

Anda akan menemukan dua jenis bab dalam buku ini: bab konsep dan bab proyek.
Di bab konsep, Anda akan mempelajari salah satu aspek dari Rust. Di bab
proyek, kita akan membangun program-program kecil bersama-sama dengan
menerapkan apa yang telah Anda pelajari sejauh ini. Bab 2, Bab 12, dan Bab 21
adalah bab proyek; sisanya adalah bab konsep.

**Bab 1** menjelaskan cara memasang Rust, cara menulis program
“Hello, world!”, dan cara menggunakan Cargo, pengelola *package* (paket) dan
tool build milik Rust. **Bab 2** adalah pengantar langsung untuk menulis
program di Rust, dengan mengajak Anda membangun permainan tebak angka. Di
sini, kita membahas konsep-konsep pada tingkat tinggi, dan bab-bab
selanjutnya akan memberikan detail tambahan. Jika Anda ingin langsung terjun
praktik, Bab 2 adalah tempatnya. Jika Anda adalah pembelajar yang sangat
teliti dan lebih suka mempelajari setiap detail sebelum melanjutkan ke bagian
berikutnya, Anda mungkin ingin melewati Bab 2 dan langsung menuju **Bab 3**,
yang membahas fitur-fitur Rust yang serupa dengan bahasa pemrograman lain;
setelah itu, Anda dapat kembali ke Bab 2 saat ingin mengerjakan sebuah proyek
dengan menerapkan detail-detail yang telah Anda pelajari.

Di **Bab 4**, Anda akan mempelajari sistem *ownership* (kepemilikan) Rust.
**Bab 5** membahas *struct* dan method. **Bab 6** membahas *enum*, expression
`match`, serta konstruksi control flow `if let` dan `let...else`. Anda akan
menggunakan *struct* dan *enum* untuk membuat type khusus.

Di **Bab 7**, Anda akan mempelajari sistem *module* (modul) Rust serta
aturan privasi untuk mengorganisasi kode Anda dan antarmuka pemrograman
aplikasi (API) publiknya. **Bab 8** membahas beberapa struktur data collection
umum yang disediakan standard library: vector, string, dan hash map. **Bab 9**
menjelajahi filosofi dan teknik penanganan error Rust.

**Bab 10** menggali *generics* (tipe generik), *trait*, dan *lifetime* (masa
hidup), yang memberi Anda kemampuan untuk mendefinisikan kode yang berlaku
untuk berbagai type. **Bab 11** seluruhnya membahas test, yang bahkan
dengan jaminan keamanan dari Rust tetap diperlukan untuk memastikan logika
program Anda benar. Di **Bab 12**, kita akan membangun implementasi sendiri
dari sebagian fungsionalitas tool command line `grep` yang mencari teks di
dalam file. Untuk itu, kita akan memakai banyak konsep yang telah kita bahas
di bab-bab sebelumnya.

**Bab 13** menjelajahi *closure* dan *iterator*: fitur Rust yang berasal
dari bahasa functional programming. Di **Bab 14**, kita akan menelaah Cargo
lebih mendalam dan membahas praktik terbaik untuk membagikan pustaka Anda
kepada orang lain. **Bab 15** membahas *smart pointer* (*pointer* pintar) yang
disediakan standard library dan *trait* yang memungkinkan fungsionalitasnya.

Di **Bab 16**, kita akan menelusuri berbagai model concurrent programming dan
membahas bagaimana Rust membantu Anda memprogram dengan banyak thread tanpa
rasa takut. Di **Bab 17**, kita melanjutkannya dengan menjelajahi sintaks
async dan await Rust, bersama *task*, *future*, dan *stream*, serta model
concurrency ringan yang dimungkinkan oleh ketiganya.

**Bab 18** membahas bagaimana idiom-idiom Rust dibandingkan dengan
prinsip-prinsip object-oriented programming yang mungkin sudah Anda kenal.
**Bab 19** adalah *reference* tentang pattern dan *pattern matching* (pencocokan
pattern), yang merupakan cara ampuh untuk mengekspresikan gagasan di seluruh
program Rust. **Bab 20** memuat aneka ragam topik lanjutan yang menarik,
termasuk *unsafe* Rust, *macro* (makro), serta pembahasan lebih lanjut
tentang *lifetime*, *trait*, type, fungsi, dan *closure*.

Di **Bab 21**, kita akan menyelesaikan sebuah proyek untuk
mengimplementasikan web server multithread tingkat rendah!

Terakhir, beberapa lampiran memuat informasi berguna tentang bahasa ini
dalam format yang lebih menyerupai *reference*. **Lampiran A** membahas kata
kunci Rust, **Lampiran B** membahas operator dan simbol Rust, **Lampiran C**
membahas *trait* yang dapat diturunkan yang disediakan standard library,
**Lampiran D** membahas beberapa tool pengembangan yang berguna, dan
**Lampiran E** menjelaskan edition Rust. Di **Lampiran F**, Anda dapat
menemukan terjemahan buku ini, dan di **Lampiran G** kita akan membahas
bagaimana Rust dibuat dan apa itu Rust nightly.

Tidak ada cara yang salah untuk membaca buku ini: jika Anda ingin melompat
ke depan, silakan saja! Anda mungkin perlu melompat kembali ke bab-bab
sebelumnya jika mengalami kebingungan. Namun, lakukan apa pun yang paling
cocok untuk Anda.

<span id="ferris"></span>

Bagian penting dari proses belajar Rust adalah belajar membaca pesan error
yang ditampilkan *compiler*: pesan-pesan ini akan memandu Anda menuju kode
yang berfungsi. Karena itu, kita akan memberikan banyak contoh yang tidak
terkompilasi beserta pesan error yang akan ditampilkan *compiler* pada setiap
situasi. Perlu Anda ketahui bahwa jika Anda mengetik dan menjalankan sebuah
contoh secara acak, contoh tersebut mungkin tidak terkompilasi! Pastikan Anda
membaca teks di sekitarnya untuk melihat apakah contoh yang coba Anda
jalankan memang sengaja dibuat agar menghasilkan error. Pada kebanyakan
situasi, kita akan memandu Anda ke versi yang benar dari setiap kode yang
tidak terkompilasi. Ferris juga akan membantu Anda membedakan kode yang
memang tidak dimaksudkan untuk berfungsi:

| Ferris                                                                                                                                                                                                                                             | Makna                                                    |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris dengan tanda tanya"/>                                                                                                                                                | Kode ini tidak terkompilasi!                             |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris mengangkat kedua tangannya"/>                                                                                                                                                  | Kode ini memicu panic!                                   |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris dengan satu capit terangkat sambil mengangkat bahu"/>                                                                                                             | Kode ini tidak menghasilkan perilaku yang diinginkan. |

Pada kebanyakan situasi, kita akan memandu Anda ke versi yang benar dari
setiap kode yang tidak terkompilasi.

## Kode Sumber

File-source file yang digunakan untuk menghasilkan buku ini dapat ditemukan
di [GitHub][book].

[book]: https://github.com/rust-lang/book/tree/main/src
