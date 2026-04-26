import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
import django
django.setup()

from services.models import ProductModel

total = ProductModel.objects.count()
filled = ProductModel.objects.exclude(site='').count()
empty = total - filled

print(f"=== ProductModel.site статистика ===")
print(f"Всего: {total}")
print(f"Заполнено: {filled} ({100*filled/total:.1f}%)")
print(f"Пусто: {empty}")
print()

from django.db.models import Count
by_brand = ProductModel.objects.exclude(site='').values('brand__name').annotate(cnt=Count('id')).order_by('-cnt')
print("По брендам (заполненные):")
for row in by_brand:
    print(f"  {row['brand__name']:15} {row['cnt']:3} моделей")
