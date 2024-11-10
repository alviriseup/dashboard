from django.urls import path
from . import views


urlpatterns = [

    # Blog

    path("", views.blog_list, name="blog_list"),
    path("blog_index/", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("post/new/", views.create_blog_post, name="create_blog_post"),
    path("post/<int:pk>/edit/", views.edit_blog_post, name="edit_blog_post"),
    path("post/<int:pk>/delete/", views.delete_blog_post, name="delete_blog_post"),

    # Category

    path("categories/", views.category_list, name="category_list"),
    path("categories/new/", views.create_category, name="create_category"),
    path("categories/<int:pk>/edit/", views.edit_category, name="edit_category"),
    path("categories/<int:pk>/delete/", views.delete_category, name="delete_category"),
]