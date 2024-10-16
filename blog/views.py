from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404

from blog.models import Post, Comment
from blog.forms import CommentForm, BlogPostForm


def blog_home(request):
    return render(request, "blog/home.html")


def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
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
    post = Post.objects.get(pk=pk)

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
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
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
        # else:
        #     print("Form is not valid")
        #     print(form.errors)  # Print form errors if any
        
    else:
        form = BlogPostForm()

    
    return render(request, "blog/blog_post_form.html", {"form": form})


@login_required
def edit_blog_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
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
    