# Services Project Documentation

Generated: 30.04.2026 01:00:45

## Summary

- Models: 38
- Views: 63
- Forms: 25
- Admin classes: 6
- URL patterns: 75
- Templates: 54

## Models

### AcceptanceDocument

| Field | Type |
|---|---|
| equipment_links | ManyToOneRel |
| id | BigAutoField |
| date | DateField |
| serviceman | ForeignKey |
| organization | ForeignKey |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### AcceptanceDocumentEquipment

| Field | Type |
|---|---|
| id | BigAutoField |
| acceptance_document | ForeignKey |
| client_equipment | ForeignKey |
| repair_document | OneToOneField |
| created_at | DateTimeField |

### Address

| Field | Type |
|---|---|
| organizations | ManyToManyRel |
| organization_links | ManyToOneRel |
| service_centers | ManyToManyRel |
| service_center_links | ManyToOneRel |
| repair_documents_as_service_center_address | ManyToOneRel |
| id | BigAutoField |
| postal_code | CharField |
| locality | CharField |
| street | CharField |
| house | CharField |
| building | CharField |
| structure | CharField |
| floor | CharField |
| room | CharField |
| note | TextField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### Brand

| Field | Type |
|---|---|
| product_models | ManyToOneRel |
| consumables | ManyToOneRel |
| parts | ManyToOneRel |
| id | BigAutoField |
| name | CharField |
| site | URLField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### CatalogAttachmentBase

| Field | Type |
|---|---|
| title | CharField |
| file | FileField |
| uploaded_at | DateTimeField |

### CatalogReferenceMixin

| Field | Type |
|---|---|
| catalog_url | URLField |

### ClientEquipment

| Field | Type |
|---|---|
| repair_documents | ManyToOneRel |
| acceptance_links | ManyToOneRel |
| shipment_links | ManyToOneRel |
| id | BigAutoField |
| organization | ForeignKey |
| product_model | ForeignKey |
| serial_number | CharField |
| inventory_number | CharField |
| print_counter | PositiveIntegerField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### Consumable

| Field | Type |
|---|---|
| characteristics | ManyToOneRel |
| compatibilities | ManyToOneRel |
| attachments | ManyToOneRel |
| work_links | ManyToOneRel |
| repair_document_links | ManyToOneRel |
| id | BigAutoField |
| catalog_url | URLField |
| name | CharField |
| site | URLField |
| category | ForeignKey |
| brand | ForeignKey |
| sku | CharField |
| created_at | DateTimeField |
| updated_at | DateTimeField |
| compatible_models | ManyToManyField |

### ConsumableAttachment

| Field | Type |
|---|---|
| id | BigAutoField |
| title | CharField |
| file | FileField |
| uploaded_at | DateTimeField |
| consumable | ForeignKey |

### ConsumableCharacteristic

| Field | Type |
|---|---|
| id | BigAutoField |
| consumable | ForeignKey |
| characteristic_type | ForeignKey |
| value | CharField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### ConsumableCompatibility

| Field | Type |
|---|---|
| id | BigAutoField |
| consumable | ForeignKey |
| product_model | ForeignKey |
| created_at | DateTimeField |

### EquipmentCharacteristicType

| Field | Type |
|---|---|
| values | ManyToOneRel |
| consumable_values | ManyToOneRel |
| part_values | ManyToOneRel |
| id | BigAutoField |
| code | CharField |
| name | CharField |
| value_kind | CharField |
| sort_order | PositiveSmallIntegerField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### Organization

| Field | Type |
|---|---|
| address_links | ManyToOneRel |
| contacts | ManyToOneRel |
| client_equipments | ManyToOneRel |
| repair_documents | ManyToOneRel |
| acceptance_documents | ManyToOneRel |
| shipment_documents | ManyToOneRel |
| id | BigAutoField |
| inn_kpp | CharField |
| ogrn_passport | CharField |
| name | CharField |
| phone | CharField |
| email | EmailField |
| status | CharField |
| created_at | DateTimeField |
| updated_at | DateTimeField |
| addresses | ManyToManyField |

### OrganizationAddress

| Field | Type |
|---|---|
| id | BigAutoField |
| organization | ForeignKey |
| address | ForeignKey |
| main_office | BooleanField |

### OrganizationContact

