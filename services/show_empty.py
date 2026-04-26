import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
import django
django.setup()

from services.models import ProductModel

print("=== Модели без ссылки на драйверы ===")
empty_models = ProductModel.objects.filter(site='')
for pm in empty_models:
    print(f"  {pm.brand.name if pm.brand else 'N/A':15} {pm.name}")
