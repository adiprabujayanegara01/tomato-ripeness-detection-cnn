import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"

# Fungsi untuk menyimpan hasil prediksi
def save_prediction(filename, label):
    new_entry = {
        "filename": filename,
        "label": label,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Jika file belum ada, buat list baru
    if not os.path.exists(HISTORY_FILE):
        data = []
    else:
        with open(HISTORY_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(new_entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
