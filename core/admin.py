from django.contrib import admin

from .models import (
    Profile,
    Skill,
    Assessment,
    Question,
    SkillExchangeRequest,
    Message,
    Review
)


admin.site.register(Profile)

admin.site.register(Skill)

admin.site.register(Assessment)

admin.site.register(Question)

admin.site.register(SkillExchangeRequest)

admin.site.register(Message)

admin.site.register(Review)