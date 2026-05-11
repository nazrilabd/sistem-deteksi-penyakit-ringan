from django.contrib import admin
from .models import Project, Certificate, Skill, Profile

admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Certificate)
admin.site.register(Skill)