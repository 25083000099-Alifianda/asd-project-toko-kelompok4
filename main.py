import atribut_produk
import produk


def tampilkan_menu():
    print("\n" + "=" * 40)
    print("   SISTEM MANAJEMEN TOKO / INVENTORI")
    print("=" * 40)
    print("1. Tambah Produk Baru")
    print("2. Tampilkan Semua Produk")
    print("3. Cari Produk")
    print("4. Update Stok Produk")
    print("5. Update Harga Produk")
    print("6. Hapus Produk")
    print("0. Keluar")
    print("-" * 40)


def menu_tambah():
    print("\n--- Tambah Produk Baru ---")
    atribut_produk.tampilkan_panduan_input()
    print(f"\nSaran kode berikutnya: {produk.saran_kode_berikutnya()}\n")
    kode = input("Kode produk : ")
    nama = input("Nama        : ")
    kategori = input("Kategori    : ")
    harga = input("Harga (Rp)  : ")
    stok = input("Stok        : ")
    sukses, pesan = produk.tambah_produk(kode, nama, kategori, harga, stok)
    print(("[OK] " if sukses else "[ERROR] ") + pesan)
    if sukses:  # tampilkan produk yang baru ditambahkan
        produk.cetak_tabel([produk.cari_by_kode(kode)])


def menu_cari():
    print("\n--- Cari Produk ---")
    print("1. Berdasarkan kode (exact match)")
    print("2. Berdasarkan nama (partial match)")
    mode = input("Pilih mode (1/2): ").strip()

    if mode not in ("1", "2"):
        print("[ERROR] Mode pencarian tidak valid.")
        return

    label = "kode" if mode == "1" else "nama"
    kata_kunci = input(f"Masukkan {label}: ").strip()
    if not kata_kunci:
        print("[ERROR] Kata kunci tidak boleh kosong.")
        return

    if mode == "1":
        hasil = produk.cari_by_kode(kata_kunci)
        hasil = [hasil] if hasil else []
    else:
        hasil = produk.cari_by_nama(kata_kunci)

    if not hasil:
        print(f"Produk dengan {label} '{kata_kunci}' tidak ditemukan.")
        return
    produk.cetak_tabel(hasil)
    print(f"Ditemukan {len(hasil)} produk.")


def menu_update_stok():
    print("\n--- Update Stok Produk ---")
    kode = input("Kode produk : ")
    if produk.cari_by_kode(kode) is None:
        print(f"[ERROR] Produk dengan kode '{kode.strip()}' tidak ditemukan.")
        return
    stok = input("Stok baru    : ")
    sukses, pesan = produk.update_stok(kode, stok)
    print(("[OK] " if sukses else "[ERROR] ") + pesan)


def menu_update_harga():
    print("\n--- Update Harga Produk ---")
    kode = input("Kode produk : ")
    if produk.cari_by_kode(kode) is None:
        print(f"[ERROR] Produk dengan kode '{kode.strip()}' tidak ditemukan.")
        return
    harga = input("Harga baru (Rp): ")
    sukses, pesan = produk.update_harga(kode, harga)
    print(("[OK] " if sukses else "[ERROR] ") + pesan)


def menu_hapus():
    print("\n--- Hapus Produk ---")
    kode = input("Kode produk : ")
    item = produk.cari_by_kode(kode)
    if item is None:
        print(f"Produk dengan kode '{kode.strip()}' tidak ditemukan.")
        return

    # tampilkan nama dulu, lalu minta konfirmasi
    nama = item["nama"]
    while True:
        jawab = input(f"Yakin hapus produk '{nama}'? (y/n): ").strip().lower()
        if jawab in ("y", "n"):
            break
        print("Ketik 'y' untuk ya atau 'n' untuk tidak.")

    if jawab == "y":
        produk.hapus_produk(kode)
        print(f"[OK] Produk {nama} berhasil dihapus dari sistem.")
    else:
        print("Penghapusan dibatalkan.")


def main():
    aksi = {
        "1": menu_tambah,
        "2": produk.tampilkan_semua,
        "3": menu_cari,
        "4": menu_update_stok,
        "5": menu_update_harga,
        "6": menu_hapus,
    }

    while True:
        tampilkan_menu()
        try:
            pilihan = input("Pilih menu: ").strip()
            if pilihan == "0":
                print("Terima kasih. Sampai jumpa!")
                break
            if pilihan in aksi:
                aksi[pilihan]()
            else:
                print("[ERROR] Pilihan tidak valid. Masukkan angka 0-6.")
        except (KeyboardInterrupt, EOFError):
            print("\nProgram dihentikan.")
            break


if __name__ == "__main__":
    main()