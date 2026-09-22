
#İLAYDA BALAL - 03.12.2025

"""
Web Arama ve Bilgi Toplama Modülü
"""

import requests
import json
from datetime import datetime
from collections import Counter
import re


class WebAramaci:    
    def __init__(self, serpapi_key=""):
        self.serpapi_key = serpapi_key
        self.serpapi_url = "https://serpapi.com/search"
    

    def alt_konular_belirle(self, kategori_str, anahtar_kelimeler):

        kategoriler_listesi = [k.strip() for k in kategori_str.replace(',', ' ').replace(' ve ', ' ').split()]
        kategori_birlesik = " ".join(kategoriler_listesi)
        
        oncelikli_kelimeler = [k for k in anahtar_kelimeler if len(k) > 3][:4] 
        
        alt_konular = []
        
        if len(oncelikli_kelimeler) >= 3:
             sorgu_parcasi = f'"{oncelikli_kelimeler[0]} {oncelikli_kelimeler[1]} {oncelikli_kelimeler[2]}"'
             alt_konular.append(f"({kategori_birlesik}) {sorgu_parcasi}")
             
        elif len(oncelikli_kelimeler) >= 2:
             alt_konular.append(f"({kategoriler_listesi[0]}) \"{oncelikli_kelimeler[0]} {oncelikli_kelimeler[1]}\"")
        
        else:
            alt_konular.append(kategori_birlesik)
            
        return [alt_konular[0]]

    
    def serpapi_search(self, query):
        """SerpAPI ile GERÇEK Google araması"""
        try:
            params = {
                "q": query,
                "location": "Turkey",
                "hl": "tr",
                "gl": "tr",
                "api_key": self.serpapi_key,
                "num": 6  
            }
            
            response = requests.get(self.serpapi_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                if 'organic_results' in data:
                    for item in data['organic_results'][:6]:  
                        try:
                            url = item.get('link', '')
                            if url:
                                site = url.split('/')[2].replace('www.', '')
                            else:
                                site = 'Bilinmeyen'
                            
                            icerik = item.get('snippet', 'İçerik yok')
                            
                            # Encoding temizleme
                            if isinstance(icerik, bytes):
                                icerik = icerik.decode('utf-8', errors='replace')
                            
                            icerik_kisa = icerik[:200] + "..." if len(icerik) > 200 else icerik
                            
                            baslik = item.get('title', 'Başlık yok')
                            if isinstance(baslik, bytes):
                                baslik = baslik.decode('utf-8', errors='replace')
                            
                            results.append({
                                'baslik': baslik,
                                'icerik': icerik, 
                                'icerik_kisa': icerik_kisa, 
                                'site': site,
                                'url': url,
                                'tarih': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                        except Exception as e:
                            continue
                
                return results
            else:
                return []
                
        except Exception as e:
            return []

    def bilgi_topla(self, metin, kategori, anahtar_kelimeler, is_groq_sorgu=False):

        if is_groq_sorgu:
            birlesik_sorgu = metin
        else:
            alt_konular = self.alt_konular_belirle(kategori, anahtar_kelimeler)
            
            if not alt_konular:
                return {
                    'basarili': False,
                    'sorgu': kategori,
                    'kaynaklar': []
                }
            
            birlesik_sorgu = " OR ".join(alt_konular)
        
        tum_kaynaklar = self.serpapi_search(birlesik_sorgu)
        
        if not tum_kaynaklar:
            return {
                'basarili': False,
                'sorgu': birlesik_sorgu,
                'kaynaklar': []
            }
                
        return {
            'basarili': True,
            'sorgu': birlesik_sorgu, 
            'kaynaklar': tum_kaynaklar,
            'kaynak_sayisi': len(tum_kaynaklar)
        }