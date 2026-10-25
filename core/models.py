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

    topic = models.CharField(max_length=100, default='General')

    question_text = models.TextField()

    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)

    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question_text


class SkillExchangeRequest(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_exchange_requests'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_exchange_requests'
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"


class Review(models.Model):
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )

    reviewed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )

    rating = models.IntegerField()

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.reviewer.username} → {self.reviewed_user.username}"

    


class LearningHelpRequest(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='learning_help_requests'
    )

    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    description = models.TextField()
    attempted_solution = models.TextField(blank=True)

    preferred_duration = models.PositiveIntegerField(default=30)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject}: {self.topic} - {self.author.username}"


class HelpOffer(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Completed', 'Completed'),
    ]

    help_request = models.ForeignKey(
        LearningHelpRequest,
        on_delete=models.CASCADE,
        related_name='offers'
    )

    helper = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='learning_help_offers'
    )

    message = models.TextField(
        blank=True,
        help_text="Explain how you can help the learner."
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['help_request', 'helper'],
                name='unique_help_offer_per_user'
            )
        ]

    def __str__(self):
        return f"{self.helper.username} offers help: {self.help_request.topic}"
