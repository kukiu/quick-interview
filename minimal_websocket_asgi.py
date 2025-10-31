# minimal_websocket_asgi.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

class DummyConsumer:
    async def __call__(self, scope, receive, send):
        if scope['type'] == 'websocket':
            await send({'type': 'websocket.accept'})
            while True:
                event = await receive()
                if event['type'] == 'websocket.disconnect':
                    break
                if event['type'] == 'websocket.receive':
                    await send({'type': 'websocket.send', 'text': f"Received: {event['text']}"})

websocket_urlpatterns = [
    re_path(r'ws/submissions/$', DummyConsumer()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})
