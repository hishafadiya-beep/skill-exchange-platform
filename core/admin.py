from django.contrib import admin
from .models import Profile, Skill, Assessment, Question

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Assessment)
admin.site.register(Question)