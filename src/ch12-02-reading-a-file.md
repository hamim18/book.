## Membaca File

Sekarang kita akan menambahkan fungsionalitas untuk membaca file yang
ditentukan di argumen `file_path`. Pertama, kita memerlukan sebuah file contoh
untuk mengujinya: Kita akan memakai sebuah file yang berisi sedikit teks dalam
beberapa baris dengan beberapa kata yang berulang. Listing 12-3 memuat sebuah
puisi Emily Dickinson yang cocok untuk ini! Buatlah sebuah file bernama
_poem.txt_ di tingkat akar proyek Anda, lalu masukkan puisi “I’m Nobody! Who
are you?”

<Listing number="12-3" file-name="poem.txt" caption="Sebuah puisi karya Emily Dickinson menjadi kasus uji yang bagus.">

```text
{{#include ../listings/ch12-an-io-project/listing-12-03/poem.txt}}
```

</Listing>

Setelah teksnya tersedia, edit _src/main.rs_ dan tambahkan kode untuk membaca
file tersebut, seperti yang ditunjukkan di Listing 12-4.

<Listing number="12-4" file-name="src/main.rs" caption="Membaca isi file yang ditentukan oleh argumen kedua">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/src/main.rs:here}}
```

</Listing>

Pertama, kita membawa bagian pustaka standar yang relevan dengan pernyataan
`use`: Kita memerlukan `std::fs` untuk menangani file.

Di dalam `main`, pernyataan baru `fs::read_to_string` menerima `file_path`,
membuka file tersebut, dan mengembalikan sebuah nilai typed
`std::io::Result<String>` yang memuat isi file tersebut.

Setelah itu, kita kembali menambahkan pernyataan `println!` sementara yang
mencetak nilai `contents` setelah file dibaca, supaya kita dapat memeriksa
bahwa program ini sejauh ini bekerja.

Mari kita jalankan kode ini dengan string apa pun sebagai argumen baris
perintah pertama (karena kita belum mengimplementasikan bagian pencariannya)
dan file _poem.txt_ sebagai argumen kedua:

```console
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/output.txt}}
```

Hebat! Kode tersebut membaca lalu mencetak isi file. Tetapi kode ini memiliki
beberapa kelemahan. Saat ini, fungsi `main` memiliki banyak tanggung jawab:
Secara umum, fungsi menjadi lebih jelas dan lebih mudah dirawat jika setiap
fungsi hanya bertanggung jawab atas satu gagasan. Masalah lainnya adalah kita
belum menangani error sebaik mungkin. Program ini masih kecil, jadi
kelemahan-kelemahan ini bukan masalah besar, tetapi seiring pertumbuhan
program, akan semakin sulit untuk memperbaikinya secara bersih. Merupakan
praktik yang baik untuk mulai melakukan refactoring sejak dini ketika
mengembangkan sebuah program, karena jauh lebih mudah melakukan refactoring
pada kode dalam jumlah yang lebih kecil. Selanjutnya kita akan melakukannya.
