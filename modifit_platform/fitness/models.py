from django.db import models
from authe.models import User

class Exercise(models.Model):
    exercise = models.CharField(max_length=255)
    count_series = models.IntegerField()
    count_repeat = models.IntegerField()
    muscle_to_trainer = models.CharField(max_length=255)
    exercise_day_execution = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.exercise

class Rutine(models.Model):
    name_rutine = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_rutine
