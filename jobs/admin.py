from django.contrib import admin
from .models import Skill, Profile, Job, Application


admin.site.register(Skill)
admin.site.register(Application)


class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('skills',)

admin.site.register(Profile, ProfileAdmin)


class JobAdmin(admin.ModelAdmin):
    filter_horizontal = ('skills',)

admin.site.register(Job, JobAdmin)