## Lampiran D: Alat Pengembangan yang Berguna

Dalam lampiran ini, kita membahas beberapa alat pengembangan yang berguna yang
disediakan oleh proyek Rust. Kita akan melihat pemformatan otomatis, cara cepat
menerapkan perbaikan peringatan, sebuah linter, dan integrasi dengan IDE.

### Pemformatan Otomatis dengan `rustfmt`

Alat `rustfmt` memformat ulang kode Anda sesuai gaya kode komunitas. Banyak
proyek kolaboratif memakai `rustfmt` untuk mencegah perdebatan tentang gaya mana
yang dipakai saat menulis Rust: semua orang memformat kodenya memakai alat
tersebut.

Instalasi Rust menyertakan `rustfmt` secara bawaan, jadi Anda seharusnya sudah
memiliki program `rustfmt` dan `cargo-fmt` di sistem Anda. Kedua perintah ini
serupa dengan `rustc` dan `cargo` dalam hal `rustfmt` memungkinkan kontrol yang
lebih halus, sementara `cargo-fmt` memahami konvensi proyek yang memakai Cargo.
Untuk memformat proyek Cargo mana pun, masukkan yang berikut:

```console
$ cargo fmt
```

Menjalankan perintah ini memformat ulang semua kode Rust di *crate* saat ini.
Perintah ini seharusnya hanya mengubah gaya kode, bukan semantik kodenya. Untuk
informasi lebih lanjut tentang `rustfmt`, lihat [dokumentasinya][rustfmt].

### Memperbaiki Kode Anda dengan `rustfix`

Alat `rustfix` disertakan dalam instalasi Rust dan dapat memperbaiki peringatan
*compiler* secara otomatis apabila ada cara yang jelas untuk mengoreksi masalah
itu yang kemungkinan besar memang Anda inginkan. Anda mungkin pernah melihat
peringatan *compiler* sebelumnya. Sebagai contoh, perhatikan kode berikut:

<span class="filename">Nama File: src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

Di sini, kita mendefinisikan variable `x` sebagai *mutable* (dapat diubah),
tetapi kita tidak pernah benar-benar mengubahnya. Rust memperingatkan kita soal
itu:

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

Peringatan itu menyarankan kita menghapus kata kunci `mut`. Kita dapat
menerapkan saran itu secara otomatis memakai alat `rustfix` dengan menjalankan
perintah `cargo fix`:

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

Saat kita melihat _src/main.rs_ lagi, kita akan melihat bahwa `cargo fix` telah
mengubah kodenya:

<span class="filename">Nama File: src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

Variable `x` sekarang *immutable*, dan peringatannya tidak lagi muncul.

Anda juga dapat memakai perintah `cargo fix` untuk memindahkan kode Anda dari
satu edisi Rust ke edisi lainnya. Edisi dibahas di [Lampiran E][editions]<!--
ignore -->.

### Lint Tambahan dengan Clippy

Alat Clippy adalah kumpulan lint untuk menganalisis kode Anda supaya Anda dapat
menangkap kesalahan umum dan meningkatkan kode Rust Anda. Clippy disertakan
dengan instalasi standar Rust.

Untuk menjalankan lint Clippy pada proyek Cargo mana pun, masukkan yang berikut:

```console
$ cargo clippy
```

Sebagai contoh, katakanlah Anda menulis program yang memakai aproksimasi
constant matematis, seperti pi, seperti yang dilakukan program ini:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Menjalankan `cargo clippy` pada proyek ini menghasilkan error berikut:

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

Error ini memberitahukan bahwa Rust sudah memiliki constant `PI` yang lebih
presisi, dan bahwa program Anda akan lebih benar jika memakai constant itu
saja. Anda kemudian akan mengubah kode Anda untuk memakai constant `PI`.

Kode berikut tidak menghasilkan error atau peringatan apa pun dari Clippy:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Untuk informasi lebih lanjut tentang Clippy, lihat
[dokumentasinya][clippy].

### Integrasi IDE Memakai `rust-analyzer`

Untuk membantu integrasi IDE, komunitas Rust merekomendasikan pemakaian
[`rust-analyzer`][rust-analyzer]<!-- ignore -->. Alat ini adalah sekumpulan
utilitas yang berpusat pada *compiler* dan memakai [Language Server
Protocol][lsp]<!-- ignore -->, spesifikasi bagi IDE dan bahasa pemrograman untuk
saling berkomunikasi. Berbagai client dapat memakai `rust-analyzer`, seperti
[plugin Rust analyzer untuk Visual Studio Code][vscode].

Kunjungi [laman utama][rust-analyzer]<!-- ignore --> proyek `rust-analyzer`
untuk petunjuk instalasi, lalu pasang dukungan language server di IDE Anda.
IDE Anda akan memperoleh kemampuan seperti pelengkapan otomatis, lompat ke
definisi, dan error inline.

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer
