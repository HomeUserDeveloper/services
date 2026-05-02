from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.db.models.functions import Lower
from types import MethodType

from .models import (
    Address,
    Brand,
    ClientEquipment,
    Consumable,
    ConsumableAttachment,
    ConsumableCharacteristic,
    ConsumableCompatibility,
    EquipmentCharacteristicType,
    Organization,
    OrganizationAddress,
    OrganizationContact,
    Part,
    PartAttachment,
    PartCharacteristic,
    PartCompatibility,
    ProductCategory,
    ProductModel,
    ProductModelAttachment,
    ProductModelCharacteristic,
    ServiceCenter,
    ServiceCenterAddress,
    ServiceCenterContact,
    ServiceMan,
    StatusDirectory,
    WorkDirectory,
    WorkDirectoryConsumable,
    WorkDirectoryPart,
)


class OrganizationAddressInline(admin.TabularInline):
    model = OrganizationAddress
    extra = 0
    fields = ("address", "main_office")
    autocomplete_fields = ("address",)


class OrganizationContactInline(admin.TabularInline):
    model = OrganizationContact
    extra = 0
    fields = ("name", "position", "phone")


class ServiceCenterAddressInline(admin.TabularInline):
    model = ServiceCenterAddress
    extra = 0
    fields = ("address", "main_office")
    autocomplete_fields = ("address",)


class ServiceCenterContactInline(admin.TabularInline):
    model = ServiceCenterContact
    extra = 0
    fields = ("name", "position", "phone")


class ProductModelCharacteristicInline(admin.TabularInline):
    model = ProductModelCharacteristic
    extra = 0
    fields = ("characteristic_type", "value")
    autocomplete_fields = ("characteristic_type",)


class ProductModelAttachmentInline(admin.TabularInline):
    model = ProductModelAttachment
    extra = 0
    fields = ("title", "file", "uploaded_at")
    readonly_fields = ("uploaded_at",)


class ConsumableCharacteristicInline(admin.TabularInline):
    model = ConsumableCharacteristic
    extra = 0
    fields = ("characteristic_type", "value")
    autocomplete_fields = ("characteristic_type",)


