from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("upload", views.PostUploadView.as_view(), name="post_upload"),
]
