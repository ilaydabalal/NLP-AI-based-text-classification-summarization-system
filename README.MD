
KURULUM VE TEST REHBERİ

Programı Başlat
python app.py

Gerekli Kütüphaneler
pip install numpy pandas openpyxl requests beautifulsoup4 groq

Kütüphane Detayları
| Kütüphane | Versiyon | Kullanım Amacı |
|-----------|----------|----------------|
| numpy | ≥1.20.0 | Matris işlemleri, matematiksel hesaplamalar |
| pandas | ≥1.3.0 | Veri manipülasyonu, CSV/Excel okuma |
| openpyxl | ≥3.0.0 | Excel (.xlsx) dosyalarını okuma |
| requests | ≥2.26.0 | HTTP istekleri, API çağrıları |
| beautifulsoup4 | ≥4.10.0 | HTML parsing, web scraping |
| groq | ≥0.4.0 | Groq AI API entegrasyonu |

TEST CÜMLELERİ
Sistemi test etmek için her kategori için 3 örnek cümle:

### 1EKONOMİ
1. Dolar kuru bugün yeni rekor kırdı ve 34 lirayı aştı.
2. Merkez Bankası faiz kararını açıkladı, piyasalar olumlu tepki verdi.
3. Borsa İstanbul yükselişe geçti, yabancı yatırımcı ilgisi arttı.

### 2SPOR
1. Galatasaray Fenerbahçe derbisinde kritik 3 puanı aldı.
2. Milli takım Dünya Kupası elemelerinde önemli bir galibiyet elde etti.
3. Transfer dönemi yaklaşıyor, büyük kulüpler yıldız futbolcu peşinde.

### 3SİYASET
1. Cumhurbaşkanı yeni reform paketini açıkladı, önemli değişiklikler geliyor.
2. Meclis bugün kritik yasa tasarısını görüşecek, muhalefet karşı çıkıyor.
3. Dışişleri Bakanı komşu ülkeyle ikili görüşmeler yaptı.

### 4TEKNOLOJİ
1. Yapay zeka destekli yeni akıllı telefon modeli tanıtıldı.
2. Siber güvenlik uzmanları yeni bir fidye yazılımı tehdidi konusunda uyardı.
3. Elektrikli araç şarj istasyonları yaygınlaşıyor, altyapı güçleniyor.

### 5SAĞLIK
1. Sağlık Bakanlığı yeni aşı kampanyasını başlattı, randevu sistemi aktif.
2. Kalp hastalıklarında erken teşhis için yeni tarama yöntemi geliştirildi.
3. Grip sezonu başladı, uzmanlar aşı olmayı tavsiye ediyor.

### 6KÜLTÜR
1. Ulusal sinema festivalinde en iyi film ödülü yerli yapıma gitti.
2. Dünyaca ünlü müze Türkiye'de sergi açıyor, tarihi eserler gelecek.
3. Ünlü yazar yeni romanını çıkardı, çok satanlar listesinde zirveye yerleşti.

### 7MAGAZİN
1. Ünlü şarkıcı sosyal medyadan nişan haberini paylaştı.
2. Dizi setinde kavga çıktı, iki oyuncu arasında gerginlik yaşandı.
3. Popüler sunucu yeni bir televizyon programına imza attı.

### 8YAŞAM
1. Sağlıklı beslenme alışkanlıkları için uzman tavsiyeleri açıklandı.
2. Evde verimli çalışma için 10 pratik öneri uzmanlardan geldi.
3. Baharda çiçek yetiştirmek isteyenler için püf noktaları paylaşıldı.


ÖNEMLİ NOT

**Model Dosyası**: İlk çalıştırmada `model_egitimi.py` mutlaka çalıştırılmalı
   - Bu işlem 5-10 dakika sürebilir
   - `metin_model.pkl` dosyası oluşturulacak
