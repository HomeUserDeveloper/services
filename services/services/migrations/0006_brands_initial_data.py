from django.db import migrations

BRANDS = [
    "1С",
    "Катюша",
    "Техноэволаб",
    "AVISION",
    "BROTHER",
    "CACTUS",
    "CANON",
    "Deli",
    "DELL",
    "DUPLO",
    "EPSON",
    "FUJITSU",
    "G&G",
    "HP",
    "KODAK",
    "KONICA MINOLTA",
    "KYOCERA",
    "LEXMARK",
    "MITSUBISHI",
    "NEC",
    "OKI",
    "PANASONIC",
    "PANTUM",
    "RICOH",
    "RISO",
    "SAMSUNG",
    "SHARP",
    "SONY",
    "TOSHIBA",
    "XEROX",
    "ZEBRA",
]


def add_brands(apps, schema_editor):
    Brand = apps.get_model("services", "Brand")
    for name in BRANDS:
        Brand.objects.get_or_create(name=name)


def remove_brands(apps, schema_editor):
    Brand = apps.get_model("services", "Brand")
    Brand.objects.filter(name__in=BRANDS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0005_brand_productmodel"),
    ]

    operations = [
        migrations.RunPython(add_brands, reverse_code=remove_brands),
    ]
