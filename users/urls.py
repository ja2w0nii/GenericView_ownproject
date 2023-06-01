from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "users"

urlpatterns = [
    # 회원가입/회원탈퇴, 로그인/로그아웃
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("signin/", views.CustomTokenObtainPairView.as_view(), name="signin"),
    path("signout/", views.SignoutView.as_view(), name="signout"),
    path("<int:pk>/unregister/", views.UnregisterView.as_view(), name="unregister"),
    # 프로필
    path("<int:pk>/profile/", views.ProfileView.as_view(), name="profile"),
    path("<int:pk>/profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    # 팔로우
    path("<int:pk>/profile/follow/", views.FollowView.as_view(), name="follow"),
]
