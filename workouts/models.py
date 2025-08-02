from django.db import models
from django.conf import settings
from users.models import CustomUser


class Workout(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    date = models.DateField(auto_now_add=True)

    # Relationships
    trainee = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="workouts",
        limit_choices_to={"role": "trainee"}
    )
    trainers = models.ManyToManyField(
        CustomUser,
        related_name="assigned_workouts",
        limit_choices_to={"role": "trainer"}
    )

    def __str__(self):
        return f"{self.name} - {self.trainee}"

class Exercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name="exercises"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.name} ({self.workout.name})"



class Progress(models.Model):
    STATUS_CHOICES = [
        ('COMPLETED', 'Completed'),
        ('PENDING', 'Pending')
    ]
    
    workout = models.ForeignKey(
        'workouts.Workout',
        on_delete=models.CASCADE,
        related_name='progress_entries'
    )
    trainee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_entries'
    )
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('workout', 'trainee', 'date')  # One progress entry per day per workout
    
    def __str__(self):
        return f"{self.trainee} - {self.workout.name} ({self.date})"
