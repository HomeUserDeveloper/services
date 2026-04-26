import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')

import django
django.setup()

from services.models import ProductModel

canon = ProductModel.objects.filter(brand__name="CANON").values_list("name", flat=True)
print("CANON models:")
for m in canon:
    print(f"  {m}")

print("\nKYOCERA models:")
kyocera = ProductModel.objects.filter(brand__name="KYOCERA").values_list("name", flat=True)
for m in kyocera:
    print(f"  {m}")

print("\nBROTHER models:")
brother = ProductModel.objects.filter(brand__name="BROTHER").values_list("name", flat=True)
for m in brother:
    print(f"  {m}")

print("\nPANTUM models:")
pantum = ProductModel.objects.filter(brand__name="PANTUM").values_list("name", flat=True)
for m in pantum:
    print(f"  {m}")
