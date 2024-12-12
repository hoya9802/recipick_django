# rest_framework의 serializers 모듈을 임포트합니다.
from rest_framework import serializers
# 현재 디렉토리의 models 모듈에서 ChatRoom, Message 모델을 임포트합니다.
from .models import ChatRoom, Message


# Message 모델에 대한 시리얼라이저 클래스입니다.
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message  # Message 모델을 기반으로 합니다.
        fields = "__all__"  # 모든 필드를 포함시킵니다.


# ChatRoom 모델에 대한 시리얼라이저 클래스입니다.
class ChatRoomSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()
    opponent_id = serializers.SerializerMethodField()
    shop_user_id = serializers.SerializerMethodField()
    visitor_user_id = serializers.SerializerMethodField()
    messages = MessageSerializer(
                    many=True,
                    read_only=True,
                    source="messages.all"
                )

    class Meta:
        model = ChatRoom  # ChatRoom 모델을 기반으로 합니다.
        # 시리얼라이즈할 필드들을 지정합니다.
        fields = (
            'id',
            'shop_user_id',
            'visitor_user_id',
            'latest_message',
            'opponent_id',
            'messages'
        )

    # 최신 메시지를 가져오는 메소드입니다.
    def get_latest_message(self, obj):
        latest_msg = Message.objects.filter(
            room=obj).order_by('-timestamp').first()
        if latest_msg:
            return latest_msg.text  # 최신 메시지의 내용을 반환합니다.
        return None  # 메시지가 없다면 None을 반환합니다.

    # 요청 사용자와 대화하는 상대방의 이메일을 가져오는 메소드입니다.
    def get_opponent_id(self, obj):
        request_user_id = self.context['request'].query_params.get('id', None)
        # 요청한 사용자가 상점 사용자일 경우, 방문자의 이메일을 반환합니다.
        if request_user_id == obj.shop_user.id:
            return obj.visitor_user.id
        else:  # 그렇지 않다면, 상점 사용자의 이메일을 반환합니다.
            return obj.shop_user.id

    # shop_user의 이메일을 반환하는 메소드입니다.
    def get_shop_user_id(self, obj):
        return obj.shop_user.id

    # visitor_user의 이메일을 반환하는 메소드입니다.
    def get_visitor_user_id(self, obj):
        return obj.visitor_user.id


class ChatRoomListSerializer(serializers.ModelSerializer):
    shop_user_id = serializers.SerializerMethodField()
    visitor_user_id = serializers.SerializerMethodField()
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'shop_user_id', 'visitor_user_id', 'latest_message']

        # shop_user의 이메일을 반환하는 메소드입니다.
    def get_shop_user_id(self, obj):
        return obj.shop_user.id

    # visitor_user의 이메일을 반환하는 메소드입니다.
    def get_visitor_user_id(self, obj):
        return obj.visitor_user.id

    def get_latest_message(self, obj):
        latest_msg = Message.objects.filter(
            room=obj).order_by('-timestamp').first()
        if latest_msg:
            return latest_msg.text
        return None