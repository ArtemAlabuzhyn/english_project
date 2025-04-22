from django import forms
from django.contrib.auth.forms import UserCreationForm
from english_course.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'role']

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        if user and user.role == 'teacher':
            self.fields.pop('role')