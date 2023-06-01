from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView


from .admin import UserCreationForm
from .forms import SigninForm, ProfileUpdateForm
from .models import User
from .serializers import CustomTokenObtainPairSerializer


class SignupView(generic.CreateView):
    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("users:signin")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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


# def keycloak_login(request):
#     # keycloak-oic 클라이언트 생성
#     client = Client(client_authn_method=CLIENT_AUTHN_METHOD)

#     # 로그인 시작을 위해 Keycloak 인증 URL 가져오기
#     auth_req = client.construct_AuthorizationRequest(
#         request_args={
#             **request.GET,
#             "response_type": "code",
#             "redirect_uri": "http://127.0.0.1:8000/keycloak/login/callback/",
#         },
#         request_kwargs={
#             "scope": ["openid", "profile", "email"],
#         },
#     )
#     login_url = auth_req.request(client.authorization_endpoint)

#     # Keycloak 로그인 페이지로 리다이렉트
#     return redirect(login_url)


# def keycloak_callback(request):
#     # keycloak-oic 클라이언트 생성
#     client = Client(client_authn_method=CLIENT_AUTHN_METHOD)

#     # 콜백 요청 처리 및 토큰 교환
#     auth_resp = client.parse_response(
#         AuthorizationResponse,
#         info=request.GET,
#         sformat="dict",
#         keyjar=client.keyjar,
#     )
#     token_resp = client.do_access_token_request(
#         state=auth_resp["state"],
#         request_args={
#             "code": auth_resp["code"],
#             "redirect_uri": "http://127.0.0.1:8000/",
#         },
#     )

#     # 토큰 활용 및 로그인 처리
#     if token_resp:
#         # 토큰을 성공적으로 받아왔을 경우, 필요한 후속 처리를 수행합니다.
#         # 예를 들어, 토큰을 쿠키에 저장하거나 사용자 인증을 수행할 수 있습니다.
#         access_token = token_resp["access_token"]
#         # 쿠키에 토큰 저장 등의 후속 처리를 진행합니다.
#         # ...

#         # 로그인 성공 후 리다이렉트할 URL 설정
#         redirect_url = "/"
#         return redirect(redirect_url)
#     else:
#         # 토큰을 받아오지 못했을 경우, 로그인 실패 처리를 수행합니다.
#         redirect_url = "/users/login/"
#         return redirect(redirect_url)


class SignoutView(LogoutView):
    template_name = "home.html"
    next_page = reverse_lazy("users:signin")


class UnregisterView(generic.DeleteView):
    model = User
    template_name = "unregister.html"
    success_url = reverse_lazy("users:signup")

    def post(self, request, *args, **kwargs):
        password_check = request.POST["password_check"]
        if check_password(password_check, request.user.password):
            request.user.delete()
            return redirect("/users/signup")


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
