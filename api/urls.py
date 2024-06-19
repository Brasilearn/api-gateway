from django.urls import path, include
from rest_framework import routers
from api import views
<<<<<<< HEAD
from .views import UserViewSet, UserSkillsViewSet, TopicViewSet, LevelViewSet, QuestionViewSet, WeeklyChallengeViewSet, ScoreViewSet, AudioUploadView
=======
from .views import UserViewSet, UserSkillsViewSet, TopicViewSet, LevelViewSet, QuestionViewSet, WeeklyChallengeViewSet, ScoreViewSet
>>>>>>> aaf6ea492d02fa19975f9e891b1d81ba6d10e585

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-skills', UserSkillsViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'weekly-challenges', WeeklyChallengeViewSet)
router.register(r'scores', ScoreViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('upload-audio/', AudioUploadView.as_view(), name='upload_audio')
]
