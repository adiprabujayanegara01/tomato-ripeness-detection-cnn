import os  
import cv2 
import numpy as np 
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model 
from skimage.feature import local_binary_pattern 

# Path folder models 
model_dir = "models" 

# Load CNN model 
print("Memuat model CNN...")
cnn_model = load_model(os.path.join(model_dir, "cnn_model.h5")) 
print("Model CNN berhasil dimuat!")

# Load label encoder (pastikan isinya adalah array string) 
print("Memuat label encoder...")
cnn_label_encoder = np.load(os.path.join(model_dir, "cnn_label_encoder.npy"), allow_pickle=True) 
print(f"Label encoder berhasil dimuat! Kelas yang tersedia: {cnn_label_encoder}")

# Fungsi ekstraksi fitur warna (histogram HSV) 
def extract_color_histogram(image, bins=(8, 8, 8)): 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
    hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256]) 
    cv2.normalize(hist, hist) 
    return hist.flatten() 

# Fungsi ekstraksi fitur tekstur (Local Binary Pattern - LBP) 
def extract_lbp_features(image): 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    lbp = local_binary_pattern(gray, P=24, R=3, method="uniform") 
    hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 27), range=(0, 26)) 
    hist = hist.astype("float") 
    hist /= hist.sum()  # Normalisasi 
    return hist 

# Fungsi preprocessing gambar untuk CNN 
def preprocess_for_cnn(image): 
    print("Melakukan preprocessing gambar untuk CNN...")
    image = cv2.resize(image, (128, 128)) 
    image = image.astype("float32") / 255.0 
    return np.expand_dims(image, axis=0) 

# Fungsi untuk melakukan prediksi dari gambar input menggunakan CNN dan fitur tambahan 
def predict_tomato(image_path): 
    print(f"\nMemproses gambar: {image_path}")

    # Baca dan preprocess gambar 
    image = cv2.imread(image_path) 
    if image is None: 
        print("❌ ERROR: Gambar tidak valid atau tidak ditemukan.")
        return {"error": "Gambar tidak valid atau tidak ditemukan."} 
    print("✅ Gambar berhasil dibaca!")

    # Ekstraksi fitur untuk CNN 
    cnn_input = preprocess_for_cnn(image) 

    # Ekstraksi fitur warna dan tekstur 
    print("🔍 Mengekstrak fitur warna dan tekstur...")
    color_features = extract_color_histogram(image) 
    texture_features = extract_lbp_features(image) 
    combined_features = np.hstack([color_features, texture_features]) 

    print(f"✅ Ekstraksi fitur selesai! Panjang fitur: {combined_features.shape[0]}")

    # Format ulang untuk input model 
    combined_features = np.expand_dims(combined_features, axis=0) 
    
    # Prediksi dari model CNN 
    print("🔮 Melakukan prediksi dengan model CNN...")
    cnn_probs = cnn_model.predict([cnn_input, combined_features])[0] 
    
    # Ambil label prediksi dan confidence 
    cnn_pred_label = np.argmax(cnn_probs) 
    cnn_confidence = np.max(cnn_probs) * 100 
    cnn_label = str(cnn_label_encoder[cnn_pred_label])  # Konversi label numerik ke string 

    print(f"🎯 Prediksi: {cnn_label} (Confidence: {cnn_confidence:.2f}%)")

    # Cek apakah confidence score terlalu rendah 
    if cnn_confidence < 90: 
        print("⚠️ Confidence rendah! Model tidak yakin dengan hasil prediksi.")
        return { 
            "Status Kematangan": "Tidak yakin", 
            "Confidence Scores": {cnn_label: f"{cnn_confidence:.2f}%"}, 
            "Note": "Confidence rendah, coba gambar lain." 
        } 
    
    return { 
        "Status Kematangan": cnn_label, 
        "Confidence Scores": {cnn_label: f"{cnn_confidence:.2f}%"} 
    } 

# Contoh penggunaan langsung di terminal 
if __name__ == "__main__": 
    test_image = "setengah matang 1.jpg" 
    result = predict_tomato(test_image) 
    print("\n📢 Hasil Akhir:")
    print(f"Status Kematangan: {result['Status Kematangan']}") 
    print(f"Confidence Scores: {result['Confidence Scores']}")
    if "Note" in result:
        print(f"📝 Catatan: {result['Note']}")
