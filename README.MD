
# Türkçe Haber Metni Konu Çıkarım Sistemi

Bu proje; kullanıcının girdiği Türkçe haber metinlerini analiz eden, çoklu girişlerde birikimli çıkarım yapabilen, web'den güncel veri toplayıp LLM destekli özetler sunan kapsamlı bir Doğal Dil İşleme (NLP) sistemidir.

## Kurulum ve Çalıştırma

1. **Gerekli Kütüphanelerin Yüklenmesi:**
```bash
pip install numpy pandas openpyxl requests beautifulsoup4 groq
```

2. **Modelin Eğitilmesi (İlk Çalıştırma):**
Sistemi ilk kez çalıştırmadan önce model dosyası oluşturulmalıdır (bu işlem 5-10 dakika sürebilir ve `metin_model.pkl` dosyasını üretir):
```bash
python model_egitimi.py
```


3. **Programı Başlatma:**
```bash
python app.py
```



---

## Temel Teknolojiler ve Mimari

* **Programlama Dili:** Python 3.x
* **Matematik & Veri:** NumPy (matris işlemleri), Pandas (veri manipülasyonu), Openpyxl (Excel okuma)
* **Veritabanı:** SQLite3 (Analizlerin ve web verilerinin saklanması)
* **Özel NLP / ML Algoritmaları (Sıfırdan Implementasyon):**
* TF-IDF Vectorizer (N-gram desteği ile)
* Multinomial Naive Bayes ve Gradient Descent tabanlı Logistic Regression
* Türkçe Tokenizer, Precision/Recall/F1-Score hesaplama ve K-Fold Cross Validation
* **API ve Web Entegrasyonları:**
* **SerpAPI:** Gerçek zamanlı Google arama motoru erişimi
* **Groq API (`llama-3.3-70b-versatile`):** Akıllı sorgu üretimi ve web içerik özeti
* **BeautifulSoup4 & Requests:** HTML parsing ve web scraping

---

## Sistem Özellikleri

1. **Metin Sınıflandırma:** Girilen Türkçe metinleri 8 ana kategoride (`ekonomi`, `kültür`, `magazin`, `sağlık`, `siyaset`, `spor`, `teknoloji`, `yaşam`) sınıflandırır.
2. **Çoklu ve Birikimli Analiz:** Oturum boyunca girilen tüm metinleri hafızada tutarak ortak/genel konuları tespit eder.
3. **Web Arama ve AI Özetleme:** Sohbetin genel konusuna göre web üzerinden güncel veriler toplar ve Groq LLM ile sentezler.
4. **Yüksek Başarım:** Kaggle veri setleri (7allV03.csv, news.xls, TurkishHeadlines.csv) ile eğitilmiş model üzerinde **%85+ Test Doğruluğu** sunar.

---

## Test Cümleleri Örnekleri

Sistemi test etmek için kullanabileceğiniz örnek kategoriler:

* **Ekonomi:** *Dolar kuru bugün yeni rekor kırdı ve 34 lirayı aştı.*
* **Spor:** *Galatasaray Fenerbahçe derbisinde kritik 3 puanı aldı.*
* **Siyaset:** *Cumhurbaşkanı yeni reform paketini açıkladı, önemli değişiklikler geliyor.*
* **Teknoloji:** *Yapay zeka destekli yeni akıllı telefon modeli tanıtıldı.*
* **Sağlık:** *Sağlık Bakanlığı yeni aşı kampanyasını başlattı, randevu sistemi aktif.*
* **Kültür:** *Ulusal sinema festivalinde en iyi film ödülü yerli yapıma gitti.*
* **Magazin:** *Ünlü şarkıcı sosyal medyadan nişan haberini paylaştı.*
* **Yaşam:** *Sağlıklı beslenme alışkanlıkları için uzman tavsiyeleri açıklandı.*

```

```
