from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Organization, OrganizationContact


class OrganizationContactInline(admin.TabularInline):
    model = OrganizationContact
    extra = 1
    fields = ("name", "position", "phone")


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


@admin.register(Organization)
class OrganizationAdmin(CaseInsensitiveSearchAdminMixin, admin.ModelAdmin):
    list_display = ("name", "inn_kpp", "phone", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("name", "inn_kpp", "ogrn_passport", "phone", "email")
    search_config = (
        ("name_lc", "name"),
        ("inn_kpp_lc", "inn_kpp"),
        ("ogrn_passport_lc", "ogrn_passport"),
        ("phone_lc", "phone"),
        ("email_lc", "email"),
    )
    inlines = [OrganizationContactInline]


@admin.register(OrganizationContact)
class OrganizationContactAdmin(CaseInsensitiveSearchAdminMixin, admin.ModelAdmin):
    list_display = ("name", "organization", "position", "phone", "created_at")
    list_filter = ("organization",)
    search_fields = ("name", "position", "phone", "organization__name")
    search_config = (
        ("name_lc", "name"),
        ("position_lc", "position"),
        ("phone_lc", "phone"),
        ("organization_name_lc", "organization__name"),
    )


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