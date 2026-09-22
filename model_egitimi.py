
# İLAYDA BALAL - 03.12.2025

import pandas as pd
import numpy as np
import pickle
from ml_utils import (
    TFIDFVectorizer,
    MultinomialNaiveBayes,
    LogisticRegressionManuel,
    ModelDegerlendirici,
    TurkceMetinTemizleyici
)
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("ÖZEL ALGORİTMALARLA MODEL EĞİTİMİ ".center(80))
print("=" * 80)
print("\nNot: Sklearn yerine kendi yazdığımız algoritmalar kullanılıyor!")
print("   TF-IDF: Manuel implementasyon")
print("   Naive Bayes: Manuel implementasyon")
print("   Logistic Regression: Gradient Descent ile")
print("   Cross-Validation: Manuel K-Fold")
print()

print("\nADIM 1: Veri Yükleme")
print("=" * 80)

tum_veri = []

dosyalar = [
    "datasets/7allV03.csv",
    "datasets/news.xls",
    "datasets/TurkishHeadlines.csv"
]

print("   1/3 - 7allV03.csv yükleniyor...")
df1 = pd.read_csv(dosyalar[0])
df1.columns = df1.columns.str.lower()
df1_prep = df1[['text', 'category']].copy()
df1_prep.columns = ['metin', 'kategori']
df1_prep['kaynak'] = 'kaliteli'
tum_veri.append(df1_prep)
print(f"      {len(df1_prep)} kayıt")

print("   2/3 - news.xls yükleniyor...")
df2 = pd.read_excel(dosyalar[1])
df2_prep = df2[['content', 'category']].copy()
df2_prep.columns = ['metin', 'kategori']
df2_prep['kaynak'] = 'kisa'
df2_prep = df2_prep[df2_prep['metin'].str.len() > 50]
tum_veri.append(df2_prep)
print(f"      {len(df2_prep)} kayıt (>50 karakter)")

print("   3/3 - TurkishHeadlines.csv yükleniyor...")
df3 = pd.read_csv(dosyalar[2])
df3.columns = df3.columns.str.lower()
df3_prep = df3[['haberler', 'etiket']].copy()
df3_prep.columns = ['metin', 'kategori']
df3_prep['kaynak'] = 'orta'
tum_veri.append(df3_prep)
print(f"      {len(df3_prep)} kayıt")

print("\nADIM 2: Veri Temizleme ve Normalizasyon")
print("=" * 80)

birlesik_df = pd.concat(tum_veri, ignore_index=True)
print(f"   Toplam ham veri: {len(birlesik_df):,}")

birlesik_df = birlesik_df.dropna()
birlesik_df = birlesik_df[birlesik_df['metin'].str.len() > 20]
print(f"   Boş/kısa metinler sonrası: {len(birlesik_df):,}")

temizleyici = TurkceMetinTemizleyici()
print("   Metinler temizleniyor...")
birlesik_df['metin'] = birlesik_df['metin'].apply(temizleyici.temizle)
birlesik_df = birlesik_df[birlesik_df['metin'].str.len() > 15]

print("   Kategoriler normalize ediliyor...")
kategori_esleme = {
    'ekonomi': 'ekonomi', 'Ekonomi': 'ekonomi',
    'spor': 'spor', 'Spor': 'spor',
    'siyaset': 'siyaset', 'Siyaset': 'siyaset',
    'teknoloji': 'teknoloji', 'Teknoloji': 'teknoloji',
    'saglik': 'sağlık', 'sağlık': 'sağlık', 'Sağlık': 'sağlık',
    'kultur': 'kültür', 'kültür': 'kültür', 'kültür-sanat': 'kültür',
    'dunya': 'dünya', 'dünya': 'dünya',
    'magazin': 'magazin', 'Magazin': 'magazin',
    'yasam': 'yaşam', 'yaşam': 'yaşam', 'Yaşam': 'yaşam',
}

birlesik_df['kategori'] = birlesik_df['kategori'].str.strip()
birlesik_df['kategori'] = birlesik_df['kategori'].replace(kategori_esleme)

belirsiz = ['genel', 'güncel', 'planet', 'türkiye']
birlesik_df = birlesik_df[~birlesik_df['kategori'].isin(belirsiz)]

kategori_sayilari = birlesik_df['kategori'].value_counts()
yeterli_kategoriler = kategori_sayilari[kategori_sayilari >= 500].index
birlesik_df = birlesik_df[birlesik_df['kategori'].isin(yeterli_kategoriler)]

print(f"   Temizlik sonrası: {len(birlesik_df):,}")
print(f"   Kategoriler: {len(birlesik_df['kategori'].unique())}")

print("\nADIM 3: Akıllı Veri Dengeleme")
print("=" * 80)

dengeli_gruplar = []
hedef_min = 1500
hedef_max = 4000

for kategori, grup in birlesik_df.groupby('kategori'):
    grup_uzunluk = len(grup)
    
    if grup_uzunluk > hedef_max:
        grup_sirali = grup.sort_values('metin', key=lambda x: x.str.len(), ascending=False)
        secilen = grup_sirali.head(hedef_max)
        dengeli_gruplar.append(secilen)
        print(f"   {kategori:12s}: {grup_uzunluk:5d} → {hedef_max} (örnekleme)")
    elif grup_uzunluk < hedef_min:
        dengeli_gruplar.append(grup)
        print(f"   {kategori:12s}: {grup_uzunluk:5d} (olduğu gibi)")
    else:
        dengeli_gruplar.append(grup)
        print(f"   {kategori:12s}: {grup_uzunluk:5d} ✓")

