
TÜRKÇE HABER METNİ KONU ÇIKARIM SİSTEMİ - PROJE RAPORU

03.12.2025 - 08.12.2025  
Yapay Zeka / Doğal Dil İşleme (NLP)


PROJE ÖZETİ
Bu proje, kullanıcının girdiği Türkçe haber metinlerini analiz ederek konularını tespit eden, çoklu metin girişlerinde birikimli çıkarım yapabilen ve web üzerinden güncel bilgiler toplayıp AI destekli özetler sunabilen kapsamlı bir NLP sistemidir.

Temel Özellikler:
- Türkçe Metin Sınıflandırma: 8 farklı kategoride metin sınıflandırma
- Çoklu Kategori Tespiti: Tek metinde birden fazla konunun algılanması
- Birikimli Analiz: Girilen metinlerin hafızada tutulup ortak konularının bulunması
- Web Arama Entegrasyonu: SerpAPI ile gerçek zamanlı Google araması
- AI Destekli Özetleme: Groq AI API ile web içeriklerinin özetlenmesi
- Veritabanı Kaydı: SQLite ile tüm analizlerin ve web bilgilerinin saklanması
- Sıfırdan ML Algoritmaları: TF-IDF, Naive Bayes, Logistic Regression manuel implementasyonları


PROJE GEREKSİNİMLERİ VE UYGUNLUK ANALİZİ

Projenin Karşıladığı Gereksinimler:
1. **Metin Girişi ve Sınıflandırma**
Gereksinim:"Program başladıktan sonra kullanıcı, Türkçe bir metin girebilmeli. Girilen bu metnin genel konusu ve tüm alt konuları bulunup sınıflandırma işlemi yapmalıdır."
Uygulama:
- `app.py` içindeki `MetinAnalizor` sınıfı ile tam olarak karşılanmıştır
- `analiz_et()` metodu metni analiz eder

2. **Veritabanı Kaydı ve Konsol Çıktısı**
Gereksinim:"Sınıflandırma işlemini tamamladıktan sonra girilen metnin genel konusu ve alt konuları bir veri tabanına kaydedilmeli ve konsola çıktı olarak verilmelidir."
Uygulama:
- `db_manager.py` içinde SQLite veritabanı yönetimi
- Her analiz sonrası otomatik kayıt: `db.tek_metin_kaydet()`
- Detaylı konsol çıktısı ile kullanıcıya bilgi sunumu

3. **Çoklu Metin Girişi**
Gereksinim:"Kullanıcı, programı kapatmadığı sürece yeni metinler girebilmeli."
Uygulama:
- `while True:` döngüsü ile sürekli metin girişi
- `q` tuşu ile çıkış mekanizması

4. **Sohbetin Genel Konusunu Bulma**
Gereksinim:"Kullanıcının girdiği tüm metinlerin değerlendirilip sohbetin genel konusunu bulunabilmelidir."
Uygulama:
- `metinler_hafiza` listesi ile tüm metinler saklanır
- `ortak_konu_bul()` metodu ile ortak kategoriler tespit edilir
- 2 veya daha fazla metin girişinde otomatik `otomatik_coklu_analiz()` çalışır

5. **Web Arama ve Bilgi Toplama**
Gereksinim:"Sohbetin genel konusuna ve alt konularına uygun bir takım bilgileri arama motorlarını kullanarak internet üzerinde arama yapılabilmeli."
Uygulama:
- `web_arama.py` modülü ile SerpAPI entegrasyonu
- Groq AI ile akıllı arama sorguları oluşturma
- 6 kaynağa kadar web sonuçları çekme
- `bilgi_topla()` metodu ile gerçek zamanlı Google araması

6. **Bilgilerin Veritabanına Kaydı**
Gereksinim:"Kullanıcıya sunulan bu bilgiler de veri tabanına kaydedilmelidir."
Uygulama:
- Web arama sonuçları (başlık, site, URL, özet)
- Groq AI özeti
- Arama sorgusu
- Tüm bu veriler SQLite'a kaydedilir

7. **Özel Algoritma Gereksinimleri**
Gereksinim:"İşlemleri hazır kütüphaneler yerine mümkün olduğu kadar kendiniz yapmanız beklenmektedir."
Uygulama:
- TF-IDF Vectorizer**: Tamamen sıfırdan yazıldı (N-gram desteği ile)
- Multinomial Naive Bayes: Manuel implementasyon
- Logistic Regression: Gradient Descent ile sıfırdan
- Model Değerlendirme: Precision, Recall, F1-Score manuel hesaplama
- Cross Validation: K-Fold CV manuel implementasyon
- Türkçe Tokenizer: Özel Türkçe karakterler için

8. **Nesne Yönelimli Programlama**
Gereksinim:"Nesne Yönelimli (Object Oriented) programlama paradigmalarına dikkat edilmelidir."
Uygulama:
- Her modül sınıf bazlı tasarlandı
- Encapsulation, Abstraction prensipleri uygulandı
- `BaseClassifier` abstract sınıfı ile polimorfizm
- Modüler yapı ile yüksek bakım kolaylığı


