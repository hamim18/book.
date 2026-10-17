<a id="to-panic-or-not-to-panic"></a>
## Untuk `panic!` atau Tidak `panic!`

Jadi, bagaimana Anda memutuskan kapan sebaiknya memanggil `panic!` dan kapan
sebaiknya mengembalikan `Result`? Ketika kode panic, tidak ada cara untuk
pulih. Anda dapat memanggil `panic!` untuk situasi galat apa pun, entah ada
cara untuk pulih atau tidak, tetapi dengan begitu Anda membuat keputusan
bahwa sebuah situasi tidak dapat dipulihkan atas nama kode pemanggil. Ketika
Anda memilih mengembalikan nilai `Result`, Anda memberi kode pemanggil
pilihan-pilihan. Kode pemanggil dapat memilih untuk mencoba pulih dengan
cara yang sesuai untuk situasinya, atau dapat memutuskan bahwa nilai `Err`
dalam kasus ini tidak dapat dipulihkan, sehingga ia dapat memanggil `panic!`
dan mengubah galat yang dapat dipulihkan menjadi galat yang tidak dapat
dipulihkan. Karena itu, mengembalikan `Result` adalah pilihan default yang
baik ketika Anda mendefinisikan fungsi yang mungkin gagal.

Dalam situasi seperti contoh, kode prototipe, dan pengujian, lebih tepat
menulis kode yang panic alih-alih mengembalikan `Result`. Mari kita telusuri
alasannya, lalu membahas situasi ketika *compiler* tidak dapat mengetahui
bahwa kegagalan itu mustahil, tetapi Anda sebagai manusia bisa. Bab ini akan
ditutup dengan beberapa panduan umum tentang cara memutuskan apakah
sebaiknya panic di kode library.

### Contoh, Kode Prototipe, dan Pengujian

Ketika Anda menulis contoh untuk mengilustrasikan suatu konsep, menyertakan
juga kode penanganan galat yang tangguh dapat membuat contohnya kurang
jelas. Dalam contoh, sudah dimaklumi bahwa pemanggilan metode seperti
`unwrap` yang dapat panic dimaksudkan sebagai placeholder untuk cara Anda
ingin aplikasi Anda menangani galat, yang dapat berbeda berdasarkan apa yang
dilakukan sisa kode Anda.

Demikian pula, metode `unwrap` dan `expect` sangat praktis ketika Anda
membuat prototipe dan belum siap memutuskan cara menangani galat. Keduanya
meninggalkan penanda yang jelas di kode Anda untuk saat Anda siap membuat
program Anda lebih tangguh.

Jika pemanggilan metode gagal dalam sebuah pengujian, Anda ingin seluruh
pengujian gagal, bahkan jika metode itu bukan fungsionalitas yang sedang
diuji. Karena `panic!` adalah cara sebuah pengujian ditandai gagal,
memanggil `unwrap` atau `expect` adalah persis yang seharusnya terjadi.

<!-- Old headings. Do not remove or links may break. -->

<a id="cases-in-which-you-have-more-information-than-the-compiler"></a>

### Ketika Anda Memiliki Lebih Banyak Informasi daripada Compiler

Memanggil `expect` juga tepat ketika Anda memiliki logika lain yang menjamin
bahwa `Result` akan memiliki nilai `Ok`, tetapi logika itu bukanlah sesuatu
yang dipahami *compiler*. Anda tetap akan memiliki nilai `Result` yang perlu
Anda tangani: operasi apa pun yang Anda panggil tetap memiliki kemungkinan
gagal secara umum, meskipun secara logis mustahil dalam situasi khusus Anda.
Jika Anda dapat memastikan dengan memeriksa kode secara manual bahwa Anda
tidak akan pernah memiliki variant `Err`, sepenuhnya dapat diterima untuk
memanggil `expect` dan mendokumentasikan alasan Anda berpikir tidak akan
pernah ada variant `Err` di teks argumennya. Berikut contohnya:

```rust
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-08-unwrap-that-cant-fail/src/main.rs:here}}
```

