from django.shortcuts import render
from django.views import generic
from .models import Post, Comment


class PostListView(generic.ListView):
    model = Post
    template_name = "home.html"


class PostUploadView(generic.FormView):
    pass
