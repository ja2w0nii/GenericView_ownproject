from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r"^$", views.chat, name="chat"),
    re_path(r"^(?P<room_name>[^/]+)/$", views.room, name="room"),
]
