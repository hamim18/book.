# Proyek Akhir: Membangun Web Server Multithreaded

Perjalanan ini sudah panjang, tetapi kita telah sampai di akhir buku. Di bab
ini, kita akan membangun satu proyek lagi bersama-sama untuk menunjukkan
beberapa konsep yang kita bahas di bab-bab terakhir, sekaligus mengulang
beberapa pelajaran sebelumnya.

Untuk proyek akhir kita, kita akan membuat server web yang menyapa “Hello!”
dan tampak seperti Gambar 21-1 di peramban web.

Berikut rencana kita untuk membangun server web itu:

1. Mempelajari sedikit tentang TCP dan HTTP.
2. Mendengarkan koneksi TCP pada sebuah soket.
3. Melakukan parsing sejumlah kecil permintaan HTTP.
4. Membuat respons HTTP yang tepat.
5. Meningkatkan throughput server kita dengan *thread pool*.

<img alt="Tangkapan layar peramban web yang mengunjungi alamat 127.0.0.1:8080 dan menampilkan halaman web dengan konten teks “Hello! Hi from Rust”" src="img/trpl21-01.png" class="center" style="width: 50%;" />

<span class="caption">Gambar 21-1: Proyek akhir kita bersama</span>

Sebelum kita mulai, ada dua hal yang perlu kami sampaikan. Pertama, metode
yang akan kita pakai bukanlah cara terbaik untuk membangun server web dengan
Rust. Anggota komunitas telah menerbitkan sejumlah *crate* siap produksi yang
tersedia di [crates.io](https://crates.io/)<!-- ignore --> yang menyediakan
implementasi server web dan *thread pool* yang lebih lengkap daripada yang
akan kita bangun. Akan tetapi, niat kami di bab ini adalah membantu Anda
belajar, bukan mengambil jalan pintas. Karena Rust adalah bahasa pemrograman
sistem, kita bisa memilih tingkat abstraksi yang ingin kita pakai untuk
bekerja dan bisa turun ke tingkat yang lebih rendah daripada yang mungkin
atau praktis di bahasa lain.

Kedua, kita tidak akan memakai async dan await di sini. Membangun thread
pool saja sudah merupakan tantangan yang cukup besar, tanpa menambahkan
pembangunan runtime async! Akan tetapi, kita akan mencatat bagaimana async
dan await mungkin bisa diterapkan pada beberapa masalah yang sama yang akan
kita lihat di bab ini. Pada akhirnya, seperti yang kami catat di Bab 17,
banyak runtime async yang memakai *thread pool* untuk mengelola pekerjaan
mereka.

Karena itu, kita akan menulis server HTTP dasar dan *thread pool*-nya secara
manual supaya Anda bisa mempelajari gagasan dan teknik umum di balik
*crate*-crate yang mungkin Anda pakai di masa depan.
