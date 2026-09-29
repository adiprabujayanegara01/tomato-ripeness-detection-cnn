import MySQLdb
import bcrypt
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from db_config import get_db_connection

# Inisialisasi Blueprint untuk modularisasi
auth = Blueprint('auth', __name__)

# Route untuk registrasi pengguna
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Registrasi berhasil! Silakan login.", "success")
            return redirect(url_for('auth.login'))
        except MySQLdb.IntegrityError:
            flash("Username atau Email sudah terdaftar!", "danger")
    
    return render_template('register.html')

# Route untuk login pengguna
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            session['user_id'] = user[0]
            flash("Login berhasil!", "success")
            return redirect(url_for('upload_file'))  
        else:
            flash("Username atau password salah!", "danger")

    return render_template('login.html')

# Route untuk logout pengguna
@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Anda telah logout.", "info")
    return redirect(url_for('auth.login'))
