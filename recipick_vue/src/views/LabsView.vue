<template>
    <div class="lab-container">
        <div v-if="labs.length > 0" class="lab-list">
            <div v-for="lab in labs" :key="lab.id" class="lab-card" @click="goToLabDetail(lab.id)">
                <div class="lab-image-container">
                    <img v-if="lab.image" :src="lab.image" alt="Lab" class="lab-image" />
                </div>
                <div class="lab-info">
                    <div class="lab-top">
                        <p class="lab-title">{{ lab.title }}</p>
                        <div class="black-bar"></div>
                    </div>
                    <div class="lab-header">
                        <div class="lab-user">
                            <span class="lab-likes">🔎 : {{ lab.likes_count }}</span>
                            <span>{{ lab.user.nick_name }} - {{ lab.user.level }}</span>
                        </div>
                    </div>
                    <div class="lab-details">
                        <p>사용 재료 : {{ lab.ingredients.map(ingredient => ingredient.name).join(", ") }}</p>
                        <p>Update : {{ lab.modify_dt }}</p>
                    </div>
                </div>
            </div>
        </div>
        <p v-else>실험 일지가 없습니다.</p>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    name: 'LabList',
    data() {
        return {
            labs: [],
        };
    },
    mounted() {
        document.title = '요리 실험 일지 - Recipick'
    },
    created() {
        this.fetchAllLabs();
    },
    methods: {
        async fetchAllLabs() {
            try {
                const response = await apiClient.get('/labs/?all=true');
                this.labs = response.data;
            } catch (error) {
                console.error('요리 실험 일지를 가져오는 중 오류 발생:', error);
                alert('실험 일지를 불러오지 못했습니다.');
            }
        },
        goToLabDetail(lab_id) {
            this.$router.push(`/labs/${lab_id}`);
        },
    },
};
</script>

<style scoped>
.lab-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px;
}
.lab-list {
    display: flex;
    flex-direction: column;
    gap: 30px;
    align-items: center;
}
.lab-card {
    display: flex;
    width: 900px;
    max-width: 100%;
    justify-content: center;
    align-items: center;
    border: 1px solid #d6d6d6;
    overflow: hidden;
    transition: transform 0.2s ease-in-out;
    cursor: pointer;
}
.lab-card:hover {
    transform: scale(1.02);
}
.lab-image-container {
    flex: 0 0 250px;
    height: 250px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-right: 1px solid #d6d6d6;
}
.lab-image {
    margin-left: 20px;
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.lab-top {
    width: 100%;
    height: 50px;
    margin-top: 10px;
    margin-bottom: 0;
}
.lab-title {
    font-weight: bold;
    margin: 0;
    font-size: 27px;
    color: black;
}
.lab-info {
    flex: 1;
    padding: 15px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 20px;
}

.lab-header {
    height: 100px;
    font-size: 17px;
    margin-bottom: 3px 0;
    display: flex;
    justify-content: flex-end;
}
.lab-user {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    font-size: 18px;
}
.lab-likes {
    margin-left: 8px;
    justify-content: flex-start;
}
.lab-details p {
    margin: 5px 0;
    font-size: 16px;
    display: flex;
    justify-content: flex-end;
}
.black-bar {
    width: 100%;
    height: 2px;
    background-color: #a7a7a7;
    margin: 3px 0;
}

</style>