import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
import django
django.setup()

from services.models import ProductModel

# Get all HP models
hp_models = ProductModel.objects.filter(brand__name="HP").order_by('id')
print("HP моделей для маппинга кодов:")
for i, pm in enumerate(hp_models, 1):
    print(f"{i:2}. {pm.name}")
