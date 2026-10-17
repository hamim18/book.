<!-- Old headings. Do not remove or links may break. -->

<a id="the-match-control-flow-operator"></a>

<a id="the-match-control-flow-construct"></a>
## Konstruk Alur Kontrol `match`

Rust memiliki konstruk control flow yang sangat tangguh bernama `match` yang
memungkinkan Anda membandingkan sebuah nilai dengan serangkaian pattern, lalu
mengeksekusi kode berdasarkan pattern mana yang cocok. Pattern dapat tersusun dari
nilai literal, nama variable, wildcard, dan banyak hal lain; [Bab
19][ch19-00-patterns]<!-- ignore --> membahas semua jenis pattern yang berbeda
dan apa yang dilakukannya. Kekuatan `match` berasal dari expressiveness patternnya
dan fakta bahwa *compiler* (kompilator) memastikan semua kasus yang mungkin
tertangani.

Bayangkan expression `match` seperti mesin penyortir koin: koin-koin meluncur
menuruni lintasan yang memiliki lubang-lubang dengan berbagai ukuran, dan
setiap koin jatuh melalui lubang pertama yang ditemuinya yang pas untuk ukurannya.
Dengan cara yang sama, nilai melewati setiap pattern dalam `match`, dan pada pattern
pertama yang “muat” dengan nilai itu, nilai tersebut jatuh ke blok kode
terkait untuk dipakai selama eksekusi.

Berbicara tentang koin, mari kita pakai koin sebagai contoh dengan `match`!
Kita dapat menulis sebuah fungsi yang menerima koin AS yang tidak diketahui
dan, dengan cara yang mirip mesin penghitung, menentukan koin apa itu dan
mengembalikan nilainya dalam sen, seperti yang ditunjukkan pada Listing 6-3.

<Listing number="6-3" caption="Sebuah enum dan expression `match` yang memakai varian-varian enum sebagai patternnya">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Listing>

Mari kita bedah `match` pada fungsi `value_in_cents`. Pertama, kita menuliskan
keyword `match` yang diikuti sebuah expression, yang pada kasus ini adalah nilai
`coin`. Ini tampak sangat mirip dengan expression kondisional yang dipakai
bersama `if`, tetapi ada perbedaan besar: pada `if`, kondisinya harus
mengevaluasi menjadi nilai Boolean, sedangkan di sini ia dapat typed apa
pun. Type `coin` pada contoh ini adalah *enum* `Coin` yang kita definisikan di
baris pertama.

Berikutnya adalah *arm*-*arm* `match`. Sebuah *arm* (lengan) memiliki dua
bagian: pattern dan kode. Arm pertama di sini memiliki pattern berupa nilai
`Coin::Penny`, lalu operator `=>` yang memisahkan pattern dan kode yang
dijalankan. Kode pada kasus ini hanyalah nilai `1`. Setiap *arm* dipisahkan dari
*arm* berikutnya dengan koma.

Ketika expression `match` dieksekusi, ia membandingkan nilai hasilnya dengan
pattern setiap *arm*, secara berurutan. Jika sebuah pattern cocok dengan nilainya,
kode yang terkait dengan pattern itu dieksekusi. Jika pattern itu tidak cocok dengan
nilainya, eksekusi berlanjut ke *arm* berikutnya, mirip seperti mesin penyortir
koin. Kita dapat memiliki *arm* sebanyak yang kita butuhkan: pada Listing 6-3,
`match` kita memiliki empat *arm*.

Kode yang terkait dengan setiap *arm* adalah expression, dan nilai hasil expression
pada *arm* yang cocok adalah nilai yang dikembalikan untuk keseluruhan expression
`match`.

