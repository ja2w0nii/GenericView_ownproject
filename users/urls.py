from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    # 회원가입, 로그인/로그아웃
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("signin/", views.SigninView.as_view(), name="signin"),
    path("signout/", views.SignoutView.as_view(), name="signout"),
    # 프로필
    path("<int:pk>/profile/", views.ProfileView.as_view(), name="profile"),
    path("<int:pk>/profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
]
