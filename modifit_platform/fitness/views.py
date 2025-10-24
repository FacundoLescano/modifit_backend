from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
