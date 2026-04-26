from collections import Counter

from django.core.management.base import BaseCommand

from services.models import ProductCategory, ProductModel


class Command(BaseCommand):
    help = "Normalize ProductModel.category from device_type/format_print/color"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Show planned changes without saving them",
        )
        parser.add_argument(
            "--no-create-categories",
            action="store_true",
            default=False,
            help="Do not create missing categories automatically",
        )

    def _pick_or_create(self, group, name, created_categories, allow_create):
        obj = ProductCategory.objects.filter(group=group, name=name).first()
        if obj:
            return obj
        if not allow_create:
            return None
        obj = ProductCategory.objects.create(group=group, name=name)
        created_categories.append(obj)
        return obj

    def _detect_target_category(self, pm, created_categories, allow_create):
        device_type = (pm.device_type or "").strip()
        fmt = (pm.format_print or "").strip().upper()
        color = (pm.color or "").strip().lower()

        if device_type == "Принтер":
            if fmt == "A4" and color == "черно-белый":
                return self._pick_or_create("Принтер", "Принтер А4 лазерный (ч/б)", created_categories, allow_create)
            if fmt == "A4" and color == "цветной":
                return self._pick_or_create("Принтер", "Принтер А4 лазерный цветной", created_categories, allow_create)
            if fmt == "A3" and color == "черно-белый":
                return self._pick_or_create("Принтер", "Принтер A3 лазерный (ч/б)", created_categories, allow_create)
            if fmt == "A3" and color == "цветной":
                return self._pick_or_create("Принтер", "Принтер A3 лазерный цветной", created_categories, allow_create)
            if color == "черно-белый":
                return self._pick_or_create("Принтер", "Принтер лазерный (ч/б)", created_categories, allow_create)
            if color == "цветной":
                return self._pick_or_create("Принтер", "Принтер лазерный цветной", created_categories, allow_create)

        if device_type == "МФУ":
            if fmt == "A4" and color == "черно-белый":
                return self._pick_or_create("МФУ", "МФУ А4 лазерный (ч/б)", created_categories, allow_create)
            if fmt == "A4" and color == "цветной":
                return self._pick_or_create("МФУ", "МФУ А4 лазерный цветной", created_categories, allow_create)
            if fmt == "A3" and color == "черно-белый":
                return self._pick_or_create("МФУ", "МФУ A3 лазерный (ч/б)", created_categories, allow_create)
            if fmt == "A3" and color == "цветной":
                return self._pick_or_create("МФУ", "МФУ A3 лазерный цветной", created_categories, allow_create)

        return None

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        allow_create = not options["no_create_categories"]

        created_categories = []
        updated = 0
        unmapped = 0

        for pm in ProductModel.objects.select_related("category").all():
            target = self._detect_target_category(pm, created_categories, allow_create)
            if target is None:
                unmapped += 1
                continue

            if pm.category_id != target.id:
                updated += 1
                if not dry_run:
                    pm.category = target
                    pm.save(update_fields=["category"])

        if created_categories:
            self.stdout.write("Созданы категории:")
            for c in created_categories:
                self.stdout.write(f"- {c.id}: {c.group} / {c.name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово. Обновлено моделей: {updated}, неразобранных: {unmapped}, dry-run: {dry_run}"
            )
        )

        distribution = Counter(ProductModel.objects.values_list("category__group", "category__name"))
        self.stdout.write("Распределение по категориям:")
        for key, count in sorted(distribution.items(), key=lambda x: (-x[1], x[0])):
            self.stdout.write(f"{key} -> {count}")
