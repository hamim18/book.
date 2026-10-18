// Templat cetak buku: B5, dua jilid.
// Kerangka awal (2026-10-17); gaya disempurnakan setelah uji coba bab.

#import "@preview/codly:2.0.0" as codly

// Kotak catatan: pembungkus <section class="note"> dari mdBook disulap
// filter Lua menjadi #catatan[...]. Latar krem muda + garis tepi kiri.
#let catatan(body) = block(
  fill: rgb("#f4f3f0"),
  stroke: (left: 3pt + rgb("#b0aea8")),
  inset: (x: 10pt, y: 8pt),
  radius: 2pt,
  width: 100%,
  breakable: true,
  body,
)

// Caption gambar/tabel/listing ("Gambar 4-1: ...", "Tabel B-1: ...",
// "Listing 6-8: ..."): rata tengah, sedikit lebih kecil dari teks isi.
// Dipakai oleh cetak/lepas-figure.py saat membungkus paragraf caption.
#let caption(body) = block(
  above: 9pt,
  below: 13pt,
  breakable: true,
)[
  #align(center)[#text(size: 9pt)[#body]]
]

// Penomoran heading: "Bab N" untuk level 1, "N.M" untuk di bawahnya.
// offset menggeser angka level 1 (Jilid 2 mulai dari Bab 13).
#let nomor(offset) = (..n) => {
  let angka = n.pos()
  if angka.len() == 1 {
    "Bab " + str(angka.first() + offset)
  } else {
    angka.map(str).join(".")
  }
}

// Aturan gaya dasar, dipakai build penuh dan pratinjau bab.
#let gaya(body) = {
  // Margin buku cetak B5: sisi dalam lebih lebar untuk ruang jilid.
  set page(paper: "iso-b5", margin: (inside: 22mm, outside: 15mm, top: 18mm, bottom: 20mm), numbering: "1")
  set text(font: "IBM Plex Serif", size: 10pt, lang: "id")
  set par(justify: true)

  // Heading: serif tebal; ukuran bertingkat.
  show heading: set text(font: "IBM Plex Serif", weight: 600)
  show heading.where(level: 1): set text(size: 16pt)
  show heading.where(level: 2): set text(size: 12.5pt)
  show heading.where(level: 3): set text(size: 10.5pt)

  // Tautan web tidak berwarna di cetak.
  show link: set text(fill: black)

  // Kode inline (backtick di prosa).
  show raw: set text(font: "IBM Plex Mono", size: 9pt)

  // Blok kode: Codly melipat baris panjang dengan penanda sambungan tanpa
  // mengubah teks sumber. Tanpa nomor baris dan badge bahasa; latar kelabu
  // muda seragam (zebra bawaan dimatikan). leading: 1.5pt merapatkan jarak
  // antar-baris (bawaan codly 0.32em per sisi) agar blok lebih ringkas.
  show: codly.line-set_(fill: none)
  show raw.where(block: true): it => {
    set text(font: "IBM Plex Mono", size: 8.5pt)
    block(
      fill: rgb("#f6f6f4"),
      inset: 7pt,
      radius: 2pt,
      width: 100%,
      breakable: true,
      codly.new(
        it,
        padding: 0pt,
        number-enabled: false,
        lang-position: none,
        file: none,
        wrap-marker: [↪ ],
        leading: 1.5pt,
      ),
    )
  }

  body
}

// Dokumen lengkap satu jilid. Urutan: sampul, halaman judul, hak cipta,
// kata pengantar penerjemah, kata pengantar penulis, panduan membaca,
// daftar isi, pendahuluan, bab bernomor (mulai Bab offset+1), lampiran,
// lalu materi belakang (glosarium, referensi, indeks, profil, info edisi).
// Semua selain bab bernomor tanpa nomor heading. Setiap heading level 1
// memulai halaman baru.
#let dokumen(
  judul-jilid,
  cakupan-jilid,
  sampul-depan: none,
  sampul-belakang: none,
  hak-cipta: none,
  kata-pengantar: none,
  foreword: none,
  panduan: none,
  pendahuluan: none,
  isi: none,
  lampiran: none,
  belakang: none,
  offset-bab: 0,
) = {
  gaya[
    // Heading level 1 selalu memulai halaman baru dan rata tengah
    // (judul bab).
    // PENTING: show rule ini harus berada di level atas konten — bila
    // dibungkus block[...], pagebreak-nya memicu galat "pagebreaks are
    // not allowed inside of containers" (ditemukan lewat uji bisect
    // 2026-10-17; breakable: true pun tidak menolong).
    #show heading.where(level: 1): it => {
      pagebreak()
      set align(center)
      it
    }

    // ---------- Sampul depan (tanpa nomor halaman) ----------
    // Desain pengguna (2026-10-18): PNG 300 DPI full-bleed di cetak/img/.
    // Bila tidak ada, pakai sampul teks sederhana (cadangan).
    #if sampul-depan != none [
      #set page(numbering: none, margin: 0pt)
      #image(sampul-depan, width: 100%, height: 100%)
    ] else [
      #set page(numbering: none)
      #align(center)[
        #v(3.5cm)
        #text(size: 26pt, weight: 700)[The Rust Programming Language]
        #v(6mm)
        #text(size: 14pt)[Terjemahan Bahasa Indonesia]
        #v(1.6cm)
        #text(size: 12pt)[Steve Klabnik · Carol Nichols · Chris Krycho]
        #v(3mm)
        #text(size: 11pt)[diterjemahkan oleh AI]
        #v(3cm)
        #text(size: 13pt)[#judul-jilid — #cakupan-jilid]
      ]
    ]

    // ---------- Halaman judul ----------
    #pagebreak()
    #set page(margin: (inside: 22mm, outside: 15mm, top: 18mm, bottom: 20mm))
    #align(center)[
      #v(3cm)
      #text(size: 22pt, weight: 600)[The Rust Programming Language]
      #v(8mm)
      #text(size: 13pt)[#judul-jilid]
      #text(size: 11pt)[#cakupan-jilid]
      #v(2.5cm)
      #text(size: 11pt)[Steve Klabnik, Carol Nichols, Chris Krycho]
      #v(2mm)
      #text(size: 11pt)[terjemahan bahasa Indonesia oleh AI]
      #v(6mm)
      #text(size: 9.5pt)[versi teks Rust 1.98.0 · edition 2024]
    ]
    #set page(numbering: "1")

    // ---------- Bagian awal & depan (tanpa nomor) ----------
    #if hak-cipta != none { hak-cipta }
    #if kata-pengantar != none { kata-pengantar }
    #if foreword != none { foreword }
    #if panduan != none { panduan }

    // ---------- Daftar isi ----------
    #set outline.entry(fill: repeat([.]))
    #outline(title: [Daftar Isi], depth: 3)

    #if pendahuluan != none { pendahuluan }

    // ---------- Isi (bab bernomor) ----------
    #if isi != none {
      set heading(numbering: nomor(offset-bab))
      isi
    }

    // ---------- Lampiran + materi belakang (tanpa nomor) ----------
    #if lampiran != none {
      set heading(numbering: none)
      lampiran
    }
    #if belakang != none {
      set heading(numbering: none)
      belakang
    }

    // ---------- Sampul belakang (halaman terakhir, full-bleed) ----------
    #if sampul-belakang != none [
      #pagebreak()
      #set page(numbering: none, margin: 0pt)
      #image(sampul-belakang, width: 100%, height: 100%)
    ]
  ]
}

// Pratinjau satu bab tanpa halaman judul/daftar isi (mode dev).
#let pratinjau(isi) = gaya[#isi]
