from django.contrib import admin
from .models import User, UserSkills, Topic, Level, Question, WeeklyChallenge, Score, PontuationUserLevel, Comunidade, UserComunity, UserProfile,UserTopicInterest
from .models import UserContext
# Register your models here.
admin.site.register(User)
admin.site.register(UserSkills)
admin.site.register(Topic)
admin.site.register(Level)
admin.site.register(Question)
admin.site.register(WeeklyChallenge)
admin.site.register(Score)
admin.site.register(PontuationUserLevel)
admin.site.register(Comunidade)
admin.site.register(UserComunity)
admin.site.register(UserProfile)
admin.site.register(UserTopicInterest)
admin.site.register(UserContext)