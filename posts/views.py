from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.contenttypes.models import ContentType

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
        form.save()
        return super().form_valid(form)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_list"] = Comment.objects.filter(post=self.object)
        return context


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostUploadForm
    template_name = "post_update.html"


class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy("posts:post_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


class CommentDeleteView(generic.DeleteView):
    model = Comment
    context_object_name = "comment"
    success_url = reverse_lazy("posts:post_detail")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

    def get_success_url(self):
        post_pk = self.object.post.pk
        success_url = reverse_lazy("posts:post_detail", kwargs={"pk": post_pk})
        return success_url
