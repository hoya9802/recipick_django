from django.urls import path
from user import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path(
        'mypage/me/',
        views.ManageUserViewSet.as_view({
            'get': 'me',
            'put': 'update',
            'patch': 'partial_update',
        }),
        name='me'
    ),
    path(
        'mypage/me/profile',
        views.ManageUserViewSet.as_view({'post': 'profile'}),
        name='profile'
    ),
    path(
        'mypage/delete/',
        views.ManageUserViewSet.as_view({'post': 'delete'}),
        name='delete'
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
