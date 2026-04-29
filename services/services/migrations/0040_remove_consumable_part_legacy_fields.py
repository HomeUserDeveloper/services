from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0039_consumable_and_part_characteristics"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="consumable",
            name="color",
        ),
        migrations.RemoveField(
            model_name="consumable",
            name="device_type",
        ),
        migrations.RemoveField(
            model_name="consumable",
            name="dimensions",
        ),
        migrations.RemoveField(
            model_name="consumable",
            name="format_print",
        ),
        migrations.RemoveField(
            model_name="consumable",
            name="speed_print",
        ),
        migrations.RemoveField(
            model_name="consumable",
            name="weight",
        ),
        migrations.RemoveField(
            model_name="part",
            name="color",
        ),
        migrations.RemoveField(
            model_name="part",
            name="device_type",
        ),
        migrations.RemoveField(
            model_name="part",
            name="dimensions",
        ),
        migrations.RemoveField(
            model_name="part",
            name="format_print",
        ),
        migrations.RemoveField(
            model_name="part",
            name="speed_print",
        ),
        migrations.RemoveField(
            model_name="part",
            name="weight",
        ),
    ]
