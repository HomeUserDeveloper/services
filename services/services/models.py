from django.db import models, transaction
from django.db.models import Q
from django.db.models.functions import Lower


class Organization(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активен"
        REGISTERED = "registered", "Зарегистрирован"

    inn_kpp = models.CharField("ИНН/КПП", max_length=32, blank=True)
    ogrn_passport = models.CharField("ОГРН/Паспорт", max_length=32, blank=True)
    name = models.CharField("Название", max_length=255)
    phone = models.CharField("Телефон", max_length=32, blank=True)
    email = models.EmailField("Email", blank=True)
    addresses = models.ManyToManyField(
        "Address",
        through="OrganizationAddress",
        through_fields=("organization", "address"),
        related_name="organizations",
        verbose_name="Адреса",
        blank=True,
    )
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.REGISTERED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name


class OrganizationAddress(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="address_links",
        verbose_name="Организация",
    )
    address = models.ForeignKey(
        "Address",
        on_delete=models.CASCADE,
        related_name="organization_links",
        verbose_name="Адрес",
    )
    main_office = models.BooleanField("Главный офис", default=False)

    class Meta:
        db_table = "services_organization_addresses"
        ordering = ("-main_office", "address__locality", "address__street", "address__house", "id")
        verbose_name = "Адрес организации"
        verbose_name_plural = "Адреса организаций"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "address"),
                name="unique_organization_address_link",
            ),
            models.UniqueConstraint(
                fields=("organization",),
                condition=Q(main_office=True),
                name="unique_main_office_per_organization",
            ),
        ]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.main_office and self.organization_id:
                type(self).objects.filter(
                    organization_id=self.organization_id,
                    main_office=True,
                ).exclude(pk=self.pk).update(main_office=False)
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.organization} / {self.address}"


