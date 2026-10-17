<!-- Old headings. Do not remove or links may break. -->

<a id="writing-error-messages-to-standard-error-instead-of-standard-output"></a>

## Mengalihkan Error ke Standard Error

Saat ini, kita menulis semua output kita ke terminal menggunakan makro
`println!`. Di sebagian besar terminal, ada dua jenis output: _standard
output_ (`stdout`) untuk informasi umum dan _standard error_ (`stderr`) untuk
pesan error. Pembedaan ini memungkinkan pengguna memilih untuk mengarahkan
output program yang berhasil ke sebuah file, tetapi tetap mencetak pesan
error ke layar.

Makro `println!` hanya mampu mencetak ke standard output, jadi kita harus
memakai sesuatu yang lain untuk mencetak ke standard error.

### Memeriksa Tempat Error Ditulis

Pertama, mari kita amati bagaimana konten yang dicetak oleh `minigrep` saat
ini ditulis ke standard output, termasuk pesan-pesan error yang ingin kita
tulis ke standard error. Kita akan melakukannya dengan mengalihkan aliran
standard output ke sebuah file sambil dengan sengaja memicu error. Kita tidak
akan mengalihkan aliran standard error, jadi konten apa pun yang dikirim ke
standard error akan terus tampil di layar.

Program command line diharapkan mengirim pesan error ke aliran standard
error sehingga kita tetap dapat melihat pesan error di layar bahkan jika kita
mengalihkan aliran standard output ke sebuah file. Program kita saat ini
belum berperilaku baik: Sebentar lagi kita akan melihat bahwa program itu
justru menyimpan output pesan errornya ke sebuah file!

Untuk mendemonstrasikan perilaku ini, kita akan menjalankan programnya dengan
`>` dan *path* file _output.txt_, tujuan pengalihan aliran standard output yang
kita inginkan. Kita tidak akan meneruskan argumen apa pun, yang seharusnya
memicu error:

```console
$ cargo run > output.txt
```

Sintaks `>` memberi tahu shell untuk menulis isi standard output ke
_output.txt_ alih-alih ke layar. Kita tidak melihat pesan error yang kita
harapkan tercetak di layar, jadi itu berarti pesan tersebut pasti berakhir di
dalam file. Inilah isi _output.txt_:

```text
Problem parsing arguments: not enough arguments
```

Ya, pesan error kita sedang dicetak ke standard output. Jauh lebih berguna
bagi pesan-pesan error seperti ini untuk dicetak ke standard error sehingga
hanya data dari proses yang berhasil yang berakhir di dalam file. Kita akan
mengubahnya.

### Mencetak Error ke Standard Error

Kita akan memakai kode di Listing 12-24 untuk mengubah cara pesan error
dicetak. Berkat refactoring yang kita lakukan di awal bab ini, semua kode
yang mencetak pesan error berada di satu fungsi, `main`. Pustaka standar
menyediakan makro `eprintln!` yang mencetak ke aliran standard error, jadi
mari kita ubah dua tempat yang kita pakai untuk memanggil `println!` guna
mencetak error menjadi memakai `eprintln!`.

<Listing number="12-24" file-name="src/main.rs" caption="Menulis pesan error ke standard error alih-alih standard output menggunakan `eprintln!`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-24/src/main.rs:here}}
```

</Listing>

Sekarang mari kita jalankan lagi programnya dengan cara yang sama, tanpa
argumen apa pun dan mengalihkan standard output dengan `>`:

```console
$ cargo run > output.txt
Problem parsing arguments: not enough arguments
```

Sekarang kita melihat errornya di layar dan _output.txt_ tidak berisi apa
pun, sesuai perilaku yang kita harapkan dari program command line.

Mari kita jalankan lagi programnya dengan argumen-argumen yang tidak memicu
error, tetapi tetap mengalihkan standard output ke sebuah file, seperti ini:

```console
$ cargo run -- to poem.txt > output.txt
```

Kita tidak akan melihat output apa pun di terminal, dan _output.txt_ akan
memuat hasil-hasil kita:

<span class="filename">Nama File: output.txt</span>

```text
Are you nobody, too?
How dreary to be somebody!
```

Ini menunjukkan bahwa sekarang kita memakai standard output untuk output
yang berhasil dan standard error untuk output error, sebagaimana mestinya.

## Ringkasan

Bab ini merangkum beberapa konsep utama yang telah Anda pelajari sejauh ini
dan membahas cara melakukan operasi I/O yang umum di Rust. Dengan memakai
argumen command line, file, environment variable, dan makro `eprintln!`
untuk mencetak error, Anda kini siap menulis aplikasi command line.
Dipadukan dengan konsep-konsep di bab-bab sebelumnya, kode Anda akan tertata
dengan baik, menyimpan data secara efektif di struktur data yang tepat,
menangani error dengan baik, dan teruji dengan baik.

Selanjutnya, kita akan menjelajahi beberapa fitur Rust yang dipengaruhi oleh
bahasa-bahasa fungsional: *closure* dan *iterator*.
