#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Генератор PDF документации проекта Services с использованием reportlab.
Поддержка кириллицы через TTF-шрифты Windows.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import inspect

# --- Django setup (до импорта приложения) ---
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
import django
django.setup()

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Регистрация TTF-шрифтов с кириллицей ---
FONTS_DIR = Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('Arial',         str(FONTS_DIR / 'arial.ttf')))
pdfmetrics.registerFont(TTFont('Arial-Bold',    str(FONTS_DIR / 'arialbd.ttf')))
pdfmetrics.registerFont(TTFont('Arial-Italic',  str(FONTS_DIR / 'ariali.ttf')))
pdfmetrics.registerFont(TTFont('CourierNew',    str(FONTS_DIR / 'cour.ttf')))
pdfmetrics.registerFont(TTFont('CourierNew-Bold', str(FONTS_DIR / 'courbd.ttf')))

# --- Параметры ---
OUTPUT_PDF  = Path(__file__).parent / 'docs' / '_build' / 'Services_Documentation.pdf'
TEMPLATES_DIR = Path(__file__).parent / 'templates'
NOW      = datetime.now()
DATE_STR = NOW.strftime('%d.%m.%Y в %H:%M:%S')

# --- Стили (все fontName используют зарегистрированные TTF с кириллицей) ---
def build_styles():
    S = {}
    S['title'] = ParagraphStyle(
        'DocTitle', fontSize=26, fontName='Arial-Bold',
        textColor=colors.HexColor('#1f4788'), alignment=TA_CENTER,
        spaceAfter=12, spaceBefore=0, leading=32
    )
    S['subtitle'] = ParagraphStyle(
        'DocSubtitle', fontSize=12, fontName='Arial',
        textColor=colors.HexColor('#4a7ba7'), alignment=TA_CENTER,
        spaceAfter=6
    )
    S['h1'] = ParagraphStyle(
        'H1', fontSize=16, fontName='Arial-Bold',
        textColor=colors.HexColor('#1f4788'), spaceBefore=16, spaceAfter=8,
        leading=20, borderPad=0
    )
    S['h2'] = ParagraphStyle(
        'H2', fontSize=13, fontName='Arial-Bold',
        textColor=colors.HexColor('#2d5aa6'), spaceBefore=12, spaceAfter=6,
        leading=16
    )
    S['h3'] = ParagraphStyle(
        'H3', fontSize=11, fontName='Arial-Bold',
        textColor=colors.HexColor('#4a7ba7'), spaceBefore=8, spaceAfter=4,
        leading=14
    )
    S['normal'] = ParagraphStyle(
        'Normal2', fontSize=9.5, fontName='Arial',
        alignment=TA_JUSTIFY, spaceAfter=4, leading=13
    )
    S['item'] = ParagraphStyle(
        'Item', fontSize=9, fontName='Arial',
        spaceAfter=2, leftIndent=12, leading=12
    )
    S['code'] = ParagraphStyle(
        'Code2', fontSize=8.5, fontName='CourierNew',
        textColor=colors.HexColor('#222222'), leftIndent=12,
        spaceAfter=2, leading=11, backColor=colors.HexColor('#f5f5f5')
    )
    S['meta'] = ParagraphStyle(
        'Meta', fontSize=8, fontName='Arial-Italic',
        textColor=colors.HexColor('#666666'), spaceAfter=2
    )
    S['toc'] = ParagraphStyle(
        'TOC', fontSize=10, fontName='Arial', spaceAfter=4, leftIndent=0
    )
    S['toc_sub'] = ParagraphStyle(
        'TOCSub', fontSize=9, fontName='Arial', spaceAfter=2, leftIndent=18,
        textColor=colors.HexColor('#555555')
    )
    return S


def hr(content):
    content.append(HRFlowable(width='100%', thickness=0.5,
                               color=colors.HexColor('#cccccc'), spaceAfter=6, spaceBefore=2))


def section_heading(content, text, S, level='h1'):
    content.append(Spacer(1, 0.2*cm))
    content.append(Paragraph(text, S[level]))
    hr(content)


