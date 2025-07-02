from django.shortcuts import render

from .models import Category


def index(request):
    categories = Category.objects.all()

    category_data = []
    for cat in categories:
        recent_posts = cat.posts.order_by('-created_at')[:2]
        category_data.append((cat, recent_posts))

    return render(request, 'main/index.html', {'category_data': category_data})
