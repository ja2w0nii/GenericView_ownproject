from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView
from keycloak import KeycloakOpenID


from .admin import UserCreationForm
from .forms import SigninForm, ProfileUpdateForm
from .models import User


class SignupView(generic.CreateView):
    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("users:signin")


class CustomTokenObtainPairView(TokenObtainPairView):
    def get(self, request, *args, **kwargs):
        return render(request, "signin.html")

    def post(self, request, *args, **kwargs):
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            if not email or not password:
                return redirect("users:signin")

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                response = super().post(request, *args, **kwargs)
                access_token = response.data.get("access")
                response = redirect("posts:post_list")
                response.set_cookie("access_token", access_token)

                return response

        return redirect("users:signin")


KEYCLOAK_URL = "http://127.0.0.1:8080"
KEYCLOAK_REALM = "genericrealm"
KEYCLOAK_CLIENT_ID = "genericclient"
KEYCLOAK_CLIENT_SECRET = "n5d5aUFAu2pX5yORXmRwKuPkq9m4iKrn"


class KeycloakLoginView(View):
    def get(self, request):
        keycloak_openid = KeycloakOpenID(
            server_url=KEYCLOAK_URL,
            client_id=KEYCLOAK_CLIENT_ID,
            realm_name=KEYCLOAK_REALM,
            client_secret_key=KEYCLOAK_CLIENT_SECRET,
        )

        # Keycloak 로그인 URL 생성
        login_url = keycloak_openid.auth_url(
            redirect_uri=request.build_absolute_uri(
                "http://127.0.0.1:8000/keycloak/login/callback/"
            ),
            scope="openid",
        )

        return HttpResponseRedirect(login_url)


class KeycloakCallbackView(View):
    def get(self, request):
        keycloak_openid = KeycloakOpenID(
            server_url=KEYCLOAK_URL,
            client_id=KEYCLOAK_CLIENT_ID,
            realm_name=KEYCLOAK_REALM,
            client_secret_key=KEYCLOAK_CLIENT_SECRET,
        )

        username = "genericuser"
        password = "genericuser"

        code = request.GET.get("code")
        token = keycloak_openid.token(username=username, password=password, code=code)

        response = redirect("posts:post_list")
        response.set_cookie("access_token", token["access_token"])

        return response


class SignoutView(LogoutView):
    template_name = "home.html"
    next_page = reverse_lazy("users:signin")

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.delete_cookie("access_token")
        return response


class UnregisterView(generic.DeleteView):
    model = User
    template_name = "unregister.html"
    success_url = reverse_lazy("users:signup")

    def post(self, request, *args, **kwargs):
        password_check = request.POST["password_check"]
        if check_password(password_check, request.user.password):
            request.user.delete()
            logout(request)
            response = redirect("users:signin")
            response.delete_cookie("access_token")
            return response


class ProfileView(generic.DetailView):
    model = User
    template_name = "profile.html"


class ProfileUpdateView(generic.UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "profile_update.html"


class FollowView(generic.View):
    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)

        if request.user.follow.filter(id=user.id).exists():
            request.user.follow.remove(user)
        else:
            request.user.follow.add(user)

        return redirect("users:profile", pk=user.id)
