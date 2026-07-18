from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from .models import Workout, Exercise, Progress
from .forms import WorkoutForm, ExerciseForm, ProgressForm
from datetime import date, timedelta
from django.views import View
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from users.models import CustomUser
from django.utils.timezone import localdate
from django.utils import timezone
import requests
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count
from collections import defaultdict

class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = 'workouts/workout_detail.html'
    context_object_name = 'workout'

    def get_queryset(self):
        user = self.request.user
        return Workout.objects.filter(trainers=user) | Workout.objects.filter(trainee=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercises'] = self.object.exercises.all()
        context['is_trainer'] = self.request.user.is_trainer  # ✅ Pass is_trainer explicitly
        return context

def preprocess_json_keys(data):
    """
    Recursively replace spaces in JSON keys with underscores.
    """
    if isinstance(data, dict):
        return {key.replace(" ", "_"): preprocess_json_keys(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [preprocess_json_keys(item) for item in data]
    else:
        return data


@login_required
def get_recommendations(request):
    """
    Render the form and fetch diet and workout recommendations from the deployed API.
    Caches results per unique payload to avoid hammering the free-tier Flask API.
    """
    if request.method == 'POST':
        payload = {
            "age": request.POST.get("age"),
            "weight": request.POST.get("weight"),
            "height": request.POST.get("height"),
            "gender": request.POST.get("gender", "Male"),
            "dietary_preference": request.POST.get("dietary_preference"),  # Veg or Non-Veg
            "fitness_goal": request.POST.get("fitness_goal"),  # e.g. "Weight Loss"
        }

        # Build a cache key from the payload so same inputs reuse cached result
        cache_key = "recom_" + "_".join(str(v) for v in payload.values())
        cached = cache.get(cache_key)
        if cached:
            return render(request, 'workouts/recommendation_results.html', {'recommendations': cached})

        try:
            # Call the deployed Flask API with a longer timeout (free tier is slow to wake)
            response = requests.post(
                'https://ai-recom-api-strideup.onrender.com/recommend',
                json=payload,
                timeout=60
            )
            if response.status_code == 429:
                return render(request, 'workouts/recommendation_results.html', {
                    'error': 'The recommendation service is busy. Please wait a moment and try again.'
                })
            response.raise_for_status()
            recommendations = preprocess_json_keys(response.json())
            # Cache result for 1 hour — same inputs don't need a fresh API call
            cache.set(cache_key, recommendations, timeout=3600)
            return render(request, 'workouts/recommendation_results.html', {'recommendations': recommendations})
        except requests.exceptions.Timeout:
            return render(request, 'workouts/recommendation_results.html', {
                'error': 'The recommendation service took too long to respond. It may be waking up — please try again in 30 seconds.'
            })
        except requests.exceptions.RequestException as e:
            return render(request, 'workouts/recommendation_results.html', {'error': str(e)})
    else:
        return render(request, 'workouts/recommendation_form.html')


class WorkoutCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = "workouts/workout_form.html"
    success_url = reverse_lazy("trainer_dashboard")  # Redirect after success

    def test_func(self):
        return self.request.user.role == "trainer"  # Only trainers can create
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.trainers.add(self.request.user)
        return response
    def get_success_url(self):
        return reverse("workouts:workout_detail", kwargs={"pk": self.object.pk})

class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = "workouts/update_workout.html"

    def get_queryset(self):
        return Workout.objects.filter(trainers=self.request.user)


    def get_success_url(self):
        return reverse("workouts:workout_detail", kwargs={"pk": self.object.pk})

class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = "workouts/delete_workout.html"
    success_url = reverse_lazy("core:trainer_dashboard")

    def get_queryset(self):
        return Workout.objects.filter(trainers=self.request.user)

class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "workouts/create_exercise.html"

    def dispatch(self, request, *args, **kwargs):
        """ Ensure only assigned trainers can add exercises. """
        self.workout = get_object_or_404(Workout, pk=self.kwargs["workout_pk"])
        if request.user not in self.workout.trainers.all():
            
            return redirect("core:trainer_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Pass workout to template context. """
        context = super().get_context_data(**kwargs)
        context["workout"] = self.workout  # ✅ Add workout to context
        return context

    def form_valid(self, form):
        """ Assign the workout and save. """
        form.instance.workout = self.workout
        
        return super().form_valid(form)

    def get_success_url(self):
        """ Redirect to workout detail page. """
        return reverse("workouts:workout_detail", kwargs={"pk": self.workout.pk})
    
class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "workouts/update_exercise.html"

    def get_queryset(self):
        """Restricts access to trainers who own the workout."""
        workout = get_object_or_404(Workout, id=self.kwargs["workout_pk"], trainers=self.request.user)
        return workout.exercises.all()


    def get_success_url(self):
        """Redirects to the workout detail page."""
        return reverse("workouts:workout_detail", kwargs={"pk": self.object.workout.pk})
    
class ExerciseDeleteView(LoginRequiredMixin, DeleteView):
    model = Exercise
    template_name = "workouts/delete_exercise.html"

    def get_success_url(self):
        return reverse_lazy("workouts:workout_detail", kwargs={"pk": self.object.workout.pk})
    

class WeeklyWorkoutView(ListView):
    model = Workout
    template_name = "workouts/weekly_workouts.html"
    context_object_name = "workouts"

    def get_queryset(self):
        user = self.request.user
        today = localdate()
        start_of_week = today - timedelta(days=today.weekday())  # Get Monday of current week
        return Workout.objects.filter(trainee=user, date__gte=start_of_week, date__lte=today).order_by("date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workouts = self.get_queryset()
        
        # Group workouts by date (formatted as string)
        weekly_data = {}
        for workout in workouts:
            date_str = workout.date.strftime("%Y-%m-%d")  # Convert to string format "YYYY-MM-DD"
            if date_str not in weekly_data:
                weekly_data[date_str] = []
            weekly_data[date_str].append(workout)

        context["weekly_workouts"] = weekly_data
        return context



class ProgressUpdateView(LoginRequiredMixin, View):
    def get(self, request, workout_pk):
        if request.user.role != "trainee":
            return HttpResponseForbidden("Only trainees can update progress.")
        
        workout = get_object_or_404(Workout, pk=workout_pk, trainee=request.user)

        progress, created = Progress.objects.get_or_create(
            workout=workout,
            trainee=request.user,
            date=timezone.now().date()  # Default to today's date
        )

        form = ProgressForm(instance=progress)
        return render(request, "workouts/update_progress.html", {"form": form, "progress": progress})

    def post(self, request, workout_pk):
        if request.user.role != "trainee":
            return HttpResponseForbidden("Only trainees can update progress.")

        workout = get_object_or_404(Workout, pk=workout_pk, trainee=request.user)

        progress, created = Progress.objects.get_or_create(
            workout=workout,
            trainee=request.user,
            date=timezone.now().date()
        )

        form = ProgressForm(request.POST, instance=progress)

        if form.is_valid():
            form.save()
            return redirect("workouts:workout_detail", pk=workout.pk)

        return render(request, "workouts/update_progress.html", {"form": form, "progress": progress})


class ProgressHistoryView(LoginRequiredMixin, ListView):
    model = Progress
    template_name = "workouts/weekly_progress.html"
    context_object_name = "progress_entries"

    def get_queryset(self):
        user = self.request.user
        if user.role == 'trainee':
            return Progress.objects.filter(trainee=user).order_by('-date')
        elif user.role == 'trainer':
            return Progress.objects.filter(workout__trainers=user).order_by('-date')
        return Progress.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get progress data for the charts
        user = self.request.user

        # Data for Workout Completion Status (Completed vs Pending)
        completed_count = Progress.objects.filter(trainee=user, status="COMPLETED").count()
        pending_count = Progress.objects.filter(trainee=user, status="PENDING").count()
        context['completed_workouts_count'] = completed_count
        context['pending_workouts_count'] = pending_count

        # Data for Workouts per Day (Bar chart)
        workouts_per_day = Workout.objects.filter(trainee=user).annotate(day_count=Count('date')).values('date', 'day_count')
        workout_counts_per_day = [(workout['date'], workout['day_count']) for workout in workouts_per_day]

        context['workout_counts_per_day'] = workout_counts_per_day

        # Data for Workout Trend (Line chart - Completed Workouts Over the Last 7 Days)
        trend_data = {}
        last_7_days = [timezone.now().date() - timezone.timedelta(days=i) for i in range(7)]
        for day in last_7_days:
            completed_count = Progress.objects.filter(trainee=user, status="COMPLETED", date=day).count()
            trend_data[day] = completed_count

        context['trend_data'] = trend_data

        # Group workouts by date for accordion view
        weekly_workouts = defaultdict(list)
        workouts = Workout.objects.filter(trainee=user).order_by('date')

        for workout in workouts:
            weekly_workouts[workout.date].append(workout)

        context['weekly_workouts'] = weekly_workouts

        return context
class TraineeWorkoutListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "workouts/trainee_workouts.html"
    context_object_name = "trainees"

    def get_queryset(self):
        return CustomUser.objects.filter(
            workouts__trainers=self.request.user  # Filter trainees assigned workouts by this trainer
        ).distinct()


def get_health_tip(request):
    # Try to get the health tip from cache first
    health_tip = cache.get('health_tip')
    
    if not health_tip:
        # If not in cache, fetch it from the USDA API
        api_key = settings.USDA_API_KEY
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query=health&api_key={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if "foods" in data and len(data["foods"]) > 0:
                health_tip = data["foods"][0]["description"]
            else:
                health_tip = "No health tip available"
            
            # Cache the health tip for 1 hour (3600 seconds)
            cache.set('health_tip', health_tip, timeout=3600)

        except requests.RequestException as e:
            return JsonResponse({"error": "Failed to fetch health tip", "details": str(e)}, status=500)
    
    # Return the health tip (either from cache or freshly fetched)
    return JsonResponse({"tip": health_tip})
    
def get_nutrition_info(request):
    cache_key = 'nutrition_info_737628064502'
    nutrition_info = cache.get(cache_key)

    if not nutrition_info:
        url = "https://world.openfoodfacts.org/api/v0/product/737628064502.json"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            # Use `or {}` to safely handle null product (API returns null when not found)
            product = data.get("product") or {}
            product_name = product.get("product_name", "Unknown Product")
            calories = product.get("nutriments", {}).get("energy-kcal", "N/A")

            nutrition_info = f"{product_name} contains {calories} kcal per serving."
            cache.set(cache_key, nutrition_info, timeout=3600)

        except Exception:
            # Return a friendly fallback — don't 500, let the UI display a message
            nutrition_info = "Eat balanced meals rich in protein, healthy fats, and complex carbs to fuel your workouts."

    return JsonResponse({"nutrition": nutrition_info})


class WorkoutAPIDataView(View):
    def get(self, request, *args, **kwargs):
        """Fetch exercises from API Ninjas"""
        url = "https://api.api-ninjas.com/v1/exercises"
        headers = {
            'X-Api-Key': settings.API_NINJAS_KEY,
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        return JsonResponse({"error": "Failed to fetch exercises"}, status=500)


    