from django.urls import path
from .views import AiChefAPIView

app_name = 'chef_ai'

urlpatterns = [
    path('ai/generate/', AiChefAPIView.as_view(), name='generate-recipe')
]
