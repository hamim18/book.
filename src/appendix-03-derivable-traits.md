## Lampiran C: Trait yang Dapat Diturunkan

Di berbagai bagian buku ini, kita sudah membahas atribut `derive`, yang dapat
Anda terapkan pada definisi *struct* atau *enum*. Atribut `derive` menghasilkan kode
yang mengimplementasikan *trait* dengan implementasi bawaannya sendiri pada tipe
yang Anda beri anotasi dengan sintaks `derive`.

Dalam lampiran ini, kami menyajikan rujukan untuk semua *trait* di pustaka standar
yang dapat Anda pakai dengan `derive`. Setiap bagian mencakup:

- Operator dan metode apa saja yang diaktifkan oleh penurunan *trait* ini
- Apa yang dilakukan implementasi *trait* yang disediakan oleh `derive`
- Apa yang ditandakan oleh pengimplementasian *trait* itu tentang tipe tersebut
- Kondisi yang mengizinkan atau tidak mengizinkan Anda mengimplementasikan *trait*
  itu
- Contoh operasi yang memerlukan *trait* itu

Jika Anda menginginkan perilaku yang berbeda dari yang disediakan atribut
`derive`, lihat [dokumentasi pustaka standar](../std/index.html)<!-- ignore -->
untuk setiap *trait* guna mengetahui detail cara mengimplementasikannya secara
manual.

*Trait* yang dicantumkan di sini adalah satu-satunya *trait* yang didefinisikan oleh
pustaka standar yang dapat diimplementasikan pada tipe Anda memakai `derive`.
*Trait* lain yang didefinisikan di pustaka standar tidak memiliki perilaku bawaan
yang masuk akal, sehingga terserah Anda untuk mengimplementasikannya dengan cara
yang masuk akal untuk apa yang ingin Anda capai.

Contoh *trait* yang tidak dapat diturunkan adalah `Display`, yang menangani
pemformatan untuk pengguna akhir. Anda sebaiknya selalu mempertimbangkan cara
yang tepat untuk menampilkan suatu tipe kepada pengguna akhir. Bagian tipe mana
yang boleh dilihat pengguna akhir? Bagian mana yang menurut mereka relevan?
Format data mana yang paling relevan bagi mereka? Kompilator Rust tidak memiliki
wawasan ini, sehingga tidak dapat menyediakan perilaku bawaan yang sesuai untuk
Anda.

Daftar *trait* yang dapat diturunkan dalam lampiran ini tidaklah lengkap: library
dapat mengimplementasikan `derive` untuk *trait* mereka sendiri, sehingga daftar
*trait* yang dapat Anda pakai bersama `derive` benar-benar terbuka.
Mengimplementasikan `derive` melibatkan pemakaian *macro* prosedural, yang dibahas
di bagian [“Macro `derive` Kustom”][custom-derive-macros]<!-- ignore --> di Bab
20.

### `Debug` untuk Keluaran Pemrogram

*Trait* `Debug` mengaktifkan pemformatan debug dalam string format, yang Anda
tandai dengan menambahkan `:?` di dalam placeholder `{}`.

*Trait* `Debug` memungkinkan Anda mencetak instance suatu tipe untuk keperluan
debugging, sehingga Anda dan pemrogram lain yang memakai tipe Anda dapat
memeriksa sebuah instance pada titik tertentu dalam eksekusi program.

*Trait* `Debug` diperlukan, misalnya, dalam pemakaian *macro* `assert_eq!`. *Macro*
ini mencetak nilai instance yang diberikan sebagai argumen jika asersi
kesamaannya gagal, supaya pemrogram dapat melihat mengapa kedua instance itu
tidak sama.

### `PartialEq` dan `Eq` untuk Perbandingan Kesamaan

*Trait* `PartialEq` memungkinkan Anda membandingkan instance suatu tipe untuk
memeriksa kesamaan dan mengaktifkan pemakaian operator `==` dan `!=`.

Menurunkan `PartialEq` mengimplementasikan metode `eq`. Ketika `PartialEq`
diturunkan pada *struct*, dua instance dianggap sama hanya jika _semua_ *field* sama,
dan instance-instance itu tidak sama jika _salah satu_ *field* tidak sama. Ketika
diturunkan pada *enum*, setiap varian sama dengan dirinya sendiri dan tidak sama
dengan varian lainnya.

