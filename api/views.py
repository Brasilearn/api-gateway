from django.shortcuts import render
from rest_framework import viewsets , generics
from .models import User, UserSkills, Topic, Level, Question, WeeklyChallenge, Score, UserProfile,PontuationUserLevel,Comunidade,UserComunity,UserTopicInterest
from .serializer import UserSerializer, UserSkillsSerializer, TopicSerializer, LevelSerializer, QuestionSerializer, WeeklyChallengeSerializer, ScoreSerializer, AudioJsonSerializer,ComunidadeSerializer,UserComunitySerializer,UserTopicInterestSerializer, PontuationUserLevelSerializer
import base64
from pydub import AudioSegment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from google.cloud import speech_v1p1beta1 as speech
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(["POST"])
def logout_user(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({"Message": "You are logget out"}, status = status.HTTP_200) 



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserSkillsViewSet(viewsets.ModelViewSet):
    queryset = UserSkills.objects.all()
    serializer_class = UserSkillsSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class WeeklyChallengeViewSet(viewsets.ModelViewSet):
    queryset = WeeklyChallenge.objects.all()
    serializer_class = WeeklyChallengeSerializer

class PontuationUserLevelViewSet(viewsets.ModelViewSet):
    queryset = PontuationUserLevel.objects.all()
    serializer_class = PontuationUserLevelSerializer

class UserTopicInterestViewSet(viewsets.ModelViewSet):
    queryset = UserTopicInterest.objects.all()
    serializer_class = UserTopicInterestSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

class ComunidadeViewSet(viewsets.ModelViewSet):
    queryset = Comunidade.objects.all()
    serializer_class = ComunidadeSerializer

class UserComunityViewSet(viewsets.ModelViewSet):
    queryset = UserComunity.objects.all()
    serializer_class = UserComunitySerializer

class AudioUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AudioJsonSerializer(data=request.data)
        if serializer.is_valid():
            audio_data = serializer.validated_data
            audio_bytes = base64.b64decode(audio_data['audio_bytes'])
            
            client = speech.SpeechClient()
            audio = speech.RecognitionAudio(content=audio_bytes)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=audio_data['frame_rate'],
                language_code='pt-BR',
            )
            response = client.recognize(config=config, audio=audio)
            
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            return Response({"transcript": transcript.strip()}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET']) 
def get_user_profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        user_info = User.objects.get(id=user.id)

        user_data = {
            'name': user_info.full_name,
            'username': user_info.username,
            'nacionalidade': user_profile.idioma_estudiado,
            'streak': user_profile.streak,
            'goal': user_profile.objetivo,
            'image_profile': user_profile.profile_pic,  # Se profile_pic for uma ImageField, adicione .url
            'progress': user_profile.progress
        }
        return Response(user_data, status=status.HTTP_202_ACCEPTED)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=404)



@api_view(['GET'])
def return_id(request):
    user_id = request.user.id
    return Response(user_id)
# Vista para obtener preguntas por nivel y tipo
@api_view(['GET'])
def get_questions(request, id_level, q_type):
    questions = Question.objects.filter(level=id_level, type=q_type)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

# Vista para obtener niveles por tópico
@api_view(['GET'])
def get_levels(request, id_topic):
    levels = Level.objects.filter(topic=id_topic)
    serializer = LevelSerializer(levels, many=True)
    return Response(serializer.data)

# Vista para obtener retos semanales filtrados por fecha
@api_view(['GET'])
def get_weekly_challenge(request, id_topic, start_date, end_date):
    challenges = WeeklyChallenge.objects.filter(topic=id_topic, start_date__gte=start_date, end_date__lte=end_date)
    serializer = WeeklyChallengeSerializer(challenges, many=True)
    return Response(serializer.data)

# Vista para obtener score y status por usuario y reto
@api_view(['GET'])
def get_user_score(request, id_user, id_challenge):
    score = Score.objects.filter(user=id_user, challenge=id_challenge).first()
    serializer = ScoreSerializer(score)
    return Response(serializer.data)

# Vista para obtener puntuación del usuario en un nivel
@api_view(['GET'])
def get_user_pontuation(request, user_id, id_topic, id_level):
    pontuation = PontuationUserLevel.objects.filter(user=user_id, level__topic=id_topic, level=id_level).first()
    serializer = PontuationUserLevel(pontuation)
    return Response(serializer.data)

# Vista para actualizar puntuación
@api_view(['POST'])
def load_pontuation(request):
    user_id = request.data.get('id_user')
    topic_id = request.data.get('topic')
    level_id = request.data.get('level')
    pontuation = request.data.get('pontuation')
    
    try:
        pontuation_record = PontuationUserLevel.objects.get(user=user_id, level=level_id)
        if pontuation > 0 and pontuation > pontuation_record.pontuation:
            pontuation_record.pontuation = pontuation
            pontuation_record.save()
            return Response({'status': 'updated'})
    except PontuationUserLevel.DoesNotExist:
        if pontuation > 0:
            new_record = PontuationUserLevel(user_id=user_id, level_id=level_id, pontuation=pontuation)
            new_record.save()
            return Response({'status': 'created'})
    
    return Response({'status': 'failed'}, status=400)

# Vista para chatbot
@api_view(['POST'])
def pathLLM_chatbot(request):
    user_id = request.data.get('id_user')
    prompt = request.data.get('prompt')
    # Implementa la lógica de respuesta del chatbot aquí
    response = "Respuesta del chatbot a: " + prompt
    return Response({'response': response})


@api_view(['GET'])
def return_topic(request, topic_slug):
    try:
        topic = Topic.objects.get(slug=topic_slug)
        serializer = TopicSerializer(topic)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Topic.DoesNotExist:
        return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)