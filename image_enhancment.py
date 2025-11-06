import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt

def proses_gambar():
    """
    Fungsi utama untuk memilih file (individual ATAU folder), 
    melakukan color enhancement, menyimpan, dan menampilkan perbandingan.
    """
    
    # --- 1. Konfigurasi Awal ---
    folder_output = "hasil_enhancement"
    if not os.path.exists(folder_output):
        os.makedirs(folder_output)
        print(f"Folder '{folder_output}' telah dibuat.")

    # --- 2. Dialog Pilih File ---
    
    # Siapkan root window tkinter dan sembunyikan
    root = tk.Tk()
    root.withdraw()

    # Buka dialog untuk memilih BANYAK file gambar
    print("Membuka dialog file... Silakan pilih satu atau lebih gambar.")
    file_paths = filedialog.askopenfilenames(
        title="Pilih satu atau lebih gambar",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
            ("All Files", "*.*")
        ]
    )

    # Hentikan program jika tidak ada file yang dipilih
    if not file_paths:
        print("Tidak ada file yang dipilih. Program berhenti.")
        return

    # --- 3. Tentukan Faktor Enhancement ---
    # nilai default:
    # <1.0 pudar
    # 1.0 = asli
    # 1.5 perubahan, dimana 50% pudar, 50% berwarna lebih kuat
    # 2.0 = dua kali lebih berwarna
    enhancement_factor = 1.5    
    try:
        faktor_str = input(f"Masukkan faktor enhancement warna (Contoh: 1.5) [Default: {enhancement_factor}]: ")
        if faktor_str.strip():
            enhancement_factor = float(faktor_str)
    except ValueError:
        print(f"Input tidak valid. Menggunakan nilai default: {enhancement_factor}")

    print(f"\nMemproses {len(file_paths)} gambar dengan faktor {enhancement_factor}...")

    # --- 4. Loop Proses Gambar ---
    for file_path in file_paths:
        try:
            img_original = Image.open(file_path)
            if img_original.mode not in ('RGB'):
                img_original = img_original.convert('RGB')

            enhancer = ImageEnhance.Color(img_original)
            img_enhanced = enhancer.enhance(enhancement_factor)

            # --- 5. Simpan Hasil ---
            filename = os.path.basename(file_path)
            nama_file, ekstensi = os.path.splitext(filename)
            nama_file_baru = f"{nama_file}_enhanced{ekstensi}"
            path_simpan = os.path.join(folder_output, nama_file_baru)
            img_enhanced.save(path_simpan)
            print(f" -> Berhasil disimpan di: {path_simpan}")

            # --- 6. Tampilkan Perbandingan ---
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            ax1.imshow(img_original)
            ax1.set_title(f"Asli: {filename}")
            ax1.axis('off') 
            ax2.imshow(img_enhanced)
            ax2.set_title(f"Enhanced (Faktor: {enhancement_factor})")
            ax2.axis('off')
            plt.suptitle("Perbandingan Gambar Asli vs Enhanced", fontsize=16)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.show() 

        except Exception as e:
            print(f" !! Gagal memproses file {file_path}: {e}")

    print("\nSemua proses telah selesai.")

# --- Jalankan Fungsi Utama ---
if __name__ == "__main__":
    proses_gambar()