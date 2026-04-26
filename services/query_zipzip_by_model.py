import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen

queries = [
    "P2040",
    "P2235",
    "P2335",
    "PA2000",
    "PA4000",
]

for q in queries:
    params = {"brand": "Kyocera", "kind": "3", "model": "", "descr": q, "pid": ""}
    url = "https://zipzip.ru/result/?" + urlencode(params)
    print("\n===", q, "===")
    print(url)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as resp:
        text = resp.read(450000).decode("cp1251", errors="ignore")

    for needle in ["TK-1150", "DK-1150"]:
        if needle.lower() in text.lower():
            print("FOUND", needle)

    idx = text.find("Найдено товаров")
    if idx >= 0:
        print(text[idx:idx+200])

    for needle in ["TK-1150", "DK-1150"]:
        idx = text.lower().find(needle.lower())
        if idx >= 0:
            start = max(0, idx - 1200)
            end = min(len(text), idx + 3000)
            print("SNIPPET", needle)
            print(text[start:end])
            print("ENDSNIPPET")
