<template>
    <div class="expiration-detail">
        <div v-if="expiration">
            <h1 class="title">{{ expiration.title }}</h1>
            <div class="black-bar"></div>
            <img :src="expiration.image" alt="이미지" class="detail-image" />
            <div class="detail-description">
                <p class="detail-title">Description</p>
                <div class="black-bar"></div>
                <p class="detail-content">{{ expiration.description }}</p>
                <p class="detail-title">The source</p>
                <div class="black-bar"></div>
                <p v-if="expiration.url" class="detail-content">
                    <a :href="expiration.url" target="_blank">{{ expiration.url }}</a>
                </p>
            </div>
            <button @click="goBack" class="back-button">목록</button>
        </div>

        <div v-else>
            <p>로딩 중...</p>
        </div>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    name: "ExpirationsDetail",
    data() {
        return {
            expiration: null,
        };
    },
    methods: {
        async fetchExpiration() {
            try {
                const id = this.$route.params.id;
                const response = await apiClient.get(`/expirations/${id}/`);
                this.expiration = response.data;
                document.title = `${this.expiration.title} - Recipick`;
            } catch (error) {
                console.error("유통기한 세부 데이터를 가져오는 중 오류가 발생했습니다.", error);
            }
        },
        goBack() {
            this.$router.push({ name: "Expirations" });
        },
    },
    mounted() {
        this.fetchExpiration();
    },
};
</script>

<style scoped>
.expiration-detail {
    width: 60%;
    margin: 50px auto;
    text-align: center;
    border: 1px solid #d6d6d6;
    padding: 20px;
    background-color: #fff;
}
.title {
    font-size: 40px;
    text-align: center;
    color: black;
}
.detail-image {
    width: auto;
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px auto 20px;
}
.detail-title{
    font-size: 25px;
    font-weight: bold;
    text-align: start;
    margin-top: 30px;
    margin-bottom: 0px;
}
.detail-description {
    text-align: left;
    margin: 20px 0;
}
.detail-content {
    width: 100%;
    margin: 20px 3px;
    font-size: 18px;
    line-height: 1.6;
    height: auto;
    overflow-wrap: break-word;
    word-wrap: break-word;
    white-space: pre-wrap;
}

/* 목록 버튼 */
.back-button {
    background-color: #575757;
    color: white;
    padding: 10px 15px;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    font-size: 16px;
    margin-top: 20px;
}
.black-bar {
    width: 100%;
    height: 2px;
    background-color: #a7a7a7;
    margin: 3px;
}
</style>