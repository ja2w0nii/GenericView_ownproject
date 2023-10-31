from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from users.models import User
from posts.models import Post, Comment
from posts.forms import PostUploadForm, CommentUploadForm


# 게시글 조회
class PostListView(generic.ListView):
    model = Post
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        kwargs["users_list"] = User.objects.all()
        return super().get_context_data(**kwargs)


# 게시글 작성
class PostUploadView(generic.FormView):
    template_name = "post_upload.html"
    form_class = PostUploadForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


# 게시글 상세 조회
class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_list"] = Comment.objects.filter(post=self.object)
        return context


# 게시글 수정
class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostUploadForm
    template_name = "post_update.html"


# 게시글 삭제
class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy("posts:post_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


# 댓글 작성
class CommentUploadView(generic.FormView):
    form_class = CommentUploadForm
    template_name = "comment_upload.html"
    success_url = reverse_lazy("posts:post_detail")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs["pk"])
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        success_url = reverse_lazy("posts:post_detail", kwargs={"pk": self.kwargs.get("pk")})
        return success_url


# 댓글 수정
class CommentUpdateView(generic.UpdateView):
    model = Comment
    form_class = CommentUploadForm
    template_name = "comment_update.html"
    success_url = reverse_lazy("posts:post_detail")

    def get_success_url(self):
        post_pk = self.object.post.pk
        success_url = reverse_lazy("posts:post_detail", kwargs={"pk": post_pk})
        return success_url


# 댓글 삭제
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


# 게시글 좋아요 등록/취소
class PostLikeView(generic.View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)

        if post.like_users.filter(id=request.user.id).exists():
            post.like_users.remove(request.user)
        else:
            post.like_users.add(request.user)

        return redirect("posts:post_detail", pk=post.id)


# 게시글 검색
class PostSearchView(generic.ListView):
    model = Post
    context_object_name = "search_results"
    template_name = "post_search.html"

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        return Post.objects.filter(Q(content__icontains=query))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("query", "")
        return context
