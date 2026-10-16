# Penanganan Galat

Galat adalah fakta kehidupan dalam perangkat lunak, jadi Rust memiliki
sejumlah fitur untuk menangani situasi ketika ada yang tidak beres. Dalam
banyak kasus, Rust mengharuskan Anda mengakui kemungkinan adanya galat dan
mengambil tindakan sebelum kode Anda mau dikompilasi. Persyaratan ini
membuat program Anda lebih tangguh dengan memastikan bahwa Anda akan
menemukan galat dan menanganinya dengan tepat sebelum menerapkan kode Anda
ke produksi!

Rust mengelompokkan galat menjadi dua kategori besar: galat yang dapat
dipulihkan dan galat yang tidak dapat dipulihkan. Untuk *galat yang dapat
dipulihkan*, seperti galat *file not found* (file tidak ditemukan),
kemungkinan besar kita hanya ingin melaporkan masalahnya kepada pengguna dan
mencoba ulang operasinya. *Galat yang tidak dapat dipulihkan* selalu
merupakan gejala bug, seperti mencoba mengakses lokasi melewati ujung array,
jadi kita ingin segera menghentikan program.

Sebagian besar bahasa tidak membedakan kedua jenis galat ini dan menangani
keduanya dengan cara yang sama, memakai mekanisme seperti *exception*. Rust
tidak memiliki exception. Sebagai gantinya, Rust memiliki tipe `Result<T,
E>` untuk galat yang dapat dipulihkan dan macro `panic!` yang menghentikan
eksekusi ketika program menemukan galat yang tidak dapat dipulihkan. Bab ini
pertama-tama membahas pemanggilan `panic!`, lalu membicarakan pengembalian
nilai `Result<T, E>`. Selain itu, kita akan mengeksplorasi
pertimbangan-pertimbangan ketika memutuskan apakah akan mencoba memulihkan
diri dari galat atau menghentikan eksekusi.
