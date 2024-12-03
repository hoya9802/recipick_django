<template>
    <div class="lab-detail-page">
        <header v-if="lab" class="lab-detail-header">
            <h1>{{ lab.title }}</h1>
            <div class="lab-meta">
                <span>{{ lab.user?.nick_name || "Unknown" }} - {{ lab.user?.level || "Unknown Level" }}</span>
                <span>🔎 : {{ lab.likes_count || 0 }}</span>
                <span>Update: {{ lab.modify_dt || "N/A" }}</span>
            </div>
        </header>

        <div v-if="lab">
            <!-- 이미지 섹션 -->
            <div class="lab-image-container">
                <img v-if="lab.image" :src="lab.image" alt="Lab" class="lab-image" />
            </div>

            <!-- 재료 및 설명 섹션 -->
            <section class="lab-content-section">
                <p class="lab-content-title">Ingredients</p>
                <div class="black-bar"></div>
                <p class="content">{{ lab.ingredients?.map(ingredient => ingredient.name).join(", ") || "재료없음" }}</p>
                <div class="lab-description">
                    <p class="lab-content-title">Description</p>
                    <div class="black-bar"></div>
                    <p class="content" v-html="lab.description || 'No description available.'"></p>
                </div>
            </section>

            <button @click="goBack" class="back-btn">목록</button>
        </div>

        <div v-else>
            <p>데이터를 불러오는 중입니다...</p>
        </div>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    name: "LabDetailPage",
    data() {
        return {
            lab: null,
        };
    },
    async created() {
        const lab_id = this.$route.params.lab_id;
        await this.fetchLabDetail(lab_id);
    },
    watch: {
        lab(newLab) {
            if (newLab && newLab.title) {
                document.title = `${newLab.title} - Recipick`;
            }
        },
    },
    methods: {
        async fetchLabDetail(lab_id) {
            try {
                const response = await apiClient.get(`/labs/${lab_id}/`);
                this.lab = response.data;
            } catch (error) {
                console.error("실험일지 상세 정보를 가져오는 중 오류 발생:", error);
                alert("실험일지 상세 정보를 불러오지 못했습니다.");
            }
        },
        goBack() {
            this.$router.push("/labs");
        },
    },
};
</script>
<style scoped>
.lab-detail-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 30px;
    background-color: #fafafa;
}
.lab-detail-header {
    text-align: center;
    margin-bottom: 20px;
}
.lab-detail-header h1 {
    font-size: 40px;
    font-weight: bold;
    color: black;
    margin-bottom: 30px;
}

.lab-meta {
    display: flex;
    justify-content: center;
    gap: 60px;
    font-size: 16px;
    color: #555;
    margin-bottom: 20px;
    font-size: 17px;
}

.lab-image-container {
    width: 100%;
    max-width: 900px;
    margin-bottom: 40px;
    text-align: center;
}

.lab-image {
    width: 100%;
    height: auto;
    object-fit: contain;
    border: 1px solid #ddd;
}

.lab-content-section {
    width: 100%;
    max-width: 900px;
    font-size: 16px;
    line-height: 1.5;
    color: #333;
    margin-bottom: 20px;
}
.lab-content-section p {
    margin: 10px 0;
}
.lab-content-title{
    font-size: 23px;
    font-weight: bold;
    color: black;
    text-align: left;
}
.content {
    color: black;
    font-size: 20px;
}
.lab-description {
    margin-top: 20px;
}
.black-bar {
    width: 100%;
    height: 2px;
    background-color: #a7a7a7;
    margin: 10px 0;
}
.back-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #575757;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>
