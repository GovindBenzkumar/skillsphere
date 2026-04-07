from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', auth_views.LoginView.as_view(template_name='jobs/login.html'), name='login'),

    path('signup/', views.signup, name='signup'),

    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('jobs/', views.job_list, name='job_list'),

    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),

    path('post-job/', views.post_job, name='post_job'),

    path('profile/', views.profile, name='profile'),

    path('my-applications/', views.my_applications, name='my_applications'),

    path('recruiter-dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),

    path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),

    path('verify/', views.upload_verification, name='upload_verification'),

]