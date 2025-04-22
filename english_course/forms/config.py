from django import forms

TRANSLATION_FIELD_CONFIG = {
    'label': 'Translation',
    'help_text': 'Use semicolons (;) to separate multiple meanings, e.g., "Бежать; Запускать"',
    'widget': forms.TextInput(attrs={'placeholder': 'Введите перевод через ;'})
}

def clean_translation_text(data):
    raw_items = data.split(';')
    cleaned_items = [item.strip().title() for item in raw_items if item.strip()]
    return '; '.join(sorted(set(cleaned_items)))