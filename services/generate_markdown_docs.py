#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate project documentation in Markdown format."""

from __future__ import annotations

import inspect
import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "services.settings")

import django

django.setup()

import services.admin as admin_module
import services.forms as forms_module
import services.models as models_module
import services.urls as urls_module
import services.views as views_module

OUTPUT_MD = BASE_DIR / "docs" / "_build" / "Services_Documentation.md"
TEMPLATES_DIR = BASE_DIR / "templates"


def own_classes(module):
    mod_file = Path(module.__file__).resolve()
    result = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if name.startswith("_"):
            continue
        try:
            cls_file = Path(inspect.getfile(obj)).resolve()
        except TypeError:
            continue
        if cls_file != mod_file:
            continue
        result.append((name, obj))
    return result


def own_functions(module):
    mod_file = Path(module.__file__).resolve()
    result = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("_"):
            continue
        try:
            fn = inspect.unwrap(obj)
            fn_file = Path(inspect.getfile(fn)).resolve()
        except (TypeError, ValueError):
            continue
        if fn_file != mod_file:
            continue
        result.append((name, fn))
    return result


def model_fields(model_cls):
    rows = []
    for f in model_cls._meta.get_fields():
        rows.append((f.name, type(f).__name__))
    return rows


def url_patterns():
    rows = []
    for p in getattr(urls_module, "urlpatterns", []):
        try:
            route = str(p.pattern)
            name = getattr(p, "name", "") or ""
            view_name = getattr(p.callback, "__name__", str(p.callback))
            rows.append((route, name, view_name))
        except Exception:
            continue
    return rows


def templates_list():
    if not TEMPLATES_DIR.exists():
        return []
    return [str(p.relative_to(TEMPLATES_DIR)) for p in sorted(TEMPLATES_DIR.rglob("*.html"))]


def write_md():
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    models = own_classes(models_module)
    forms = own_classes(forms_module)
    views = own_functions(views_module)
    admins = own_classes(admin_module)
    urls = url_patterns()
    templates = templates_list()

    lines: list[str] = []
    lines.append("# Services Project Documentation")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Models: {len(models)}")
    lines.append(f"- Views: {len(views)}")
    lines.append(f"- Forms: {len(forms)}")
    lines.append(f"- Admin classes: {len(admins)}")
    lines.append(f"- URL patterns: {len(urls)}")
    lines.append(f"- Templates: {len(templates)}")
    lines.append("")

    lines.append("## Models")
    lines.append("")
    for name, cls in models:
        lines.append(f"### {name}")
        lines.append("")
        lines.append("| Field | Type |")
        lines.append("|---|---|")
        for field_name, field_type in model_fields(cls):
            lines.append(f"| {field_name} | {field_type} |")
        lines.append("")

    lines.append("## Views")
    lines.append("")
    for name, fn in views:
        try:
            sig = str(inspect.signature(fn))
        except (TypeError, ValueError):
            sig = "(...)"
        lines.append(f"- `{name}{sig}`")
    lines.append("")

    lines.append("## Forms")
    lines.append("")
    for name, _ in forms:
        lines.append(f"- `{name}`")
    lines.append("")

    lines.append("## Admin")
    lines.append("")
    for name, _ in admins:
        lines.append(f"- `{name}`")
    lines.append("")

    lines.append("## URL Patterns")
    lines.append("")
    lines.append("| Route | Name | View |")
    lines.append("|---|---|---|")
    for route, name, view_name in urls:
        lines.append(f"| {route} | {name} | {view_name} |")
    lines.append("")

    lines.append("## Templates")
    lines.append("")
    for item in templates:
        lines.append(f"- `{item}`")
    lines.append("")

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown documentation generated: {OUTPUT_MD}")


if __name__ == "__main__":
    write_md()
