from django.urls import path
from .views import LandingPageView, DashboardRedirectView, TraineeDashboardView, TrainerDashboardView, AboutPageView, GalleryPageView,ProgramPageView, MemPageView

app_name = "core"

urlpatterns = [
    # Landing Page
    path("", LandingPageView.as_view(), name="landing"),
    path("about/", AboutPageView.as_view(), name = "about"),
    path("gallery/", GalleryPageView.as_view(), name = "gallery"),
    path("programs/", ProgramPageView.as_view(), name = "programs"),
    path("memberShipPlan/", MemPageView.as_view(), name = "memPlan"),


    # Dashboard Redirect (Handles role-based redirection)
    path("dashboard/", DashboardRedirectView.as_view(), name="dashboard_redirect"),
    
    path("trainee/dashboard/", TraineeDashboardView.as_view(), name="trainee_dashboard"),
   
    path("trainer/dashboard/", TrainerDashboardView.as_view(), name="trainer_dashboard"),
]
