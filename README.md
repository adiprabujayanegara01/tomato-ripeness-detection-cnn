# 🍅 Deteksi Kematangan Buah Tomat Menggunakan CNN

Sistem berbasis web untuk **mendeteksi tingkat kematangan buah tomat** menggunakan **Convolutional Neural Network (CNN)** dengan memanfaatkan citra digital serta ekstraksi fitur **warna** dan **tekstur**.

Proyek ini dikembangkan sebagai bagian dari penelitian/skripsi dengan judul:

> **Deteksi Kematangan Buah Tomat Menggunakan Convolutional Neural Network Berdasarkan Ekstraksi Fitur Warna dan Tekstur**

---

## 📌 Deskripsi

Sistem menerima gambar buah tomat dari pengguna, kemudian melakukan preprocessing dan ekstraksi fitur sebelum menghasilkan prediksi tingkat kematangan.

Model menggunakan dua jenis informasi:

1. **Fitur citra** → diproses menggunakan CNN.
2. **Fitur warna dan tekstur** → diproses menggunakan jaringan MLP dan kemudian digabungkan dengan keluaran CNN.

Klasifikasi yang tersedia:

- 🍅 **Mentah**
- 🍅 **Setengah Matang**
- 🍅 **Matang**

Aplikasi dibangun menggunakan **Flask** dan menyediakan fitur autentikasi pengguna, upload/ambil gambar, prediksi, riwayat prediksi, rekap hasil, serta statistik kategori kematangan.

---

## ✨ Fitur Sistem

- 🔐 Registrasi dan login pengguna
- 📷 Upload gambar tomat
- 📸 Pengambilan gambar melalui kamera browser
- 🧠 Prediksi menggunakan model CNN
- 🎨 Ekstraksi fitur warna menggunakan **HSV Color Histogram**
- 🔎 Ekstraksi fitur tekstur menggunakan **Local Binary Pattern (LBP)**
- 📊 Confidence score hasil prediksi
- 📂 Riwayat hasil prediksi
- 📈 Statistik kategori kematangan
- 🧾 Rekap hasil prediksi terakhir
- 🧠 Halaman informasi arsitektur/model CNN

---

## 🧠 Metodologi

Secara umum, proses sistem adalah:

```text
Input Gambar Tomat
        │
        ▼
Preprocessing
(Resize 128 × 128)
        │
        ├──────────────────────┐
        ▼                      ▼
   Citra RGB             Ekstraksi Fitur
        │                Warna + Tekstur
        │                      │
        ▼                      ▼
       CNN                    MLP
        │                      │
        └──────────┬───────────┘
                   ▼
              Concatenate
                   │
                   ▼
          Fully Connected Layer
                   │
                   ▼
              Softmax
                   │
                   ▼
       Klasifikasi Kematangan
```

### 1. Preprocessing

Gambar input diubah ukurannya menjadi:

```text
128 × 128 × 3
```

Kemudian nilai piksel dinormalisasi ke rentang `0–1`.

### 2. Ekstraksi Fitur Warna

Sistem menggunakan **Histogram HSV** dengan konfigurasi:

```text
bins = (8, 8, 8)
```

Sehingga menghasilkan:

```text
8 × 8 × 8 = 512 fitur
```

### 3. Ekstraksi Fitur Tekstur

Tekstur diekstraksi menggunakan **Local Binary Pattern (LBP)** dengan:

```text
P = 24
R = 3
method = uniform
```

Histogram LBP kemudian dinormalisasi.

### 4. CNN

Citra diproses melalui beberapa convolutional layer:

```text
Input 128 × 128 × 3
        ↓
Conv2D 32 filter
        ↓
MaxPooling
        ↓
Conv2D 64 filter
        ↓
MaxPooling
        ↓
Conv2D 128 filter
        ↓
MaxPooling
        ↓
Flatten
```

### 5. Penggabungan Fitur

Fitur citra dari CNN digabungkan dengan fitur warna dan tekstur melalui:

```text
Concatenate(CNN Features + Color/Texture Features)
```

Kemudian diproses melalui Dense Layer dan Dropout sebelum menghasilkan kelas menggunakan Softmax.

---

## 📁 Struktur Repository

```text
Tomat/
├── app.py
├── predict.py
├── auth_routes.py
├── db_config.py
├── history_handler.py
├── history.json
│
├── models/
│   ├── cnn_model.h5
│   ├── cnn_label_encoder.npy
│   └── train_cnn.py
│
├── templates/
│   ├── index.html
│   ├── loading.html
│   ├── login.html
│   ├── register.html
│   ├── model_cnn.html
│   ├── result.html
│   ├── rekap_prediksi.html
│   ├── riwayat_prediksi.html
│   └── statistik_prediksi.html
│
└── static/
    ├── style.css
    ├── script.js
    └── *.png
```

> Folder `dataset/` tidak terdapat pada ZIP aplikasi yang diberikan. Dataset diperlukan apabila ingin melakukan pelatihan ulang model menggunakan `models/train_cnn.py`.

---

## ⚙️ Teknologi yang Digunakan

| Teknologi | Fungsi |
|---|---|
| Python | Bahasa pemrograman |
| Flask | Web framework |
| TensorFlow / Keras | Pembuatan dan penggunaan model CNN |
| OpenCV | Pengolahan citra |
| scikit-image | Ekstraksi fitur LBP |
| NumPy | Pengolahan array dan fitur |
| scikit-learn | Encoding label dan pembagian dataset |
| MySQL | Penyimpanan data pengguna |
| bcrypt | Hash password |
| Bootstrap | Tampilan antarmuka |

