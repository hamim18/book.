# Smart Pointers

*Pointer* adalah konsep umum untuk variabel yang memuat sebuah alamat di memori.
Alamat ini merujuk ke, atau "menunjuk ke," sejumlah data lain. Jenis *pointer*
yang paling umum di Rust adalah *reference*, yang telah Anda pelajari di Bab 4.
*Reference* ditandai dengan simbol `&` dan meminjam nilai yang ditunjuknya.
*Reference* tidak memiliki kemampuan khusus apa pun selain merujuk data, dan
tidak memiliki overhead.

_Smart pointer_ (penunjuk pintar), di sisi lain, adalah struktur data yang
berperilaku seperti *pointer* tetapi juga memiliki metadata dan kemampuan
tambahan. Konsep *smart pointer* tidak unik bagi Rust: *Smart pointer* berasal
dari C++ dan ada juga di bahasa-bahasa lain. Rust memiliki beragam smart
*pointer* yang didefinisikan di pustaka standar yang menyediakan fungsionalitas
di luar yang disediakan oleh *reference*. Untuk mengeksplorasi konsep umumnya,
kita akan melihat beberapa contoh *smart pointer* yang berbeda, termasuk type
*smart pointer* _reference counting_ (penghitungan referensi). *Pointer* ini
memungkinkan Anda mengizinkan data memiliki beberapa pemilik dengan melacak
jumlah pemilik dan, ketika tidak ada pemilik tersisa, membersihkan data itu.

Di Rust, dengan konsep *ownership* dan *borrowing*-nya, ada perbedaan tambahan
antara *reference* dan *smart pointer*: Sementara *reference* hanya meminjam data,
dalam banyak kasus *smart pointer* _memiliki_ data yang ditunjuknya.

*Smart pointer* biasanya diimplementasikan menggunakan *struct*. Tidak seperti
*struct* biasa, *smart pointer* mengimplementasikan *trait* `Deref` dan `Drop`.
*Trait* `Deref` memungkinkan sebuah instance dari *struct* *smart pointer*
berperilaku seperti sebuah *reference* sehingga Anda dapat menulis kode yang
bekerja dengan *reference* ataupun *smart pointer*. *Trait* `Drop` memungkinkan Anda
menyesuaikan kode yang dijalankan ketika sebuah instance *smart pointer* keluar
dari *scope*. Di bab ini, kita akan membahas kedua *trait* ini dan menunjukkan
mengapa keduanya penting bagi *smart pointer*.

Mengingat pola *smart pointer* adalah pola desain umum yang sering dipakai di
Rust, bab ini tidak akan membahas setiap *smart pointer* yang ada. Banyak
library memiliki *smart pointer* sendiri, dan Anda bahkan dapat menulis smart
*pointer* Anda sendiri. Kita akan membahas *smart pointer* yang paling umum di
pustaka standar:

- `Box<T>`, untuk mengalokasikan nilai di *heap*
- `Rc<T>`, type penghitungan referensi yang memungkinkan banyak kepemilikan
- `Ref<T>` dan `RefMut<T>`, diakses melalui `RefCell<T>`, type yang menegakkan
  aturan *borrowing* pada runtime alih-alih pada waktu kompilasi

Selain itu, kita akan membahas pola _interior mutability_ (mutabilitas
internal) di mana sebuah type *immutable* mengekspos API untuk mengubah nilai
di bagian dalamnya. Kita juga akan membahas *reference cycle* (siklus
referensi): bagaimana siklus itu bisa membocorkan memori dan bagaimana
mencegahnya.

Mari kita mulai!
