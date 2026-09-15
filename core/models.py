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


class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    score = models.IntegerField()
    level = models.CharField(max_length=20)

    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.skill.name} - {self.score}"

class Question(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    question_text = models.TextField()

    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)

    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question_text