from pathlib import Path

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import (
    AcceptanceDocument,
    AcceptanceDocumentEquipment,
    ATTACHMENT_ALLOWED_EXTENSIONS,
    Address,
    Brand,
    ClientEquipment,
    Consumable,
    EquipmentCharacteristicType,
    Organization,
    OrganizationContact,
    Part,
    ProductCategory,
    ProductModel,
    RepairDocument,
    RepairDocumentConsumable,
    RepairDocumentPart,
    RepairDocumentWork,
    ShipmentDocument,
    ShipmentDocumentEquipment,
    ServiceCenter,
    ServiceCenterAddress,
    ServiceCenterContact,
    ServiceMan,
    StatusDirectory,
    WorkDirectory,
)


class AdminUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all().order_by("name"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        label="Группы",
    )

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "password1", "password2", "groups")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email", "")
        if commit:
            user.save()
        return user


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)
        labels = {"name": "Название группы"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Например, Менеджеры"})


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ("name", "inn_kpp", "ogrn_passport", "phone", "email", "status")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "inn_kpp": forms.TextInput(attrs={"class": "form-control"}),
            "ogrn_passport": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class OrganizationContactForm(forms.ModelForm):
    class Meta:
        model = OrganizationContact
        fields = ("name", "position", "phone")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }


class ServiceCenterForm(forms.ModelForm):
    class Meta:
        model = ServiceCenter
        fields = ("name", "inn_kpp", "ogrn_passport", "phone", "email", "status")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "inn_kpp": forms.TextInput(attrs={"class": "form-control"}),
            "ogrn_passport": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class ServiceCenterContactForm(forms.ModelForm):
    class Meta:
        model = ServiceCenterContact
        fields = ("name", "position", "phone")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }


class ServiceManForm(forms.ModelForm):
    class Meta:
        model = ServiceMan
        fields = ("full_name", "phone", "status")
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ("name", "group")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "group": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, ПК, Ноутбуки, МФУ/Копиры"}),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ("name", "site")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "site": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://example.com"}),
        }


class EquipmentCharacteristicTypeForm(forms.ModelForm):
    class Meta:
        model = EquipmentCharacteristicType
        fields = ("code", "name", "value_kind", "sort_order")
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, weight"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, Вес"}),
            "value_kind": forms.Select(attrs={"class": "form-select"}),
            "sort_order": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ("name", "site", "catalog_url", "category", "brand", "sku")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "site": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://example.com/product"}),
            "catalog_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://example.com/catalog-folder"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "brand": forms.Select(attrs={"class": "form-select"}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = ProductCategory.objects.all().order_by("group", "name")
        self.fields["category"].empty_label = "— не выбрана —"
        self.fields["brand"].queryset = Brand.objects.all().order_by("name")
        self.fields["brand"].empty_label = "— не выбран —"


class ConsumableForm(forms.ModelForm):
    class Meta:
        model = Consumable
        fields = ("name", "site", "catalog_url", "category", "brand", "sku")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "site": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://example.com/product"}),
            "catalog_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://example.com/catalog-folder"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "brand": forms.Select(attrs={"class": "form-select"}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = ProductCategory.objects.all().order_by("group", "name")
        self.fields["category"].empty_label = "— не выбрана —"
        self.fields["brand"].queryset = Brand.objects.all().order_by("name")
        self.fields["brand"].empty_label = "— не выбран —"


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ("name", "site", "catalog_url", "category", "brand", "sku")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "site": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://example.com/product"}),
            "catalog_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://example.com/catalog-folder"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "brand": forms.Select(attrs={"class": "form-select"}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = ProductCategory.objects.all().order_by("group", "name")
        self.fields["category"].empty_label = "— не выбрана —"
        self.fields["brand"].queryset = Brand.objects.all().order_by("name")
        self.fields["brand"].empty_label = "— не выбран —"


class WorkDirectoryForm(forms.ModelForm):
    class Meta:
        model = WorkDirectory
        fields = ("code", "name", "unit_price")
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, WRK-001"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Наименование работы"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
        }

    def clean_code(self):
        code = (self.cleaned_data.get("code") or "").strip().upper()
        if not code:
            return code

        existing_qs = WorkDirectory.objects.filter(code__iexact=code)
        if self.instance and self.instance.pk:
            existing_qs = existing_qs.exclude(pk=self.instance.pk)

        if existing_qs.exists():
            raise forms.ValidationError("Работа с таким кодом уже существует.")
        return code


class CatalogAttachmentForm(forms.Form):
    title = forms.CharField(
        label="Название файла",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Необязательно"}),
    )
    file = forms.FileField(
        label="Файл",
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".pdf,image/*"}),
    )

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        extension = Path(uploaded_file.name).suffix.lower().lstrip(".")
        if extension not in ATTACHMENT_ALLOWED_EXTENSIONS:
            raise forms.ValidationError("Допустимы только изображения и PDF.")
        return uploaded_file