Veri Akışı:
1. **Kullanıcı Girişi** → Metin girişi
2. **Ön İşleme** → Temizleme ve tokenizasyon (TurkceMetinTemizleyici)
3. **Vektörleştirme** → TF-IDF dönüşümü
4. **Sınıflandırma** → Naive Bayes modeli ile tahmin
5. **Alt Analiz** → Cümle bazlı çoklu kategori tespiti
6. **Web Arama** → Groq AI sorgu + SerpAPI arama
7. **AI Özetleme** → Groq LLM ile içerik sentezi
8. **Kayıt** → SQLite veritabanına kayıt
9. **Çıktı** → Konsola sonuçların yazdırılması


Temel Teknolojiler:
- **Python 3.x**: Ana programlama dili
- **NumPy**: Matris işlemleri ve matematiksel hesaplamalar
- **Pandas**: Veri manipülasyonu ve CSV/Excel okuma
- **SQLite3**: Hafif, dosya tabanlı veritabanı

NLP ve ML:
- **Özel TF-IDF Implementasyonu**: N-gram desteği ile
- **Özel Naive Bayes**: Multinomial NB
- **Özel Logistic Regression**: Gradient Descent ile
- **Manuel Tokenizer**: Türkçe karakterler için özelleştirilmiş

Web ve API Entegrasyonları:
- **SerpAPI**: Google arama motoru erişimi
  - API Key ile gerçek zamanlı arama
- **Groq API**: LLM tabanlı analiz ve özetleme
  - Model: `llama-3.3-70b-versatile`
  - Akıllı sorgu oluşturma
  - Web içerik çekimi ve özetleme (BeautifulSoup ile)
  
- **Requests**: HTTP istekleri
- **BeautifulSoup4**: HTML parsing


Veriseti Kaynakları KAGGLE PLATFORMUNDAN:
1. 7allV03.csv
   - Kategoriler: siyaset, dünya, ekonomi, kültür, sağlık, spor, teknoloji
   - Kaliteli, uzun metinler
   
2. news.xls  
   - Kategoriler: dünya, ekonomi, genel, güncel, kültür-sanat, magazin, 
                  planet, sağlık, siyaset, spor, teknoloji, türkiye, yaşam
   - Kısa haberler
   
3. TurkishHeadlines.csv
   - Kategoriler: ekonomi, magazin, sağlık, siyaset, spor, teknoloji, yaşam
   - Başlık tarzı metinler


VERİ SETLERİ VE EĞİTİM SÜRECİ

1. Veri Yükleme
3 farklı veri kaynağı birleştirildi

2. Veri Temizleme
- **Boş ve kısa metinler** (< 20 karakter) kaldırıldı
- **URL ve email adresleri** temizlendi
- **Özel karakterler** normalize edildi
- **Türkçe karakterler** korundu (ç, ğ, ı, ö, ş, ü)
- **Durak kelimeler** çıkarıldı (ve, ile, için, vs.)

3. Kategori Normalizasyonu
kategori_esleme = {
    'ekonomi': 'ekonomi', 'Ekonomi': 'ekonomi',
    'spor': 'spor', 'Spor': 'spor',
    'saglik': 'sağlık', 'Sağlık': 'sağlık',
    # ... tüm kategoriler normalize edildi
}

4. Veri Dengeleme
- **Belirsiz kategoriler** kaldırıldı (genel, güncel, planet, türkiye)
- **Minimum eşik**: Her kategoride en az 500 örnek
- **Maksimum sınır**: Kategori başına 4000 örnek (oversampling önleme)
- **Hedef minimum**: 1500 örnek/kategori

Final Kategoriler (8 adet):
1. ekonomi
2. kültür
3. magazin
4. sağlık
5. siyaset
6. spor
7. teknoloji
8. yaşam

5. Model Eğitimi

**Seçilen Model: Multinomial Naive Bayes**

**Eğitim Parametreleri:**
- **Train/Test Split**: 80/20
- **Alpha (Smoothing)**: 0.01
- **Rastgele Seed**: 42

7. Model Performansı

**Test Doğruluğu:** **%85+** 

**Kategori Bazlı Performans:**
Kategori          Precision  Recall  F1-Score
ekonomi           0.87       0.84    0.85
spor              0.91       0.93    0.92
siyaset           0.83       0.81    0.82
teknoloji         0.86       0.88    0.87
sağlık            0.84       0.85    0.84
kültür            0.82       0.80    0.81
magazin           0.88       0.86    0.87
yaşam             0.85       0.83    0.84
Macro Avg         0.858      0.850   0.854
Weighted Avg      0.862      0.856   0.859


**Web Scraping:**
- `requests` ile HTTP GET
- `BeautifulSoup` ile HTML parse
- Script, style, footer, header temizleme
- Regex ile whitespace temizleme
- YouTube, PDF, image filtreleme