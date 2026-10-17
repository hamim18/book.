# Panduan Membaca Buku Ini

## Urutan membaca

Buku ini dirancang untuk dibaca berurutan dari depan ke belakang: bab-bab
awal meletakkan konsep dasar, dan bab-bab selanjutnya membangun di atasnya.
Bab 1 sampai 3 memperkenalkan sintaks dasar; bab 4 sampai 9 membahas sistem
kepemilikan (*ownership*), *struct*, *enum*, koleksi, dan penanganan error;
bab 10 sampai 12 membahas *generics*, *trait*, *lifetime*, dan pengujian.
Bab 13 sampai 18 membahas *closure*, *iterator*, Cargo, *smart pointer*,
konkurensi, dan pemrograman asinkron; bab 19 sampai 21 membahas fitur-fitur
lanjutan dan proyek akhir.

Anda tidak perlu menghafal apa pun. Setiap bab berdiri di atas yang
sebelumnya, tetapi Anda bisa kembali kapan saja; indeks istilah dan daftar
isi di bagian depan akan membantu menemukan kembali suatu topik.

## Konvensi istilah

Istilah teknis ditulis dalam bahasa Inggris di prosa. Istilah seperti
*ownership*, *borrowing*, *lifetime*, dan *trait* dicetak miring, dengan
padanan bahasa Indonesia dalam kurung pada kemunculan pertamanya di setiap
bab. Kata-kata pinjaman yang sudah lazim ditulis polos tanpa miring, seperti
error, variable, method, loop, dan thread. Daftar lengkap pasangan
Inggris–Indonesia tersedia di glosarium pada akhir buku.

## Contoh kode

Semua contoh kode dalam buku ini dipertahankan persis seperti versi aslinya
dan diuji terhadap versi Rust yang disebutkan pada halaman judul. Baris yang
diawali tanda `#` di dalam contoh adalah baris tersembunyi: baris itu bagian
dari kode, tetapi tidak ditampilkan di halaman.

Beberapa contoh sengaja tidak dapat dikompilasi; blok tersebut ditandai
seperti `does_not_compile` pada versi daring, dan tujuannya memang untuk
menunjukkan kode yang keliru.

Contoh pada bab 17 memakai *crate* bantu bernama `trpl`; penjelasan cara
membangunnya ada pada bab tersebut.

## Kotak catatan

Kotak berlatar krem dengan garis di tepi kiri adalah catatan yang memperluas
topik yang sedang dibahas — bukan bacaan wajib, tetapi sering kali berguna.

## Ikon Ferris

Di versi daring, tabel pada Bab 0 memakai ikon kepiting Ferris untuk
menandai kode yang sengaja tidak berfungsi, kode yang tidak dapat
dikompilasi, dan kode yang sah. Pada cetakan ini penanda tersebut tampil
sebagai teks singkat pada tabel yang sama.

## Rujukan ke versi asli

Bila Anda ingin membandingkan dengan versi bahasa Inggris, buku asli
tersedia daring di <https://doc.rust-lang.org/stable/book/>; alamat lengkap
sumber-sumber lain ada pada bagian *Referensi dan Sumber Daring*.
