# Pattern dan Pencocokan

Pattern adalah sintaks khusus di Rust untuk mencocokkan struktur type, baik yang
kompleks maupun yang sederhana. Memakai pattern bersamaan dengan expression
`match` dan konstruksi lain memberi Anda kontrol yang lebih besar atas alur
kontrol program. Sebuah pattern terdiri dari kombinasi hal-hal berikut:

- Literal
- Array, *enum*, *struct*, atau *tuple* yang didestrukturisasi
- Variable
- Wildcard
- Placeholder

Beberapa contoh pattern mencakup `x`, `(a, 3)`, dan `Some(Color::Red)`. Pada
konteks tempat pattern valid, komponen-komponen ini menggambarkan bentuk data.
Program kita kemudian mencocokkan nilai terhadap pattern-pattern itu untuk
menentukan apakah ia memiliki bentuk data yang tepat untuk terus menjalankan
potongan kode tertentu.

Untuk memakai sebuah pattern, kita membandingkannya dengan suatu nilai. Jika
pattern itu cocok dengan nilainya, kita memakai bagian-bagian nilai itu di kode
kita. Ingat kembali expression `match` di Bab 6 yang memakai pattern, seperti
contoh mesin penyortir koin. Jika nilai itu sesuai dengan bentuk patternnya,
kita bisa memakai bagian-bagian yang diberi nama. Jika tidak, kode yang
dikaitkan dengan pattern itu tidak akan berjalan.

Bab ini adalah rujukan untuk segala hal yang berkaitan dengan pattern. Kita
akan membahas tempat-tempat yang valid untuk memakai pattern, perbedaan antara
pattern *refutable* dan *irrefutable*, serta berbagai jenis sintaks pattern yang
mungkin Anda lihat. Di akhir bab ini, Anda akan tahu cara memakai pattern untuk
mengekspresikan banyak konsep dengan cara yang jelas.
