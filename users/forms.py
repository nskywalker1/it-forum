from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from .models import User, Profile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Your username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_classes = (
            'w-full px-3 py-2 bg-gray-800 border border-gray-600 '
            'rounded-md text-white placeholder-gray-400 '
            'focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent'
        )

        for field_name in ['username', 'email', 'password1', 'password2']:
            field = self.fields[field_name]
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' ' + common_classes).strip()

            placeholders = {
                'username': 'Your username',
                'email': 'Your email',
                'password1': 'Your password',
                'password2': 'Password confirmation',
            }
            field.widget.attrs['placeholder'] = placeholders[field_name]


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_classes = (
            'w-full px-3 py-2 bg-gray-800 border border-gray-600 '
            'rounded-md text-white placeholder-gray-400 '
            'focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent'
        )

        for field_name in ['email', 'password']:
            field = self.fields[field_name]
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' ' + common_classes).strip()

            placeholders = {
                'email': 'Your email',
                'password': 'Your password',
            }
            field.widget.attrs['placeholder'] = placeholders[field_name]

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password")
            return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio", "github", "telegram", "youtube", "linkedin"]
