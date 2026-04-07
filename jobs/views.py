from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Job, Application, Profile
from .forms import ProfileForm


# -------------------------
# Signup View
# -------------------------

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Profile

def signup(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        email = request.POST.get("email")
        phone = request.POST.get("phone")
        role = request.POST.get("role")

        if form.is_valid():

            user = form.save(commit=False)
            user.email = email
            user.save()

            Profile.objects.create(
                user=user,
                role=role,
                phone=phone
            )

            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, "jobs/signup.html", {"form": form})


# -------------------------
# Skill Matching Function
# -------------------------

def calculate_match(user_skills, job_skills):

    user_set = set(user_skills)
    job_set = set(job_skills)

    matched = user_set.intersection(job_set)

    if len(job_set) == 0:
        return 0

    return round((len(matched) / len(job_set)) * 100)


# -------------------------
# Job List View
# -------------------------

def job_list(request):

    jobs = Job.objects.all().order_by('-posted_at')

    applied_jobs = []
    job_matches = []

    if request.user.is_authenticated:

        applied_jobs = Application.objects.filter(
            user=request.user
        ).values_list('job_id', flat=True)

        profile, created = Profile.objects.get_or_create(user=request.user)
        if profile.role == 'recruiter':
            return redirect('recruiter_dashboard')
        user_skills = list(profile.skills.all())

        # Only force skills for candidates
        if profile.role == 'candidate' and not user_skills:
             return redirect('profile')

        for job in jobs:
            job_skills = list(job.skills.all())

            match = calculate_match(user_skills, job_skills)

            # Only show jobs with at least 30% match
            if match >= 30:
                job_matches.append({
                    "job": job,
                    "match": match
                })

    else:
        for job in jobs:
            job_matches.append({
                "job": job,
                "match": 0
            })

    return render(request, 'jobs/job_list.html', {
        'job_matches': job_matches,
        'applied_jobs': applied_jobs,
        'profile' : profile
    })

# -------------------------
# Apply Job
# -------------------------

@login_required
def apply_job(request, job_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'candidate':
        return redirect('job_list')

    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(user=request.user, job=job).exists():
        return redirect('job_list')

    Application.objects.create(user=request.user, job=job)

    return redirect('job_list')

from .forms import JobForm

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            form.save_m2m()
            return redirect('recruiter_dashboard')
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})


@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        

        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('job_list')

    else:
        form = ProfileForm(instance=profile)

    return render(request, "jobs/profile.html", {"form": form})



@login_required
def my_applications(request):

    applications = Application.objects.filter(user=request.user).select_related('job')

    return render(request, 'jobs/my_applications.html', {
        'applications': applications
    })


@login_required
def recruiter_dashboard(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'recruiter':
        return redirect('job_list')
    
    jobs = Job.objects.filter(recruiter=request.user)

    job_data = []

    for job in jobs:
        applicant_count = Application.objects.filter(job=job).count()

        job_data.append({
            'job': job,
            'applicant_count': applicant_count
        })

    return render(request, 'jobs/recruiter_dashboard.html', {
        'job_data': job_data
    })


@login_required
def view_applicants(request, job_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'recruiter':
        return redirect('job_list')

    job = get_object_or_404(Job, id=job_id)

    applications = Application.objects.filter(job=job)

    applicant_data = []

    for application in applications:

        candidate = application.user
        candidate_profile = Profile.objects.get(user=candidate)

        user_skills = list(candidate_profile.skills.all())
        job_skills = list(job.skills.all())

        match = calculate_match(user_skills, job_skills)

        applicant_data.append({
            'candidate': candidate,
            'match': match
        })

    # Sort by highest match score
    applicant_data.sort(key=lambda x: x['match'], reverse=True)

    return render(request, 'jobs/view_applicants.html', {
        'job': job,
        'applicant_data': applicant_data
    })



@login_required
def upload_verification(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":

        certificate = request.FILES.get("certificate")
        company_proof = request.FILES.get("company_proof")
        project_link = request.POST.get("project_link")

        # Candidate uploads certificate
        if profile.role == "candidate":
            if certificate:
                profile.certificate = certificate

            if project_link:
                profile.project_link = project_link

        # Recruiter uploads company proof
        elif profile.role == "recruiter":
            if company_proof:
                profile.company_proof = company_proof

        profile.verification_status = "pending"
        profile.save()

        return redirect("job_list")

    return render(request, "jobs/upload_verification.html")