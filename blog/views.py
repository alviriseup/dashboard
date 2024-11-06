from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count

from blog.models import Post, Category, Comment
from blog.forms import CommentForm, BlogPostForm, CategoryForm


# -------------- Blog Views Start -------------- #

def blog_home(request):
    return render(request, "blog/home.html")


def blog_index(request):
    posts_list = Post.objects.all().order_by("-created_on").annotate(comment_count=Count('comment'))
    
    paginator = Paginator(posts_list, 4)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    
    context = {
        "posts": posts,
    }
    return render(request, "blog/blog_index.html", context)



def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)



def blog_detail(request, pk):
    post = Post.objects.filter(pk=pk).annotate(comment_count=Count('comment')).first()

    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)


    comments = Comment.objects.filter(post=post)
    # comment_count = comments.count()

    lastest_posts = Post.objects.all().order_by("-created_on")[:3]  # Get the 3 latest posts for the sidebar

    # Fetch the previous post
    previous_post = Post.objects.filter(created_on__lt=post.created_on).order_by("-created_on").first()

    # Fetch the next post
    next_post = Post.objects.filter(created_on__gt=post.created_on).order_by("created_on").first()

    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
        # "comment_count": comment_count,
        "latest_posts": lastest_posts,
        "previous_post": previous_post,
        "next_post": next_post,
    }

    return render(request, "blog/post_detail.html", context)


@login_required
def blog_list(request):
    query = request.GET.get('search', '')
    blogs = Post.objects.filter(title__icontains=query).order_by("-created_on")

    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {'page_obj': page_obj, 'query': query})



@login_required
def create_blog_post(request):
    if request.method == "POST":
        print(request.POST.get('body'))
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # post.body = request.POST.get('body')    # Get the HTML from the hidden textarea
            # print("Post body:", post.body)  # Debug the post body
            post.save()
            form.save_m2m()     # save the mant-to-many data (categories)
            return redirect("blog_list")
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors if any
            print(form)
        
    else:
        form = BlogPostForm()

    
    return render(request, "blog/blog_post_form.html", {"form": form})


@login_required
def edit_blog_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post_title = form.cleaned_data['title']
            form.save()
            messages.success(request, f'Post "{post_title}" has been updated successfully!')
            return redirect("blog_list")
    
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, "blog/blog_post_form.html", {"form": form, "post": post})


@login_required
def delete_blog_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post_title = post.title
        post.delete()
        messages.success(request, f'Post "{post_title}" has been deleted successfully!')
        return redirect("blog_list")


# -------------- Blog Views End -------------- #


# -------------- Category Views Start -------------- #


@login_required
def category_list(request):
    query = request.GET.get('search', '')
    categories = Category.objects.filter(name__icontains=query).order_by("name")

    paginator = Paginator(categories, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/category_list.html', {'page_obj': page_obj, 'query': query})


@login_required
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            form.save()
            messages.success(request, f'Category "{category_name}" created successfully!')
            return redirect('category_list')
        
    else:
        form = CategoryForm()

    return render(request, 'blog/category_form.html', {'form': form}) 



@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        old_category = category.name
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            new_category = form.cleaned_data['name']
            form.save()
            messages.success(request, f'Category "{old_category}" has been changed to "{new_category}" succussfully!')
            return redirect('category_list')
        
    else:
        form = CategoryForm(instance=category)

    return render(request, "blog/category_form.html", {"form": form, "category": category})


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" has been deleted succussfully!')
        return redirect("category_list")
    