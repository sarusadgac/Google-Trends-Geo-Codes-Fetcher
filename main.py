import requests 
import re

# Geo konum bilgisini atom feed linkinden alan fonksiyon
def get_geo_from_pn(pn):
    url = f'https://trends.google.com/trends/hottrends/atom/feed?pn={pn}'
    response = requests.get(url)
    if response.status_code == 200:
        # Atom linkinden geo bilgisini çıkarma
        match = re.search(r'geo=([A-Z]{2})', response.text)
        if match:
            return pn, match.group(1)  # US, IN gibi geo kodlarını döndürür
        else:
            return pn, ''  # Geo bilgisi yoksa boş bırak
    else:
        return pn, 'Error'  # Trend verisi yoksa 'Error' olarak işaretle

# Sonuçları dosyaya yazdırma
with open('found_geo_codes.txt', 'w') as f:
    for i in range(1001):
        pn = f'p{i}'
        pn, geo = get_geo_from_pn(pn)
        if geo != '' and geo != 'Error':
            f.write(f'{pn} belongs to: {geo}\n')
