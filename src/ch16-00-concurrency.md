# Concurrency Tanpa Takut

Menangani concurrent programming secara aman dan efisien adalah salah satu
tujuan utama Rust lainnya. _Concurrent programming_ (concurrent programming),
ketika bagian-bagian berbeda dari sebuah program berjalan secara independen,
dan _parallel programming_ (parallel programming), ketika bagian-bagian
berbeda dari sebuah program berjalan pada saat yang sama, menjadi semakin
penting seiring semakin banyak komputer memanfaatkan banyaknya prosesor yang
mereka miliki. Secara historis, pemrograman dalam konteks ini sulit dan rawan
error. Rust berharap mengubah hal itu.

Awalnya, tim Rust mengira bahwa menjamin memory safety dan mencegah masalah
concurrency adalah dua tantangan terpisah yang harus diselesaikan dengan method
yang berbeda. Seiring waktu, tim itu menemukan bahwa sistem *ownership* dan type
adalah seperangkat tool yang ampuh untuk membantu mengelola memory safety
_dan_ masalah concurrency! Dengan memanfaatkan *ownership* dan pemeriksaan type,
banyak error concurrency menjadi error waktu kompilasi di Rust alih-alih error
runtime. Karena itu, alih-alih membuat Anda menghabiskan banyak waktu mencoba
mereproduksi keadaan persis ketika bug concurrency runtime terjadi, kode yang
salah akan menolak untuk dikompilasi dan menyajikan error yang menjelaskan
masalahnya. Akibatnya, Anda dapat memperbaiki kode Anda selagi mengerjakannya,
alih-alih berpotensi setelah kode itu dikirim ke produksi. Kami menjuluki
aspek Rust ini _fearless concurrency_ (concurrency tanpa takut). Concurrency
tanpa takut memungkinkan Anda menulis kode yang bebas dari bug yang samar dan
mudah di-refactor tanpa memperkenalkan bug baru.

> Catatan: Demi kesederhanaan, kita akan menyebut banyak masalah itu sebagai
> _concurrent_ alih-alih lebih tepat dengan menyebut _concurrent dan/atau
> parallel_. Untuk bab ini, mohon secara mental gantikan _concurrent dan/atau
> parallel_ setiap kali kita memakai _concurrent_. Di bab berikutnya, ketika
> perbedaannya lebih penting, kita akan lebih spesifik.

Banyak bahasa bersikap dogmatis tentang solusi yang mereka tawarkan untuk
menangani masalah concurrent. Sebagai contoh, Erlang memiliki fungsionalitas
elegan untuk concurrency message-passing tetapi hanya memiliki cara yang
samar-samar untuk berbagi state antar-thread. Mendukung hanya sebagian
himpunan solusi yang mungkin adalah strategi yang masuk akal untuk bahasa
tingkat tinggi karena bahasa tingkat tinggi menjanjikan keuntungan dari
melepas sebagian kontrol demi mendapatkan abstraksi. Namun, bahasa tingkat
rendah diharapkan menyediakan solusi dengan performa terbaik dalam situasi
apa pun dan memiliki lebih sedikit abstraksi di atas perangkat keras. Karena
itu, Rust menawarkan beragam tool untuk memodelkan masalah dengan cara apa pun
yang sesuai untuk situasi dan kebutuhan Anda.

Berikut topik yang akan kita bahas di bab ini:

- Cara membuat thread untuk menjalankan beberapa potongan kode pada saat yang
  sama
- Concurrency _message-passing_ (message passing), di mana *channel* mengirim
  pesan antar-thread
- Concurrency _shared-state_ (state bersama), di mana beberapa thread memiliki
  akses ke sepotong data tertentu
- *Trait* `Sync` dan `Send`, yang memperluas jaminan concurrency Rust ke type
  yang didefinisikan pengguna maupun type yang disediakan standard library
