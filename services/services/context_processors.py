from .theme_utils import get_active_theme, get_default_theme_key, get_latest_uploaded_theme, list_available_themes


def theme_context(request):
    themes = list_available_themes()
    return {
        "available_themes": themes,
        "current_theme": get_active_theme(request, themes=themes),
        "default_theme_key": get_default_theme_key(themes=themes),
        "latest_uploaded_theme": get_latest_uploaded_theme(themes=themes),
    }
