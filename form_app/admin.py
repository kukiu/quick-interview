from django.contrib import admin
from .models import IntervieweeForm

# Register your models here.

@admin.register(IntervieweeForm)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'qualification', 'address', 'designation','skills')

