from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import AIGeneratedRoutine
from .serializers import AIGeneratedRoutineSerializer, GenerateRoutineRequestSerializer
from .ai_service import AIFitnessService


class HomeView(APIView):
    """
    GET /api/fitness/home/
    Vista principal de fitness - requiere autenticación
    """
    def get(self, request):
        return Response({
            'message': f'Bienvenido a Modifit, {request.user.username}!',
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email
            }
        }, status=status.HTTP_200_OK)


class GenerateAIRoutineView(APIView):
    """
    POST /api/fitness/generate-routine/
    Genera una rutina de ejercicios usando el modelo de IA
    Requiere autenticación JWT
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validar los datos de entrada
        serializer = GenerateRoutineRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        prompt = serializer.validated_data['prompt']
        routine_name = serializer.validated_data.get(
            'routine_name',
            f"Routine_{request.user.id}_{AIGeneratedRoutine.objects.filter(user=request.user).count() + 1}"
        )

        # Llamar al servicio de IA
        ai_service = AIFitnessService()
        ai_result = ai_service.generate_exercises(prompt)

        # Verificar si la generación fue exitosa
        if ai_result['status'] != 'success':
            return Response(
                ai_result,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Guardar la rutina en la base de datos
        try:
            routine = AIGeneratedRoutine.objects.create(
                user=request.user,
                name=routine_name,
                prompt=prompt,
                exercises=ai_result['exercises']
            )

            serializer = AIGeneratedRoutineSerializer(routine)
            return Response(
                {
                    'status': 'success',
                    'message': 'Rutina generada y guardada exitosamente',
                    'routine': serializer.data,
                    'routines': [serializer.data],
                    'raw_response': ai_result.get('raw_response', '')
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'message': f'Error al guardar la rutina: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListUserRoutinesView(APIView):
    """
    GET /api/fitness/user-routines/
    Lista todas las rutinas generadas por IA del usuario autenticado
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            routines = AIGeneratedRoutine.objects.filter(user=request.user).order_by('-generated_at')
            serializer = AIGeneratedRoutineSerializer(routines, many=True)

            return Response(
                {
                    'status': 'success',
                    'count': routines.count(),
                    'routines': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'message': f'Error al obtener rutinas: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RoutineDetailView(APIView):
    """
    GET /api/fitness/routine/<id>/
    Obtiene una rutina específica del usuario
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, routine_id):
        try:
            routine = AIGeneratedRoutine.objects.get(id=routine_id, user=request.user)
            serializer = AIGeneratedRoutineSerializer(routine)

            return Response(
                {
                    'status': 'success',
                    'routine': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except AIGeneratedRoutine.DoesNotExist:
            return Response(
                {
                    'status': 'error',
                    'message': 'Rutina no encontrada'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'message': f'Error: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
