import re
import json
import shutil
import zipfile
from pathlib import Path

from django.conf import settings
from django.urls import reverse

THEME_SESSION_KEY = "active_theme_key"
THEMES_ROOT = settings.BASE_DIR / "themes"
BUILTIN_ROOT = THEMES_ROOT / "_builtin"
UPLOADED_ROOT = THEMES_ROOT / "uploaded"
THEME_CONFIG_PATH = THEMES_ROOT / "theme_settings.json"

BUILTIN_THEMES = {
    "builtin-light": {"name": "Светлая", "relative_path": Path("light.css")},
    "builtin-dark": {"name": "Темная", "relative_path": Path("dark.css")},
    "builtin-high-contrast": {"name": "Для слабовидящих", "relative_path": Path("high-contrast.css")},
}


def ensure_theme_directories():
    THEMES_ROOT.mkdir(parents=True, exist_ok=True)
    BUILTIN_ROOT.mkdir(parents=True, exist_ok=True)
    UPLOADED_ROOT.mkdir(parents=True, exist_ok=True)
    if not THEME_CONFIG_PATH.exists():
        THEME_CONFIG_PATH.write_text(json.dumps({"default_theme_key": "builtin-light"}, ensure_ascii=False, indent=2), encoding="utf-8")



def _theme_file_url(theme_key: str, relative_path: Path) -> str:
    return reverse("theme_asset", kwargs={"theme_key": theme_key, "asset_path": str(relative_path).replace('\\', '/')})



def _build_builtin_theme(theme_key: str, theme_name: str, relative_path: Path) -> dict:
    theme_path = BUILTIN_ROOT / relative_path
    return {
        "key": theme_key,
        "name": theme_name,
        "source": "builtin",
        "css_path": theme_path,
        "relative_path": relative_path,
        "css_url": _theme_file_url(theme_key, relative_path),
        "uploaded_at": None,
    }



def _discover_uploaded_theme(theme_dir: Path):
    css_files = list(theme_dir.rglob("*.css"))
    if not css_files:
        return None

    preferred_names = ("bootstrap.min.css", "bootstrap.css")
    selected_css = None
    for preferred_name in preferred_names:
        for candidate in css_files:
            if candidate.name.lower() == preferred_name:
                selected_css = candidate
                break
        if selected_css:
            break
    if not selected_css:
        css_files.sort(key=lambda item: (item.name.lower() != "theme.css", -item.stat().st_size, str(item).lower()))
        selected_css = css_files[0]

    try:
        display_name = theme_dir.name.split("_", 1)[1].replace("-", " ").strip().title()
    except IndexError:
        display_name = theme_dir.name.replace("-", " ").title()

    relative_path = selected_css.relative_to(theme_dir)
    return {
        "key": theme_dir.name,
        "name": display_name,
        "source": "uploaded",
        "css_path": selected_css,
        "relative_path": relative_path,
        "css_url": _theme_file_url(theme_dir.name, relative_path),
        "uploaded_at": theme_dir.stat().st_mtime,
    }



def list_available_themes():
    ensure_theme_directories()
    themes = [
        _build_builtin_theme(theme_key, meta["name"], meta["relative_path"])
        for theme_key, meta in BUILTIN_THEMES.items()
        if (BUILTIN_ROOT / meta["relative_path"]).exists()
    ]

    uploaded_themes = []
    for theme_dir in sorted(UPLOADED_ROOT.iterdir()):
        if not theme_dir.is_dir():
            continue
        theme_info = _discover_uploaded_theme(theme_dir)
        if theme_info:
            uploaded_themes.append(theme_info)

    uploaded_themes.sort(key=lambda item: item["uploaded_at"] or 0, reverse=True)
    themes.extend(uploaded_themes)
    return themes



def get_latest_uploaded_theme(themes=None):
    themes = themes or list_available_themes()
    uploaded = [theme for theme in themes if theme["source"] == "uploaded"]
    return uploaded[0] if uploaded else None



def get_theme_by_key(theme_key: str, themes=None):
    if not theme_key:
        return None
    themes = themes or list_available_themes()
    for theme in themes:
        if theme["key"] == theme_key:
            return theme
    return None


