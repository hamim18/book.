#!/usr/bin/env python3
"""Pemeriksaan tata letak jilid cetak secara terprogram.

Untuk tiap jilid: jumlah halaman (dari PDF), ukuran & halaman tiap gambar,
ukuran & halaman tiap blok kode, ukuran & halaman tiap tabel, serta halaman
tiap label caption. Dipakai untuk memastikan gambar tidak melebihi kolom
teks, blok kode tinggi pecah lintas halaman (bukan terpotong), dan caption
berada di halaman yang masuk akal.

Pemakaian: python3 cetak/periksa.py [jilid-1|jilid-2]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
CETAK = AKAR / "cetak"
FONT = str(CETAK / "fonts")
TEKS_TINGGI = 601.0  # pt: 250mm - margin atas 18mm - bawah 20mm
LEBAR_KOLOM = 394.0


def eval_typ(ekspr: str, masuk: Path) -> object:
    r = subprocess.run(
        ["typst", "eval", ekspr, f"--in={masuk}", f"--font-path={FONT}",
         f"--root={CETAK}", "--format=json"],
        cwd=AKAR, capture_output=True, text=True, timeout=600,
    )
    if r.returncode != 0:
        print(r.stderr[:900], file=sys.stderr)
        sys.exit("eval gagal")
    m = re.search(r"\[.*\]", r.stdout, re.S)
    if not m:
        print(r.stdout[:900], file=sys.stderr)
        sys.exit("keluaran eval tak terbaca")
    return json.loads(m.group(0))


def halaman_pdf(jilid: str) -> int:
    r = subprocess.run(
        ["grep", "-ao", "/Count [0-9]*",
         str(CETAK / "keluaran" / f"rust-book-id-{jilid}.pdf")],
        cwd=AKAR, capture_output=True, text=True,
    )
    angka = [int(x.split()[1]) for x in r.stdout.splitlines()
             if len(x.split()) > 1]
    return angka[0] if angka else -1


def periksa(jilid: str) -> dict:
    # Probe: jilid + blok metadata (measure butuh context, hanya tersedia
    # di dalam dokumen).
    probe = CETAK / "build" / f"probe-{jilid}.typ"
    probe.write_text(
        f'#include "/{jilid}.typ"\n'
        '#context [#metadata((cek: query(image).map(it => '
        '(it.fields().source, measure(it), it.location().page()))))]\n'
        '#context [#metadata((cek: query(raw.where(block: true)).map(it => '
        '(measure(it), it.location().page(), it.location().position().y))))]\n'
        '#context [#metadata((cek: query(table).map(t => '
        '(measure(t), t.location().page()))))]\n'
    )
    data = eval_typ(
        'query(metadata).filter(m => type(m.value) == dictionary and '
        '"cek" in m.value).map(m => m.value.cek)',
        probe,
    )
    img = [(p, float(s["width"][:-2]), float(s["height"][:-2]), h)
           for (p, s, h) in data[0]]
    blok = [(float(s["width"][:-2]), float(s["height"][:-2]), h, y)
            for (s, h, y) in data[1]]
    tab = [(float(s["width"][:-2]), float(s["height"][:-2]), h)
           for (s, h) in data[2]]

    # Halaman tiap label caption: satu eval untuk semua label.
    fragmen = ["foreword", "pendahuluan", jilid, "lampiran"]
    label = set()
    for f in fragmen:
        t = (CETAK / "build" / f"{f}.typ").read_text()
        label.update(re.findall(r"<cap-[a-z]+-[0-9A-Za-z-]+>", t))
    nama = sorted(l.strip("<>") for l in label)
    if nama:
        ekspr = "((" + ", ".join(
            f'"{n}", query(label("{n}")).at(0).location().page()' for n in nama
        ) + "))"
        cap = eval_typ(ekspr, CETAK / f"{jilid}.typ")
        cap = dict(zip(cap[::2], cap[1::2]))
    else:
        cap = {}

    return {"hal": halaman_pdf(jilid), "cap": cap, "img": img,
            "blok": blok, "tab": tab}


def main() -> None:
    for jilid in sys.argv[1:] or ("jilid-1", "jilid-2"):
        d = periksa(jilid)
        print(f"===== {jilid}: {d['hal']} halaman =====")
        # Gambar sampul (full-bleed, selebar halaman) dikecualikan dari
        # batas kolom teks.
        lebar_masalah = [g for g in d["img"]
                         if g[1] > LEBAR_KOLOM + 0.5
                         and "sampul" not in str(g[0])]
        print(f"gambar: {len(d['img'])} total; "
              f"{len(lebar_masalah)} melebihi kolom teks")
        for g in lebar_masalah:
            print(f"  !! {g[0]} {g[1]:.1f}pt hal {g[3]}")
        pecah = [b for b in d["blok"] if b[1] > TEKS_TINGGI]
        print(f"blok kode: {len(d['blok'])} total; "
              f"{len(pecah)} lebih tinggi dari 1 halaman (pecah lintas "
              f"halaman, bukan terpotong)")
        for b in pecah:
            print(f"  pecah: h={b[1]:.1f} mulai hal {b[2]}")
        t_pecah = [t for t in d["tab"] if t[1] > TEKS_TINGGI]
        print(f"tabel: {len(d['tab'])} total; {len(t_pecah)} pecah lintas "
              f"halaman")
        print(f"label caption: {len(d['cap'])}")


if __name__ == "__main__":
    main()
