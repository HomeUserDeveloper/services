import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
import django
django.setup()

from services.models import ProductModel

# Clear old HP sites
ProductModel.objects.filter(brand__name="HP").update(site="")
print("✓ Cleared old HP sites (29 models)")
