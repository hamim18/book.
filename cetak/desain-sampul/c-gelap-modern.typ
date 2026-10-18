// Desain C — "Gelap Modern": arang gelap, judul rata kiri dengan aksen
// oranye, panel kode "Hello, world!" sebagai visual utama, badge jilid
// oranye di kanan bawah. Belakang: arang penuh. Pratinjau:
// typst compile c-gelap-modern.typ keluaran/sampul-c.png --format png
#set page(paper: "iso-b5", margin: 0pt, numbering: none, fill: rgb("#23272E"))
#set text(font: "IBM Plex Serif", lang: "id")

// ---------- Depan ----------
#place(top + left, dx: 36pt, dy: 46pt)[
  #block(width: 280pt)[
    #text(size: 26pt, weight: 700, fill: white)[The Rust Programming Language]
    #v(12pt)
    #rect(width: 56pt, height: 1.5pt, fill: rgb("#F74C00"))
    #v(12pt)
    #text(size: 13pt, fill: rgb("#D9DBE0"))[Terjemahan Bahasa Indonesia]
    #v(26pt)
    #text(size: 11pt, fill: rgb("#B8BCC4"))[Steve Klabnik · Carol Nichols · Chris Krycho]
    #v(4pt)
    #text(size: 10pt, fill: rgb("#B8BCC4"))[diterjemahkan oleh AI]
  ]
]

#place(horizon + center, dy: 14pt)[
  #block(width: 300pt)[
    #rect(
      fill: rgb("#2B303B"),
      stroke: (left: 2.5pt + rgb("#F74C00")),
      inset: (x: 22pt, y: 20pt),
      radius: 6pt,
    )[
      #set text(font: "IBM Plex Mono", size: 14pt, fill: rgb("#EDEEF0"))
      fn main() { \
          println!("Hello, world!"); \
      }
    ]
  ]
]

#place(bottom + right, dx: -34pt, dy: -34pt)[
  #rect(fill: rgb("#F74C00"), radius: 8pt, inset: (x: 16pt, y: 10pt))[
    #text(fill: white, size: 12pt, weight: 700)[JILID 1 · BAB 1–12]
  ]
]

// ---------- Belakang ----------
#pagebreak()

#place(top + left, dx: 36pt, dy: 46pt)[
  #align(left)[
    #text(size: 13pt, weight: 700, fill: white)[The Rust Programming Language]
    #v(8pt)
    #rect(width: 36pt, height: 1pt, fill: rgb("#F74C00"))
  ]
]

#place(horizon + center, dy: -30pt)[
  #block(width: 78%)[
    #align(center)[
      #text(fill: rgb("#D9DBE0"), size: 10.5pt)[
        Rust adalah bahasa pemrograman sistem yang cepat, andal, dan aman — tanpa pengumpul sampah. Buku resmi ini memandu Anda dari dasar: *variable*, *function*, *ownership*, hingga fitur paling canggih seperti generics, async, *unsafe*, dan macro. Ditutup dengan proyek akhir: membangun server web multithread dari nol.
      ]
      #v(16pt)
      #text(fill: rgb("#B8BCC4"), size: 10pt)[
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
    #text(fill: rgb("#8A919E"), size: 9pt)[Edisi cetak pribadi · Oktober 2026]
  ]
]
