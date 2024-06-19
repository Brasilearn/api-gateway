from rest_framework import serializers
from .models import User
from .models import UserSkills
from .models import Topic
from .models import Level
from .models import Question
from .models import WeeklyChallenge
from .models import Score
from .models import PontuationUserLevel
from .models import Comunidade, UserComunity, UserProfile ,UserTopicInterest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class UserSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkills
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class WeeklyChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyChallenge
        fields = '__all__'
    
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'user', 'challenge', 'score', 'status']

class AudioJsonSerializer(serializers.Serializer):
    duration_seconds = serializers.FloatField()
    frame_rate = serializers.IntegerField()
    channels = serializers.IntegerField()
    sample_width = serializers.IntegerField()
    audio_bytes = serializers.CharField()
        
class PuntuationUserLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PontuationUserLevel
        fields = '__all__'

class UserTopicInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTopicInterest
        fields = '__all__'

class ComunidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunidade
        fields = '__all__'

class UserComunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComunity
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'