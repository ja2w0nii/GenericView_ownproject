from django.urls import path
from . import views


app_name = "detection"

urlpatterns = [
    path("", views.DetectionView.as_view(), name="detection"),
]
