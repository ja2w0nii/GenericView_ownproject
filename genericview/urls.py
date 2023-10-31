from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from allauth.socialaccount import urls as socialaccount_urls
from users import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("", include("posts.urls")),
    path("chat/", include("chat.urls")),
    path("detection/", include("detection.urls")),
    # Django Allauth
    path("accounts/", include("allauth.urls")),
    path("accounts/", include(socialaccount_urls)),
    # 로그인 - Keycloak 연동
    path("keycloak/login/", views.KeycloakLoginView.as_view(), name="keycloak_login"),
    path("keycloak/login/callback/", views.KeycloakCallbackView.as_view(), name="keycloak_callback"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
