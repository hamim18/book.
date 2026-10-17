# Konkurensi Tanpa Takut

Menangani pemrograman konkuren secara aman dan efisien adalah salah satu
tujuan utama Rust lainnya. _Concurrent programming_ (pemrograman konkuren),
ketika bagian-bagian berbeda dari sebuah program berjalan secara independen,
dan _parallel programming_ (pemrograman paralel), ketika bagian-bagian
berbeda dari sebuah program berjalan pada saat yang sama, menjadi semakin
penting seiring semakin banyak komputer memanfaatkan banyaknya prosesor yang
mereka miliki. Secara historis, pemrograman dalam konteks ini sulit dan rawan
galat. Rust berharap mengubah hal itu.

Awalnya, tim Rust mengira bahwa menjamin keamanan memori dan mencegah masalah
konkurensi adalah dua tantangan terpisah yang harus diselesaikan dengan metode
yang berbeda. Seiring waktu, tim itu menemukan bahwa sistem ownership dan tipe
adalah seperangkat alat yang ampuh untuk membantu mengelola keamanan memori
_dan_ masalah konkurensi! Dengan memanfaatkan ownership dan pemeriksaan tipe,
banyak galat konkurensi menjadi galat waktu kompilasi di Rust alih-alih galat
runtime. Karena itu, alih-alih membuat Anda menghabiskan banyak waktu mencoba
mereproduksi keadaan persis ketika bug konkurensi runtime terjadi, kode yang
salah akan menolak untuk dikompilasi dan menyajikan galat yang menjelaskan
masalahnya. Akibatnya, Anda dapat memperbaiki kode Anda selagi mengerjakannya,
alih-alih berpotensi setelah kode itu dikirim ke produksi. Kami menjuluki
aspek Rust ini _fearless concurrency_ (konkurensi tanpa takut). Konkurensi
tanpa takut memungkinkan Anda menulis kode yang bebas dari bug yang samar dan
mudah di-refactor tanpa memperkenalkan bug baru.

> Catatan: Demi kesederhanaan, kami akan menyebut banyak masalah itu sebagai
> _concurrent_ alih-alih lebih tepat dengan menyebut _concurrent dan/atau
> parallel_. Untuk bab ini, mohon secara mental gantikan _concurrent dan/atau
> parallel_ setiap kali kami memakai _concurrent_. Di bab berikutnya, ketika
> perbedaannya lebih penting, kami akan lebih spesifik.

Banyak bahasa bersikap dogmatis tentang solusi yang mereka tawarkan untuk
menangani masalah konkuren. Sebagai contoh, Erlang memiliki fungsionalitas
elegan untuk konkurensi message-passing tetapi hanya memiliki cara yang
samar-samar untuk berbagi state antar-thread. Mendukung hanya sebagian
himpunan solusi yang mungkin adalah strategi yang masuk akal untuk bahasa
tingkat tinggi karena bahasa tingkat tinggi menjanjikan keuntungan dari
melepas sebagian kontrol demi mendapatkan abstraksi. Namun, bahasa tingkat
rendah diharapkan menyediakan solusi dengan performa terbaik dalam situasi
apa pun dan memiliki lebih sedikit abstraksi di atas perangkat keras. Karena
itu, Rust menawarkan beragam alat untuk memodelkan masalah dengan cara apa pun
yang sesuai untuk situasi dan kebutuhan Anda.

Berikut topik yang akan kita bahas di bab ini:

- Cara membuat thread untuk menjalankan beberapa potongan kode pada saat yang
  sama
- Konkurensi _message-passing_ (pengiriman pesan), di mana channel mengirim
  pesan antar-thread
- Konkurensi _shared-state_ (state bersama), di mana beberapa thread memiliki
  akses ke sepotong data tertentu
- Trait `Sync` dan `Send`, yang memperluas jaminan konkurensi Rust ke tipe
  yang didefinisikan pengguna maupun tipe yang disediakan pustaka standar
