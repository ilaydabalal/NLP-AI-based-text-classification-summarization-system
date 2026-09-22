
# İLAYDA BALAL - 03.12.2025

"""
Türkçe Metin Sınıflandırma - Ana Kullanım Scripti
"""
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pickle
import re
import numpy as np
from collections import Counter
from db_manager import DatabaseManager
from ml_utils import TurkceMetinTemizleyici 
from web_arama import WebAramaci 
from groq_api import GroqAIAnalizor 

class MetinAnalizor:
    def __init__(self, model_dosyasi="metin_model.pkl"):
        try:
            with open(model_dosyasi, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.kategoriler = data['kategoriler']
                self.accuracy = data.get('accuracy', 0)
                self.vectorizer = data.get('vectorizer') 
                
        except FileNotFoundError:
            print(f"Hata: Model dosyası bulunamadı: {model_dosyasi}")
            exit(1)
        except Exception as e:
            print(f"Hata: Model yüklenirken bir sorun oluştu: {e}")
            exit(1)
        
        self.temizleyici = TurkceMetinTemizleyici()

    def metin_temizle(self, metin):
        metin = metin.lower()
        metin = re.sub(r'[^\w\sçğıöşüÇĞİÖŞÜ]', ' ', metin)
        metin = re.sub(r'\s+', ' ', metin)
        return metin.strip()
    
    def analiz_et(self, metin):

        temiz_metin = self.metin_temizle(metin)
        if not temiz_metin or len(temiz_metin) < 3:
            return {'kategori': 'belirsiz', 'guven': 0.0, 'anahtar_kelimeler': [], 'coklu_kategori': False}
        
        is_pipeline = hasattr(self.model, 'named_steps')
        
        try:
            if is_pipeline:
                tahmin_tum = self.model.predict([temiz_metin])[0]
                olasiliklar_tum = self.model.predict_proba([temiz_metin])[0]
            elif self.vectorizer:
                X_tum = self.vectorizer.transform([temiz_metin])
                tahmin_tum = self.model.predict(X_tum)[0]
                olasiliklar_tum = self.model.predict_proba(X_tum)[0]
            else:
                raise ValueError("Model ve/veya Vektörleştirici tanımlı değil.")

            model_classes = self.model.classes_ if hasattr(self.model, 'classes_') else self.kategoriler
            guven_tum = float(olasiliklar_tum[list(model_classes).index(tahmin_tum)])
            
        except Exception as e:
            print(f"Tahmin sırasında hata: {e}")
            return {'kategori': 'hata', 'guven': 0.0, 'anahtar_kelimeler': [], 'coklu_kategori': False}
        
        tokenler = self.temizleyici.tokenize(metin)
        tokenler_temiz = self.temizleyici.durak_kelime_cikar(tokenler)
        
        frekanslar = Counter(tokenler_temiz)
        
        anahtar_kelimeler = [k for k, v in frekanslar.most_common() if len(k) > 3][:5]

        cumleler = [c.strip() for c in metin.replace('!', '.').replace('?', '.').split('.') if len(c.strip()) > 10]
        c_kategoriler = [] 
        c_guvenler = []
        
        if len(cumleler) > 1:
            for cumle in cumleler:
                if len(cumle.strip()) < 10: continue
                try:
                    if is_pipeline:
                        tahmin = self.model.predict([cumle])[0]
                        olasiliklar = self.model.predict_proba([cumle])[0]
                    elif self.vectorizer:
                        X_cumle = self.vectorizer.transform([cumle])
                        tahmin = self.model.predict(X_cumle)[0]
                        olasiliklar = self.model.predict_proba(X_cumle)[0]
                        
                    guven = float(olasiliklar[list(model_classes).index(tahmin)])
                    
                    if guven > 0.40 and tahmin != tahmin_tum and tahmin not in c_kategoriler:
                        c_kategoriler.append(tahmin)
                        c_guvenler.append(guven)
                except:
                    continue
        
        if c_kategoriler:
            tum_kategoriler = [tahmin_tum] + c_kategoriler
            tum_guvenler = [guven_tum] + c_guvenler
            
            birlesik_kategori = tahmin_tum
            if c_kategoriler:
                birlesik_kategori += ", " + ", ".join(c_kategoriler)
                
            return { 
                'kategori': birlesik_kategori, 
                'coklu_kategori': True, 
                'anahtar_kelimeler': anahtar_kelimeler,
                'guven': np.mean(tum_guvenler),
                'alt_kategoriler': c_kategoriler,
                'guvenler': tum_guvenler
            }
        
        return { 
            'kategori': tahmin_tum, 
            'guven': guven_tum, 
            'anahtar_kelimeler': anahtar_kelimeler, 
            'coklu_kategori': False 
        }
    
    def ortak_konu_bul(self, metinler):
        sonuclar = [self.analiz_et(m) for m in metinler]
        
        tum_benzersiz_kategoriler = set()
        for s in sonuclar:
            parcalar = [k.strip() for k in s['kategori'].split(',')]
            tum_benzersiz_kategoriler.update(parcalar)
        
        benzersiz_kategoriler = sorted(list(tum_benzersiz_kategoriler))
        
        tum_kelime_listeleri = [s['anahtar_kelimeler'] for s in sonuclar]
        tum_kelimeler = sum(tum_kelime_listeleri, [])
        
        kelime_sayilari = Counter(tum_kelimeler)
        
        ortak_kelimeler_listesi = [
            kelime for kelime, sayi in kelime_sayilari.most_common() 
            if sum(1 for kelime_listesi in tum_kelime_listeleri if kelime in kelime_listesi) >= 2
        ][:5]

        ortak_kategori_str = ", ".join(benzersiz_kategoriler)
        
        if ortak_kelimeler_listesi:
            ortak_konu_baslik = f"{ortak_kategori_str} ({' '.join(ortak_kelimeler_listesi[:3])})"
        else:
            ortak_konu_baslik = ortak_kategori_str
        
        return {
            'ortak_konu': ortak_konu_baslik,
            'ortak_kategori': ortak_kategori_str,
            'benzersiz_kategoriler': benzersiz_kategoriler,
            'ortak_kelimeler': ortak_kelimeler_listesi,
            'aciklama': f"Girilen metinler '{ortak_kategori_str}' konusunda birleşiyor."
        }

def otomatik_coklu_analiz(analizor, db, web_arama, groq_analizor, metinler_hafiza):
    
    metinler = [m['metin'] for m in metinler_hafiza]
    ortak = analizor.ortak_konu_bul(metinler)
    
    if not ortak['ortak_kelimeler']:
        tum_kelimeler = sum([analizor.analiz_et(m)['anahtar_kelimeler'] for m in metinler], [])
        kelime_sayilari = Counter(tum_kelimeler)
        
        ortak_kelime_listesi_yedek = [k for k, v in kelime_sayilari.most_common(4) if len(k) > 3]
        
        if ortak_kelime_listesi_yedek:
            ortak['ortak_kelimeler'] = ortak_kelime_listesi_yedek
            ortak['ortak_konu'] = f"{ortak['ortak_kategori']} ({' '.join(ortak_kelime_listesi_yedek)})"
            
    
    birlesik_metin = " ".join(metinler)
    
    groq_sorgu = groq_analizor.sorgu_olustur(
        ortak['benzersiz_kategoriler'], 
        ortak['ortak_kelimeler'],
        birlesik_metin
    )
    
    web_bilgi = web_arama.bilgi_topla(
        groq_sorgu, 
        ortak['ortak_kategori'], 
        ortak['ortak_kelimeler'],
        is_groq_sorgu=True
    )
    
    
    print("\n" + "-" * 40)
    print("BİRİKİMLİ ÇIKARIM ANALİZİ")
    print("-" * 40)

    print(f"Kategoriler: {ortak['ortak_kategori']}")
    
    if web_bilgi.get('basarili'):
        sorgu_kelimeleri = groq_sorgu
        print(f"\nWeb'de Aranıyor... Arama Sorgusu: {sorgu_kelimeleri}")
    else:
        print("Arama sorgusu oluşturulamadı.")


    groq_ozet = "Groq analizi başarısız oldu veya kaynak çekilemedi."
    if web_bilgi and web_bilgi.get('basarili'):
        kaynaklar = web_bilgi.get('kaynaklar', []) 
        birlesik_metin_kisa = birlesik_metin[:500] if len(birlesik_metin) > 500 else birlesik_metin
        
        kisa_kaynaklar = [{
            'baslik': k.get('baslik', 'Başlık yok'), 
            'icerik': k.get('icerik_kisa', k.get('icerik', 'İçerik yok')), 
            'site': k.get('site', 'Bilinmeyen'),
            'url': k.get('url', '') 
        } for k in kaynaklar]
        
        groq_ozet = groq_analizor.analyze(groq_sorgu, kisa_kaynaklar)
        
        print("\n" + "-" * 40)
        print(" GENEL BİLGİ ")
        print("-" * 40)
        
        print(groq_ozet)
        
    else:
        print("\n Web bilgisi alınamadı")
        print(f" Groq Özeti: {groq_ozet}")
    
    metin_sayisi = len(metinler_hafiza)
    web_bilgi['ozet'] = groq_ozet
    web_bilgi['sorgu'] = groq_sorgu 
    db.coklu_metin_kaydet(ortak, metin_sayisi, web_bilgi)

def main():
    
    print("═" * 80)
    print(" TÜRKÇE METİN KONU ÇIKARIM SİSTEMİ".center(80, " "))
    print("═" * 80)
    
    analizor = MetinAnalizor()
    db = DatabaseManager()
    SERPAPI_KEY = ""
    web_arama = WebAramaci(SERPAPI_KEY)
    groq_analizor = GroqAIAnalizor()
    
    metinler_hafiza = []
    
    while True:
            
        metin = input("\n  Metni girin (çıkmak için q): ").strip()

        if metin.lower() == 'q':
            print("GÖRÜŞMEK ÜZERE! ".center(80, " "))
            db.baglanti_kapat()
            break
            
        if not metin:
            print("Boş metin girildi!")
            continue
        
        sonuc = analizor.analiz_et(metin)
        
        print("\n" + "-" * 40)
        print("METİN ANALİZ SONUCU")
        print("-" * 40)
        
        kategori_str = sonuc['kategori']
        print(f"Kategori: {kategori_str}") 
        
        if sonuc.get('coklu_kategori', False):
            print(f"Alt Kategoriler: {', '.join(sonuc.get('alt_kategoriler', []))}")
            print(f"Ortalama Güven: %{sonuc['guven']*100:.1f}")
        else:
            print(f"Güven: %{sonuc['guven']*100:.1f}")
            
        tekil_groq_sorgu = groq_analizor.sorgu_olustur(
            [k.strip() for k in sonuc['kategori'].split(',')], 
            sonuc['anahtar_kelimeler'],
            metin
        )
        
        web_bilgi = web_arama.bilgi_topla(
            tekil_groq_sorgu, 
            sonuc['kategori'], 
            sonuc['anahtar_kelimeler'],
            is_groq_sorgu=True 
        )
     
        if len(metinler_hafiza) == 0: 
            
            visible_sorgu = tekil_groq_sorgu 
            
            print(f"\nWeb'de Aranıyor... Arama Sorgusu: {visible_sorgu}")
            
            if web_bilgi.get('basarili'):
                kaynaklar = web_bilgi.get('kaynaklar', [])
                kisa_kaynaklar = [{
                    'baslik': k.get('baslik', 'Başlık yok'), 
                    'icerik': k.get('icerik_kisa', k.get('icerik', 'İçerik yok')), 
                    'site': k.get('site', 'Bilinmeyen'),
                    'url': k.get('url', '')
                } for k in kaynaklar]
                
                try:
                    groq_ozet = groq_analizor.analyze(tekil_groq_sorgu, kisa_kaynaklar)
                    
                    if isinstance(groq_ozet, bytes):
                        groq_ozet = groq_ozet.decode('utf-8', errors='replace')
                    
                    print("\n" + "-" * 40)
                    print(" GENEL BİLGİ ")
                    print("-" * 40)
                    print(groq_ozet)
                except Exception as e:
                    print(f"\nGroq analizi sırasında hata: {e}")
                    groq_ozet = "Analiz yapılamadı"
            
                web_bilgi['ozet'] = groq_ozet
            else:
                web_bilgi['ozet'] = ""

        else:
            web_bilgi['ozet'] = "" 
            
        web_bilgi['sorgu'] = tekil_groq_sorgu 

        kayit_id = db.tek_metin_kaydet(metin, sonuc, web_bilgi)
        
        metinler_hafiza.append({
            'metin': metin,
            'kategori': sonuc['kategori'],
            'anahtar_kelimeler': sonuc['anahtar_kelimeler'],
            'db_id': kayit_id,
            'birlesik_sorgu': web_bilgi.get('sorgu', '')
        })
                
        if len(metinler_hafiza) >= 2:
            otomatik_coklu_analiz(analizor, db, web_arama, groq_analizor, metinler_hafiza)


if __name__ == "__main__":
    main()

