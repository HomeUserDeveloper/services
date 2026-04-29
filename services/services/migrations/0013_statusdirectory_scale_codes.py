from django.db import migrations


def scale_status_codes(apps, schema_editor):
    StatusDirectory = apps.get_model("services", "StatusDirectory")

    rows = list(StatusDirectory.objects.all().order_by("code", "id"))
    if not rows:
        return

    # If already scaled (10, 20, 30, ...), do nothing.
    if all((row.code % 10 == 0) for row in rows):
        return

    # Step 1: move all codes to a temporary safe range to avoid unique collisions.
    for row in rows:
        row.code = row.code + 1000
        row.save(update_fields=["code"])

    # Step 2: assign final scaled codes in stable order.
    tmp_rows = list(StatusDirectory.objects.all().order_by("code", "id"))
    for index, row in enumerate(tmp_rows, start=1):
        row.code = index * 10
        row.save(update_fields=["code"])


def noop_reverse(apps, schema_editor):
    # Not reversible because original custom code values are unknown.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0012_statusdirectory"),
    ]

    operations = [
        migrations.RunPython(scale_status_codes, noop_reverse),
    ]