| Field | Type |
|---|---|
| id | BigAutoField |
| organization | ForeignKey |
| name | CharField |
| position | CharField |
| phone | CharField |
| created_at | DateTimeField |

### Part

| Field | Type |
|---|---|
| characteristics | ManyToOneRel |
| attachments | ManyToOneRel |
| compatibilities | ManyToOneRel |
| work_links | ManyToOneRel |
| repair_document_links | ManyToOneRel |
| id | BigAutoField |
| catalog_url | URLField |
| name | CharField |
| site | URLField |
| category | ForeignKey |
| brand | ForeignKey |
| sku | CharField |
| created_at | DateTimeField |
| updated_at | DateTimeField |
| compatible_models | ManyToManyField |

### PartAttachment

| Field | Type |
|---|---|
| id | BigAutoField |
| title | CharField |
| file | FileField |
| uploaded_at | DateTimeField |
| part | ForeignKey |

### PartCharacteristic

| Field | Type |
|---|---|
| id | BigAutoField |
| part | ForeignKey |
| characteristic_type | ForeignKey |
| value | CharField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### PartCompatibility

| Field | Type |
|---|---|
| id | BigAutoField |
| part | ForeignKey |
| product_model | ForeignKey |
| created_at | DateTimeField |

### ProductCategory

| Field | Type |
|---|---|
| product_models | ManyToOneRel |
| consumables | ManyToOneRel |
| parts | ManyToOneRel |
| id | BigAutoField |
| name | CharField |
| group | CharField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### ProductModel

| Field | Type |
|---|---|
| characteristics | ManyToOneRel |
| compatible_consumables | ManyToManyRel |
| consumable_links | ManyToOneRel |
| compatible_parts | ManyToManyRel |
| attachments | ManyToOneRel |
| part_links | ManyToOneRel |
| client_equipments | ManyToOneRel |
| id | BigAutoField |
| catalog_url | URLField |
| name | CharField |
| site | URLField |
| category | ForeignKey |
| brand | ForeignKey |
| device_type | CharField |
| color | CharField |
| format_print | CharField |
| speed_print | PositiveIntegerField |
| sku | CharField |
| weight | CharField |
| dimensions | CharField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### ProductModelAttachment

| Field | Type |
|---|---|
| id | BigAutoField |
| title | CharField |
| file | FileField |
| uploaded_at | DateTimeField |
| product_model | ForeignKey |

### ProductModelCharacteristic

| Field | Type |
|---|---|
| id | BigAutoField |
| product_model | ForeignKey |
| characteristic_type | ForeignKey |
| value | CharField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### RepairDocument

| Field | Type |
|---|---|
| status_revisions | ManyToOneRel |
| work_links | ManyToOneRel |
| acceptance_equipment_link | OneToOneRel |
| shipment_equipment_link | OneToOneRel |
| part_links | ManyToOneRel |
| consumable_links | ManyToOneRel |
| id | BigAutoField |
| date | DateField |
| repair_place | CharField |
| service_center | ForeignKey |
| service_center_address | ForeignKey |
| organization | ForeignKey |
| serviceman | ForeignKey |
| status | ForeignKey |
| client_equipment | ForeignKey |
| source_document | ForeignKey |
| status_edited_at | DateTimeField |
| malfunction | TextField |
| work_performed | TextField |
| note | TextField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### RepairDocumentConsumable

| Field | Type |
|---|---|
| id | BigAutoField |
| repair_document | ForeignKey |
| consumable | ForeignKey |
| manual_quantity | PositiveIntegerField |
| work_quantity | PositiveIntegerField |
| quantity | PositiveIntegerField |
| created_at | DateTimeField |

### RepairDocumentPart

| Field | Type |
|---|---|
| id | BigAutoField |
| repair_document | ForeignKey |
| part | ForeignKey |
| manual_quantity | PositiveIntegerField |
| work_quantity | PositiveIntegerField |
| quantity | PositiveIntegerField |
| created_at | DateTimeField |

### RepairDocumentWork

| Field | Type |
|---|---|
| id | BigAutoField |
| repair_document | ForeignKey |
| work | ForeignKey |
| quantity | PositiveIntegerField |
| created_at | DateTimeField |

### ServiceCenter