Kita membuat instance `IpAddr` dengan mengurai string yang ditulis langsung
(hardcoded). Kita dapat melihat bahwa `127.0.0.1` adalah alamat IP yang
valid, jadi dapat diterima untuk memakai `expect` di sini. Namun, memiliki
string valid yang ditulis langsung tidak mengubah tipe kembalian metode
`parse`: kita tetap mendapat nilai `Result`, dan *compiler* tetap mengharuskan
kita menangani `Result` itu seolah-olah variant `Err` adalah sebuah
kemungkinan karena *compiler* tidak cukup pintar untuk melihat bahwa string
ini selalu merupakan alamat IP yang valid. Jika string alamat IP berasal
dari pengguna alih-alih ditulis langsung ke dalam program dan karena itu
_memang_ memiliki kemungkinan gagal, kita tentu ingin menangani `Result` itu
dengan cara yang lebih tangguh. Menyebutkan asumsi bahwa alamat IP ini
ditulis langsung akan mendorong kita mengubah `expect` menjadi kode
penanganan galat yang lebih baik jika, di masa depan, kita perlu mendapatkan
alamat IP dari sumber lain.

<a id="guidelines-for-error-handling"></a>
### Panduan untuk Penanganan Galat

Disarankan agar kode Anda panic ketika ada kemungkinan kode Anda berakhir
dalam keadaan yang buruk. Dalam konteks ini, *bad state* (keadaan yang
buruk) adalah ketika suatu asumsi, jaminan, kontrak, atau invarian telah
dilanggar, seperti ketika nilai yang tidak valid, nilai yang kontradiktif,
atau nilai yang hilang diteruskan ke kode Anda—ditambah satu atau lebih hal
berikut:

- Keadaan yang buruk itu adalah sesuatu yang tidak diharapkan, alih-alih
  sesuatu yang mungkin sesekali terjadi, seperti pengguna memasukkan data
  dengan format yang salah.
- Kode Anda setelah titik ini perlu mengandalkan tidak berada dalam keadaan
  yang buruk ini, alih-alih memeriksa masalahnya di setiap langkah.
- Tidak ada cara yang baik untuk menyandikan informasi ini di tipe yang Anda
  pakai. Kita akan menelusuri contoh tentang apa yang kami maksud di
  [“Menyandikan State dan Perilaku sebagai Tipe”][encoding]<!-- ignore --> di
  Bab 18.

Jika seseorang memanggil kode Anda dan meneruskan nilai yang tidak masuk
akal, sebaiknya kembalikan galat jika Anda bisa supaya pengguna library
dapat memutuskan apa yang ingin mereka lakukan dalam kasus itu. Namun,
dalam kasus ketika melanjutkan dapat menjadi tidak aman atau berbahaya,
pilihan terbaik mungkin adalah memanggil `panic!` dan memperingatkan orang
yang memakai library Anda tentang bug di kode mereka supaya mereka dapat
memperbaikinya selama pengembangan. Demikian pula, `panic!` sering tepat
jika Anda memanggil kode eksternal yang berada di luar kendali Anda dan
mengembalikan state yang tidak valid yang tidak dapat Anda perbaiki.

Namun, ketika kegagalan itu diharapkan, lebih tepat mengembalikan `Result`
daripada melakukan pemanggilan `panic!`. Contohnya termasuk parser yang
diberi data yang cacat atau permintaan HTTP yang mengembalikan status yang
mengindikasikan Anda telah melampaui batas laju (rate limit). Dalam
kasus-kasus ini, mengembalikan `Result` mengindikasikan bahwa kegagalan
adalah kemungkinan yang diharapkan yang harus diputuskan cara
penanganannya oleh kode pemanggil.

Ketika kode Anda melakukan operasi yang dapat membahayakan pengguna jika
dipanggil memakai nilai yang tidak valid, kode Anda sebaiknya memverifikasi
nilai-nilainya valid terlebih dahulu dan panic jika nilainya tidak valid.
Ini terutama demi alasan keamanan: mencoba beroperasi pada data yang tidak
valid dapat mengekspos kode Anda terhadap kerentanan. Inilah alasan utama
pustaka standar memanggil `panic!` jika Anda mencoba akses memori di luar
batas: mencoba mengakses memori yang bukan milik struktur data saat ini
adalah masalah keamanan yang umum. Fungsi sering memiliki _kontrak_:
perilakunya hanya dijamin jika masukannya memenuhi persyaratan tertentu.
Panic ketika kontrak dilanggar masuk akal karena pelanggaran kontrak selalu
mengindikasikan bug di sisi pemanggil, dan itu bukan jenis galat yang Anda
ingin kode pemanggilnya tangani secara eksplisit. Kenyataannya, tidak ada
cara yang masuk akal bagi kode pemanggil untuk pulih; para _pemrogram_
pemanggil yang perlu memperbaiki kodenya. Kontrak untuk sebuah fungsi,
terutama ketika pelanggarannya akan menyebabkan panic, sebaiknya dijelaskan
di dokumentasi API fungsi tersebut.

