import re
from urllib.request import Request, urlopen


def fetch(url):
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8",
    })
    with urlopen(req, timeout=15) as resp:
        ct = resp.headers.get("Content-Type", "")
        charset = "utf-8"
        if "charset=" in ct:
            charset = ct.split("charset=")[-1].split(";")[0].strip() or "utf-8"
        return resp.read(220000).decode(charset, errors="ignore")

urls = [
    "https://support.hp.com/kz-ru/drivers/hp-color-laser-150-printer-series/model/24494353",
    "https://support.hp.com/kz-ru/drivers/hp-color-laser-150a-printer-series",
]

for u in urls:
    print("URL:", u)
    try:
        text = fetch(u)
        m = re.search(r"/drivers/[^\"'\s]+/model/(\d+)", text)
        print("match:", m.group(0) if m else "NONE")
        print("len:", len(text))
    except Exception as e:
        print("error:", e)
    print("-" * 40)
