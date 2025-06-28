from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import User, Profile


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
    return redirect(request, 'users/login.html', {'form': form})


def my_profile(request):
    profile = request.user.profile
    return redirect('profile_detail', pk=profile.pk)


def profile_detail(request, pk):
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
