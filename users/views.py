from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from .models import CustomUser

class CustomSignupView(CreateView):
    form_class = CustomUserCreationForm
    model = CustomUser
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")

class CustomLoginView(LoginView):
    template_name = "users/login.html"

class CustomLogoutView(LogoutView):
    pass

