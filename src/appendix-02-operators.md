## Lampiran B: Operator dan Simbol

Lampiran ini memuat glosarium sintaks Rust, termasuk operator dan simbol lain
yang muncul sendiri-sendiri atau dalam konteks *path*, *generics*, *trait bound*,
*macro*, atribut, komentar, *tuple*, dan tanda kurung.

### Operator

Tabel B-1 memuat operator-operator di Rust, contoh bagaimana operator itu muncul
dalam konteks, penjelasan singkat, dan apakah operator tersebut dapat
di-overload. Jika suatu operator dapat di-overload, *trait* yang relevan untuk
meng-overload operator itu dicantumkan.

<span class="caption">Tabel B-1: Operator</span>

| Operator                  | Contoh                                                  | Penjelasan                                                                     | Dapat di-Overload? |
| ------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------ |
| `!`                       | `ident!(...)`, `ident!{...}`, `ident![...]`             | Ekspansi macro                                                                 |                    |
| `!`                       | `!expr`                                                 | Komplemen bitwise atau logis                                                   | `Not`              |
| `!=`                      | `expr != expr`                                          | Perbandingan ketidaksamaan                                                     | `PartialEq`        |
| `%`                       | `expr % expr`                                           | Sisa pembagian aritmetika                                                      | `Rem`              |
| `%=`                      | `var %= expr`                                           | Sisa pembagian aritmetika dan penetapan                                        | `RemAssign`        |
| `&`                       | `&expr`, `&mut expr`                                    | Peminjaman                                                                     |                    |
| `&`                       | `&type`, `&mut type`, `&'a type`, `&'a mut type`        | Type pointer yang dipinjam                                                     |                    |
| `&`                       | `expr & expr`                                           | AND bitwise                                                                    | `BitAnd`           |
| `&=`                      | `var &= expr`                                           | AND bitwise dan penetapan                                                      | `BitAndAssign`     |
| `&&`                      | `expr && expr`                                          | AND logis dengan evaluasi hubung singkat                                       |                    |
| `*`                       | `expr * expr`                                           | Perkalian aritmetika                                                           | `Mul`              |
| `*=`                      | `var *= expr`                                           | Perkalian aritmetika dan penetapan                                             | `MulAssign`        |
| `*`                       | `*expr`                                                 | Dereferensi                                                                    | `Deref`            |
| `*`                       | `*const type`, `*mut type`                              | Pointer mentah                                                                 |                    |
| `+`                       | `trait + trait`, `'a + trait`                           | Batasan compound type                                                           |                    |
| `+`                       | `expr + expr`                                           | Penjumlahan aritmetika                                                         | `Add`              |
| `+=`                      | `var += expr`                                           | Penjumlahan aritmetika dan penetapan                                           | `AddAssign`        |
| `,`                       | `expr, expr`                                            | Pemisah argumen dan elemen                                                     |                    |
| `-`                       | `- expr`                                                | Negasi aritmetika                                                              | `Neg`              |
| `-`                       | `expr - expr`                                           | Pengurangan aritmetika                                                         | `Sub`              |
| `-=`                      | `var -= expr`                                           | Pengurangan aritmetika dan penetapan                                           | `SubAssign`        |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Type kembalian fungsi dan closure                                              |                    |
| `.`                       | `expr.ident`                                            | Akses field                                                                    |                    |
| `.`                       | `expr.ident(expr, ...)`                                 | Pemanggilan metode                                                             |                    |
| `.`                       | `expr.0`, `expr.1`, dan seterusnya                      | Pengindeksan tuple                                                             |                    |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Literal rentang eksklusif-kanan                                                | `PartialOrd`       |
| `..=`                     | `..=expr`, `expr..=expr`                                | Literal rentang inklusif-kanan                                                 | `PartialOrd`       |
| `..`                      | `..expr`                                                | Sintaks update literal struct                                                  |                    |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | Pengikatan pola “dan sisanya”                                                  |                    |
| `...`                     | `expr...expr`                                           | (Usang, pakai `..=` saja) Di dalam pola: pola rentang inklusif                 |                    |
| `/`                       | `expr / expr`                                           | Pembagian aritmetika                                                           | `Div`              |
| `/=`                      | `var /= expr`                                           | Pembagian aritmetika dan penetapan                                             | `DivAssign`        |
| `:`                       | `pat: type`, `ident: type`                              | Batasan                                                                        |                    |
| `:`                       | `ident: expr`                                           | Penginisialisasi field struct                                                  |                    |
| `:`                       | `'a: loop {...}`                                        | Label loop                                                               |                    |
| `;`                       | `expr;`                                                 | Terminator statement dan item                                                 |                    |
| `;`                       | `[...; len]`                                            | Bagian dari sintaks array berukuran tetap                                      |                    |
| `<<`                      | `expr << expr`                                          | Pergeseran kiri                                                                | `Shl`              |
| `<<=`                     | `var <<= expr`                                          | Pergeseran kiri dan penetapan                                                  | `ShlAssign`        |
| `<`                       | `expr < expr`                                           | Perbandingan kurang dari                                                       | `PartialOrd`       |
| `<=`                      | `expr <= expr`                                          | Perbandingan kurang dari atau sama dengan                                      | `PartialOrd`       |
| `=`                       | `var = expr`, `ident = type`                            | Penetapan/kesetaraan                                                           |                    |
| `==`                      | `expr == expr`                                          | Perbandingan kesamaan                                                          | `PartialEq`        |
| `=>`                      | `pat => expr`                                           | Bagian dari sintaks arm match                                                  |                    |
| `>`                       | `expr > expr`                                           | Perbandingan lebih dari                                                        | `PartialOrd`       |
| `>=`                      | `expr >= expr`                                          | Perbandingan lebih dari atau sama dengan                                       | `PartialOrd`       |
| `>>`                      | `expr >> expr`                                          | Pergeseran kanan                                                               | `Shr`              |
| `>>=`                     | `var >>= expr`                                          | Pergeseran kanan dan penetapan                                                 | `ShrAssign`        |
| `@`                       | `ident @ pat`                                           | Pengikatan pola                                                                |                    |
| `^`                       | `expr ^ expr`                                           | OR eksklusif bitwise                                                           | `BitXor`           |
| `^=`                      | `var ^= expr`                                           | OR eksklusif bitwise dan penetapan                                             | `BitXorAssign`     |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Alternatif pola                                                                |                    |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | OR bitwise                                                                     | `BitOr`            |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | OR bitwise dan penetapan                                                       | `BitOrAssign`      |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | OR logis dengan evaluasi hubung singkat                                        |                    |
| `?`                       | `expr?`                                                 | Penerusan error                                                                |                    |