*Trait* `PartialEq` diperlukan, misalnya, dalam pemakaian *macro* `assert_eq!`, yang
harus mampu membandingkan dua instance suatu tipe untuk kesamaan.

*Trait* `Eq` tidak memiliki metode. Tujuannya adalah memberi sinyal bahwa untuk
setiap nilai dari tipe yang dianotasi, nilai itu sama dengan dirinya sendiri.
*Trait* `Eq` hanya dapat diterapkan pada tipe yang juga mengimplementasikan
`PartialEq`, meskipun tidak semua tipe yang mengimplementasikan `PartialEq` dapat
mengimplementasikan `Eq`. Salah satu contohnya adalah tipe angka titik
mengambang: implementasi angka titik mengambang menyatakan bahwa dua instance
nilai not-a-number (`NaN`) tidak sama satu sama lain.

Contoh saat `Eq` diperlukan adalah untuk kunci dalam `HashMap<K, V>`, supaya
`HashMap<K, V>` dapat mengetahui apakah dua kunci itu sama.

### `PartialOrd` dan `Ord` untuk Perbandingan Urutan

*Trait* `PartialOrd` memungkinkan Anda membandingkan instance suatu tipe untuk
keperluan pengurutan. Tipe yang mengimplementasikan `PartialOrd` dapat dipakai
dengan operator `<`, `>`, `<=`, dan `>=`. Anda hanya dapat menerapkan *trait*
`PartialOrd` pada tipe yang juga mengimplementasikan `PartialEq`.

Menurunkan `PartialOrd` mengimplementasikan metode `partial_cmp`, yang
mengembalikan `Option<Ordering>` yang akan menjadi `None` ketika nilai yang
diberikan tidak menghasilkan urutan. Contoh nilai yang tidak menghasilkan
urutan, meskipun sebagian besar nilai bertipe itu dapat dibandingkan, adalah
nilai titik mengambang `NaN`. Memanggil `partial_cmp` dengan angka titik
mengambang mana pun dan nilai titik mengambang `NaN` akan mengembalikan `None`.

Ketika diturunkan pada *struct*, `PartialOrd` membandingkan dua instance dengan
membandingkan nilai di setiap *field* sesuai urutan kemunculan *field* tersebut
dalam definisi *struct*. Ketika diturunkan pada *enum*, varian *enum* yang
dideklarasikan lebih awal dalam definisi *enum* dianggap kurang dari varian yang
dicantumkan kemudian.

*Trait* `PartialOrd` diperlukan, misalnya, untuk metode `gen_range` dari *crate*
`rand` yang membangkitkan nilai acak dalam rentang yang ditentukan oleh ekspresi
rentang.

*Trait* `Ord` memungkinkan Anda mengetahui bahwa untuk dua nilai apa pun dari tipe
yang dianotasi, urutan yang valid akan selalu ada. *Trait* `Ord`
mengimplementasikan metode `cmp`, yang mengembalikan `Ordering`, bukan
`Option<Ordering>`, karena urutan yang valid akan selalu memungkinkan. Anda
hanya dapat menerapkan *trait* `Ord` pada tipe yang juga mengimplementasikan
`PartialOrd` dan `Eq` (dan `Eq` mensyaratkan `PartialEq`). Ketika diturunkan
pada *struct* dan *enum*, `cmp` berperilaku sama seperti implementasi hasil
penurunan untuk `partial_cmp` pada `PartialOrd`.

Contoh saat `Ord` diperlukan adalah ketika menyimpan nilai dalam `BTreeSet<T>`,
struktur data yang menyimpan data berdasarkan urutan sortir nilainya.

### `Clone` dan `Copy` untuk Menduplikasi Nilai

*Trait* `Clone` memungkinkan Anda secara eksplisit membuat salinan dalam dari
sebuah nilai, dan proses duplikasinya mungkin melibatkan menjalankan kode
arbitrer serta menyalin data di *heap*. Lihat bagian [“Variabel dan Data yang
Berinteraksi dengan Clone”][variables-and-data-interacting-with-clone]<!--
ignore --> di Bab 4 untuk informasi lebih lanjut tentang `Clone`.

