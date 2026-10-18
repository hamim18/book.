-- Untuk buku cetak: buang tautan internal (#anchor) menjadi teks polos.
-- Prosa sudah menyebut nama sasarannya ("di Bab 18", "Bab 13"), dan label
-- antar-jilid tidak akan pernah ada di dokumen yang sama.
function Link(el)
  if el.target:match("^#") then
    return el.content
  end
  return nil
end

-- Kotak catatan mdBook (<section class="note">) dibungkus ulang menjadi
-- panggilan #catatan[...] agar gaya kotaknya bisa diatur di templat Typst.
-- (Pandoc mengubah div ini menjadi #block[...] polos dan membuang kelasnya.)
function Div(el)
  if el.classes:includes("note") then
    local hasil = {pandoc.RawBlock("typst", "#catatan[")}
    for _, b in ipairs(el.content) do
      table.insert(hasil, b)
    end
    table.insert(hasil, pandoc.RawBlock("typst", "]"))
    return hasil
  end
  return nil
end

-- Sisipkan import di kepala setiap file hasil konversi: include() Typst
-- mengevaluasi file dalam scope-nya SENDIRI (terbukti lewat uji), sehingga
-- file yang di-include tidak melihat binding file pemanggil.
-- Catatan: handler akar pandoc bernama `Pandoc`, bukan `Doc`.
function Pandoc(doc)
  doc.blocks:insert(1, pandoc.RawBlock("typst", '#import "../template.typ": catatan, caption'))
  return doc
end
