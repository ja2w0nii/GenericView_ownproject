from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from .models import Post, Comment
from .forms import ImageUploadForm


class PostListView(generic.ListView):
    model = Post
    template_name = "home.html"


# class PostUploadView(generic.FormView):
#     """이미지를 업로드하는 폼 클래스"""

#     form_class = ImageUploadForm
#     template_name = "post_upload.html"

#     def form_valid(self, form):
#         image, _ = Post.objects.update_or_create(
#             post_image=form.cleaned_data["image"],
#         )
#         return JsonResponse({"url": image.pk})


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = "post"
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        post = self.get_object()
        kwargs["title"] = Post.objects.filter(title=post.title)
        kwargs["image"] = Post.objects.filter(image=post.image)
        kwargs["content"] = Post.objects.filter(content=post.content)
        return super().get_context_data(**kwargs)
