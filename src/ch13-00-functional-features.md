# Fitur Bahasa Fungsional: Iterator dan Closure

Desain Rust mengambil inspirasi dari banyak bahasa dan teknik yang sudah ada,
dan salah satu pengaruh yang signifikan adalah _functional programming_
(functional programming). Memprogram dengan gaya fungsional sering kali
mencakup memakai fungsi sebagai nilai dengan meneruskannya sebagai argumen,
mengembalikannya dari fungsi lain, menetapkannya ke variable untuk dieksekusi
nanti, dan seterusnya.

Di bab ini, kita tidak akan memperdebatkan soal apa itu functional programming
atau bukan, melainkan membahas beberapa fitur Rust yang mirip dengan
fitur-fitur di banyak bahasa yang sering disebut fungsional.

Secara lebih spesifik, kita akan membahas:

- _Closure_, konstruksi mirip fungsi yang dapat Anda simpan di sebuah variable
- _Iterator_, cara memproses serangkaian elemen
- Cara memakai *closure* dan *iterator* untuk memperbaiki proyek I/O di Bab 12
- Performa *closure* dan *iterator* (peringatan spoiler: Mereka lebih cepat
  daripada yang mungkin Anda kira!)

Kita telah membahas beberapa fitur Rust lain, seperti *pattern matching*
(pencocokan pattern) dan *enum*, yang juga dipengaruhi gaya fungsional. Karena
menguasai *closure* dan *iterator* merupakan bagian penting dari menulis kode Rust
yang cepat dan idiomatis, kita akan mendedikasikan seluruh bab ini untuk
mereka.
