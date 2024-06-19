from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

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
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    role = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    speaking = models.IntegerField(default=0)
    listening = models.IntegerField(default=0)
    vocabulary = models.IntegerField(default=0)
    reading = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'topic', 'level')

# Topic Model
class Topic(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='topics/', blank=True, null=True)

    def __str__(self):
        return self.title

# Level Model
class Level(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='levels/', blank=True, null=True)

    def __str__(self):
        return self.title

# Question Model
class Question(models.Model):
    QUESTION_TYPES = [
        ('speaking', 'Speaking'),
        ('listening', 'Listening'),
        ('vocabulary', 'Vocabulary'),
        ('reading', 'Reading'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question = models.TextField()
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    options = models.JSONField(blank=True, null=True)
    answer = models.IntegerField()

    def __str__(self):
        return self.question

# WeeklyChallenge Model
class WeeklyChallenge(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.description

# Score Model
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(WeeklyChallenge, on_delete=models.CASCADE)
    score = models.IntegerField()
    status = models.CharField(max_length=20, default='pendiente')

    def __str__(self):
        return f'{self.user.username} - {self.score}'