from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomSignupView, CustomLoginView, CustomLogoutView

app_name = "users"

urlpatterns = [
    # Authentication
    path("signup/", CustomSignupView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    
]