def table_style_default():
    return TableStyle([
        ('FONTNAME',  (0, 0), (-1, 0),  'Arial-Bold'),
        ('FONTNAME',  (0, 1), (-1, -1), 'Arial'),
        ('FONTSIZE',  (0, 0), (-1, -1), 8.5),
        ('BACKGROUND',(0, 0), (-1,  0), colors.HexColor('#dde3ef')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.HexColor('#f4f6fb')]),
        ('GRID',      (0, 0), (-1, -1), 0.4, colors.HexColor('#aaaaaa')),
        ('LEFTPADDING',  (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING',   (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
        ('VALIGN',    (0, 0), (-1, -1), 'TOP'),
    ])


# --- Извлечение данных из Django-модулей ---
import services.views  as _views_mod
import services.models as _models_mod
import services.forms  as _forms_mod
import services.urls   as _urls_mod
import services.admin  as _admin_mod


def get_functions(module):
    """Все публичные функции модуля, определённые в нём (не импортированные).
    Раскрывает декораторы через inspect.unwrap для корректного определения файла.
    """
    mod_file = getattr(module, '__file__', None)
    result = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.startswith('_'):
            continue
        # Раскрываем декораторы (@login_required и др.)
        try:
            unwrapped = inspect.unwrap(obj)
        except Exception:
            unwrapped = obj
        try:
            fn_file = inspect.getfile(unwrapped)
        except TypeError:
            continue
        if mod_file and os.path.normcase(str(Path(fn_file).resolve())) != \
                        os.path.normcase(str(Path(mod_file).resolve())):
            continue
        doc = inspect.getdoc(unwrapped) or ''
        try:
            sig = str(inspect.signature(unwrapped))
        except (ValueError, TypeError):
            sig = '(...)'
        result.append({'name': name, 'sig': sig, 'doc': doc})
    return result


def get_classes(module, include_methods=True):
    """Все публичные классы модуля."""
    mod_file = getattr(module, '__file__', None)
    result = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if name.startswith('_'):
            continue
        try:
            cls_file = inspect.getfile(obj)
        except TypeError:
            continue
        if mod_file and Path(cls_file).resolve() != Path(mod_file).resolve():
            continue
        bases = [b.__name__ for b in obj.__bases__ if b.__name__ != 'object']
        doc = inspect.getdoc(obj) or ''
        methods = []
        if include_methods:
            for mname, mobj in inspect.getmembers(obj):
                if mname.startswith('_'):
                    continue
                if not (inspect.isfunction(mobj) or inspect.ismethod(mobj)):
                    continue
                try:
                    sig = str(inspect.signature(mobj))
                except (ValueError, TypeError):
                    sig = '(...)'
                mdoc = inspect.getdoc(mobj) or ''
                methods.append({'name': mname, 'sig': sig, 'doc': mdoc})
        result.append({'name': name, 'bases': bases, 'doc': doc, 'methods': methods})
    return result


def get_model_fields(model_class):
    """Возвращает список полей модели Django."""
    fields = []
    try:
        for f in model_class._meta.get_fields():
            fname = f.name
            ftype = type(f).__name__
            fields.append({'name': fname, 'type': ftype})
    except Exception:
        pass
    return fields


def get_url_patterns(url_module):
    """Возвращает список URL-маршрутов."""
    patterns = []
    for p in getattr(url_module, 'urlpatterns', []):
        try:
            route   = str(p.pattern)
            name    = getattr(p, 'name', '') or ''
            cb      = p.callback
            view_fn = getattr(cb, '__name__', str(cb))
            patterns.append({'route': route, 'name': name, 'view': view_fn})
        except Exception:
            pass
    return patterns


def get_templates():
    """Список HTML-шаблонов."""
    result = []
    if TEMPLATES_DIR.exists():
        for tmpl in sorted(TEMPLATES_DIR.rglob('*.html')):
            rel = tmpl.relative_to(TEMPLATES_DIR)
            result.append(str(rel))
    return result


# --- Построение PDF ---
def create_pdf():
    print(f"Создание PDF документации Services Project")
    print(f"   Дата формирования: {DATE_STR}\n")

    S = build_styles()
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm,   bottomMargin=2.5*cm,
        title='Services Project Documentation',
        author='Services',
        subject='Полная документация проекта Django Services'
    )

    content = []

    # ======================================================
    # ТИТУЛЬНАЯ СТРАНИЦА
    # ======================================================
    content.append(Spacer(1, 2.5*cm))
    content.append(Paragraph('Services Project', S['title']))
    content.append(Paragraph('Документация исходного кода', S['subtitle']))
    content.append(Spacer(1, 1.5*cm))

    meta_data = [
        ['Платформа', 'Django 6.0.4 / Python 3.14'],
        ['База данных', 'SQLite'],
        ['Дата формирования', DATE_STR],
        ['Версия документа', '1.0'],
    ]
    t = Table(meta_data, colWidths=[5*cm, 11*cm])
    t.setStyle(TableStyle([
        ('FONTNAME',     (0, 0), (-1, -1), 'Arial'),
        ('FONTNAME',     (0, 0), (0, -1),  'Arial-Bold'),
        ('FONTSIZE',     (0, 0), (-1, -1), 9.5),
        ('BACKGROUND',   (0, 0), (0, -1),  colors.HexColor('#dde3ef')),
        ('BACKGROUND',   (1, 0), (1, -1),  colors.white),
        ('GRID',         (0, 0), (-1, -1), 0.5, colors.HexColor('#aaaaaa')),
        ('TOPPADDING',   (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
        ('LEFTPADDING',  (0, 0), (-1, -1), 8),
    ]))
    content.append(t)
    content.append(PageBreak())

    # ======================================================
    # ОГЛАВЛЕНИЕ (строится после сбора всех разделов)
    # ======================================================
    toc_items = [
        ('1. Модуль models.py — Модели данных',    None),
        ('2. Модуль views.py — Представления',      None),
        ('3. Модуль forms.py — Формы',              None),
        ('4. Модуль admin.py — Администрирование',  None),
        ('5. Модуль urls.py — URL-маршруты',        None),
        ('6. Шаблоны (Templates)',                  None),
    ]
    content.append(Paragraph('Содержание', S['h1']))
    content.append(Spacer(1, 0.3*cm))
    for i, (title, _) in enumerate(toc_items, 1):
        content.append(Paragraph(title, S['toc']))
    content.append(PageBreak())

    # ======================================================
    # 1. МОДЕЛИ
    # ======================================================
    section_heading(content, '1. Модели данных (models.py)', S, 'h1')
    content.append(Paragraph(
        'Модуль определяет структуру базы данных проекта. '
        'Каждый класс соответствует таблице SQLite.',
        S['normal']
    ))
    content.append(Spacer(1, 0.3*cm))

    models = get_classes(_models_mod, include_methods=False)
    print(f"   Моделей: {len(models)}")

    for cls in models:
        content.append(Paragraph(cls['name'], S['h3']))
        bases_str = ', '.join(cls['bases']) if cls['bases'] else '—'
        content.append(Paragraph(f'Родитель: {bases_str}', S['meta']))
        if cls['doc']:
            content.append(Paragraph(cls['doc'], S['normal']))
        # Поля модели
        fields = get_model_fields(getattr(_models_mod, cls['name']))
        if fields:
            rows = [['Поле', 'Тип']]
            for f in fields:
                rows.append([f['name'], f['type']])
            ft = Table(rows, colWidths=[7*cm, 9*cm])
            ft.setStyle(table_style_default())
            content.append(ft)
        content.append(Spacer(1, 0.4*cm))

    content.append(PageBreak())

    # ======================================================
    # 2. ПРЕДСТАВЛЕНИЯ (views)
    # ======================================================
    section_heading(content, '2. Представления (views.py)', S, 'h1')
    content.append(Paragraph(
        'Функции-обработчики HTTP-запросов. Реализуют логику отображения, '
        'фильтрации, сортировки, пагинации и экспорта данных.',
        S['normal']
    ))
    content.append(Spacer(1, 0.3*cm))

    funcs = get_functions(_views_mod)
    print(f"   Функций views: {len(funcs)}")

    # Сводная таблица
    rows = [['Функция', 'Сигнатура']]
    for f in funcs:
        sig_short = f['sig'][:80] + ('…' if len(f['sig']) > 80 else '')
        rows.append([f['name'], sig_short])
    t = Table(rows, colWidths=[7*cm, 9*cm])
    t.setStyle(table_style_default())
    content.append(t)
    content.append(Spacer(1, 0.5*cm))

    # Детальное описание
    for f in funcs:
        content.append(Paragraph(f['name'] + f['sig'], S['code']))
        if f['doc']:
            first_line = f['doc'].split('\n')[0]
            content.append(Paragraph(first_line, S['item']))
        content.append(Spacer(1, 0.1*cm))

    content.append(PageBreak())

    # ======================================================
    # 3. ФОРМЫ
    # ======================================================
    section_heading(content, '3. Формы (forms.py)', S, 'h1')
    content.append(Paragraph(
        'Классы форм для валидации и обработки пользовательских данных.',
        S['normal']
    ))
    content.append(Spacer(1, 0.3*cm))

    form_classes = get_classes(_forms_mod, include_methods=False)
    print(f"   Форм: {len(form_classes)}")

    rows = [['Класс формы', 'Базовый класс']]
    for cls in form_classes:
        rows.append([cls['name'], ', '.join(cls['bases']) or '—'])
    t = Table(rows, colWidths=[9*cm, 7*cm])
    t.setStyle(table_style_default())
    content.append(t)

    content.append(Spacer(1, 0.5*cm))
    for cls in form_classes:
        if cls['doc']:
            content.append(Paragraph(f"<b>{cls['name']}</b> — {cls['doc'][:200]}", S['item']))

    content.append(PageBreak())

    # ======================================================
    # 4. ADMIN
    # ======================================================
    section_heading(content, '4. Администрирование (admin.py)', S, 'h1')
    content.append(Paragraph(
        'Регистрация моделей в Django Admin и настройки отображения.',
        S['normal']
    ))
    content.append(Spacer(1, 0.3*cm))

    admin_classes = get_classes(_admin_mod, include_methods=False)
    print(f"   Admin-классов: {len(admin_classes)}")

    if admin_classes:
        rows = [['Класс Admin', 'Базовый']]
        for cls in admin_classes:
            rows.append([cls['name'], ', '.join(cls['bases']) or '—'])
        t = Table(rows, colWidths=[9*cm, 7*cm])
        t.setStyle(table_style_default())
        content.append(t)
    else:
        content.append(Paragraph('Классы администрирования не определены в модуле.', S['normal']))

    content.append(PageBreak())

    # ======================================================
    # 5. URL-МАРШРУТЫ
    # ======================================================
    section_heading(content, '5. URL-маршруты (urls.py)', S, 'h1')
    content.append(Paragraph(
        'Все зарегистрированные маршруты приложения. '
        'Каждый маршрут связывает URL-шаблон с функцией-обработчиком.',
        S['normal']
    ))
    content.append(Spacer(1, 0.3*cm))

    patterns = get_url_patterns(_urls_mod)
    print(f"   URL-паттернов: {len(patterns)}")

    rows = [['Маршрут (URL)', 'Имя', 'Функция']]
    for p in patterns:
        rows.append([p['route'], p['name'], p['view']])
    t = Table(rows, colWidths=[7.5*cm, 3.5*cm, 5*cm])
    t.setStyle(table_style_default())
    content.append(t)
    content.append(PageBreak())

    # ======================================================
    # 6. ШАБЛОНЫ
    # ======================================================
    section_heading(content, '6. Шаблоны (templates/)', S, 'h1')
    content.append(Paragraph(
        'HTML-шаблоны приложения на основе Bootstrap. '
        'Используют наследование от base.html и reusable-компоненты (includes/).',
        S['normal']
    ))
    content.append(Spacer(1, 0.3*cm))

    templates = get_templates()
    print(f"   Шаблонов: {len(templates)}")

    rows = [['Путь шаблона']]
    for tmpl in templates:
        rows.append([tmpl])
    t = Table(rows, colWidths=[16*cm])
    t.setStyle(table_style_default())
    content.append(t)
    content.append(PageBreak())

    # ======================================================
    # ФИНАЛЬНАЯ СТРАНИЦА
    # ======================================================
    content.append(Spacer(1, 3*cm))
    final = Table([[
        f'Дата формирования: {DATE_STR}',
        'Services Project v1.0'
    ]], colWidths=[10*cm, 6*cm])
    final.setStyle(TableStyle([
        ('FONTNAME',     (0, 0), (-1, -1), 'Arial-Bold'),
        ('FONTSIZE',     (0, 0), (-1, -1), 9),
        ('BACKGROUND',   (0, 0), (-1, -1), colors.HexColor('#dde3ef')),
        ('ALIGN',        (0, 0), (-1, -1), 'CENTER'),
        ('GRID',         (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING',   (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 10),
    ]))
    content.append(final)

    # ======================================================
    # BUILD
    # ======================================================
    try:
        doc.build(content)
        size_kb = OUTPUT_PDF.stat().st_size / 1024
        print(f"\nPDF документация успешно создана!")
        print(f"   Путь:   {OUTPUT_PDF}")
        print(f"   Размер: {size_kb:.1f} КБ")
        print(f"   Дата:   {DATE_STR}")
        return True
    except Exception as e:
        print(f"Ошибка при создании PDF: {e}")
        import traceback; traceback.print_exc()
        return False


if __name__ == '__main__':
    success = create_pdf()
    sys.exit(0 if success else 1)
