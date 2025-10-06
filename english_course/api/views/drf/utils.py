def validate_tranlsation(value):
    items = value.split(';')
    cleaned_items = [item.strip().capitalize() for item in items if item.strip()]
    return '; '.join(sorted(set(cleaned_items)))