class ConsumableCompatibilityInline(admin.TabularInline):
    model = ConsumableCompatibility
    extra = 0
    fields = ("product_model", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("product_model",)


class ConsumableAttachmentInline(admin.TabularInline):
    model = ConsumableAttachment
    extra = 0
    fields = ("title", "file", "uploaded_at")
    readonly_fields = ("uploaded_at",)


class PartCharacteristicInline(admin.TabularInline):
    model = PartCharacteristic
    extra = 0
    fields = ("characteristic_type", "value")
    autocomplete_fields = ("characteristic_type",)


class PartCompatibilityInline(admin.TabularInline):
    model = PartCompatibility
    extra = 0
    fields = ("product_model", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("product_model",)


class PartAttachmentInline(admin.TabularInline):
    model = PartAttachment
    extra = 0
    fields = ("title", "file", "uploaded_at")
    readonly_fields = ("uploaded_at",)


class WorkDirectoryConsumableInline(admin.TabularInline):
    model = WorkDirectoryConsumable
    extra = 0
    fields = ("consumable", "quantity")
    autocomplete_fields = ("consumable",)


class WorkDirectoryPartInline(admin.TabularInline):
    model = WorkDirectoryPart
    extra = 0
    fields = ("part", "quantity")
    autocomplete_fields = ("part",)


ADMIN_SECTION_ORDER = {
    "Контрагенты": 10,
    "Каталог оборудования": 20,
    "Сервис и работы": 30,
    "Адреса и статусы": 40,
}


ADMIN_MODEL_SECTIONS = {
    "Organization": "Контрагенты",
    "OrganizationAddress": "Контрагенты",
    "OrganizationContact": "Контрагенты",
    "ServiceCenter": "Контрагенты",
    "ServiceCenterAddress": "Контрагенты",
    "ServiceCenterContact": "Контрагенты",
    "ProductCategory": "Каталог оборудования",
    "Brand": "Каталог оборудования",
    "ProductModel": "Каталог оборудования",
    "EquipmentCharacteristicType": "Каталог оборудования",
    "ProductModelCharacteristic": "Каталог оборудования",
    "ProductModelAttachment": "Каталог оборудования",
    "Consumable": "Каталог оборудования",
    "ConsumableCharacteristic": "Каталог оборудования",
    "ConsumableCompatibility": "Каталог оборудования",
    "ConsumableAttachment": "Каталог оборудования",
    "Part": "Каталог оборудования",
    "PartCharacteristic": "Каталог оборудования",
    "PartCompatibility": "Каталог оборудования",
    "PartAttachment": "Каталог оборудования",
    "ServiceMan": "Сервис и работы",
    "WorkDirectory": "Сервис и работы",
    "WorkDirectoryConsumable": "Сервис и работы",
    "WorkDirectoryPart": "Сервис и работы",
    "ClientEquipment": "Сервис и работы",
    "Address": "Адреса и статусы",
    "StatusDirectory": "Адреса и статусы",
}


ADMIN_MODEL_ORDER = {
    "Organization": 10,
    "OrganizationAddress": 20,
    "OrganizationContact": 30,
    "ServiceCenter": 40,
    "ServiceCenterAddress": 50,
    "ServiceCenterContact": 60,
    "ProductCategory": 10,
    "Brand": 20,
    "ProductModel": 30,
    "EquipmentCharacteristicType": 40,
    "ProductModelCharacteristic": 50,
    "ProductModelAttachment": 60,
    "Consumable": 70,
    "ConsumableCharacteristic": 80,
    "ConsumableCompatibility": 90,
    "ConsumableAttachment": 100,
    "Part": 110,
    "PartCharacteristic": 120,
    "PartCompatibility": 130,
    "PartAttachment": 140,
    "ServiceMan": 10,
    "WorkDirectory": 20,
    "WorkDirectoryConsumable": 30,
    "WorkDirectoryPart": 40,
    "ClientEquipment": 50,
    "Address": 10,
    "StatusDirectory": 20,
}


class CaseInsensitiveSearchAdminMixin:
    search_config: tuple[tuple[str, str], ...] = ()

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not search_term or not self.search_config:
            return queryset, use_distinct

        lowered_term = search_term.lower()
        annotations = {alias: Lower(field) for alias, field in self.search_config}
        annotated_queryset = queryset.annotate(**annotations)

        condition = Q()
        for alias, _ in self.search_config:
            condition |= Q(**{f"{alias}__contains": lowered_term})

        return annotated_queryset.filter(condition).distinct(), True


class TimestampReadonlyAdminMixin:
    save_on_top = True
    list_per_page = 50
    show_full_result_count = False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        model_field_names = {field.name for field in self.model._meta.fields}
        for field_name in ("created_at", "updated_at", "uploaded_at"):
            if field_name in model_field_names and field_name not in readonly_fields:
                readonly_fields.append(field_name)
        return tuple(readonly_fields)


class SearchableAdminMixin(TimestampReadonlyAdminMixin, CaseInsensitiveSearchAdminMixin):
    pass


def _build_admin_sections(self, request, app_list):
    grouped_apps = []

    for app in app_list:
        if app["app_label"] != "services":
            grouped_apps.append(app)
            continue

        sections = {}
        for model_info in app["models"]:
            object_name = model_info.get("object_name")
            section_name = ADMIN_MODEL_SECTIONS.get(object_name, app["name"])
            sections.setdefault(section_name, []).append(model_info)

        for section_name, models in sorted(sections.items(), key=lambda item: ADMIN_SECTION_ORDER.get(item[0], 999)):
            grouped_apps.append(
                {
                    "name": section_name,
                    "app_label": f"services-{section_name.lower().replace(' ', '-')}",
                    "app_url": app["app_url"],
                    "has_module_perms": app["has_module_perms"],
                    "models": sorted(
                        models,
                        key=lambda model: (
                            ADMIN_MODEL_ORDER.get(model.get("object_name"), 999),
                            model["name"],
                        ),
                    ),
                }
            )

    return grouped_apps


def _grouped_get_app_list(self, request, app_label=None):
    app_list = admin.AdminSite.get_app_list(self, request, app_label)
    if app_label and app_label != "services":
        return app_list
    return _build_admin_sections(self, request, app_list)


admin.site.site_header = "Администрирование Services"
admin.site.site_title = "Services Admin"
admin.site.index_title = "Справочники и настройки"
admin.site.get_app_list = MethodType(_grouped_get_app_list, admin.site)


@admin.register(Organization)
class OrganizationAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "inn_kpp", "phone", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("name", "inn_kpp", "ogrn_passport", "phone", "email")
    ordering = ("name",)
    search_config = (
        ("name_lc", "name"),
        ("inn_kpp_lc", "inn_kpp"),
        ("ogrn_passport_lc", "ogrn_passport"),
        ("phone_lc", "phone"),
        ("email_lc", "email"),
    )
    inlines = [OrganizationAddressInline, OrganizationContactInline]


@admin.register(OrganizationAddress)
class OrganizationAddressAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("organization", "address", "main_office")
    list_filter = ("organization", "main_office")
    search_fields = ("organization__name", "address__locality", "address__street", "address__house")
    autocomplete_fields = ("organization", "address")
    list_select_related = ("organization", "address")


@admin.register(OrganizationContact)
class OrganizationContactAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "organization", "position", "phone", "created_at")
    list_filter = ("organization",)
    search_fields = ("name", "position", "phone", "organization__name")
    list_select_related = ("organization",)
    search_config = (
        ("name_lc", "name"),
        ("position_lc", "position"),
        ("phone_lc", "phone"),
        ("organization_name_lc", "organization__name"),
    )


@admin.register(ServiceCenter)
class ServiceCenterAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "inn_kpp", "phone", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("name", "inn_kpp", "ogrn_passport", "phone", "email")
    ordering = ("name",)
    search_config = (
        ("name_lc", "name"),
        ("inn_kpp_lc", "inn_kpp"),
        ("ogrn_passport_lc", "ogrn_passport"),
        ("phone_lc", "phone"),
        ("email_lc", "email"),
    )
    inlines = [ServiceCenterAddressInline, ServiceCenterContactInline]


@admin.register(ServiceCenterAddress)
class ServiceCenterAddressAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("service_center", "address", "main_office")
    list_filter = ("service_center", "main_office")
    search_fields = ("service_center__name", "address__locality", "address__street", "address__house")
    autocomplete_fields = ("service_center", "address")
    list_select_related = ("service_center", "address")


@admin.register(ServiceCenterContact)
class ServiceCenterContactAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "service_center", "position", "phone", "created_at")
    list_filter = ("service_center",)
    search_fields = ("name", "position", "phone", "service_center__name")
    list_select_related = ("service_center",)
    search_config = (
        ("name_lc", "name"),
        ("position_lc", "position"),
        ("phone_lc", "phone"),
        ("service_center_name_lc", "service_center__name"),
    )


