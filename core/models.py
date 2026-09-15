from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)

    skills_to_teach = models.ManyToManyField(
        'Skill',
        related_name='teachers',
        blank=True
    )

    skills_to_learn = models.ManyToManyField(
        'Skill',
        related_name='learners',
        blank=True
    )

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name