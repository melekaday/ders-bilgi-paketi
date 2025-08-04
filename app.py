from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Veritabanı bağlantı ayarları
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Melek4334',  # MySQL root şifren
    'database': 'ders_bilgi_paketi'
}

# Ana sayfa - Dersleri listeler
@app.route('/')
def index():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dersler")
        dersler = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', dersler=dersler)
    except mysql.connector.Error as err:
        return f"Veritabanı bağlantı hatası: {err}"

# Fakülteleri listeler
@app.route('/fakulteler')
def fakulteleri_goster():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fakulteler")
        fakulteler = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('fakulteler.html', fakulteler=fakulteler)
    except mysql.connector.Error as err:
        return f"Veritabanı bağlantı hatası: {err}"

# Yeni fakülte ekleme sayfası
@app.route('/fakulte-ekle', methods=['GET', 'POST'])
def fakulte_ekle():
    if request.method == 'POST':
        fakulte_adi = request.form['fakulte_adi']
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO fakulteler (fakulte_adi) VALUES (%s)", (fakulte_adi,))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/fakulteler')
        except mysql.connector.Error as err:
            return f"Veritabanı hatası: {err}"
    return render_template('fakulte_ekle.html')

# Bölümleri listeler
@app.route('/bolumler')
def bolumleri_goster():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bolumler.bolum_id, bolumler.bolum_adi, fakulteler.fakulte_adi
            FROM bolumler
            JOIN fakulteler ON bolumler.fakulte_id = fakulteler.fakulte_id
        """)
        bolumler = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('bolumler.html', bolumler=bolumler)
    except mysql.connector.Error as err:
        return f"Veritabanı hatası: {err}"

# Yeni bölüm ekleme sayfası
@app.route('/bolum-ekle', methods=['GET', 'POST'])
def bolum_ekle():
    if request.method == 'POST':
        bolum_adi = request.form['bolum_adi']
        fakulte_id = request.form['fakulte_id']
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bolumler (bolum_adi, fakulte_id) VALUES (%s, %s)", 
                (bolum_adi, fakulte_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/bolumler')
        except mysql.connector.Error as err:
            return f"Veritabanı hatası: {err}"
    else:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT fakulte_id, fakulte_adi FROM fakulteler")
            fakulteler = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('bolum_ekle.html', fakulteler=fakulteler)
        except mysql.connector.Error as err:
            return f"Veritabanı hatası: {err}"

if __name__ == '__main__':
    app.run(debug=True)
