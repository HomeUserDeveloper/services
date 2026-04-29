from django.db import migrations


def clear_unconfirmed_brand_sites(apps, schema_editor):
    Brand = apps.get_model("services", "Brand")
    Brand.objects.filter(name="Техноэволаб").update(site="")


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0009_brand_site_data"),
    ]

    operations = [
        migrations.RunPython(clear_unconfirmed_brand_sites, noop_reverse),
    ]