### Simbol Non-operator

Tabel-tabel berikut memuat semua simbol yang tidak berfungsi sebagai operator;
artinya, simbol-simbol itu tidak berperilaku seperti pemanggilan fungsi atau
metode.

Tabel B-2 menunjukkan simbol yang muncul sendirian dan berlaku di berbagai
lokasi.

<span class="caption">Tabel B-2: Sintaks Berdiri Sendiri</span>

| Simbol                                                                 | Penjelasan                                                                                       |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `'ident`                                                               | Lifetime bernama atau loop label                                                           |
| Digit yang langsung diikuti `u8`, `i32`, `f64`, `usize`, dan seterusnya | Literal numerik typed tertentu                                                                 |
| `"..."`                                                                | String literal                                                                                   |
| `r"..."`, `r#"..."#`, `r##"..."##`, dan seterusnya                      | Raw string literal; karakter escape tidak diproses                                               |
| `b"..."`                                                               | Byte string literal; membangun array berisi byte, bukan string                                   |
| `br"..."`, `br#"..."#`, `br##"..."##`, dan seterusnya                   | Raw byte string literal; gabungan raw dan byte string literal                                    |
| `'...'`                                                                | Literal karakter                                                                                 |
| `b'...'`                                                               | Literal byte ASCII                                                                               |
| <code>&vert;...&vert; expr</code>                                      | Closure                                                                                          |
| `!`                                                                    | Type bottom yang selalu kosong untuk fungsi divergen                                             |
| `_`                                                                    | Pengikatan pola “yang diabaikan”; juga dipakai untuk membuat literal integer mudah dibaca        |

Tabel B-3 menunjukkan simbol yang muncul dalam konteks *path* menuju suatu item
melalui hierarki *module*.

<span class="caption">Tabel B-3: Sintaks Terkait *Path*</span>

| Simbol                                  | Penjelasan                                                                                                                    |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `ident::ident`                          | Path ruang nama                                                                                                               |
| `::path`                                | Path relatif terhadap akar crate (yaitu, path yang secara eksplisit absolut)                                                  |
| `self::path`                            | Path relatif terhadap module saat ini (yaitu, path yang secara eksplisit relatif)                                             |
| `super::path`                           | Path relatif terhadap induk module saat ini                                                                                    |
| `type::ident`, `<type as trait>::ident` | Constant, fungsi, dan associated type                                                                                           |
| `<type>::...`                           | Item asosiasi untuk type yang tidak dapat dinamai secara langsung (misalnya, `<&T>::...`, `<[T]>::...`, dan seterusnya)        |
| `trait::method(...)`                    | Mendisambiguasi pemanggilan metode dengan menamai trait yang mendefinisikannya                                                 |
| `type::method(...)`                     | Mendisambiguasi pemanggilan metode dengan menamai type tempat metode itu didefinisikan                                         |
| `<type as trait>::method(...)`          | Mendisambiguasi pemanggilan metode dengan menamai trait dan typenya                                                             |

Tabel B-4 menunjukkan simbol yang muncul dalam konteks pemakaian parameter
generic type.

<span class="caption">Tabel B-4: *Generics*</span>

