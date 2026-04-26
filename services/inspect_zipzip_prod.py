from urllib.request import Request, urlopen

urls = [
    'https://zipzip.ru/prod/?pid=710363',  # TK-1150 JPN
    'https://zipzip.ru/prod/?pid=892243',  # DK-1150 CET
    'https://zipzip.ru/prod/?pid=766068',  # DK-1150 OEM
]

for url in urls:
    print('\nURL', url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=30) as resp:
        text = resp.read(450000).decode('cp1251', errors='ignore')
    for needle in ['TK-1150', 'DK-1150', 'P2040', 'P2235', 'P2335', 'M2135', 'M2635', 'M2735']:
        if needle.lower() in text.lower():
            print('FOUND', needle)
    low = text.lower()
    for needle in ['tk-1150', 'dk-1150', 'p2040', 'p2235', 'p2335']:
        idx = low.find(needle)
        if idx >= 0:
            start = max(0, idx - 1800)
            end = min(len(text), idx + 4000)
            print('SNIPPET for', needle)
            print(text[start:end])
            print('-' * 80)
            break
