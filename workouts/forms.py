from django import forms
from django.contrib.auth import get_user_model
from .models import Workout, Exercise, Progress



CustomUser = get_user_model()

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'description', 'duration', 'trainee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Explicitly filter users with role="trainee"
        self.fields['trainee'].queryset = CustomUser.objects.filter(role="trainee")




class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'sets', 'reps']



class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(choices=Progress.STATUS_CHOICES, attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
