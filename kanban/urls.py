from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    BoardViewSet, ListViewSet, CardViewSet, CommentViewSet, 
    UserViewSet, AuthViewSet, LabelViewSet, GoalViewSet, 
    NotificationViewSet, AIAssistantViewSet, PomodoroViewSet, 
    TaskChecklistViewSet, EisenhowerMatrixView, TeamViewSet,
    ImportExportViewSet, shared_board_view, dashboard_stats
)

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'lists', ListViewSet, basename='list')
router.register(r'cards', CardViewSet, basename='card')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'labels', LabelViewSet, basename='label')
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'ai-assistant', AIAssistantViewSet, basename='ai-assistant')
router.register(r'pomodoro', PomodoroViewSet, basename='pomodoro')
router.register(r'checklists', TaskChecklistViewSet, basename='checklist')
router.register(r'eisenhower', EisenhowerMatrixView, basename='eisenhower')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'import-export', ImportExportViewSet, basename='import-export')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', dashboard_stats, name='dashboard_stats'),
    path('api/shared/<str:token>/', shared_board_view, name='shared_board'),
    path('accounts/', include('allauth.urls')),
]