| Field | Type |
|---|---|
| address_links | ManyToOneRel |
| contacts | ManyToOneRel |
| repair_documents | ManyToOneRel |
| id | BigAutoField |
| inn_kpp | CharField |
| ogrn_passport | CharField |
| name | CharField |
| phone | CharField |
| email | EmailField |
| status | CharField |
| created_at | DateTimeField |
| updated_at | DateTimeField |
| addresses | ManyToManyField |

### ServiceCenterAddress

| Field | Type |
|---|---|
| id | BigAutoField |
| service_center | ForeignKey |
| address | ForeignKey |
| main_office | BooleanField |

### ServiceCenterContact

| Field | Type |
|---|---|
| id | BigAutoField |
| service_center | ForeignKey |
| name | CharField |
| position | CharField |
| phone | CharField |
| created_at | DateTimeField |

### ServiceExchangeLog

| Field | Type |
|---|---|
| id | BigAutoField |
| user | ForeignKey |
| action | CharField |
| section | CharField |
| result_status | CharField |
| dry_run | BooleanField |
| file_name | CharField |
| selected_keys | JSONField |
| summary | JSONField |
| message | TextField |
| created_at | DateTimeField |

### ServiceMan

| Field | Type |
|---|---|
| repair_documents | ManyToOneRel |
| acceptance_documents | ManyToOneRel |
| shipment_documents | ManyToOneRel |
| id | BigAutoField |
| full_name | CharField |
| phone | CharField |
| status | CharField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### ShipmentDocument

| Field | Type |
|---|---|
| equipment_links | ManyToOneRel |
| id | BigAutoField |
| date | DateField |
| serviceman | ForeignKey |
| organization | ForeignKey |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### ShipmentDocumentEquipment

| Field | Type |
|---|---|
| id | BigAutoField |
| shipment_document | ForeignKey |
| client_equipment | ForeignKey |
| repair_document | OneToOneField |
| created_at | DateTimeField |

### StatusDirectory

| Field | Type |
|---|---|
| repair_documents | ManyToOneRel |
| id | BigAutoField |
| code | PositiveSmallIntegerField |
| name | CharField |
| description | TextField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### WorkDirectory

| Field | Type |
|---|---|
| consumable_links | ManyToOneRel |
| part_links | ManyToOneRel |
| repair_document_links | ManyToOneRel |
| id | BigAutoField |
| code | CharField |
| name | CharField |
| unit_price | DecimalField |
| created_at | DateTimeField |
| updated_at | DateTimeField |

### WorkDirectoryConsumable

| Field | Type |
|---|---|
| id | BigAutoField |
| work | ForeignKey |
| consumable | ForeignKey |
| quantity | PositiveIntegerField |
| created_at | DateTimeField |

### WorkDirectoryPart

| Field | Type |
|---|---|
| id | BigAutoField |
| work | ForeignKey |
| part | ForeignKey |
| quantity | PositiveIntegerField |
| created_at | DateTimeField |

## Views

- `acceptance_document(request)`
- `acceptance_document_add_equipment(request, document_id)`
- `acceptance_document_edit(request, document_id=None)`
- `address_directory(request)`
- `address_directory_delete(request, address_id)`
- `brand(request)`
- `brand_delete(request, brand_id)`
- `client_equipment(request)`
- `client_equipment_delete(request, equipment_id)`
- `consumable(request)`
- `consumable_delete(request, consumable_id)`
- `consumable_edit(request, consumable_id=None)`
- `consumable_product_models(request, consumable_id)`
- `contacts(request)`
- `egrul_lookup(request)`
- `equipment_characteristic_type(request)`
- `home(request)`
- `home_logo(request)`
- `organizations(request)`
- `part(request)`
- `part_delete(request, part_id)`
- `part_edit(request, part_id=None)`
- `part_product_models(request, part_id)`
- `product_category(request)`
- `product_category_delete(request, category_id)`
- `product_model(request)`
- `product_model_consumables(request, model_id)`
- `product_model_delete(request, model_id)`
- `product_model_edit(request, model_id=None)`
- `product_model_parts(request, model_id)`
- `profile(request)`
- `repair_document(request)`
- `repair_document_delete(request, document_id)`
- `repair_document_edit(request, document_id=None)`
- `repair_document_equipment_history(request, equipment_id)`
- `repair_document_view(request, document_id)`
- `report_acceptance_document(request)`
- `report_address_directory(request)`
- `report_brand(request)`
- `report_characteristics(request)`
- `report_consumable(request)`
- `report_part(request)`
- `report_product_category(request)`
- `report_repair_document(request)`
- `report_shipment_document(request)`
- `report_status_directory(request)`
- `report_work_directory(request)`
- `service_centers(request)`
- `service_exchange(request)`
- `service_exchange_log_download(request, log_id: int)`
- `serviceman(request)`
- `serviceman_delete(request, serviceman_id)`
- `shipment_document(request)`
- `shipment_document_edit(request, document_id=None)`
- `status_directory(request)`
- `status_directory_delete(request, status_id)`
- `style_select(request, theme_key)`
- `style_settings(request)`
- `theme_asset(request, theme_key, asset_path)`
- `users(request)`
- `work_directory(request)`
- `work_directory_delete(request, work_id)`
- `work_directory_edit(request, work_id=None)`

