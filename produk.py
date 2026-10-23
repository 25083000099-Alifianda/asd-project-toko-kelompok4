import math

from models.atribut_produk import AtributProduk
from models.data_awal import buat_data_awal

# Array of Struct: seluruh produk disimpan di sini.
# Diisi dari data_awal.py (fungsi mengembalikan list baru tiap dipanggil).
daftar_produk = buat_data_awal()



parse_harga = AtributProduk.parse_harga


parse_stok = AtributProduk.parse_stok


def format_rupiah(angka):
    """Contoh: 15000.0 -> 'Rp 15.000'"""
    return "Rp " + f"{angka:,.0f}".replace(",", ".")



def cari_by_kode(kode):
    """Exact match. Return dict produk atau None."""
    kode = kode.strip()
    for produk in daftar_produk:
        if produk["kode_produk"] == kode:
            return produk
    return None


def cari_by_nama(kata_kunci):
    """Partial match (tidak peka huruf besar/kecil). Return list produk."""
    kata_kunci = kata_kunci.strip().lower()
    return [p for p in daftar_produk if kata_kunci in p["nama"].lower()]


def saran_kode_berikutnya(prefix="PRD-", lebar=3):
    """Saran kode baru = nomor terbesar yang sudah ada + 1 (contoh: PRD-008)."""
    nomor_terbesar = 0
    for p in daftar_produk:
        kode = p["kode_produk"]
        sisa = kode[len(prefix):]
        if kode.startswith(prefix) and sisa.isdigit():
            nomor_terbesar = max(nomor_terbesar, int(sisa))
    return f"{prefix}{nomor_terbesar + 1:0{lebar}d}"


# ---------------------------------------------------------------
# Fitur 1: Tambah produk
# ---------------------------------------------------------------
def tambah_produk(kode, nama, kategori, harga_teks, stok_teks):
    """Validasi (lewat class AtributProduk) lalu tambah produk. Return (sukses, pesan)."""
    kode = kode.strip()
    if kode and cari_by_kode(kode) is not None:
        return False, f"Kode produk '{kode}' sudah digunakan."
    try:
        item = AtributProduk.dari_teks(kode, nama, kategori, harga_teks, stok_teks)
    except ValueError as err:
        return False, str(err)
    daftar_produk.append(item.to_dict())
    return True, f"Produk {item.nama} berhasil ditambahkan."


# ---------------------------------------------------------------
# Fitur 2 & 3: Tampilan tabel
# ---------------------------------------------------------------
def cetak_tabel(produk_list):
    """Cetak list produk sebagai tabel rapi (dipakai F2 dan F3)."""
    header = ["No", "Kode", "Nama", "Kategori", "Harga", "Stok"]
    baris = [
        [str(i), p["kode_produk"], p["nama"], p["kategori"],
         format_rupiah(p["harga"]), str(p["stok"])]
        for i, p in enumerate(produk_list, start=1)
    ]

    # lebar tiap kolom = teks terpanjang di kolom itu
    lebar = [max(len(r[k]) for r in [header] + baris) for k in range(len(header))]

    def format_baris(r):
        sel = []
        for k, teks in enumerate(r):
            # kolom Harga & Stok rata kanan, sisanya rata kiri
            sel.append(teks.rjust(lebar[k]) if k >= 4 or k == 0 else teks.ljust(lebar[k]))
        return "│ " + " │ ".join(sel) + " │"

    garis = "├─" + "─┼─".join("─" * w for w in lebar) + "─┤"
    print("┌─" + "─┬─".join("─" * w for w in lebar) + "─┐")
    print(format_baris(header))
    print(garis)
    for r in baris:
        print(format_baris(r))
    print("└─" + "─┴─".join("─" * w for w in lebar) + "─┘")


def tampilkan_semua():
    if not daftar_produk:
        print("Belum ada produk yang tersimpan.")
        return
    cetak_tabel(daftar_produk)
    print(f"Total: {len(daftar_produk)} produk.")


# ---------------------------------------------------------------
# Fitur 4 & 5: Update stok / harga
# ---------------------------------------------------------------
def update_stok(kode, stok_teks):
    """Ganti stok ke nilai baru. Return (sukses, pesan)."""
    produk = cari_by_kode(kode)
    if produk is None:
        return False, f"Produk dengan kode '{kode.strip()}' tidak ditemukan."
    stok_baru = parse_stok(stok_teks)
    if stok_baru is None:
        return False, "Stok baru harus berupa angka bulat dan tidak boleh negatif."
    stok_lama = produk["stok"]
    produk["stok"] = stok_baru
    return True, (f"Stok produk {produk['nama']} berhasil diperbarui: "
                  f"{stok_lama} menjadi {stok_baru}")


def update_harga(kode, harga_teks):
    """Ganti harga ke nilai baru. Return (sukses, pesan)."""
    produk = cari_by_kode(kode)
    if produk is None:
        return False, f"Produk dengan kode '{kode.strip()}' tidak ditemukan."
    harga_baru = parse_harga(harga_teks)
    if harga_baru is None:
        return False, "Harga baru harus berupa angka dan lebih dari 0."
    harga_lama = produk["harga"]
    produk["harga"] = harga_baru
    return True, (f"Harga produk {produk['nama']} berhasil diperbarui: "
                  f"{format_rupiah(harga_lama)} menjadi {format_rupiah(harga_baru)}")


# ---------------------------------------------------------------
# Fitur 6: Hapus produk
# ---------------------------------------------------------------
def hapus_produk(kode):
    """Hapus produk dari list. Konfirmasi dilakukan di main.py."""
    produk = cari_by_kode(kode)
    if produk is None:
        return False
    daftar_produk.remove(produk)
    return True