from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0007_productmodel_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="productmodel",
            name="device_type",
            field=models.CharField(blank=True, max_length=32, verbose_name="Тип устройства"),
        ),
        migrations.AddField(
            model_name="productmodel",
            name="color",
            field=models.CharField(blank=True, max_length=32, verbose_name="Цветность"),
        ),
        migrations.AddField(
            model_name="productmodel",
            name="format_print",
            field=models.CharField(blank=True, max_length=8, verbose_name="Формат"),
        ),
        migrations.AddField(
            model_name="productmodel",
            name="speed_print",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="Скорость печати (стр/мин)"),
        ),
    ]
