"""
Management command: import_product_models

Reads *.md files from a folder (default: D:/proj/services/Model).
Each subfolder name is treated as a brand name.
Each file contains YAML front matter with:
  Model:      -> name
  ModelType:  -> device_type, color, format_print
  SpeedPrint: -> speed_print
  uid:        -> skipped (we use Django's auto id)

Usage:
  python manage.py import_product_models
  python manage.py import_product_models --path "D:/my/Model" --update
"""

import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from services.models import Brand, ProductModel


def _parse_front_matter(text: str) -> dict:
    """Extract YAML-like front matter between first pair of --- markers."""
    lines = text.splitlines()
    # Find opening ---
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            start = i
            break
    if start is None:
        return {}
    # Find closing ---
    end = None
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}

    data = {}
    current_key = None
    for line in lines[start + 1:end]:
        if not line.strip():
            continue
        # List item
        if line.startswith("  - "):
            if current_key == "ModelType":
                data.setdefault("ModelType", []).append(line[4:].strip())
            continue
        # Key: value
        m = re.match(r"^(\w+):\s*(.*)", line)
        if m:
            current_key = m.group(1)
            value = m.group(2).strip()
            if value:
                data[current_key] = value
            # else: list follows
    return data


def _extract_attributes(model_types: list[str]) -> tuple[str, str, str]:
    """Return (device_type, color, format_print) from ModelType list."""
    types_set = set(model_types)

    # Device type
    device_type = ""
    for candidate in ("МФУ", "Принтер", "Сканер", "Копир"):
        if candidate in types_set:
            device_type = candidate
            break

    # Color
    color = ""
    if "цветной" in types_set:
        color = "цветной"
    elif "черно-белый" in types_set:
        color = "черно-белый"

    # Format — normalise both ASCII and Cyrillic А
    format_print = ""
    for t in model_types:
        normalized = t.replace("\u0410", "A").replace("\u0430", "a")  # Cyrillic А/а -> ASCII
        if normalized in ("A3", "A4"):
            format_print = normalized
            break

    return device_type, color, format_print


class Command(BaseCommand):
    help = "Import product models from *.md files organised by brand folders"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default=r"D:\proj\services\Model",
            help="Root folder containing brand subfolders with *.md files",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            default=False,
            help="Update existing records (matched by name + brand) instead of skipping",
        )

    def handle(self, *args, **options):
        root = Path(options["path"])
        if not root.is_dir():
            raise CommandError(f"Directory not found: {root}")

        do_update = options["update"]

        # Cache brands by uppercase name for case-insensitive lookup
        brand_cache: dict[str, Brand] = {b.name.upper(): b for b in Brand.objects.all()}

        created = 0
        updated = 0
        skipped = 0
        errors = 0

        for brand_dir in sorted(root.iterdir()):
            if not brand_dir.is_dir():
                continue
            brand_name_key = brand_dir.name.upper()
            # Try exact match first, then strip accents / spaces
            brand_obj = brand_cache.get(brand_name_key)
            if brand_obj is None:
                # Try case-insensitive match ignoring extra whitespace
                for key, obj in brand_cache.items():
                    if key.strip() == brand_name_key.strip():
                        brand_obj = obj
                        break
            if brand_obj is None:
                self.stderr.write(self.style.WARNING(
                    f"Brand not found in DB: '{brand_dir.name}' — skipping folder"
                ))
                errors += 1
                continue

            for md_file in sorted(brand_dir.glob("*.md")):
                try:
                    text = md_file.read_text(encoding="utf-8")
                except Exception as exc:
                    self.stderr.write(self.style.ERROR(f"Cannot read {md_file}: {exc}"))
                    errors += 1
                    continue

                fm = _parse_front_matter(text)
                name = fm.get("Model", "").strip()
                if not name:
                    self.stderr.write(self.style.WARNING(f"No Model field in {md_file}"))
                    errors += 1
                    continue

                model_types = fm.get("ModelType", [])
                device_type, color, format_print = _extract_attributes(model_types)

                speed_raw = fm.get("SpeedPrint", "")
                speed_print = None
                if speed_raw:
                    try:
                        speed_print = int(speed_raw)
                    except ValueError:
                        pass

                existing = ProductModel.objects.filter(name=name, brand=brand_obj).first()
                if existing:
                    if do_update:
                        existing.device_type = device_type
                        existing.color = color
                        existing.format_print = format_print
                        existing.speed_print = speed_print
                        existing.save(update_fields=["device_type", "color", "format_print", "speed_print"])
                        updated += 1
                        self.stdout.write(f"  updated: {brand_obj.name} / {name}")
                    else:
                        skipped += 1
                    continue

                ProductModel.objects.create(
                    name=name,
                    brand=brand_obj,
                    device_type=device_type,
                    color=color,
                    format_print=format_print,
                    speed_print=speed_print,
                )
                created += 1
                self.stdout.write(f"  created: {brand_obj.name} / {name}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created: {created}, updated: {updated}, skipped: {skipped}, errors: {errors}"
        ))
