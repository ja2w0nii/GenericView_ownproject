from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from .models import Post, Comment

from .forms import PostUploadForm


class PostListView(generic.ListView):
    model = Post
    template_name = "home.html"


class PostUploadView(generic.FormView):
    template_name = "post_upload.html"
    form_class = PostUploadForm
    success_url = "/"

    def form_valid(self, form):
        print(form)
        form.save()
        return super().form_valid(form)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        post = self.get_object()
        kwargs["title"] = Post.objects.filter(title=post.title)
        kwargs["image"] = Post.objects.filter(image=post.image)
        kwargs["content"] = Post.objects.filter(content=post.content)
        return super().get_context_data(**kwargs)
