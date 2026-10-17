<!-- Old headings. Do not remove or links may break. -->

<a id="managing-growing-projects-with-packages-crates-and-modules"></a>

# Mengelola Proyek yang Berkembang dengan Package (Paket), Crate, dan Module (Modul)

Saat Anda menulis program yang besar, pengaturan kode akan menjadi semakin
penting. Dengan mengelompokkan fungsionalitas yang berkaitan dan memisahkan
kode dengan fitur-fitur yang berbeda, Anda akan memperjelas tempat menemukan
kode yang mengimplementasikan sebuah fitur tertentu dan tempat yang harus
dituju untuk mengubah cara kerja sebuah fitur.

Program-program yang kita tulis sejauh ini berada dalam satu *module* (modul)
di dalam satu file. Seiring berkembangnya sebuah proyek, Anda harus mengatur
kode dengan membaginya ke dalam beberapa module, lalu ke dalam beberapa file.
Sebuah *package* (paket) dapat berisi beberapa *crate* binary dan, opsional,
satu crate library. Seiring berkembangnya sebuah package, Anda dapat
mengekstrak bagian-bagiannya ke dalam crate-crate terpisah yang menjadi
dependensi eksternal. Bab ini membahas semua teknik tersebut. Untuk proyek
yang sangat besar yang terdiri atas sekumpulan package yang saling terkait dan
berkembang bersama, Cargo menyediakan workspace, yang akan kita bahas di
[“Workspace Cargo”][workspaces]<!-- ignore --> di Bab 14.

Kita juga akan membahas enkapsulasi detail implementasi, yang memungkinkan
Anda memakai ulang kode pada tingkat yang lebih tinggi: begitu Anda
mengimplementasikan sebuah operasi, kode lain dapat memanggil kode Anda lewat
antarmuka publiknya tanpa perlu tahu cara kerja implementasinya. Cara Anda
menulis kode menentukan bagian mana yang publik untuk dipakai kode lain dan
bagian mana yang merupakan detail implementasi privat yang hak perubahannya
Anda simpan sendiri. Ini cara lain untuk membatasi banyaknya detail yang harus
Anda simpan di kepala.

Konsep yang berkaitan adalah *scope* (cakupan): konteks bersarang tempat kode
ditulis memiliki sekumpulan nama yang didefinisikan sebagai “berada di dalam
scope”. Ketika membaca, menulis, dan mengompilasi kode, pemrogram dan
*compiler* (kompilator) perlu tahu apakah sebuah nama pada titik tertentu
merujuk ke variabel, fungsi, struct, enum, module, konstanta, atau item lain,
dan apa makna item tersebut. Anda dapat membuat scope dan mengubah nama-nama
mana yang berada di dalam atau di luar scope. Anda tidak dapat memiliki dua
item dengan nama yang sama di dalam scope yang sama; tersedia perangkat untuk
menyelesaikan konflik nama.

Rust memiliki sejumlah fitur yang memungkinkan Anda mengelola pengaturan kode
Anda, termasuk detail mana yang diekspos, detail mana yang privat, dan
nama-nama apa saja yang berada di setiap scope di dalam program Anda.
Fitur-fitur ini, yang kadang secara kolektif disebut sebagai *module system*
(sistem modul), meliputi:

* **Package**: Fitur Cargo yang memungkinkan Anda membangun, menguji, dan
  membagikan crate
* **Crate**: Pohon modul yang menghasilkan library atau program yang dapat
  dieksekusi
* **Module dan use**: Memungkinkan Anda mengontrol pengaturan, scope, dan
  privasi path
* **Path**: Cara memberi nama sebuah item, seperti struct, fungsi, atau module

Dalam bab ini, kita akan membahas semua fitur ini, mendiskusikan bagaimana
fitur-fitur tersebut berinteraksi, dan menjelaskan cara menggunakannya untuk
mengelola scope. Pada akhir bab ini, Anda akan memiliki pemahaman yang solid
tentang module system dan mampu bekerja dengan scope seperti seorang
profesional!

[workspaces]: ch14-03-cargo-workspaces.html
