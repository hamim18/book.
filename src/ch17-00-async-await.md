# Dasar-Dasar Pemrograman Asinkron: Async, Await, Futures, dan Streams

Banyak operasi yang kita minta komputer lakukan bisa memakan waktu cukup lama
untuk selesai. Alangkah baiknya bila kita bisa mengerjakan hal lain selagi
menunggu proses-proses yang berjalan lama itu selesai. Komputer modern
menawarkan dua teknik untuk mengerjakan lebih dari satu operasi pada satu
waktu: paralelisme dan konkurensi. Namun, logika program kita kebanyakan
ditulis secara linear. Kita ingin bisa menentukan operasi-operasi yang harus
dijalankan sebuah program serta titik-titik ketika sebuah fungsi bisa berhenti
sejenak dan bagian lain program bisa berjalan menggantikannya, tanpa perlu
menentukan di muka urutan dan cara setiap potongan kode dijalankan secara
persis. Pemrograman asinkron adalah abstraksi yang memungkinkan kita
mengekspresikan kode dalam bentuk titik-titik yang mungkin dijeda dan hasil
yang pada akhirnya diperoleh, sambil mengurus detail koordinasinya untuk kita.

Bab ini melanjutkan pemakaian thread untuk paralelisme dan konkurensi di Bab 16
dengan memperkenalkan pendekatan alternatif dalam menulis kode: *futures*,
*streams*, dan sintaks `async` serta `await` dari Rust yang memungkinkan kita
mengekspresikan bagaimana sebuah operasi bisa berjalan asinkron, berikut
*crate*-crate pihak ketiga yang mengimplementasikan runtime asinkron: kode yang
mengelola dan mengoordinasikan eksekusi operasi-operasi asinkron.

Mari kita lihat sebuah contoh. Katakan Anda sedang mengekspor video perayaan
keluarga yang Anda buat, sebuah operasi yang bisa memakan waktu dari beberapa
menit hingga berjam-jam. Ekspor video itu akan memakai daya CPU dan GPU
sebanyak mungkin. Jika Anda hanya punya satu inti CPU dan sistem operasi Anda
tidak menjeda ekspor itu sampai selesai—artinya, jika ekspor itu dijalankan
secara sinkron—Anda tidak bisa melakukan hal lain di komputer selama tugas itu
berjalan. Pengalaman itu tentu cukup menjengkelkan. Untungnya, sistem operasi
komputer Anda dapat, dan memang, menginterupsi ekspor itu secara tak terlihat
cukup sering sehingga Anda bisa menyelesaikan pekerjaan lain secara bersamaan.

Sekarang katakan Anda sedang mengunduh video yang dibagikan orang lain, yang
juga bisa memakan waktu, tetapi tidak menyita banyak waktu CPU. Dalam kasus
ini, CPU harus menunggu data tiba dari jaringan. Begitu data mulai tiba, Anda
bisa mulai membacanya, tetapi semua data itu mungkin baru lengkap setelah
beberapa saat. Bahkan setelah semua data hadir, jika videonya cukup besar,
memuat semuanya bisa butuh setidaknya satu atau dua detik. Itu mungkin tidak
terdengar lama, tetapi bagi prosesor modern, yang bisa menjalankan miliaran
operasi setiap detik, itu waktu yang sangat lama. Sekali lagi, sistem operasi
Anda akan menginterupsi program Anda secara tak terlihat agar CPU bisa
mengerjakan pekerjaan lain selagi menunggu panggilan jaringan itu selesai.

Ekspor video adalah contoh operasi _CPU-bound_ (terikat CPU) atau
_compute-bound_ (terikat komputasi). Operasi ini dibatasi oleh kecepatan
pemrosesan data potensial komputer di dalam CPU atau GPU, dan seberapa banyak
kecepatan itu bisa dicurahkan untuk operasi tersebut. Unduhan video adalah
contoh operasi _I/O-bound_ (terikat I/O), karena operasi ini dibatasi oleh
kecepatan masukan dan keluaran komputer; operasi ini hanya bisa secepat
pengiriman data melintasi jaringan.

