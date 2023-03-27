from django.urls import path
from . import views


app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("upload/", views.PostUploadView.as_view(), name="post_upload"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("update/<int:pk>/", views.PostUpdateView.as_view(), name="post_update"),
    path("delete/<int:pk>/", views.PostDeleteView.as_view(), name="post_delete"),
]
