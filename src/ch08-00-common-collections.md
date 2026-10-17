# Koleksi Umum

Pustaka standar Rust menyertakan sejumlah struktur data yang sangat berguna
yang disebut koleksi. Sebagian besar data type lain merepresentasikan satu
nilai tertentu, tetapi koleksi dapat menampung banyak nilai. Tidak seperti
type built-in array dan *tuple*, data yang ditunjuk koleksi-koleksi ini
disimpan di *heap*, yang berarti banyaknya data tidak perlu diketahui pada
waktu kompilasi dan dapat bertambah atau menyusut seiring berjalannya
program. Setiap jenis koleksi memiliki kemampuan dan biaya yang berbeda, dan
memilih yang tepat untuk situasi Anda saat ini adalah keterampilan yang akan
Anda kembangkan seiring waktu. Di bab ini, kita akan membahas tiga koleksi
yang sangat sering dipakai di program Rust:

- Sebuah vektor memungkinkan Anda menyimpan sejumlah nilai yang jumlahnya
  dapat berubah, bersebelahan satu sama lain.
- Sebuah *string* adalah koleksi karakter. Kita telah menyinggung type
  `String` sebelumnya, tetapi di bab ini, kita akan membahasnya secara
  mendalam.
- Sebuah hash map memungkinkan Anda mengasosiasikan sebuah nilai dengan
  sebuah kunci tertentu. Ini adalah implementasi khusus dari struktur data
  yang lebih umum yang disebut *map*.

Untuk mempelajari jenis koleksi lain yang disediakan oleh pustaka standar,
lihat [dokumentasinya][collections].

Kita akan membahas cara membuat dan memperbarui vektor, string, dan hash
map, serta apa yang membuat masing-masing istimewa.

[collections]: ../std/collections/index.html
