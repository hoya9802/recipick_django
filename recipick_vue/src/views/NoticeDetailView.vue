<template>
    <div class="announcement-detail">
        <div v-if="announcement">
            <h1 class="title">{{ announcement.title }}</h1>
            <div class="black-bar"></div>
            <p class="date">{{ formatDate(announcement.announce_dt) }}</p>
            <div class="contents">{{ announcement.contents }}</div>
            <button @click="goBack">목록</button>
        </div>
        <div v-else>
            <p>로딩 중</p>
        </div>
    </div>
</template>

<script>
import apiClient from '@/store/api';

export default {
    name: "NoticeDetail",
    data() {
        return {
            announcement: null,
        };
    },
    methods: {
        async fetchAnnouncement() {
            try {
                const id = this.$route.params.id;
                const response = await apiClient.get(`/announcements/${id}/`);
                this.announcement = response.data;
                document.title = `${this.announcement.title} - Recipick`;
            } catch (error) {
                console.error("오류가 발생했습니다.", error);
            }
        },
        formatDate(date) {
            const options = { year: "numeric", month: "2-digit", day: "2-digit" };
            return new Date(date).toLocaleDateString("ko-KR", options);
        },
        goBack() {
            this.$router.push({ name: "NoticeView" });
        },
    },
    mounted() {
        this.fetchAnnouncement();
    },
};
</script>

<style scoped>
.announcement-detail {
    width: 60%;
    margin: 50px auto;
    border: 1px solid #d6d6d6;
    padding: 20px;
}
.title {
    color: black;
    font-size: 40px;
    text-align: center;
}
.date {
    color: #888;
    margin-top: 20px;
    margin-bottom: 20px;
    text-align: end;
}
.contents {
    margin-bottom: 30px;
    padding: 20px;
    border: 1px solid #d6d6d6;
    height: 400px;
    text-emphasis: none;
    font-size: 20px;
    overflow-y: auto;
}
button {
    display: block;
    background-color: #575757;
    color: white;
    margin: 0 auto;
    padding: 10px 15px;
    border: none;
    cursor: pointer;
    border-radius: 5px;
}
.black-bar {
    width: 100%;
    height: 2px;
    background-color: #a7a7a7;
    margin: 10px 0;
}
</style>