# Pola dan Pencocokan

Pola adalah sintaks khusus di Rust untuk mencocokkan struktur type, baik yang
kompleks maupun yang sederhana. Memakai pola bersamaan dengan expression
`match` dan konstruksi lain memberi Anda kontrol yang lebih besar atas alur
kontrol program. Sebuah pola terdiri dari kombinasi hal-hal berikut:

- Literal
- Array, *enum*, *struct*, atau *tuple* yang didestrukturisasi
- Variable
- Wildcard
- Placeholder

Beberapa contoh pola mencakup `x`, `(a, 3)`, dan `Some(Color::Red)`. Pada
konteks tempat pola valid, komponen-komponen ini menggambarkan bentuk data.
Program kita kemudian mencocokkan nilai terhadap pola-pola itu untuk
menentukan apakah ia memiliki bentuk data yang tepat untuk terus menjalankan
potongan kode tertentu.

Untuk memakai sebuah pola, kita membandingkannya dengan suatu nilai. Jika
pola itu cocok dengan nilainya, kita memakai bagian-bagian nilai itu di kode
kita. Ingat kembali expression `match` di Bab 6 yang memakai pola, seperti
contoh mesin penyortir koin. Jika nilai itu sesuai dengan bentuk polanya,
kita bisa memakai bagian-bagian yang diberi nama. Jika tidak, kode yang
dikaitkan dengan pola itu tidak akan berjalan.

Bab ini adalah rujukan untuk segala hal yang berkaitan dengan pola. Kita
akan membahas tempat-tempat yang valid untuk memakai pola, perbedaan antara
pola *refutable* dan *irrefutable*, serta berbagai jenis sintaks pola yang
mungkin Anda lihat. Di akhir bab ini, Anda akan tahu cara memakai pola untuk
mengekspresikan banyak konsep dengan cara yang jelas.
