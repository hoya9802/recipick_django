import os
from django.core.asgi import get_asgi_application
import django

# 환경변수 설정 (Django 설정 파일을 지정)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipick_app.settings')

# Django 초기화
django.setup()

# channels 라우팅과 미들웨어는 Django 초기화 이후에 가져와야 합니다.
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

# Django ASGI 애플리케이션 초기화
django_asgi_app = get_asgi_application()

# ASGI 프로토콜 타입별 라우팅 설정
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        ),
})
