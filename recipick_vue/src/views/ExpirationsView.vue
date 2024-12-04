<template>
    <div class="expiration-list">
        <img src="@/assets/expiration.png" class="expirationimage">
        <div class="expiration-grid">
            <div v-for="item in paginatedExpirations" :key="item.id" class="expiration-item" @click="goToDetail(item.id)">
                <div class="post-body" :style="{ backgroundImage: `url(${item.image})` }"></div>
                <div class="post-content">
                    <p class="expiration-title">{{ item.title }}</p>
                </div>

            </div>
        </div>
        <div class="pagination">
            <button @click="prevPage" :disabled="currentPage === 1">이전</button>
            <span>{{ currentPage }} / {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
        </div>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    name: "Expirations",
    data() {
        return {
            expirations: [],
            currentPage: 1,
            itemsPerPage: 12,
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.expirations.length / this.itemsPerPage);
        },
        paginatedExpirations() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = this.currentPage * this.itemsPerPage;
            return this.expirations.slice(start, end);
        },
    },
    methods: {
        async fetchExpirations() {
            try {
                const response = await apiClient.get("/expirations/");
                this.expirations = response.data;
            } catch (error) {
                console.error("유통기한 데이터를 가져오는 중 오류가 발생했습니다.", error);
            }
        },
        goToDetail(id) {
            this.$router.push({ name: "ExpirationsDetail", params: { id } });
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
    },
    mounted() {
        document.title = "유통기한 알림 - Recipick"
        this.fetchExpirations();
    },
};
</script>

<style scoped>
.expiration-list {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: white;
}
.expiration-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    width: 100%;
    max-width: 1200px;
}
.expiration-item {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.2s ease;
}
.expiration-item:hover {
    transform: scale(1.02);
}
.post-body {
    width: 100%;
    aspect-ratio: 4 / 3;
    background-size: cover;
    background-position: center;
    border-top: 1px solid #ddd;
}
.post-content {
    padding: 10px;
    text-align: center;
    margin: 10px;
}
.post-content p{
    color: black;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: bold;
    font-size: 17px !important;
    margin: 0;
}

/* 페이지네이션 */
.pagination {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
}

.pagination button {
    padding: 5px 10px;
    background-color: #575757;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.pagination button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.pagination span {
    font-size: 16px;
}
</style>