@admin.register(ServiceMan)
class ServiceManAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("full_name", "phone", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("full_name", "phone")
    search_config = (
        ("full_name_lc", "full_name"),
        ("phone_lc", "phone"),
    )


@admin.register(ProductCategory)
class ProductCategoryAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "group", "updated_at")
    list_filter = ("group",)
    search_fields = ("name", "group")
    search_config = (
        ("name_lc", "name"),
        ("group_lc", "group"),
    )


@admin.register(Brand)
class BrandAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "site", "updated_at")
    search_fields = ("name", "site")
    search_config = (
        ("name_lc", "name"),
        ("site_lc", "site"),
    )


@admin.register(EquipmentCharacteristicType)
class EquipmentCharacteristicTypeAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "code", "value_kind", "sort_order", "updated_at")
    list_filter = ("value_kind",)
    ordering = ("sort_order", "name", "id")
    search_fields = ("name", "code")
    search_config = (
        ("name_lc", "name"),
        ("code_lc", "code"),
    )


@admin.register(ProductModel)
class ProductModelAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "brand", "category", "sku", "updated_at")
    list_filter = ("brand", "category")
    search_fields = ("name", "sku", "brand__name", "category__name")
    list_select_related = ("brand", "category")
    search_config = (
        ("name_lc", "name"),
        ("sku_lc", "sku"),
        ("brand_name_lc", "brand__name"),
        ("category_name_lc", "category__name"),
    )
    autocomplete_fields = ("brand", "category")
    inlines = [ProductModelCharacteristicInline, ProductModelAttachmentInline]


