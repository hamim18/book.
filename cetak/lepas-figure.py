#!/usr/bin/env python3
"""Buka pembungkus #figure pandoc pada .typ hasil konversi HTML -> Typst.

Pandoc membungkus blok kode + caption listing dengan #figure(...) dan tabel
dengan #figure(align(center)[#table(...)], kind: table). Figure Typst tidak
bisa pecah lintas halaman, sehingga listing/tabel yang lebih tinggi dari sisa
halaman dipaksa muat satu halaman: bagian bawah terpotong dan caption menimpa
nomor halaman. Di sini:

1. Figure listing diubah jadi #block(breakable: true)[...] dengan caption
   #caption[...] di dalamnya (ikut blok saat pecah lintas halaman).
2. Figure tabel dibuka jadi #table(...) polos (tabel Typst bisa pecah
   lintas halaman; header diulang lewat show rule di template.typ).
3. Paragraf caption Gambar/Tabel (sudah polos dari pandoc) dibungkus
   #caption[...] supaya gayanya seragam, dengan label <cap-jenis-N-M>
   untuk pemeriksaan halaman lewat `typst eval`.
4. Gambar (SVG tanpa ukuran bawaan) dirender Typst selebar viewBox — jauh
   melebihi kolom teks (±394 pt). Lebar diatur di sini (bukan show rule)
   karena path relatif "media/..." hanya benar bila ditulis di file .typ
   tempat gambar dipanggil. Peta ukuran alami di bawah diukur lewat
   `measure(image(...))`; assert memastikan gambar baru tidak lolos tanpa
   lebar.

Dipanggil oleh konversi.sh dan dev-bab.sh setelah pandoc, dijalankan dari
akar repo.
"""
import re
import sys
from pathlib import Path

# File hasil konversi pandoc yang dirapikan (konversi.sh), atau nama file
# tunggal bila dipanggil dengan argumen (dev-bab.sh).
DAFTAR_BAWAAN = ["foreword", "pendahuluan", "jilid-1", "jilid-2", "lampiran"]

RE_CAPTION = re.compile(r"^(Gambar|Tabel) ([0-9A-Za-z-]+):")
RE_LABEL = re.compile(r"Listing (\d+-\d+)|Gambar (\d+-\d+)|Tabel ([A-Z]-\d+)")

# Lebar alami gambar diukur Typst (pt); 394 pt = lebar kolom teks B5 dengan
# margin dalam 22 mm + luar 15 mm. None = biarkan ukuran alami.
LEBAR_GAMBAR = {
    "ferris/does_not_compile.svg": 70,
    "ferris/panics.svg": 70,
    "ferris/not_desired_behavior.svg": 70,
    "trpl04-01.svg": 394,
    "trpl04-02.svg": 394,
    "trpl04-03.svg": 394,
    "trpl04-04.svg": 394,
    "trpl04-05.svg": 394,
    "trpl04-06.svg": 394,
    "trpl04-07.svg": 394,
    "trpl14-01.png": 394,
    "trpl14-02.png": 394,
    "trpl14-03.png": 394,
    "trpl14-04.png": 394,
    "trpl15-01.svg": 394,
    "trpl15-02.svg": None,
    "trpl15-03.svg": 394,
    "trpl15-04.svg": 394,
    "trpl17-01.svg": 394,
    "trpl17-02.svg": 394,
    "trpl17-03.svg": 394,
    "trpl17-04.svg": None,
    "trpl17-05.svg": 394,
    "trpl17-06.svg": 394,
    "trpl17-07.svg": 394,
    "trpl17-08.svg": 394,
    "trpl17-09.svg": 394,
    "trpl21-01.png": None,
}

# Gambar bisa berada di awal baris (prosa), di dalam sel tabel, atau di
# dalam figure gambar (tanpa pembungkus #box).
RE_GAMBAR_AWAL = re.compile(r'(?:#box\()?image\("media/img/([^"]+)", alt: ')


def label_dari_caption(teks: str) -> str | None:
    m = RE_LABEL.search(teks)
    if not m:
        return None
    for jenis, g in zip(("listing", "gambar", "tabel"), m.groups()):
        if g:
            return f"cap-{jenis}-{g}"
    return None


def rapikan_gambar(b: str) -> str:
    """Sisipkan lebar gambar sesuai peta LEBAR_GAMBAR; garis tanpa gambar
    dikembalikan apa adanya. Idempoten: garis yang sudah memuat width tidak
    diubah."""
    g = RE_GAMBAR_AWAL.search(b)
    if not g:
        return b
    nama = g.group(1)
    if nama not in LEBAR_GAMBAR:
        sys.exit(f"galat: gambar {nama} belum ada di peta LEBAR_GAMBAR")
    lebar = LEBAR_GAMBAR[nama]
    if lebar is None or ", width:" in b[g.end():]:
        return b
    # Panggilan image() ditutup oleh `))` pertama setelah alt bila dibungkus
    # #box(...), atau oleh `)` terakhir bila berdiri sendiri (alt bisa memuat
    # tanda kurung, jadi tidak boleh mencari `)` pertama).
    diboks = b[g.start():].startswith("#box(")
    pos = b.find("))", g.end()) if diboks else b.rfind(")")
    if pos < 0:
        sys.exit(f"galat: tidak ada penutup image() di: {b[:70]!r}")
    return b[:pos] + f", width: {lebar}pt" + b[pos:]


