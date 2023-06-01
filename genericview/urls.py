from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from allauth.socialaccount import urls as socialaccount_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("", include("posts.urls")),
    path("chat/", include("chat.urls")),
    # allauth
    path("accounts/", include("allauth.urls")),
    path("accounts/", include(socialaccount_urls)),
    # keycloak
    # path("keycloak/login/", views.keycloak_login, name="keycloak_login"),
    # path("keycloak/login/callback/", views.keycloak_callback, name="keycloak_callback"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
