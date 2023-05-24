from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from users.utils.jwt import encode_jwt
from datetime import datetime, timedelta

from .admin import UserCreationForm
from .forms import ProfileUpdateForm
from .models import User


def generate_access_token(email):
    iat = datetime.now()
    exp = iat + timedelta(days=7)

    data = {
        "iat": iat.timestamp(),
        "exp": exp.timestamp(),
        "aud": email,
        "iss": "Redux Todo Web Backend",
    }

    return encode_jwt(data)


class SignupView(generic.CreateView):
    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("users:signin")


# session 로그인
# class SigninView(generic.FormView):
#     template_name = "signin.html"
#     form_class = SigninForm
#     success_url = reverse_lazy("posts:post_list")

#     def form_valid(self, form):
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         user = authenticate(self.request, username=email, password=password)
#         if user is not None:
#             login(self.request, user)
#         return super().form_valid(form)


# token 로그인
class SigninView(View):
    def get(self, request):
        return render(request, "signin.html")

    def post(self, request):
        data = {}

        try:
            email = request.POST.get("email")
            password = request.POST.get("password")

            if not email or not password:
                raise ValueError()

            user = User.objects.get(email=email)

            # 토큰 생성
            access_token = generate_access_token(email)

            # 쿠키에 토큰 저장
            response = redirect("posts:post_list")
            response.set_cookie("access_token", access_token)

            data["email"] = email

            user = authenticate(self.request, email=email, password=password)
            if user is not None:
                login(self.request, user)

            return response

        except (ValueError, User.DoesNotExist):
            data["error"] = "유효하지 않은 양식입니다. 다시 작성해주세요."
            return render(request, "signin.html", context=data, status=400)


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
