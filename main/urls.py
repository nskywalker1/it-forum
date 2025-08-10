from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="home"),
    path("topic/<int:post_id>/", views.post_detail, name="post_detail"),
    path(
        "category/<int:category_id>/", views.posts_by_category, name="posts_by_category"
    ),
    path("topic/create/", views.post_create, name="post_create"),
    path('topic/search/', views.post_search, name="post_search"),
    path('like/<int:post_id>/', views.toggle_like, name="toggle_like"),
    path('delete/<int:post_id>/', views.post_delete, name="post_delete"),
]
