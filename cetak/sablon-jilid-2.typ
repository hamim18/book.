// Sablon sampul Jilid 2 untuk percetakan: satu lembar berisi
// belakang–punggung–depan dengan bleed 3 mm di keempat sisi.
// Trim: 176 × 250 mm (B5). Lebar punggung dihitung dari 437 halaman
// pada kertas 80 gsm (≈0,1 mm/lembar): 437/2 × 0,1 ≈ 21,9 mm.
// Untuk kertas lain, sesuaikan LEBAR_PUNGGUNG (70 gsm ≈ 19,2 mm,
// 100 gsm ≈ 26,2 mm).
#let LEBAR_PUNGGUNG = 21.9mm
#let WARNA = rgb("#6E2A1D")
#let KREM = rgb("#EFE8D8")

#set page(
  width: 3mm + 176mm + LEBAR_PUNGGUNG + 176mm + 3mm,
  height: 256mm,
  margin: 0pt,
  fill: WARNA,
)

// Belakang (bleed kiri + atas-bawah diisi warna latar halaman).
#place(top + left, dx: 3mm, dy: 3mm)[
  #image("img/sampul-belakang-jilid2.png", width: 176mm, height: 250mm)
]

// Punggung: warna latar seragam + judul tegak (baca atas ke bawah).
#place(top + left, dx: 3mm + 176mm, dy: 3mm)[
  #rect(fill: WARNA, width: LEBAR_PUNGGUNG, height: 250mm)[
    #align(center + horizon)[
      #rotate(-90deg)[
        #text(fill: KREM, size: 11pt, weight: 700)[The Rust Programming Language]
        #h(10pt)
        #text(fill: KREM, size: 9pt)[· JILID 2 ·]
      ]
    ]
  ]
]

// Depan (bleed kanan diisi warna latar halaman).
#place(top + left, dx: 3mm + 176mm + LEBAR_PUNGGUNG, dy: 3mm)[
  #image("img/sampul-depan-jilid2.png", width: 176mm, height: 250mm)
]
