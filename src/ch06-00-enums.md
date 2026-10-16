# Enums dan Pattern Matching (Pencocokan Pola)

Dalam bab ini, kita akan melihat enumerasi, yang juga disebut *enum*. Enum
memungkinkan Anda mendefinisikan sebuah tipe dengan menyebutkan satu per satu
*variant* (varian) yang mungkin. Pertama-tama kita akan mendefinisikan dan
memakai sebuah enum untuk menunjukkan bagaimana enum dapat mengkodekan makna
beserta data. Selanjutnya, kita akan mengeksplorasi sebuah enum yang sangat
berguna, bernama `Option`, yang menyatakan bahwa sebuah nilai dapat berupa
sesuatu atau tidak ada apa pun. Lalu, kita akan melihat bagaimana *pattern
matching* (pencocokan pola) dalam ekspresi `match` memudahkan kita menjalankan
kode yang berbeda untuk nilai enum yang berbeda. Terakhir, kita akan membahas
bagaimana konstruk `if let` adalah idiom praktis dan ringkas lainnya yang
tersedia untuk menangani enum di kode Anda.
