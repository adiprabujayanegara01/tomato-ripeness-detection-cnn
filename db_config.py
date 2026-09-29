import MySQLdb

# Fungsi untuk mendapatkan koneksi ke database
def get_db_connection():
    return MySQLdb.connect(
        host="localhost",     
        user="root",         
        passwd="",          
        db="tomato_ripeness_system",  
        charset="utf8mb4"
    )
