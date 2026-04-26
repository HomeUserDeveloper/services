from django.db import migrations, models


def populate_brand_sites(apps, schema_editor):
    Brand = apps.get_model("services", "Brand")

    sites = {
        "1С": "https://1c.ru",
        "AVISION": "https://www.avision.com.tw",
        "BROTHER": "https://www.brother.com",
        "CACTUS": "https://cactus-russia.ru",
        "CANON": "https://global.canon",
        "DELL": "https://www.dell.com",
        "DUPLO": "https://www.duplointernational.com",
        "Deli": "https://www.deliworld.com",
        "EPSON": "https://www.epson.com",
        "FUJITSU": "https://www.fujitsu.com",
        "G&G": "https://www.ggimage.com",
        "HP": "https://www.hp.com",
        "KODAK": "https://www.kodak.com",
        "KONICA MINOLTA": "https://www.konicaminolta.com",
        "KYOCERA": "https://www.kyocera.com",
        "LEXMARK": "https://www.lexmark.com",
        "MITSUBISHI": "https://www.mitsubishielectric.com",
        "NEC": "https://www.nec.com",
        "OKI": "https://www.oki.com",
        "PANASONIC": "https://www.panasonic.com",
        "PANTUM": "https://global.pantum.com",
        "RICOH": "https://www.ricoh.com",
        "RISO": "https://www.riso.com",
        "SAMSUNG": "https://www.samsung.com",
        "SHARP": "https://global.sharp",
        "SONY": "https://www.sony.com",
        "TOSHIBA": "https://www.toshiba.com",
        "XEROX": "https://www.xerox.com",
        "ZEBRA": "https://www.zebra.com",
        "Катюша": "https://katusha-it.ru",
        "Техноэволаб": "https://tehnoevolab.ru",
    }

    for name, site in sites.items():
        Brand.objects.filter(name=name).update(site=site)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0008_productmodel_extra_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="brand",
            name="site",
            field=models.URLField(blank=True, verbose_name="Сайт"),
        ),
        migrations.RunPython(populate_brand_sites, noop_reverse),
    ]
