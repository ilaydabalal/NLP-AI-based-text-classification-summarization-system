
# İLAYDA BALAL - 06.12.2025

"""
Türkçe Metin Analiz - Veritabanı Yönetim Sistemi
"""
import sqlite3
from datetime import datetime


class DatabaseManager:
    
    def __init__(self, db_path="metin_analiz.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.baglanti_ac()
        self.tablolari_olustur()
        self.last_coklu_id = None
    
    def baglanti_ac(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.conn.text_factory = str
        except sqlite3.Error as e:
            raise
    
    def tablolari_olustur(self):
        try:
            # TEKİL METİN ANALİZLERİ TABLOSU
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tek_metin_analizler (
                    id INTEGER PRIMARY KEY,
                    metin TEXT NOT NULL,
                    kategori TEXT NOT NULL,
                    guven_skoru REAL NOT NULL,
                    guven_yuzdesi TEXT,
                    anahtar_kelimeler TEXT,
                    
                    arama_sorgusu TEXT,
                    
                    genel_bilgi TEXT,
                    
                    kaynak1_baslik TEXT,
                    kaynak1_site TEXT,
                    kaynak1_url TEXT,
                    kaynak1_icerik_ozet TEXT,
                    
                    kaynak2_baslik TEXT,
                    kaynak2_site TEXT,
                    kaynak2_url TEXT,
                    kaynak2_icerik_ozet TEXT,
                    
                    kaynak3_baslik TEXT,
                    kaynak3_site TEXT,
                    kaynak3_url TEXT,
                    kaynak3_icerik_ozet TEXT,
                    
                    kaynak4_baslik TEXT,
                    kaynak4_site TEXT,
                    kaynak4_url TEXT,
                    kaynak4_icerik_ozet TEXT,
                    
                    kaynak5_baslik TEXT,
                    kaynak5_site TEXT,
                    kaynak5_url TEXT,
                    kaynak5_icerik_ozet TEXT,
                    
                    kaynak6_baslik TEXT,
                    kaynak6_site TEXT,
                    kaynak6_url TEXT,
                    kaynak6_icerik_ozet TEXT,
                    
                    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # ÇOKLU METİN ANALİZLERİ TABLOSU
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS coklu_metin_analizler (
                    id INTEGER PRIMARY KEY,
                    
                    ortak_kategori TEXT NOT NULL,
                    metin_sayisi INTEGER,
                    
                    arama_sorgusu TEXT,
                    
                    genel_bilgi TEXT,
                    
                    kaynak1_baslik TEXT,
                    kaynak1_site TEXT,
                    kaynak1_url TEXT,
                    kaynak1_icerik_ozet TEXT,
                    
                    kaynak2_baslik TEXT,
                    kaynak2_site TEXT,
                    kaynak2_url TEXT,
                    kaynak2_icerik_ozet TEXT,
                    
                    kaynak3_baslik TEXT,
                    kaynak3_site TEXT,
                    kaynak3_url TEXT,
                    kaynak3_icerik_ozet TEXT,
                    
                    kaynak4_baslik TEXT,
                    kaynak4_site TEXT,
                    kaynak4_url TEXT,
                    kaynak4_icerik_ozet TEXT,
                    
                    kaynak5_baslik TEXT,
                    kaynak5_site TEXT,
                    kaynak5_url TEXT,
                    kaynak5_icerik_ozet TEXT,
                    
                    kaynak6_baslik TEXT,
                    kaynak6_site TEXT,
                    kaynak6_url TEXT,
                    kaynak6_icerik_ozet TEXT,
                    
                    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_tek_kategori 
                ON tek_metin_analizler(kategori)
            ''')
            
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_tek_tarih 
                ON tek_metin_analizler(kayit_tarihi)
            ''')
            
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_coklu_kategori 
                ON coklu_metin_analizler(ortak_kategori)
            ''')
            
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_coklu_tarih 
                ON coklu_metin_analizler(kayit_tarihi)
            ''')
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            print(f"Tablo oluşturma hatası: {e}")
            raise
    
    def tek_metin_kaydet(self, metin, sonuc, web_bilgi=None):

        try:
            anahtar_kelimeler = ", ".join(sonuc.get('anahtar_kelimeler', []))
            
            guven_skoru = sonuc.get('guven', 0.0)
            guven_yuzdesi = f"%{guven_skoru * 100:.1f}"
            
            # Web bilgilerini hazırla
            arama_sorgusu = ""
            genel_bilgi = ""
            kaynaklar = []
            
            if web_bilgi:
                arama_sorgusu = web_bilgi.get('sorgu', '')
                genel_bilgi = web_bilgi.get('ozet', '')
                kaynaklar = web_bilgi.get('kaynaklar', [])
            
            kaynak_verileri = []
            for i in range(6):
                if i < len(kaynaklar):
                    k = kaynaklar[i]
                    kaynak_verileri.extend([
                        k.get('baslik', ''),
                        k.get('site', ''),
                        k.get('url', ''),
                        k.get('icerik_kisa', k.get('icerik', ''))[:500]
                    ])
                else:
                    kaynak_verileri.extend(['', '', '', ''])
            
            self.cursor.execute('''
                INSERT INTO tek_metin_analizler 
                (metin, kategori, guven_skoru, guven_yuzdesi, anahtar_kelimeler, 
                 arama_sorgusu, genel_bilgi,
                 kaynak1_baslik, kaynak1_site, kaynak1_url, kaynak1_icerik_ozet,
                 kaynak2_baslik, kaynak2_site, kaynak2_url, kaynak2_icerik_ozet,
                 kaynak3_baslik, kaynak3_site, kaynak3_url, kaynak3_icerik_ozet,
                 kaynak4_baslik, kaynak4_site, kaynak4_url, kaynak4_icerik_ozet,
                 kaynak5_baslik, kaynak5_site, kaynak5_url, kaynak5_icerik_ozet,
                 kaynak6_baslik, kaynak6_site, kaynak6_url, kaynak6_icerik_ozet)
                VALUES (?, ?, ?, ?, ?, ?, ?, 
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metin, sonuc['kategori'], guven_skoru, guven_yuzdesi, anahtar_kelimeler,
                arama_sorgusu, genel_bilgi,
                *kaynak_verileri
            ))
            
            self.conn.commit()
            kayit_id = self.cursor.lastrowid
            
            return kayit_id
            
        except sqlite3.Error as e:
            print(f"Kayıt hatası: {e}")
            return None
    
    def coklu_metin_kaydet(self, ortak_sonuc, metin_sayisi, web_bilgi=None):

        try:
            arama_sorgusu = ""
            genel_bilgi = ""
            kaynaklar = []
            
            if web_bilgi:
                arama_sorgusu = web_bilgi.get('sorgu', '')
                genel_bilgi = web_bilgi.get('ozet', '')
                kaynaklar = web_bilgi.get('kaynaklar', [])
            
            kaynak_verileri = []
            for i in range(6):
                if i < len(kaynaklar):
                    k = kaynaklar[i]
                    kaynak_verileri.extend([
                        k.get('baslik', ''),
                        k.get('site', ''),
                        k.get('url', ''),
                        k.get('icerik_kisa', k.get('icerik', ''))[:500]
                    ])
                else:
                    kaynak_verileri.extend(['', '', '', ''])
            
            self.cursor.execute('''
                INSERT INTO coklu_metin_analizler 
                (ortak_kategori, metin_sayisi,
                 arama_sorgusu, genel_bilgi,
                 kaynak1_baslik, kaynak1_site, kaynak1_url, kaynak1_icerik_ozet,
                 kaynak2_baslik, kaynak2_site, kaynak2_url, kaynak2_icerik_ozet,
                 kaynak3_baslik, kaynak3_site, kaynak3_url, kaynak3_icerik_ozet,
                 kaynak4_baslik, kaynak4_site, kaynak4_url, kaynak4_icerik_ozet,
                 kaynak5_baslik, kaynak5_site, kaynak5_url, kaynak5_icerik_ozet,
                 kaynak6_baslik, kaynak6_site, kaynak6_url, kaynak6_icerik_ozet)
                VALUES (?, ?, ?, ?, 
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ortak_sonuc['ortak_kategori'], metin_sayisi,
                arama_sorgusu, genel_bilgi,
                *kaynak_verileri
            ))
            
            self.conn.commit()
            self.last_coklu_id = self.cursor.lastrowid
            kayit_id = self.cursor.lastrowid
            
            return kayit_id
            
        except sqlite3.Error as e:
            print(f"Kayıt hatası: {e}")
            return None
    
    def kategoriye_gore_getir(self, kategori, limit=10):
        try:
            self.cursor.execute('''
                SELECT id, metin, kategori, guven_yuzdesi, anahtar_kelimeler, 
                       arama_sorgusu, kayit_tarihi
                FROM tek_metin_analizler
                WHERE kategori LIKE ?
                ORDER BY kayit_tarihi DESC
                LIMIT ?
            ''', (f'%{kategori}%', limit))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Sorgulama hatası: {e}")
            return []
    
    def son_analizleri_getir(self, limit=10):
        try:
            self.cursor.execute('''
                SELECT id, metin, kategori, guven_yuzdesi, anahtar_kelimeler, 
                       arama_sorgusu, genel_bilgi, kayit_tarihi
                FROM tek_metin_analizler
                ORDER BY kayit_tarihi DESC
                LIMIT ?
            ''', (limit,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Sorgulama hatası: {e}")
            return []
    
    def detayli_analiz_getir(self, analiz_id, analiz_tipi='tek'):
        try:
            if analiz_tipi == 'tek':
                self.cursor.execute('''
                    SELECT * FROM tek_metin_analizler WHERE id = ?
                ''', (analiz_id,))
            else:
                self.cursor.execute('''
                    SELECT * FROM coklu_metin_analizler WHERE id = ?
                ''', (analiz_id,))
            
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Sorgulama hatası: {e}")
            return None
    
    def web_kaynaklarini_getir(self, analiz_id, analiz_tipi='tek'):
        try:
            if analiz_tipi == 'tek':
                tablo = 'tek_metin_analizler'
            else:
                tablo = 'coklu_metin_analizler'
            
            self.cursor.execute(f'''
                SELECT 
                    kaynak1_baslik, kaynak1_site, kaynak1_url,
                    kaynak2_baslik, kaynak2_site, kaynak2_url,
                    kaynak3_baslik, kaynak3_site, kaynak3_url,
                    kaynak4_baslik, kaynak4_site, kaynak4_url,
                    kaynak5_baslik, kaynak5_site, kaynak5_url,
                    kaynak6_baslik, kaynak6_site, kaynak6_url
                FROM {tablo}
                WHERE id = ?
            ''', (analiz_id,))
            
            sonuc = self.cursor.fetchone()
            if not sonuc:
                return []
            
            kaynaklar = []
            for i in range(6):
                idx = i * 3
                if sonuc[idx]:
                    kaynaklar.append({
                        'baslik': sonuc[idx],
                        'site': sonuc[idx + 1],
                        'url': sonuc[idx + 2]
                    })
            
            return kaynaklar
            
        except sqlite3.Error as e:
            print(f"Sorgulama hatası: {e}")
            return []
    
    def istatistikler(self):
        try:
            self.cursor.execute('SELECT COUNT(*) FROM tek_metin_analizler')
            toplam_tek = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM coklu_metin_analizler')
            toplam_coklu = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT AVG(guven_skoru) FROM tek_metin_analizler')
            ortalama_guven = self.cursor.fetchone()[0] or 0
            
            self.cursor.execute('''
                SELECT kategori, COUNT(*) as sayi
                FROM tek_metin_analizler
                GROUP BY kategori
                ORDER BY sayi DESC
                LIMIT 10
            ''')
            kategori_dagilim = self.cursor.fetchall()
            
            return {
                'toplam_tek_analiz': toplam_tek,
                'toplam_coklu_analiz': toplam_coklu,
                'ortalama_guven': f"%{ortalama_guven * 100:.1f}",
                'kategori_dagilim': kategori_dagilim
            }
        except sqlite3.Error as e:
            print(f"İstatistik hatası: {e}")
            return {}
    
    def veritabani_yedekle(self, yedek_dosya=None):
        if not yedek_dosya:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            yedek_dosya = self.db_path.replace('.db', f'_yedek_{timestamp}.db')
        
        try:
            yedek_conn = sqlite3.connect(yedek_dosya)
            self.conn.backup(yedek_conn)
            yedek_conn.close()
            return yedek_dosya
        except sqlite3.Error as e:
            print(f"Yedekleme hatası: {e}")
            return None
    
    def baglanti_kapat(self):
        if self.conn:
            self.conn.close()
