<template>
    <div class="chat-list-container">
        <h2>채팅 목록</h2>
        <div class="chat-rooms" v-if="chatRooms.length > 0">
            <div v-for="room in chatRooms" :key="room.id"
                 class="chat-room-item" @click="enterChatRoom(room)">
                <div class="chat-info">
                    <div class="chat-user">상대방: {{ room.opponent_id }}</div>
                    <div class="last-message">{{ room.latest_message || '메시지가 없습니다.' }}</div>
                </div>
                <div class="chat-arrow">→</div>
            </div>
        </div>
        <div v-else class="no-chats">
            진행 중인 채팅이 없습니다.
        </div>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    name: 'ChatListView',
    data() {
        return {
            chatRooms: []
        }
    },
    async created() {
        await this.fetchChatRooms();
    },
    methods: {
        async fetchChatRooms() {
            try {
                const userId = this.$route.query.id;
                const response = await fetch(`http://127.0.0.1:8000/api/rooms/?id=2`);
                const data = await response.json();
                this.chatRooms = data;
            } catch (error) {
                console.error('채팅방 목록을 불러오는데 실패했습니다:', error);
            }
        },
        enterChatRoom(room) {
            this.$router.push({
                path: '/chat/room',
                query: {
                    shop_user_id: room.shop_user_id,
                    visitor_user_id: room.visitor_user_id
                }
            });
        }
    }
}
</script>

<style scoped>
.chat-list-container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
}

.chat-rooms {
    margin-top: 20px;
}

.chat-room-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.chat-room-item:hover {
    background-color: #f5f5f5;
}

.chat-info {
    flex-grow: 1;
}

.chat-user {
    font-weight: bold;
    margin-bottom: 5px;
}

.last-message {
    color: #666;
    font-size: 0.9em;
}

.chat-arrow {
    margin-left: 15px;
    color: #666;
}

.no-chats {
    text-align: center;
    padding: 20px;
    color: #666;
}
</style>