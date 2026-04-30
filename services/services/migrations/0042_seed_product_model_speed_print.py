from django.db import migrations


def forward_seed_speed_print(apps, schema_editor):
    """Seed speed_print characteristic for ProductModel (it was missed in 0036).

    Migrations 0036 seeded: weight, dimensions, color, format_print, device_type.
    Migration 0038 added the speed_print EquipmentCharacteristicType record.
    This migration seeds ProductModelCharacteristic rows for speed_print.
    """
    ProductModel = apps.get_model("services", "ProductModel")
    ProductModelCharacteristic = apps.get_model("services", "ProductModelCharacteristic")
    EquipmentCharacteristicType = apps.get_model("services", "EquipmentCharacteristicType")

    try:
        speed_print_type = EquipmentCharacteristicType.objects.get(code="speed_print")
    except EquipmentCharacteristicType.DoesNotExist:
        return

    for model in ProductModel.objects.all().iterator():
        raw_value = getattr(model, "speed_print", None)
        if raw_value is None:
            continue
        normalized_value = str(raw_value)
        if not normalized_value:
            continue
        ProductModelCharacteristic.objects.update_or_create(
            product_model=model,
            characteristic_type=speed_print_type,
            defaults={"value": normalized_value},
        )


def backward_seed_speed_print(apps, schema_editor):
    ProductModelCharacteristic = apps.get_model("services", "ProductModelCharacteristic")
    EquipmentCharacteristicType = apps.get_model("services", "EquipmentCharacteristicType")
    try:
        speed_print_type = EquipmentCharacteristicType.objects.get(code="speed_print")
    except EquipmentCharacteristicType.DoesNotExist:
        return
    ProductModelCharacteristic.objects.filter(characteristic_type=speed_print_type).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0041_consumable_catalog_url_part_catalog_url_and_more"),
    ]

    operations = [
        migrations.RunPython(forward_seed_speed_print, backward_seed_speed_print),
    ]
