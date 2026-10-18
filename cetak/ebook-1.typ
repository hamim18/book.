// E-book Jilid 1 — sama dengan jilid cetak, tetapi margin kiri dan
// kanan sama (x: 18,5 mm) dengan lebar area teks sama dengan cetak (139 mm)
// sehingga paginasi dan nomor halaman indeks tidak berubah.
// Jilid 1 — lengkap: sampul, judul, hak cipta, kata pengantar penerjemah,
// kata pengantar penulis, panduan membaca, daftar isi, pendahuluan,
// Bab 1-12, lampiran, glosarium, referensi, indeks, profil, informasi edisi.

#import "template.typ": dokumen

#dokumen(
  "Jilid 1",
  "Kata Pengantar, Pendahuluan, Bab 1–12, Lampiran, Glosarium, Indeks",
  sampul-depan: "img/sampul-depan-jilid1.png",
  sampul-belakang: "img/sampul-belakang-jilid1.png",
  hak-cipta: include("build/hak-cipta.typ"),
  kata-pengantar: include("build/kata-pengantar-penerjemah.typ"),
  foreword: include("build/foreword.typ"),
  panduan: include("build/panduan-membaca.typ"),
  pendahuluan: include("build/pendahuluan.typ"),
  isi: include("build/jilid-1.typ"),
  lampiran: include("build/lampiran.typ"),
  belakang: [
    #include("build/glosarium.typ")
    #include("build/referensi.typ")
    #include("build/indeks.typ")
    #include("build/profil.typ")
    #include("build/info-edisi.typ")
  ],
  margin: (x: 18.5mm, top: 18mm, bottom: 20mm),
)