def _load_theme_config():
    ensure_theme_directories()
    try:
        return json.loads(THEME_CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"default_theme_key": "builtin-light"}


def get_default_theme_key(themes=None):
    themes = themes or list_available_themes()
    config = _load_theme_config()
    default_key = config.get("default_theme_key") or "builtin-light"
    if get_theme_by_key(default_key, themes=themes):
        return default_key
    return "builtin-light"


def set_default_theme_key(theme_key: str):
    ensure_theme_directories()
    config = _load_theme_config()
    config["default_theme_key"] = theme_key
    THEME_CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")



def get_active_theme(request, themes=None):
    themes = themes or list_available_themes()
    preview_key = ""
    if hasattr(request, "GET"):
        preview_key = (request.GET.get("preview_theme") or "").strip()
    if preview_key and get_theme_by_key(preview_key, themes=themes):
        return get_theme_by_key(preview_key, themes=themes)

    theme_key = request.session.get(THEME_SESSION_KEY) if hasattr(request, "session") else None
    if not theme_key:
        theme_key = get_default_theme_key(themes=themes)
    theme = get_theme_by_key(theme_key, themes=themes)
    if theme:
        return theme
    return get_theme_by_key(get_default_theme_key(themes=themes), themes=themes) or get_theme_by_key("builtin-light", themes=themes)



def set_active_theme(request, theme_key: str):
    if hasattr(request, "session"):
        request.session[THEME_SESSION_KEY] = theme_key
        request.session.modified = True



def slugify_theme_name(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", name).strip("-_").lower()
    return cleaned or "theme"



def _safe_archive_members(archive: zipfile.ZipFile):
    members = []
    for member in archive.infolist():
        member_path = Path(member.filename)
        if member_path.is_absolute() or ".." in member_path.parts:
            continue
        if member.is_dir():
            continue
        members.append(member)
    return members



def install_theme_from_zip(uploaded_file):
    ensure_theme_directories()

    original_name = Path(uploaded_file.name or "theme.zip").stem
    slug = slugify_theme_name(original_name)
    existing_dirs = sorted(UPLOADED_ROOT.glob(f"*_{slug}"))
    next_index = len(existing_dirs) + 1
    target_dir = UPLOADED_ROOT / f"{next_index:03d}_{slug}"
    target_dir.mkdir(parents=True, exist_ok=False)

    try:
        with zipfile.ZipFile(uploaded_file) as archive:
            members = _safe_archive_members(archive)
            if not members:
                raise ValueError("Архив не содержит допустимых файлов.")
            archive.extractall(target_dir, members=members)
    except zipfile.BadZipFile as exc:
        shutil.rmtree(target_dir, ignore_errors=True)
        raise ValueError("Загруженный файл не является корректным ZIP-архивом.") from exc
    except Exception:
        shutil.rmtree(target_dir, ignore_errors=True)
        raise

    theme = _discover_uploaded_theme(target_dir)
    if not theme:
        shutil.rmtree(target_dir, ignore_errors=True)
        raise ValueError("В архиве не найден CSS-файл темы Bootstrap.")

    return theme


def delete_uploaded_theme(theme_key: str):
    ensure_theme_directories()
    if theme_key in BUILTIN_THEMES:
        raise ValueError("Встроенные темы нельзя удалять.")

    theme_dir = (UPLOADED_ROOT / theme_key).resolve()
    allowed_root = UPLOADED_ROOT.resolve()
    if not str(theme_dir).startswith(str(allowed_root)) or not theme_dir.exists() or not theme_dir.is_dir():
        raise ValueError("Тема для удаления не найдена.")

    shutil.rmtree(theme_dir, ignore_errors=False)



def get_theme_asset_path(theme_key: str, asset_path: str):
    ensure_theme_directories()
    asset_rel_path = Path(asset_path)
    if asset_rel_path.is_absolute() or ".." in asset_rel_path.parts:
        raise FileNotFoundError

    if theme_key in BUILTIN_THEMES:
        base_dir = BUILTIN_ROOT
    else:
        base_dir = UPLOADED_ROOT / theme_key

    file_path = (base_dir / asset_rel_path).resolve()
    allowed_root = base_dir.resolve()
    if not str(file_path).startswith(str(allowed_root)) or not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError
    return file_path
