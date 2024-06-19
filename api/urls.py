from django.urls import path, include
from rest_framework import routers
from api import views
from .views import UserViewSet, UserSkillsViewSet, TopicViewSet, LevelViewSet, QuestionViewSet, WeeklyChallengeViewSet, ScoreViewSet, AudioUploadView, GetUserProfile

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-skills', UserSkillsViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'weekly-challenges', WeeklyChallengeViewSet)
router.register(r'scores', ScoreViewSet)
router.register(r"GetUserProfile", GetUserProfile)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('upload-audio/', AudioUploadView.as_view(), name='upload_audio')
]
