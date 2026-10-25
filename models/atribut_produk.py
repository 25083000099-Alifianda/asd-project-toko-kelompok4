import math


ATRIBUT_PRODUK = [
    {"nama_atribut": "kode_produk", "tipe_data": "str", "contoh_nilai": '"PRD-001"',
     "keterangan": "Kode unik produk. Tidak boleh duplikat dan tidak boleh kosong. Format bebas."},
    {"nama_atribut": "nama", "tipe_data": "str", "contoh_nilai": '"Kemeja Flanel Casual"',
     "keterangan": "Nama produk. Tidak boleh kosong."},
    {"nama_atribut": "kategori", "tipe_data": "str", "contoh_nilai": '"Pakaian"',
     "keterangan": "Kategori produk. Bebas diisi, tidak boleh kosong."},
    {"nama_atribut": "harga", "tipe_data": "float", "contoh_nilai": "150000.0",
     "keterangan": "Harga satuan dalam Rupiah. Harus lebih dari 0."},
    {"nama_atribut": "stok", "tipe_data": "int", "contoh_nilai": "45",
     "keterangan": "Jumlah stok tersedia. Tidak boleh negatif."},
]


class AtributProduk:
    """Satu produk dengan 5 atribut + validasinya."""

    def __init__(self, kode_produk, nama, kategori, harga, stok):
        self.kode_produk = kode_produk
        self.nama = nama
        self.kategori = kategori
        self.harga = harga
        self.stok = stok

   
    @staticmethod
    def parse_harga(teks):
        """Teks -> float > 0. Return None jika tidak valid."""
        try:
            harga = float(teks.strip())
        except ValueError:
            return None
        if math.isnan(harga) or math.isinf(harga) or harga <= 0:
            return None
        return harga

    @staticmethod
    def parse_stok(teks):
        """Teks -> int >= 0. Return None jika tidak valid."""
        try:
            stok = int(teks.strip())
        except ValueError:
            return None
        return None if stok < 0 else stok

    @classmethod
    def dari_teks(cls, kode, nama, kategori, harga_teks, stok_teks):
        """Validasi semua input teks. Raise ValueError(pesan) jika salah."""
        kode, nama, kategori = kode.strip(), nama.strip(), kategori.strip()
        if not kode:
            raise ValueError("Kode produk tidak boleh kosong.")
        if not nama:
            raise ValueError("Nama produk tidak boleh kosong.")
        if not kategori:
            raise ValueError("Kategori tidak boleh kosong.")
        harga = cls.parse_harga(harga_teks)
        if harga is None:
            raise ValueError("Harga harus berupa angka dan lebih dari 0.")
        stok = cls.parse_stok(stok_teks)
        if stok is None:
            raise ValueError("Stok harus berupa angka bulat dan tidak boleh negatif.")
        return cls(kode, nama, kategori, harga, stok)

    def to_dict(self):
        """Ubah ke dict (struct) agar bisa disimpan di daftar_produk."""
        return {
            "kode_produk": self.kode_produk,
            "nama": self.nama,
            "kategori": self.kategori,
            "harga": self.harga,
            "stok": self.stok,
        }

    @staticmethod
    def tampilkan_tabel_atribut():
        judul = ("Nama Atribut", "Tipe Data (Python)", "Contoh Nilai", "Keterangan")
        kunci = ("nama_atribut", "tipe_data", "contoh_nilai", "keterangan")
        baris = [tuple(a[k] for k in kunci) for a in ATRIBUT_PRODUK]
        lebar = [max(len(r[i]) for r in [judul] + baris) for i in range(len(judul))]

        def cetak(isi):
            print("│ " + " │ ".join(isi[i].ljust(lebar[i]) for i in range(len(isi))) + " │")

        print("┌─" + "─┬─".join("─" * w for w in lebar) + "─┐")
        cetak(judul)
        print("├─" + "─┼─".join("─" * w for w in lebar) + "─┤")
        for isi in baris:
            cetak(isi)
        print("└─" + "─┴─".join("─" * w for w in lebar) + "─┘")

    @staticmethod
    def tampilkan_panduan_input():
        print("Atribut produk yang perlu diisi:")
        for a in ATRIBUT_PRODUK:
            print(f"  - {a['nama_atribut']} ({a['tipe_data']}), contoh: {a['contoh_nilai']}")
            print(f"      {a['keterangan']}")

tampilkan_tabel_atribut = AtributProduk.tampilkan_tabel_atribut
tampilkan_panduan_input = AtributProduk.tampilkan_panduan_input


def jalankan_cli():
    import os, sys
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root not in sys.path:
        sys.path.insert(0, root)   # root proyek, tempat produk.py berada
    import produk                  # import 
    import cari_update             # fitur 3 (cari) dan 4 (update stok)

    print("ENTITAS: PRODUK\n")
    AtributProduk.tampilkan_tabel_atribut()

    while True:
        print("\n1. Tambah produk  2. Lihat semua produk  3. Cari produk  4. Update stok  0. Keluar")
        try:
            pilihan = input("Pilih: ").strip()
            if pilihan == "0":
                print("Sampai jumpa!")
                break
            elif pilihan == "1":
                print(f"\nSaran kode berikutnya: {produk.saran_kode_berikutnya()}")
                kode = input("Kode produk : ")
                nama = input("Nama        : ")
                kategori = input("Kategori    : ")
                harga = input("Harga (Rp)  : ")
                stok = input("Stok        : ")
                ok, pesan = produk.tambah_produk(kode, nama, kategori, harga, stok)
                print(("[OK] " if ok else "[ERROR] ") + pesan)
            elif pilihan == "2":
                produk.tampilkan_semua()
            elif pilihan == "3":
                cari_update.menu_cari(produk.daftar_produk)
            elif pilihan == "4":
                cari_update.menu_update_stok(produk.daftar_produk)
            else:
                print("[ERROR] Pilihan tidak valid.")
        except (KeyboardInterrupt, EOFError):
            print("\nProgram dihentikan.")
            break

if __name__ == "__main__":        
    jalankan_cli()