class StatusDirectoryForm(forms.ModelForm):
    class Meta:
        model = StatusDirectory
        fields = ("code", "name", "description")
        widgets = {
            "code": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Например, 10"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, Получено"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Описание статуса"}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("postal_code", "locality", "street", "house", "building", "structure", "floor", "room", "note")
        widgets = {
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, 101000"}),
            "locality": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, Москва"}),
            "street": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, Тверская"}),
            "house": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, 12"}),
            "building": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, 1"}),
            "structure": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, 2"}),
            "floor": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, 3"}),
            "room": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, 305"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Примечание"}),
        }


class AcceptanceDocumentForm(forms.ModelForm):
    class Meta:
        model = AcceptanceDocument
        fields = ("date", "serviceman", "organization")
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "serviceman": forms.Select(attrs={"class": "form-select"}),
            "organization": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["serviceman"].queryset = ServiceMan.objects.all().order_by("full_name")
        self.fields["serviceman"].required = True
        self.fields["organization"].queryset = Organization.objects.all().order_by("name")

        if self.instance and self.instance.pk:
            self.fields["date"].disabled = True
            self.fields["date"].required = False

    def clean_date(self):
        if self.instance and self.instance.pk:
            return self.instance.date
        return self.cleaned_data.get("date")


class ShipmentDocumentForm(forms.ModelForm):
    class Meta:
        model = ShipmentDocument
        fields = ("date", "serviceman", "organization")
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "serviceman": forms.Select(attrs={"class": "form-select"}),
            "organization": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["serviceman"].queryset = ServiceMan.objects.all().order_by("full_name")
        self.fields["serviceman"].required = True
        self.fields["organization"].queryset = Organization.objects.all().order_by("name")

        if self.instance and self.instance.pk:
            self.fields["date"].disabled = True
            self.fields["date"].required = False

    def clean_date(self):
        if self.instance and self.instance.pk:
            return self.instance.date
        return self.cleaned_data.get("date")


