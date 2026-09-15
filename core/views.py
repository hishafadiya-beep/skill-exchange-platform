from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill


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
        'skills': skills
    })

def logout_view(request):
    logout(request)
    return redirect('/')