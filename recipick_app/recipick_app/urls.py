from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs'
    ),
    path('api/user/', include('user.urls')),
<<<<<<< HEAD
    path('api/report/', include('report.urls')),
=======
    path('api/', include('recipe.urls')),
>>>>>>> a04f3cc98fa6c7f0c2ffa30e9a72ae52e1c09b5a
]
