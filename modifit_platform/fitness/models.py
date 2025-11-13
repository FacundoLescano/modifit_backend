from django.db import models
from authe.models import User
import json

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

class AIGeneratedRoutine(models.Model):
    """
    Modelo para guardar las rutinas generadas por el modelo de IA
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_routines')
    name = models.CharField(max_length=255)
    prompt = models.TextField()  # El prompt del usuario que generó la rutina
    exercises = models.JSONField(default=list)  # Lista de ejercicios generados
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}"
