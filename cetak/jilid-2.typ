// Jilid 2: sampul, judul, daftar isi, Bab 13-21, lampiran, glosarium,
// referensi, indeks, profil, informasi edisi.

#import "template.typ": dokumen

#dokumen(
  "Jilid 2",
  "Bab 13–21, Lampiran, Glosarium, Indeks",
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
