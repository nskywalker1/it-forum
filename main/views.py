from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from .forms import CommentForm, PostForm


def index(request):
    categories = Category.objects.all()
    categories = sorted(
        categories, key=lambda c: 0 if c.name.lower() == "general" else 1
    )

    category_data = []
    for cat in categories:
        recent_posts = cat.posts.order_by("-created_at")[:2]
        category_data.append((cat, recent_posts))

    return render(request, "main/index.html", {"category_data": category_data})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect("main:post_detail", post_id=post_id)
    else:
        form = CommentForm()
        return render(
            request,
            "main/detail.html",
            {"post": post, "form": form, "comments": comments},
        )


def posts_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = category.posts.all()

    return render(
        request, "main/posts_category.html", {"category": category, "posts": posts}
    )


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("main:post_detail", post.id)
    else:
        form = PostForm(user=request.user)

    return render(request, "main/create_post.html", {"form": form})
