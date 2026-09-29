import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Model, Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input, Concatenate
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import cv2
from skimage.feature import local_binary_pattern

# Path dataset
dataset_path = "dataset"
labels = []
features = []
color_texture_features = []

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

# Load dataset dan ekstrak fitur gambar
num_images = 0
for category in os.listdir(dataset_path):
    category_path = os.path.join(dataset_path, category)
    if os.path.isdir(category_path):
        for filename in os.listdir(category_path):
            file_path = os.path.join(category_path, filename)
            image = cv2.imread(file_path)
            if image is None:
                print(f"Gagal membaca gambar: {file_path}")
                continue
            
            image = cv2.resize(image, (128, 128))
            color_features = extract_color_histogram(image)
            texture_features = extract_lbp_features(image)
            combined_features = np.hstack([color_features, texture_features])
            
            features.append(image)
            color_texture_features.append(combined_features)
            labels.append(category)
            num_images += 1
            print(f"Memproses: {file_path} ({num_images} gambar)")

print(f"Total gambar yang berhasil diproses: {num_images}")

# Konversi ke array NumPy
features = np.array(features, dtype="float32") / 255.0  # Normalisasi gambar
color_texture_features = np.array(color_texture_features, dtype="float32")
labels = np.array(labels)

# Encoding label
le = LabelEncoder()
labels = le.fit_transform(labels)
labels = to_categorical(labels)

# Split data menjadi train dan test
X_train, X_test, y_train, y_test, feat_train, feat_test = train_test_split(features, labels, color_texture_features, test_size=0.2, random_state=42)

# Augmentasi data
train_datagen = ImageDataGenerator(rotation_range=20, width_shift_range=0.2, height_shift_range=0.2, 
                                   horizontal_flip=True, fill_mode='nearest')

# Model CNN untuk fitur gambar
cnn_input = Input(shape=(128, 128, 3))
x = Conv2D(32, (3, 3), activation='relu')(cnn_input)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(64, (3, 3), activation='relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(128, (3, 3), activation='relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Flatten()(x)

# Model MLP untuk fitur warna dan tekstur
mlp_input = Input(shape=(color_texture_features.shape[1],))
y = Dense(64, activation='relu')(mlp_input)

# Gabungkan CNN dan MLP
merged = Concatenate()([x, y])
z = Dense(128, activation='relu')(merged)
z = Dropout(0.5)(z)
output = Dense(len(le.classes_), activation='softmax')(z)

# Model final
model = Model(inputs=[cnn_input, mlp_input], outputs=output)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Cetak jumlah sampel setelah split data
print("Shape X_train:", X_train.shape)
print("Shape y_train:", y_train.shape)
print("Shape feat_train:", feat_train.shape)

# Training model
print("Mulai pelatihan model...")
model.fit(
    [X_train, feat_train], y_train, 
    batch_size=32, epochs=20, 
    validation_data=([X_test, feat_test], y_test)
)

# Simpan model
os.makedirs("models", exist_ok=True)
model.save("models/cnn_model.h5")

# Simpan label encoder
np.save("models/cnn_label_encoder.npy", le.classes_)

print("Model CNN dengan fitur warna dan tekstur telah dilatih dan disimpan!")