## Forms

- `AcceptanceDocumentForm`
- `AcceptanceEquipmentCreateForm`
- `AddressForm`
- `AdminUserCreateForm`
- `BrandForm`
- `CatalogAttachmentForm`
- `ClientEquipmentForm`
- `ConsumableForm`
- `EquipmentCharacteristicTypeForm`
- `GroupCreateForm`
- `OrganizationContactForm`
- `OrganizationForm`
- `PartForm`
- `ProductCategoryForm`
- `ProductModelForm`
- `RepairDocumentConsumableForm`
- `RepairDocumentForm`
- `RepairDocumentPartForm`
- `RepairDocumentWorkForm`
- `ServiceCenterContactForm`
- `ServiceCenterForm`
- `ServiceManForm`
- `ShipmentDocumentForm`
- `StatusDirectoryForm`
- `WorkDirectoryForm`

## Admin

- `CaseInsensitiveSearchAdminMixin`
- `CustomGroupAdmin`
- `CustomUserAdmin`
- `OrganizationAdmin`
- `OrganizationContactAdmin`
- `OrganizationContactInline`

## URL Patterns

| Route | Name | View |
|---|---|---|
|  | home | home |
| home/logo.jpg | home_logo | home_logo |
| style/ | style_settings | style_settings |
| style/select/<slug:theme_key>/ | style_select | style_select |
| style/assets/<slug:theme_key>/<path:asset_path> | theme_asset | theme_asset |
| profile/ | profile | profile |
| organizations/ | organizations | organizations |
| service-centers/ | service_centers | service_centers |
| contacts/ | contacts | contacts |
| serviceman/ | serviceman | serviceman |
| serviceman/<int:serviceman_id>/delete/ | serviceman_delete | serviceman_delete |
| product-category/ | product_category | product_category |
| product-category/<int:category_id>/delete/ | product_category_delete | product_category_delete |
| brand/ | brand | brand |
| brand/<int:brand_id>/delete/ | brand_delete | brand_delete |
| product-model/ | product_model | product_model |
| product-model/new/ | product_model_new | product_model_edit |
| product-model/<int:model_id>/ | product_model_edit | product_model_edit |
| product-model/<int:model_id>/consumables/ | product_model_consumables | product_model_consumables |
| product-model/<int:model_id>/parts/ | product_model_parts | product_model_parts |
| product-model/<int:model_id>/delete/ | product_model_delete | product_model_delete |
| equipment-characteristics/ | equipment_characteristic_type | equipment_characteristic_type |
| characteristics/ | characteristic_directory | equipment_characteristic_type |
| consumable/ | consumable | consumable |
| consumable/new/ | consumable_new | consumable_edit |
| consumable/<int:consumable_id>/ | consumable_edit | consumable_edit |
| consumable/<int:consumable_id>/models/ | consumable_product_models | consumable_product_models |
| consumable/<int:consumable_id>/delete/ | consumable_delete | consumable_delete |
| part/ | part | part |
| part/new/ | part_new | part_edit |
| part/<int:part_id>/ | part_edit | part_edit |
| part/<int:part_id>/models/ | part_product_models | part_product_models |
| part/<int:part_id>/delete/ | part_delete | part_delete |
| work-directory/ | work_directory | work_directory |
| work-directory/new/ | work_directory_new | work_directory_edit |
| work-directory/<int:work_id>/ | work_directory_edit | work_directory_edit |
| work-directory/<int:work_id>/delete/ | work_directory_delete | work_directory_delete |
| statuses/ | status_directory | status_directory |
| statuses/<int:status_id>/delete/ | status_directory_delete | status_directory_delete |
| addresses/ | address_directory | address_directory |
| addresses/<int:address_id>/delete/ | address_directory_delete | address_directory_delete |
| documents/repair/ | repair_document | repair_document |
| documents/repair/new/ | repair_document_new | repair_document_edit |
| documents/repair/equipment/<int:equipment_id>/history/ | repair_document_equipment_history | repair_document_equipment_history |
| documents/repair/<int:document_id>/view/ | repair_document_view | repair_document_view |
| documents/repair/<int:document_id>/ | repair_document_edit | repair_document_edit |
| documents/repair/<int:document_id>/delete/ | repair_document_delete | repair_document_delete |
| documents/acceptance/ | acceptance_document | acceptance_document |
| documents/acceptance/new/ | acceptance_document_new | acceptance_document_edit |
| documents/acceptance/<int:document_id>/ | acceptance_document_edit | acceptance_document_edit |
| documents/acceptance/<int:document_id>/add-equipment/ | acceptance_document_add_equipment | acceptance_document_add_equipment |
| documents/shipment/ | shipment_document | shipment_document |
| documents/shipment/new/ | shipment_document_new | shipment_document_edit |
| documents/shipment/<int:document_id>/ | shipment_document_edit | shipment_document_edit |
| reports/acceptance/ | report_acceptance_document | report_acceptance_document |
| reports/shipment/ | report_shipment_document | report_shipment_document |
| reports/repair/ | report_repair_document | report_repair_document |
| reports/part/ | report_part | report_part |
| reports/consumable/ | report_consumable | report_consumable |
| reports/work-directory/ | report_work_directory | report_work_directory |
| reports/address/ | report_address_directory | report_address_directory |
| reports/brand/ | report_brand | report_brand |
| reports/status/ | report_status_directory | report_status_directory |
| reports/product-category/ | report_product_category | report_product_category |
| reports/characteristics/ | report_characteristics | report_characteristics |
| service/exchange/ | service_exchange | service_exchange |
| service/exchange/log/<int:log_id>/download/ | service_exchange_log_download | service_exchange_log_download |
| client-equipment/ | client_equipment | client_equipment |
| client-equipment/<int:equipment_id>/delete/ | client_equipment_delete | client_equipment_delete |
| api/egrul-lookup/ | egrul_lookup | egrul_lookup |
| users/ | users | users |
| login/ | login | view |
| logout/ | logout | view |
| admin/ |  | None |
| ^media/(?P<path>.*)$ |  | serve |

