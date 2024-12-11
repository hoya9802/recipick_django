<template>
    <div class="chat-container">
        <!-- 채팅창 -->
        <div class="chat-box">
            <!-- 채팅 메시지 영역 -->
            <div class="chat-messages" ref="chatMessages">
                <div v-for="(message, index) in messages" :key="index" class="message"
                    :class="message.sender_id === currentUserId ? 'sent' : 'received'">
                    <div class="message-content">
                        <span class="sender">{{ message.sender_id }}</span>
                        <p class="text">{{ message.text || message.message}}</p>
                    </div>
                </div>
            </div>
            <!-- 메시지 입력 영역 -->
            <div class="chat-input-container">
                <input type="text" class="chat-input" v-model="messageInput" @keyup.enter="sendMessage"
                    placeholder="메시지를 입력하세요">
                <button class="send-btn" @click="sendMessage">전송</button>
            </div>
        </div>
    </div>
    {{ currentRoomId }}
</template>

<script>
export default {
    name: 'ChatRoomView',
    data() {
        return {
            shopUserId: null,
            currentUserId: null,
            visitorUserId: null,
            currentRoomId: null,
            socket: null,
            messages: [],
            messageInput: ''
        }
    },
    created() {
        // URL 쿼리 파라미터에서 사용자 정보 가져오기
        const { shop_user_id, visitor_user_id, current_user } = this.$route.query;
        if (shop_user_id && visitor_user_id) {
            this.shopUserId = shop_user_id;     // 마켓 글 작성자
            this.visitorUserId = visitor_user_id;  // 현재 로그인한 사용자
            this.currentUserId = current_user;
            this.openOrCreateRoom();
        }
    },
    methods: {
        async loginAsUser(userId) {
            this.currentUserId = userId;
            this.visitorUserId = userId === 'admin' ? 'test1' : 'admin';
            await this.openOrCreateRoom();
        },

        async openOrCreateRoom() {
            if (this.socket) {
                this.socket.close();
            }
            try {
                const response = await fetch('http://127.0.0.1:8000/api/rooms/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        shop_user_id: this.shopUserId,
                        visitor_user_id: this.visitorUserId
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const roomData = await response.json();
                this.currentRoomId = roomData.id;
                this.messages = roomData.messages;

                this.setupWebSocket(this.currentRoomId);
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            } catch (error) {
                console.error('Error:', error);
            }
        },

        setupWebSocket(roomId) {
            this.socket = new WebSocket(`ws://127.0.0.1:8000/ws/room/${roomId}/messages`);
            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.messages.push(data);
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            };
        },

        sendMessage() {
            if (this.messageInput && this.socket) {
                const messagePayload = {
                    sender_id: this.currentUserId,
                    message: this.messageInput,
                    shop_user_id: this.shopUserId,
                    visitor_user_id: this.visitorUserId
                };

                this.socket.send(JSON.stringify(messagePayload));
                this.messageInput = '';
            }
        },

        scrollToBottom() {
            const chatMessages = this.$refs.chatMessages;
            if (chatMessages) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }
    }
}
</script>

<style scoped>
.chat-container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
}

.user-buttons {
    margin-bottom: 20px;
    text-align: center;
}

.login-btn {
    padding: 8px 16px;
    margin: 0 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.login-btn:hover {
    background-color: #45a049;
}

.chat-box {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    background-color: #f9f9f9;
}

.chat-messages {
    height: 400px;
    overflow-y: auto;
    padding: 20px;
    background-color: white;
}

.message {
    margin-bottom: 15px;
    max-width: 70%;
}

.message-content {
    padding: 10px 15px;
    border-radius: 15px;
    position: relative;
}

.sender {
    font-size: 0.8em;
    color: #666;
    margin-bottom: 4px;
    display: block;
}

.text {
    margin: 0;
    word-wrap: break-word;
}

.sent {
    margin-left: auto;
}

.sent .message-content {
    background-color: #0084ff;
    color: white;
}

.sent .sender {
    text-align: right;
    color: #999;
}

.received .message-content {
    background-color: #01ff23;
    color: black;
}

.chat-input-container {
    display: flex;
    padding: 15px;
    background-color: #f8f9fa;
    border-top: 1px solid #ddd;
}

.chat-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-right: 10px;
}

.send-btn {
    padding: 10px 20px;
    background-color: #0084ff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.send-btn:hover {
    background-color: #0073e6;
}

/* 스크롤바 스타일링 */
.chat-messages::-webkit-scrollbar {
    width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.chat-messages::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
    background: #555;
}
</style>