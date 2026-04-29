from django.db import migrations, models


def seed_statuses(apps, schema_editor):
    StatusDirectory = apps.get_model("services", "StatusDirectory")

    rows = [
        (1, "Получено", "Оборудование принято в сервис и зарегистрировано."),
        (2, "Ожидание диагностики", "Устройство ожидает постановки на диагностику."),
        (3, "Диагностика", "Проводится техническая диагностика и проверка неисправностей."),
        (4, "Результат диагностики - исправно", "По результатам диагностики неисправности не обнаружены."),
        (5, "Результат диагностики - требуется ремонт", "Подтверждена неисправность, требуется ремонт."),
        (6, "Заказ запчастей", "Сформирован и размещен заказ на необходимые запчасти."),
        (7, "Ожидание запчастей", "Ожидание поступления заказанных запчастей."),
        (8, "Запчасти получены", "Необходимые запчасти получены и готовы к установке."),
        (9, "Ремонт", "Выполняются ремонтные работы."),
        (10, "Тестирование/Контроль качества", "После ремонта выполняется тестирование и контроль качества."),
        (11, "Готово к выдаче", "Оборудование готово к передаче клиенту."),
        (12, "Отгружено клиенту", "Оборудование выдано или отправлено клиенту."),
        (13, "Списание без ремонта", "Принято решение о списании оборудования без ремонта."),
        (14, "Возврат клиенту по гарантии", "Оборудование возвращено клиенту в рамках гарантийного случая."),
        (15, "Отказ от ремонта", "Клиент отказался от проведения ремонта."),
    ]

    for code, name, description in rows:
        StatusDirectory.objects.update_or_create(
            code=code,
            defaults={"name": name, "description": description},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0011_productmodel_site"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatusDirectory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.PositiveSmallIntegerField(unique=True, verbose_name="Код")),
                ("name", models.CharField(max_length=255, verbose_name="Статус")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Статус",
                "verbose_name_plural": "Статусы",
                "ordering": ("code",),
            },
        ),
        migrations.RunPython(seed_statuses, migrations.RunPython.noop),
    ]
