import cv2
import os
import glob

# --- KONFIGURASI ---
# 1. Tentukan path ke folder input Anda
FOLDER_INPUT = r"D:\Lutter\PROJECT\Image_Enhancment_ColorScale\gambar"

# 2. Tentukan path ke folder output Anda (akan dibuat jika belum ada)
FOLDER_OUTPUT = "folder_output_hasil"

# 3. (Opsional) Sesuaikan parameter CLAHE
CLIP_LIMIT = 2.0
TILE_GRID_SIZE = (8, 8)
# --------------------


def enhance_image_clahe(image):
    """
    Menerapkan CLAHE pada gambar input (berwarna atau grayscale).
    """
    # Inisialisasi objek CLAHE
    # clipLimit: Ambang batas untuk membatasi kontras.
    # tileGridSize: Ukuran area lokal untuk histogram equalization.
    clahe = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=TILE_GRID_SIZE)
    
    # Cek apakah gambar berwarna atau grayscale
    if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
        # Ini adalah gambar grayscale
        # Langsung terapkan CLAHE
        enhanced_image = clahe.apply(image)
    
    elif len(image.shape) == 3:
        # Ini adalah gambar berwarna
        # Konversi dari BGR ke L*a*b* color space
        # Kita hanya ingin menerapkan CLAHE pada channel 'L' (Lightness)
        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Pisahkan channel L, a, dan b
        l_channel, a_channel, b_channel = cv2.split(lab_image)
        
        # Terapkan CLAHE pada channel L
        enhanced_l_channel = clahe.apply(l_channel)
        
        # Gabungkan kembali channel L yang sudah di-enhance dengan channel a dan b asli
        merged_lab_image = cv2.merge([enhanced_l_channel, a_channel, b_channel])
        
        # Konversi kembali dari L*a*b* ke BGR
        enhanced_image = cv2.cvtColor(merged_lab_image, cv2.COLOR_LAB2BGR)
    
    else:
        # Jika format tidak terduga, kembalikan gambar asli
        print(f"Format gambar tidak didukung: {image.shape}")
        enhanced_image = image

    return enhanced_image

def process_images_in_folder(input_dir, output_dir):
    """
    Memproses semua gambar dalam folder input dan menyimpannya di folder output.
    """
    # Pastikan folder output ada
    os.makedirs(output_dir, exist_ok=True)
    print(f"Folder output dipastikan ada di: {output_dir}")

    # Tentukan tipe file gambar yang ingin dicari
    file_types = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif"]
    
    image_paths = []
    for file_type in file_types:
        # Menggunakan glob untuk mencari file berdasarkan pola
        search_path = os.path.join(input_dir, file_type)
        image_paths.extend(glob.glob(search_path))

    if not image_paths:
        print(f"Tidak ditemukan gambar di folder: {input_dir}")
        return

    print(f"Ditemukan {len(image_paths)} gambar. Memulai proses...")

    # Loop melalui setiap path gambar
    for img_path in image_paths:
        try:
            # Baca gambar
            image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            
            if image is None:
                print(f"Gagal membaca: {img_path}. Melanjutkan...")
                continue

            print(f"Memproses: {img_path}")
            
            # Lakukan enhancement
            enhanced_image = enhance_image_clahe(image)
            
            # Dapatkan nama file asli
            filename = os.path.basename(img_path)
            
            # Tentukan path penyimpanan output
            output_path = os.path.join(output_dir, filename)
            
            # Simpan gambar yang sudah di-enhance
            cv2.imwrite(output_path, enhanced_image)
            print(f"Berhasil disimpan ke: {output_path}")

        except Exception as e:
            print(f"Gagal memproses {img_path}: {e}")

# --- Jalankan Skrip ---
if __name__ == "__main__":
    if not os.path.isdir(FOLDER_INPUT):
        print(f"Error: Folder input '{FOLDER_INPUT}' tidak ditemukan.")
    else:
        process_images_in_folder(FOLDER_INPUT, FOLDER_OUTPUT)
        print("\n--- Proses Selesai ---")