import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Melek4334',
    'database': 'ders_bilgi_paketi'
}

def create_tables():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Fakülteler
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fakulteler (
        fakulte_id INT PRIMARY KEY AUTO_INCREMENT,
        fakulte_adi VARCHAR(100)
    )
    """)

    # Bölümler
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bolumler (
        bolum_id INT PRIMARY KEY AUTO_INCREMENT,
        fakulte_id INT,
        bolum_adi VARCHAR(100),
        bolum_adi_ingilizce VARCHAR(100),
        FOREIGN KEY (fakulte_id) REFERENCES fakulteler(fakulte_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """)

    # Program Bilgisi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS program_bilgisi (
        program_bilgisi_id INT PRIMARY KEY AUTO_INCREMENT,
        bolum_id INT,
        mezuniyet_derecesi VARCHAR(50),
        egitim_seviyesi VARCHAR(50),
        egitim_tipi VARCHAR(50),
        aciklama TEXT,
        FOREIGN KEY (bolum_id) REFERENCES bolumler(bolum_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """)

    # Program Kazanımları
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS program_kazanimlari (
        kazanim_id INT PRIMARY KEY AUTO_INCREMENT,
        bolum_id INT,
        kodu VARCHAR(10),
        aciklama TEXT,
        FOREIGN KEY (bolum_id) REFERENCES bolumler(bolum_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """)

    # Dersler
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dersler (
        ders_id INT PRIMARY KEY AUTO_INCREMENT,
        bolum_id INT,
        ders_kodu VARCHAR(20),
        ders_adi VARCHAR(100),
        donem VARCHAR(10),
        kredi INT,
        ects INT,
        FOREIGN KEY (bolum_id) REFERENCES bolumler(bolum_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """)

    # Kazanım-Ders Matrisi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kazanım_ders_matris (
        matris_id INT PRIMARY KEY AUTO_INCREMENT,
        ders_id INT,
        kazanım_id INT,
        katkı_seviyesi TINYINT CHECK (katkı_seviyesi BETWEEN 0 AND 4),
        FOREIGN KEY (ders_id) REFERENCES dersler(ders_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (kazanım_id) REFERENCES program_kazanimlari(kazanim_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """)

    # Akademik Personel
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS akademik_personel (
        personel_id INT PRIMARY KEY AUTO_INCREMENT,
        bolum_id INT,
        ad_soyad VARCHAR(100),
        unvan VARCHAR(50),
        email VARCHAR(100),
        gorev VARCHAR(100),
        FOREIGN KEY (bolum_id) REFERENCES bolumler(bolum_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tüm tablolar başarıyla oluşturuldu.")

if __name__ == '__main__':
    create_tables()
