from django import forms

from english_course.models import UserWord
from .config import TRANSLATION_FIELD_CONFIG, clean_translation_text


class UserWordForm(forms.ModelForm):
    word_text = forms.CharField(label='Word',
                                help_text='Enter the word (e.g. "Run")',
                                widget=forms.TextInput(attrs={'placeholder': 'Enter your word'}))

    translation = forms.CharField(**TRANSLATION_FIELD_CONFIG)

    class Meta:
        model = UserWord
        fields = ['translation']

    def clean_word_text(self):
        data = self.cleaned_data['word_text']
        return data.strip().capitalize()

    def clean_translation(self):
        data = self.cleaned_data['translation']
        return clean_translation_text(data)


class EditUserWordForm(forms.ModelForm):
    class Meta:
        model = UserWord
        fields = ['translation']

    def clean_translation(self):
        data = self.cleaned_data['translation']
        return clean_translation_text(data)
