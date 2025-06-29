from django.urls import path, include
from . import views
app_name = 'users'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
]
