# Menggunakan Struct untuk Menyusun Data yang Berkaitan

Sebuah *struct*, atau *structure*, adalah data custom type yang memungkinkan
Anda mengemas dan memberi nama pada beberapa nilai terkait yang membentuk
sebuah kelompok yang bermakna. Jika Anda familier dengan bahasa berorientasi
objek, *struct* mirip dengan atribut data sebuah objek. Dalam bab ini, kita akan
membandingkan dan membedakan *tuple* dengan *struct* untuk membangun di atas apa
yang sudah Anda ketahui, dan menunjukkan kapan *struct* adalah cara yang lebih
baik untuk mengelompokkan data.

Kita akan menunjukkan cara mendefinisikan dan menginstansiasi *struct*. Kita
akan membahas cara mendefinisikan *associated function* (fungsi asosiasi),
khususnya jenis *associated function* yang disebut metode, untuk menentukan
perilaku yang terkait dengan sebuah type *struct*. *Struct* dan *enum* (dibahas di
Bab 6) adalah blok penyusun untuk membuat type baru di dalam domain program
Anda guna memanfaatkan sepenuhnya pemeriksaan type pada waktu kompilasi milik
Rust.
