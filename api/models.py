from django.db import models

# Create your models here.

class Programmer(models.Model):
    fullname = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name