from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class IntervieweeForm(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
    ]
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    address = models.TextField()
    designation = models.CharField(max_length=100)
    skills = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    mobile_no = models.BigIntegerField(null=True, blank=True)  
    email = models.TextField(null=True, blank=True)  
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    reference = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


    def __str__(self):
        return self.name


class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    candidate = models.ForeignKey('IntervieweeForm', on_delete=models.CASCADE)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.candidate.name} by {self.interviewer.username}"
