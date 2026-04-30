from django import template

register = template.Library()


def _decode_mojibake(value: str) -> str:
    if not isinstance(value, str):
        return value
    # Fast-path: skip strings without typical mojibake markers.
    if "Р" not in value and "С" not in value:
        return value

    for encoding in ("cp1251", "latin1"):
        try:
            fixed = value.encode(encoding).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue

        # Apply only if it clearly reduced mojibake pattern.
        before = value.count("Р") + value.count("С")
        after = fixed.count("Р") + fixed.count("С")
        if after < before:
            return fixed

    return value


@register.filter(name="repair_mojibake")
def repair_mojibake(value):
    return _decode_mojibake(value)
