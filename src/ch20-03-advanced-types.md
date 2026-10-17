## Type Lanjutan

Sistem type Rust memiliki beberapa fitur yang sejauh ini sudah kita singgung
tetapi belum kita bahas. Kita akan mulai dengan membahas newtype secara umum
sambil menelaah mengapa ia berguna sebagai type. Lalu, kita akan beralih ke
type alias, fitur yang mirip dengan newtype tetapi dengan semantik yang
sedikit berbeda. Kita juga akan membahas type `!` dan type berukuran dinamis.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-for-type-safety-and-abstraction"></a>

### Keamanan Type dan Abstraksi dengan Pattern Newtype

Seksi ini mengasumsikan Anda telah membaca seksi sebelumnya,
[“Mengimplementasikan Trait Eksternal dengan Pattern Newtype”][newtype]<!-- ignore -->.
Pattern newtype juga berguna untuk tugas-tugas di luar yang sudah kita bahas
sejauh ini, termasuk menegakkan secara statis bahwa nilai-nilai tidak pernah
tertukar dan menunjukkan satuan dari sebuah nilai. Anda sudah melihat contoh
pemakaian newtype untuk menunjukkan satuan di Listing 20-16: Ingat kembali
bahwa *struct* `Millimeters` dan `Meters` membungkus nilai `u32` di dalam
sebuah newtype. Jika kita menulis fungsi dengan parameter typed
`Millimeters`, kita tidak akan bisa mengompilasi program yang tanpa sengaja
mencoba memanggil fungsi itu dengan nilai typed `Meters` atau `u32` polos.

Kita juga bisa memakai newtype pattern untuk mengabstraksi beberapa detail
implementasi sebuah type: Type baru itu bisa mengekspos API publik yang
berbeda dari API type privat di dalamnya.

Newtype juga bisa menyembunyikan implementasi internal. Misalnya, kita bisa
menyediakan type `People` untuk membungkus `HashMap<i32, String>` yang
menyimpan ID seseorang yang dikaitkan dengan namanya. Kode yang memakai
`People` hanya akan berinteraksi dengan API publik yang kita sediakan,
seperti method untuk menambahkan string nama ke collection `People`; kode itu
tidak perlu tahu bahwa secara internal kita menetapkan ID `i32` untuk
nama-nama itu. Pattern newtype adalah cara yang ringan untuk mencapai enkapsulasi
guna menyembunyikan detail implementasi, yang kita bahas di seksi
[“Enkapsulasi yang Menyembunyikan Detail
Implementasi”][encapsulation-that-hides-implementation-details]<!-- ignore -->
pada Bab 18.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-type-synonyms-with-type-aliases"></a>

<a id="type-synonyms-and-type-aliases"></a>
### Sinonim Type dan Alias Type

Rust menyediakan kemampuan untuk mendeklarasikan *type alias* (alias tipe)
untuk memberi nama lain pada sebuah type yang sudah ada. Untuk ini kita
memakai kata kunci `type`. Misalnya, kita bisa membuat alias `Kilometers`
untuk `i32` seperti berikut:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

Sekarang alias `Kilometers` adalah *sinonim* untuk `i32`; tidak seperti type
`Millimeters` dan `Meters` yang kita buat di Listing 20-16, `Kilometers`
bukan type baru yang terpisah. Nilai yang typed `Kilometers` akan
diperlakukan sama dengan nilai typed `i32`:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

Karena `Kilometers` dan `i32` adalah type yang sama, kita bisa menjumlahkan
nilai dari kedua type itu dan bisa memberikan nilai `Kilometers` ke fungsi
yang menerima parameter `i32`. Akan tetapi, dengan memakai cara ini, kita
tidak mendapatkan manfaat pemeriksaan type yang kita dapatkan dari pattern
newtype yang dibahas sebelumnya. Dengan kata lain, jika kita
mencampuradukkan nilai `Kilometers` dan `i32` di suatu tempat, kompilator
tidak akan memberi kita error.