def proses(teks: str) -> str:
    baris = teks.split("\n")
    hasil: list[str] = []
    i, n = 0, len(baris)
    while i < n:
        b = baris[i]
        if b.startswith("#figure(image(") and b.rstrip().endswith("),"):
            # ---- Figure gambar: #figure(image(...), caption: [...]) ----
            # Panggilan image() diambil utuh dari argumen pertama figure,
            # lalu lebar diatur lewat peta LEBAR_GAMBAR.
            panggilan = "image(" + b[len("#figure("):-2] + ")"
            hasil.append(rapikan_gambar(panggilan))
            i += 1
            if i < n and baris[i] == "  caption: [":
                i += 1
                cap = []
                while i < n and baris[i] != "  ]":
                    cap.append(baris[i].strip())
                    i += 1
                if i >= n:
                    sys.exit("galat: caption gambar tanpa penutup `  ]`")
                i += 1  # lewati "  ]"
                teks_cap = " ".join(x for x in cap if x)
                if teks_cap:
                    lab = label_dari_caption(teks_cap)
                    hasil.append(
                        f"#caption[{teks_cap}]" + (f" <{lab}>" if lab else "")
                    )
            if i >= n or baris[i] != ")":
                sys.exit(f"galat: penutup figure gambar tak terduga: "
                         f"{baris[i]!r}")
            i += 1  # lewati ")"
            continue

        if b.startswith("#figure(["):
            # ---- Figure listing: #figure([BODY ... ], caption: [...]) ----
            hasil.append("#block(breakable: true)[" + b[len("#figure(["):])
            i += 1
            badan = []
            while i < n and not (
                baris[i] == "  ]," and i + 1 < n and baris[i + 1] == "  caption: ["
            ):
                badan.append(baris[i])
                i += 1
            if i >= n:
                sys.exit(f"galat: figure listing tanpa penutup `  ],` "
                         f"di dekat baris {len(hasil)}")
            hasil.extend(badan)
            i += 1  # lewati "  ],"
            i += 1  # lewati "  caption: ["
            cap = []
            while i < n and baris[i] != "  ]":
                cap.append(baris[i].strip())
                i += 1
            if i >= n:
                sys.exit("galat: caption listing tanpa penutup `  ]`")
            i += 1  # lewati "  ]"
            if i >= n or baris[i] != ")":
                sys.exit(f"galat: penutup figure listing tak terduga: "
                         f"{baris[i]!r}")
            i += 1  # lewati ")"
            teks_cap = " ".join(x for x in cap if x)
            if teks_cap:
                hasil.append("#v(4pt)")
                lab = label_dari_caption(teks_cap)
                hasil.append(
                    f"#caption[{teks_cap}]" + (f" <{lab}>" if lab else "")
                )
            hasil.append("]")
            continue

        if b == "#figure(" and i + 1 < n and baris[i + 1] == "  align(center)[#table(":
            # ---- Figure tabel ----
            hasil.append("#table(")
            i += 2
            while i < n and baris[i] != "  )]":
                hasil.append(rapikan_gambar(baris[i]))
                i += 1
            if (
                i + 2 >= n
                or baris[i + 1] != "  , kind: table"
                or baris[i + 2] != "  )"
            ):
                sys.exit(f"galat: penutup figure tabel tak terduga di "
                         f"baris {i}")
            hasil.append("  )")
            i += 3
            continue

        m = RE_CAPTION.match(b)
        if m:
            # ---- Paragraf caption gambar/tabel ----
            jenis = {"Gambar": "gambar", "Tabel": "tabel"}[m.group(1)]
            hasil.append(f"#caption[{b}] <cap-{jenis}-{m.group(2)}>")
            i += 1
            continue

        g = RE_GAMBAR_AWAL.search(b)
        if g:
            # ---- Gambar di prosa: atur lebar sesuai peta ----
            hasil.append(rapikan_gambar(b))
            i += 1
            continue

        hasil.append(b)
        i += 1

    teks_baru = "\n".join(hasil)
    # Sisa pola berarti ada bentuk yang belum ditangani.
    if "\n  caption: [" in teks_baru:
        sys.exit("galat: masih ada sisa `  caption: [` setelah pemrosesan")
    sisa_figure = re.search(r"^#figure\(", teks_baru, re.M)
    if sisa_figure:
        sys.exit(f"galat: masih ada sisa #figure: {sisa_figure.group(0)!r}")
    # Gambar yang seharusnya diberi lebar tidak boleh lolos tanpa width.
    for baris_g in teks_baru.split("\n"):
        awal = re.search(r'(?:#box\()?image\("media/img/([^"]+)", alt: ', baris_g)
        if not awal:
            continue
        nama = awal.group(1)
        if LEBAR_GAMBAR.get(nama) is None:
            continue  # memang dibiarkan ukuran alami
        if ", width:" not in baris_g[awal.start():]:
            sys.exit(f"galat: gambar {nama} lolos tanpa lebar: {baris_g[:70]!r}")
    return teks_baru


def main() -> None:
    akar = Path(__file__).resolve().parent.parent
    nama = sys.argv[1:] or DAFTAR_BAWAAN
    for n in nama:
        target = akar / "cetak" / "build" / f"{n}.typ"
        if not target.exists():
            sys.exit(f"galat: {target} tidak ada")
        teks = target.read_text()
        teks_baru = proses(teks)
        target.write_text(teks_baru)
        print(f"rapikan: {n}.typ")


if __name__ == "__main__":
    main()
