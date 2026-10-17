## Error yang Tidak Dapat Dipulihkan dengan `panic!`

Terkadang hal buruk terjadi di kode Anda, dan tidak ada yang dapat Anda
lakukan untuk itu. Dalam kasus-kasus ini, Rust memiliki *macro* `panic!`. Ada
dua cara menyebabkan panic dalam praktik: dengan melakukan tindakan yang
membuat kode kita panic (seperti mengakses array melewati ujungnya) atau
dengan memanggil *macro* `panic!` secara eksplisit. Dalam kedua kasus, kita
menyebabkan panic di program kita. Secara default, panic ini akan mencetak
pesan kegagalan, melakukan unwinding, membersihkan tumpukan, dan berhenti.
Lewat sebuah environment variable, Anda juga dapat membuat Rust menampilkan
tumpukan panggilan ketika panic terjadi agar lebih mudah melacak sumber
panic.

> ### Melakukan Unwinding pada Tumpukan atau Aborting sebagai Tanggapan atas Panic
>
> Secara default, ketika panic terjadi, program mulai melakukan *unwinding*,
> yang berarti Rust berjalan mundur ke atas tumpukan dan membersihkan data
> dari setiap fungsi yang ditemuinya. Namun, berjalan mundur dan membersihkan
> adalah banyak pekerjaan. Karena itu, Rust mengizinkan Anda memilih
> alternatif untuk segera melakukan *aborting* (pembatalan), yang mengakhiri
> program tanpa pembersihan.
>
> Memori yang sedang dipakai program kemudian perlu dibersihkan oleh sistem
> operasi. Jika di proyek Anda, Anda perlu membuat binary hasilnya sekecil
> mungkin, Anda dapat beralih dari unwinding ke aborting saat panic dengan
> menambahkan `panic = 'abort'` ke bagian `[profile]` yang sesuai di file
> _Cargo.toml_ Anda. Misalnya, jika Anda ingin abort saat panic dalam mode
> release, tambahkan ini:
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

Mari kita coba memanggil `panic!` di program sederhana:

