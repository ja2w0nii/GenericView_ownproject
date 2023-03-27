from django.urls import path
from . import views


app_name = "posts"

urlpatterns = [
    # 게시글 CRUD
    path("", views.PostListView.as_view(), name="post_list"),
    path("upload/", views.PostUploadView.as_view(), name="post_upload"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    # 댓글 CRUD
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),
]
