from django.urls import path
from .views import HomeView, GenerateAIRoutineView, ListUserRoutinesView, RoutineDetailView

app_name = 'fitness'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('generate-routine/', GenerateAIRoutineView.as_view(), name='generate-routine'),
    path('user-routines/', ListUserRoutinesView.as_view(), name='user-routines'),
    path('routine/<int:routine_id>/', RoutineDetailView.as_view(), name='routine-detail'),
]
