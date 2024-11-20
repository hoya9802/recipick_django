from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('mypage/me/', views.ManageUserView.as_view(), name='me'),
    path('mypage/me/delete/', views.DeleteUserView.as_view(), name='delete'),
]
