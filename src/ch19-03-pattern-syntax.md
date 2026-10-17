## Sintaks Pola

Pada bagian ini, kita menghimpun semua sintaks yang valid pada pola dan
membahas mengapa serta kapan Anda mungkin ingin memakai masing-masing.

### Mencocokkan Literal

Seperti yang Anda lihat di Bab 6, Anda bisa mencocokkan pola terhadap literal
secara langsung. Kode berikut memberi beberapa contoh:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

Kode ini mencetak `one` karena nilai pada `x` adalah `1`. Sintaks ini berguna
ketika Anda ingin kode Anda mengambil tindakan jika ia mendapat nilai konkret
tertentu.

### Mencocokkan Variabel Bernama

Variabel bernama adalah pola *irrefutable* yang cocok dengan nilai apa pun, dan
kita telah memakainya berkali-kali di buku ini. Akan tetapi, ada satu
kerumitan ketika Anda memakai variabel bernama di ekspresi `match`, `if let`,
atau `while let`. Karena setiap jenis ekspresi ini memulai *scope* baru,
variabel yang dideklarasikan sebagai bagian dari pola di dalam ekspresi ini
akan melakukan shadowing terhadap variabel bernama sama di luar konstruksi
itu, sebagaimana halnya semua variabel. Di Listing 19-11, kita
mendeklarasikan variabel bernama `x` dengan nilai `Some(5)` dan variabel `y`
dengan nilai `10`. Kita kemudian membuat ekspresi `match` pada nilai `x`.
Lihat pola-pola di arm match dan `println!` di akhir, dan coba tebak apa yang
akan dicetak kode itu sebelum menjalankannya atau membaca lebih lanjut.

<Listing number="19-11" file-name="src/main.rs" caption="Ekspresi `match` dengan arm yang memperkenalkan variabel baru yang melakukan shadowing terhadap variabel `y` yang sudah ada">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

Mari kita telusuri apa yang terjadi saat ekspresi `match` berjalan. Pola di
arm match pertama tidak cocok dengan nilai `x` yang didefinisikan, jadi kode
berlanjut.

Pola di arm match kedua memperkenalkan variabel baru bernama `y` yang akan
cocok dengan nilai apa pun di dalam nilai `Some`. Karena kita berada di *scope*
baru di dalam ekspresi `match`, ini variabel `y` yang baru, bukan `y` yang
kita deklarasikan di awal dengan nilai `10`. Binding `y` baru ini akan cocok
dengan nilai apa pun di dalam `Some`, yaitu yang kita miliki di `x`. Karena
itu, `y` baru ini mengikat nilai bagian dalam `Some` di `x`. Nilai itu adalah
`5`, jadi ekspresi untuk arm itu dijalankan dan mencetak `Matched, y = 5`.

Jika `x` adalah nilai `None` alih-alih `Some(5)`, pola di dua arm pertama
tidak akan cocok, jadi nilainya akan cocok dengan underscore. Kita tidak
memperkenalkan variabel `x` pada pola arm underscore, jadi `x` di ekspresi
itu tetaplah `x` luar yang belum di-shadow. Dalam kasus hipotetis ini,
`match` akan mencetak `Default case, x = None`.

Ketika ekspresi `match` selesai, *scope*-nya berakhir, begitu pula *scope* `y`
bagian dalam. `println!` terakhir menghasilkan `at the end: x = Some(5), y =
10`.

