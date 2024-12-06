<template>
    <div class="help-detail-container">
        <div v-if="help" class="help-detail">
            <div class="help-header">
                <h1 class="help-title">{{ help.title }}</h1>
                <div class="black-bar"></div>
                <div class="help-meta">
                    <span class="user">{{ help.user.nick_name }} - {{ help.user.level }}</span>
                    <span class="date">Update : {{ help.modify_dt }}</span>
                </div>
            </div>

            <div class="help-image-container">
                <img v-if="help.image" :src="help.image" alt="Help Image" class="help-image" />
            </div>

            <div class="help-content">
                <h2>Question</h2>
                <div class="black-bar"></div>
                <p>{{ help.description }}</p>
            </div>

            <div class="help-comment">
                <h2>Comment</h2>
                <div class="black-bar"></div>
                <p>댓글 예정</p>
            </div>

            <div class="back">
                <button class="back-btn" @click="goBack">목록</button>
            </div>
        </div>
        <div v-else>
            <p>지식인 데이터를 불러오는 중입니다.</p>
        </div>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    name: "HelpDetail",
    data() {
        return {
            help: null,
        };
    },
    async created() {
        const id = this.$route.params.id;
        await this.fetchHelpDetail(id);
    },
    methods: {
        async fetchHelpDetail(id) {
            try {
                const response = await apiClient.get(`/helps/${id}/`);
                this.help = response.data;
                document.title = `${this.help.title} - Recipick`;
            } catch (error) {
                console.error("지식인 상세 정보를 불러오는 중 오류 발생:", error);
                alert("지식인 상세 정보를 불러오지 못했습니다.");
            }
        },
        goBack() {
            this.$router.push("/help");
        },
    },
};
</script>

<style scoped>
.help-detail-container {
    padding: 20px;
    background-color: white
}
.help-detail {
    max-width: 800px;
    margin: auto;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
}
.help-header {
    margin-bottom: 30px;
}
.help-title {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
}
.help-meta {
    display: flex;
    justify-content: space-between;
    margin: 20px;
}
.user {
    color: #777;
    text-align: start;
    font-size: 17px;
}
.date {
    color: #777;
    font-size: 17px;
    text-align: end;
}
.help-image-container {
    margin: 20px 0;
    text-align: center;
}
.help-image {
    max-width: 100%;
    border-radius: 8px;
}
.help-content {
    margin: 0 auto 50px; /* 아래 섹션과 간격 */
    padding: 20px;
    border: 1px solid #ddd; /* 병합 방지 */
    border-radius: 8px;
    overflow: hidden; /* 마진 병합 방지 */
}

.help-comment {
    margin-top: 50px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden; /* 마진 병합 방지 */
    clear: both; /* 질문 섹션과의 시각적 분리 */
}
.help-content h2,
.help-comment h2{
    font-weight: bold;
    font-size: 25px;
    text-align: left;
}
.help-content p {
    font-size: 18px;
    line-height: 1.6; /* 읽기 쉽게 줄 간격 조정 */
    text-align: left;
    max-height: 400px; /* 최대 높이 제한 */
    overflow-y: auto; /* 질문이 너무 길 경우 스크롤 추가 */
}
.help-comment p{
    font-size: 18px;
    text-align: left;
}
.black-bar {
    width: 100%;
    height: 2px;
    background-color: #a7a7a7;
    margin-bottom: 10px;
}

.back {
    margin: 20px;
}
.back-btn {
    display: block;
    margin: auto;
    padding: 10px 20px;
    background-color: #575757;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>