## Templates

- `acceptance_document.html`
- `acceptance_document_add_equipment.html`
- `acceptance_document_edit.html`
- `address_directory.html`
- `base.html`
- `brand.html`
- `client_equipment.html`
- `consumable.html`
- `consumable_delete.html`
- `consumable_edit.html`
- `consumable_product_models.html`
- `contacts.html`
- `dictionary_delete.html`
- `equipment_characteristic_type.html`
- `home.html`
- `includes\pagination_controls.html`
- `includes\per_page_select.html`
- `organizations.html`
- `part.html`
- `part_delete.html`
- `part_edit.html`
- `part_product_models.html`
- `product_category.html`
- `product_model.html`
- `product_model_consumables.html`
- `product_model_edit.html`
- `product_model_parts.html`
- `profile.html`
- `registration\login.html`
- `repair_document.html`
- `repair_document_edit.html`
- `repair_document_equipment_history.html`
- `repair_document_view.html`
- `report_acceptance_document.html`
- `report_address_directory.html`
- `report_brand.html`
- `report_characteristics.html`
- `report_consumable.html`
- `report_part.html`
- `report_product_category.html`
- `report_repair_document.html`
- `report_shipment_document.html`
- `report_status_directory.html`
- `report_work_directory.html`
- `service_centers.html`
- `service_exchange.html`
- `serviceman.html`
- `shipment_document.html`
- `shipment_document_edit.html`
- `status_directory.html`
- `style_settings.html`
- `users.html`
- `work_directory.html`
- `work_directory_edit.html`
