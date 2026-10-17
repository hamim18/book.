## Lampiran G: Bagaimana Rust Dibuat dan “Nightly Rust”

Lampiran ini membahas bagaimana Rust dibuat dan bagaimana hal itu memengaruhi
Anda sebagai pengembang Rust.

### Stabilitas Tanpa Stagnasi

Sebagai sebuah bahasa, Rust sangat _memperhatikan_ stabilitas kode Anda. Kami
ingin Rust menjadi fondasi yang kokoh untuk Anda bangun, dan jika segala
sesuatunya terus berubah, hal itu mustahil terwujud. Pada saat yang sama, jika
kami tidak dapat bereksperimen dengan fitur baru, kami mungkin baru menemukan
kelemahan penting setelah fitur itu dirilis, saat kami tidak bisa lagi mengubah
apa pun.

Solusi kami untuk masalah ini adalah apa yang kami sebut “stabilitas tanpa
stagnasi”, dan prinsip panduan kami adalah ini: Anda tidak perlu takut
meningkatkan ke versi baru Rust stable. Setiap peningkatan seharusnya tidak
menyakitkan, tetapi juga memberi Anda fitur baru, lebih sedikit bug, dan waktu
kompilasi yang lebih cepat.

### Choo, Choo! Saluran Rilis dan Menumpangi Kereta

Pengembangan Rust berjalan menurut _jadwal kereta_. Artinya, semua pengembangan
dilakukan di branch main repositori Rust. Rilis mengikuti model kereta rilis
perangkat lunak, yang telah dipakai oleh Cisco IOS dan proyek perangkat lunak
lainnya. Ada tiga *release channel* (saluran rilis) untuk Rust:

- Nightly
- Beta
- Stable

Sebagian besar pengembang Rust terutama memakai saluran stable, tetapi mereka
yang ingin mencoba fitur eksperimental baru boleh memakai nightly atau beta.

Berikut contoh cara kerja proses pengembangan dan rilis: anggaplah tim Rust
sedang mengerjakan rilis Rust 1.5. Rilis itu terjadi pada Desember 2015, tetapi
akan memberi kita nomor versi yang realistis. Sebuah fitur baru ditambahkan ke
Rust: commit baru masuk ke branch main. Setiap malam, versi nightly Rust yang
baru diproduksi. Setiap hari adalah hari rilis, dan rilis-rilis ini dibuat oleh
infrastruktur rilis kami secara otomatis. Jadi, seiring berjalannya waktu,
rilis kami tampak seperti ini, sekali setiap malam:

```text
nightly: * - - * - - *
```

Setiap enam minggu, tiba saatnya menyiapkan rilis baru! Branch `beta` repositori
Rust bercabang dari branch main yang dipakai nightly. Sekarang, ada dua rilis:

```text
nightly: * - - * - - *
                     |
beta:                *
```

Sebagian besar pengguna Rust tidak memakai rilis beta secara aktif, tetapi
menguji terhadap beta di sistem CI mereka untuk membantu Rust menemukan
kemungkinan regresi. Sementara itu, masih ada rilis nightly setiap malam:

```text
nightly: * - - * - - * - - * - - *
                     |
beta:                *
```

Katakanlah sebuah regresi ditemukan. Untungnya kita sempat menguji rilis beta
sebelum regresi itu menyelinap ke rilis stable! Perbaikan diterapkan ke branch
main, sehingga nightly diperbaiki, lalu perbaikan itu di-backport ke branch
`beta`, dan rilis beta baru diproduksi:

```text
nightly: * - - * - - * - - * - - * - - *
                     |
beta:                * - - - - - - - - *
```

Enam minggu setelah beta pertama dibuat, tiba saatnya rilis stable! Branch
`stable` dihasilkan dari branch `beta`:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |
beta:                * - - - - - - - - *
                                       |
