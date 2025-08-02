from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TRAINEE = 'trainee'
    TRAINER = 'trainer'

    ROLE_CHOICES = [
        (TRAINEE, 'Trainee'),
        (TRAINER, 'Trainer'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_trainer = models.BooleanField(default=False)
    is_trainee = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """ Automatically set is_trainer and is_trainee based on role """
        if self.role == self.TRAINER:
            self.is_trainer = True
            self.is_trainee = False
        elif self.role == self.TRAINEE:
            self.is_trainer = False
            self.is_trainee = True
        super().save(*args, **kwargs)
