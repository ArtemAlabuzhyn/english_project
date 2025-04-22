from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    teacher = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': 'teacher'},
        related_name='students'
    )

    def __str__(self):
        return self.first_name + " " + self.last_name


class Word(models.Model):
    word = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.word


class UserWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    translation = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.translation


class Topic(models.Model):
    topic_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.topic_name


class UserTopicWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
