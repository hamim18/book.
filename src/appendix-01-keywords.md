## Lampiran A: Keywords

Daftar berikut memuat *keyword* (kata kunci) yang dicadangkan untuk pemakaian
saat ini atau masa depan oleh bahasa Rust. Karena itu, kata-kata tersebut tidak
dapat dipakai sebagai *identifier* (pengidentifikasi), kecuali sebagai *raw
identifier* (identifier mentah), seperti yang kita bahas di bagian [“Raw
Identifiers”][raw-identifiers]<!-- ignore -->.

_Identifier_ adalah nama dari fungsi, variabel, parameter, *field* (medan)
struct, *module* (modul), crate, konstanta, *macro* (makro), nilai static,
atribut, tipe, trait, atau *lifetime* (masa hidup).

[raw-identifiers]: #raw-identifiers

### Keyword yang Sedang Dipakai

Berikut adalah daftar kata kunci yang sedang dipakai, beserta penjelasan
fungsionalitasnya.

- **`as`**: Melakukan casting primitif, mendisambiguasi trait tertentu yang
  memuat suatu item, atau mengganti nama item dalam pernyataan `use`.
- **`async`**: Mengembalikan `Future` alih-alih memblokir thread saat ini.
- **`await`**: Menangguhkan eksekusi sampai hasil `Future` siap.
- **`break`**: Keluar dari perulangan dengan segera.
- **`const`**: Mendefinisikan item konstanta atau raw pointer konstan.
- **`continue`**: Melanjutkan ke iterasi perulangan berikutnya.
- **`crate`**: Di dalam module path, merujuk ke akar crate.
- **`dyn`**: Dispatch dinamis ke trait object.
- **`else`**: Cadangan untuk konstruk alur kontrol `if` dan `if let`.
- **`enum`**: Mendefinisikan enumerasi.
- **`extern`**: Menautkan fungsi atau variabel eksternal.
- **`false`**: Literal Boolean false.
- **`fn`**: Mendefinisikan fungsi atau tipe pointer fungsi.
- **`for`**: Melakukan perulangan atas item dari iterator, mengimplementasikan
  trait, atau menentukan lifetime berperingkat lebih tinggi.
- **`if`**: Melakukan percabangan berdasarkan hasil ekspresi kondisional.
- **`impl`**: Mengimplementasikan fungsionalitas inherent atau trait.
- **`in`**: Bagian dari sintaks perulangan `for`.
- **`let`**: Mengikat variabel.
- **`loop`**: Melakukan perulangan tanpa syarat.
- **`match`**: Mencocokkan nilai dengan pola.
- **`mod`**: Mendefinisikan module.
- **`move`**: Membuat closure mengambil kepemilikan atas semua yang
  ditangkapnya.
- **`mut`**: Menandai mutabilitas pada reference, raw pointer, atau pengikatan
  pola.
- **`pub`**: Menandai visibilitas publik pada field struct, blok `impl`, atau
  module.
- **`ref`**: Mengikat berdasarkan reference.
- **`return`**: Kembali dari fungsi.
- **`Self`**: Alias tipe untuk tipe yang sedang kita definisikan atau
  implementasikan.
- **`self`**: Subjek metode atau module saat ini.
- **`static`**: Variabel global atau lifetime yang berlangsung selama eksekusi
  program.
- **`struct`**: Mendefinisikan struktur.
- **`super`**: Module induk dari module saat ini.
- **`trait`**: Mendefinisikan trait.
- **`true`**: Literal Boolean true.
- **`type`**: Mendefinisikan alias tipe atau associated type.
- **`union`**: Mendefinisikan [union][union]<!-- ignore -->; merupakan kata
  kunci hanya ketika dipakai dalam deklarasi union.
- **`unsafe`**: Menandai kode, fungsi, trait, atau implementasi yang unsafe.
- **`use`**: Membawa simbol ke dalam scope.
- **`where`**: Menandai klausa yang membatasi suatu tipe.
- **`while`**: Melakukan perulangan bersyarat berdasarkan hasil suatu ekspresi.

[union]: ../reference/items/unions.html

### Kata Kunci yang Dicadangkan untuk Pemakaian Masa Depan

Kata kunci berikut belum memiliki fungsionalitas apa pun, tetapi dicadangkan
oleh Rust untuk kemungkinan pemakaian di masa depan:

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

### Raw Identifiers

_Raw identifiers_ adalah sintaks yang memungkinkan Anda memakai kata kunci di
tempat yang biasanya tidak mengizinkannya. Anda memakai raw identifier dengan
memberi prefiks `r#` pada kata kunci.

Sebagai contoh, `match` adalah kata kunci. Jika Anda mencoba mengompilasi fungsi
berikut yang memakai `match` sebagai namanya:

<span class="filename">Nama File: src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

Anda akan mendapatkan galat berikut:

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

Galat tersebut menunjukkan bahwa Anda tidak dapat memakai kata kunci `match`
sebagai identifier fungsi. Untuk memakai `match` sebagai nama fungsi, Anda perlu
memakai sintaks raw identifier, seperti ini:

<span class="filename">Nama File: src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

Kode ini akan terkompilasi tanpa galat apa pun. Perhatikan prefiks `r#` pada
nama fungsi, baik pada definisinya maupun pada tempat fungsi itu dipanggil di
dalam `main`.

Raw identifier memungkinkan Anda memakai kata apa pun yang Anda pilih sebagai
identifier, bahkan jika kata itu kebetulan merupakan kata kunci yang
dicadangkan. Ini memberi kita lebih banyak kebebasan untuk memilih nama
identifier, sekaligus memungkinkan kita berintegrasi dengan program yang ditulis
dalam bahasa yang kata-kata ini bukan kata kuncinya. Selain itu, raw identifier
memungkinkan Anda memakai library yang ditulis dengan edisi Rust yang berbeda
dari yang dipakai crate Anda. Sebagai contoh, `try` bukan kata kunci pada edisi
2015, tetapi merupakan kata kunci pada edisi 2018, 2021, dan 2024. Jika Anda
bergantung pada library yang ditulis memakai edisi 2015 dan memiliki fungsi
`try`, Anda perlu memakai sintaks raw identifier, `r#try` dalam kasus ini, untuk
memanggil fungsi tersebut dari kode Anda pada edisi yang lebih baru. Lihat
[Lampiran E][appendix-e]<!-- ignore --> untuk informasi lebih lanjut tentang
edisi.

[appendix-e]: appendix-05-editions.html
