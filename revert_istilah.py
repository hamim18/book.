#!/usr/bin/env python3
"""revert_istilah.py — mengembalikan istilah glosarium ke bahasa Inggris di src/.

Pemakaian:
    python3 revert_istilah.py --dry <group>   # hitung saja
    python3 revert_istilah.py <group>         # terapkan

Group: error, tipe, dasar, oop, memory, misc
Aturan: hanya prosa yang diubah (blok kode dan inline code dilindungi);
padanan dalam kurung setelah istilah miring dilindungi dari penggantian.
"""
import re
import sys
from pathlib import Path

SRC = Path("src")

# --------------------------------------------------------------------------
# Bantuan
# --------------------------------------------------------------------------

def b(word: str) -> str:
    """Regex kata utuh (word boundary), di-escape."""
    return r"\b" + re.escape(word) + r"\b"


def kap(phrase: str) -> str:
    """Varian kapital di awal (untuk heading/awal kalimat)."""
    return phrase[0].upper() + phrase[1:]


def buat_rules(pasangan, kapital=True):
    """pasangan: list (indonesia, inggris). Hasilkan rules kata utuh,
    plus varian kapital bila diminta. Frasa didahulukan otomatis oleh
    pemanggil (urutkan sendiri di group)."""
    rules = []
    for indo, eng in pasangan:
        rules.append((b(indo), eng))
        if kapital:
            rules.append((b(kap(indo)), kap(eng)))
    return rules


# --------------------------------------------------------------------------
# Kelompok aturan — urutan penting: frasa dulu, lalu kata tunggal
# --------------------------------------------------------------------------

GROUPS: dict[str, list[tuple[str, str]]] = {}

GROUPS["error"] = [
    ("galatnya", "errornya"),
    ("galat kompilator", "error kompilator"),
] + buat_rules([("galat", "error")])

GROUPS["tipe"] = [
    ("inferensi tipe", "type inference"),
    ("anotasi tipe", "type annotation"),
    ("tipe data", "data type"),
    ("tipe majemuk", "compound type"),
    ("tipe primitif", "primitive type"),
    ("tipe kembalian", "return type"),
    ("alias tipe", "type alias"),
    ("sinonim tipe", "type synonym"),
    ("teori tipe", "type theory"),
    ("parameter tipe", "type parameter"),
    ("bertipe statis", "statically typed"),
    ("bertipe dinamis", "dynamically typed"),
    ("bertipe", "typed"),
    ("tipenya", "typenya"),
    # frasa padanan yang juga muncul mandiri (asli & bentuk pasca-revert)
    ("sistem typenya", "type systemnya"),
    ("sistem type", "type system"),
    ("sistem tipe", "type system"),
    ("tipe berukuran dinamis", "dynamically sized type"),
    ("tipe yang tidak berukuran", "unsized type"),
    ("tipe yang berukuran", "sized type"),
    ("tipe asosiasi", "associated type"),
    ("type asosiasi", "associated type"),
    ("tipe generik", "generic type"),
    ("type generik", "generic type"),
    ("tipe kustom", "custom type"),
    ("type kustom", "custom type"),
    ("tipe angka", "numeric type"),
    ("type angka", "numeric type"),
    ("pengetikan bebek", "duck typing"),
] + buat_rules([("tipe", "type")])

GROUPS["dasar"] = [
    ("pembangkit angka acak", "random number generator"),
    ("variabel lingkungan", "environment variable"),
    ("variabel konfigurasi", "configuration variable"),
    ("nilai kembalian", "return value"),
    ("perulangan tak berujung", "infinite loop"),
    ("label perulangan", "loop label"),
    ("alur kontrol", "control flow"),
    ("bahasa tingkat rendah", "low-level language"),
    ("titik mengambang", "floating point"),
    ("masukan/keluaran", "input/output"),
    ("masukan standar", "standard input"),
    ("keluaran standar", "standard output"),
    ("masukan pengguna", "user input"),
    ("spasi lebar nol", "zero-width space"),
    ("variabelnya", "variablenya"),
    ("perulangannya", "loopnya"),
    ("masukannya", "inputnya"),
    ("keluarannya", "outputnya"),
    ("ekspresinya", "expressionnya"),
    ("konstantanya", "constantnya"),
] + buat_rules([
    ("variabel", "variable"),
    ("konstanta", "constant"),
    ("pernyataan", "statement"),
    ("ekspresi", "expression"),
    ("perulangan", "loop"),
    ("masukan", "input"),
    ("keluaran", "output"),
])

GROUPS["oop"] = [
    ("pola newtype", "newtype pattern"),
    ("pola state", "state pattern"),
    ("metodenya", "methodnya"),
    ("polanya", "patternnya"),
    ("vektornya", "vectornya"),
    ("koleksinya", "collectionnya"),
] + buat_rules([
    ("metode", "method"),
    ("koleksi", "collection"),
    ("pola", "pattern"),
    ("vektor", "vector"),
])

