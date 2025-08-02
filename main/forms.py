from django import forms
from .models import Category, Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Enter your comment",
                    "class": "w-full px-3 py-2 bg-gray-800 border border-gray-600 "
                             "rounded-md text-white "
                             "placeholder-gray-400 focus:outline-none focus:ring-2 "
                             "focus:ring-green-500 "
                             "focus:border-transparent resize-none",
                }
            ),
        }


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if not (self.user and self.user.is_superuser):
            self.fields["category"].queryset = Category.objects.exclude(
                name__iexact="general"
            )

    class Meta:
        model = Post
        fields = ["title", "body", "category", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": """w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-md 
                    text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 
                    focus:border-transparent""",
                    "placeholder": "Enter title",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": """w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-b-md text-white 
                    placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 
                    focus:border-transparent""",
                    "placeholder": "Enter body",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": """w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-md text-white 
                    focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"""
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": """block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 
                    file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-green-600 
                    file:text-white hover:file:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"""
                }
            ),
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Enter title...',
        required=False,
        widget=forms.TextInput(attrs={
            "class": """w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-md 
            text-white placeholder-gray-400 focus:outline-none focus:ring-2 
            focus:ring-green-500 focus:border-transparent""",
            "placeholder": "Enter title",
        }),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All categories",
        widget=forms.Select(attrs={
            "class": """w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none 
            focus:ring-2 focus:ring-green-500 focus:border-transparent"""
        })
    )
