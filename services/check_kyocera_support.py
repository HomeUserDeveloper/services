from urllib.request import Request, urlopen

URLS = [
    "https://www.kyoceradocumentsolutions.com/en-us/support/product/p2040dn",
    "https://www.kyoceradocumentsolutions.com/en-us/support/product/p2040dw",
    "https://www.kyoceradocumentsolutions.com/en-us/support/product/p2235dn",
    "https://www.kyoceradocumentsolutions.com/en-us/support/product/p2335dw",
]

NEEDLES = ["TK-1150", "DK-1150", "P2040dn", "P2040dw", "P2235dn", "P2335dw"]

for url in URLS:
    print("URL:", url)
    try:
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9",
        })
        with urlopen(req, timeout=25) as resp:
            ct = resp.headers.get("Content-Type", "")
            charset = "utf-8"
            if "charset=" in ct:
                charset = ct.split("charset=")[-1].split(";")[0].strip() or "utf-8"
            text = resp.read(350000).decode(charset, errors="ignore")
        print("len=", len(text))
        for needle in NEEDLES:
            if needle.lower() in text.lower():
                print("FOUND", needle)
    except Exception as exc:
        print("ERROR", exc)
    print("-" * 40)
