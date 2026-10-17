#!/usr/bin/env python3
"""buat-materi.py — pembangkit materi belakang buku cetak (poin 3).

Sub-perintah:
  glosarium     : merangkai glosarium Inggris–Indonesia dari tabel glosarium
                  CLAUDE.md + log istilah ROADMAP.md + pemetaan revert
                  (revert_istilah.py) → cetak/build/glosarium.md
  indeks-scan   : memindai fragmen .typ (build/) untuk kemunculan istilah
                  glosarium → cetak/build/indeks-scan.json
  indeks-rakit  : menggabungkan hasil scan + peta heading→halaman
                  (cetak/build/halaman-{1,2}.json, dihasilkan typst eval)
                  → cetak/build/indeks.typ

Urutan dalam konversi.sh: glosarium → pandoc → compile pass 1 → typst eval
(halaman-*.json) → indeks-scan → indeks-rakit → compile pass 2.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CETAK = os.path.join(ROOT, "cetak")
BUILD = os.path.join(CETAK, "build")
MATERI = os.path.join(CETAK, "materi")
sys.path.insert(0, ROOT)


# ---------------------------------------------------------------------------
# Glosarium: kumpulkan pasangan Inggris → Indonesia
# ---------------------------------------------------------------------------

def baca_tabel_claude():
    """Tabel glosarium CLAUDE.md: | Inggris | Penulisan |."""
    hasil = []
    dalam = False
    for baris in open(os.path.join(ROOT, "CLAUDE.md"), encoding="utf-8"):
        if baris.startswith("| Inggris | Penulisan |"):
            dalam = True
            continue
        if not dalam or not baris.startswith("|"):
            if dalam:
                break
            continue
        sel = [s.strip() for s in baris.strip("|\n").split("|")]
        if len(sel) < 2 or not sel[0]:
            continue
        eng, tulis = sel[0], sel[1]
        if eng.startswith(":"):
            continue
        hasil.append((bersih_eng(eng), padanan_dari(tulis)))
    return hasil


def padanan_dari(tulis: str):
    """Ambil padanan dari kolom 'Penulisan' CLAUDE.md.

    "*ownership* (kepemilikan)" → "kepemilikan"; "(tetap)" → None;
    "error (polos) / penanganan error" → bagian-bagiannya dipisah pemanggil.
    """
    if tulis in ("", "—"):
        return None
    m = re.search(r"\(([^)]+)\)", tulis)
    if m:
        dalam = m.group(1)
        if re.match(r"^(tetap|polos|tanpa miring|miring)", dalam):
            return None
        return dalam
    return None


def baca_log_roadmap():
    """Tabel 'Log keputusan istilah' ROADMAP.md: | Istilah | Padanan | Bab |."""
    hasil = []
    dalam = False
    for baris in open(os.path.join(ROOT, "ROADMAP.md"), encoding="utf-8"):
        if baris.startswith("| Istilah | Padanan | Bab |"):
            dalam = True
            continue
        if not dalam or not baris.startswith("|"):
            if dalam:
                break
            continue
        sel = [s.strip() for s in baris.strip("|\n").split("|")]
        if len(sel) < 2 or not sel[0]:
            continue
        istilah, padanan = sel[0], sel[1]
        if re.fullmatch(r"[\w -]+", istilah) and not re.search(r"[a-z]{3}", istilah):
            continue  # kolom Istilah berbahasa Indonesia; arahnya ditangani revert
        if not re.search(r"[A-Za-z]", istilah):
            continue
        padanan = padanan_log(padanan)
        hasil.append((bersih_eng(istilah), padanan))
    return hasil


def padanan_log(padanan: str):
    """Padanan dari tabel log: ambil isi kurung bila ada; buang penanda."""
    padanan = padanan.strip()
    m = re.search(r"\(([^)]+)\)", padanan)
    if m and not re.match(
        r"^(tetap|tanpa miring|polos|miring|verba|nomina|nama)", m.group(1)
    ):
        padanan = m.group(1)
    else:
        padanan = re.sub(r"\*", "", padanan)
    padanan = padanan.strip()
    return None if padanan in ("", "tetap") else padanan


def baca_revert():
    """Pemetaan revert_istilah.py: (indonesia, inggris) → pasangan Inggris–Indonesia."""
    import revert_istilah

    indo = set()
    for aturan in revert_istilah.GROUPS.values():
        for lama, baru in aturan:
            indo.add(lama.lower())
    hasil = []
    for aturan in revert_istilah.GROUPS.values():
        for lama, baru in aturan:
            eng = baru
            # buang pasangan majemuk yang memuat kata Indonesia / akhiran -nya
            kata = [w for w in re.sub(r"[*_]", "", eng).split() if w]
            if any(k.lower() in indo or k.lower().endswith("nya") for k in kata):
                continue
            hasil.append((bersih_eng(eng), lama))
    return hasil


def bersih_eng(eng: str):
    """Bersihkan markup di sisi Inggris (tabel tetap menyimpan *miring*)."""
    return re.sub(r"\s+", " ", eng).strip()


def pasangan_unik(pasangan):
    kunci = {}
    for eng, indo in pasangan:
        polos = re.sub(r"[*_`]", "", eng).lower()
        if not polos or polos in ("tetap",):
            continue
        if polos not in kunci:
            # padanan sama dengan istilahnya → tak bermakna, tampilkan "—"
            if indo is not None and re.sub(r"[*_`]", "", indo).lower() == polos:
                indo = None
            kunci[polos] = (eng, indo)
    return [kunci[k] for k in sorted(kunci)]


def tulis_glosarium():
    pasangan = pasangan_unik(
        baca_tabel_claude() + baca_log_roadmap() + baca_revert()
    )
    # Tulis langsung .typ (bukan .md → pandoc): pandoc membungkus tabel
    # dalam #figure yang tidak bisa dipecah lintas halaman, sehingga tabel
    # sepanjang ini rusak. Sel konten dibungkus [...] dengan isi yang
    # di-escape secukupnya (tidak ada ] atau \ di istilah glosarium).
    sel = lambda s: "[" + str(s).replace("\\", "\\\\").replace("]", r"\]") + "]"
    baris = [
        '#import "../template.typ": catatan',
        "= Glosarium Inggris–Indonesia",
        "<glosarium-inggris-indonesia>",
        "",
        "Daftar berikut memuat istilah teknis yang dipakai dalam buku ini "
        "beserta padanan bahasa Indonesianya. Istilah yang dicetak miring "
        "ditulis miring pula di dalam prosa buku; istilah polos ditulis "
        "polos. Tanda — berarti istilah itu dipertahankan apa adanya tanpa "
        "padanan.",
        "",
        "#table(",
        "  columns: (1fr, 1fr),",
        "  inset: (x: 4pt, y: 3pt),",
        "  table.header(" + sel("Istilah Inggris") + ", "
        + sel("Padanan Indonesia") + ",),",
        "  table.hline(),",
    ]
    for eng, indo in pasangan:
        polos = re.sub(r"[*_`]", "", eng)
        if polos == "---" or "<span" in polos or polos.startswith('"'):
            continue
        indo_t = "—" if indo is None else indo
        baris.append("  " + sel(eng) + ", " + sel(indo_t) + ",")
    baris.append(")")
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, "glosarium.typ"), "w", encoding="utf-8") as f:
        f.write("\n".join(baris) + "\n")
    print(f"tulis cetak/build/glosarium.typ: {len(pasangan)} entri")


# ---------------------------------------------------------------------------
# Indeks: pindai fragmen .typ, lalu rakit dengan peta halaman
# ---------------------------------------------------------------------------

# Urutan fragmen per jilid dalam dokumen cetak (setelah template.typ).
# isi_nama: nama file di cetak/build; dipindai_istilah: kemunculan istilah
# di dalamnya ikut diindeks. "DAFTAR-ISI" adalah heading sintetis #outline.
FRAGMEN = [
    ("J1", "hak-cipta", False),
    ("J1", "kata-pengantar-penerjemah", True),
    ("J1", "foreword", True),
    ("J1", "panduan-membaca", True),
    ("J1", "DAFTAR-ISI", False),
    ("J1", "pendahuluan", True),
    ("J1", "jilid-1", True),
    ("J2", "DAFTAR-ISI", False),
    ("J2", "jilid-2", True),
    ("J2", "lampiran", True),
    ("J2", "glosarium", False),
    ("J2", "referensi", False),
    ("J2", "indeks", False),
    ("J2", "profil", False),
    ("J2", "info-edisi", False),
]


def bersih_teks(s: str) -> str:
    s = re.sub(r"#emph\[", "", s)
    s = s.replace("]", "")
    return re.sub(r"[*_`]", "", s)


def istilah_glosarium():
    pasangan = pasangan_unik(
        baca_tabel_claude() + baca_log_roadmap() + baca_revert()
    )
    istilah = set()
    for eng, _ in pasangan:
        polos = re.sub(r"[*_`]", "", eng).strip()
        if 2 <= len(polos) <= 40 and re.search(r"[A-Za-z]", polos):
            istilah.add(polos)
    return sorted(istilah, key=str.lower)


def pindai():
    istilah = istilah_glosarium()
    pola = {t: re.compile(r"\b" + re.escape(t) + r"\b", re.IGNORECASE) for t in istilah}

    heading_per_jilid = {"J1": [], "J2": []}   # [(level, teks)] urut dokumen
    temuan = {t: [] for t in istilah}          # istilah → [(jilid, idx_heading)]
    dalam_kode = False

    for jilid, nama, dipindai in FRAGMEN:
        if nama == "DAFTAR-ISI":
            heading_per_jilid[jilid].append((1, "Daftar Isi"))
            continue
        path = os.path.join(BUILD, nama + ".typ")
        if not os.path.exists(path):
            print(f"LEWAT (tidak ada): {path}")
            continue
        idx_h1 = idx_h2 = idx_h3 = None
        for baris in open(path, encoding="utf-8"):
            if baris.startswith("```"):
                dalam_kode = not dalam_kode
                continue
            m = re.match(r"^(=+)\s+(.+?)\s*$", baris)
            if m and not dalam_kode:
                tingkat = len(m.group(1))
                teks = bersih_teks(m.group(2))
                i = len(heading_per_jilid[jilid])
                heading_per_jilid[jilid].append((tingkat, teks))
                if tingkat == 1:
                    idx_h1 = i
                    idx_h2 = idx_h3 = None
                elif tingkat == 2:
                    idx_h2 = i
                    idx_h3 = None
                elif tingkat == 3:
                    idx_h3 = i
                continue  # heading sendiri bukan lokasi kemunculan
            if dalam_kode or not dipindai:
                continue
            baris_b = bersih_teks(baris)
            for t, pat in pola.items():
                if pat.search(baris_b):
                    tujuan = idx_h3 if idx_h3 is not None else (idx_h2 if idx_h2 is not None else idx_h1)
                    if tujuan is None:
                        continue
                    entri = (jilid, tujuan)
                    if entri not in temuan[t]:
                        temuan[t].append(entri)

    with open(os.path.join(BUILD, "indeks-scan.json"), "w", encoding="utf-8") as f:
        json.dump(
            {"heading": heading_per_jilid, "temuan": temuan},
            f, ensure_ascii=False, indent=1,
        )
    ada = sum(1 for v in temuan.values() if v)
    print(f"tulis cetak/build/indeks-scan.json: {len(temuan)} istilah, {ada} ditemukan")


def muat_halaman(jilid: str):
    path = os.path.join(BUILD, f"halaman-{1 if jilid == 'J1' else 2}.json")
    with open(path, encoding="utf-8") as f:
        mentah = json.load(f)
    return [(e[0], e[2]) for e in mentah]  # [(level, halaman)]


def rakit():
    with open(os.path.join(BUILD, "indeks-scan.json"), encoding="utf-8") as f:
        data = json.load(f)
    heading_per_jilid = data["heading"]
    temuan = data["temuan"]

    halaman = {}
    for jilid in ("J1", "J2"):
        peta = muat_halaman(jilid)
        if len(peta) != len(heading_per_jilid[jilid]):
            sys.exit(
                f"jumlah heading {jilid} tidak cocok: peta {len(peta)} vs "
                f"pindai {len(heading_per_jilid[jilid])}; periksa urutan "
                f"fragmen di FRAGMEN buat-materi.py."
            )
        halaman[jilid] = peta

    entri = []
    for t in sorted(temuan, key=str.lower):
        lokasi = temuan[t]
        if not lokasi:
            continue
        bagian = []
        for jilid, idx in lokasi[:15]:
            tingkat, teks = heading_per_jilid[jilid][idx]
            hal = halaman[jilid][idx][1]
            teks_t = re.sub(r"<[^>]+>", "", teks)
            bagian.append(f"#emph[{teks_t}] ({jilid}·{hal})")
        baris = f"*{t}* — {'; '.join(bagian)}"
        if len(lokasi) > 15:
            baris += f"; +{len(lokasi) - 15} lokasi lain"
        entri.append(baris)

    with open(os.path.join(BUILD, "indeks.typ"), "w", encoding="utf-8") as f:
        f.write("= Indeks Istilah\n\n")
        f.write("<indeks-istilah>\n\n")
        f.write("#set text(size: 9.5pt)\n")
        f.write("#set par(justify: false, leading: 0.9em)\n\n")
        f.write(
            "Indeks ini memuat istilah teknis dari glosarium beserta halaman "
            "awal seksi yang membahasnya. Penanda J1/J2 menunjukkan jilid; "
            "angka menunjuk halaman di jilid tersebut.\n\n"
        )
        f.write("\n\n".join(entri) + "\n")
    print(f"tulis cetak/build/indeks.typ: {len(entri)} entri")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    perintah = sys.argv[1]
    if perintah == "glosarium":
        tulis_glosarium()
    elif perintah == "indeks-scan":
        pindai()
    elif perintah == "indeks-rakit":
        rakit()
    else:
        sys.exit(__doc__)
