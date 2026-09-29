import os
import time
import json
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.utils import secure_filename
from predict import predict_tomato
from db_config import get_db_connection
from auth_routes import auth 
from history_handler import save_prediction


# Inisialisasi Flask
app = Flask(__name__)
app.secret_key = "-"  

# Konfigurasi session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem" 
Session(app)  


# Register Blueprint untuk autentikasi
app.register_blueprint(auth, url_prefix='/auth')

# Folder untuk menyimpan gambar yang diunggah
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Fungsi untuk memeriksa ekstensi file yang diizinkan
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Pastikan folder upload ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Middleware untuk mengecek apakah pengguna sudah login
def login_required(f):
    def wrap(*args, **kwargs):
        if "user_id" not in session:
            flash("Anda harus login terlebih dahulu!", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Halaman utama (hanya bisa diakses jika login)
@app.route("/", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Tidak ada file yang diunggah!", "danger")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("Tidak ada file yang dipilih!", "danger")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            timestamp = int(time.time()) 
            filename = secure_filename(f"{timestamp}_" + file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            # Simpan nama file ke sesi
            session["filename"] = filename

            return redirect(url_for("loading"))

    return render_template("index.html")

# Halaman loading sebelum hasil prediksi
@app.route("/loading")
@login_required
def loading():
    return render_template("loading.html")

# Halaman Model CNN
@app.route("/model-cnn")
@login_required
def model_cnn():
    return render_template("model_cnn.html")


# Halaman Ringkasan hasil prediksi terakhir
@app.route("/rekap-prediksi")
def rekap_prediksi():
    filename = session.get("filename")
    result = session.get("result")
    return render_template("rekap_prediksi.html", filename=filename, result=result)

@app.route("/statistik-prediksi")
def statistik_prediksi():
    history_file = "history.json"
    stats = {"Matang": 0, "Setengah_Matang": 0, "Mentah": 0}

    try:
        if os.path.exists(history_file) and os.path.getsize(history_file) > 0:
            with open(history_file, "r") as f:
                data = json.load(f)
                for item in data:
                    label = item.get("label", "").strip().lower()
                    if label == "matang":
                        stats["Matang"] += 1
                    elif label == "setengah_matang":
                        stats["Setengah_Matang"] += 1
                    elif label == "mentah":
                        stats["Mentah"] += 1
    except (json.JSONDecodeError, FileNotFoundError):
        pass

    return render_template("statistik_prediksi.html", stats=stats)

# Halaman Hasil Prediksi
@app.route("/result")
def result():
    if "filename" in session:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], session["filename"])
        result = predict_tomato(file_path)
        session["result"] = result

        # Simpan hasil prediksi ke history.json
        if "Status Kematangan" in result:
            from history_handler import save_prediction
            save_prediction(session["filename"], result["Status Kematangan"])

        return render_template("result.html", filename=session["filename"], result=session["result"])
    return redirect(url_for("upload_file"))

# Halaman Riwayat Hasil Prediksi
@app.route("/riwayat-prediksi")
def riwayat_prediksi():
    history_file = "history.json"
    sort_by = request.args.get("sort_by", "time_desc")

    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    # Urutkan berdasarkan parameter
    if sort_by == "time_asc":
        history.sort(key=lambda x: x["timestamp"])
    elif sort_by == "label":
        history.sort(key=lambda x: x["label"])
    else:  
        history.sort(key=lambda x: x["timestamp"], reverse=True)

    return render_template("riwayat_prediksi.html", history=history, sort_by=sort_by)


# Jalankan aplikasi Flask
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)