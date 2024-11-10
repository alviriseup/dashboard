from django import forms
from blog.models import Post, Category

class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        # widget=forms.TextInput(
        #     attrs={"class": "form-control", "placeholder": "Your Name"}
        # ),
    )

    body = forms.CharField(
        # widget=forms.Textarea(
        #     attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        # ),
    )


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'banner_image_url', 'body', 'categories']
        # widgets = {
        #     # 'categories': forms.CheckboxSelectMultiple,
        #     'categories': forms.SelectMultiple,
        #     # 'categories': forms.SelectMultiple(attrs={
        #     #     'class': 'form-control select2-multiple',
        #     #     'data-toggle': 'select2',
        #     #     'multiple': 'multiple',
        #     #     'data-placeholder': 'Choose categories...'
        #     # }),
        # }
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