Biasanya kita tidak memakai kurung kurawal jika kode *arm* match pendek, seperti
pada Listing 6-3 yang setiap *arm*-nya hanya mengembalikan sebuah nilai. Jika
Anda ingin menjalankan beberapa baris kode di dalam *arm* match, Anda harus
memakai kurung kurawal, dan koma setelah *arm* itu bersifat opsional. Contohnya,
kode berikut mencetak “Lucky penny!” setiap kali methodnya dipanggil dengan
`Coin::Penny`, tetapi ia tetap mengembalikan nilai terakhir bloknya, yaitu
`1`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```

<a id="patterns-that-bind-to-values"></a>
### Pattern yang Mengikat Nilai

Fitur *arm* match lain yang berguna adalah kemampuannya untuk mengikat
bagian-bagian nilai yang cocok dengan patternnya. Inilah cara kita mengekstrak
nilai dari *variant* (varian) *enum*.

Sebagai contoh, mari kita ubah salah satu *variant* *enum* kita agar menampung
data di dalamnya. Dari tahun 1999 sampai 2008, Amerika Serikat mencetak koin
quarter (25 sen) dengan desain berbeda untuk masing-masing 50 negara bagian di
salah satu sisinya. Tidak ada koin lain yang mendapat desain negara bagian,
jadi hanya koin quarter yang memiliki nilai tambahan ini. Kita dapat
menambahkan informasi ini ke `enum` kita dengan mengubah *variant* `Quarter`
agar menyertakan nilai `UsState` yang tersimpan di dalamnya, yang telah kita
lakukan pada Listing 6-4.

<Listing number="6-4" caption="Enum `Coin` yang varian `Quarter`-nya juga menampung nilai `UsState`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Listing>

Bayangkan seorang teman sedang mencoba mengumpulkan kelima puluh koin quarter
negara bagian. Sambil memilah uang receh kita berdasarkan jenis koinnya, kita
juga akan menyebutkan nama negara bagian yang terkait dengan setiap quarter
sehingga jika itu salah satu yang belum dimiliki teman kita, ia dapat
menambahkannya ke collectionnya.

Pada expression match untuk kode ini, kita menambahkan variable bernama `state`
ke pattern yang mencocokkan nilai *variant* `Coin::Quarter`. Ketika
`Coin::Quarter` cocok, variable `state` akan mengikat nilai negara bagian
quarter tersebut. Lalu, kita dapat memakai `state` di kode untuk *arm* itu,
seperti ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

Jika kita memanggil `value_in_cents(Coin::Quarter(UsState::Alaska))`, `coin`
akan menjadi `Coin::Quarter(UsState::Alaska)`. Ketika kita membandingkan nilai
itu dengan setiap *arm* match, tidak ada yang cocok sampai kita mencapai
`Coin::Quarter(state)`. Pada titik itu, ikatan untuk `state` adalah nilai
`UsState::Alaska`. Kita kemudian dapat memakai ikatan itu dalam expression
`println!`, sehingga mengeluarkan nilai negara bagian dari dalam
*variant* *enum* `Coin` untuk `Quarter`.

<!-- Old headings. Do not remove or links may break. -->

<a id="matching-with-optiont"></a>

### Pattern `match` untuk `Option<T>`


Pada bagian sebelumnya, kita ingin mengeluarkan nilai `T` di dalamnya dari
kasus `Some` ketika memakai `Option<T>`; kita juga dapat menangani `Option<T>`
dengan `match`, seperti yang kita lakukan pada *enum* `Coin`! Alih-alih
membandingkan koin, kita akan membandingkan *variant*-*variant* `Option<T>`,
tetapi cara kerja expression `match` tetap sama.

Katakanlah kita ingin menulis fungsi yang menerima `Option<i32>` dan, jika ada
nilai di dalamnya, menambahkan 1 ke nilai itu. Jika tidak ada nilai di
dalamnya, fungsi itu seharusnya mengembalikan nilai `None` dan tidak mencoba
melakukan operasi apa pun.

Fungsi ini sangat mudah ditulis berkat `match`, dan akan tampak seperti
Listing 6-5.

<Listing number="6-5" caption="Fungsi yang memakai expression `match` pada `Option<i32>`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Listing>

Mari kita telaah eksekusi pertama `plus_one` secara lebih mendetail. Ketika
kita memanggil `plus_one(five)`, variable `x` di badan `plus_one` akan
memiliki nilai `Some(5)`. Kita lalu membandingkannya dengan setiap *arm* match:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Nilai `Some(5)` tidak cocok dengan pattern `None`, jadi kita melanjutkan ke *arm*
berikutnya:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

Apakah `Some(5)` cocok dengan `Some(i)`? Ya! Kita memiliki *variant* yang
sama. `i` mengikat nilai yang terkandung di dalam `Some`, jadi `i` mengambil
nilai `5`. Kode di *arm* match itu kemudian dieksekusi, jadi kita menambahkan 1
ke nilai `i` dan membuat nilai `Some` baru dengan total `6` di dalamnya.

Sekarang mari kita pertimbangkan pemanggilan kedua `plus_one` pada Listing
6-5, ketika `x` adalah `None`. Kita memasuki `match` dan membandingkannya
dengan *arm* pertama:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Cocok! Tidak ada nilai yang bisa ditambahi, jadi program berhenti dan
mengembalikan nilai `None` di sisi kanan `=>`. Karena *arm* pertama cocok, tidak
ada *arm* lain yang dibandingkan.

Menggabungkan `match` dan *enum* berguna dalam banyak situasi. Anda akan sering
melihat pattern ini di kode Rust: `match` terhadap sebuah *enum*, mengikat variable
ke data di dalamnya, lalu mengeksekusi kode berdasarkan itu. Pada awalnya agak
rumit, tetapi begitu Anda terbiasa, Anda akan berharap fitur ini ada di semua
bahasa. Fitur ini selalu menjadi favorit pengguna.

### Match Bersifat Ekshaustif

Ada satu aspek lain dari `match` yang perlu kita bahas: pattern-pattern *arm* harus
mencakup semua kemungkinan. Perhatikan versi fungsi `plus_one` kita ini, yang
memiliki bug dan tidak akan terkompilasi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```

