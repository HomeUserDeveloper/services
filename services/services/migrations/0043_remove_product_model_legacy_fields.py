from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0042_seed_product_model_speed_print"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productmodel",
            name="color",
        ),
        migrations.RemoveField(
            model_name="productmodel",
            name="device_type",
        ),
        migrations.RemoveField(
            model_name="productmodel",
            name="dimensions",
        ),
        migrations.RemoveField(
            model_name="productmodel",
            name="format_print",
        ),
        migrations.RemoveField(
            model_name="productmodel",
            name="speed_print",
        ),
        migrations.RemoveField(
            model_name="productmodel",
            name="weight",
        ),
    ]
