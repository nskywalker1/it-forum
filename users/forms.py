from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from .models import User, Profile, Tag


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Your username"}),
            "email": forms.TextInput(attrs={"placeholder": "Your email"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_classes = (
            "w-full px-3 py-2 bg-gray-800 border border-gray-600 "
            "rounded-md text-white placeholder-gray-400 "
            "focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
        )

        for field_name in ["username", "email", "password1", "password2"]:
            field = self.fields[field_name]
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                    existing_classes + " " + common_classes
            ).strip()

            placeholders = {
                "username": "Your username",
                "email": "Your email",
                "password1": "Your password",
                "password2": "Password confirmation",
            }
            field.widget.attrs["placeholder"] = placeholders[field_name]


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_classes = (
            "w-full px-3 py-2 bg-gray-800 border border-gray-600 "
            "rounded-md text-white placeholder-gray-400 "
            "focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
        )

        for field_name in ["email", "password"]:
            field = self.fields[field_name]
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                    existing_classes + " " + common_classes
            ).strip()

            placeholders = {
                "email": "Your email",
                "password": "Your password",
            }
            field.widget.attrs["placeholder"] = placeholders[field_name]

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password")
            return self.cleaned_data


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_classes = (
            "w-full px-3 py-2 bg-gray-800 border border-gray-600 "
            "rounded-md text-white placeholder-gray-400 "
            "focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
        )
        for field_name in ["username", "email"]:
            field = self.fields[field_name]
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                    existing_classes + " " + common_classes
            ).strip()

            placeholders = {
                "username": "Your username",
                "email": "Your email",
            }
            field.widget.attrs["placeholder"] = placeholders[field_name]

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "class": """w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white 
                        placeholder-gray-400 focus:outline-none 
                        focus:ring-2 focus:ring-green-500 focus:border-transparent""",
                "placeholder": "Description",
            }
        ),
    )
    github = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": """w-full px-3 py-2 bg-gray-800 border border-gray-600 
                        rounded-md text-white placeholder-gray-400 
                        focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"""
            }
        ),
    )
    telegram = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": """w-full px-3 py-2 bg-gray-800 border border-gray-600 
                            rounded-md text-white placeholder-gray-400 
                            focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"""
            }
        ),
    )
    linkedin = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": """w-full px-3 py-2 bg-gray-800 border border-gray-600 
                                rounded-md text-white placeholder-gray-400 
                                focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"""
            }
        ),
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                "class": (
                    "w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md "
                    "text-white placeholder-gray-400 focus:outline-none "
                    "focus:ring-2 focus:ring-green-500 focus:border-transparent"
                )
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["avatar", "bio", "github", "telegram", "youtube", "linkedin", "tags"]


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=66,
        widget=forms.EmailInput(attrs={
            "class": """w-full px-3 py-2 bg-gray-800 border border-gray-600 
                        rounded-md text-white placeholder-gray-400 
                        focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent""",
            "placeholder": "Your email",
        })
    )


from django import forms


class PasswordResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": """w-full px-3 py-2 bg-gray-800 border border-gray-600 
                        rounded-md text-white placeholder-gray-400 
                        focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent""",
            "placeholder": "Your password",
        })
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": """w-full px-3 py-2 bg-gray-800 border border-gray-600 
                        rounded-md text-white placeholder-gray-400 
                        focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent""",
            "placeholder": "Confirm your password",
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data