class OrganizationContact(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="contacts",
        verbose_name="Организация",
    )
    name = models.CharField("Имя", max_length=255)
    position = models.CharField("Должность", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"{self.name} ({self.organization.name})"


class ServiceCenter(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активен"
        REGISTERED = "registered", "Зарегистрирован"

    inn_kpp = models.CharField("ИНН/КПП", max_length=32, blank=True)
    ogrn_passport = models.CharField("ОГРН/Паспорт", max_length=32, blank=True)
    name = models.CharField("Название", max_length=255)
    phone = models.CharField("Телефон", max_length=32, blank=True)
    email = models.EmailField("Email", blank=True)
    addresses = models.ManyToManyField(
        "Address",
        through="ServiceCenterAddress",
        through_fields=("service_center", "address"),
        related_name="service_centers",
        verbose_name="Адреса",
        blank=True,
    )
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.REGISTERED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Сервисный центр"
        verbose_name_plural = "Сервисные центры"

    def __str__(self):
        return self.name


class ServiceCenterAddress(models.Model):
    service_center = models.ForeignKey(
        ServiceCenter,
        on_delete=models.CASCADE,
        related_name="address_links",
        verbose_name="Сервисный центр",
    )
    address = models.ForeignKey(
        "Address",
        on_delete=models.CASCADE,
        related_name="service_center_links",
        verbose_name="Адрес",
    )
    main_office = models.BooleanField("Главный офис", default=False)

    class Meta:
        db_table = "services_servicecenter_addresses"
        ordering = ("-main_office", "address__locality", "address__street", "address__house", "id")
        verbose_name = "Адрес сервисного центра"
        verbose_name_plural = "Адреса сервисных центров"
        constraints = [
            models.UniqueConstraint(
                fields=("service_center", "address"),
                name="unique_service_center_address_link",
            ),
            models.UniqueConstraint(
                fields=("service_center",),
                condition=Q(main_office=True),
                name="unique_main_office_per_service_center",
            ),
        ]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.main_office and self.service_center_id:
                type(self).objects.filter(
                    service_center_id=self.service_center_id,
                    main_office=True,
                ).exclude(pk=self.pk).update(main_office=False)
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service_center} / {self.address}"


class ServiceCenterContact(models.Model):
    service_center = models.ForeignKey(
        ServiceCenter,
        on_delete=models.CASCADE,
        related_name="contacts",
        verbose_name="Сервисный центр",
    )
    name = models.CharField("Имя", max_length=255)
    position = models.CharField("Должность", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Контакт сервисного центра"
        verbose_name_plural = "Контакты сервисных центров"

    def __str__(self):
        return f"{self.name} ({self.service_center.name})"


class ServiceMan(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активен"
        DISABLED = "disabled", "Отключен"
        DELETED = "deleted", "Удален"

    full_name = models.CharField("ФИО", max_length=255)
    phone = models.CharField("Телефон", max_length=32, blank=True)
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("full_name",)
        verbose_name = "Сервисный инженер"
        verbose_name_plural = "Сервисные инженеры"

    def __str__(self):
        return self.full_name


class ProductCategory(models.Model):
    name = models.CharField("Название", max_length=255)
    group = models.CharField("Группа", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("group", "name")
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return f"{self.group} / {self.name}" if self.group else self.name


class Brand(models.Model):
    name = models.CharField("Название", max_length=255)
    site = models.URLField("Сайт", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField("Наименование", max_length=255)
    site = models.URLField("Сайт", blank=True)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_models",
        verbose_name="Категория товара",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_models",
        verbose_name="Бренд",
    )
    device_type = models.CharField("Тип устройства", max_length=32, blank=True)
    color = models.CharField("Цветность", max_length=32, blank=True)
    format_print = models.CharField("Формат", max_length=8, blank=True)
    speed_print = models.PositiveIntegerField("Скорость печати (стр/мин)", null=True, blank=True)
    sku = models.CharField("Артикул", max_length=128, blank=True)
    weight = models.CharField("Вес", max_length=64, blank=True)
    dimensions = models.CharField("Габариты", max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Техника"
        verbose_name_plural = "Техника"

    def __str__(self):
        return f"{self.brand.name} {self.name}" if self.brand_id else self.name


class EquipmentCharacteristicType(models.Model):
    class ValueKind(models.TextChoices):
        TEXT = "text", "Текст"
        NUMBER = "number", "Число"
        BOOLEAN = "boolean", "Логический (чекбокс)"
        TAGS = "tags", "Список (теги)"

    code = models.CharField("Код", max_length=64, unique=True)
    name = models.CharField("Название", max_length=128, unique=True)
    value_kind = models.CharField(
        "Тип значения",
        max_length=16,
        choices=ValueKind.choices,
        default=ValueKind.TEXT,
    )
    sort_order = models.PositiveSmallIntegerField("Порядок", default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("sort_order", "name", "id")
        verbose_name = "Тип характеристики техники"
        verbose_name_plural = "Типы характеристик техники"

    def __str__(self):
        return self.name


class ProductModelCharacteristic(models.Model):
    product_model = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name="characteristics",
        verbose_name="Техника",
    )
    characteristic_type = models.ForeignKey(
        EquipmentCharacteristicType,
        on_delete=models.PROTECT,
        related_name="values",
        verbose_name="Характеристика",
    )
    value = models.CharField("Значение", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("characteristic_type__sort_order", "characteristic_type__name", "id")
        verbose_name = "Характеристика техники"
        verbose_name_plural = "Характеристики техники"
        constraints = [
            models.UniqueConstraint(fields=["product_model", "characteristic_type"], name="uniq_model_characteristic_type"),
        ]

    def __str__(self):
        return f"{self.product_model}: {self.characteristic_type.name} = {self.value}"


class Consumable(models.Model):
    name = models.CharField("Наименование", max_length=255)
    site = models.URLField("Сайт", blank=True)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consumables",
        verbose_name="Категория товара",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consumables",
        verbose_name="Бренд",
    )
    device_type = models.CharField("Тип устройства", max_length=32, blank=True)
    color = models.CharField("Цветность", max_length=32, blank=True)
    format_print = models.CharField("Формат", max_length=8, blank=True)
    speed_print = models.PositiveIntegerField("Скорость печати (стр/мин)", null=True, blank=True)
    sku = models.CharField("Артикул", max_length=128, blank=True)
    weight = models.CharField("Вес", max_length=64, blank=True)
    dimensions = models.CharField("Габариты", max_length=128, blank=True)
    compatible_models = models.ManyToManyField(
        ProductModel,
        through="ConsumableCompatibility",
        related_name="compatible_consumables",
        verbose_name="Совместимая техника",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Расходный материал"
        verbose_name_plural = "Расходные материалы"

    def __str__(self):
        return f"{self.brand.name} {self.name}" if self.brand_id else self.name


class ConsumableCompatibility(models.Model):
    consumable = models.ForeignKey(
        Consumable,
        on_delete=models.CASCADE,
        related_name="compatibilities",
        verbose_name="Расходный материал",
    )
    product_model = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name="consumable_links",
        verbose_name="Техника",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("product_model__name",)
        verbose_name = "Совместимость расходного материала"
        verbose_name_plural = "Совместимость расходных материалов"
        constraints = [
            models.UniqueConstraint(fields=["consumable", "product_model"], name="uniq_consumable_product_model"),
        ]

    def __str__(self):
        return f"{self.consumable} -> {self.product_model}"


class Part(models.Model):
    name = models.CharField("Наименование", max_length=255)
    site = models.URLField("Сайт", blank=True)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="parts",
        verbose_name="Категория товара",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="parts",
        verbose_name="Бренд",
    )
    device_type = models.CharField("Тип устройства", max_length=32, blank=True)
    color = models.CharField("Цветность", max_length=32, blank=True)
    format_print = models.CharField("Формат", max_length=8, blank=True)
    speed_print = models.PositiveIntegerField("Скорость печати (стр/мин)", null=True, blank=True)
    sku = models.CharField("Артикул", max_length=128, blank=True)
    weight = models.CharField("Вес", max_length=64, blank=True)
    dimensions = models.CharField("Габариты", max_length=128, blank=True)
    compatible_models = models.ManyToManyField(
        ProductModel,
        through="PartCompatibility",
        related_name="compatible_parts",
        verbose_name="Совместимая техника",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"

    def __str__(self):
        return f"{self.brand.name} {self.name}" if self.brand_id else self.name


class PartCompatibility(models.Model):
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name="compatibilities",
        verbose_name="Запчасть",
    )
    product_model = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name="part_links",
        verbose_name="Техника",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("product_model__name",)
        verbose_name = "Совместимость запчасти"
        verbose_name_plural = "Совместимость запчастей"
        constraints = [
            models.UniqueConstraint(fields=["part", "product_model"], name="uniq_part_product_model"),
        ]

    def __str__(self):
        return f"{self.part} -> {self.product_model}"


class WorkDirectory(models.Model):
    code = models.CharField("Код", max_length=64, unique=True)
    name = models.CharField("Наименование", max_length=255)
    unit_price = models.DecimalField("Цена за единицу", max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("code", "name")
        verbose_name = "Работа"
        verbose_name_plural = "Работы"
        constraints = [
            models.UniqueConstraint(
                Lower("code"),
                name="uniq_workdirectory_code_ci",
            ),
        ]

    def __str__(self):
        return f"{self.code} / {self.name}"


class WorkDirectoryConsumable(models.Model):
    work = models.ForeignKey(
        WorkDirectory,
        on_delete=models.CASCADE,
        related_name="consumable_links",
        verbose_name="Работа",
    )
    consumable = models.ForeignKey(
        Consumable,
        on_delete=models.PROTECT,
        related_name="work_links",
        verbose_name="Расходный материал",
    )
    quantity = models.PositiveIntegerField("Количество", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("consumable__name", "id")
        verbose_name = "Расходный материал в работе"
        verbose_name_plural = "Расходные материалы в работах"
        constraints = [
            models.UniqueConstraint(fields=["work", "consumable"], name="uniq_work_consumable"),
        ]

    def __str__(self):
        return f"{self.work} -> {self.consumable}"


class WorkDirectoryPart(models.Model):
    work = models.ForeignKey(
        WorkDirectory,
        on_delete=models.CASCADE,
        related_name="part_links",
        verbose_name="Работа",
    )
    part = models.ForeignKey(
        Part,
        on_delete=models.PROTECT,
        related_name="work_links",
        verbose_name="Запчасть",
    )
    quantity = models.PositiveIntegerField("Количество", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("part__name", "id")
        verbose_name = "Запчасть в работе"
        verbose_name_plural = "Запчасти в работах"
        constraints = [
            models.UniqueConstraint(fields=["work", "part"], name="uniq_work_part"),
        ]

    def __str__(self):
        return f"{self.work} -> {self.part}"


class Address(models.Model):
    postal_code = models.CharField("Индекс", max_length=20, blank=True)
    locality = models.CharField("Населенный пункт", max_length=255)
    street = models.CharField("Улица/Проспект", max_length=255, blank=True)
    house = models.CharField("Дом", max_length=32, blank=True)
    building = models.CharField("Корпус", max_length=32, blank=True)
    structure = models.CharField("Строение", max_length=32, blank=True)
    floor = models.CharField("Этаж", max_length=32, blank=True)
    room = models.CharField("Комната", max_length=64, blank=True)
    note = models.TextField("Примечание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("locality", "street", "house", "id")
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        parts = [self.locality]
        if self.street:
            parts.append(self.street)
        if self.house:
            parts.append(f"д. {self.house}")
        return ", ".join(parts)


class StatusDirectory(models.Model):
    code = models.PositiveSmallIntegerField("Код", unique=True)
    name = models.CharField("Статус", max_length=255)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("code",)
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return f"{self.code}. {self.name}"


class ClientEquipment(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="client_equipments",
        verbose_name="Организация",
    )
    product_model = models.ForeignKey(
        ProductModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_equipments",
        verbose_name="Наименование",
    )
    serial_number = models.CharField("Серийный номер", max_length=255, blank=True)
    inventory_number = models.CharField("Инвентарный номер", max_length=255, blank=True)
    print_counter = models.PositiveIntegerField("Счетчик печати", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("organization__name", "product_model__name", "id")
        verbose_name = "Техника клиента"
        verbose_name_plural = "Техника клиентов"

    def __str__(self):
        parts = []
        if self.product_model_id:
            parts.append(str(self.product_model))
        if self.serial_number:
            parts.append(f"Сер: {self.serial_number}")
        if self.inventory_number:
            parts.append(f"Инв: {self.inventory_number}")
        
        if parts:
            return " | ".join(parts)
        return f"Техника #{self.id}"

    def clean(self):
        from django.core.exceptions import ValidationError

        errors = {}
        organization_id = self.organization_id

        if not organization_id:
            if self.serial_number.strip() or self.inventory_number.strip():
                errors["organization"] = "Для проверки уникальности необходимо указать организацию."
            if errors:
                raise ValidationError(errors)
            return

        # Проверка уникальности серийного номера в пределах организации
        if self.serial_number.strip():
            existing_serial = ClientEquipment.objects.filter(
                organization_id=organization_id,
                serial_number=self.serial_number.strip(),
            ).exclude(pk=self.pk)
            if existing_serial.exists():
                errors["serial_number"] = "Серийный номер уже используется в этой организации."

        # Проверка уникальности инвентарного номера в пределах организации
        if self.inventory_number.strip():
            existing_inventory = ClientEquipment.objects.filter(
                organization_id=organization_id,
                inventory_number=self.inventory_number.strip(),
            ).exclude(pk=self.pk)
            if existing_inventory.exists():
                errors["inventory_number"] = "Инвентарный номер уже используется в этой организации."

        if errors:
            raise ValidationError(errors)


class RepairDocument(models.Model):
    class RepairPlace(models.TextChoices):
        OFFICE = "office", "Офис"
        ONSITE = "onsite", "Выезд"

    date = models.DateField("Дата")
    repair_place = models.CharField(
        "Место ремонта",
        max_length=16,
        choices=RepairPlace.choices,
        default=RepairPlace.OFFICE,
    )
    service_center = models.ForeignKey(
        ServiceCenter,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="repair_documents",
        verbose_name="Сервисный центр",
    )
    service_center_address = models.ForeignKey(
        "Address",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="repair_documents_as_service_center_address",
        verbose_name="Адрес сервисного центра",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="repair_documents",
        verbose_name="Название",
    )
    serviceman = models.ForeignKey(
        ServiceMan,
        on_delete=models.PROTECT,
        related_name="repair_documents",
        verbose_name="ФИО",
    )
    status = models.ForeignKey(
        StatusDirectory,
        on_delete=models.PROTECT,
        related_name="repair_documents",
        verbose_name="Статус",
    )
    client_equipment = models.ForeignKey(
        ClientEquipment,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="repair_documents",
        verbose_name="Техника клиента",
    )
    source_document = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="status_revisions",
        verbose_name="Предыдущий документ",
    )
    status_edited_at = models.DateTimeField("Дата редактирования статуса", auto_now_add=True, editable=False)
    malfunction = models.TextField("Неисправность", blank=True)
    work_performed = models.TextField("Выполненные работы", blank=True)
    note = models.TextField("Примечание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date", "-id")
        verbose_name = "Документ ремонта"
        verbose_name_plural = "Документы ремонта"

    def __str__(self):
        return f"Ремонт #{self.id} от {self.date}"

    def clean(self):
        if self.client_equipment_id and self.organization_id and self.client_equipment.organization_id != self.organization_id:
            from django.core.exceptions import ValidationError

            raise ValidationError({"client_equipment": "Техника должна принадлежать выбранной организации."})

        if self.service_center_address_id and not self.service_center_id:
            from django.core.exceptions import ValidationError

            raise ValidationError({"service_center_address": "Сначала выберите сервисный центр."})

        if self.service_center_id and self.service_center_address_id:
            address_ok = ServiceCenterAddress.objects.filter(
                service_center_id=self.service_center_id,
                address_id=self.service_center_address_id,
            ).exists()
            if not address_ok:
                from django.core.exceptions import ValidationError

                raise ValidationError({"service_center_address": "Адрес должен принадлежать выбранному сервисному центру."})


class RepairDocumentWork(models.Model):
    repair_document = models.ForeignKey(
        RepairDocument,
        on_delete=models.CASCADE,
        related_name="work_links",
        verbose_name="Документ ремонта",
    )
    work = models.ForeignKey(
        WorkDirectory,
        on_delete=models.PROTECT,
        related_name="repair_document_links",
        verbose_name="Работа",
    )
    quantity = models.PositiveIntegerField("Количество работ", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("work__code", "work__name", "id")
        verbose_name = "Работа в документе ремонта"
        verbose_name_plural = "Работы в документах ремонта"
        constraints = [
            models.UniqueConstraint(fields=["repair_document", "work"], name="uniq_repair_document_work"),
        ]

    def __str__(self):
        return f"{self.repair_document} -> {self.work}"


class AcceptanceDocument(models.Model):
    date = models.DateField("Дата")
    serviceman = models.ForeignKey(
        ServiceMan,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="acceptance_documents",
        verbose_name="Сервисный инженер",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="acceptance_documents",
        verbose_name="Организация",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date", "-id")
        verbose_name = "Документ приемки техники"
        verbose_name_plural = "Документы приемки техники"

    def __str__(self):
        return f"Приемка #{self.id} от {self.date}"


class AcceptanceDocumentEquipment(models.Model):
    acceptance_document = models.ForeignKey(
        AcceptanceDocument,
        on_delete=models.CASCADE,
        related_name="equipment_links",
        verbose_name="Документ приемки",
    )
    client_equipment = models.ForeignKey(
        ClientEquipment,
        on_delete=models.PROTECT,
        related_name="acceptance_links",
        verbose_name="Техника клиента",
    )
    repair_document = models.OneToOneField(
        RepairDocument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acceptance_equipment_link",
        verbose_name="Документ ремонта",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("client_equipment__product_model__name", "client_equipment__serial_number", "id")
        verbose_name = "Техника в документе приемки"
        verbose_name_plural = "Техника в документах приемки"
        constraints = [
            models.UniqueConstraint(
                fields=("acceptance_document", "client_equipment"),
                name="unique_acceptance_document_equipment",
            ),
        ]

    def __str__(self):
        return f"{self.acceptance_document} / {self.client_equipment}"


class ShipmentDocument(models.Model):
    date = models.DateField("Дата")
    serviceman = models.ForeignKey(
        ServiceMan,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="shipment_documents",
        verbose_name="Сервисный инженер",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="shipment_documents",
        verbose_name="Организация",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date", "-id")
        verbose_name = "Документ отгрузки техники"
        verbose_name_plural = "Документы отгрузки техники"

    def __str__(self):
        return f"Отгрузка #{self.id} от {self.date}"


class ShipmentDocumentEquipment(models.Model):
    shipment_document = models.ForeignKey(
        ShipmentDocument,
        on_delete=models.CASCADE,
        related_name="equipment_links",
        verbose_name="Документ отгрузки",
    )
    client_equipment = models.ForeignKey(
        ClientEquipment,
        on_delete=models.PROTECT,
        related_name="shipment_links",
        verbose_name="Техника клиента",
    )
    repair_document = models.OneToOneField(
        RepairDocument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shipment_equipment_link",
        verbose_name="Документ ремонта",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("client_equipment__product_model__name", "client_equipment__serial_number", "id")
        verbose_name = "Техника в документе отгрузки"
        verbose_name_plural = "Техника в документах отгрузки"
        constraints = [
            models.UniqueConstraint(
                fields=("shipment_document", "client_equipment"),
                name="unique_shipment_document_equipment",
            ),
        ]

    def __str__(self):
        return f"{self.shipment_document} / {self.client_equipment}"


class RepairDocumentPart(models.Model):
    repair_document = models.ForeignKey(
        RepairDocument,
        on_delete=models.CASCADE,
        related_name="part_links",
        verbose_name="Документ ремонта",
    )
    part = models.ForeignKey(
        Part,
        on_delete=models.PROTECT,
        related_name="repair_document_links",
        verbose_name="Запчасть",
    )
    manual_quantity = models.PositiveIntegerField("Ручное количество", default=0)
    work_quantity = models.PositiveIntegerField("Количество из работ", default=0)
    quantity = models.PositiveIntegerField("Количество", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("part__name",)
        verbose_name = "Запчасть в документе ремонта"
        verbose_name_plural = "Запчасти в документах ремонта"
        constraints = [
            models.UniqueConstraint(fields=["repair_document", "part"], name="uniq_repair_document_part"),
        ]

    def __str__(self):
        return f"{self.repair_document} -> {self.part}"


class RepairDocumentConsumable(models.Model):
    repair_document = models.ForeignKey(
        RepairDocument,
        on_delete=models.CASCADE,
        related_name="consumable_links",
        verbose_name="Документ ремонта",
    )
    consumable = models.ForeignKey(
        Consumable,
        on_delete=models.PROTECT,
        related_name="repair_document_links",
        verbose_name="Расходный материал",
    )
    manual_quantity = models.PositiveIntegerField("Ручное количество", default=0)
    work_quantity = models.PositiveIntegerField("Количество из работ", default=0)
    quantity = models.PositiveIntegerField("Количество", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("consumable__name",)
        verbose_name = "Расходный материал в документе ремонта"
        verbose_name_plural = "Расходные материалы в документах ремонта"
        constraints = [
            models.UniqueConstraint(fields=["repair_document", "consumable"], name="uniq_repair_document_consumable"),
        ]

    def __str__(self):
        return f"{self.repair_document} -> {self.consumable}"


class ServiceExchangeLog(models.Model):
    class Action(models.TextChoices):
        EXPORT = "export", "Выгрузка"
        IMPORT = "import", "Загрузка"
        CLEANUP = "cleanup", "Очистка"
        ARCHIVE = "archive", "Архив базы"

    class Section(models.TextChoices):
        DIRECTORIES = "directories", "Справочники"
        DOCUMENTS = "documents", "Документы"
        ALL = "all", "Все"

    class ResultStatus(models.TextChoices):
        SUCCESS = "success", "Успешно"
        ERROR = "error", "Ошибка"

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_exchange_logs",
        verbose_name="Пользователь",
    )
    action = models.CharField("Действие", max_length=16, choices=Action.choices)
    section = models.CharField("Раздел", max_length=16, choices=Section.choices)
    result_status = models.CharField("Результат", max_length=16, choices=ResultStatus.choices)
    dry_run = models.BooleanField("Только проверка", default=False)
    file_name = models.CharField("Имя файла", max_length=255, blank=True)
    selected_keys = models.JSONField("Выбранные наборы", default=list, blank=True)
    summary = models.JSONField("Сводка", default=dict, blank=True)
    message = models.TextField("Сообщение", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "-id")
        verbose_name = "Лог обмена данными"
        verbose_name_plural = "Логи обмена данными"

    def __str__(self):
        return f"{self.get_action_display()} / {self.get_section_display()} / {self.created_at:%d.%m.%Y %H:%M}"
