from django.urls import path

from report import views

app_name = 'report'

urlpatterns = [
    path('reportview/', views.ReportpageView.as_view(), name='reportview'),
]
