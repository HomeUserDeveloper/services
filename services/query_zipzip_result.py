import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen

queries = [
    ("TK-1150", {"brand": "Kyocera", "kind": "3", "model": "TK-1150", "descr": "", "pid": ""}),
    ("DK-1150", {"brand": "Kyocera", "kind": "3", "model": "DK-1150", "descr": "", "pid": ""}),
]

for label, params in queries:
    url = "https://zipzip.ru/result/?" + urlencode(params)
    print("\n===", label, "===")
    print(url)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as resp:
        text = resp.read(450000).decode("cp1251", errors="ignore")

    print("has label:", label.lower() in text.lower())

    for pat in [
        r"Совместим(?:ость|ые модели)?[^<]{0,400}",
        r"Применяется[^<]{0,400}",
        r"Подходит[^<]{0,400}",
        r"P\d{4,5}[a-z]{0,2}",
        r"PA\d{4}[A-Za-z]{0,2}",
    ]:
        hits = re.findall(pat, text, flags=re.I)
        if hits:
            print("PATTERN", pat)
            uniq = []
            for h in hits:
                if h not in uniq:
                    uniq.append(h)
            for h in uniq[:50]:
                print(" ", h)

    idx = text.lower().find(label.lower())
    if idx >= 0:
        start = max(0, idx - 4000)
        end = min(len(text), idx + 12000)
        print("SNIPPET_START")
        print(text[start:end])
        print("SNIPPET_END")
