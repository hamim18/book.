// Desain B — "Ferris Raksasa": krem hangat, siluet kepiting besar
// merah khas Ferris sebagai pahlawan visual, pita marun di bawah.
// Belakang: marun penuh. Pratinjau: typst compile b-ferris-raksasa.typ
// keluaran/sampul-b.png --format png
#set page(paper: "iso-b5", margin: 0pt, numbering: none, fill: rgb("#FBF6EE"))
#set text(font: "IBM Plex Serif", lang: "id")

// ---------- Depan ----------
#place(top + center, dy: 42pt)[
  #align(center)[
    #text(size: 25pt, weight: 700, fill: rgb("#7A1B18"))[The Rust Programming Language]
    #v(10pt)
    #rect(width: 56pt, height: 1.2pt, fill: rgb("#7A1B18"))
    #v(10pt)
    #text(size: 13.5pt, fill: rgb("#7A1B18"))[Terjemahan Bahasa Indonesia]
  ]
]

#place(horizon + center, dy: -4pt)[
  #image("/img/crab-merah.svg", width: 250pt)
]

#place(bottom)[
  #rect(fill: rgb("#7A1B18"), width: 100%, height: 172pt)[
    #align(center)[
      #v(30pt)
      #text(fill: white, size: 21pt, weight: 700)[JILID 1]
      #v(7pt)
      #text(fill: rgb("#F3D9C9"), size: 11pt)[Kata Pengantar · Pendahuluan · Bab 1–12]
      #v(7pt)
      #text(fill: rgb("#F3D9C9"), size: 9.5pt)[Steve Klabnik · Carol Nichols · Chris Krycho — diterjemahkan oleh AI]
    ]
  ]
]

// ---------- Belakang ----------
#pagebreak()
#set page(fill: rgb("#7A1B18"))

#place(top + center, dy: 44pt)[
  #align(center)[
    #text(fill: white, size: 15pt, weight: 700)[The Rust Programming Language]
    #v(8pt)
    #rect(width: 40pt, height: 1pt, fill: rgb("#F3D9C9"))
  ]
]

#place(horizon + center, dy: -26pt)[
  #block(width: 78%)[
    #align(center)[
      #text(fill: rgb("#F7ECE4"), size: 10.5pt)[
        Rust adalah bahasa pemrograman sistem yang cepat, andal, dan aman — tanpa pengumpul sampah. Buku resmi ini memandu Anda dari dasar: *variable*, *function*, *ownership*, hingga fitur paling canggih seperti generics, async, *unsafe*, dan macro. Ditutup dengan proyek akhir: membangun server web multithread dari nol.
      ]
      #v(16pt)
      #text(fill: rgb("#F3D9C9"), size: 10pt)[
        21 bab + 7 lampiran — terjemahan lengkap \
        Glosarium Inggris–Indonesia (±650 istilah) \
        Indeks istilah dengan nomor halaman \
        Kanal koreksi terbuka
      ]
    ]
  ]
]

#place(bottom + center, dy: -38pt)[
  #align(center)[
    #image("/img/crab-oranye.svg", width: 24pt)
    #v(10pt)
    #text(fill: rgb("#F3D9C9"), size: 9pt)[Edisi cetak pribadi · Oktober 2026]
  ]
]
