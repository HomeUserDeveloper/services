import re
from urllib.request import Request, urlopen

url = 'https://zipzip.ru/search/'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urlopen(req, timeout=25) as resp:
    text = resp.read(300000).decode('cp1251', errors='ignore')

for pat in [
    r'<form[^>]+action="([^"]+)"[^>]*>(.*?)</form>',
    r'<input[^>]+name="([^"]+)"[^>]*>',
    r'<select[^>]+name="([^"]+)"[^>]*>',
]:
    print('\nPATTERN', pat)
    hits = re.findall(pat, text, flags=re.I | re.S)
    if isinstance(hits, list):
        for h in hits[:20]:
            print(h)

idx = text.lower().find('поиск товаров в прайс-листе')
if idx >= 0:
    print('\nSECTION:')
    print(text[idx:idx+5000])
