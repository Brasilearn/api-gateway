from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# User Model
class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100, null = True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    role = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    is_admin = models.BooleanField(default=False)

# UserSkills Model
class UserSkills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    speaking = models.IntegerField(default=0, blank=True, null=True)
    listening = models.IntegerField(default=0, blank=True, null=True)
    vocabulary = models.IntegerField(default=0, blank=True, null=True)
    reading = models.IntegerField(default=0, blank=True, null=True)

# Topic Model
class Topic(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

# Level Model
class Level(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

# Question Model
class Question(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    question = models.TextField()
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    options = models.TextField(blank=True, null=True)
    answer = models.IntegerField()

    def __str__(self):
        return self.question

# WeeklyChallenge Model
class WeeklyChallenge(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True, default=0)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.description

# Score Model
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(WeeklyChallenge, on_delete=models.CASCADE)
    score = models.IntegerField()
    status = models.CharField(max_length=50, blank=True, null=True, default='pendente')

    def __str__(self):
        return f'{self.user.username} - {self.score}'

# PontuationUserLevel Model
class PontuationUserLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    pontuation = models.IntegerField()

    class Meta:
        unique_together = ('user', 'level')

# UserTopicInterest Model
class UserTopicInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'topic')

# Comunidade Model
class Comunidade(models.Model):
    community_id = models.AutoField(primary_key=True)
    community_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    fecha_creacion = models.IntegerField()
    numero_miembros = models.IntegerField()

    def __str__(self):
        return str(self.community_id)

# UserComunity Model
class UserComunity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Comunidade, on_delete=models.CASCADE)
    fecha_entrada = models.IntegerField()

    class Meta:
        unique_together = ('user', 'community')

# UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    streak = models.IntegerField()
    objetivo = models.IntegerField()
    idioma_estudiado = models.IntegerField()
    progress = models.IntegerField()
    profile_pic = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user)

class UserContext(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    context_data = models.JSONField(default=None, null=True)

    def __str__(self):
        return self.user.email
    