---

## 💻 Persyaratan

Disarankan menggunakan:

- Python 3.x
- MySQL / XAMPP
- pip
- Browser modern

Install library yang digunakan:

```bash
pip install flask flask-session werkzeug mysqlclient bcrypt numpy tensorflow opencv-python scikit-image scikit-learn
```

> Catatan: instalasi `mysqlclient` pada Windows dapat membutuhkan konfigurasi/komponen tambahan. Sesuaikan dengan environment Python yang digunakan.

---

## 🗄️ Konfigurasi Database

Aplikasi menggunakan database MySQL dengan nama:

```text
tomato_ripeness_system
```

Konfigurasi saat ini berada pada:

```text
db_config.py
```

Konfigurasi default pada kode:

```text
host     = localhost
user     = root
password = kosong
database = tomato_ripeness_system
```

Buat database terlebih dahulu:

```sql
CREATE DATABASE tomato_ripeness_system
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Kemudian buat tabel pengguna:

```sql
USE tomato_ripeness_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
```

---

## 🚀 Instalasi dan Menjalankan Sistem

### 1. Clone repository

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
```

### 2. Buat virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask flask-session werkzeug mysqlclient bcrypt numpy tensorflow opencv-python scikit-image scikit-learn
```

### 4. Pastikan MySQL aktif

Jika menggunakan XAMPP, aktifkan:

```text
Apache
MySQL
```

Buat database dan tabel `users` sesuai bagian konfigurasi database di atas.

### 5. Jalankan aplikasi

```bash
python app.py
```

Jika berhasil, Flask akan menjalankan aplikasi pada:

```text
http://127.0.0.1:5000
```

Buka alamat tersebut melalui browser.

---

## 🔮 Cara Menggunakan Sistem

1. Buka aplikasi melalui browser.
2. Lakukan registrasi akun.
3. Login menggunakan akun yang telah dibuat.
4. Pilih atau ambil gambar buah tomat.
5. Klik **Upload & Prediksi**.
6. Sistem melakukan preprocessing dan ekstraksi fitur.
7. Model CNN melakukan klasifikasi.
8. Sistem menampilkan:
   - Status kematangan
   - Confidence score
9. Hasil prediksi dapat dilihat kembali melalui menu riwayat dan statistik.

---

## 📊 Kelas Prediksi

Model menggunakan tiga kelas:

```text
matang
mentah
setengah_matang
```

Label tersebut tersimpan pada:

```text
models/cnn_label_encoder.npy
```

---

## 🏋️ Training Model

Pelatihan model dilakukan menggunakan:

```text
models/train_cnn.py
```

Script tersebut membaca dataset dari:

```text
dataset/
```

Struktur dataset yang digunakan:

```text
dataset/
├── matang/
│   ├── gambar1.jpg
│   ├── gambar2.jpg
│   └── ...
│
├── mentah/
│   ├── gambar1.jpg
│   └── ...
│
└── setengah_matang/
    ├── gambar1.jpg
    └── ...
```

Setelah proses training selesai, model disimpan sebagai:

```text
models/cnn_model.h5
```

dan label encoder disimpan sebagai:

```text
models/cnn_label_encoder.npy
```

Parameter training pada script saat ini antara lain:

```text
Batch size : 32
Epoch      : 20
Test size  : 20%
Random     : 42
Optimizer  : Adam
```

---

## 📈 Dokumentasi Visual

Repository menyediakan beberapa gambar pendukung penelitian, antara lain:

- Arsitektur CNN
- Contoh dataset RGB
- Citra grayscale
- Citra HSV
- Histogram HSV
- Citra LBP
- Histogram LBP
- Confusion matrix
- Perbandingan accuracy
- Perbandingan loss

File-file tersebut tersedia pada folder:

```text
static/
```

---

## ⚠️ Catatan Keamanan Sebelum Repository Dipublikasikan

Sebelum menjadikan repository **Public**, sebaiknya lakukan beberapa perubahan:

### 1. Jangan menyimpan secret key langsung di source code

Saat ini terdapat:

```python
app.secret_key = "supersecretkey"
```

Untuk repository publik, sebaiknya gunakan environment variable.

### 2. Jangan menyimpan password database

Konfigurasi database sebaiknya tidak menggunakan kredensial pribadi secara langsung.

Gunakan `.env` atau environment variable.

### 3. Jangan upload data sensitif

Pastikan repository tidak berisi:

- Password
- API key
- Secret key
- Data pengguna
- Data pribadi
- Credential database

### 4. Folder upload

Folder:

```text
static/uploads/
```

sebaiknya tidak digunakan untuk menyimpan gambar pengguna yang bersifat pribadi pada repository.

---


## 👤 Author

**[Adi Prabu Jayanegara]**

Program Studi: **[Informatika]**  
Universitas: **[Universitas Teknologi Yogyakarta]**  
Tahun: **2026**

---

## 📚 Referensi

Proyek ini dikembangkan sebagai bagian dari penelitian:

> **Deteksi Kematangan Buah Tomat Menggunakan Convolutional Neural Network Berdasarkan Ekstraksi Fitur Warna dan Tekstur**