Kasus pemakaian utama type synonym adalah mengurangi pengulangan. Misalnya,
kita mungkin memiliki type yang panjang seperti ini:

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

Menulis type yang panjang ini di tanda tangan fungsi dan sebagai type annotation
di seluruh kode bisa melelahkan dan rawan error. Bayangkan memiliki proyek
yang penuh dengan kode seperti di Listing 20-25.

<Listing number="20-25" caption="Memakai type yang panjang di banyak tempat">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

Alias type membuat kode ini lebih mudah dikelola dengan mengurangi
pengulangannya. Di Listing 20-26, kita memperkenalkan alias bernama `Thunk`
untuk type yang bertele-tele itu dan bisa mengganti semua pemakaian type itu
dengan alias `Thunk` yang lebih pendek.

<Listing number="20-26" caption="Memperkenalkan type alias `Thunk` untuk mengurangi pengulangan">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

Kode ini jauh lebih mudah dibaca dan ditulis! Memilih nama yang bermakna
untuk type alias juga bisa membantu menyampaikan maksud Anda (*thunk* adalah
kata untuk kode yang akan dievaluasi pada waktu yang akan datang, jadi itu
nama yang tepat untuk *closure* yang disimpan).

Alias type juga umum dipakai bersama type `Result<T, E>` untuk mengurangi
pengulangan. Perhatikan modul `std::io` di pustaka standar. Operasi I/O
sering kali mengembalikan `Result<T, E>` untuk menangani situasi ketika
operasi gagal bekerja. Library ini memiliki *struct* `std::io::Error` yang
mewakili semua error I/O yang mungkin terjadi. Banyak fungsi di `std::io`
mengembalikan `Result<T, E>` dengan `E` berupa `std::io::Error`, seperti
fungsi-fungsi berikut di *trait* `Write`:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

`Result<..., Error>` diulang berkali-kali. Karena itu, `std::io` memiliki
deklarasi type alias berikut:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

Karena deklarasi ini berada di modul `std::io`, kita bisa memakai alias yang
fully qualified, `std::io::Result<T>`; artinya, sebuah `Result<T, E>` dengan
`E` diisi `std::io::Error`. Tanda tangan fungsi *trait* `Write` akhirnya
tampak seperti ini:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

Alias type membantu dalam dua hal: Ia membuat kode lebih mudah ditulis *dan*
ia memberi kita antarmuka yang konsisten di seluruh `std::io`. Karena ia
adalah alias, ia hanyalah `Result<T, E>` yang lain, yang berarti kita bisa
memakai method apa pun yang bekerja pada `Result<T, E>` dengannya, serta
sintaks khusus seperti operator `?`.

### Type Never yang Tidak Pernah Mengembalikan

Rust memiliki type khusus bernama `!` yang dalam istilah type theory dikenal
sebagai *empty type* (tipe kosong) karena ia tidak memiliki nilai apa pun.
Kami lebih suka menyebutnya *never type* (tipe never) karena ia menempati
posisi return type ketika sebuah fungsi tidak akan pernah mengembalikan
nilai. Berikut contohnya:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

Kode ini dibaca sebagai “fungsi `bar` mengembalikan never.” Fungsi yang
mengembalikan never disebut *diverging function* (fungsi divergen). Kita
tidak bisa membuat nilai dari type `!`, jadi `bar` mustahil untuk
mengembalikan nilai.

Tetapi apa gunanya type yang tidak pernah bisa Anda buat nilainya? Ingat
kembali kode dari Listing 2-5, bagian dari permainan tebak angka; sebagian
kecil kode itu kita reproduksi di sini di Listing 20-27.

<Listing number="20-27" caption="Sebuah `match` dengan arm yang berakhir di `continue`">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

Pada saat itu, kita melewati beberapa detail di kode ini. Di seksi
[“Konstruk Alur Kontrol `match`”][the-match-control-flow-construct]<!-- ignore -->
pada Bab 6, kita membahas bahwa semua arm `match` harus mengembalikan type
yang sama. Jadi, misalnya, kode berikut tidak akan bekerja:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

