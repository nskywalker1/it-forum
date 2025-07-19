from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from main.models import Post


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required(login_url='users:login')
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('users/includes/post_list.html', {'posts': page_obj})
        return JsonResponse({
            'posts_html': html,
            'has_next': page_obj.has_next(),
        })

    return render(request, 'users/profile.html', {'user': user, 'posts': page_obj})


def profile_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'users/profile_detail.html', {'profile': profile})


def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if profile.user != request.user:
        return HttpResponseForbidden("You can't edit someone else's profile.")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', pk=profile.pk)
        else:
            form = UserProfileForm(instance=profile)
        return render(request, 'users/profile_edit.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('users:login')
