from django import forms
from .models import Job, Profile


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'salary', 'job_type', 'description', 'skills']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['skills', 'resume']