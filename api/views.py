from django.shortcuts import render
from rest_framework import viewsets
from .models import User, UserSkills, Topic, Level, Question, WeeklyChallenge, Score, UserProfile
from .serializer import UserSerializer, UserSkillsSerializer, TopicSerializer, LevelSerializer, QuestionSerializer, WeeklyChallengeSerializer, ScoreSerializer, AudioJsonSerializer
import base64
from pydub import AudioSegment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from google.cloud import speech_v1p1beta1 as speech
from rest_framework.decorators import action, api_view

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

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

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
    

class UserProfileViewSet(viewsets.ViewSet):
 
    @action(detail=False, methods=['get'])
    def get_user_profile(self, request):
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
        