Type `guess` di kode ini harus berupa integer *dan* string, sedangkan Rust
mewajibkan `guess` hanya memiliki satu type. Jadi, apa yang dikembalikan
`continue`? Bagaimana kita bisa diizinkan mengembalikan `u32` dari satu arm
dan memiliki arm lain yang berakhir dengan `continue` di Listing 20-27?

Seperti yang mungkin sudah Anda duga, `continue` memiliki nilai `!`.
Artinya, saat Rust menghitung type `guess`, ia melihat kedua arm match, yang
pertama dengan nilai `u32` dan yang kedua dengan nilai `!`. Karena `!` tidak
akan pernah memiliki nilai, Rust memutuskan bahwa type `guess` adalah `u32`.

Cara formal untuk menggambarkan perilaku ini adalah bahwa expression typed
`!` bisa dikoersi menjadi type lain mana pun. Kita diizinkan mengakhiri arm
`match` ini dengan `continue` karena `continue` tidak mengembalikan nilai;
sebaliknya, ia memindahkan kontrol kembali ke bagian atas loop, sehingga pada
kasus `Err`, kita tidak pernah menetapkan nilai ke `guess`.

Type never juga berguna bersama *macro* `panic!`. Ingat kembali fungsi
`unwrap` yang kita panggil pada nilai `Option<T>` untuk menghasilkan nilai
atau memicu panic, dengan definisi berikut:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

Pada kode ini, hal yang sama terjadi seperti pada `match` di Listing 20-27:
Rust melihat bahwa `val` typed `T` dan `panic!` typed `!`, sehingga hasil
keseluruhan expression `match` adalah `T`. Kode ini bekerja karena `panic!`
tidak menghasilkan nilai; ia mengakhiri program. Pada kasus `None`, kita
tidak akan mengembalikan nilai dari `unwrap`, jadi kode ini valid.

Expression terakhir yang typed `!` adalah loop:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

Di sini, loop-nya tidak pernah berakhir, jadi `!` adalah nilai dari expression
itu. Akan tetapi, hal ini tidak akan berlaku jika kita menyertakan `break`,
karena loop itu akan berakhir saat ia mencapai `break`.

<a id="dynamically-sized-types-and-the-sized-trait"></a>
### Type Berukuran Dinamis dan Trait `Sized`

Rust perlu mengetahui detail tertentu tentang type-typenya, seperti berapa
banyak ruang yang harus dialokasikan untuk nilai dari type tertentu. Hal ini
membuat salah satu sudut type systemnya sedikit membingungkan pada awalnya:
konsep *dynamically sized type* (tipe berukuran dinamis). Kadang disebut
*DST* atau *unsized type* (tipe yang tidak berukuran), type-type ini
memungkinkan kita menulis kode yang memakai nilai yang ukurannya hanya bisa
kita ketahui pada runtime.

Mari kita gali detail type berukuran dinamis yang disebut `str`, yang sudah
kita pakai di sepanjang buku ini. Benar, bukan `&str`, melainkan `str` itu
sendiri, adalah sebuah DST. Dalam banyak kasus, seperti saat menyimpan teks
yang dimasukkan pengguna, kita tidak bisa tahu berapa panjang string itu
sampai runtime. Itu berarti kita tidak bisa membuat variable typed `str`,
dan kita juga tidak bisa menerima argumen typed `str`. Perhatikan kode
berikut, yang tidak akan bekerja:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

Rust perlu tahu berapa banyak memori yang harus dialokasikan untuk nilai apa
pun dari type tertentu, dan semua nilai dari sebuah type harus memakai jumlah
memori yang sama. Jika Rust mengizinkan kita menulis kode ini, kedua nilai
`str` ini harus menempati jumlah ruang yang sama. Tetapi panjang keduanya
berbeda: `s1` butuh 12 byte penyimpanan dan `s2` butuh 15. Inilah sebabnya
tidak mungkin membuat variable yang menyimpan type berukuran dinamis.

