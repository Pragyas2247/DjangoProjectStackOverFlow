from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, VoteViewSet, UserViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core import views

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]