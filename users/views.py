from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView


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
