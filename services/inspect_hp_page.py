import re
from urllib.request import Request, urlopen

URLS = [
    "https://support.hp.com/kz-ru/drivers/hp-color-laser-150-printer-series/model/24494353",
    "https://support.hp.com/kz-ru/drivers/hp-color-laserjet-enterprise-m455dn-printer-series",
]


def fetch(url):
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8",
    })
    with urlopen(req, timeout=25) as resp:
        ct = resp.headers.get("Content-Type", "")
        charset = "utf-8"
        if "charset=" in ct:
            charset = ct.split("charset=")[-1].split(";")[0].strip() or "utf-8"
        return resp.read(350000).decode(charset, errors="ignore")


for u in URLS:
    print("\nURL:", u)
    try:
        text = fetch(u)
        print("LEN:", len(text))
        for p in [
            r"wcc-services[^\"'\s]+",
            r"api[^\"'\s]*hp[^\"'\s]*",
            r"model/\d+",
            r"product/details/[^\"'\s]+/model/\d+",
            r"drivers/[^\"'\s]+/model/\d+",
        ]:
            hits = re.findall(p, text)
            if hits:
                uniq = []
                for h in hits:
                    if h not in uniq:
                        uniq.append(h)
                print("PATTERN", p, "HITS", len(uniq))
                for h in uniq[:10]:
                    print("  ", h)
    except Exception as e:
        print("ERROR:", e)
