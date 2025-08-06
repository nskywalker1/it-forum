from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.my_profile_redirect, name="my_profile"),
    path("profile/<int:pk>/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path('password-reset/', views.password_reset_request,
         name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm,
         name='password_reset_confirm'),
]
