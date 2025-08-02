from django.urls import path
from . import views
from .views import (
    WorkoutDetailView, WorkoutCreateView, WorkoutUpdateView, WorkoutDeleteView,
    ExerciseCreateView, ExerciseUpdateView, ExerciseDeleteView, WeeklyWorkoutView, ProgressUpdateView, ProgressHistoryView, TraineeWorkoutListView, get_health_tip, get_nutrition_info, WorkoutAPIDataView, get_recommendations
)

app_name = "workouts"

urlpatterns = [
    # Workouts
    path("create/", WorkoutCreateView.as_view(), name="workout_create"),
    path("<int:pk>/", WorkoutDetailView.as_view(), name="workout_detail"),
    path("<int:pk>/update/", WorkoutUpdateView.as_view(), name="workout_update"),
    path("<int:pk>/delete/", WorkoutDeleteView.as_view(), name="workout_delete"),

    # Exercises (linked correctly to workouts)
    path("<int:workout_pk>/exercises/create/", ExerciseCreateView.as_view(), name="exercise_create"),
    path("<int:workout_pk>/exercises/<int:pk>/update/", ExerciseUpdateView.as_view(), name="exercise_update"),
    path("<int:workout_pk>/exercises/<int:pk>/delete/", ExerciseDeleteView.as_view(), name="exercise_delete"),

    path('weekly/', WeeklyWorkoutView.as_view(), name='weekly_workout'),

    path('<int:workout_pk>/progress/update/', ProgressUpdateView.as_view(), name='progress_update'),
    path('progress/history/', ProgressHistoryView.as_view(), name='progress_history'),

    path("trainees/", TraineeWorkoutListView.as_view(), name="trainee_workouts"),

    path('api/health-tip/', get_health_tip, name='health_tip'),
    path('api/nutrition-info/', get_nutrition_info, name='nutrition_info'),

    path("trainer/exercises/", WorkoutAPIDataView.as_view(), name="trainer_exercises_api"),
    path('recommendations/', get_recommendations, name='get_recommendations'),

]
