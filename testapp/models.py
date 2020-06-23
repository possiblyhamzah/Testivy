from django.db import models
import json
# Create your models here.

class Test(models.Model):
    user = models.TextField()
    name = models.TextField()
    chapter = models.TextField()
    questions = models.TextField()
    answers = models.TextField(default='0')
    choices = models.TextField(default='0')
    questionScores = models.TextField(default='0')
    userScores = models.TextField(default='0')
    isCompleted = models.BooleanField(default=False)
    userPercentage = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.name}"

class Chapter(models.Model):
    user = models.TextField()
    name = models.TextField()
    questions = models.TextField()
    answers = models.TextField(default='0')
    choices = models.TextField(default='0')
    questionScores = models.TextField(default='0')
    
    def __str__(self):
        return f"{self.name}"