Jadi, apa yang kita lakukan? Dalam kasus ini, Anda sudah tahu jawabannya:
Kita membuat type `s1` dan `s2` menjadi string *slice* (`&str`), bukan `str`.
Ingat kembali dari seksi [“Slice String”][string-slices]<!-- ignore --> di
Bab 4 bahwa struktur data *slice* hanya menyimpan posisi awal dan panjang
*slice*. Jadi, meskipun `&T` adalah nilai tunggal yang menyimpan alamat memori
tempat `T` berada, string *slice* adalah *dua* nilai: alamat `str` dan
panjangnya. Dengan begitu, kita bisa mengetahui ukuran nilai string *slice*
pada waktu kompilasi: ukurannya dua kali panjang `usize`. Artinya, kita
selalu tahu ukuran string *slice*, tidak peduli seberapa panjang string yang
dirujuknya. Secara umum, beginilah cara type berukuran dinamis dipakai di
Rust: Type-type itu memiliki sedikit metadata tambahan yang menyimpan ukuran
informasi dinamisnya. Aturan emas type berukuran dinamis adalah kita harus
selalu menempatkan nilai type berukuran dinamis di belakang *pointer* dalam
bentuk apa pun.

Kita bisa menggabungkan `str` dengan segala macam *pointer*: misalnya,
`Box<str>` atau `Rc<str>`. Bahkan, Anda sudah pernah melihat hal ini
sebelumnya, tetapi dengan type berukuran dinamis yang berbeda: *trait*. Setiap
*trait* adalah type berukuran dinamis yang bisa kita rujuk dengan memakai nama
*trait* itu. Di seksi [“Memakai *Trait Object* untuk Mengabstraksi Perilaku
Bersama”][using-trait-objects-to-abstract-over-shared-behavior]<!-- ignore -->
pada Bab 18, kita menyebutkan bahwa untuk memakai *trait* sebagai *trait object*,
kita harus menempatkannya di belakang *pointer*, seperti `&dyn Trait` atau
`Box<dyn Trait>` (`Rc<dyn Trait>` juga bisa).

Untuk bekerja dengan DST, Rust menyediakan *trait* `Sized` untuk menentukan
apakah ukuran sebuah type diketahui pada waktu kompilasi atau tidak. *Trait*
ini diimplementasikan secara otomatis untuk semua hal yang ukurannya
diketahui pada waktu kompilasi. Selain itu, Rust secara implisit menambahkan
bound pada `Sized` ke setiap fungsi generik. Artinya, definisi fungsi generik
seperti ini:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

sebenarnya diperlakukan seolah-olah kita menulis ini:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

Secara bawaan, fungsi generik hanya akan bekerja pada type yang ukurannya
diketahui pada waktu kompilasi. Akan tetapi, Anda bisa memakai sintaks khusus
berikut untuk melonggarkan batasan ini:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

*Trait bound* pada `?Sized` berarti “`T` bisa `Sized` atau tidak,” dan notasi
ini menggantikan bawaan bahwa generic type harus memiliki ukuran yang
diketahui pada waktu kompilasi. Sintaks `?Trait` dengan makna ini hanya
tersedia untuk `Sized`, tidak untuk *trait* lainnya.

Perhatikan juga bahwa kita mengubah type parameter `t` dari `T` menjadi
`&T`. Karena type itu mungkin bukan `Sized`, kita perlu memakainya di
belakang *pointer* dalam bentuk apa pun. Dalam kasus ini, kita memilih
*reference*.

Selanjutnya, kita akan membahas fungsi dan *closure*!

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-03-slices.html#string-slices
[the-match-control-flow-construct]: ch06-02-match.html#the-match-control-flow-construct
[using-trait-objects-to-abstract-over-shared-behavior]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