| Simbol                         | Penjelasan                                                                                                                                                     |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `path<...>`                    | Menentukan parameter untuk generic type dalam suatu type (misalnya, `Vec<u8>`)                                                                                 |
| `path::<...>`, `method::<...>` | Menentukan parameter untuk type, fungsi, atau metode generik dalam suatu expression; sering disebut _turbofish_ (misalnya, `"42".parse::<i32>()`)                 |
| `fn ident<...> ...`            | Mendefinisikan fungsi generik                                                                                                                                  |
| `struct ident<...> ...`        | Mendefinisikan struktur generik                                                                                                                                |
| `enum ident<...> ...`          | Mendefinisikan enumerasi generik                                                                                                                               |
| `impl<...> ...`                | Mendefinisikan implementasi generik                                                                                                                            |
| `for<...> type`                | Batasan lifetime berperingkat lebih tinggi                                                                                                                     |
| `type<ident=type>`             | Type generik yang satu atau beberapa associated type-nya memiliki penetapan spesifik (misalnya, `Iterator<Item=T>`)                                            |

Tabel B-5 menunjukkan simbol yang muncul dalam konteks pembatasan parameter
generic type dengan *trait bound*.

<span class="caption">Tabel B-5: Batasan *Trait Bound*</span>

| Simbol                        | Penjelasan                                                                                                                                              |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `T: U`                        | Parameter generik `T` dibatasi pada type-type yang mengimplementasikan `U`                                                                               |
| `T: 'a`                       | Type generik `T` harus hidup lebih lama daripada lifetime `'a` (artinya type itu tidak boleh memuat reference apa pun secara transitif dengan lifetime yang lebih pendek daripada `'a`) |
| `T: 'static`                  | Type generik `T` tidak memuat reference yang dipinjam selain reference `'static`                                                                         |
| `'b: 'a`                      | Lifetime generik `'b` harus hidup lebih lama daripada lifetime `'a`                                                                                      |
| `T: ?Sized`                   | Mengizinkan type parameter generik menjadi type berukuran dinamis                                                                                        |
| `'a + trait`, `trait + trait` | Batasan compound type                                                                                                                                     |

Tabel B-6 menunjukkan simbol yang muncul dalam konteks pemanggilan atau
pendefinisian *macro* dan penentuan atribut pada suatu item.

<span class="caption">Tabel B-6: *Macro* dan Atribut</span>

| Simbol                                      | Penjelasan         |
| ------------------------------------------- | ------------------ |
| `#[meta]`                                   | Atribut luar       |
| `#![meta]`                                  | Atribut dalam      |
| `$ident`                                    | Substitusi macro   |
| `$ident:kind`                               | Metavariabel macro |
| `$(...)...`                                 | Pengulangan macro  |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Invokasi macro     |

Tabel B-7 menunjukkan simbol yang membuat komentar.

<span class="caption">Tabel B-7: Komentar</span>

| Simbol     | Penjelasan            |
| ---------- | --------------------- |
| `//`       | Komentar baris        |
| `//!`      | Komentar dok baris dalam  |
| `///`      | Komentar dok baris luar  |
| `/*...*/`  | Komentar blok         |
| `/*!...*/` | Komentar dok blok dalam |
| `/**...*/` | Komentar dok blok luar |

Tabel B-8 menunjukkan konteks pemakaian tanda kurung.

<span class="caption">Tabel B-8: Tanda Kurung</span>

| Simbol                   | Penjelasan                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------- |
| `()`                     | Tuple kosong (alias unit), baik sebagai literal maupun type                                        |
| `(expr)`                 | Expression dalam tanda kurung                                                                        |
| `(expr,)`                | Expression tuple satu elemen                                                                         |
| `(type,)`                | Type tuple satu elemen                                                                             |
| `(expr, ...)`            | Expression tuple                                                                                     |
| `(type, ...)`            | Type tuple                                                                                         |
| `expr(expr, ...)`        | Expression pemanggilan fungsi; juga dipakai untuk menginisialisasi `struct` tuple dan varian `enum` tuple |

Tabel B-9 menunjukkan konteks pemakaian kurung kurawal.

<span class="caption">Tabel B-9: Kurung Kurawal</span>

| Konteks      | Penjelasan     |
| ------------ | -------------- |
| `{...}`      | Expression blok  |
| `Type {...}` | Literal struct |

Tabel B-10 menunjukkan konteks pemakaian kurung siku.

<span class="caption">Tabel B-10: Kurung Siku</span>

| Konteks                                            | Penjelasan                                                                                                                     |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `[...]`                                            | Literal array                                                                                                                  |
| `[expr; len]`                                      | Literal array berisi `len` salinan `expr`                                                                                      |
| `[type; len]`                                      | Type array berisi `len` instance dari `type`                                                                                   |
| `expr[expr]`                                       | Pengindeksan koleksi; dapat di-overload (`Index`, `IndexMut`)                                                                  |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]` | Pengindeksan koleksi yang berperan sebagai slicing koleksi, memakai `Range`, `RangeFrom`, `RangeTo`, atau `RangeFull` sebagai “index” |