Kita tidak menangani kasus `None`, jadi kode ini akan menimbulkan bug.
Untungnya, ini adalah bug yang diketahui Rust cara menangkapnya. Jika kita
mencoba mengompilasi kode ini, kita akan mendapatkan error ini:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

Rust tahu bahwa kita tidak mencakup semua kasus yang mungkin dan bahkan tahu
pattern mana yang kita lupakan! Match di Rust bersifat *exhaustive* (ekshaustif):
kita harus menuntaskan semua kemungkinan sampai yang terakhir agar kodenya
valid. Khususnya pada kasus `Option<T>`, ketika Rust mencegah kita lupa
menangani kasus `None` secara eksplisit, ia melindungi kita dari menganggap
bahwa kita memiliki nilai ketika mungkin saja nilainya null, sehingga
kesalahan senilai satu miliar dolar yang dibahas sebelumnya menjadi mustahil.

### Pattern Catch-All dan Placeholder `_`

Dengan *enum*, kita juga dapat mengambil tindakan khusus untuk beberapa nilai
tertentu, tetapi untuk semua nilai lain mengambil satu tindakan bawaan.
Bayangkan kita sedang mengimplementasikan sebuah permainan di mana, jika Anda
melempar angka 3 pada lemparan dadu, pemain Anda tidak bergerak tetapi malah
mendapatkan topi baru yang mewah. Jika Anda melempar 7, pemain Anda kehilangan
topi mewah. Untuk semua nilai lain, pemain Anda melangkah sejauh angka itu di
papan permainan. Berikut `match` yang mengimplementasikan logika itu, dengan
hasil lemparan dadu ditulis langsung (hardcoded) alih-alih nilai acak, dan
semua logika lain direpresentasikan oleh fungsi tanpa badan karena
mengimplementasikannya sungguhan berada di luar *scope* contoh ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```

Untuk dua *arm* pertama, patternnya adalah nilai literal `3` dan `7`. Untuk *arm*
terakhir yang mencakup semua nilai lain yang mungkin, patternnya adalah variable
yang kita pilih namai `other`. Kode yang berjalan untuk *arm* `other` memakai
variable itu dengan meneruskannya ke fungsi `move_player`.

Kode ini terkompilasi, meskipun kita belum mendaftarkan semua nilai yang
mungkin dimiliki `u8`, karena pattern terakhir akan mencocokkan semua nilai yang
tidak didaftarkan secara khusus. Pattern catch-all ini memenuhi persyaratan
bahwa `match` harus ekshaustif. Perhatikan bahwa kita harus meletakkan *arm*
catch-all paling akhir karena pattern dievaluasi secara berurutan. Seandainya
kita meletakkan *arm* catch-all lebih awal, *arm*-*arm* lain tidak akan pernah
berjalan, jadi Rust akan memperingatkan kita jika kita menambahkan *arm* setelah
catch-all!

Rust juga memiliki pattern yang dapat kita pakai ketika kita menginginkan
catch-all tetapi tidak ingin _memakai_ nilai pada pattern catch-all itu: `_`
adalah pattern khusus yang mencocokkan nilai apa pun dan tidak mengikat nilai
itu. Ini memberi tahu Rust bahwa kita tidak akan memakai nilainya, jadi Rust
tidak akan memperingatkan kita tentang variable yang tidak terpakai.

Mari kita ubah aturan permainannya: sekarang, jika Anda melempar selain 3
atau 7, Anda harus melempar lagi. Kita tidak lagi perlu memakai nilai
catch-all, jadi kita dapat mengubah kode kita untuk memakai `_` alih-alih
variable bernama `other`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

Contoh ini juga memenuhi persyaratan ekshaustivitas karena kita secara
eksplisit mengabaikan semua nilai lain di *arm* terakhir; kita tidak melupakan
apa pun.

Terakhir, kita akan mengubah aturan permainannya sekali lagi sehingga tidak
ada hal lain yang terjadi pada giliran Anda jika Anda melempar selain 3 atau
7. Kita dapat menyatakannya dengan memakai nilai unit (type *tuple* kosong yang
kita sebutkan di bagian [“Type Tuple”][tuples]<!-- ignore -->) sebagai kode
yang menyertai *arm* `_`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

Di sini, kita memberi tahu Rust secara eksplisit bahwa kita tidak akan memakai
nilai lain mana pun yang tidak cocok dengan pattern pada *arm* sebelumnya, dan kita
tidak ingin menjalankan kode apa pun pada kasus ini.

Masih ada lagi tentang pattern dan pencocokan yang akan kita bahas di
[Bab 19][ch19-00-patterns]<!-- ignore -->. Untuk sekarang, kita akan
melanjutkan ke sintaks `if let`, yang dapat berguna pada situasi ketika
expression `match` agak bertele-tele.

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html