# Kelompok memory memakai istilah miring; padanan dilindungi lewat PROTECT_MEMORY.
GROUPS["memory"] = [
    ("pointer menggantung", "*dangling pointer*"),
    ("reference menggantung", "*dangling reference*"),
    ("salinan dangkal", "*shallow copy*"),
    ("salinan dalam", "*deep copy*"),
    ("perilaku tak terdefinisi", "*undefined behavior*"),
    ("kebocoran memori", "*memory leak*"),
    ("memori bersama", "*shared memory*"),
    ("pengalokasi memori", "*memory allocator*"),
    ("masa hidup", "*lifetime*"),
    ("tanda tangan", "*signature*"),
    ("tidak dapat diubah", "*immutable*"),
    ("dapat diubah", "*mutable*"),
    ("pemiliknya", "*owner*nya"),
    ("kepemilikannya", "*ownership*nya"),
    ("referensinya", "*reference*nya"),
    ("kompilatornya", "*compiler*nya"),
] + buat_rules([
    ("kompilator", "*compiler*"),
    ("kepemilikan", "*ownership*"),
    ("pemilik", "*owner*"),
    ("peminjaman", "*borrowing*"),
    ("referensi", "*reference*"),
    ("pemindahan", "*move*"),
    ("penunjuk", "*pointer*"),
    ("alokasi", "*allocation*"),
    ("pengalokasi", "*allocator*"),
    ("tumpukan", "*stack*"),
    ("timbunan", "*heap*"),
    ("menggantung", "*dangling*"),
    ("penetapan", "assignment"),
    ("salinan", "copy"),
]) + [
    # cakupan: *scope* kecuali bab 11 (coverage) — ditangani lewat filter file
    (b("cakupan"), "*scope*"),
    (b("Cakupan"), "*Scope*"),
]

GROUPS["misc"] = [
    ("pengelola dependensi", "dependency manager"),
    ("sistem kontrol versi", "version control system"),
    ("pustaka standar", "standard library"),
    ("baris perintah", "command line"),
    ("file sumber", "source file"),
    ("keamanan memori", "memory safety"),
    ("ruang nama", "namespace"),
    ("pengiriman pesan", "message passing"),
    ("pengguna akhir", "end user"),
    ("pembelajaran mesin", "machine learning"),
    ("peramban web", "web browser"),
    ("server web", "web server"),
    ("denda performa", "performance penalty"),
    ("pemrograman fungsional", "functional programming"),
    ("pemrograman berorientasi objek", "object-oriented programming"),
    ("pemrograman sistem tingkat rendah", "low-level systems programming"),
    ("pemrograman konkuren", "concurrent programming"),
    ("pemrograman paralel", "parallel programming"),
    ("pemrograman asinkron", "asynchronous programming"),
    ("multitasking kooperatif", "cooperative multitasking"),
    ("pengembangan yang digerakkan oleh pengujian", "test-driven development"),
    ("pengembangan yang digerakkan oleh kompilator", "compiler-driven development"),
    ("keadaan internal", "internal state"),
    ("keadaan yang buruk", "bad state"),
    ("keadaan mutable", "mutable state"),
    ("state bersama", "shared state"),
    ("pemisahan tanggung jawab", "separation of concerns"),
    ("alur kerja", "workflow"),
    ("akhir masa pakai", "end of life"),
    ("pengujian unit", "unit test"),
    ("pengujian integrasi", "integration test"),
    ("pengujiannya", "testnya"),
    ("dependensinya", "dependencynya"),
] + buat_rules([
    ("pemrogram", "programmer"),
    ("dependensi", "dependency"),
    ("konkurensi", "concurrency"),
    ("konkuren", "concurrent"),
    ("asinkron", "asynchronous"),
    ("pengujian", "test"),
    ("pemrosesan", "processing"),
    ("penyaringan", "filtering"),
    ("luring", "offline"),
    ("alat", "tool"),
])

