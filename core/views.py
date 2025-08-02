from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from workouts.models import Workout, Exercise, Progress
from django.utils.timezone import localdate



class LandingPageView(TemplateView):
    template_name = "core/landing_page.html"

class DashboardRedirectView(LoginRequiredMixin, RedirectView):
    """ Redirects users to the appropriate dashboard based on role """
    
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_trainer:
            return reverse_lazy('core:trainer_dashboard')
        return reverse_lazy('core:trainee_dashboard')


class TraineeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/trainee_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = localdate()
        context['workouts'] = self.request.user.workouts.filter(date=today)
        return context

    
class TrainerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/trainer_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        trainer = self.request.user
        trainees_workouts = Workout.objects.filter(trainers = trainer)

        trainees = set()
        for workout in trainees_workouts:
            trainees.add(workout.trainee)

        context['trainees'] = trainees
        return context

class AboutPageView(TemplateView):
    template_name = 'core/about_page.html'

class GalleryPageView(TemplateView):
    template_name = 'core/gallery_page.html'

class ProgramPageView(TemplateView):
    template_name = 'core/programs_page.html'

class MemPageView(TemplateView):
    template_name = 'core/mem_page.html'