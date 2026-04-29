from django.db import migrations, models
import django.db.models.deletion


LEGACY_CHARACTERISTIC_FIELD_MAP = {
    "weight": "weight",
    "dimensions": "dimensions",
    "color": "color",
    "format_print": "format_print",
    "device_type": "device_type",
    "speed_print": "speed_print",
}


def _seed_characteristics(apps, entity_model_name, characteristic_model_name, owner_field_name):
    EntityModel = apps.get_model("services", entity_model_name)
    CharacteristicModel = apps.get_model("services", characteristic_model_name)
    EquipmentCharacteristicType = apps.get_model("services", "EquipmentCharacteristicType")

    type_map = {
        item.code: item
        for item in EquipmentCharacteristicType.objects.filter(code__in=LEGACY_CHARACTERISTIC_FIELD_MAP)
    }

    for entity in EntityModel.objects.all().iterator():
        for code, field_name in LEGACY_CHARACTERISTIC_FIELD_MAP.items():
            characteristic_type = type_map.get(code)
            if not characteristic_type:
                continue

            raw_value = getattr(entity, field_name, None)
            if code == "speed_print":
                if raw_value is None:
                    continue
                normalized_value = str(raw_value)
            else:
                normalized_value = (raw_value or "").strip()
                if not normalized_value:
                    continue

            CharacteristicModel.objects.update_or_create(
                **{
                    owner_field_name: entity,
                    "characteristic_type": characteristic_type,
                },
                defaults={"value": normalized_value},
            )


def forward_seed_characteristics(apps, schema_editor):
    _seed_characteristics(apps, "Consumable", "ConsumableCharacteristic", "consumable")
    _seed_characteristics(apps, "Part", "PartCharacteristic", "part")


def backward_seed_characteristics(apps, schema_editor):
    ConsumableCharacteristic = apps.get_model("services", "ConsumableCharacteristic")
    PartCharacteristic = apps.get_model("services", "PartCharacteristic")

    ConsumableCharacteristic.objects.all().delete()
    PartCharacteristic.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0038_add_speed_print_characteristic"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConsumableCharacteristic",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("value", models.CharField(max_length=255, verbose_name="Значение")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "characteristic_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="consumable_values",
                        to="services.equipmentcharacteristictype",
                        verbose_name="Характеристика",
                    ),
                ),
                (
                    "consumable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="characteristics",
                        to="services.consumable",
                        verbose_name="Расходный материал",
                    ),
                ),
            ],
            options={
                "verbose_name": "Характеристика расходного материала",
                "verbose_name_plural": "Характеристики расходных материалов",
                "ordering": ("characteristic_type__sort_order", "characteristic_type__name", "id"),
                "constraints": [
                    models.UniqueConstraint(
                        fields=("consumable", "characteristic_type"),
                        name="uniq_consumable_characteristic_type",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="PartCharacteristic",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("value", models.CharField(max_length=255, verbose_name="Значение")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "characteristic_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="part_values",
                        to="services.equipmentcharacteristictype",
                        verbose_name="Характеристика",
                    ),
                ),
                (
                    "part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="characteristics",
                        to="services.part",
                        verbose_name="Запчасть",
                    ),
                ),
            ],
            options={
                "verbose_name": "Характеристика запчасти",
                "verbose_name_plural": "Характеристики запчастей",
                "ordering": ("characteristic_type__sort_order", "characteristic_type__name", "id"),
                "constraints": [
                    models.UniqueConstraint(
                        fields=("part", "characteristic_type"),
                        name="uniq_part_characteristic_type",
                    )
                ],
            },
        ),
        migrations.RunPython(forward_seed_characteristics, backward_seed_characteristics),
    ]