class AcceptanceEquipmentCreateForm(forms.ModelForm):
    class Meta:
        model = ClientEquipment
        fields = ("product_model", "serial_number", "inventory_number", "print_counter")
        widgets = {
            "product_model": forms.Select(attrs={"class": "form-select"}),
            "serial_number": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "inventory_number": forms.TextInput(attrs={"class": "form-control"}),
            "print_counter": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product_model"].queryset = ProductModel.objects.select_related("brand").all().order_by("name")
        self.fields["product_model"].empty_label = "— не выбрана —"

    def clean(self):
        cleaned_data = super().clean()

        temp_instance = self.instance if self.instance.pk else ClientEquipment()
        temp_instance.organization_id = getattr(self, "_organization_id", None)
        temp_instance.serial_number = cleaned_data.get("serial_number", "")
        temp_instance.inventory_number = cleaned_data.get("inventory_number", "")
        temp_instance.product_model = cleaned_data.get("product_model")

        try:
            temp_instance.clean()
        except forms.ValidationError as error:
            for field, message in error.message_dict.items():
                self.add_error(field, message)

        return cleaned_data


class RepairDocumentForm(forms.ModelForm):
    class Meta:
        model = RepairDocument
        fields = (
            "date",
            "repair_place",
            "service_center",
            "service_center_address",
            "organization",
            "serviceman",
            "status",
            "client_equipment",
            "malfunction",
            "work_performed",
            "note",
        )
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "repair_place": forms.RadioSelect(),
            "service_center": forms.Select(attrs={"class": "form-select"}),
            "service_center_address": forms.Select(attrs={"class": "form-select"}),
            "organization": forms.Select(attrs={"class": "form-select"}),
            "serviceman": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "client_equipment": forms.Select(attrs={"class": "form-select"}),
            "malfunction": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "work_performed": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service_center"].queryset = ServiceCenter.objects.all().order_by("name")
        self.fields["organization"].queryset = Organization.objects.all().order_by("name")
        self.fields["serviceman"].queryset = ServiceMan.objects.all().order_by("full_name")
        self.fields["status"].queryset = StatusDirectory.objects.all().order_by("code")
        self.fields["service_center_address"].empty_label = "— не выбран —"
        self.fields["client_equipment"].empty_label = "— не выбрана —"

        # Дата документа фиксируется после создания и не должна изменяться при редактировании.
        if self.instance and self.instance.pk:
            self.fields["date"].disabled = True
            self.fields["date"].required = False

        organization_id = None
        service_center_id = None

        if self.is_bound:
            posted_service_center = self.data.get("service_center")
            if posted_service_center and str(posted_service_center).isdigit():
                service_center_id = int(posted_service_center)
        elif self.initial.get("service_center"):
            initial_service_center = self.initial.get("service_center")
            if hasattr(initial_service_center, "id"):
                service_center_id = initial_service_center.id
            elif str(initial_service_center).isdigit():
                service_center_id = int(initial_service_center)
        elif self.instance and self.instance.pk and self.instance.service_center_id:
            service_center_id = self.instance.service_center_id

        if self.is_bound:
            posted_organization = self.data.get("organization")
            if posted_organization and str(posted_organization).isdigit():
                organization_id = int(posted_organization)
        elif self.initial.get("organization"):
            initial_organization = self.initial.get("organization")
            if hasattr(initial_organization, "id"):
                organization_id = initial_organization.id
            elif str(initial_organization).isdigit():
                organization_id = int(initial_organization)
        elif self.instance and self.instance.pk and self.instance.organization_id:
            organization_id = self.instance.organization_id

        if organization_id:
            self.fields["client_equipment"].queryset = ClientEquipment.objects.select_related("product_model", "organization").filter(
                organization_id=organization_id
            ).order_by("product_model__name", "id")
        else:
            self.fields["client_equipment"].queryset = ClientEquipment.objects.none()

        if service_center_id:
            self.fields["service_center_address"].queryset = Address.objects.filter(
                service_center_links__service_center_id=service_center_id
            ).order_by("locality", "street", "house", "id")
        else:
            self.fields["service_center_address"].queryset = Address.objects.none()

        if not self.is_bound and service_center_id:
            current_address_id = self.initial.get("service_center_address")
            if not current_address_id and self.instance and self.instance.pk:
                current_address_id = self.instance.service_center_address_id

            current_address_valid = False
            if current_address_id:
                current_address_valid = self.fields["service_center_address"].queryset.filter(id=current_address_id).exists()

            if not current_address_valid:
                main_office_link = ServiceCenterAddress.objects.filter(
                    service_center_id=service_center_id,
                    main_office=True,
                ).select_related("address").first()
                if main_office_link:
                    self.initial["service_center_address"] = main_office_link.address_id
                    self.fields["service_center_address"].initial = main_office_link.address_id

    def clean_date(self):
        if self.instance and self.instance.pk:
            return self.instance.date
        return self.cleaned_data.get("date")


class ClientEquipmentForm(forms.ModelForm):
    class Meta:
        model = ClientEquipment
        fields = ("organization", "product_model", "serial_number", "inventory_number", "print_counter")
        widgets = {
            "organization": forms.Select(attrs={"class": "form-select"}),
            "product_model": forms.Select(attrs={"class": "form-select"}),
            "serial_number": forms.TextInput(attrs={"class": "form-control"}),
            "inventory_number": forms.TextInput(attrs={"class": "form-control"}),
            "print_counter": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["organization"].queryset = Organization.objects.all().order_by("name")
        self.fields["organization"].empty_label = "— выберите организацию —"
        self.fields["product_model"].queryset = ProductModel.objects.select_related("brand").all().order_by("name")
        self.fields["product_model"].empty_label = "— не выбрана —"


class RepairDocumentPartForm(forms.ModelForm):
    class Meta:
        model = RepairDocumentPart
        fields = ("part", "quantity")
        widgets = {
            "part": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["part"].queryset = Part.objects.select_related("brand").all().order_by("name")


class RepairDocumentConsumableForm(forms.ModelForm):
    class Meta:
        model = RepairDocumentConsumable
        fields = ("consumable", "quantity")
        widgets = {
            "consumable": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["consumable"].queryset = Consumable.objects.select_related("brand").all().order_by("name")


class RepairDocumentWorkForm(forms.ModelForm):
    class Meta:
        model = RepairDocumentWork
        fields = ("work", "quantity")
        widgets = {
            "work": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["work"].queryset = WorkDirectory.objects.all().order_by("code", "name")
