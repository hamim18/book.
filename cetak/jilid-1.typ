// Jilid 1: sampul, judul, hak cipta, kata pengantar penerjemah,
// kata pengantar penulis, panduan membaca, daftar isi, pendahuluan,
// Bab 1-12.

#import "template.typ": dokumen

#dokumen(
  "Jilid 1",
  "Kata Pengantar, Pendahuluan, Bab 1–12",
  hak-cipta: include("build/hak-cipta.typ"),
  kata-pengantar: include("build/kata-pengantar-penerjemah.typ"),
  foreword: include("build/foreword.typ"),
  panduan: include("build/panduan-membaca.typ"),
  pendahuluan: include("build/pendahuluan.typ"),
  isi: include("build/jilid-1.typ"),
)
