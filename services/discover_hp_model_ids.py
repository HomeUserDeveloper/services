import os
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
import django
django.setup()

from services.models import ProductModel


def fetch_text(url, timeout=12):
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        },
    )
    with urlopen(req, timeout=timeout) as resp:
        content_type = resp.headers.get("Content-Type", "")
        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip() or "utf-8"
        raw = resp.read(500000)
    return raw.decode(charset, errors="ignore")


def hp_slug(model_name):
    raw = (model_name or "").strip()
    if raw.upper().startswith("HP "):
        raw = raw[3:]
    return re.sub(r"[^a-zA-Z0-9]+", "-", raw.lower()).strip("-")


def find_model_id_from_page(page_text):
    patterns = [
        r"/drivers/[^\"'\s]+/model/(\d+)",
        r"/product/details/[^\"'\s]+/model/(\d+)",
        r"/model/(\d+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, page_text)
        if m:
            return m.group(1)
    return ""


hp_models = list(ProductModel.objects.filter(brand__name='HP').values_list('name', flat=True))

print('HP models:', len(hp_models))
found = {}

for name in hp_models:
    model_id = ''
    slug = hp_slug(name)
    base_url = f"https://support.hp.com/kz-ru/drivers/hp-{slug}-printer-series" if slug else ''

    if base_url:
        try:
            page = fetch_text(base_url)
            model_id = find_model_id_from_page(page)
        except Exception:
            pass

    if not model_id:
        try:
            q = quote(name)
            search_url = f"https://support.hp.com/kz-ru/search?q={q}"
            page = fetch_text(search_url)
            model_id = find_model_id_from_page(page)
            if not model_id:
                m = re.search(r"/kz-ru/drivers/([^\"'\s]+)/model/(\d+)", page)
                if m:
                    model_id = m.group(2)
                    base_url = f"https://support.hp.com/kz-ru/drivers/{m.group(1)}"
        except Exception:
            pass

    if model_id and base_url:
        found[name] = f"{base_url}/model/{model_id}"
        print(f"FOUND: {name} -> {found[name]}")
    else:
        print(f"MISS:  {name}")

print('\nFOUND_TOTAL=', len(found))
print('\nOVERRIDES = {')
for k, v in found.items():
    print(f'    "{k}": "{v}",')
print('}')
