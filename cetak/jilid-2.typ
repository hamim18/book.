// Jilid 2 — lengkap: sampul, judul, hak cipta, kata pengantar penerjemah,
// kata pengantar penulis, panduan membaca, daftar isi, pendahuluan,
// Bab 13-21, lampiran, glosarium, referensi, indeks, profil, informasi edisi.

#import "template.typ": dokumen

#dokumen(
  "Jilid 2",
  "Kata Pengantar, Pendahuluan, Bab 13–21, Lampiran, Glosarium, Indeks",
  hak-cipta: include("build/hak-cipta.typ"),
  kata-pengantar: include("build/kata-pengantar-penerjemah.typ"),
  foreword: include("build/foreword.typ"),
  panduan: include("build/panduan-membaca.typ"),
  pendahuluan: include("build/pendahuluan.typ"),
  isi: include("build/jilid-2.typ"),
  lampiran: include("build/lampiran.typ"),
  belakang: [
    #include("build/glosarium.typ")
    #include("build/referensi.typ")
    #include("build/indeks.typ")
    #include("build/profil.typ")
    #include("build/info-edisi.typ")
  ],
  offset-bab: 12,
)
