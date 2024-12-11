from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('rooms/', views.ChatRoomListCreateView.as_view(), name='chat_rooms'),
    path(
        '<int:room_id>/messages',
        views.MessageListView.as_view(),
        name='chat_messages'
    ),
    path('chatrooms/', views.ChatRoomUsersListView.as_view(), name='chat_room_list'),
]
