from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0010_brand_site_corrections"),
    ]

    operations = [
        migrations.AddField(
            model_name="productmodel",
            name="site",
            field=models.URLField(blank=True, verbose_name="Сайт"),
        ),
    ]