@admin.register(ProductModelCharacteristic)
class ProductModelCharacteristicAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("product_model", "characteristic_type", "value", "updated_at")
    list_filter = ("characteristic_type",)
    search_fields = ("product_model__name", "characteristic_type__name", "value")
    autocomplete_fields = ("product_model", "characteristic_type")
    list_select_related = ("product_model", "characteristic_type")


@admin.register(ProductModelAttachment)
class ProductModelAttachmentAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("display_name", "product_model", "uploaded_at")
    search_fields = ("title", "product_model__name", "file")
    autocomplete_fields = ("product_model",)
    list_select_related = ("product_model",)


@admin.register(Consumable)
class ConsumableAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "brand", "category", "sku", "updated_at")
    list_filter = ("brand", "category")
    search_fields = ("name", "sku", "brand__name", "category__name")
    list_select_related = ("brand", "category")
    search_config = (
        ("name_lc", "name"),
        ("sku_lc", "sku"),
        ("brand_name_lc", "brand__name"),
        ("category_name_lc", "category__name"),
    )
    autocomplete_fields = ("brand", "category")
    inlines = [ConsumableCharacteristicInline, ConsumableCompatibilityInline, ConsumableAttachmentInline]


@admin.register(ConsumableCharacteristic)
class ConsumableCharacteristicAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("consumable", "characteristic_type", "value", "updated_at")
    list_filter = ("characteristic_type",)
    search_fields = ("consumable__name", "characteristic_type__name", "value")
    autocomplete_fields = ("consumable", "characteristic_type")
    list_select_related = ("consumable", "characteristic_type")


@admin.register(ConsumableCompatibility)
class ConsumableCompatibilityAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("consumable", "product_model", "created_at")
    list_filter = ("consumable__brand", "product_model__brand")
    search_fields = ("consumable__name", "product_model__name", "product_model__brand__name")
    autocomplete_fields = ("consumable", "product_model")
    list_select_related = ("consumable", "product_model", "product_model__brand")


@admin.register(ConsumableAttachment)
class ConsumableAttachmentAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("display_name", "consumable", "uploaded_at")
    search_fields = ("title", "consumable__name", "file")
    autocomplete_fields = ("consumable",)
    list_select_related = ("consumable",)


@admin.register(Part)
class PartAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "brand", "category", "sku", "updated_at")
    list_filter = ("brand", "category")
    search_fields = ("name", "sku", "brand__name", "category__name")
    list_select_related = ("brand", "category")
    search_config = (
        ("name_lc", "name"),
        ("sku_lc", "sku"),
        ("brand_name_lc", "brand__name"),
        ("category_name_lc", "category__name"),
    )
    autocomplete_fields = ("brand", "category")
    inlines = [PartCharacteristicInline, PartCompatibilityInline, PartAttachmentInline]


