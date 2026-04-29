from django.db import migrations


def forward_seed_characteristics(apps, schema_editor):
    ProductModel = apps.get_model("services", "ProductModel")
    EquipmentCharacteristicType = apps.get_model("services", "EquipmentCharacteristicType")
    ProductModelCharacteristic = apps.get_model("services", "ProductModelCharacteristic")

    default_types = [
        ("weight", "Вес", 10),
        ("dimensions", "Габариты", 20),
        ("color", "Цветность", 30),
        ("format_print", "Формат", 40),
        ("device_type", "Тип устройства", 50),
    ]

    type_map = {}
    for code, name, sort_order in default_types:
        ctype, _ = EquipmentCharacteristicType.objects.get_or_create(
            code=code,
            defaults={"name": name, "sort_order": sort_order},
        )
        type_map[code] = ctype

    for model in ProductModel.objects.all().iterator():
        for code in ("weight", "dimensions", "color", "format_print", "device_type"):
            value = getattr(model, code, "") or ""
            value = value.strip()
            if not value:
                continue
            ProductModelCharacteristic.objects.get_or_create(
                product_model=model,
                characteristic_type=type_map[code],
                defaults={"value": value},
            )


def backward_seed_characteristics(apps, schema_editor):
    EquipmentCharacteristicType = apps.get_model("services", "EquipmentCharacteristicType")
    ProductModelCharacteristic = apps.get_model("services", "ProductModelCharacteristic")

    ProductModelCharacteristic.objects.filter(
        characteristic_type__code__in=["weight", "dimensions", "color", "format_print", "device_type"]
    ).delete()
    EquipmentCharacteristicType.objects.filter(
        code__in=["weight", "dimensions", "color", "format_print", "device_type"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0035_equipmentcharacteristictype_and_more"),
    ]

    operations = [
        migrations.RunPython(forward_seed_characteristics, backward_seed_characteristics),
    ]
