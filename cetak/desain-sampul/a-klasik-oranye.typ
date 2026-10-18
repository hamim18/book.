// Desain A — "Klasik Oranye": putih bersih, emblem kepiting kecil,
// tipografi serif terpusat, pita oranye di bawah. Belakang: oranye penuh.
// Pratinjau: typst compile a-klasik-oranye.typ keluaran/sampul-a.png --format png
#set page(paper: "iso-b5", margin: 0pt, numbering: none, fill: white)
#set text(font: "IBM Plex Serif", lang: "id")

// ---------- Depan ----------
#place(top + center, dy: 50pt)[
  #align(center)[
    #image("/img/crab-oranye.svg", width: 44pt)
    #v(22pt)
    #text(size: 27pt, weight: 700)[The Rust Programming Language]
    #v(12pt)
    #rect(width: 62pt, height: 1.2pt, fill: rgb("#F74C00"))
    #v(12pt)
    #text(size: 14pt)[Terjemahan Bahasa Indonesia]
    #v(30pt)
    #text(size: 12pt)[Steve Klabnik · Carol Nichols · Chris Krycho]
    #v(5pt)
    #text(size: 11pt)[diterjemahkan oleh AI]
  ]
]

#place(bottom)[
  #rect(fill: rgb("#F74C00"), width: 100%, height: 208pt)[
    #align(center)[
      #v(40pt)
      #text(fill: white, size: 25pt, weight: 700)[JILID 1]
      #v(8pt)
      #text(fill: white, size: 11.5pt)[Kata Pengantar · Pendahuluan · Bab 1–12]
      #v(10pt)
      #text(fill: white, size: 9.5pt)[edisi 2024 · Rust 1.98]
    ]
  ]
]

// ---------- Belakang ----------
#pagebreak()
#set page(fill: rgb("#F74C00"))

#place(top + center, dy: 44pt)[
  #align(center)[
    #text(fill: white, size: 15pt, weight: 700)[The Rust Programming Language]
    #v(8pt)
    #rect(width: 40pt, height: 1pt, fill: white)
  ]
]

#place(horizon + center, dy: -26pt)[
  #block(width: 78%)[
    #align(center)[
      #text(fill: white, size: 10.5pt)[
        Rust adalah bahasa pemrograman sistem yang cepat, andal, dan aman — tanpa pengumpul sampah. Buku resmi ini memandu Anda dari dasar: *variable*, *function*, *ownership*, hingga fitur paling canggih seperti generics, async, *unsafe*, dan macro. Ditutup dengan proyek akhir: membangun server web multithread dari nol.
      ]
      #v(16pt)
      #text(fill: white, size: 10pt)[
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
    #image("/img/crab-putih.svg", width: 24pt)
    #v(10pt)
    #text(fill: white, size: 9pt)[Edisi cetak pribadi · Oktober 2026]
  ]
]
