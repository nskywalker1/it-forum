from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter your comment',
                                             'class': 'w-full px-3 py-2 bg-gray-800 border border-gray-600 '
                                                      'rounded-md text-white '
                                                      'placeholder-gray-400 focus:outline-none focus:ring-2 '
                                                      'focus:ring-green-500 '
                                                      'focus:border-transparent resize-none'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category']
