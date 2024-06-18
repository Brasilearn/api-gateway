from django.contrib import admin
from .models import User, UserSkills, Topic, Level, Question, WeeklyChallenge, Score
# Register your models here.
admin.site.register(User)
admin.site.register(UserSkills)
admin.site.register(Topic)
admin.site.register(Level)
admin.site.register(Question)
admin.site.register(WeeklyChallenge)
admin.site.register(Score)
