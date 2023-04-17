from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model


class SignupView(generic.CreateView):
    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("users:signin")


class SigninView(LoginView):
    template_name = "signin.html"
    success_url = reverse_lazy("posts:post_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class ProfileView(generic.ListView):
    model = get_user_model()
    template_name = "profile.html"


class ProfileUpdateView(generic.UpdateView):
    model = get_user_model()
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
