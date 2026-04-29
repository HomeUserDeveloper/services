import re
from urllib.request import Request, urlopen

URLS = [
    ("TK-1150", "https://zipzip.ru/search/?q=TK-1150"),
    ("DK-1150", "https://zipzip.ru/search/?q=DK-1150"),
]

for label, url in URLS:
    print("\n===", label, "===")
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=25) as resp:
        raw = resp.read(350000)
    text = raw.decode("cp1251", errors="ignore")
    print("has label:", label.lower() in text.lower())

    for pat in [
        r'href="([^"]+)"',
        r'href=([^\s>]+)',
    ]:
        hits = re.findall(pat, text, flags=re.I)
        found = [h for h in hits if label.lower() in h.lower() or 'product' in h.lower() or 'price' in h.lower()]
        if found:
            print("PATTERN", pat)
            for h in found[:30]:
                print(" ", h)

    idx = text.lower().find(label.lower())
    if idx >= 0:
        start = max(0, idx - 2500)
        end = min(len(text), idx + 6000)
        snippet = text[start:end]
        print("SNIPPET_START")
        print(snippet)
        print("SNIPPET_END")
