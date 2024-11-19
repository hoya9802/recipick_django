from django.urls import path

from report import views

app_name = 'report'

urlpatterns = [
    path('report/', views.ReportView.as_view(), name='report'),
]