stable:                                *
```

Hore! Rust 1.5 selesai! Namun, kita lupa satu hal: karena enam minggu telah
berlalu, kita juga butuh beta baru untuk versi Rust _berikutnya_, 1.6. Jadi,
setelah `stable` bercabang dari `beta`, versi `beta` berikutnya bercabang lagi
dari `nightly`:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

Ini disebut “model kereta” karena setiap enam minggu, sebuah rilis “berangkat
dari stasiun”, tetapi masih harus menempuh perjalanan melalui saluran beta
sebelum tiba sebagai rilis stable.

Rust merilis setiap enam minggu, seperti jarum jam. Jika Anda tahu tanggal salah
satu rilis Rust, Anda bisa tahu tanggal rilis berikutnya: enam minggu kemudian.
Aspek menyenangkan dari rilis yang dijadwalkan setiap enam minggu adalah kereta
berikutnya segera datang. Jika sebuah fitur kebetulan melewatkan rilis tertentu,
tidak perlu khawatir: rilis berikutnya akan segera tiba! Ini membantu mengurangi
tekanan untuk menyelundupkan fitur yang mungkin belum sempurna menjelang tenggat
rilis.

Berkat proses ini, Anda selalu dapat memeriksa build Rust berikutnya dan
membuktikan sendiri bahwa peningkatannya mudah: jika rilis beta tidak berjalan
seperti yang diharapkan, Anda dapat melaporkannya ke tim dan mendapat perbaikan
sebelum rilis stable berikutnya terjadi! Kerusakan pada rilis beta relatif
jarang, tetapi `rustc` tetaplah sebuah perangkat lunak, dan bug memang ada.

### Waktu Pemeliharaan

Proyek Rust mendukung versi stable terbaru. Ketika versi stable baru dirilis,
versi lama mencapai akhir masa pakainya (end of life, EOL). Artinya, setiap
versi didukung selama enam minggu.

### Unstable Features

Ada satu lagi hal yang perlu diperhatikan dengan model rilis ini: fitur yang
tidak stabil. Rust memakai teknik yang disebut “feature flag” untuk menentukan
fitur apa saja yang diaktifkan pada rilis tertentu. Jika fitur baru sedang
dalam pengembangan aktif, fitur itu masuk ke branch main, dan karena itu juga
ke nightly, tetapi di balik _feature flag_. Jika Anda, sebagai pengguna, ingin
mencoba fitur yang masih dalam pengerjaan itu, Anda boleh melakukannya, tetapi
Anda harus memakai rilis nightly Rust dan memberi anotasi pada kode sumber Anda
dengan flag yang sesuai untuk ikut serta.

Jika Anda memakai rilis beta atau stable dari Rust, Anda tidak dapat memakai
feature flag apa pun. Inilah kuncinya yang memungkinkan kita mendapatkan
pemakaian praktis fitur-fitur baru sebelum kita menyatakannya stable selamanya.
Mereka yang ingin ikut di garis terdepan boleh melakukannya, dan mereka yang
menginginkan pengalaman yang kokoh dapat bertahan di stable dan yakin bahwa
kode mereka tidak akan rusak. Stabilitas tanpa stagnasi.

Buku ini hanya memuat informasi tentang fitur stable, karena fitur yang masih
dalam pengerjaan masih terus berubah, dan tentu saja fitur itu akan berbeda
antara saat buku ini ditulis dan saat fitur itu diaktifkan di build stable. Anda
dapat menemukan dokumentasi fitur-fitur yang hanya ada di nightly secara daring.

### Rustup dan Peran Rust Nightly

Rustup memudahkan perpindahan antara saluran rilis Rust yang berbeda, baik
secara global maupun per proyek. Secara bawaan, Anda akan memasang Rust stable.
Untuk memasang nightly, misalnya:

```console
$ rustup toolchain install nightly
```

Anda juga dapat melihat semua *toolchain* (rantai alat, yaitu rilis Rust beserta
komponen terkaitnya) yang terpasang dengan `rustup`. Berikut contohnya di
komputer Windows salah satu penulis buku ini:

```powershell
> rustup toolchain list
stable-x86_64-pc-windows-msvc (default)
beta-x86_64-pc-windows-msvc
nightly-x86_64-pc-windows-msvc
```

Seperti yang Anda lihat, toolchain stable adalah bawaannya. Sebagian besar
pengguna Rust memakai stable hampir sepanjang waktu. Anda mungkin ingin memakai
stable hampir sepanjang waktu, tetapi memakai nightly pada proyek tertentu,
karena Anda menginginkan fitur yang paling mutakhir. Untuk melakukannya, Anda
dapat memakai `rustup override` di direktori proyek itu untuk menetapkan
toolchain nightly sebagai yang harus dipakai `rustup` ketika Anda berada di
direktori itu:

```console
$ cd ~/projects/needs-nightly
$ rustup override set nightly
```

Sekarang, setiap kali Anda memanggil `rustc` atau `cargo` di dalam
_~/projects/needs-nightly_, `rustup` akan memastikan bahwa Anda memakai Rust
nightly, bukan stable yang menjadi bawaan Anda. Ini sangat berguna ketika Anda
punya banyak proyek Rust!

### Proses RFC dan Tim

Lalu, bagaimana Anda mengetahui fitur-fitur baru ini? Model pengembangan Rust
mengikuti *Request For Comments* (RFC). Jika Anda menginginkan peningkatan pada
Rust, Anda dapat menulis proposal yang disebut RFC.

Siapa pun dapat menulis RFC untuk meningkatkan Rust, dan proposal itu ditinjau
serta didiskusikan oleh tim Rust, yang terdiri atas banyak subtim berdasarkan
topik. Ada daftar lengkap tim-tim itu [di situs web
Rust](https://www.rust-lang.org/governance), yang mencakup tim untuk setiap
bidang proyek: desain bahasa, implementasi kompilator, infrastruktur,
dokumentasi, dan lain-lain. Tim yang sesuai membaca proposal dan
komentar-komentarnya, menulis beberapa komentar sendiri, dan pada akhirnya,
tercapai konsensus untuk menerima atau menolak fitur tersebut.

Jika fitur itu diterima, sebuah issue dibuka di repositori Rust, dan seseorang
dapat mengimplementasikannya. Orang yang mengimplementasikannya dengan sangat
baik boleh jadi bukan orang yang pertama kali mengusulkan fitur itu! Ketika
implementasinya siap, implementasi itu masuk ke branch main di balik feature
gate, seperti yang kita bahas di bagian [“Unstable
Features”](#unstable-features)<!-- ignore -->.

Setelah beberapa waktu, setelah para pengembang Rust yang memakai rilis nightly
sempat mencoba fitur baru itu, anggota tim akan mendiskusikan fitur tersebut,
bagaimana hasilnya di nightly, dan memutuskan apakah fitur itu layak masuk ke
Rust stable atau tidak. Jika keputusannya adalah melanjutkan, feature gate-nya
dihapus, dan fitur itu kini dianggap stable! Fitur itu menumpangi kereta menuju
rilis stable Rust yang baru.
