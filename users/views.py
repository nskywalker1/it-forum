from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from pyexpat.errors import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from main.models import Post
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm, UserForm, PasswordResetRequestForm, \
    PasswordResetConfirmForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from .tasks import send_welcome_email, send_password_reset_email


def user_register(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Profile.objects.create(user=user)
            send_welcome_email.delay(user.email, user.username)
            return redirect("main:home")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})


def profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    posts = Post.objects.filter(author=profile_user).order_by("-created_at")
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("users/includes/post_list.html", {"posts": page_obj})
        return JsonResponse(
            {
                "posts_html": html,
                "has_next": page_obj.has_next(),
            }
        )

    is_owner = request.user == profile_user

    return render(
        request,
        "users/profile.html",
        {
            "profile_user": profile_user,
            "posts": page_obj,
            "is_owner": is_owner,
        },
    )


@login_required(login_url="users:login")
def my_profile_redirect(request):
    return redirect("users:profile", pk=request.user.pk)


@login_required(login_url="users:login")
def profile_edit(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect("users:profile", pk=user.pk)
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "users/profile_edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                send_password_reset_email.delay(email, user.pk)
                return render(request, 'users/password_reset_done.html')
            else:
                messages.warning(request, "No account found with this email.")
        else:
            messages.error(request, "Please enter a valid email address.")
    else:
        form = PasswordResetRequestForm()
    return render(request, 'users/password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect("main:home")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return render(request, 'users/password_reset_complete.html')
        else:
            form = PasswordResetConfirmForm()
        return render(request, 'users/password_reset_confirm.html', {'form': form, 'validlink': True})
    else:
        return render(request, 'users/password_reset_confirm.html', {'validlink': False})


def user_logout(request):
    logout(request)
    return redirect("users:login")