# Pola padanan yang harus dilindungi (tetap Indonesia), per group.
# Bentuk: (regex_find, ) — teks yang cocok dibungkus sentinel lalu dipulihkan.
PROTECT: dict[str, list[str]] = {
    "tipe": [r"\*[^*]+\* \([^()]*tipe[^()]*\)"],
    "memory": [
        r"\*compiler\* \([^()]*kompilator[^()]*\)",
        r"\*ownership\* \([^()]*kepemilikan[^()]*\)",
        r"\*owner\* \([^()]*pemilik[^()]*\)",
        r"\*borrowing\* \([^()]*peminjaman[^()]*\)",
        r"\*reference\* \([^()]*referensi[^()]*\)",
        r"\*lifetime\* \([^()]*masa hidup[^()]*\)",
        r"\*move\* \([^()]*pemindahan[^()]*\)",
        r"\*scope\* \([^()]*cakupan[^()]*\)",
        r"\*mutable\* \([^()]*dapat diubah[^()]*\)",
        r"\*immutable\* \([^()]*tidak dapat diubah[^()]*\)",
        r"\*pointer\* \([^()]*penunjuk[^()]*\)",
        r"\*allocation\* \([^()]*alokasi[^()]*\)",
        r"\*stack\* \([^()]*tumpukan[^()]*\)",
        r"\*heap\* \([^()]*timbunan[^()]*\)",
        r"\*signature\* \([^()]*tanda tangan[^()]*\)",
        r"\*dangling pointer\* \([^()]*pointer menggantung[^()]*\)",
        r"\*dangling reference\* \([^()]*reference menggantung[^()]*\)",
        r"\*memory leak\* \([^()]*kebocoran memori[^()]*\)",
        r"\*floating point\* \([^()]*titik mengambang[^()]*\)",
        r"coverage \([^()]*cakupan[^()]*\)",
    ],
    "misc": [
        r"\*shared-state\* \([^()]*state bersama[^()]*\)",
        r"\*release channel\* \([^()]*saluran rilis[^()]*\)",
    ],
}

# Rule tertentu hanya berlaku di file tertentu.
# cakupan di bab 11 = coverage (polos), bukan scope.
FILE_RULES: dict[str, list[tuple[str, str, callable]]] = {
    "memory": [
        (b("cakupan"), "coverage", lambda f: f.name.startswith("ch11-")),
        (b("Cakupan"), "Coverage", lambda f: f.name.startswith("ch11-")),
    ],
}

# --------------------------------------------------------------------------
# Mesin
# --------------------------------------------------------------------------

def proses(teks: str, rules, protect: list[str], file_rules) -> tuple[str, dict]:
    n = 0
    hitung = {}
    # 1) lindungi blok kode berfence
    potong = re.split(r"(```.*?```)", teks, flags=re.DOTALL)
    for i in range(0, len(potong), 2):
        potong[i] = _proses_prosa(potong[i], rules, protect, file_rules, hitung)
    return "".join(potong), hitung


def _proses_prosa(prosa: str, rules, protect, file_rules, hitung) -> str:
    # lindungi inline code
    inline = re.findall(r"`[^`]*`", prosa)
    for j, kode in enumerate(inline):
        prosa = prosa.replace(kode, f"\x00I{j}\x00", 1)

    # lindungi padanan
    sentinel = {}
    if protect:
        for pat in protect:
            for m in list(re.finditer(pat, prosa)):
                kunci = f"\x00P{len(sentinel)}\x00"
                sentinel[kunci] = m.group(0)
                prosa = prosa.replace(m.group(0), kunci, 1)

    def terapkan(aturan, filt=None):
        nonlocal prosa
        for pat, repl in aturan:
            if filt is not None and not filt(None):
                pass
            cnt = prosa.count(pat) if False else 0
            prosa2, nsub = re.subn(pat, repl, prosa)
            if nsub:
                hitung[repl] = hitung.get(repl, 0) + nsub
                prosa = prosa2

    # aturan spesifik-file dulu (mis. cakupan bab 11)
    for pat, repl, filt in file_rules:
        prosa2, nsub = re.subn(pat, repl, prosa)
        if nsub:
            hitung[f"{repl} [{filt.__name__}]"] = hitung.get(repl, 0) + nsub
            prosa = prosa2

    terapkan(rules)

    # pulihkan padanan lalu inline code
    for kunci, asli in sentinel.items():
        prosa = prosa.replace(kunci, asli)
    for j, kode in enumerate(inline):
        prosa = prosa.replace(f"\x00I{j}\x00", kode, 1)
    return prosa


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    dry = "--dry" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--dry"]
    group = args[0]
    if group not in GROUPS:
        sys.exit(f"group tak dikenal: {group}")

    files = sorted(SRC.glob("*.md"))
    total = {}
    for f in files:
        teks = f.read_text()
        baru, hitung = proses(teks, GROUPS[group], PROTECT.get(group, []),
                              FILE_RULES.get(group, []))
        if baru != teks:
            if not dry:
                f.write_text(baru)
            print(f"{f.name}: {sum(hitung.values())} pergantian")
        for k, v in hitung.items():
            total[k] = total.get(k, 0) + v
    print("\nTotal per aturan:")
    for k, v in sorted(total.items(), key=lambda x: -x[1]):
        print(f"  {v:5d}  {k}")
    print(f"\n{'DRY RUN' if dry else 'SELESAI'} — {sum(total.values())} pergantian")


if __name__ == "__main__":
    main()
