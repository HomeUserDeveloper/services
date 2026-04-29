import re
from html import unescape
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand, CommandError

from services.models import Brand, Consumable, ConsumableCompatibility, Part, PartCompatibility, ProductModel


BRAND_RULES = [
    ("CACTUS", [r"\bCACTUS\b", r"\bCS-[A-Z0-9-]+"]),
    ("CET", [r"\bCET\b", r"\bCET[-A-Z0-9]*"]),
    ("ELP", [r"\bELP\b", r"\bELP-[A-Z0-9-]+"]),
    ("FUJI", [r"\bFUJI\b"]),
    ("MASTER", [r"\bMASTER\b"]),
    ("STATIC CONTROL", [r"\bSTATIC\s+CONTROL\b", r"\bSCC\b"]),
    ("DELACAMP", [r"\bDELACAMP\b"]),
    ("HANP", [r"\bHANP\b"]),
    ("NV PRINT", [r"\bNV\s?-?PRINT\b"]),
    ("BULAT", [r"\bBULAT\b"]),
    ("PATRON", [r"\bPATRON\b"]),
    ("HI-BLACK", [r"\bHI-?BLACK\b"]),
    ("G&G", [r"\bG&G\b", r"\bGG\b"]),
    ("ДРУГИЕ", [r"\bДРУГИЕ\b"]),
]


def _clean_html(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", unescape(value))).strip()


def _extract_sku(title: str, description: str) -> str:
    text = f"{title} {description}".upper()
    patterns = [
        r"\b(?:TK|DK|MK|FK|DV|WT|PU|TR)-\d+[A-Z0-9-]*\b",
        r"\b(?:CS|ELP|CET)[-A-Z0-9]+\b",
        r"\b\d[A-Z0-9]{5,}\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return title[:128]


def _detect_brand_name(raw_text: str, fallback_brand_name: str) -> str:
    normalized = f" {raw_text.upper()} "
    for brand_name, patterns in BRAND_RULES:
        for pattern in patterns:
            if re.search(pattern, normalized, re.IGNORECASE):
                return brand_name
    return fallback_brand_name


class Command(BaseCommand):
    help = "Import parts/consumables compatibility from zipzip model page with automatic brand detection"

    def add_arguments(self, parser):
        parser.add_argument(
            "--model",
            required=True,
            help="Exact ProductModel.name value in DB (example: Kyocera ECOSYS P2040dn)",
        )
        parser.add_argument(
            "--url",
            required=True,
            help="zipzip model page URL (example: https://zipzip.ru/price2/?brand=Kyocera&pcl=3056&gr=5&pgsize=0)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Parse and display summary without saving records",
        )

    def handle(self, *args, **options):
        model_name = options["model"].strip()
        source_url = options["url"].strip()
        dry_run = options["dry_run"]

        model = ProductModel.objects.select_related("brand", "category").filter(name=model_name).first()
        if model is None:
            raise CommandError(f"ProductModel not found: {model_name}")

        try:
            request = Request(source_url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(request, timeout=30) as response:
                body = response.read()
        except Exception as exc:
            raise CommandError(f"Cannot fetch URL: {source_url}\n{exc}") from exc

        page_text = body.decode("cp1251", errors="replace")
        rows = re.findall(r"<tr height='50px'>(.*?)</tr>", page_text, re.S)
        if not rows:
            raise CommandError("No table rows found. Check URL and page format.")

        created_consumables = 0
        created_parts = 0
        linked_consumables = 0
        linked_parts = 0
        updated_existing = 0

        for row in rows:
            columns = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            if len(columns) < 4:
                continue

            kind_text = _clean_html(columns[2])
            link_match = re.search(r"<a href='([^']+)'[^>]*>(.*?)</a>(.*)", columns[3], re.S)
            if link_match is None:
                continue

            item_url = urljoin("https://zipzip.ru", link_match.group(1))
            item_title = _clean_html(link_match.group(2))
            item_description = _clean_html(link_match.group(3))
            if not item_title:
                continue

            item_name = f"{item_title} {item_description}".strip() if item_description else item_title
            item_sku = _extract_sku(item_title, item_description)
            detected_brand_name = _detect_brand_name(item_name, model.brand.name if model.brand_id else "")

            brand_obj, _ = Brand.objects.get_or_create(name=detected_brand_name)

            common_fields = {
                "name": item_name,
                "site": item_url,
                "sku": item_sku,
                "category": model.category,
                "brand": brand_obj,
                "device_type": model.device_type,
                "color": model.color,
                "format_print": model.format_print,
                "speed_print": model.speed_print,
            }

            if kind_text.startswith("Расходные материалы"):
                existing = Consumable.objects.filter(site=item_url).first()
                if existing is None:
                    if not dry_run:
                        existing = Consumable.objects.create(**common_fields)
                    created_consumables += 1
                else:
                    changed = False
                    for field_name, field_value in common_fields.items():
                        if getattr(existing, field_name) != field_value:
                            setattr(existing, field_name, field_value)
                            changed = True
                    if changed:
                        updated_existing += 1
                        if not dry_run:
                            existing.save()

                if not dry_run:
                    _, created_link = ConsumableCompatibility.objects.get_or_create(
                        consumable=existing,
                        product_model=model,
                    )
                    if created_link:
                        linked_consumables += 1
                else:
                    linked_consumables += 1

            elif kind_text.startswith("Запчасти"):
                existing = Part.objects.filter(site=item_url).first()
                if existing is None:
                    if not dry_run:
                        existing = Part.objects.create(**common_fields)
                    created_parts += 1
                else:
                    changed = False
                    for field_name, field_value in common_fields.items():
                        if getattr(existing, field_name) != field_value:
                            setattr(existing, field_name, field_value)
                            changed = True
                    if changed:
                        updated_existing += 1
                        if not dry_run:
                            existing.save()

                if not dry_run:
                    _, created_link = PartCompatibility.objects.get_or_create(
                        part=existing,
                        product_model=model,
                    )
                    if created_link:
                        linked_parts += 1
                else:
                    linked_parts += 1

        summary = {
            "model": model.name,
            "dry_run": dry_run,
            "created_consumables": created_consumables,
            "created_parts": created_parts,
            "linked_consumables": linked_consumables,
            "linked_parts": linked_parts,
            "updated_existing": updated_existing,
            "total_consumables_for_model": Consumable.objects.filter(compatibilities__product_model=model).distinct().count(),
            "total_parts_for_model": Part.objects.filter(compatibilities__product_model=model).distinct().count(),
        }
        self.stdout.write(self.style.SUCCESS(str(summary)))