#!/usr/bin/env python3
"""Pengecek struktur terjemahan Rust Book.

Membandingkan file di asli/ (Inggris) dengan src/ (terjemahan):
  - urutan dan tingkat heading
  - jumlah, penanda info, dan isi blok kode
  - direktif {{#include ...}} dan sejenisnya
  - target tautan
  - rasio jumlah kata (untuk mendeteksi bagian yang terlewat)

Pemakaian:
  python3 cek_terjemahan.py                    # cek semua file
  python3 cek_terjemahan.py ch04-01-what-is-ownership.md
  python3 cek_terjemahan.py --longgar          # abaikan komentar // di kode

Kode keluar 0 jika bersih, 1 jika ada galat.
"""
import argparse
import re
import sys
from pathlib import Path

FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^(#{1,6})\s+\S")
DIREKTIF = re.compile(r"\{\{#[^}]*\}\}")
TAUTAN = re.compile(r"\]\(([^)\s]+)")
KATA = re.compile(r"\w+", re.UNICODE)

RASIO_MIN, RASIO_MAX = 0.85, 1.60


def pisah(teks):
    """Pisahkan teks menjadi baris prosa dan daftar blok kode (info, isi)."""
    prosa, blok = [], []
    di_kode, pagar, info, buf = False, "", "", []
    for baris in teks.splitlines():
        m = FENCE.match(baris)
        if not di_kode and m:
            di_kode, pagar, info, buf = True, m.group(1), m.group(2).strip(), []
            continue
        if di_kode and m and m.group(1).startswith(pagar[0] * len(pagar)) \
                and m.group(2).strip() == "":
            blok.append((info, "\n".join(buf)))
            di_kode = False
            continue
        (buf if di_kode else prosa).append(baris)
    return prosa, blok


def tanpa_komentar(kode):
    hasil = []
    for baris in kode.splitlines():
        baris = re.sub(r"//.*$", "", baris).rstrip()
        if baris.strip():
            hasil.append(baris)
    return "\n".join(hasil)


def analisis(teks):
    prosa, blok = pisah(teks)
    heading = [len(HEADING.match(b).group(1)) for b in prosa if HEADING.match(b)]
    teks_prosa = "\n".join(prosa)
    return {
        "heading": heading,
        "blok": blok,
        "direktif": DIREKTIF.findall(teks),
        "tautan": TAUTAN.findall(teks_prosa),
        "kata": len(KATA.findall(DIREKTIF.sub("", TAUTAN.sub("", teks_prosa)))),
    }


def bandingkan(asli, terj, longgar):
    galat, peringatan = [], []

    if asli["heading"] != terj["heading"]:
        galat.append(
            f"Heading berbeda: asli {len(asli['heading'])} "
            f"({asli['heading']}), terjemahan {len(terj['heading'])} "
            f"({terj['heading']})"
        )

    if len(asli["blok"]) != len(terj["blok"]):
        galat.append(
            f"Jumlah blok kode berbeda: asli {len(asli['blok'])}, "
            f"terjemahan {len(terj['blok'])}"
        )
    else:
        for i, ((ia, ka), (it, kt)) in enumerate(zip(asli["blok"], terj["blok"]), 1):
            if ia != it:
                galat.append(f"Blok kode #{i}: penanda info berubah ('{ia}' -> '{it}')")
            if longgar:
                ka, kt = tanpa_komentar(ka), tanpa_komentar(kt)
            if ka != kt:
                galat.append(f"Blok kode #{i}: isi berubah")

    if asli["direktif"] != terj["direktif"]:
        galat.append(
            f"Direktif {{{{#...}}}} berbeda: asli {len(asli['direktif'])}, "
            f"terjemahan {len(terj['direktif'])}"
        )

    if asli["tautan"] != terj["tautan"]:
        galat.append(
            f"Target tautan berbeda: asli {len(asli['tautan'])}, "
            f"terjemahan {len(terj['tautan'])}"
        )

    if asli["kata"] > 0:
        rasio = terj["kata"] / asli["kata"]
        if rasio < RASIO_MIN:
            galat.append(
                f"Terjemahan terlalu pendek (rasio kata {rasio:.2f}); "
                f"kemungkinan ada bagian terlewat atau diringkas"
            )
        elif rasio > RASIO_MAX:
            peringatan.append(
                f"Terjemahan jauh lebih panjang (rasio kata {rasio:.2f}); "
                f"periksa apakah ada tambahan yang tidak perlu"
            )
    return galat, peringatan


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="*", help="nama file relatif terhadap src/ (opsional)")
    ap.add_argument("--asli", default="asli", help="folder sumber Inggris (default: asli)")
    ap.add_argument("--src", default="src", help="folder terjemahan (default: src)")
    ap.add_argument("--longgar", action="store_true",
                    help="abaikan komentar // di dalam blok kode")
    args = ap.parse_args()

    asli_dir, src_dir = Path(args.asli), Path(args.src)
    if not asli_dir.is_dir() or not src_dir.is_dir():
        sys.exit(f"Folder tidak ditemukan: {asli_dir} atau {src_dir}")

    if args.file:
        daftar = [Path(f) for f in args.file]
    else:
        daftar = sorted(p.relative_to(asli_dir) for p in asli_dir.rglob("*.md"))

    total_galat = 0
    for rel in daftar:
        pa, ps = asli_dir / rel, src_dir / rel
        if not pa.exists():
            print(f"[LEWAT] {rel}: tidak ada di {asli_dir}/")
            continue
        if not ps.exists():
            print(f"[GALAT] {rel}: file terjemahan tidak ada")
            total_galat += 1
            continue

        ta, ts = pa.read_text(encoding="utf-8"), ps.read_text(encoding="utf-8")
        if ta == ts:
            print(f"[BELUM] {rel}: identik dengan aslinya (belum diterjemahkan)")
            continue

        galat, peringatan = bandingkan(analisis(ta), analisis(ts), args.longgar)
        if galat:
            total_galat += len(galat)
            print(f"[GALAT] {rel}")
            for g in galat:
                print(f"    - {g}")
        else:
            print(f"[OK]    {rel}")
        for w in peringatan:
            print(f"    ! {w}")

    print()
    if total_galat:
        print(f"Selesai: {total_galat} galat ditemukan.")
        sys.exit(1)
    print("Selesai: tidak ada galat.")


if __name__ == "__main__":
    main()
