import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
import django
django.setup()

from services.models import ProductModel, Brand

# Check if Техноэволаб brand has site
brand = Brand.objects.get(name="Техноэволаб")
print(f"Техноэволаб site: {brand.site if brand.site else 'нет'}")

# Manual fill for Техноэволаб if we have the URL
# For now, leave it empty since it's unclear what the official support page is
