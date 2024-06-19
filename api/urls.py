from django.urls import path, include
from rest_framework import routers
from api import views

from rest_framework.authtoken.views import obtain_auth_token
from .views import get_questions, get_levels, get_weekly_challenge, get_user_score, get_user_pontuation, load_pontuation, pathLLM_chatbot, get_user_profile

from .views import UserViewSet, UserSkillsViewSet, TopicViewSet, LevelViewSet, QuestionViewSet, WeeklyChallengeViewSet, ScoreViewSet, AudioUploadView,ComunidadeViewSet,PontuationUserLevelViewSet,UserTopicInterestViewSet
from .views import get_questions, get_levels, get_weekly_challenge, get_user_score, get_user_pontuation, load_pontuation, pathLLM_chatbot, return_id, return_topic
from .views import UserComunityViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-skills', UserSkillsViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'weekly-challenges', WeeklyChallengeViewSet)
router.register(r'scores', ScoreViewSet)

router.register(r'comunidade', ComunidadeViewSet)
router.register(r'pontuation', PontuationUserLevelViewSet)
router.register(r'userTopicInterest' ,UserTopicInterestViewSet)
router.register(r'userComunity', UserComunityViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('upload-audio/', AudioUploadView.as_view(), name='upload_audio'),
    path('login/', obtain_auth_token, name="login" ),

    # Nuevas rutas GET
    path('questions/<int:id_level>/<str:q_type>/', get_questions, name='get_questions'),
    path('level/<int:id_topic>/', get_levels, name='get_levels'),
    path('weeklyChallenge/<int:id_topic>/<str:start_date>/<str:end_date>/', get_weekly_challenge, name='get_weekly_challenge'),
    path('user/<int:id_user>/<int:id_challenge>/', get_user_score, name='get_user_score'),
    path('puntuacion/<int:user_id>/<int:id_topic>/<int:id_level>/', get_user_pontuation, name='get_user_pontuation'),

    # Nuevas rutas POST
    path('pathLLM-chatbot/', pathLLM_chatbot, name='pathLLM_chatbot'),
    path('load_pontuation/', load_pontuation, name='load_pontuation'),

    
    path("GetUserProfile/",get_user_profile, name="get_user_profile" ),
    path("ReturnID/",return_id,name="return_id" ),

    path('return_topic/<str:topic_slug>/', return_topic, name='return_topic'),

]
