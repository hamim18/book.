# Penanganan Error

Error adalah fakta kehidupan dalam perangkat lunak, jadi Rust memiliki
sejumlah fitur untuk menangani situasi ketika ada yang tidak beres. Dalam
banyak kasus, Rust mengharuskan Anda mengakui kemungkinan adanya error dan
mengambil tindakan sebelum kode Anda mau dikompilasi. Persyaratan ini
membuat program Anda lebih tangguh dengan memastikan bahwa Anda akan
menemukan error dan menanganinya dengan tepat sebelum menerapkan kode Anda
ke produksi!

Rust mengelompokkan error menjadi dua kategori besar: error yang dapat
dipulihkan dan error yang tidak dapat dipulihkan. Untuk *error yang dapat
dipulihkan*, seperti error *file not found* (file tidak ditemukan),
kemungkinan besar kita hanya ingin melaporkan masalahnya kepada pengguna dan
mencoba ulang operasinya. *Error yang tidak dapat dipulihkan* selalu
merupakan gejala bug, seperti mencoba mengakses lokasi melewati ujung array,
jadi kita ingin segera menghentikan program.

Sebagian besar bahasa tidak membedakan kedua jenis error ini dan menangani
keduanya dengan cara yang sama, memakai mekanisme seperti *exception*. Rust
tidak memiliki exception. Sebagai gantinya, Rust memiliki type `Result<T,
E>` untuk error yang dapat dipulihkan dan macro `panic!` yang menghentikan
eksekusi ketika program menemukan error yang tidak dapat dipulihkan. Bab ini
pertama-tama membahas pemanggilan `panic!`, lalu membicarakan pengembalian
nilai `Result<T, E>`. Selain itu, kita akan mengeksplorasi
pertimbangan-pertimbangan ketika memutuskan apakah akan mencoba memulihkan
diri dari error atau menghentikan eksekusi.
