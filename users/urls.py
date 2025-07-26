from django.urls import path, include
from . import views
app_name = 'users'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
