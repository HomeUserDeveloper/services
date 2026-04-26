import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
import django
django.setup()

from services.models import ProductModel

# Clear old HP sites
ProductModel.objects.filter(brand__name="HP").update(site="")
print("Cleared HP sites")

# Show examples of what will be generated
hp_models = ProductModel.objects.filter(brand__name="HP")[:3]
for pm in hp_models:
    name = pm.name.strip()
    if name.upper().startswith("HP "):
        name = name[3:]
    slug = name.lower().replace(" ", "-").replace(".", "-")
    url = f"https://support.hp.com/us-en/drivers/hp-{slug}-printer-series"
    print(f"{pm.name} -> {url}")

print("\nRunning populate command...")
