from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill, Assessment, Question

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('/')

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
            return redirect('/')

    return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    skills = Skill.objects.all()
    assessments = Assessment.objects.filter(user=request.user)

    if request.method == 'POST':
        skill_id = request.POST.get('skill')
        skill = Skill.objects.get(id=skill_id)

        if 'teach' in request.POST:
            profile.skills_to_teach.add(skill)

        if 'learn' in request.POST:
            profile.skills_to_learn.add(skill)

        return redirect('/profile/')

    return render(request, 'profile.html', {
        'profile': profile,
        'skills': skills,
        'assessments': assessments
    })

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
@login_required
def assessment(request):
    questions = Question.objects.filter(skill__name='Python')

    if request.method == 'POST':
        score = 0

        for question in questions:
            answer = request.POST.get(f'question_{question.id}')

            if answer == question.correct_answer:
                score += 1

        total = questions.count()
        percentage = int((score / total) * 100)

        if percentage >= 90:
            level = "Advanced"
        elif percentage >= 70:
            level = "Intermediate"
        elif percentage >= 50:
            level = "Basic"
        else:
            level = "Not Verified"

        skill = Skill.objects.get(name='Python')

        Assessment.objects.create(
            user=request.user,
            skill=skill,
            score=percentage,
            level=level
        )

        return render(request, 'assessment_result.html', {
            'score': percentage,
            'level': level
        })

    return render(request, 'assessment.html', {
        'questions': questions
    })

@login_required
def find_people(request):
    skill_name = request.GET.get('skill', '')

    people = []

    if skill_name:
        people = Profile.objects.filter(
            skills_to_teach__name__icontains=skill_name
        ).exclude(user=request.user)

    return render(request, 'find_people.html', {
        'people': people,
        'skill_name': skill_name
    })