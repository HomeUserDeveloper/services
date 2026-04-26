import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
import django
django.setup()

from services.models import ProductModel

print("=== Примеры новых HP ссылок ===")
hp_models = ProductModel.objects.filter(brand__name="HP")[:5]
for pm in hp_models:
    print(f"\n{pm.name}")
    print(f"  → {pm.site}")
