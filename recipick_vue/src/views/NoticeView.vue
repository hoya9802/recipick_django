<template>
    <div class="announcements">
        <img src="@/assets/notice.png" class="noticeimage">
        <table class="announcement-table">
            <thead>
                <tr>
                    <th class="number">번호</th>
                    <th class="title">제목</th>
                    <th class="date">작성일</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(announcement, index) in announcements" :key="announcement.id"
                    @click="goToDetail(announcement.id)" class="announcement-row">
                    <td>{{ announcements.length - index }}</td>
                    <td>{{ announcement.title }}</td>
                    <td>{{ formatDate(announcement.announce_dt) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import apiClient from '@/store/api';

export default {
    name: "NoticeView",
    data() {
        return {
            announcements: [],
        };
    },
    methods: {
        async fetchAnnouncements() {
            try {
                const response = await apiClient.get("/announcements/");
                this.announcements = response.data;
            } catch (error) {
                console.error("공지사항 데이터를 가져오는 중 오류가 발생했습니다.", error);
            }
        },
        goToDetail(id) {
            this.$router.push({ name: "NoticeDetailView", params: { id } });
        },
        formatDate(date) {
            const options = { year: "numeric", month: "2-digit", day: "2-digit" };
            return new Date(date).toLocaleDateString("ko-KR", options);
        },
    },
    mounted() {
        document.title = '공지사항 - Recipick'
        this.fetchAnnouncements();
    },
};
</script>
<style scoped>
.noticeimage {
    margin-top: 10px;
}
.announcement-table {
    width: 50%;
    margin: 20px auto;
    border-collapse: collapse;
}
.announcement-table th,
.announcement-table td {
    padding: 10px;
    text-align: center;
    border: 1px solid #d6d6d6;
    color: black;
}
.announcement-table th {
    border-bottom: 2px solid #000000;
    font-size: 20px;
}
.announcement-row {
    cursor: pointer;
}
.announcement-row:hover {
    background-color: #f9f9f9;
}

.number {
    width: 15%;
    font-size: 17px;
}

.title {
    width: 60%;
    font-size: 17px;
}

.date {
    width: 25%;
    font-size: 17px;
}
</style>

