# form_app/routing.py
from django.urls import re_path
from .consumers import SubmissionConsumer

websocket_urlpatterns = [
    re_path(r'ws/submissions/$', SubmissionConsumer.as_asgi()),
]
