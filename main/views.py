from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post, Comment, Like
from .forms import CommentForm, PostForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


def index(request):
    cache_key = "category_data"
    category_data = cache.get(cache_key)
    if category_data is None:
        categories = Category.objects.all()
        categories = sorted(
            categories, key=lambda c: 0 if c.name.lower() == "general" else 1
        )

        category_data = []
        for cat in categories:
            recent_posts = cat.posts.order_by("-created_at")[:2]
            category_data.append((cat, recent_posts))

        cache.set(cache_key, category_data, 300)

    return render(request, "main/index.html", {"category_data": category_data})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.filter(parent__isnull=True)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('users:login')
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get("parent_id")
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            if parent_id:
                new_comment.parent = Comment.objects.get(pk=parent_id)
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


@login_required(login_url="users:login")
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("main:post_detail", post.id)
    else:
        form = PostForm(user=request.user)

    return render(request, "main/create_post.html", {"form": form})


@login_required(login_url="users:login")
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
    return redirect('main:post_detail', post_id=post_id)


def post_search(request):
    form = SearchForm(request.GET or None)
    posts = None
    query = None

    if request.GET and form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        posts = Post.objects.all()

        if query:
            posts = posts.filter(title__icontains=query)
        if category:
            posts = posts.filter(category=category)

    return render(request, 'main/search.html', {"posts": posts, 'form': form, 'query': query})
