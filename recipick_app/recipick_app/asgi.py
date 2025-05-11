"""
ASGI config for recipick_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application

# channels 라우팅과 미들웨어는 Django 초기화 이후에 가져와야 합니다.
from channels.auth import AuthMiddlewareStack                   # noqa: E402
from channels.routing import ProtocolTypeRouter, URLRouter      # noqa: E402
import chat.routing                                             # noqa: E402

# 환경변수 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipick_app.settings')

# Django ASGI 애플리케이션 초기화
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        ),
})
