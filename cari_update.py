from models.atribut_produk import AtributProduk


def tampilkan_tabel(daftar):
    print("-" * 80)
    print(f"{'No':<4}| {'Kode':<8}| {'Nama':<25}| {'Kategori':<24}| {'Harga':>10} | {'Stok':>5}")
    print("-" * 80)
    nomor = 1
    for p in daftar:
        print(f"{nomor:<4}| {p['kode_produk']:<8}| {p['nama']:<25}| "
              f"{p['kategori']:<24}| {p['harga']:>10.0f} | {p['stok']:>5}")
        nomor = nomor + 1
    print("-" * 80)


# ===== FITUR 3: CARI PRODUK =====
def cari_produk(daftar, mode, kata_kunci):
    kata_kunci = kata_kunci.strip()

    if kata_kunci == "":
        return False, "Kata kunci tidak boleh kosong.", []

    hasil = []
    for p in daftar:
        if mode == "kode":
            if p["kode_produk"] == kata_kunci:        # harus persis sama
                hasil.append(p)
                break                                  # kode unik, cukup 1
        else:
            if kata_kunci.lower() in p["nama"].lower():  # cukup mengandung
                hasil.append(p)

    if len(hasil) == 0:
        return False, f"Produk dengan {mode} '{kata_kunci}' tidak ditemukan.", []

    return True, f"Ditemukan {len(hasil)} produk.", hasil


def menu_cari(daftar):
    print("\n=== CARI PRODUK ===")
    print("1. Cari berdasarkan kode")
    print("2. Cari berdasarkan nama")
    pilihan = input("Pilih (1/2): ").strip()

    if pilihan == "1":
        mode = "kode"
    elif pilihan == "2":
        mode = "nama"
    else:
        print("[ERROR] Pilihan tidak valid.")
        return

    kata_kunci = input("Kata kunci: ")
    ok, pesan, hasil = cari_produk(daftar, mode, kata_kunci)

    if ok:
        print("[OK] " + pesan)
        tampilkan_tabel(hasil)
    else:
        print("[ERROR] " + pesan)


# ===== FITUR 4: UPDATE STOK =====
def update_stok(daftar, kode, stok_teks):
    kode = kode.strip()
    if kode == "":
        return False, "Kode produk tidak boleh kosong."

    # cari produknya
    target = None
    for p in daftar:
        if p["kode_produk"] == kode:
            target = p
            break

    if target is None:
        return False, f"Produk dengan kode '{kode}' tidak ditemukan."

    # validasi stok memakai fungsi buatan teman
    stok_baru = AtributProduk.parse_stok(stok_teks)
    if stok_baru is None:
        return False, "Stok harus berupa angka bulat dan tidak boleh negatif."

    stok_lama = target["stok"]
    target["stok"] = stok_baru
    return True, f"Stok produk {target['nama']} berhasil diperbarui: {stok_lama} menjadi {stok_baru}"


def menu_update_stok(daftar):
    print("\n=== UPDATE STOK PRODUK ===")
    kode = input("Kode produk : ")
    stok = input("Stok baru   : ")
    ok, pesan = update_stok(daftar, kode, stok)

    if ok:
        print("[OK] " + pesan)
    else:
        print("[ERROR] " + pesan)


# ===== Menu tes (jalankan file ini langsung) =====
if __name__ == "__main__":
    from models.data_awal import buat_data_awal
    data = buat_data_awal()

    while True:
        print("\n3. Cari produk   4. Update stok   0. Keluar")
        pilih = input("Pilih: ").strip()
        if pilih == "0":
            break
        elif pilih == "3":
            menu_cari(data)
        elif pilih == "4":
            menu_update_stok(data)
        else:
            print("[ERROR] Pilihan tidak valid.")