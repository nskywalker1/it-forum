from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('topic/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
]