<Listing file-name="src/main.rs">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-01-panic/src/main.rs}}
```

</Listing>

Ketika Anda menjalankan programnya, Anda akan melihat sesuatu seperti ini:

```console
{{#include ../listings/ch09-error-handling/no-listing-01-panic/output.txt}}
```

Pemanggilan `panic!` menyebabkan pesan error yang terdapat di dua baris
terakhir. Baris pertama menunjukkan pesan panic kita dan tempat di kode
sumber kita tempat panic terjadi: _src/main.rs:2:5_ menunjukkan bahwa itu
adalah baris kedua, karakter kelima dari file _src/main.rs_ kita.

Dalam kasus ini, baris yang ditunjukkan adalah bagian dari kode kita, dan
jika kita pergi ke baris itu, kita melihat pemanggilan *macro* `panic!`. Dalam
kasus lain, pemanggilan `panic!` mungkin berada di kode yang dipanggil kode
kita, dan nama file serta nomor baris yang dilaporkan pesan error akan
menjadi kode orang lain tempat *macro* `panic!` dipanggil, bukan baris kode
kita yang akhirnya berujung ke pemanggilan `panic!`.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-a-panic-backtrace"></a>

Kita dapat memakai backtrace dari fungsi-fungsi asal pemanggilan `panic!`
untuk mencari tahu bagian kode kita yang menyebabkan masalah. Untuk memahami
cara memakai backtrace `panic!`, mari kita lihat contoh lain dan seperti apa
rasanya ketika pemanggilan `panic!` datang dari sebuah library karena bug di
kode kita, alih-alih dari kode kita yang memanggil *macro* itu secara
langsung. Listing 9-1 memiliki kode yang mencoba mengakses indeks di vektor
di luar jangkauan indeks yang valid.

<Listing number="9-1" file-name="src/main.rs" caption="Mencoba mengakses elemen melewati ujung vektor, yang akan menyebabkan pemanggilan `panic!`">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-01/src/main.rs}}
```

</Listing>

Di sini, kita mencoba mengakses elemen ke-100 dari vektor kita (yang berada
pada indeks 99 karena pengindeksan dimulai dari nol), tetapi vektornya hanya
memiliki tiga elemen. Dalam situasi ini, Rust akan panic. Memakai `[]`
seharusnya mengembalikan sebuah elemen, tetapi jika Anda memberikan indeks
yang tidak valid, tidak ada elemen yang dapat dikembalikan Rust di sini yang
akan benar.

Di C, mencoba membaca melewati ujung sebuah struktur data adalah perilaku
tak terdefinisi. Anda mungkin mendapatkan apa pun yang berada di lokasi
memori yang berkorespondensi dengan elemen itu di struktur data, meskipun
memori itu bukan milik struktur tersebut. Ini disebut *buffer overread*
(pembacaan buffer berlebih) dan dapat mengarah pada kerentanan keamanan jika
seorang penyerang mampu memanipulasi indeks sedemikian rupa sehingga membaca
data yang tidak boleh mereka baca yang tersimpan setelah struktur data.

Untuk melindungi program Anda dari kerentanan semacam ini, jika Anda mencoba
membaca elemen pada indeks yang tidak ada, Rust akan menghentikan eksekusi
dan menolak melanjutkan. Mari kita mencobanya dan melihat hasilnya:

```console
{{#include ../listings/ch09-error-handling/listing-09-01/output.txt}}
```

Error ini menunjuk ke baris 4 dari _main.rs_ kita tempat kita mencoba
mengakses indeks 99 dari vektor di `v`.

Baris `note:` memberi tahu kita bahwa kita dapat menetapkan variable
lingkungan `RUST_BACKTRACE` untuk mendapatkan backtrace tentang apa yang
persisnya terjadi sehingga menyebabkan error. Sebuah *backtrace* adalah
daftar semua fungsi yang telah dipanggil untuk sampai ke titik ini.
Backtrace di Rust bekerja seperti di bahasa lain: kunci membaca backtrace
adalah memulai dari atas dan membaca sampai Anda melihat file yang Anda
tulis. Di situlah tempat masalah bermula. Baris-baris di atas titik itu
adalah kode yang telah dipanggil kode Anda; baris-baris di bawahnya adalah
kode yang memanggil kode Anda. Baris-baris sebelum-dan-sesudah ini mungkin
mencakup kode inti Rust, kode pustaka standar, atau *crate* yang sedang Anda
pakai. Mari kita coba mendapatkan backtrace dengan menetapkan variable
lingkungan `RUST_BACKTRACE` ke nilai apa pun kecuali `0`. Listing 9-2
menunjukkan output yang mirip dengan yang akan Anda lihat.

<!-- manual-regeneration
cd listings/ch09-error-handling/listing-09-01
RUST_BACKTRACE=1 cargo run
copy the backtrace output below
check the backtrace number mentioned in the text below the listing
-->

<Listing number="9-2" caption="Backtrace yang dihasilkan pemanggilan `panic!` yang ditampilkan ketika environment variable `RUST_BACKTRACE` ditetapkan">

```console
$ RUST_BACKTRACE=1 cargo run
thread 'main' panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
stack backtrace:
   0: rust_begin_unwind
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/std/src/panicking.rs:692:5
   1: core::panicking::panic_fmt
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:75:14
   2: core::panicking::panic_bounds_check
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:273:5
   3: <usize as core::slice::index::SliceIndex<[T]>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:274:10
   4: core::slice::index::<impl core::ops::index::Index<I> for [T]>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:16:9
   5: <alloc::vec::Vec<T,A> as core::ops::index::Index<I>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/vec/mod.rs:3361:9
   6: panic::main
             at ./src/main.rs:4:6
   7: core::ops::function::FnOnce::call_once
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

</Listing>

Banyak sekali outputnya! Output persis yang Anda lihat mungkin berbeda
tergantung sistem operasi dan versi Rust Anda. Untuk mendapatkan backtrace
dengan informasi ini, simbol debug harus diaktifkan. Simbol debug aktif
secara default ketika memakai `cargo build` atau `cargo run` tanpa flag
`--release`, seperti yang kita lakukan di sini.

Pada output di Listing 9-2, baris 6 dari backtrace menunjuk ke baris di
proyek kita yang menyebabkan masalah: baris 4 dari _src/main.rs_. Jika kita
tidak ingin program kita panic, kita harus memulai penyelidikan kita di
lokasi yang ditunjuk oleh baris pertama yang menyebut file yang kita tulis.
Di Listing 9-1, tempat kita sengaja menulis kode yang akan panic, cara
memperbaiki panic-nya adalah dengan tidak meminta elemen di luar jangkauan
indeks vektor. Ketika kode Anda panic di masa depan, Anda perlu mencari tahu
tindakan apa yang diambil kode dengan nilai apa sehingga menyebabkan panic
dan apa yang seharusnya dilakukan kode sebagai gantinya.

Kita akan kembali ke `panic!` dan kapan kita sebaiknya memakai dan tidak
memakai `panic!` untuk menangani kondisi error di bagian [“Untuk `panic!`
atau Tidak `panic!`”][to-panic-or-not-to-panic]<!-- ignore --> nanti di bab
ini. Berikutnya, kita akan melihat cara memulihkan diri dari error memakai
`Result`.

[to-panic-or-not-to-panic]: ch09-03-to-panic-or-not-to-panic.html#to-panic-or-not-to-panic
