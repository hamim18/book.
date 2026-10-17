# Panduan Prompt Bertahap: Menerjemahkan Rust Book dengan Claude Code

Tempel prompt di bawah ini ke Claude Code, **satu tahap per kali**.
Ganti bagian yang diapit `<...>` dengan nama file atau nomor bab yang sesuai.

Aturan umum:
- Jalankan `claude` dari akar repo (folder yang berisi `src/`, `asli/`, `CLAUDE.md`).
- Ketik `/clear` sebelum memulai file atau bab baru.
- Commit ke git setelah setiap tahap yang hasilnya sudah kamu periksa.

---

## Tahap 0: Cek kesiapan (sekali saja)

```
Baca CLAUDE.md. Jangan menerjemahkan apa pun dulu.
Jalankan `ls` dan `python3 cek_terjemahan.py | head -20`.
Lalu jelaskan dengan kata-katamu sendiri: (1) folder mana yang boleh diedit,
(2) lima aturan ketat yang paling penting, (3) bagaimana kamu menangani
istilah teknis saat pertama kali muncul di sebuah bab.
Laporkan juga jika ada yang tidak sesuai dengan struktur yang dijelaskan di CLAUDE.md.
```

**Periksa:** jawabannya cocok dengan `CLAUDE.md`. Jika meleset, perbaiki `CLAUDE.md` dulu.

---

## Tahap 1: Uji coba satu file pendek

Pilih file pendek dulu, misalnya `ch04-01-what-is-ownership.md` (sesuaikan nama persis di `src/`).

```
Terjemahkan src/<nama-file>.md sesuai CLAUDE.md.
Kerjakan per bagian heading, lalu tulis hasilnya ke file yang sama.
Setelah selesai, jalankan `python3 cek_terjemahan.py <nama-file>.md`
dan perbaiki sampai tidak ada galat.
Akhiri dengan laporan sesuai format di CLAUDE.md.
```

**Periksa sendiri:**
- Baca 2-3 paragraf konsep inti. Apakah natural dan benar secara teknis?
- `git diff` : pastikan hanya prosa yang berubah, bukan kode.
- Jika gaya kurang pas, **jangan lanjut**. Perbaiki aturan di `CLAUDE.md`, lalu `git checkout src/<nama-file>.md` dan ulangi.

---

## Tahap 2: Review kedua (pencari kesalahan makna)

Dalam sesi baru (`/clear`):

```
Tugasmu sekarang adalah reviewer, bukan penerjemah.
Bandingkan asli/<nama-file>.md dengan src/<nama-file>.md.
Cari dan daftarkan: (1) kalimat yang maknanya bergeser, (2) bagian yang
terlewat atau diringkas, (3) istilah yang tidak konsisten dengan glosarium
di CLAUDE.md, (4) kalimat yang terdengar seperti terjemahan mesin.
Untuk setiap temuan, tuliskan nomor baris, kutipan singkat, dan usulan perbaikan.
Jangan mengedit file dulu. Tunggu persetujuanku.
```

Setelah kamu menyetujui:

```
Terapkan perbaikan nomor <1, 3, 4> saja. Edit hanya baris yang bersangkutan,
lalu jalankan ulang cek_terjemahan.py.
```

---

## Tahap 3: Satu bab penuh

```
Terjemahkan seluruh file Bab <NN> satu per satu, urut sesuai src/SUMMARY.md:
<daftar nama file>.
Untuk setiap file: terjemahkan, jalankan cek_terjemahan.py, perbaiki galat.
Berhenti dan tanyakan padaku jika menemukan istilah baru yang belum ada
di glosarium. Jangan mulai bab berikutnya.
Di akhir, berikan satu laporan gabungan sesuai format di CLAUDE.md.
```

**Periksa:** baca laporan, setujui atau koreksi istilah baru, tambahkan ke glosarium `CLAUDE.md`, lalu commit:

```bash
git add -A && git commit -m "terjemah: bab <NN>"
```

---

## Tahap 4: Uji kompilasi kode

```
Jalankan `mdbook test`. Jika ada contoh kode yang gagal, tunjukkan file dan
penyebabnya. Bandingkan dengan asli/ untuk melihat apakah kodenya berubah.
Perbaiki hanya jika penyebabnya perubahan yang kita buat.
Jika penyebabnya lingkungan (versi Rust atau mdbook), jelaskan saja, jangan diubah.
```

---

## Tahap 5: Konsistensi istilah (setelah beberapa bab)

```
Telusuri src/ untuk istilah-istilah di glosarium CLAUDE.md. Cari variasi
penulisan yang tidak konsisten, misalnya "kepemilikan" dan "ownership" yang
dipakai bergantian tanpa pola, atau padanan Indonesia yang muncul berulang
setelah penyebutan pertama dalam bab yang sama.
Buat daftar temuan beserta nama file. Jangan mengedit dulu.
```

---

## Tahap 6: Bagian khusus

**Pendahuluan, kata pengantar, lampiran:**
```
Terjemahkan <nama-file>.md dengan aturan yang sama. Untuk bagian
ucapan terima kasih dan lisensi, pertahankan nama orang dan teks lisensi
persis seperti aslinya; terjemahkan hanya kalimat penjelasnya.
```

**Daftar isi:**
```
Terjemahkan judul bab di src/SUMMARY.md. Path tautan tidak boleh berubah.
Judul harus sama persis dengan heading pertama di file bab yang bersangkutan.
```

---

## Tahap 7: Pembangunan buku dan tautan

```
Jalankan `mdbook build`. Laporkan peringatan atau error, terutama tautan
anchor (#...) yang rusak karena heading diterjemahkan.
Beri daftar tautan yang rusak beserta usulan perbaikan. Jangan mengedit dulu.
```

---

## Tahap 8: Persiapan cetak B5 (setelah terjemahan selesai)

```
Buat alur pembuatan PDF ukuran B5 (176 × 250 mm) dari src/ memakai
Pandoc + Typst (keputusan 2026-10-17; Typst dipilih karena cepat, ringan,
dan Unicode-native, dengan XeLaTeX sebagai cadangan). Syaratnya: font isi
10 pt, margin sekitar 1,5-2 cm, blok kode tidak terpotong di tepi halaman
(baris panjang dilipat dengan penanda sambungan), nomor halaman di bawah,
daftar isi otomatis dengan nomor halaman, dan buku dipecah menjadi dua
jilid (usulan titik potong: jilid 1 = bab 00-12, jilid 2 = bab 13-21 +
Lampiran; sesuaikan setelah melihat jumlah halaman build pertama).
Jelaskan dulu rencananya, tunggu persetujuanku, baru buat filenya.
```

---

## Prompt cadangan (untuk situasi tertentu)

**Hasil terasa kaku atau seperti mesin:**
```
Tulis ulang paragraf di bawah heading "<judul>" agar lebih natural dalam
bahasa Indonesia akademis, tanpa mengubah makna, kode, atau istilah glosarium.
```

**Skrip pengecek gagal berulang:**
```
Tunjukkan perbedaan persis antara blok kode di asli/<file> dan src/<file>
untuk galat yang tersisa. Kembalikan blok kode itu ke versi aslinya.
```

**Sesi terasa melantur atau lambat:**
```
/clear
```
lalu mulai ulang dari prompt tahap yang sedang dikerjakan.

**Ingin berhenti dan melanjutkan besok:**
```
Tulis ringkasan 5 baris di file CATATAN.md: bab yang sudah selesai,
bab yang sedang dikerjakan, keputusan istilah baru, dan masalah yang masih terbuka.
```
