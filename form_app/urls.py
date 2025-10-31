from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit_form, name='submit_form'),
    path('view/<int:interviewee_id>/', views.view_interviewee_form, name='view_interviewee_form'),
    path('welcome/', views.welcome_page, name='welcome_page'),
    path('success/', views.success, name='success'),
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('submit-feedback/<int:candidate_id>/', views.submit_feedback, name='submit_feedback'),
    path('view-feedback/<int:candidate_id>/', views.view_feedback, name='view_feedback'),
]