Untuk membuat ekspresi `match` yang membandingkan nilai `x` dan `y` luar,
alih-alih memperkenalkan variabel baru yang melakukan shadowing terhadap
variabel `y` yang sudah ada, kita perlu memakai kondisional *match guard*.
Kita akan membahas *match guard* nanti di bagian [“Menambahkan Kondisional
dengan Match Guard”](#adding-conditionals-with-match-guards)<!-- ignore -->.

<!-- Old headings. Do not remove or links may break. -->
<a id="multiple-patterns"></a>

### Mencocokkan Banyak Pola

Pada ekspresi `match`, Anda bisa mencocokkan banyak pola menggunakan sintaks
`|`, yang merupakan operator pola _or_. Contohnya, pada kode berikut, kita
mencocokkan nilai `x` terhadap arm-arm match, yang pertamanya memiliki opsi
_or_, artinya jika nilai `x` cocok dengan salah satu nilai di arm itu, kode
arm itu akan berjalan:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

Kode ini mencetak `one or two`.

### Mencocokkan Rentang Nilai dengan `..=`

Sintaks `..=` memungkinkan kita mencocokkan rentang nilai yang inklusif. Pada
kode berikut, ketika sebuah pola cocok dengan salah satu nilai di dalam
rentang yang diberikan, arm itu akan dijalankan:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

Jika `x` adalah `1`, `2`, `3`, `4`, atau `5`, arm pertama akan cocok. Sintaks
ini lebih nyaman untuk banyak nilai match daripada memakai operator `|` untuk
mengekspresikan gagasan yang sama; jika kita memakai `|`, kita harus
menentukan `1 | 2 | 3 | 4 | 5`. Menentukan rentang jauh lebih singkat,
apalagi jika kita ingin mencocokkan, katakanlah, angka apa pun antara 1 dan
1.000!

Kompilator memeriksa bahwa rentangnya tidak kosong pada waktu kompilasi, dan
karena satu-satunya tipe yang bisa dipakai Rust untuk mengetahui apakah
sebuah rentang kosong atau tidak adalah `char` dan nilai numerik, rentang
hanya diizinkan untuk nilai numerik atau `char`.

Berikut contoh memakai rentang nilai `char`:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

Rust bisa mengetahui bahwa `'c'` berada di dalam rentang pola pertama dan
mencetak `early ASCII letter`.

### Mendestrukturisasi untuk Memecah Nilai

Kita juga bisa memakai pola untuk mendestrukturisasi *struct*, *enum*, dan *tuple*
untuk memakai bagian-bagian berbeda dari nilai-nilai ini. Mari kita telusuri
setiap nilai.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs"></a>

#### Struct

Listing 19-12 menunjukkan *struct* `Point` dengan dua *field*, `x` dan `y`, yang
bisa kita pecah menggunakan pola dengan pernyataan `let`.

<Listing number="19-12" file-name="src/main.rs" caption="Mendestrukturisasi field-field struct menjadi variabel-variabel terpisah">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

Kode ini membuat variabel `a` dan `b` yang cocok dengan nilai *field* `x` dan
`y` dari *struct* `p`. Contoh ini menunjukkan bahwa nama variabel pada pola
tidak harus sama dengan nama *field* *struct*. Akan tetapi, umum untuk
menyesuaikan nama variabel dengan nama *field* supaya lebih mudah mengingat
variabel mana yang berasal dari *field* mana. Karena pemakaian umum ini, dan
karena menulis `let Point { x: x, y: y } = p;` mengandung banyak duplikasi,
Rust punya bentuk singkat untuk pola yang mencocokkan *field* *struct*: Anda
hanya perlu mencantumkan nama *field* *struct*, dan variabel yang dibuat dari
pola itu akan memiliki nama yang sama. Listing 19-13 berperilaku sama dengan
kode di Listing 19-12, tetapi variabel yang dibuat di pola `let` adalah `x`
dan `y` alih-alih `a` dan `b`.

<Listing number="19-13" file-name="src/main.rs" caption="Mendestrukturisasi field struct menggunakan bentuk singkat field struct">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

Kode ini membuat variabel `x` dan `y` yang cocok dengan *field* `x` dan `y`
dari variabel `p`. Hasilnya adalah variabel `x` dan `y` memuat nilai dari
*struct* `p`.

Kita juga bisa mendestrukturisasi dengan nilai literal sebagai bagian dari
pola *struct* alih-alih membuat variabel untuk semua *field*. Melakukannya
memungkinkan kita menguji sebagian *field* untuk nilai tertentu sambil membuat
variabel untuk mendestrukturisasi *field* lainnya.

Di Listing 19-14, kita punya ekspresi `match` yang memisahkan nilai `Point`
menjadi tiga kasus: titik yang terletak tepat di sumbu `x` (yang benar ketika
`y = 0`), di sumbu `y` (`x = 0`), atau tidak di sumbu mana pun.

<Listing number="19-14" file-name="src/main.rs" caption="Mendestrukturisasi dan mencocokkan nilai literal dalam satu pola">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

Arm pertama akan cocok dengan titik mana pun yang terletak di sumbu `x`
dengan menentukan bahwa *field* `y` cocok jika nilainya cocok dengan literal
`0`. Pola itu tetap membuat variabel `x` yang bisa kita pakai di kode untuk
arm ini.

Serupa, arm kedua cocok dengan titik mana pun di sumbu `y` dengan menentukan
bahwa *field* `x` cocok jika nilainya `0` dan membuat variabel `y` untuk nilai
*field* `y`. Arm ketiga tidak menentukan literal apa pun, jadi ia cocok dengan
`Point` lain mana pun dan membuat variabel untuk *field* `x` maupun `y`.

Pada contoh ini, nilai `p` cocok dengan arm kedua karena `x` memuat `0`, jadi
kode ini akan mencetak `On the y axis at 7`.

Ingat bahwa ekspresi `match` berhenti memeriksa arm begitu menemukan pola
pertama yang cocok, jadi meskipun `Point { x: 0, y: 0 }` berada di sumbu `x`
dan sumbu `y`, kode ini hanya akan mencetak `On the x axis at 0`.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-enums"></a>

#### Enum

Kita telah mendestrukturisasi *enum* di buku ini (contohnya, Listing 6-5 di Bab
6), tetapi kita belum secara eksplisit membahas bahwa pola untuk
mendestrukturisasi *enum* berpadanan dengan cara data yang tersimpan di dalam
*enum* itu didefinisikan. Sebagai contoh, di Listing 19-15, kita memakai *enum*
`Message` dari Listing 6-2 dan menulis `match` dengan pola yang akan
mendestrukturisasi setiap nilai bagian dalamnya.

<Listing number="19-15" file-name="src/main.rs" caption="Mendestrukturisasi varian enum yang menampung berbagai jenis nilai">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

Kode ini akan mencetak `Change color to red 0, green 160, and blue 255`. Coba
ubah nilai `msg` untuk melihat kode dari arm-arm lain berjalan.

Untuk varian *enum* tanpa data apa pun, seperti `Message::Quit`, kita tidak bisa
mendestrukturisasi nilainya lebih jauh. Kita hanya bisa mencocokkan nilai
literal `Message::Quit`, dan tidak ada variabel pada pola itu.

Untuk varian *enum* yang mirip *struct*, seperti `Message::Move`, kita bisa
memakai pola yang mirip dengan pola yang kita tentukan untuk mencocokkan
*struct*. Setelah nama varian, kita menaruh kurung kurawal lalu mencantumkan
*field*-field dengan variabel supaya kita memecah bagian-bagiannya untuk dipakai
di kode untuk arm ini. Di sini kita memakai bentuk singkat seperti yang kita
lakukan di Listing 19-13.

Untuk varian *enum* yang mirip *tuple*, seperti `Message::Write` yang menampung
*tuple* dengan satu elemen dan `Message::ChangeColor` yang menampung *tuple*
dengan tiga elemen, polanya mirip dengan pola yang kita tentukan untuk
mencocokkan *tuple*. Jumlah variabel pada pola harus sama dengan jumlah elemen
pada varian yang kita cocokkan.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-nested-structs-and-enums"></a>

#### Struct dan Enum Bersarang

Sejauh ini, semua contoh kita mencocokkan *struct* atau *enum* sedalam satu
tingkat, tetapi pencocokan bisa bekerja pada item yang bersarang juga!
Contohnya, kita bisa me-refactor kode di Listing 19-15 untuk mendukung warna
RGB dan HSV pada pesan `ChangeColor`, seperti yang ditunjukkan di Listing
19-16.

<Listing number="19-16" caption="Mencocokkan enum bersarang">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

Pola arm pertama pada ekspresi `match` cocok dengan varian *enum*
`Message::ChangeColor` yang memuat varian `Color::Rgb`; kemudian, pola itu
mengikat tiga nilai `i32` bagian dalam. Pola arm kedua juga cocok dengan
varian *enum* `Message::ChangeColor`, tetapi *enum* bagian dalamnya cocok dengan
`Color::Hsv`. Kita bisa menentukan kondisi kompleks ini dalam satu ekspresi
`match`, meskipun ada dua *enum* yang terlibat.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs-and-tuples"></a>

#### Struct dan Tuple

Kita bisa mencampur, mencocokkan, dan menyarangkan pola destrukturisasi
dengan cara yang bahkan lebih kompleks. Contoh berikut menunjukkan
destrukturisasi rumit tempat kita menyarangkan *struct* dan *tuple* di dalam
sebuah *tuple* dan mendestrukturisasi semua nilai primitifnya:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

Kode ini memungkinkan kita memecah tipe kompleks menjadi bagian-bagian
komponennya supaya kita bisa memakai nilai-nilai yang kita minati secara
terpisah.

Mendestrukturisasi dengan pola adalah cara yang nyaman untuk memakai
bagian-bagian nilai, seperti nilai dari setiap *field* di *struct*, secara
terpisah satu sama lain.

<a id="ignoring-values-in-a-pattern"></a>
### Mengabaikan Nilai dalam Pola

Anda telah melihat bahwa terkadang berguna untuk mengabaikan nilai pada pola,
seperti pada arm terakhir `match`, untuk mendapatkan catch-all yang tidak
benar-benar melakukan apa pun tetapi memperhitungkan semua nilai yang
mungkin tersisa. Ada beberapa cara untuk mengabaikan seluruh nilai atau
sebagian nilai pada pola: memakai pola `_` (yang telah Anda lihat), memakai
pola `_` di dalam pola lain, memakai nama yang diawali underscore, atau
memakai `..` untuk mengabaikan sisa nilai. Mari kita jelajahi bagaimana dan
mengapa memakai masing-masing pola ini.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-entire-value-with-_"></a>

#### Seluruh Nilai dengan `_`

Kita telah memakai underscore sebagai pola wildcard yang akan cocok dengan
nilai apa pun tetapi tidak mengikat ke nilainya. Ini sangat berguna sebagai
arm terakhir di ekspresi `match`, tetapi kita juga bisa memakainya di pola
mana pun, termasuk parameter fungsi, seperti yang ditunjukkan di Listing
19-17.

<Listing number="19-17" file-name="src/main.rs" caption="Memakai `_` di tanda tangan fungsi">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

Kode ini akan sepenuhnya mengabaikan nilai `3` yang diteruskan sebagai
argumen pertama, dan akan mencetak `This code only uses the y parameter: 4`.

Dalam kebanyakan kasus, ketika Anda tidak lagi membutuhkan parameter fungsi
tertentu, Anda akan mengubah tanda tangannya supaya tidak menyertakan
parameter yang tidak terpakai itu. Mengabaikan parameter fungsi bisa sangat
berguna dalam kasus ketika, contohnya, Anda mengimplementasikan sebuah *trait*
yang mengharuskan tanda tangan tipe tertentu, tetapi badan fungsi di
implementasi Anda tidak membutuhkan salah satu parameternya. Anda pun
terhindar dari peringatan kompilator tentang parameter fungsi yang tidak
terpakai, yang akan Anda dapatkan jika memakai nama.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-parts-of-a-value-with-a-nested-_"></a>

#### Sebagian Nilai dengan `_` Bersarang

Kita juga bisa memakai `_` di dalam pola lain untuk mengabaikan sebagian
nilai saja, misalnya ketika kita ingin menguji sebagian nilai saja tetapi
tidak memakai bagian lain di kode yang ingin kita jalankan. Listing 19-18
menunjukkan kode yang bertanggung jawab mengelola nilai sebuah pengaturan.
Persyaratan bisnisnya adalah pengguna tidak boleh diizinkan menimpa
kustomisasi yang sudah ada dari sebuah pengaturan, tetapi boleh menghapus
nilai pengaturan itu dan memberinya nilai jika saat ini belum diset.

<Listing number="19-18" caption="Memakai underscore di dalam pola yang mencocokkan varian `Some` ketika kita tidak perlu memakai nilai di dalam `Some`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

Kode ini akan mencetak `Can't overwrite an existing customized value` lalu
`setting is Some(5)`. Di arm match pertama, kita tidak perlu mencocokkan atau
memakai nilai di dalam salah satu varian `Some`, tetapi kita perlu menguji
kasus ketika `setting_value` dan `new_setting_value` adalah varian `Some`.
Dalam kasus itu, kita mencetak alasan tidak mengubah `setting_value`, dan
nilai itu tidak jadi diubah.

Dalam semua kasus lain (jika `setting_value` atau `new_setting_value` adalah
`None`) yang diekspresikan oleh pola `_` di arm kedua, kita ingin mengizinkan
`new_setting_value` menjadi `setting_value`.

Kita juga bisa memakai underscore di beberapa tempat dalam satu pola untuk
mengabaikan nilai-nilai tertentu. Listing 19-19 menunjukkan contoh
mengabaikan nilai kedua dan keempat pada *tuple* berisi lima item.

<Listing number="19-19" caption="Mengabaikan banyak bagian dari sebuah tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

Kode ini akan mencetak `Some numbers: 2, 8, 32`, dan nilai `4` serta `16`
akan diabaikan.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-unused-variable-by-starting-its-name-with-_"></a>

#### Variabel yang Tidak Dipakai dengan Mengawali Namanya dengan `_`

Jika Anda membuat variabel tetapi tidak memakainya di mana pun, Rust biasanya
akan mengeluarkan peringatan karena variabel yang tidak terpakai bisa menjadi
bug. Akan tetapi, terkadang berguna untuk bisa membuat variabel yang belum
akan Anda pakai, seperti saat Anda membuat prototipe atau baru memulai
proyek. Dalam situasi ini, Anda bisa memberi tahu Rust untuk tidak
memperingatkan Anda tentang variabel yang tidak terpakai itu dengan mengawali
nama variabelnya dengan underscore. Di Listing 19-20, kita membuat dua
variabel yang tidak terpakai, tetapi ketika kita mengompilasi kode ini, kita
seharusnya hanya mendapat peringatan tentang salah satunya.

<Listing number="19-20" file-name="src/main.rs" caption="Mengawali nama variabel dengan underscore untuk menghindari peringatan variabel tidak terpakai">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

Di sini, kita mendapat peringatan tentang tidak memakai variabel `y`, tetapi
kita tidak mendapat peringatan tentang tidak memakai `_x`.

Perhatikan bahwa ada perbedaan halus antara memakai `_` saja dan memakai nama
yang diawali underscore. Sintaks `_x` tetap mengikat nilainya ke variabel,
sedangkan `_` tidak mengikat sama sekali. Untuk menunjukkan kasus ketika
perbedaan ini penting, Listing 19-21 akan memberi kita galat.

<Listing number="19-21" caption="Variabel tidak terpakai yang diawali underscore tetap mengikat nilainya, yang bisa mengambil kepemilikan nilai itu.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

Kita akan menerima galat karena nilai `s` tetap akan dipindahkan ke `_s`,
yang mencegah kita memakai `s` lagi. Akan tetapi, memakai underscore saja
tidak pernah mengikat ke nilainya. Listing 19-22 akan terkompilasi tanpa
galat apa pun karena `s` tidak dipindahkan ke `_`.

<Listing number="19-22" caption="Memakai underscore tidak mengikat nilainya.">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

Kode ini bekerja dengan baik karena kita tidak pernah mengikat `s` ke apa
pun; ia tidak dipindahkan.

<a id="ignoring-remaining-parts-of-a-value-with-"></a>

#### Sisa Nilai dengan `..`

Dengan nilai yang punya banyak bagian, kita bisa memakai sintaks `..` untuk
memakai bagian-bagian tertentu dan mengabaikan sisanya, menghindari kebutuhan
mencantumkan underscore untuk setiap nilai yang diabaikan. Pola `..`
mengabaikan bagian mana pun dari nilai yang belum kita cocokkan secara
eksplisit di sisa pola. Di Listing 19-23, kita punya *struct* `Point` yang
menampung koordinat di ruang tiga dimensi. Pada ekspresi `match`, kita ingin
mengoperasikan koordinat `x` saja dan mengabaikan nilai di *field* `y` dan `z`.

<Listing number="19-23" caption="Mengabaikan semua field `Point` kecuali `x` dengan memakai `..`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs:here}}
```

</Listing>

Kita mencantumkan nilai `x` lalu menyertakan pola `..` saja. Ini lebih cepat
daripada harus mencantumkan `y: _` dan `z: _`, terutama saat kita bekerja
dengan *struct* yang punya banyak *field* dalam situasi ketika hanya satu atau
dua *field* yang relevan.

Sintaks `..` akan meluas menjadi nilai sebanyak yang dibutuhkannya. Listing
19-24 menunjukkan cara memakai `..` dengan *tuple*.

<Listing number="19-24" file-name="src/main.rs" caption="Mencocokkan hanya nilai pertama dan terakhir pada sebuah tuple dan mengabaikan semua nilai lainnya">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

Pada kode ini, nilai pertama dan terakhir dicocokkan dengan `first` dan
`last`. `..` akan mencocokkan dan mengabaikan semua yang ada di tengah.

Akan tetapi, pemakaian `..` harus tidak ambigu. Jika tidak jelas nilai mana
yang dimaksudkan untuk dicocokkan dan mana yang harus diabaikan, Rust akan
memberi kita galat. Listing 19-25 menunjukkan contoh pemakaian `..` secara
ambigu, jadi kode ini tidak akan terkompilasi.

<Listing number="19-25" file-name="src/main.rs" caption="Upaya memakai `..` dengan cara yang ambigu">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

Ketika kita mengompilasi contoh ini, kita mendapat galat ini:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

Mustahil bagi Rust untuk menentukan berapa banyak nilai pada *tuple* yang harus
diabaikan sebelum mencocokkan sebuah nilai dengan `second` dan kemudian
berapa banyak nilai lagi yang harus diabaikan setelahnya. Kode ini bisa
berarti kita ingin mengabaikan `2`, mengikat `second` ke `4`, lalu
mengabaikan `8`, `16`, dan `32`; atau kita ingin mengabaikan `2` dan `4`,
mengikat `second` ke `8`, lalu mengabaikan `16` dan `32`; dan seterusnya.
Nama variabel `second` tidak berarti apa-apa secara khusus bagi Rust, jadi
kita mendapat galat kompilator karena memakai `..` di dua tempat seperti ini
bersifat ambigu.

<!-- Old headings. Do not remove or links may break. -->

<a id="extra-conditionals-with-match-guards"></a>

<a id="adding-conditionals-with-match-guards"></a>
### Menambahkan Kondisional dengan Match Guard

_Match guard_ (pengawal match) adalah kondisi `if` tambahan, yang ditentukan
setelah pola pada arm `match`, yang juga harus cocok agar arm itu dipilih.
*Match guard* berguna untuk mengekspresikan gagasan yang lebih kompleks
daripada yang diizinkan pola saja. Akan tetapi, perhatikan bahwa *match guard*
hanya tersedia pada ekspresi `match`, bukan pada ekspresi `if let` atau
`while let`.

Kondisi itu bisa memakai variabel yang dibuat di pola. Listing 19-26
menunjukkan `match` yang arm pertamanya memiliki pola `Some(x)` dan juga
memiliki *match guard* `if x % 2 == 0` (yang akan bernilai `true` jika angkanya
genap).

<Listing number="19-26" caption="Menambahkan match guard ke sebuah pola">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

Contoh ini akan mencetak `The number 4 is even`. Ketika `num` dibandingkan
dengan pola di arm pertama, ia cocok karena `Some(4)` cocok dengan `Some(x)`.
Kemudian, *match guard* memeriksa apakah sisa pembagian `x` dengan 2 sama
dengan 0, dan karena memang begitu, arm pertama dipilih.

Jika `num` adalah `Some(5)`, *match guard* di arm pertama akan bernilai `false`
karena sisa pembagian 5 dengan 2 adalah 1, yang tidak sama dengan 0. Rust
kemudian akan pergi ke arm kedua, yang akan cocok karena arm kedua tidak
memiliki *match guard* dan karena itu cocok dengan varian `Some` mana pun.

Tidak ada cara untuk mengekspresikan kondisi `if x % 2 == 0` di dalam sebuah
pola, jadi *match guard* memberi kita kemampuan untuk mengekspresikan logika
ini. Sisi buruk dari ekspresivitas tambahan ini adalah kompilator tidak
mencoba memeriksa ekshaustivitas ketika ekspresi *match guard* terlibat.

Saat membahas Listing 19-11, kami menyebutkan bahwa kita bisa memakai match
guard untuk memecahkan masalah shadowing pola kita. Ingat bahwa kita membuat
variabel baru di dalam pola pada ekspresi `match` alih-alih memakai variabel
di luar `match`. Variabel baru itu berarti kita tidak bisa menguji nilai
variabel luar. Listing 19-27 menunjukkan cara memakai *match guard* untuk
memperbaiki masalah ini.

<Listing number="19-27" file-name="src/main.rs" caption="Memakai match guard untuk menguji kesamaan dengan variabel luar">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

Kode ini sekarang akan mencetak `Default case, x = Some(5)`. Pola di arm
match kedua tidak memperkenalkan variabel `y` baru yang akan melakukan
shadowing terhadap `y` luar, yang berarti kita bisa memakai `y` luar di match
guard. Alih-alih menentukan polanya sebagai `Some(y)`, yang akan melakukan
shadowing terhadap `y` luar, kita menentukan `Some(n)`. Ini membuat variabel
baru `n` yang tidak melakukan shadowing terhadap apa pun karena tidak ada
variabel `n` di luar `match`.

*Match guard* `if n == y` bukanlah pola dan karena itu tidak memperkenalkan
variabel baru. `y` ini _adalah_ `y` luar alih-alih `y` baru yang
menaunginya, dan kita bisa mencari nilai yang sama dengan nilai `y` luar
dengan membandingkan `n` dengan `y`.

Anda juga bisa memakai operator _or_ `|` di *match guard* untuk menentukan
beberapa pola; kondisi *match guard* akan berlaku untuk semua pola itu. Listing
19-28 menunjukkan prioritas ketika menggabungkan pola yang memakai `|` dengan
*match guard*. Bagian penting dari contoh ini adalah bahwa *match guard* `if y`
berlaku untuk `4`, `5`, _dan_ `6`, meskipun mungkin terlihat seperti `if y`
hanya berlaku untuk `6`.

<Listing number="19-28" caption="Menggabungkan beberapa pola dengan match guard">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

Kondisi match menyatakan bahwa arm itu hanya cocok jika nilai `x` sama
dengan `4`, `5`, atau `6` _dan_ jika `y` bernilai `true`. Ketika kode ini
berjalan, pola arm pertama cocok karena `x` adalah `4`, tetapi *match guard*
`if y` bernilai `false`, jadi arm pertama tidak dipilih. Kode berlanjut ke
arm kedua, yang cocok, dan program ini mencetak `no`. Alasannya adalah
kondisi `if` berlaku untuk seluruh pola `4 | 5 | 6`, bukan hanya untuk nilai
terakhir `6`. Dengan kata lain, prioritas *match guard* dalam hubungannya
dengan sebuah pola berperilaku seperti ini:

```text
(4 | 5 | 6) if y => ...
```

alih-alih seperti ini:

```text
4 | 5 | (6 if y) => ...
```

Setelah menjalankan kodenya, perilaku prioritasnya terbukti: jika *match guard*
hanya diterapkan pada nilai terakhir dalam daftar nilai yang ditentukan
menggunakan operator `|`, arm itu akan cocok dan program akan mencetak `yes`.

<!-- Old headings. Do not remove or links may break. -->

<a id="-bindings"></a>

### Memakai Binding `@`

Operator _at_ `@` memungkinkan kita membuat variabel yang menampung sebuah
nilai pada saat yang sama kita menguji nilai itu untuk kecocokan pola. Di
Listing 19-29, kita ingin menguji bahwa *field* `id` dari `Message::Hello`
berada di dalam rentang `3..=7`. Kita juga ingin mengikat nilainya ke
variabel `id` supaya bisa kita pakai di kode yang terkait dengan arm itu.

<Listing number="19-29" caption="Memakai `@` untuk mengikat ke nilai di dalam pola sambil mengujinya">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

Contoh ini akan mencetak `Found an id in range: 5`. Dengan menentukan `id @`
sebelum rentang `3..=7`, kita menangkap nilai apa pun yang cocok dengan
rentang itu ke variabel bernama `id` sambil juga menguji bahwa nilainya cocok
dengan pola rentangnya.

Di arm kedua, tempat kita hanya menentukan rentang di polanya, kode yang
terkait dengan arm itu tidak memiliki variabel yang memuat nilai aktual *field*
`id`. Nilai *field* `id` bisa saja 10, 11, atau 12, tetapi kode yang menyertai
pola itu tidak tahu yang mana. Kode pola itu tidak bisa memakai nilai dari
*field* `id` karena kita belum menyimpan nilai `id` di variabel.

Di arm terakhir, tempat kita menentukan variabel tanpa rentang, kita memang
memiliki nilainya untuk dipakai di kode arm itu dalam variabel bernama `id`.
Alasannya adalah kita telah memakai sintaks bentuk singkat *field* *struct*.
Tetapi kita belum menerapkan pengujian apa pun pada nilai di *field* `id` di
arm ini, seperti yang kita lakukan di dua arm pertama: nilai apa pun akan
cocok dengan pola ini.

Memakai `@` memungkinkan kita menguji sebuah nilai dan menyimpannya di
variabel dalam satu pola.

## Ringkasan

Pola di Rust sangat berguna untuk membedakan berbagai jenis data. Ketika
dipakai di ekspresi `match`, Rust memastikan pola-pola Anda mencakup setiap
nilai yang mungkin, atau program Anda tidak akan terkompilasi. Pola di
pernyataan `let` dan parameter fungsi membuat konstruksi-konstruksi itu lebih
berguna, memungkinkan destrukturisasi nilai menjadi bagian-bagian yang lebih
kecil dan menetapkan bagian-bagian itu ke variabel. Kita bisa membuat pola
sederhana atau kompleks sesuai kebutuhan kita.

Berikutnya, untuk bab kedua terakhir buku ini, kita akan melihat beberapa
aspek lanjutan dari berbagai fitur Rust.
