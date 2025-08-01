from django.db import models
from django.urls import reverse
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    bg_color = models.CharField(max_length=20, default="bg-gray-600")
    text_color = models.CharField(max_length=20, default="text-gray-400")
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to="images/%Y/%m/%d", blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    def total_comments(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} ({'Reply' if self.parent else 'Main'})"

    def is_reply(self):
        return self.parent is not None
