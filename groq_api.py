
# İLAYDA BALAL - 04.12.2025

import os
from groq import Groq
import requests
from bs4 import BeautifulSoup
import json
import re

class GroqAIAnalizor:
    """Groq API kullanarak web içeriği çekme ve özetleme yapan sınıf."""
    
    GROQ_API_KEY = "" 
    
    def __init__(self, model="llama-3.3-70b-versatile"): 
        try:
            self.client = Groq(api_key=self.GROQ_API_KEY)
            self.model = model
        except Exception as e:
            print(f"Groq API başlatma hatası: {e}")
            self.client = None
            
    def __fetch_web_content(self, url):
        
        if any(keyword in url for keyword in ['youtube.com', '.pdf', 'translate.google.com']):
            return ""

        if re.search(r'\.(jpg|jpeg|png|gif|svg|webp)$', url, re.IGNORECASE):
            return ""

        try:
            response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            
            response.encoding = response.apparent_encoding or 'utf-8'

            if not response.text or len(response.text.strip()) < 50: 
                 return ""

            soup = BeautifulSoup(response.text, 'html.parser') 
            
            for element in soup(["script", "style", "footer", "header", "nav"]):
                element.decompose()
            
            text = soup.get_text()
            
            text = re.sub(r'\s+', ' ', text).strip()
            
            MAX_CHAR_LIMIT = 2500
            if len(text) > MAX_CHAR_LIMIT:
                text = text[:MAX_CHAR_LIMIT] + "..."

            return text
            
        except requests.exceptions.RequestException as e:
            return ""
        except Exception as e:
            return ""

    def sorgu_olustur(self, kategoriler, anahtar_kelimeler, metin_parcasi):

        if not self.client:
            return f"{' '.join(kategoriler)} {' '.join(anahtar_kelimeler)}" 

        
        if len(kategoriler) > 1:
            # ÇOKLU KATEGORİ 
            kategori_listesi_str = " ".join(kategoriler).upper() 
            
            sistem_istemi = (
                "Sen bir Gündem Birleştirme Uzmanısın. Sana verilen hiçbir kategoriyi atlamadan, "
                "HAFIDAZADAKİ BÜTÜN konuları yansıtacak, tek bir arama sorgusu oluştur. "
                f"Sorgun KESİNLİKLE '{kategori_listesi_str}' kategorilerini içermelidir. "
                "Kurallar: 1) Sorgu KESİNLİKLE sadece 5 kelimeden oluşmalıdır. "
                "2) Başka hiçbir metin, açıklama veya noktalama işareti içermemelidir. YALNIZCA 5 kelime."
            )

            kullanici_istemi = (
                f"Kategoriler: {', '.join(kategoriler)}\n"
                f"Metin İçeriği: '{metin_parcasi[:500]}...'\n\n" 
                "Yukarıdaki tüm konuları birleştiren, 5 kelimelik en iyi arama sorgusunu oluştur:"
            )

        else:
            # TEKİL KATEGORİ 
            sistem_istemi = (
                "Sen bir arama sorgusu uzmanısın. Görevin, sana verilen metne ait "
                "en güncel ve alakalı haberi bulacak tek bir arama sorgusu oluşturmaktır. "
                "Kurallar: 1) Sorgu KESİNLİKLE sadece 5 kelimeden oluşmalıdır. "
                "2) Başka hiçbir metin, açıklama veya noktalama işareti içermemelidir. YALNIZCA 5 kelime."
            )

            kullanici_istemi = (
                f"Kategori: {kategoriler[0]}\n"
                f"Anahtar Kelimeler: {', '.join(anahtar_kelimeler)}\n"
                f"Metin Parçası: '{metin_parcasi[:100]}...'\n\n"
                "Bu bilgileri kullanarak, 5 kelimelik en iyi arama sorgusunu oluştur:"
            )
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": sistem_istemi}, 
                    {"role": "user", "content": kullanici_istemi}
                ],
                model=self.model,
                temperature=0.0,
            )
            
            sorgu = chat_completion.choices[0].message.content.strip()
            
            sorgu = sorgu.replace('.', '').replace(',', '').replace('?', '').replace('"', '')
            sorgu_kelimeler = sorgu.split()
            
            if len(sorgu_kelimeler) > 5:
                sorgu = " ".join(sorgu_kelimeler[:5])
                
            return sorgu
            
        except Exception as e:
            print(f"Groq sorgu oluşturma hatası: {e}")
            return f"{' '.join(kategoriler)} {' '.join(anahtar_kelimeler)}"
    
    def analyze(self, metin_konusu, web_sonuclari):

        if not self.client:
            return "Groq API istemcisi başlatılamadı."
        
        kaynak_metinleri = []
        for i, kaynak in enumerate(web_sonuclari, 1):
            url = kaynak.get('url', '')
            
            if any(keyword in url for keyword in ['youtube.com', 'translate.google.com']):
                 icerik = kaynak.get('icerik', kaynak.get('icerik_kisa', 'Metin içeriği çekilemedi.'))
                 kaynak_metinleri.append(
                    f"--- KAYNAK {i} (URL: {url[:50]}...) - SNIPPET KULLANILDI ---\n"
                    f"BAŞLIK: {kaynak.get('baslik', 'Başlık Yok')}\n"
                    f"ÖZET: {icerik}\n"
                )
                 continue

            cekilen_metin = self.__fetch_web_content(url)
            
            if cekilen_metin:
                kaynak_metinleri.append(
                    f"--- KAYNAK {i} (URL: {url[:50]}...) ---\n"
                    f"BAŞLIK: {kaynak.get('baslik', 'Başlık Yok')}\n"
                    f"ÇEKİLEN İÇERİK: {cekilen_metin}\n"
                )
            else:
                 kaynak_metinleri.append(
                    f"--- KAYNAK {i} (URL: {url[:50]}...) - ÇEKİLEMEDİ ---\n"
                    f"BAŞLIK: {kaynak.get('baslik', 'Başlık Yok')}\n"
                    f"ÖZET: {kaynak.get('icerik', 'Metin içeriği çekilemedi.')}\n"
                )
            
        tum_kaynaklar = "\n\n".join(kaynak_metinleri)

        MAX_TOTAL_CONTEXT_CHARS = 10000 
        if len(tum_kaynaklar) > MAX_TOTAL_CONTEXT_CHARS:
             tum_kaynaklar = tum_kaynaklar[:MAX_TOTAL_CONTEXT_CHARS] + "\n\n[... Toplam kaynak metin içeriği kesildi. ...]"

        sistem_istemi = (
            "Sen bir Türkçe Analiz uzmanısın. "
            "Amacın, **yalnızca** sana verilen web kaynaklarının içeriğini dikkatlice incelemek ve "
            "**Kullanıcıya özel** bir bakış açısıyla, tarafsız, bilgilendirici ve derinlemesine bir özet sunmaktır. "
            "YANITINDA, **'{metin_konusu}'** olarak belirtilen tüm konuları (varsa) özetine dahil etmen **ZORUNLUDUR**, web kaynakları yetersiz kalsa bile. "
            "Yanıtın, **tek bir paragrafta, 10 cümleyi aşmayacak şekilde** olmalıdır. "
            "Analizini **yalnızca sana verilen verilerle sınırlı tut** ve asla 'kaynaklara göre' gibi ifadeler kullanma. "
        )
        
        kullanici_istemi = (
            f"Aşağıdaki kaynakları analiz et. Kullanıcıyla olan sohbetin ana konusu: **'{metin_konusu}'**. " 
            "Analizinde, bu konuyla ilgili kaynaklardaki **en önemli gelişmeleri ve ana tartışma noktalarını** "
            "birleştirerek bütünsel bir durum özeti hazırla. Tüm ana konuları özetine dahil ettiğinden emin ol.\n\n"
            "VERİLEN KAYNAKLAR:\n"
            f"{tum_kaynaklar}"
        )
        
        try:
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": sistem_istemi},
                    {"role": "user", "content": kullanici_istemi}
                ],
                model=self.model,
                temperature=0.3, 
            )
            
            response_text = chat_completion.choices[0].message.content
            
            # Encoding sorunlarını temizle
            if isinstance(response_text, bytes):
                response_text = response_text.decode('utf-8', errors='replace')
            
            return response_text
            
        except Exception as e:
            return f"Groq API çağrısı hatası: {e}"