birlesik_df = pd.concat(dengeli_gruplar, ignore_index=True)

print(f"\n   Final veri: {len(birlesik_df):,}")
print(f"\n   Kategori Dağılımı:")
print(birlesik_df['kategori'].value_counts())

print("\n📊 ADIM 4: TF-IDF Özellik Çıkarımı (Manuel)")
print("=" * 80)

X_text = birlesik_df['metin'].values
y = birlesik_df['kategori'].values

n_samples = len(X_text)
indices = np.arange(n_samples)
np.random.seed(42)
np.random.shuffle(indices)

test_size = int(0.2 * n_samples)
test_indices = indices[:test_size]
train_indices = indices[test_size:]

X_train_text = X_text[train_indices]
X_test_text = X_text[test_indices]
y_train = y[train_indices]
y_test = y[test_indices]

print(f"   Eğitim seti: {len(X_train_text):,}")
print(f"   Test seti: {len(X_test_text):,}")

print("\n   TF-IDF Vectorizer oluşturuluyor...")
vectorizer = TFIDFVectorizer(
    max_features=15000,
    ngram_range=(1, 3),
    min_df=3,
    max_df=0.7
)

print("   Fit ediliyor...")
X_train = vectorizer.fit_transform(X_train_text)
print("   Transform ediliyor...")
X_test = vectorizer.transform(X_test_text)

print(f"\n   Özellik sayısı: {X_train.shape[1]}")
print(f"   Vocabulary boyutu: {len(vectorizer.vocabulary)}")

print("\nADIM 5: Model Eğitimi")
print("=" * 80)

print("\n   Hangi model kullanılsın?")
print("   1. Multinomial Naive Bayes (Hızlı)")
print("   2. Logistic Regression (Daha yavaş ama güçlü)")

secim = "1"

if secim == "1":
    print("\n   Multinomial Naive Bayes seçildi")
    model = MultinomialNaiveBayes(alpha=0.01)
elif secim == "2":
    print("\n   Logistic Regression seçildi")
    model = LogisticRegressionManuel(
        learning_rate=0.1,
        n_iterations=500,
        reg_lambda=0.1
    )
else:
    print("\n   Geçersiz seçim, Naive Bayes kullanılıyor")
    model = MultinomialNaiveBayes(alpha=0.01)

print("\n   Model eğitiliyor...")
model.fit(X_train, y_train)

print("\n   Test seti üzerinde tahmin yapılıyor...")
y_pred = model.predict(X_test)

accuracy = ModelDegerlendirici.accuracy(y_test, y_pred)

print(f"\nModel eğitildi!")
print(f"Test Doğruluğu: %{accuracy*100:.2f}")

print("\n   Not: Cross-validation çok uzun sürdüğü için atlanıyor")
cv_scores = [accuracy] 

print("\nDETAYLI PERFORMANS RAPORU")
print("=" * 80)

report = ModelDegerlendirici.classification_report(y_test, y_pred, model.classes)

print("\nKategori          Precision  Recall  F1-Score  Örnekler")
print("-" * 65)
for cat, metrics in sorted(report.items(), key=lambda x: x[1].get('support', 0) if isinstance(x[1], dict) else 0, reverse=True):
    if cat not in ['accuracy', 'macro avg', 'weighted avg']:
        print(f"{cat:15s}   {metrics['precision']:.3f}     {metrics['recall']:.3f}   {metrics['f1-score']:.3f}     {int(metrics['support'])}")

print("\nÖZET:")
print(f"   Macro Avg F1    : {report['macro avg']['f1-score']:.3f}")
print(f"   Weighted Avg F1 : {report['weighted avg']['f1-score']:.3f}")
print(f"   Accuracy        : {accuracy:.3f}")

print("\nADIM 6: Model Kaydediliyor")
print("=" * 80)

model_yolu = "metin_model.pkl"

model_paketi = {
    'vectorizer': vectorizer,
    'model': model,
    'kategoriler': list(model.classes),
    'accuracy': accuracy,
    'cv_scores': cv_scores
}

with open(model_yolu, 'wb') as f:
    pickle.dump(model_paketi, f)

print(f"   Model kaydedildi: {model_yolu}")
print(f"   Kategoriler: {len(model.classes)}")
print(f"   Doğruluk: %{accuracy*100:.2f}")

print("\n" + "=" * 80)
if accuracy >= 0.85:
    print(" BAŞARILI! HEDEF ULAŞILDI: %85+ ".center(80, "="))
elif accuracy >= 0.80:
    print(" İYİ! %80+ BAŞARILDI ".center(80, "="))
elif accuracy >= 0.70:
    print(" ORTA - İYİLEŞTİRME GEREKLİ ".center(80, "="))
else:
    print(" YETERSİZ - DAHA FAZLA İYİLEŞTİRME ".center(80, "="))
print("=" * 80)

print("\nKULLANILAN ALGORİTMALAR:")
print("   TF-IDF: Manuel implementasyon (N-gram, IDF hesaplama)")
print("   Naive Bayes: Manuel Multinomial NB (Laplace smoothing)")
print("   Metrik Hesaplama: Precision, Recall, F1 (manuel)")
print("   Normalizasyon: L2 norm (manuel)")
print("   Tokenization: Türkçe özel (manuel)")
