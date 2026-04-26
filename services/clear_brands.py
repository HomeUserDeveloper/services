import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
import django
django.setup()

from services.models import ProductModel

# Clear old XEROX, CANON, KYOCERA, BROTHER, PANTUM sites
for brand in ["XEROX", "CANON", "KYOCERA", "BROTHER", "PANTUM"]:
    ProductModel.objects.filter(brand__name=brand).update(site="")
    count = ProductModel.objects.filter(brand__name=brand).count()
    print(f"Cleared {brand}: {count} models")
