import re
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand

from services.models import ProductModel


def normalize_text(value):
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def fetch_text(url, timeout=8):
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        },
    )
    with urlopen(req, timeout=timeout) as resp:
        content_type = resp.headers.get("Content-Type", "")
        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip() or "utf-8"
        raw = resp.read(250000)
    return raw.decode(charset, errors="ignore")


def hp_slug(model_name):
    raw = (model_name or "").strip()
    if raw.upper().startswith("HP "):
        raw = raw[3:]
    return re.sub(r"[^a-zA-Z0-9]+", "-", raw.lower()).strip("-")


def extract_hp_model_id(page_text):
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


HP_DRIVER_URL_OVERRIDES = {
    "HP Color Laser 150a": "https://support.hp.com/kz-ru/drivers/hp-color-laser-150-printer-series/model/24494353",
    "HP Color LaserJet 150nw": "https://support.hp.com/kz-ru/drivers/hp-color-laser-150-printer-series/model/24494353",
}


def find_hp_driver_url(model_name):
    forced_url = HP_DRIVER_URL_OVERRIDES.get((model_name or "").strip())
    if forced_url:
        return forced_url

    # First build stable drivers URL from model slug.
    slug = hp_slug(model_name)
    if slug:
        base_url = f"https://support.hp.com/kz-ru/drivers/hp-{slug}-printer-series"
        try:
            page = fetch_text(base_url)
            model_id = extract_hp_model_id(page)
            if model_id:
                return f"{base_url}/model/{model_id}"
        except Exception:
            pass

        # Keep stable slug URL if model id is not available.
        return base_url

    # Last fallback: try HP search page.
    q = quote((model_name or "").strip())
    search_url = f"https://support.hp.com/kz-ru/search?q={q}"
    try:
        page = fetch_text(search_url)
        m_abs = re.search(r"https://support\.hp\.com/kz-ru/drivers/[^\"'\s]+/model/\d+", page)
        if m_abs:
            return m_abs.group(0)

        m_rel = re.search(r"/kz-ru/drivers/[^\"'\s]+/model/\d+", page)
        if m_rel:
            return f"https://support.hp.com{m_rel.group(0)}"
    except Exception:
        pass

    return ""


class Command(BaseCommand):
    help = "Populate ProductModel.site with official product pages for supported brands"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", default=False)
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--brand", type=str, default="")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        limit = options["limit"]
        only_brand = options["brand"].strip()

        local_hint = {}
        model_dir = Path("Model")
        if model_dir.exists():
            for md in model_dir.rglob("*.md"):
                try:
                    text = md.read_text(encoding="utf-8")
                except Exception:
                    continue
                m_model = re.search(r"^Model:\s*(.+)$", text, flags=re.MULTILINE)
                m_tag = re.search(r"^#(.+)$", text, flags=re.MULTILINE)
                if m_model and m_tag:
                    local_hint[m_model.group(1).strip()] = m_tag.group(1).strip()

        qs = ProductModel.objects.select_related("brand").filter(site="").exclude(brand__site="")
        if only_brand:
            qs = qs.filter(brand__name=only_brand)
        qs = qs.order_by("id")
        if limit > 0:
            qs = qs[:limit]

        updated = 0
        checked = 0

        for pm in qs:
            checked += 1
            brand_name = (pm.brand.name if pm.brand_id else "").strip()
            chosen = ""

            if brand_name == "HP":
                chosen = find_hp_driver_url(pm.name)

            elif brand_name == "XEROX":
                # Xerox support page for printers
                model_slug = normalize_text(pm.name).replace("xerox", "").strip().lower()
                if model_slug:
                    chosen = f"https://www.xerox.com/en-us/support/printers/{model_slug}"

            elif brand_name == "CANON":
                # Canon support page for printers
                model_slug = normalize_text(pm.name).replace("canon", "").strip().lower()
                if model_slug:
                    chosen = f"https://support.canon.com/en-us/product/{model_slug}"

            elif brand_name == "KYOCERA":
                # Kyocera support page
                model_slug = normalize_text(pm.name).replace("kyocera", "").replace("ecosys", "").strip().lower()
                if model_slug:
                    chosen = f"https://www.kyoceradocumentsolutions.com/en-us/support/product/{model_slug}"

            elif brand_name == "BROTHER":
                # Brother support page
                model_slug = normalize_text(pm.name).replace("brother", "").strip().lower()
                if model_slug:
                    chosen = f"https://support.brother.com/g/s/solution/printers/{model_slug}"

            elif brand_name == "PANTUM":
                # Pantum support page
                model_slug = normalize_text(pm.name).replace("pantum", "").strip().lower()
                if model_slug:
                    chosen = f"https://support.pantum.com/product/{model_slug}"

            elif brand_name == "CACTUS":
                # Cactus support page
                model_slug = normalize_text(pm.name).replace("cactus", "").strip().lower()
                if model_slug:
                    chosen = f"https://www.cactus-russia.ru/products/{model_slug}"

            elif brand_name == "Deli":
                # Deli support page
                model_slug = normalize_text(pm.name).replace("deli", "").replace("laser", "").strip().lower()
                if model_slug:
                    chosen = f"https://www.deliprinttech.com/en/products/{model_slug}"

            elif brand_name == "G&G":
                # G&G support page
                model_slug = normalize_text(pm.name).replace("gg", "").strip().lower()
                if model_slug:
                    chosen = f"https://www.gg.com.cn/en/products/{model_slug}"

            elif brand_name == "OKI":
                # OKI support page
                model_slug = normalize_text(pm.name).replace("oki", "").strip().lower()
                if model_slug:
                    chosen = f"https://www.oki.com/en/support/{model_slug}"

            elif brand_name == "Катюша":
                tag = local_hint.get(pm.name, "")
                part = tag.split("/")[-1].strip().lower() if "/" in tag else ""
                if part:
                    candidate = f"https://katusha-it.ru/products/{part}"
                    try:
                        page = fetch_text(candidate)
                        if normalize_text(pm.name) in normalize_text(page) or part in page.lower():
                            chosen = candidate
                    except Exception:
                        pass

            if chosen:
                if not dry_run:
                    pm.site = chosen
                    pm.save(update_fields=["site"])
                updated += 1
                self.stdout.write(f"filled: {brand_name} / {pm.name} -> {chosen}")

        self.stdout.write(self.style.SUCCESS(f"Done. checked={checked}, updated={updated}, dry_run={dry_run}, brand={only_brand or 'ALL'}"))
