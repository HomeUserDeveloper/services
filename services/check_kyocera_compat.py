from urllib.request import Request, urlopen

URLS = [
    "https://www.kyoceradocumentsolutions.com/en/products/supplies/TK-1150.html",
    "https://www.kyoceradocumentsolutions.com/en/products/supplies/DK-1150.html",
]

NEEDLES = [
    "P2040dn",
    "P2040dw",
    "P2235dn",
    "P2335dw",
    "PA2000",
    "PA2000W",
    "PA4000x",
]

for url in URLS:
    print("URL:", url)
    try:
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        })
        with urlopen(req, timeout=25) as resp:
            ct = resp.headers.get("Content-Type", "")
            charset = "utf-8"
            if "charset=" in ct:
                charset = ct.split("charset=")[-1].split(";")[0].strip() or "utf-8"
            text = resp.read(400000).decode(charset, errors="ignore")
        print("len=", len(text))
        for needle in NEEDLES:
            if needle.lower() in text.lower():
                print("FOUND", needle)
    except Exception as exc:
        print("ERROR", exc)
    print("-" * 40)
