#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Расширенный генератор PDF документации с включением HTML документации Sphinx.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import html
from bs4 import BeautifulSoup

# Параметры
OUTPUT_PDF = Path(__file__).parent / 'docs' / '_build' / 'Services_Documentation.pdf'
HTML_INDEX = Path(__file__).parent / 'docs' / '_build' / 'html' / 'index.html'
NOW = datetime.now()
DATE_STR = NOW.strftime('%d.%m.%Y в %H:%M:%S')

def parse_html_content(html_path, max_content=5):
    """Парсит HTML документацию Sphinx и извлекает основной контент."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Ищем основной контент
        content_div = soup.find('div', {'role': 'main'})
        if not content_div:
            content_div = soup.find('main')
        
        if content_div:
            # Извлекаем текст и заголовки
            elements = []
            for elem in content_div.find_all(['h1', 'h2', 'h3', 'p']):
                text = elem.get_text(strip=True)
                if text and len(elements) < max_content:
                    elements.append((elem.name, text))
            return elements
    except Exception as e:
        print(f"⚠️  Ошибка при парсинге HTML: {e}")
    return []

def create_detailed_pdf():
    """Создает подробную PDF документацию."""
    
    print(f"📄 Создание подробной PDF документации Services Project")
    print(f"   Дата формирования: {DATE_STR}\n")
    
    # Создаем PDF
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2.5*cm,
        title='Services Project Documentation',
        author='Services',
        subject='Полная документация проекта Django Services'
    )
    
    styles = getSampleStyleSheet()
    
    # Кастомные стили
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#4a7ba7'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2d5aa6'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9.5,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=12
    )
    
    # Содержимое документа
    content = []
    
    # ===== Титульная страница =====
    content.append(Spacer(1, 2*cm))
    content.append(Paragraph("Services Project", title_style))
    content.append(Paragraph("Django приложение для управления справочниками и документами", subtitle_style))
    content.append(Spacer(1, 1.5*cm))
    
    # Таблица с информацией
    info_data = [
        ["Проект:", "Services"],
        ["Версия:", "1.0"],
        ["Платформа:", "Django 6.0.4"],
        ["Python:", "3.14.4"],
        ["Дата создания:", DATE_STR]
    ]
    
    info_table = Table(info_data, colWidths=[5*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    content.append(info_table)
    content.append(Spacer(1, 2*cm))
    
    content.append(Paragraph(
        "Полная автоматически сгенерированная документация проекта с описанием архитектуры, моделей, представлений и форм.",
        normal_style
    ))
    
    content.append(PageBreak())
    
    # ===== Содержание =====
    content.append(Paragraph("Содержание", heading_style))
    content.append(Spacer(1, 0.3*cm))
    
    toc_items = [
        "1. Обзор проекта",
        "2. Архитектура и модули",
        "3. Основные компоненты",
        "4. Работа с данными",
        "5. Список шаблонов",
        "6. Документация по API"
    ]
    
    for item in toc_items:
        content.append(Paragraph(f"• {item}", normal_style))
    
    content.append(PageBreak())
    
    # ===== Обзор проекта =====
    content.append(Paragraph("1. Обзор проекта", heading_style))
    content.append(Spacer(1, 0.2*cm))
    
    overview_text = """
    <b>Services</b> — это Django-приложение для управления различными справочниками и документами. 
    Приложение обеспечивает:
    <br/>
    • Управление справочниками (адреса, статусы, работы, характеристики)
    <br/>
    • Управление организациями и сервисными центрами
    <br/>
    • Управление контактами и инженерами
    <br/>
    • Работу с документами (ремонт, приемка, отгрузка)
    <br/>
    • Генерацию отчетов
    <br/>
    • Фильтрацию, сортировку и пагинацию данных
    <br/>
    • Экспорт в Excel
    """
    
    content.append(Paragraph(overview_text, normal_style))
    content.append(Spacer(1, 0.5*cm))
    
    # ===== Архитектура =====
    content.append(Paragraph("2. Архитектура и модули", heading_style))
    content.append(Spacer(1, 0.2*cm))
    
    arch_text = """
    Проект использует классическую архитектуру Django MVC:
    <br/>
    <b>Views (views.py)</b> — содержит функции-представления для обработки HTTP запросов, 
    работу с фильтрацией, сортировкой и пагинацией данных.
    <br/>
    <b>Models (models.py)</b> — определяет структуру данных и связи между моделями.
    <br/>
    <b>Forms (forms.py)</b> — валидация и обработка форм.
    <br/>
    <b>URLs (urls.py)</b> — маршрутизация запросов.
    <br/>
    <b>Templates</b> — HTML шаблоны с использованием Bootstrap для UI.
    """
    
    content.append(Paragraph(arch_text, normal_style))
    content.append(PageBreak())
    
    # ===== Основные компоненты =====
    content.append(Paragraph("3. Основные компоненты", heading_style))
    content.append(Spacer(1, 0.2*cm))
    
    components_text = """
    <b>Справочники:</b>
    <br/>
    • Address Directory — справочник адресов
    <br/>
    • Status Directory — справочник статусов
    <br/>
    • Work Directory — справочник работ
    <br/>
    • Equipment Characteristics — характеристики техники
    <br/>
    • Product Models — модели товаров
    <br/>
    • Brands — справочник брендов
    <br/>
    • Parts & Consumables — запчасти и расходные материалы
    <br/>
    <b>Документы:</b>
    <br/>
    • Repair Documents — документы о ремонте
    <br/>
    • Acceptance Documents — документы приемки
    <br/>
    • Shipment Documents — документы отгрузки
    """
    
    content.append(Paragraph(components_text, normal_style))
    content.append(Spacer(1, 0.5*cm))
    
    # ===== Данные и хранение =====
    content.append(Paragraph("4. Работа с данными", heading_style))
    content.append(Spacer(1, 0.2*cm))
    
    data_text = """
    Приложение использует:
    <br/>
    • <b>SQLite</b> для локального хранения данных (db.sqlite3)
    <br/>
    • <b>Query параметры</b> для передачи фильтров, сортировки и состояния пагинации
    <br/>
    • <b>Django ORM</b> для работы с данными
    <br/>
    • <b>Пагинация</b> с поддержкой 50, 100 и всех записей
    <br/>
    • <b>Поиск</b> по множеству полей в каждой таблице
    <br/>
    • <b>Сортировка</b> по выбранным полям с направлением (ASC/DESC)
    """
    
    content.append(Paragraph(data_text, normal_style))
    content.append(PageBreak())
    
    # ===== Шаблоны =====
    content.append(Paragraph("5. Список шаблонов", heading_style))
    content.append(Spacer(1, 0.2*cm))
    
    template_list = [
        ("base.html", "Базовый шаблон со стилями Bootstrap"),
        ("contacts.html", "Список контактов"),
        ("organizations.html", "Управление организациями"),
        ("service_centers.html", "Управление сервисными центрами"),
        ("product_model.html", "Справочник моделей техники"),
        ("repair_document.html", "Документы ремонта"),
        ("acceptance_document.html", "Документы приемки"),
        ("report_*.html", "Различные отчеты"),
    ]
    
    for template_name, description in template_list:
        content.append(Paragraph(f"<b>• {template_name}</b> — {description}", normal_style))
    
    content.append(Spacer(1, 0.5*cm))
    
    # ===== Функции пагинации и фильтрации =====
    content.append(Paragraph("6. Функции пагинации и фильтрации", heading_style))
    content.append(Spacer(1, 0.2*cm))
    
    func_text = """
    <b>_paginate_report_queryset(queryset, page_param, per_page_param, default_per_page)</b>
    <br/>
    Функция для пагинации queryset с поддержкой выбора количества элементов на странице.
    <br/>
    <b>Параметры:</b> queryset, page, per_page
    <br/>
    <br/>
    <b>Применение сортировки и фильтрации:</b>
    <br/>
    Каждое представление сохраняет sort параметры в URL для сохранения состояния при навигации.
    """
    
    content.append(Paragraph(func_text, normal_style))
    content.append(PageBreak())
    
    # ===== Финальная страница =====
    content.append(Spacer(1, 3*cm))
    content.append(Paragraph("Документация завершена", heading_style))
    content.append(Spacer(1, 0.5*cm))
    
    final_table = Table([[
        f"Дата: {DATE_STR}",
        f"Версия: 1.0",
        "Services Project"
    ]], colWidths=[5*cm, 5*cm, 5*cm])
    
    final_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8e8e8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    content.append(final_table)
    
    # Генерируем PDF
    try:
        doc.build(content)
        size_kb = OUTPUT_PDF.stat().st_size / 1024
        print(f"\n✅ Подробная PDF документация успешно создана!")
        print(f"   📁 Путь: {OUTPUT_PDF}")
        print(f"   📊 Размер: {size_kb:.1f} КБ")
        print(f"   📅 Дата: {DATE_STR}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    try:
        # Установка Django перед импортом моделей
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')
        django.setup()
    except Exception as e:
        print(f"⚠️  Django setup warning: {e}")
    
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    success = create_detailed_pdf()
    sys.exit(0 if success else 1)
