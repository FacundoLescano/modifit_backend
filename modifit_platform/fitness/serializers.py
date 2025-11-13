from rest_framework import serializers
from .models import Exercise, Rutine, AIGeneratedRoutine


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'exercise', 'count_series', 'count_repeat', 'muscle_to_trainer', 'exercise_day_execution']


class RutineSerializer(serializers.ModelSerializer):
    exercise_detail = ExerciseSerializer(source='exercise', read_only=True)

    class Meta:
        model = Rutine
        fields = ['id', 'name_rutine', 'user', 'exercise', 'exercise_detail']


class AIGeneratedRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIGeneratedRoutine
        fields = ['id', 'user', 'name', 'prompt', 'exercises', 'generated_at', 'updated_at']
        read_only_fields = ['id', 'user', 'generated_at', 'updated_at']


class GenerateRoutineRequestSerializer(serializers.Serializer):
    """
    Serializer para la solicitud de generar una rutina
    """
    prompt = serializers.CharField(max_length=2000, help_text="Descripción del entrenamiento deseado")
    routine_name = serializers.CharField(max_length=255, required=False, help_text="Nombre opcional de la rutina")

    def validate_prompt(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("El prompt debe tener al menos 10 caracteres")
        return value
