# Memahami Ownership (Kepemilikan)

*Ownership* adalah fitur paling unik dari Rust dan memiliki implikasi yang
mendalam bagi bahasa ini secara keseluruhan. Fitur ini memungkinkan Rust
menjamin keamanan memori tanpa membutuhkan *garbage collector* (pengumpul
sampah), sehingga penting untuk memahami cara kerja *ownership*. Dalam bab ini,
kita akan membahas *ownership* beserta beberapa fitur terkait: *borrowing*
(peminjaman), *slice*, dan cara Rust menata data di dalam memori.