Namun, memiliki banyak pemeriksaan galat di semua fungsi Anda akan
bertele-tele dan menjengkelkan. Untungnya, Anda dapat memakai sistem tipe
Rust (dan dengan demikian pemeriksaan tipe yang dilakukan *compiler*) untuk
melakukan banyak pemeriksaan itu untuk Anda. Jika fungsi Anda memiliki tipe
tertentu sebagai parameter, Anda dapat melanjutkan logika kode Anda dengan
mengetahui bahwa *compiler* telah memastikan Anda memiliki nilai yang valid.
Misalnya, jika Anda memiliki sebuah tipe alih-alih `Option`, program Anda
mengharapkan memiliki _sesuatu_ alih-alih _tidak ada apa-apa_. Kode Anda
kemudian tidak harus menangani dua kasus untuk variant `Some` dan `None`: ia
hanya akan memiliki satu kasus untuk pasti memiliki nilai. Kode yang mencoba
meneruskan tidak ada apa-apa ke fungsi Anda bahkan tidak akan terkompilasi,
jadi fungsi Anda tidak perlu memeriksa kasus itu pada runtime. Contoh lain
adalah memakai tipe bilangan bulat tak bertanda seperti `u32`, yang
menjamin parameter tidak pernah negatif.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-custom-types-for-validation"></a>

### Tipe Kustom untuk Validasi

Mari kita bawa gagasan memakai sistem tipe Rust untuk memastikan kita
memiliki nilai yang valid selangkah lebih jauh dan melihat pembuatan tipe
kustom untuk validasi. Ingat permainan tebak angka di Bab 2 ketika kode kita
meminta pengguna menebak angka antara 1 dan 100. Kita tidak pernah
memvalidasi bahwa tebakan pengguna berada di antara angka-angka itu sebelum
memeriksanya terhadap angka rahasia kita; kita hanya memvalidasi bahwa
tebakannya positif. Dalam kasus ini, konsekuensinya tidak terlalu parah:
output kita “Too high” atau “Too low” akan tetap benar. Tetapi akan menjadi
penyempurnaan yang berguna untuk mengarahkan pengguna ke tebakan yang valid
dan berperilaku berbeda ketika pengguna menebak angka di luar jangkauan
dibandingkan ketika pengguna mengetik, misalnya, huruf.

Salah satu caranya adalah mengurai tebakan sebagai `i32`, bukan hanya `u32`,
untuk mengizinkan angka negatif yang mungkin, lalu menambahkan pemeriksaan
bahwa angkanya berada dalam jangkauan, seperti ini:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-09-guess-out-of-range/src/main.rs:here}}
```

</Listing>

Ekspresi `if` memeriksa apakah nilai kita di luar jangkauan, memberi tahu
pengguna tentang masalahnya, dan memanggil `continue` untuk memulai iterasi
perulangan berikutnya dan meminta tebakan lain. Setelah ekspresi `if`, kita
dapat melanjutkan perbandingan antara `guess` dan angka rahasia dengan
mengetahui bahwa `guess` berada antara 1 dan 100.

Namun, ini bukan solusi yang ideal: jika benar-benar krusial bahwa program
hanya beroperasi pada nilai antara 1 dan 100, dan program memiliki banyak
fungsi dengan persyaratan ini, memiliki pemeriksaan seperti ini di setiap
fungsi akan melelahkan (dan mungkin memengaruhi kinerja).

Sebagai gantinya, kita dapat membuat tipe baru di *module* khusus dan menaruh
validasinya di fungsi untuk membuat instance tipe itu alih-alih mengulang
validasinya di mana-mana. Dengan begitu, aman bagi fungsi untuk memakai tipe
baru di tanda tangannya dan dengan yakin memakai nilai yang diterimanya.
Listing 9-13 menunjukkan salah satu cara mendefinisikan tipe `Guess` yang
hanya akan membuat instance `Guess` jika fungsi `new` menerima nilai antara
1 dan 100.

<Listing number="9-13" caption="Tipe `Guess` yang hanya akan berlanjut dengan nilai antara 1 dan 100" file-name="src/guessing_game.rs">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-13/src/guessing_game.rs}}
```

