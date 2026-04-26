# Services

Services — Django-проект для ведения сервисных справочников, клиентов, техники, документов и отчетов в рамках локальной системы сервисного обслуживания.

## English Summary

Services is a Django-based local service management project for maintaining reference data, client equipment, service documents, and reports.

The repository intentionally does not contain real data for Organizations, Service Centers, Contacts, and Client Equipment. Each tester is expected to fill these directories with their own data. The Service Engineers directory contains one fictional test record. For local and public deployments, create your own administrator account with Django management commands.

## Quick Start for GitHub

```powershell
git clone <repository-url>
cd proj
python -m venv .venv
.venv/Scripts/Activate.ps1
pip install -r requirements.txt
cd services
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8080
```

## Что умеет проект

- вести справочники и связанные сущности сервисного учета
- работать с организациями, контактами, сервисными центрами и техникой клиентов
- оформлять сервисные документы
- формировать отчеты по основным разделам системы
- использовать фильтрацию, сортировку и пагинацию в списках и отчетах
- экспортировать данные в табличные форматы для дальнейшей обработки

## Основные разделы

- Организации
- Сервисные центры
- Контакты
- Техника клиентов
- Сервисные инженеры
- Документы
- Отчеты
- Справочники

## Важное замечание по тестовым данным

По принципиальным соображениям следующие справочники в репозитории не заполнены:

- Организации
- Сервисные центры
- Контакты
- Техника клиентов

Предполагается, что каждый тестирующий заполняет эти разделы своими собственными данными.

Справочник Сервисные инженеры содержит одну тестовую вымышленную запись.

## Учетная запись администратора

В публичной версии репозитория действующие логины и пароли не публикуются.

После первого запуска создайте собственного суперпользователя:

```powershell
cd services
python manage.py createsuperuser
```

## Быстрый локальный запуск

Если зависимости уже установлены и виртуальное окружение готово:

```powershell
cd services
../.venv/Scripts/Activate.ps1
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8080
```

После запуска приложение будет доступно по адресу http://127.0.0.1:8080.

## Установка зависимостей

В корне проекта подготовлен файл requirements.txt с основными зависимостями.

Если виртуальное окружение уже существует, достаточно активировать его и установить зависимости из requirements.txt.

Пример для Windows PowerShell:

```powershell
cd services
../.venv/Scripts/Activate.ps1
python -m pip install -r ../requirements.txt
```

Если окружение нужно развернуть с нуля:

```powershell
python -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Для запуска веб-приложения критически нужен Django. Остальные пакеты используются для экспорта XLSX, генерации PDF и документации.

## Production configuration

Для публичного запуска рекомендуется задавать настройки через переменные окружения:

В корне проекта добавлен шаблон [.env.example](.env.example) с примером безопасной конфигурации.

```powershell
$env:DJANGO_SECRET_KEY = "replace-with-long-random-secret"
$env:DJANGO_DEBUG = "false"
$env:DJANGO_ALLOWED_HOSTS = "example.com,www.example.com"
```

При `DJANGO_DEBUG=false` проект автоматически включает базовые secure-настройки Django для cookies, HTTPS redirect и HSTS.

## Структура проекта

```text
services/
├── manage.py
├── db.sqlite3
├── services/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   └── admin.py
├── templates/
│   ├── base.html
│   ├── organizations.html
│   ├── contacts.html
│   ├── profile.html
│   └── report_*.html
└── docs/
	└── _build/
```

## Пересоздание суперпользователя в Django

Команды recreate в Django нет. Если нужно пересоздать суперпользователя с тем же именем, это делается в два шага.

### 1. Удалить старого пользователя

```bash
cd services
python manage.py shell
```

В интерактивной оболочке выполнить:

```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(username='<username>').delete()
exit()
```

### 2. Создать нового суперпользователя

```bash
cd services
python manage.py createsuperuser
```

Во время выполнения Django запросит:

- Username
- Email address
- Password

## Если нужно только сменить пароль

```bash
cd services
python manage.py changepassword <username>
```

## Безынтерактивное создание суперпользователя

Подходит для автоматизации, контейнеров и деплоя:

```bash
DJANGO_SUPERUSER_PASSWORD=mypassword \
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@example.com \
python manage.py createsuperuser --noinput
```

## Примечания по репозиторию

- файлы SQLite базы данных не предназначены для публикации в GitHub
- содержимое архивных папок не должно попадать в репозиторий
- соответствующие исключения настроены через .gitignore
