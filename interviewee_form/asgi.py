"""
ASGI config for interviewee_form project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# interviewee_form/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from form_app.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interviewee_form.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})



# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from form_app.routing import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interviewee_form.settings')

# django_asgi_app = get_asgi_application()

# async def application(scope, receive, send):
#     print(f"Scope: {scope}")  # Log the scope to see what type of connection is being made
#     if scope['type'] == 'websocket':
#         print("WebSocket connection attempt")
#         for route in websocket_urlpatterns:
#             match = route.pattern.match(scope['path'])
#             if match:
#                 print(f"Matched route: {route.pattern}")
#                 instance = route.callback()
#                 await instance(scope, receive, send)
#                 return
#         print("No matching route found")
#         await send({'type': 'websocket.close', 'code': 1003})
#     else:
#         await django_asgi_app(scope, receive, send)

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
# })
