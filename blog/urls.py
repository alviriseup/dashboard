from django.urls import path
from . import views


urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("blog_index/", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("create/", views.create_blog_post, name="create_blog_post"),
]