Menurunkan `Clone` mengimplementasikan metode `clone`, yang ketika
diimplementasikan untuk seluruh tipe, memanggil `clone` pada setiap bagian tipe
tersebut. Artinya, semua *field* atau nilai dalam tipe itu juga harus
mengimplementasikan `Clone` untuk menurunkan `Clone`.

Contoh saat `Clone` diperlukan adalah ketika memanggil metode `to_vec` pada
*slice*. *Slice* tidak memiliki instance tipe yang dimuatnya, tetapi vektor yang
dikembalikan dari `to_vec` perlu memiliki instance-instancenya, sehingga
`to_vec` memanggil `clone` pada setiap item. Karena itu, tipe yang disimpan
dalam *slice* harus mengimplementasikan `Clone`.

*Trait* `Copy` memungkinkan Anda menduplikasi nilai hanya dengan menyalin bit yang
tersimpan di *stack*; tidak ada kode arbitrer yang diperlukan. Lihat bagian
[“Data yang Hanya Ada di Stack: Copy”][stack-only-data-copy]<!-- ignore --> di
Bab 4 untuk informasi lebih lanjut tentang `Copy`.

*Trait* `Copy` tidak mendefinisikan metode apa pun untuk mencegah pemrogram
meng-overload metode tersebut dan melanggar asumsi bahwa tidak ada kode
arbitrer yang dijalankan. Dengan demikian, semua pemrogram dapat berasumsi bahwa
menyalin nilai akan berlangsung sangat cepat.

Anda dapat menurunkan `Copy` pada tipe apa pun yang semua bagiannya
mengimplementasikan `Copy`. Tipe yang mengimplementasikan `Copy` juga harus
mengimplementasikan `Clone`, karena tipe yang mengimplementasikan `Copy`
memiliki implementasi `Clone` yang trivial dan menjalankan tugas yang sama
seperti `Copy`.

*Trait* `Copy` jarang diperlukan; tipe yang mengimplementasikan `Copy` memiliki
optimasi yang tersedia, artinya Anda tidak perlu memanggil `clone`, yang membuat
kode menjadi lebih ringkas.

Semua yang mungkin dilakukan dengan `Copy` juga dapat Anda capai dengan `Clone`,
tetapi kodenya mungkin lebih lambat atau harus memakai `clone` di beberapa
tempat.

### `Hash` untuk Memetakan Nilai ke Nilai Berukuran Tetap

*Trait* `Hash` memungkinkan Anda mengambil instance suatu tipe berukuran arbitrer
dan memetakan instance itu ke nilai berukuran tetap memakai fungsi hashing.
Menurunkan `Hash` mengimplementasikan metode `hash`. Implementasi hasil
penurunan metode `hash` menggabungkan hasil pemanggilan `hash` pada setiap
bagian tipe, artinya semua *field* atau nilai juga harus mengimplementasikan
`Hash` untuk menurunkan `Hash`.

Contoh saat `Hash` diperlukan adalah ketika menyimpan kunci dalam `HashMap<K,
V>` untuk menyimpan data secara efisien.

### `Default` untuk Nilai Bawaan

*Trait* `Default` memungkinkan Anda membuat nilai bawaan untuk suatu tipe.
Menurunkan `Default` mengimplementasikan fungsi `default`. Implementasi hasil
penurunan fungsi `default` memanggil fungsi `default` pada setiap bagian tipe,
artinya semua *field* atau nilai dalam tipe itu juga harus mengimplementasikan
`Default` untuk menurunkan `Default`.

Fungsi `Default::default` umum dipakai bersama sintaks update *struct* yang
dibahas di bagian [“Membuat Instance dengan Sintaks Update
Struct”][creating-instances-from-other-instances-with-struct-update-syntax]<!--
ignore --> di Bab 5. Anda dapat mengkustomisasi beberapa field struct, lalu
menetapkan dan memakai nilai bawaan untuk *field* sisanya dengan
`..Default::default()`.

*Trait* `Default` diperlukan, misalnya, ketika Anda memakai metode
`unwrap_or_default` pada instance `Option<T>`. Jika `Option<T>`-nya adalah
`None`, metode `unwrap_or_default` akan mengembalikan hasil `Default::default`
untuk tipe `T` yang tersimpan dalam `Option<T>`.

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros
