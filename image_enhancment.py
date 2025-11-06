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

    # --- 2. Dialog Pilih MODE dan FILE/FOLDER ---
    
    # Siapkan root window tkinter dan sembunyikan
    root = tk.Tk()
    root.withdraw() 

    # Inisialisasi list file_paths
    file_paths = []

    # Tanyakan mode kepada user
    print("Pilih mode input:")
    print(" 1 = Pilih File (bisa pilih banyak file secara manual)")
    print(" 2 = Pilih Folder (memproses semua gambar di dalam satu folder)")
    mode = input("Masukkan pilihan (1 atau 2): ").strip()

    # --- PERBAIKAN KUAT: Paksa window untuk "bangun" ---
    # Kita paksa window utama (yang tersembunyi) untuk
    # aktif sesaat agar dialognya muncul di depan.
    try:
        root.deiconify() # Batal sembunyi (mungkin berkedip)
        root.lift()      # Bawa ke tumpukan paling atas
        root.attributes('-topmost', True)  # Paksa selalu di atas
        root.update()    # Proses semua perintah ini
        root.withdraw()  # Sembunyikan lagi dengan cepat
    except tk.TclError:
        # Beberapa sistem (spt Linux) mungkin tidak suka -topmost
        # Jika error, biarkan saja
        pass 
    # --- Akhir Perbaikan Kuat ---

    # --- Blok IF/ELSE ---
    if mode == '1':
        # --- Mode 1: Pilih File Individual ---
        print("\nMembuka dialog file... Silakan pilih satu atau lebih gambar.")
        file_paths_tuple = filedialog.askopenfilenames(
            title="Pilih satu atau lebih gambar",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("All Files", "*.*")
            ]
        )
        file_paths = list(file_paths_tuple) 

    elif mode == '2':
        # --- Mode 2: Pilih Folder ---
        print("\nMembuka dialog folder... Silakan pilih folder SUMBER gambar.")
        folder_input_path = filedialog.askdirectory(
            title="Pilih Folder Sumber Gambar"
        )
        if folder_input_path: 
            print(f"Memindai gambar di: {folder_input_path}...")
            ekstensi_gambar = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
            for filename in os.listdir(folder_input_path):
                if filename.lower().endswith(ekstensi_gambar):
                    full_path = os.path.join(folder_input_path, filename)
                    file_paths.append(full_path)
    else:
        # --- Mode Tidak Valid ---
        print(f"Pilihan '{mode}' tidak valid. Program berhenti.")

    # --- Kembalikan ke normal & Hancurkan ---
    try:
        root.attributes('-topmost', False) # Matikan mode "topmost"
    except tk.TclError:
        pass # Abaikan jika error
    
    root.destroy()

    # --- 2C. Validasi Gabungan ---
    if not file_paths:
        print("Tidak ada file gambar yang dipilih atau ditemukan. Program berhenti.")
        return
        
    print(f"\nDitemukan total {len(file_paths)} file gambar untuk diproses.")

    # --- 3. Tentukan Faktor Enhancement ---
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