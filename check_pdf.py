from pathlib import Path
import datetime

pdf_path = Path('d:/proj/services/docs/_build/Services_Documentation.pdf')
if pdf_path.exists():
    size_kb = pdf_path.stat().st_size / 1024
    mtime = datetime.datetime.fromtimestamp(pdf_path.stat().st_mtime)
    print(f"✅ PDF Документация создана успешно!")
    print(f"   📁 Файл: {pdf_path.name}")
    print(f"   📊 Размер: {size_kb:.1f} КБ")
    print(f"   📅 Дата создания: {mtime.strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"   🔗 Полный путь: {pdf_path}")
else:
    print(f"❌ PDF файл не найден")
