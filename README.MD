# Turkish News Text Topic Extraction System

This project is a comprehensive Natural Language Processing (NLP) system that analyzes Turkish news text entered by the user, performs cumulative inferences across multiple text inputs, collects up-to-date information from the web, and provides LLM-backed summaries.

## Installation and Execution

1. **Install Required Libraries:**
```bash
pip install numpy pandas openpyxl requests beautifulsoup4 groq
```

2. **Train the Model (First Run):**
Before running the system for the first time, the model file must be generated (this process may take 5-10 minutes and will produce the `metin_model.pkl` file):
```bash
python model_egitimi.py
```

3. **Start the Program:**
```bash
python app.py
```

---

## Core Technologies and Architecture

* **Programming Language:** Python 3.x
* **Mathematics & Data:** NumPy (matrix operations), Pandas (data manipulation), Openpyxl (Excel file reading)
* **Database:** SQLite3 (storing analyses and web data)
* **Custom NLP / ML Algorithms (Implemented from Scratch):**
  * TF-IDF Vectorizer (with N-gram support)
  * Multinomial Naive Bayes and Gradient Descent-based Logistic Regression
  * Custom Turkish Tokenizer, Precision/Recall/F1-Score calculations, and K-Fold Cross Validation
* **API and Web Integrations:**
  * **SerpAPI:** Real-time Google search engine access
  * **Groq API (`llama-3.3-70b-versatile`):** Intelligent query generation and web content summarization
  * **BeautifulSoup4 & Requests:** HTML parsing and web scraping

---

## System Features

1. **Text Classification:** Classifies entered Turkish texts into 8 main categories (`ekonomi` [economy], `kültür` [culture], `magazin` [magazine/entertainment], `sağlık` [health], `siyaset` [politics], `spor` [sports], `teknoloji` [technology], `yaşam` [lifestyle]).
2. **Multiple and Cumulative Analysis:** Retains all entered texts in memory throughout the session to detect common/general topics.
3. **Web Search and AI Summarization:** Gathers up-to-date data from the web based on the general topic of the conversation and synthesizes it using the Groq LLM.
4. **High Performance:** Delivers **over 85% Test Accuracy** on models trained with Kaggle datasets (`7allV03.csv`, `news.xls`, `TurkishHeadlines.csv`).

---

## Example Test Sentences

Sample categories you can use to test the system:

* **Economy:** *The exchange rate of the dollar hit a new record today and exceeded 34 liras.*
* **Sports:** *Galatasaray secured crucial 3 points in the derby against Fenerbahçe.*
* **Politics:** *The President announced the new reform package, bringing significant changes.*
* **Technology:** *A new artificial intelligence-powered smartphone model was introduced.*
* **Health:** *The Ministry of Health launched a new vaccination campaign, and the appointment system is active.*
* **Culture:** *The best film award at the national film festival went to a domestic production.*
* **Magazine:** *The famous singer shared the news of their engagement on social media.*
* **Lifestyle:** *Expert advice on healthy eating habits was published.*

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
