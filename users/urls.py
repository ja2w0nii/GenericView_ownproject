from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "users"

urlpatterns = [
    # 회원가입, 로그인/로그아웃
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("signin/", auth_views.LoginView.as_view(template_name="signin.html"), name="signin"),
    path("signout/", auth_views.LogoutView.as_view(), name="signout"),
    # 프로필 수정
    path("<int:pk>/profile/", views.ProfileUpdateView.as_view(), name="profile_update"),
]
