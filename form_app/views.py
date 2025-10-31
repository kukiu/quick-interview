from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import IntervieweeFormForm, FeedbackForm
from .models import IntervieweeForm, Feedback
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from collections import Counter
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.utils import timezone
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg



def welcome_page(request):
    return render(request, 'form_app/welcome.html')

@login_required
def submit_feedback(request, candidate_id):
    candidate = get_object_or_404(IntervieweeForm, id=candidate_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.candidate = candidate
            feedback.interviewer = request.user
            feedback.save()
            candidate.status = 'reviewed'
            candidate.save()
            return redirect('hr_dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'form_app/submit_feedback.html', {'form': form, 'candidate': candidate})

@login_required
def view_feedback(request, candidate_id):
    candidate = get_object_or_404(IntervieweeForm, id=candidate_id)
    feedbacks = Feedback.objects.filter(candidate=candidate)
    return render(request, 'form_app/view_feedback.html', {'candidate': candidate, 'feedbacks': feedbacks})

@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        form = IntervieweeFormForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'submissions_group',
                {
                    'type': 'send_submission',
                    'submission_id': submission.id
                }
            )
            return redirect('success')
    else:
        form = IntervieweeFormForm()
    return render(request, 'form_app/form.html', {'form': form})

def success(request):
    return render(request, 'form_app/success.html')

def index(request):
    return render(request, 'form_app/index.html')

@login_required
def hr_dashboard(request):
    submissions = IntervieweeForm.objects.all().order_by('-submitted_at')

    # Calculate submissions for today
    today = timezone.now().date()
    submissions_today = IntervieweeForm.objects.filter(submitted_at__date=today).count()

    # Data for bar chart: Submissions by designation
    designations = IntervieweeForm.objects.values('designation').annotate(count=Count('designation')).order_by('-count')
    designations_labels = [item['designation'] for item in designations]
    designations_data = [item['count'] for item in designations]

    # Data for pie chart: Distribution of qualifications
    qualifications = IntervieweeForm.objects.values('qualification').annotate(count=Count('qualification')).order_by('-count')
    qualifications_labels = [item['qualification'] for item in qualifications]
    qualifications_data = [item['count'] for item in qualifications]

    # Data for pie chart: Distribution of skills (top 5 skills)
    # Note: This assumes skills are comma-separated in the database
    all_skills = []
    for submission in submissions:
        skills = submission.skills.split(',')
        all_skills.extend([skill.strip() for skill in skills])

    skills_counter = Counter(all_skills)
    top_skills_labels = [skill for skill, count in skills_counter.most_common(5)]
    top_skills_data = [count for skill, count in skills_counter.most_common(5)]

    # Data for line graph: Trends of submissions over time
    daily_trends = (IntervieweeForm.objects
                    .annotate(date=TruncDate('submitted_at'))
                    .values('date')
                    .annotate(count=Count('id'))
                    .order_by('date'))

    weekly_trends = (IntervieweeForm.objects
                     .annotate(week=TruncWeek('submitted_at'))
                     .values('week')
                     .annotate(count=Count('id'))
                     .order_by('week'))

    monthly_trends = (IntervieweeForm.objects
                      .annotate(month=TruncMonth('submitted_at'))
                      .values('month')
                      .annotate(count=Count('id'))
                      .order_by('month'))

    daily_dates = [entry['date'].strftime('%Y-%m-%d') for entry in daily_trends]
    daily_counts = [entry['count'] for entry in daily_trends]

    weekly_dates = [entry['week'].strftime('%Y-%m-%d') for entry in weekly_trends]
    weekly_counts = [entry['count'] for entry in weekly_trends]

    monthly_dates = [entry['month'].strftime('%Y-%m') for entry in monthly_trends]
    monthly_counts = [entry['count'] for entry in monthly_trends]

    pending_reviews = IntervieweeForm.objects.filter(status='pending').order_by('-submitted_at')
    reviewed_reviews = IntervieweeForm.objects.filter(status='reviewed').order_by('-submitted_at')
    avg_response_time = calculate_avg_response_time()
    
     


    context = {
        # Existing context...
        'daily_dates': json.dumps(daily_dates),
        'daily_counts': json.dumps(daily_counts),
        'weekly_dates': json.dumps(weekly_dates),
        'weekly_counts': json.dumps(weekly_counts),
        'monthly_dates': json.dumps(monthly_dates),
        'monthly_counts': json.dumps(monthly_counts),
        'submissions': submissions,
        'submissions_today': submissions_today,
        'designations_labels': json.dumps(designations_labels),
        'designations_data': json.dumps(designations_data),
        'qualifications_labels': json.dumps(qualifications_labels),
        'qualifications_data': json.dumps(qualifications_data),
        'top_skills_labels': json.dumps(top_skills_labels),
        'top_skills_data': json.dumps(top_skills_data),
        'pending_reviews': pending_reviews,
        'reviewed_reviews': reviewed_reviews,
        'avg_response_time': avg_response_time,
    }
    return render(request, 'form_app/hr_dashboard.html', context)


def view_interviewee_form(request, interviewee_id):
    interviewee = get_object_or_404(IntervieweeForm, id=interviewee_id)
    return render(request, 'form_app/view_interviewee_form.html', {'interviewee': interviewee})



def calculate_avg_response_time():
    feedbacks = Feedback.objects.all()

    response_times = []
    for feedback in feedbacks:
        if feedback.candidate.submitted_at and feedback.submitted_at:
            time_diff = feedback.submitted_at - feedback.candidate.submitted_at
            response_times.append(time_diff.total_seconds() / 3600)  # Convert to hours

    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
    else:
        avg_response_time = 0

    return avg_response_time
