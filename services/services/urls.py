"""
URL configuration for services project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/logo.jpg", views.home_logo, name="home_logo"),
    path("style/", views.style_settings, name="style_settings"),
    path("style/select/<slug:theme_key>/", views.style_select, name="style_select"),
    path("style/assets/<slug:theme_key>/<path:asset_path>", views.theme_asset, name="theme_asset"),
    path("profile/", views.profile, name="profile"),
    path("organizations/", views.organizations, name="organizations"),
    path("service-centers/", views.service_centers, name="service_centers"),
    path("contacts/", views.contacts, name="contacts"),
    path("serviceman/", views.serviceman, name="serviceman"),
    path("serviceman/<int:serviceman_id>/delete/", views.serviceman_delete, name="serviceman_delete"),
    path("product-category/", views.product_category, name="product_category"),
    path("product-category/<int:category_id>/delete/", views.product_category_delete, name="product_category_delete"),
    path("brand/", views.brand, name="brand"),
    path("brand/<int:brand_id>/delete/", views.brand_delete, name="brand_delete"),
    path("product-model/", views.product_model, name="product_model"),
    path("product-model/new/", views.product_model_edit, name="product_model_new"),
    path("product-model/<int:model_id>/", views.product_model_edit, name="product_model_edit"),
    path("product-model/<int:model_id>/consumables/", views.product_model_consumables, name="product_model_consumables"),
    path("product-model/<int:model_id>/parts/", views.product_model_parts, name="product_model_parts"),
    path("product-model/<int:model_id>/delete/", views.product_model_delete, name="product_model_delete"),
    path("equipment-characteristics/", views.equipment_characteristic_type, name="equipment_characteristic_type"),
    path("characteristics/", views.equipment_characteristic_type, name="characteristic_directory"),
    path("consumable/", views.consumable, name="consumable"),
    path("consumable/new/", views.consumable_edit, name="consumable_new"),
    path("consumable/<int:consumable_id>/", views.consumable_edit, name="consumable_edit"),
    path("consumable/<int:consumable_id>/models/", views.consumable_product_models, name="consumable_product_models"),
    path("consumable/<int:consumable_id>/delete/", views.consumable_delete, name="consumable_delete"),
    path("part/", views.part, name="part"),
    path("part/new/", views.part_edit, name="part_new"),
    path("part/<int:part_id>/", views.part_edit, name="part_edit"),
    path("part/<int:part_id>/models/", views.part_product_models, name="part_product_models"),
    path("part/<int:part_id>/delete/", views.part_delete, name="part_delete"),
    path("work-directory/", views.work_directory, name="work_directory"),
    path("work-directory/new/", views.work_directory_edit, name="work_directory_new"),
    path("work-directory/<int:work_id>/", views.work_directory_edit, name="work_directory_edit"),
    path("work-directory/<int:work_id>/delete/", views.work_directory_delete, name="work_directory_delete"),
    path("statuses/", views.status_directory, name="status_directory"),
    path("statuses/<int:status_id>/delete/", views.status_directory_delete, name="status_directory_delete"),
    path("addresses/", views.address_directory, name="address_directory"),
    path("addresses/<int:address_id>/delete/", views.address_directory_delete, name="address_directory_delete"),
    path("documents/repair/", views.repair_document, name="repair_document"),
    path("documents/repair/new/", views.repair_document_edit, name="repair_document_new"),
    path("documents/repair/equipment/<int:equipment_id>/history/", views.repair_document_equipment_history, name="repair_document_equipment_history"),
    path("documents/repair/<int:document_id>/view/", views.repair_document_view, name="repair_document_view"),
    path("documents/repair/<int:document_id>/", views.repair_document_edit, name="repair_document_edit"),
    path("documents/repair/<int:document_id>/delete/", views.repair_document_delete, name="repair_document_delete"),
    path("documents/acceptance/", views.acceptance_document, name="acceptance_document"),
    path("documents/acceptance/new/", views.acceptance_document_edit, name="acceptance_document_new"),
    path("documents/acceptance/<int:document_id>/", views.acceptance_document_edit, name="acceptance_document_edit"),
    path("documents/acceptance/<int:document_id>/add-equipment/", views.acceptance_document_add_equipment, name="acceptance_document_add_equipment"),
    path("documents/shipment/", views.shipment_document, name="shipment_document"),
    path("documents/shipment/new/", views.shipment_document_edit, name="shipment_document_new"),
    path("documents/shipment/<int:document_id>/", views.shipment_document_edit, name="shipment_document_edit"),
    path("reports/acceptance/", views.report_acceptance_document, name="report_acceptance_document"),
    path("reports/shipment/", views.report_shipment_document, name="report_shipment_document"),
    path("reports/repair/", views.report_repair_document, name="report_repair_document"),
    path("reports/part/", views.report_part, name="report_part"),
    path("reports/consumable/", views.report_consumable, name="report_consumable"),
    path("reports/work-directory/", views.report_work_directory, name="report_work_directory"),
    path("reports/address/", views.report_address_directory, name="report_address_directory"),
    path("reports/brand/", views.report_brand, name="report_brand"),
    path("reports/status/", views.report_status_directory, name="report_status_directory"),
    path("reports/product-category/", views.report_product_category, name="report_product_category"),
    path("reports/characteristics/", views.report_characteristics, name="report_characteristics"),
    path("service/exchange/", views.service_exchange, name="service_exchange"),
    path("service/exchange/log/<int:log_id>/download/", views.service_exchange_log_download, name="service_exchange_log_download"),
    path("client-equipment/", views.client_equipment, name="client_equipment"),
    path("client-equipment/<int:equipment_id>/delete/", views.client_equipment_delete, name="client_equipment_delete"),
    path("planned-visit/", views.planned_visit, name="planned_visit"),
    path("planned-visit/<int:visit_id>/delete/", views.planned_visit_delete, name="planned_visit_delete"),
    path("api/egrul-lookup/", views.egrul_lookup, name="egrul_lookup"),
    path("users/", views.users, name="users"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("admin/", admin.site.urls),
]
