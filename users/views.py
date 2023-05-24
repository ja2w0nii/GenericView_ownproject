from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password

from .admin import UserCreationForm
from .forms import SigninForm, ProfileUpdateForm
from .models import User


class SignupView(generic.CreateView):
    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("users:signin")


class SigninView(generic.FormView):
    template_name = "signin.html"
    form_class = SigninForm
    success_url = reverse_lazy("posts:post_list")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


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