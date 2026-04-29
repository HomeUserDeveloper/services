from django.db import migrations


def forward_add_speed_print_characteristic(apps, schema_editor):
    ProductModel = apps.get_model("services", "ProductModel")
    EquipmentCharacteristicType = apps.get_model("services", "EquipmentCharacteristicType")
    ProductModelCharacteristic = apps.get_model("services", "ProductModelCharacteristic")

    speed_print_type, _ = EquipmentCharacteristicType.objects.update_or_create(
        code="speed_print",
        defaults={
            "name": "Скорость печати",
            "sort_order": 45,
            "value_kind": "number",
        },
    )

    for model in ProductModel.objects.exclude(speed_print__isnull=True).iterator():
        ProductModelCharacteristic.objects.update_or_create(
            product_model=model,
            characteristic_type=speed_print_type,
            defaults={"value": str(model.speed_print)},
        )


def backward_add_speed_print_characteristic(apps, schema_editor):
    EquipmentCharacteristicType = apps.get_model("services", "EquipmentCharacteristicType")
    ProductModelCharacteristic = apps.get_model("services", "ProductModelCharacteristic")

    ProductModelCharacteristic.objects.filter(characteristic_type__code="speed_print").delete()
    EquipmentCharacteristicType.objects.filter(code="speed_print").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0037_equipmentcharacteristictype_value_kind"),
    ]

    operations = [
        migrations.RunPython(
            forward_add_speed_print_characteristic,
            backward_add_speed_print_characteristic,
        ),
    ]