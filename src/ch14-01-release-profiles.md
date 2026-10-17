## Menyesuaikan Build dengan Release Profile

Dalam Rust, *release profile* (profil rilis) adalah profil yang telah
didefinisikan sebelumnya dan dapat disesuaikan, dengan konfigurasi yang
berbeda-beda sehingga seorang pemrogram memiliki kontrol lebih besar atas
berbagai opsi untuk mengompilasi kode. Setiap profil dikonfigurasi secara
terpisah dari yang lain.

Cargo memiliki dua profil utama: profil `dev` yang dipakai Cargo saat Anda
menjalankan `cargo build`, dan profil `release` yang dipakai Cargo saat Anda
menjalankan `cargo build --release`. Profil `dev` didefinisikan dengan default
yang baik untuk pengembangan, dan profil `release` memiliki default yang baik
untuk build rilis.

Nama-nama profil ini mungkin tidak asing bagi Anda karena muncul di keluaran
build:

<!-- manual-regeneration
anywhere, run:
cargo build
cargo build --release
and ensure output below is accurate
-->

```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

`dev` dan `release` adalah kedua profil berbeda yang dipakai oleh kompilator.

Cargo memiliki pengaturan default untuk masing-masing profil yang berlaku
ketika Anda belum menambahkan seksi `[profile.*]` apa pun secara eksplisit di
file _Cargo.toml_ proyek Anda. Dengan menambahkan seksi `[profile.*]` untuk
profil mana pun yang ingin Anda sesuaikan, Anda menimpa sebagian saja dari
pengaturan default itu. Sebagai contoh, berikut nilai default untuk pengaturan
`opt-level` pada profil `dev` dan `release`:

<span class="filename">Nama File: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

Pengaturan `opt-level` mengontrol banyaknya optimasi yang akan diterapkan Rust
pada kode Anda, dengan rentang 0 sampai 3. Menerapkan lebih banyak optimasi
memperpanjang waktu kompilasi, jadi jika Anda sedang dalam tahap pengembangan
dan sering mengompilasi kode, Anda tentu ingin lebih sedikit optimasi supaya
kompilasi lebih cepat meskipun kode yang dihasilkan berjalan lebih lambat.
Karena itu, `opt-level` default untuk `dev` adalah `0`. Ketika Anda siap
merilis kode, sebaiknya Anda menghabiskan lebih banyak waktu untuk kompilasi.
Anda hanya akan mengompilasi dalam mode rilis satu kali, tetapi Anda akan
menjalankan program hasil kompilasi itu berkali-kali, jadi mode rilis
menukarkan waktu kompilasi yang lebih lama dengan kode yang berjalan lebih
cepat. Itulah sebabnya `opt-level` default untuk profil `release` adalah `3`.

Anda dapat menimpa pengaturan default dengan menambahkan nilai yang berbeda
untuknya di _Cargo.toml_. Sebagai contoh, jika kita ingin memakai tingkat
optimasi 1 pada profil pengembangan, kita dapat menambahkan dua baris berikut
ke file _Cargo.toml_ proyek kita:

<span class="filename">Nama File: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

Kode ini menimpa pengaturan default `0`. Sekarang, ketika kita menjalankan
`cargo build`, Cargo akan memakai default profil `dev` ditambah penyesuaian
kita pada `opt-level`. Karena kita menetapkan `opt-level` menjadi `1`, Cargo
akan menerapkan lebih banyak optimasi daripada default, tetapi tidak sebanyak
build rilis.

Untuk daftar lengkap opsi konfigurasi dan default untuk setiap profil, lihat
[dokumentasi Cargo](https://doc.rust-lang.org/cargo/reference/profiles.html).