Pada kedua contoh itu, interupsi tak terlihat dari sistem operasi menyediakan
satu bentuk konkurensi. Akan tetapi, konkurensi itu hanya terjadi di tingkat
keseluruhan program: sistem operasi menginterupsi satu program agar program
lain bisa menyelesaikan pekerjaan. Dalam banyak kasus, karena kita memahami
program kita pada tingkat yang jauh lebih rinci daripada sistem operasi, kita
bisa menemukan peluang konkurensi yang tidak terlihat oleh sistem operasi.

Contohnya, jika kita sedang membangun alat untuk mengelola unduhan file, kita
seharusnya bisa menulis program sedemikian rupa sehingga memulai satu unduhan
tidak membuat UI macet, dan pengguna bisa memulai beberapa unduhan sekaligus.
Akan tetapi, banyak API sistem operasi untuk berinteraksi dengan jaringan
bersifat _blocking_ (memblokir); artinya, API tersebut menahan kemajuan program
sampai data yang sedang diprosesnya benar-benar siap.

> Catatan: Kalau dipikir-pikir, beginilah cara kerja _sebagian besar_
> pemanggilan fungsi. Akan tetapi, istilah _blocking_ biasanya dikhususkan
> untuk pemanggilan fungsi yang berinteraksi dengan file, jaringan, atau
> sumber daya lain di komputer, karena pada kasus-kasus itulah sebuah program
> akan diuntungkan bila operasinya bersifat _non_-blocking (tidak memblokir).

Kita bisa menghindari pemblokiran thread utama dengan membuat sebuah thread
khusus untuk mengunduh setiap file. Namun, overhead sumber daya sistem yang
dipakai thread-thread itu pada akhirnya akan menjadi masalah. Akan lebih baik
bila pemanggilannya sejak awal tidak memblokir, dan sebagai gantinya kita bisa
mendefinisikan sejumlah *task* yang ingin diselesaikan program kita, lalu
membiarkan runtime memilih urutan dan cara terbaik untuk menjalankannya.

Itulah tepatnya yang diberikan abstraksi async (singkatan dari asynchronous)
milik Rust. Di bab ini, Anda akan mempelajari segala hal tentang async sembari
kita membahas topik-topik berikut:

- Cara memakai sintaks `async` dan `await` dari Rust serta menjalankan fungsi
  asinkron dengan sebuah runtime
- Cara memakai model async untuk menyelesaikan sebagian tantangan yang sama
  dengan yang kita lihat di Bab 16
- Bagaimana multithreading dan async memberikan solusi yang saling melengkapi
  dan dapat Anda kombinasikan dalam banyak kasus

Namun, sebelum kita melihat cara kerja async dalam praktik, kita perlu
berputar sebentar untuk membahas perbedaan antara paralelisme dan konkurensi.

## Paralelisme dan Konkurensi

Sejauh ini kita memperlakukan paralelisme dan konkurensi sebagai dua hal yang
hampir bisa dipertukarkan. Sekarang kita perlu membedakan keduanya dengan
lebih cermat, karena perbedaannya akan terlihat begitu kita mulai bekerja.

Perhatikan berbagai cara sebuah tim membagi pekerjaan pada sebuah proyek
perangkat lunak. Anda bisa memberi satu anggota beberapa tugas, memberi setiap
anggota satu tugas, atau memakai campuran dari dua pendekatan tersebut.

Ketika satu orang mengerjakan beberapa tugas berbeda sebelum salah satu
darinya selesai, itulah konkurensi. Salah satu cara mengimplementasikan
konkurensi mirip dengan memiliki dua proyek berbeda yang di-_check out_ di
komputer Anda; saat Anda bosan atau buntu di satu proyek, Anda beralih ke
proyek yang lain. Anda hanya satu orang, jadi Anda tidak bisa membuat kemajuan
pada kedua tugas pada saat yang persis sama, tetapi Anda bisa melakukan banyak
hal sekaligus, membuat kemajuan satu per satu dengan beralih di antara
keduanya (lihat Gambar 17-1).

<figure>

<img src="img/trpl17-01.svg" class="center" alt="Diagram dengan kotak bertumpuk berlabel Task A dan Task B, dengan belah ketupat di dalamnya yang mewakili subtugas. Panah menunjuk dari A1 ke B1, B1 ke A2, A2 ke B2, B2 ke A3, A3 ke A4, dan A4 ke B3. Panah-panah di antara subtugas itu melintasi kotak di antara Task A dan Task B." />

<figcaption>Gambar 17-1: Alur kerja konkuren, beralih antara *Task* A dan *Task* B</figcaption>

</figure>

Ketika tim membagi sekelompok tugas dengan cara setiap anggota mengambil satu
tugas dan mengerjakannya sendiri-sendiri, itulah paralelisme. Setiap orang di
tim bisa membuat kemajuan pada saat yang persis sama (lihat Gambar 17-2).

<figure>

<img src="img/trpl17-02.svg" class="center" alt="Diagram dengan kotak bertumpuk berlabel Task A dan Task B, dengan belah ketupat di dalamnya yang mewakili subtugas. Panah menunjuk dari A1 ke A2, A2 ke A3, A3 ke A4, B1 ke B2, dan B2 ke B3. Tidak ada panah yang melintas di antara kotak Task A dan Task B." />

<figcaption>Gambar 17-2: Alur kerja paralel, tempat pekerjaan pada *Task* A dan *Task* B berlangsung secara independen</figcaption>

</figure>

Pada kedua alur kerja ini, Anda mungkin harus berkoordinasi di antara berbagai
tugas. Barangkali Anda mengira tugas yang diberikan kepada satu orang
sepenuhnya independen dari pekerjaan orang lain, tetapi ternyata tugas itu
mengharuskan orang lain di tim menyelesaikan tugasnya lebih dulu. Sebagian
pekerjaan bisa dikerjakan secara paralel, tetapi sebagian lagi sebenarnya
serial: pekerjaan itu hanya bisa terjadi dalam urutan, satu tugas setelah
tugas berikutnya, seperti pada Gambar 17-3.

<figure>

<img src="img/trpl17-03.svg" class="center" alt="Diagram dengan kotak bertumpuk berlabel Task A dan Task B, dengan belah ketupat di dalamnya yang mewakili subtugas. Pada Task A, panah menunjuk dari A1 ke A2, dari A2 ke sepasang garis vertikal tebal seperti simbol “pause”, dan dari simbol itu ke A3. Pada Task B, panah menunjuk dari B1 ke B2, dari B2 ke B3, dari B3 ke A3, dan dari B3 ke B4." />

<figcaption>Gambar 17-3: Alur kerja yang sebagian paralel, tempat pekerjaan pada *Task* A dan *Task* B berlangsung secara independen sampai *Task* A3 terblokir menunggu hasil *Task* B3</figcaption>

</figure>

Begitu pula, Anda mungkin menyadari bahwa salah satu tugas Anda bergantung
pada tugas Anda yang lain. Sekarang pekerjaan konkuren Anda ikut menjadi
serial.

Paralelisme dan konkurensi juga bisa saling bersinggungan. Jika Anda tahu
seorang kolega terhenti sampai Anda menyelesaikan salah satu tugas Anda, Anda
mungkin akan memusatkan seluruh tenaga pada tugas itu untuk “membuka jalan”
bagi kolega Anda. Anda dan rekan kerja Anda tidak lagi bisa bekerja secara
paralel, dan Anda juga tidak lagi bisa bekerja secara konkuren pada
tugas-tugas Anda sendiri.

Dinamika dasar yang sama berlaku pada perangkat lunak dan perangkat keras.
Pada mesin dengan satu inti CPU, CPU hanya bisa menjalankan satu operasi pada
satu waktu, tetapi ia tetap bisa bekerja secara konkuren. Dengan memakai
alat-alat seperti thread, *process*, dan async, komputer bisa menjeda satu
aktivitas dan beralih ke aktivitas lain sebelum akhirnya kembali ke aktivitas
pertama itu. Pada mesin dengan beberapa inti CPU, komputer juga bisa bekerja
secara paralel. Satu inti bisa mengerjakan satu tugas sementara inti lain
mengerjakan tugas yang sama sekali tidak berkaitan, dan operasi-operasi itu
benar-benar berlangsung pada saat yang sama.

Menjalankan kode async di Rust biasanya berlangsung secara konkuren.
Bergantung pada perangkat keras, sistem operasi, dan runtime async yang kita
pakai (runtime async akan segera kita bahas lebih lanjut), konkurensi itu
mungkin juga memakai paralelisme di balik layar.

Sekarang, mari selami cara kerja pemrograman asinkron di Rust yang
sesungguhnya.
