# form_app/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import IntervieweeForm


class SubmissionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected")
        await self.accept()
        # await self.send(text_data=json.dumps({"message": "Connected to WebSocket!"}))

    async def disconnect(self, close_code):
        print("WebSocket disconnected")

    async def receive(self, text_data):
        print(f"Received: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({"message": f"Received: {message}"}))


    async def send_submission(self, event):
        submission = await self.get_submission_data(event['submission_id'])
        await self.send(text_data=json.dumps({
            'type': 'new_submission',
            'data': submission
        }))

    @sync_to_async
    def get_submission_data(self, submission_id):
        submission = IntervieweeForm.objects.get(id=submission_id)
        return {
            'name': submission.name,
            'designation': submission.designation,
            'skills': submission.skills,
        }















