# Menulis Pengujian Terotomatisasi

Dalam esainya tahun 1972 yang berjudul “The Humble Programmer,” Edsger W.
Dijkstra mengatakan bahwa “pengujian program bisa menjadi cara yang sangat
efektif untuk menunjukkan keberadaan bug, tetapi sama sekali tidak memadai
untuk menunjukkan ketiadaan bug.” Itu tidak berarti kita tidak boleh
berusaha menguji sebanyak mungkin!

*Correctness* (kebenaran) dalam program kita adalah sejauh mana kode kita
melakukan apa yang kita maksudkan. Rust dirancang dengan tingkat kepedulian
yang tinggi terhadap kebenaran program, tetapi kebenaran itu kompleks dan
tidak mudah dibuktikan. Sistem type Rust memikul sebagian besar beban ini,
tetapi type system tidak bisa menangkap semuanya. Karena itu, Rust
menyertakan dukungan untuk menulis *test* (pengujian) perangkat lunak
terotomatisasi.

Katakanlah kita menulis fungsi `add_two` yang menambahkan 2 ke angka apa pun
yang diteruskan kepadanya. Tanda tangan fungsi ini menerima sebuah integer
sebagai parameter dan mengembalikan sebuah integer sebagai hasil. Ketika
kita mengimplementasikan dan mengompilasi fungsi itu, Rust melakukan semua
pemeriksaan type dan pemeriksaan borrow yang telah Anda pelajari sejauh ini
untuk memastikan bahwa, misalnya, kita tidak meneruskan nilai `String` atau
*reference* yang tidak valid ke fungsi ini. Akan tetapi, Rust _tidak bisa_
memeriksa bahwa fungsi ini akan melakukan persis apa yang kita maksudkan,
yaitu mengembalikan parameter plus 2 alih-alih, katakanlah, parameter plus
10 atau parameter minus 50! Di sinilah pengujian berperan.

Kita bisa menulis pengujian yang menegaskan, misalnya, bahwa ketika kita
meneruskan `3` ke fungsi `add_two`, nilai yang dikembalikan adalah `5`.
Kita bisa menjalankan pengujian ini kapan pun kita membuat perubahan pada
kode kita untuk memastikan perilaku benar yang sudah ada tidak berubah.

Pengujian adalah keterampilan yang kompleks: meskipun kita tidak bisa
membahas setiap detail tentang cara menulis pengujian yang baik dalam satu
bab, di bab ini kita akan membahas mekanisme fasilitas pengujian Rust. Kita
akan membicarakan anotasi dan *macro* (makro) yang tersedia bagi Anda saat
menulis pengujian, perilaku bawaan dan opsi-opsi yang disediakan untuk
menjalankan pengujian, serta cara mengorganisasikan pengujian menjadi
pengujian unit dan pengujian integrasi.
