from django.shortcuts import render, redirect
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Skill, Assessment, Question, SkillExchangeRequest, Message, Review
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('dashboard')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile(request, user_id=None):

    if user_id:
        profile = Profile.objects.get(user_id=user_id)
    else:
        profile = Profile.objects.get(user=request.user)

    skills = Skill.objects.all()

    assessments = Assessment.objects.filter(
        user=profile.user
    )

    reviews = Review.objects.filter(
        reviewed_user=profile.user
    )

    # Check if this is the logged-in user's own profile
    is_own_profile = profile.user == request.user

    can_review = False

    if user_id and profile.user != request.user:

        can_review = SkillExchangeRequest.objects.filter(
            status='Accepted'
        ).filter(
            Q(sender=request.user, receiver=profile.user) |
            Q(sender=profile.user, receiver=request.user)
        ).exists()

    # Only allow users to modify their own skills
    if request.method == 'POST' and is_own_profile:

        action = request.POST.get('action')
        skill_id = request.POST.get('skill')

        if skill_id:

            skill = Skill.objects.get(id=skill_id)

            if action == 'teach':
                profile.skills_to_teach.add(skill)

            elif action == 'learn':
                profile.skills_to_learn.add(skill)

            elif action == 'remove_teach':
                profile.skills_to_teach.remove(skill)

                Assessment.objects.filter(
                    user=profile.user,
                    skill=skill
                ).delete()

            elif action == 'remove_learn':
                profile.skills_to_learn.remove(skill)

        return redirect('profile')

    return render(request, 'profile.html', {
        'profile': profile,
        'skills': skills,
        'assessments': assessments,
        'reviews': reviews,
        'can_review': can_review,
        'is_own_profile': is_own_profile
    })

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


@login_required
def assessment(request, skill_id):
    skill = Skill.objects.get(id=skill_id)
    questions = Question.objects.filter(skill=skill)

    if request.method == 'POST':
        score = 0
        topic_scores = {}

        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            topic = question.topic or 'General'

            if topic not in topic_scores:
                topic_scores[topic] = {
                    'correct': 0,
                    'total': 0
                }

            topic_scores[topic]['total'] += 1

            if answer == question.correct_answer:
                score += 1
                topic_scores[topic]['correct'] += 1

        total = questions.count()

        if total > 0:
            percentage = int((score / total) * 100)
        else:
            percentage = 0

        if percentage >= 90:
            level = "Advanced"
        elif percentage >= 70:
            level = "Intermediate"
        elif percentage >= 50:
            level = "Basic"
        else:
            level = "Not Verified"

        topic_results = []
        weak_topics = []

        for topic, data in topic_scores.items():
            if data['total'] > 0:
                topic_percentage = int(
                    (data['correct'] / data['total']) * 100
                )
            else:
                topic_percentage = 0

            topic_results.append({
                'topic': topic,
                'score': topic_percentage,
                'correct': data['correct'],
                'total': data['total']
            })

            if topic_percentage < 50:
                weak_topics.append(topic)

        Assessment.objects.create(
            user=request.user,
            skill=skill,
            score=percentage,
            level=level
        )

        return render(request, 'assessment_result.html', {
            'score': percentage,
            'level': level,
            'skill': skill,
            'topic_results': topic_results,
            'weak_topics': weak_topics
        })

    return render(request, 'assessment.html', {
        'questions': questions,
        'skill': skill
    })


@login_required
def find_people(request):
    skill_name = request.GET.get('skill', '').strip()

    people = []
    compatible_people = []

    if skill_name:

        # People who can teach the skill I want to learn
        people = Profile.objects.filter(
            skills_to_teach__name__icontains=skill_name
        ).exclude(
            user=request.user
        ).distinct()

        # My skills
        my_profile = Profile.objects.get(user=request.user)

        my_teaching_skills = my_profile.skills_to_teach.all()
        my_learning_skills = my_profile.skills_to_learn.all()

        # Find people who can teach what I want to learn
        # AND want to learn something that I can teach
        for person in people:

            person.assessments = Assessment.objects.filter(
                user=person.user,
                skill__name__icontains=skill_name
            ).order_by('-completed_at')

            person.reviews = Review.objects.filter(
                reviewed_user=person.user
            ).order_by('-created_at')

            person.is_compatible = person.skills_to_learn.filter(
                id__in=my_teaching_skills.values_list('id', flat=True)
            ).exists()

            if person.is_compatible:
                compatible_people.append(person)

    return render(request, 'find_people.html', {
        'people': people,
        'compatible_people': compatible_people,
        'skill_name': skill_name
    })


@login_required
def send_exchange_request(request, user_id, skill_id):

    receiver = Profile.objects.get(user_id=user_id).user
    skill = Skill.objects.get(id=skill_id)

    if request.user != receiver:

        existing_request = SkillExchangeRequest.objects.filter(
            sender=request.user,
            receiver=receiver,
            skill=skill
        ).first()

        if existing_request:

            if existing_request.status == 'Rejected':
                existing_request.status = 'Pending'
                existing_request.save()

        else:

            SkillExchangeRequest.objects.create(
                sender=request.user,
                receiver=receiver,
                skill=skill,
                status='Pending'
            )

    return redirect('find_people')

@login_required
def exchange_requests(request):
    received_requests = SkillExchangeRequest.objects.filter(
        receiver=request.user
    ).order_by('-created_at')

    sent_requests = SkillExchangeRequest.objects.filter(
        sender=request.user
    ).order_by('-created_at')

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        exchange_request = SkillExchangeRequest.objects.get(
            id=request_id,
            receiver=request.user
        )

        if action == 'accept':
            exchange_request.status = 'Accepted'
            exchange_request.save()

        elif action == 'reject':
            exchange_request.status = 'Rejected'
            exchange_request.save()

        return redirect('exchange_requests')

    return render(request, 'exchange_requests.html', {
        'received_requests': received_requests,
        'sent_requests': sent_requests
    })

@login_required
def chat(request, user_id):
    other_user = User.objects.get(id=user_id)

    exchange_exists = SkillExchangeRequest.objects.filter(
        status='Accepted'
    ).filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).exists()

    if not exchange_exists:
        return redirect('exchange_requests')

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('created_at')

    if request.method == 'POST':
        message_text = request.POST.get('message')

        if message_text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                message=message_text
            )

        return redirect('chat', user_id=user_id)

    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages
    })

@login_required
def review_user(request, user_id):

    reviewed_user = User.objects.get(id=user_id)

    if reviewed_user == request.user:
        return redirect('profile')

    exchange_exists = SkillExchangeRequest.objects.filter(
        status='Accepted'
    ).filter(
        Q(sender=request.user, receiver=reviewed_user) |
        Q(sender=reviewed_user, receiver=request.user)
    ).exists()

    if not exchange_exists:
        return redirect('user_profile', user_id=user_id)

    if request.method == 'POST':

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating:
            Review.objects.create(
                reviewer=request.user,
                reviewed_user=reviewed_user,
                rating=rating,
                comment=comment
            )

        return redirect('user_profile', user_id=user_id)

    return render(request, 'review.html', {
        'reviewed_user': reviewed_user
    })