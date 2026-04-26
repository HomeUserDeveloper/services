from urllib.parse import urlencode
from urllib.request import Request, urlopen

queries = ["P2040", "P2335"]
needles = ["TK-1150", "DK-1150", "P2235", "P2040", "P2335"]

for q in queries:
    params = {"brand": "Kyocera", "kind": "3", "model": "", "descr": q, "pid": ""}
    url = "https://zipzip.ru/result/?" + urlencode(params)
    print("\n===", q, "===")
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as resp:
        text = resp.read(500000).decode("cp1251", errors="ignore")
    for needle in needles:
        idx = text.lower().find(needle.lower())
        if idx >= 0:
            print("NEEDLE", needle)
            start = max(0, idx - 1500)
            end = min(len(text), idx + 3500)
            print(text[start:end])
            print("-" * 80)
