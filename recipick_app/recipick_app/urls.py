from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/update_check/', core_views.update_check, name='update-check'),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs'
    ),
    path('api/user/', include('user.urls')),
    path('api/report/', include('report.urls')),
    path('api/', include('recipe.urls')),
    path('api/', include('help.urls')),
    path('api/', include('lab.urls')),
    path('api/', include('freemarket.urls')),
    path('api/', include('notification.urls')),
    path('api/', include('chef_ai.urls')),
    path('api/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
