# Proyek I/O: Membangun Program Baris Perintah

Bab ini merangkum banyak keterampilan yang telah Anda pelajari sejauh ini
sekaligus menjelajahi beberapa fitur pustaka standar lainnya. Kita akan
membangun sebuah alat baris perintah yang berinteraksi dengan input/output
file dan baris perintah untuk melatih sebagian konsep Rust yang kini telah Anda
kuasai.

Kecepatan, keamanan, output binary tunggal, dan dukungan lintas platform Rust
menjadikannya bahasa yang ideal untuk membuat alat baris perintah, jadi untuk
proyek kita, kita akan membuat versi kita sendiri dari alat pencarian baris
perintah klasik `grep` (**g**lobally search a **r**egular **e**xpression and
**p**rint, mencari secara global sebuah expression reguler lalu mencetaknya).
Pada kasus penggunaan paling sederhana, `grep` mencari sebuah string tertentu
di dalam sebuah file tertentu. Untuk melakukannya, `grep` menerima sebuah *path*
file dan sebuah string sebagai argumennya. Kemudian, ia membaca file tersebut,
menemukan baris-baris di dalam file itu yang memuat string argumen tersebut,
dan mencetak baris-baris itu.

Sepanjang perjalanan, kita akan menunjukkan cara membuat alat baris perintah
kita memakai fitur-fitur terminal yang dipakai banyak alat baris perintah
lainnya. Kita akan membaca nilai sebuah environment variable untuk memungkinkan
pengguna mengonfigurasi perilaku alat kita. Kita juga akan mencetak pesan
error ke aliran konsol standard error (`stderr`) alih-alih standard output
(`stdout`) sehingga, misalnya, pengguna bisa mengalihkan output yang berhasil
ke sebuah file sambil tetap melihat pesan error di layar.

Seorang anggota komunitas Rust, Andrew Gallant, telah membuat versi `grep`
yang lengkap fiturnya dan sangat cepat, bernama `ripgrep`. Sebagai
perbandingan, versi kita akan cukup sederhana, tetapi bab ini akan memberi
Anda sebagian pengetahuan dasar yang Anda perlukan untuk memahami proyek dunia
nyata seperti `ripgrep`.

Proyek `grep` kita akan memadukan sejumlah konsep yang telah Anda pelajari
sejauh ini:

- Menata kode ([Bab 7][ch7]<!-- ignore -->)
- Memakai vektor dan string ([Bab 8][ch8]<!-- ignore -->)
- Menangani error ([Bab 9][ch9]<!-- ignore -->)
- Memakai *trait* dan *lifetime* bilamana sesuai ([Bab 10][ch10]<!-- ignore -->)
- Menulis pengujian ([Bab 11][ch11]<!-- ignore -->)

Kita juga akan memperkenalkan secara singkat *closure*, *iterator*, dan *trait
object* (objek *trait*), yang akan dibahas secara mendetail di [Bab 13][ch13]<!--
ignore --> dan [Bab 18][ch18]<!-- ignore -->.

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[ch8]: ch08-00-common-collections.html
[ch9]: ch09-00-error-handling.html
[ch10]: ch10-00-generics.html
[ch11]: ch11-00-testing.html
[ch13]: ch13-00-functional-features.html
[ch18]: ch18-00-oop.html
