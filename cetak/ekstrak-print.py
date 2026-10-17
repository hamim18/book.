#!/usr/bin/env python3
"""Ekstrak isi `book/print.html` (output mdBook) menjadi fragmen HTML
siap dikonversi Pandoc ke Typst.

Keluarannya (di `cetak/build/`):
- `depan.html`    : kata pengantar + pendahuluan (tanpa nomor bab)
- `jilid-1.html`  : bab 1-12
- `jilid-2.html`  : bab 13-21
- `lampiran.html` : lampiran A-G (tanpa nomor)

Aturan transformasi:
- Unit potongan adalah `<h1>` sintetis mdBook, satu per file sumber, urut
  sesuai `src/SUMMARY.md` (jumlah keduanya harus sama; diverifikasi).
- Bab `title-page.md` dibuang (halaman judul dibuat sendiri oleh templat).
- Sub-bab (entri SUMMARY berindentasi): `<h1>` sintetisnya duplikat judul
  yang juga muncul sebagai `<h2>` pertama dari sumber, jadi dibuang;
  `<h2>` dari sumber itulah yang menjadi judul seksi.
- Bab induk: `<h1>` dipertahankan (diberi nomor "Bab N" oleh Typst).
- Tautan pembungkus heading, anchor kosong, dan penanda page-break mdBook
  dibersihkan di sini.
"""

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
BUILD = os.path.join(ROOT, "cetak", "build")

# File pertama Jilid 2; semua entri mulai dari sini masuk jilid 2.
BATAS_JILID = "ch13-00-functional-features"


def entri_summary():
    """Kembalikan [(id_file, judul, parent)] urut dari src/SUMMARY.md.

    `parent` bernilai True bila baris SUMMARY tidak berindentasi (bab, bab
    induk, atau entri depan); entri berindentasi adalah sub-bab/anak.
    """
    entri = []
    for baris in open(os.path.join(SRC, "SUMMARY.md"), encoding="utf-8"):
        m = re.match(r"^(?P<indent>\s*)-?\s*\[(.*?)\]\(([^)]+\.md)\)", baris)
        if m:
            path = m.group(3).replace("\\", "/")
            entri.append(
                (path.rsplit("/", 1)[-1][:-3], m.group(2), m.group("indent") == "")
            )
    return entri


def bersihkan(html: str) -> str:
    # Penanda page-break mdBook antar-bab; page break diatur ulang di Typst.
    html = re.sub(
        r'<div style="break-before: page; page-break-before: always;"></div>',
        "",
        html,
    )
    # Buka pembungkus tautan heading: <hN id="x"><a class="header" ...>T</a></hN>
    html = re.sub(
        r'(<h([1-6])[^>]*>)<a class="header" href="[^"]*">(.*?)</a></h\2>',
        r"\1\3</h\2>",
        html,
    )
    # Anchor kosong (penanda posisi, tidak bermakna di buku cetak).
    html = re.sub(r'<a id="[^"]+"></a>', "", html)
    # Tautan di dalam caption listing -> teks polos.
    html = re.sub(r'(<figcaption[^>]*>)<a href="[^"]+">(.*?)</a>', r"\1\2", html)
    return html


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--satu",
        metavar="ID",
        help="hanya ekstrak satu file bab (mode dev pratinjau), "
        "mis. ch04-01-what-is-ownership",
    )
    args = ap.parse_args()

    try:
        print_html = open(os.path.join(ROOT, "book", "print.html"), encoding="utf-8").read()
    except OSError:
        sys.exit("book/print.html tidak ada; jalankan `mdbook build` dulu.")
    m = re.search(r"<main>(.*?)</main>", print_html, re.S)
    if not m:
        sys.exit("print.html tidak memiliki <main>.")
    inner = bersihkan(m.group(1))

    awal = [mm.start() for mm in re.finditer(r"<h1", inner)]
    batas = awal[1:] + [len(inner)]
    blok = [inner[a:b] for a, b in zip(awal, batas)]

    entri = entri_summary()
    if len(blok) != len(entri):
        sys.exit(
            f"jumlah <h1> di print.html ({len(blok)}) tidak sama dengan "
            f"entri SUMMARY.md ({len(entri)}); periksa SUMMARY.md."
        )

    depan, isi1, isi2, lampiran = [], [], [], []
    idx_batas = next(
        i for i, (idf, _, _) in enumerate(entri) if idf == BATAS_JILID
    )
    for i, ((idf, _judul, parent), b) in enumerate(zip(entri, blok)):
        if args.satu and idf != args.satu:
            continue
        if idf == "title-page":
            continue  # halaman judul dibuat oleh templat
        if not parent:
            # Buang <h1> sintetis yang duplikat judul <h2> pertama sumber.
            b = re.sub(r"^\s*<h1.*?</h1>\s*", "", b, count=1, flags=re.S)
        if idf == "foreword" or idf.startswith("ch00"):
            depan.append(b)
        elif idf.startswith("appendix"):
            lampiran.append(b)
        elif i >= idx_batas:
            isi2.append(b)
        else:
            isi1.append(b)

    os.makedirs(BUILD, exist_ok=True)
    if args.satu:
        dengan = [p for p in depan + isi1 + isi2 + lampiran]
        if not dengan:
            sys.exit(f"id '{args.satu}' tidak ditemukan di SUMMARY.md")
        with open(os.path.join(BUILD, "bab-dev.html"), "w", encoding="utf-8") as f:
            f.write("\n".join(dengan))
        print(f"tulis cetak/build/bab-dev.html")
        return

    for nama, potongan in (
        ("depan.html", depan),
        ("jilid-1.html", isi1),
        ("jilid-2.html", isi2),
        ("lampiran.html", lampiran),
    ):
        with open(os.path.join(BUILD, nama), "w", encoding="utf-8") as f:
            f.write("\n".join(potongan))
        print(f"tulis cetak/build/{nama}: {len(potongan)} bab")


if __name__ == "__main__":
    main()
