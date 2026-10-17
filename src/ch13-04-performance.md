<!-- Old headings. Do not remove or links may break. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## Performa pada Perulangan vs. Iterator

Untuk menentukan apakah akan memakai perulangan atau *iterator*, Anda perlu
mengetahui implementasi mana yang lebih cepat: versi fungsi `search` dengan
perulangan `for` eksplisit atau versi dengan *iterator*.

Kita menjalankan sebuah benchmark dengan memuat seluruh isi _The Adventures of
Sherlock Holmes_ karya Sir Arthur Conan Doyle ke dalam sebuah `String` dan
mencari kata _the_ di dalam isi tersebut. Berikut hasil benchmark pada versi
`search` yang memakai perulangan `for` dan versi yang memakai *iterator*:

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

Kedua implementasi itu memiliki performa yang mirip! Kita tidak akan
menjelaskan kode benchmark di sini karena tujuannya bukan untuk membuktikan
bahwa kedua versi itu setara, melainkan untuk mendapat gambaran umum tentang
bagaimana kedua implementasi ini dibandingkan dari segi performa.

Untuk benchmark yang lebih menyeluruh, Anda sebaiknya memeriksa menggunakan
berbagai teks dengan berbagai ukuran sebagai `contents`, kata-kata yang
berbeda dan kata-kata dengan panjang yang berbeda sebagai `query`, dan segala
macam variasi lainnya. Intinya begini: *Iterator*, meskipun merupakan
abstraksi tingkat tinggi, terkompilasi menjadi kode yang kurang lebih sama
dengan jika Anda menulis sendiri kode tingkat rendahnya. *Iterator* adalah
salah satu *zero-cost abstraction* (abstraksi tanpa biaya) Rust, yang berarti
memakai abstraksi itu tidak menimbulkan overhead runtime tambahan. Ini analog
dengan cara Bjarne Stroustrup, perancang dan pengimplementasi asli C++,
mendefinisikan zero-overhead dalam presentasi utama (keynote) ETAPS tahun
2012-nya yang berjudul “Foundations of C++”:

> Secara umum, implementasi C++ menaati prinsip zero-overhead: Apa yang tidak
> Anda pakai, tidak Anda bayar. Dan lebih jauh lagi: Apa yang Anda pakai,
> tidak bisa Anda tulis kodenya secara manual dengan lebih baik.

Dalam banyak kasus, kode Rust yang memakai *iterator* terkompilasi menjadi
assembly yang sama dengan yang akan Anda tulis secara manual. Optimasi seperti
loop unrolling dan penghapusan pemeriksaan batas pada akses array berlaku dan
membuat kode yang dihasilkan menjadi sangat efisien. Sekarang setelah Anda
tahu ini, Anda dapat memakai *iterator* dan *closure* tanpa takut! Mereka
membuat kode tampak lebih tinggi tingkatnya tetapi tidak mengenakan denda
performa runtime karenanya.

## Ringkasan

*Closure* dan *iterator* adalah fitur Rust yang terinspirasi oleh gagasan-gagasan
bahasa pemrograman fungsional. Keduanya berkontribusi pada kemampuan Rust
untuk mengekspresikan gagasan tingkat tinggi dengan jelas pada performa
tingkat rendah. Implementasi *closure* dan *iterator* dibuat sedemikian rupa
sehingga performa runtime tidak terpengaruh. Ini adalah bagian dari tujuan
Rust untuk berupaya menyediakan *zero-cost abstraction*.

Sekarang setelah kita memperbaiki ekspresivitas proyek I/O kita, mari kita
lihat beberapa fitur `cargo` lainnya yang akan membantu kita membagikan
proyek ini kepada dunia.