</Listing>

Perhatikan bahwa kode di *src/guessing_game.rs* ini bergantung pada
penambahan deklarasi *module* `mod guessing_game;` di *src/lib.rs* yang belum
kita tampilkan di sini. Di dalam file *module* baru ini, kita mendefinisikan
*struct* bernama `Guess` yang memiliki *field* bernama `value` yang memegang
`i32`. Di sinilah angkanya akan disimpan.

Lalu, kita mengimplementasikan *associated function* (fungsi asosiasi)
bernama `new` pada `Guess` yang membuat instance nilai `Guess`. Fungsi `new`
didefinisikan memiliki satu parameter bernama `value` bertipe `i32` dan
mengembalikan `Guess`. Kode di badan fungsi `new` menguji `value` untuk
memastikan ia berada antara 1 dan 100. Jika `value` tidak lulus uji ini,
kita melakukan pemanggilan `panic!`, yang akan memperingatkan pemrogram yang
menulis kode pemanggil bahwa mereka memiliki bug yang perlu diperbaiki,
karena membuat `Guess` dengan `value` di luar jangkauan ini akan melanggar
kontrak yang diandalkan `Guess::new`. Kondisi ketika `Guess::new` mungkin
panic sebaiknya dibahas di dokumentasi API yang menghadap publik; kita akan
membahas konvensi dokumentasi yang mengindikasikan kemungkinan `panic!` di
dokumentasi API yang Anda buat di Bab 14. Jika `value` lulus uji, kita
membuat `Guess` baru dengan *field* `value`-nya ditetapkan ke parameter
`value` dan mengembalikan `Guess` itu.

Berikutnya, kita mengimplementasikan metode bernama `value` yang meminjam
`self`, tidak memiliki parameter lain, dan mengembalikan `i32`. Metode
semacam ini kadang disebut *getter* karena tujuannya adalah mengambil
sebagian data dari *field*-fieldnya dan mengembalikannya. Metode publik ini
diperlukan karena *field* `value` dari *struct* `Guess` bersifat privat. Penting
bahwa *field* `value` privat sehingga kode yang memakai *struct* `Guess` tidak
diizinkan menetapkan `value` secara langsung: kode di luar *module*
`guessing_game` _harus_ memakai fungsi `Guess::new` untuk membuat instance
`Guess`, sehingga terjamin tidak ada cara bagi `Guess` untuk memiliki
`value` yang belum diperiksa oleh kondisi-kondisi di fungsi `Guess::new`.

Sebuah fungsi yang memiliki parameter atau hanya mengembalikan angka antara
1 dan 100 kemudian dapat menyatakan di tanda tangannya bahwa ia menerima
atau mengembalikan `Guess` alih-alih `i32` dan tidak perlu melakukan
pemeriksaan tambahan apa pun di badannya.

## Ringkasan

Fitur penanganan galat Rust dirancang untuk membantu Anda menulis kode yang
lebih tangguh. *Macro* `panic!` menandakan bahwa program Anda berada dalam
state yang tidak dapat ditanganinya dan memungkinkan Anda menyuruh
prosesnya berhenti alih-alih mencoba melanjutkan dengan nilai yang tidak
valid atau tidak benar. *Enum* `Result` memakai sistem tipe Rust untuk
mengindikasikan bahwa operasi mungkin gagal dengan cara yang dapat
dipulihkan kode Anda. Anda dapat memakai `Result` untuk memberi tahu kode
yang memanggil kode Anda bahwa ia juga perlu menangani kemungkinan sukses
atau gagal. Memakai `panic!` dan `Result` pada situasi yang tepat akan
membuat kode Anda lebih andal dalam menghadapi masalah yang tak
terhindarkan.

Setelah Anda melihat cara-cara bermanfaat pustaka standar memakai *generics*
dengan *enum* `Option` dan `Result`, kita akan membicarakan cara kerja
*generics* dan cara Anda dapat memakainya di kode Anda.

[encoding]: ch18-03-oo-design-patterns.html#encoding-states-and-behavior-as-types