@admin.register(PartCharacteristic)
class PartCharacteristicAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("part", "characteristic_type", "value", "updated_at")
    list_filter = ("characteristic_type",)
    search_fields = ("part__name", "characteristic_type__name", "value")
    autocomplete_fields = ("part", "characteristic_type")
    list_select_related = ("part", "characteristic_type")


@admin.register(PartCompatibility)
class PartCompatibilityAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("part", "product_model", "created_at")
    list_filter = ("part__brand", "product_model__brand")
    search_fields = ("part__name", "product_model__name", "product_model__brand__name")
    autocomplete_fields = ("part", "product_model")
    list_select_related = ("part", "product_model", "product_model__brand")


@admin.register(PartAttachment)
class PartAttachmentAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("display_name", "part", "uploaded_at")
    search_fields = ("title", "part__name", "file")
    autocomplete_fields = ("part",)
    list_select_related = ("part",)


@admin.register(WorkDirectory)
class WorkDirectoryAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("code", "name", "unit_price", "updated_at")
    search_fields = ("code", "name")
    search_config = (
        ("code_lc", "code"),
        ("name_lc", "name"),
    )
    inlines = [WorkDirectoryConsumableInline, WorkDirectoryPartInline]


@admin.register(WorkDirectoryConsumable)
class WorkDirectoryConsumableAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("work", "consumable", "quantity", "created_at")
    list_filter = ("work",)
    search_fields = ("work__code", "work__name", "consumable__name")
    autocomplete_fields = ("work", "consumable")
    list_select_related = ("work", "consumable")


@admin.register(WorkDirectoryPart)
class WorkDirectoryPartAdmin(TimestampReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ("work", "part", "quantity", "created_at")
    list_filter = ("work",)
    search_fields = ("work__code", "work__name", "part__name")
    autocomplete_fields = ("work", "part")
    list_select_related = ("work", "part")


@admin.register(Address)
class AddressAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("locality", "street", "house", "postal_code", "updated_at")
    search_fields = ("postal_code", "locality", "street", "house", "building", "structure", "room", "note")
    search_config = (
        ("postal_code_lc", "postal_code"),
        ("locality_lc", "locality"),
        ("street_lc", "street"),
        ("house_lc", "house"),
        ("building_lc", "building"),
        ("structure_lc", "structure"),
        ("room_lc", "room"),
        ("note_lc", "note"),
    )


@admin.register(StatusDirectory)
class StatusDirectoryAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("code", "name", "updated_at")
    search_fields = ("name", "description")
    search_config = (
        ("name_lc", "name"),
        ("description_lc", "description"),
    )


@admin.register(ClientEquipment)
class ClientEquipmentAdmin(SearchableAdminMixin, admin.ModelAdmin):
    list_display = ("organization", "product_model", "serial_number", "inventory_number", "print_counter", "updated_at")
    list_filter = ("organization", "product_model__brand", "product_model__category")
    search_fields = ("organization__name", "product_model__name", "serial_number", "inventory_number")
    search_config = (
        ("organization_name_lc", "organization__name"),
        ("product_model_name_lc", "product_model__name"),
        ("serial_number_lc", "serial_number"),
        ("inventory_number_lc", "inventory_number"),
    )
    autocomplete_fields = ("organization", "product_model")
    list_select_related = ("organization", "product_model", "product_model__brand", "product_model__category")


try:
    admin.site.unregister(User)
except NotRegistered:
    pass


try:
    admin.site.unregister(Group)
except NotRegistered:
    pass


@admin.register(User)
class CustomUserAdmin(CaseInsensitiveSearchAdminMixin, UserAdmin):
    search_config = (
        ("username_lc", "username"),
        ("first_name_lc", "first_name"),
        ("last_name_lc", "last_name"),
        ("email_lc", "email"),
    )


@admin.register(Group)
class CustomGroupAdmin(CaseInsensitiveSearchAdminMixin, GroupAdmin):
    search_config = (("name_lc", "name"),)