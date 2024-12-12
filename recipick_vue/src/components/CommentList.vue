<template>
    <div>
        <ul class="comment-list">
            <li v-for="comment in comments" :key="comment.id" class="comment-item">
                <div v-if="editingCommentId === comment.id" class="comment-edit">
                    <textarea v-model="editedComment"></textarea>
                    <div class="edit-buttons">
                        <button @click="updateComment(comment.id)">수정</button>
                        <button @click="cancelEdit">취소</button>
                    </div>
                </div>
                <div v-else class="comment-content">
                    <div class="comment-profile-wrapper">
                        <img
                            class="comment-profile"
                            :src="comment.user_profile_image || require('@/assets/default-profile.png')"
                            alt="프로필 이미지"
                        />
                        <div class="comment-body">
                            <div class="comment-header">
                                <strong class="comment-author">{{ comment.user_name }} - {{ comment.user_level }}</strong>
                            </div>
                            <p class="comment-text">{{ comment.content }}</p>
                        </div>
                    </div>
                    <div class="comment-meta">
                        <span class="comment-date">{{ new Date(comment.modify_dt).toLocaleString() }}</span>
                        <div class="comment-actions" v-if="comment.user === currentUserId">
                            <button @click="startEdit(comment)">수정</button>
                            <button @click="deleteComment(comment.id)">삭제</button>
                        </div>
                    </div>
                </div>
            </li>
        </ul>
        <form @submit.prevent="addComment" class="comment-form">
            <textarea v-model="newComment" placeholder="댓글을 입력해주세요."></textarea>
            <button type="submit">등록</button>
        </form>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    props: ["postId", "currentUserId"],
    data() {
        return {
            comments: [],
            newComment: "",
            editingCommentId: null,
            editedComment: "",
        };
    },
    methods: {
        fetchComments() {
            apiClient
                .get(`/comments?post=${this.postId}`)
                .then((response) => {
                    this.comments = response.data;
                })
                .catch((error) => {
                    console.error("댓글 불러오기 실패:", error);
                    alert("댓글을 불러오는 중 문제가 발생했습니다.");
                });
        },
        addComment() {
            apiClient
                .post("/comments/", {
                    post: this.postId,
                    content: this.newComment,
                })
                .then(() => {
                    this.newComment = "";
                    this.fetchComments();
                })
                .catch((error) => {
                    console.error("댓글 등록 실패:", error);
                });
        },
        startEdit(comment) {
            this.editingCommentId = comment.id;
            this.editedComment = comment.content;
        },
        cancelEdit() {
            this.editingCommentId = null;
            this.editedComment = "";
        },
        updateComment(commentId) {
            apiClient
                .patch(`/comments/${commentId}/`, {
                    content: this.editedComment,
                })
                .then(() => {
                    this.fetchComments();
                    this.editingCommentId = null;
                    this.editedComment = "";
                })
                .catch((error) => {
                    console.error("댓글 수정 실패:", error);
                    alert(
                        error.response?.data?.error ||
                        "댓글 수정 중 문제가 발생했습니다."
                    );
                });
        },
        deleteComment(commentId) {
            if (confirm("댓글을 삭제하시겠습니까?")) {
                apiClient
                    .delete(`/comments/${commentId}/`)
                    .then(() => {
                        this.fetchComments();
                    })
                    .catch((error) => {
                        console.error("댓글 삭제 실패:", error);
                        alert(
                            error.response?.data?.error ||
                            "댓글 삭제 중 문제가 발생했습니다."
                        );
                    });
            } else {
                console.log("삭제가 취소되었습니다.");
            }
        },
    },
    mounted() {
        this.fetchComments();
    },
};
</script>

<style scoped>
/* 댓글 목록 스타일 */
.comment-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.comment-item {
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: white;
}

/* 댓글 수정 섹션 */
.comment-edit textarea {
    width: 100%;
    height: 80px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: none;
    font-size: 14px;
}

.edit-buttons {
    margin-top: 10px;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.edit-buttons button {
    width: 50px;
    padding: 5px 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}
.edit-buttons button:first-child {
    background-color: #aa74f1;
    color: white;
}
.edit-buttons button:last-child {
    background-color: #f44336;
    color: white;
}

/* 댓글 내용 섹션 */
.comment-profile-wrapper {
    display: flex;
    align-items: flex-start;
    gap: 10px;
}

.comment-profile {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.comment-body {
    flex-grow: 1;
}

.comment-header {
    font-size: 15px;
    font-weight: bold;
    color: #333;
    text-align: left;
}

.comment-text {
    margin: 5px 0 0;
    font-size: 15px;
    color: #555;
}

/* 댓글 메타 정보 */
.comment-meta {
    margin-top: 10px;
    font-size: 12px;
    color: #888888;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.comment-actions button {
    margin-left: 10px;
    background: none;
    border: none;
    color: #2600ff;
    cursor: pointer;
    font-size: 12px;
}

.comment-actions button:hover {
    text-decoration: underline;
}

/* 댓글 폼 */
.comment-form {
    margin-top: 20px;
}

.comment-form textarea {
    width: 100%;
    height: 60px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: none;
    font-size: 14px;
    margin-bottom: 10px;
}

.comment-form button {
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
    background-color: #576779;
    color: white;
    font-size: 14px;
    cursor: pointer;
}
</style>
