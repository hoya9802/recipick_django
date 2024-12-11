from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    print('내가 보인다면 너는 redis를 쓸 수 있는 것이다하하하하핳')
    async def connect(self):
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']

            if not await self.check_room_exists(self.room_id):
                raise ValueError('채팅방이 존재하지 않습니다.')

            group_name = self.get_group_name(self.room_id)

            await self.channel_layer.group_add(group_name, self.channel_name)
            # WebSocket 연결을 수락합니다.
            await self.accept()

        except ValueError as e:
            await self.send_json({'error': str(e)})
            await self.close()

    async def disconnect(self, close_code):
        try:
            group_name = self.get_group_name(self.room_id)
            await self.channel_layer.group_discard(
                group_name,
                self.channel_name
            )

        except Exception:
            pass

    async def receive_json(self, content):
        try:
            # 수신된 JSON에서 필요한 정보를 추출합니다.
            print('여기까지는 오는걸..까...?')
            message = content['message']
            sender_id = content['sender_id']
            shop_user_id = content.get('shop_user_id')
            visitor_user_id = content.get('visitor_user_id')

            # 두 ID가 모두 제공되었는지 확인합니다.
            if not shop_user_id or not visitor_user_id:
                raise ValueError("상점 및 방문자 ID가 모두 필요합니다.")

            # 제공된 ID를 사용하여 방을 가져오거나 생성합니다.
            room = await self.get_or_create_room(shop_user_id, visitor_user_id)

            # room_id 속성을 업데이트합니다.
            self.room_id = str(room.id)

            # 그룹 이름을 가져옵니다.
            group_name = self.get_group_name(self.room_id)
            # 수신된 메시지를 데이터베이스에 저장합니다.
            await self.save_message(room, sender_id, message)
            print('오류가 가고 드뎌 희망이 오는군요')
            # 메시지를 전체 그룹에 전송합니다.
            await self.channel_layer.group_send(group_name, {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id
            })

        except ValueError as e:
            # 값 오류가 있을 경우, 오류 메시지를 전송합니다.
            await self.send_json({'error': str(e)})

    async def chat_message(self, event):
        try:
            # 이벤트에서 메시지와 발신자 이메일을 추출합니다.
            message = event['message']
            sender_id = event['sender_id']  # 발신자 이메일 정보 추출

            # 추출된 메시지와 발신자 이메일을 JSON으로 전송합니다.
            await self.send_json({'message': message, 'sender_id': sender_id})
        except Exception:
            # 일반 예외를 처리하여 오류 메시지를 보냅니다.
            await self.send_json({'error': '메시지 전송 실패'})

    @staticmethod
    def get_group_name(room_id):
        # 방 ID를 사용하여 고유한 그룹 이름을 구성합니다.
        return f"chat_room_{room_id}"

    @database_sync_to_async
    def get_or_create_room(self, shop_user_id, visitor_user_id):
        User = get_user_model()

        shop_user = User.objects.get(id=shop_user_id)
        visitor_user = User.objects.get(id=visitor_user_id)

        room, created = ChatRoom.objects.get_or_create(
            shop_user=shop_user,
            visitor_user=visitor_user
        )
        return room

    @database_sync_to_async
    def save_message(self, room, sender_id, message_text):
        # 발신자 이메일과 메시지 텍스트가 제공되었는지 확인합니다.
        if not sender_id or not message_text:
            raise ValueError("발신자 아이디 및 메시지 텍스트가 필요합니다.")

        User = get_user_model()
        sender = User.objects.get(id=sender_id)
        # 메시지를 생성하고 데이터베이스에 저장합니다.
        # timestamp 필드는 auto_now_add=True 속성 때문에 자동으로 현재 시간이 저장됩니다.
        Message.objects.create(room=room, sender_id=sender, text=message_text)

    @database_sync_to_async
    def check_room_exists(self, room_id):
        # 주어진 ID로 채팅방이 존재하는지 확인합니다.
        return ChatRoom.objects.filter(id=room_id).exists()
