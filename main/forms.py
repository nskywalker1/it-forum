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
        fields = ["title", "body", "category"]
