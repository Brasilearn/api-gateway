from rest_framework import serializers
from .models import User
from .models import UserSkills
from .models import Topic
from .models import Level
from .models import Question
from .models import WeeklyChallenge
from .models import Score

     
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
<<<<<<< HEAD
        fields = ['id', 'user', 'challenge', 'score', 'status']

class AudioJsonSerializer(serializers.Serializer):
    duration_seconds = serializers.FloatField()
    frame_rate = serializers.IntegerField()
    channels = serializers.IntegerField()
    sample_width = serializers.IntegerField()
    audio_bytes = serializers.CharField()
=======
        fields = ['id', 'user', 'challenge', 'score', 'status']
>>>>>>> aaf6ea492d02fa19975f9e891b1d81ba6d10e585
