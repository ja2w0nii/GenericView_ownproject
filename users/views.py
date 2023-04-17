from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from .admin import UserCreationForm
from .forms import SigninForm
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


class ProfileView(generic.ListView):
    model = User
    template_name = "profile.html"


class ProfileUpdateView(generic.UpdateView):
    model = User
    fields = [
        "username",
    ]
    template_name = "profile_update.html"
    success_url = reverse_lazy("posts:post_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)
