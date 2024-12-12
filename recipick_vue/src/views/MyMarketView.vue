<template>
    <div class="my-freemarkets-container">
        <div>
            <img src="@/assets/mymarket.png" class="mymarket">
            <div v-for="freemarket in paginatedMyfreemarkets" :key="freemarket.id" class="freemarket-item">
                <router-link :to="`/freemarkets/${freemarket.id}`" class="freemarket-content">
                    <img v-if="freemarket.image" :src="freemarket.image" alt="freemarket Image" class="freemarket-image" />
                    <div class="freemarket-info">
                        <h3>{{ freemarket.name }}</h3>
                    </div>
                </router-link>
                <div class="freemarket-actions">
                    <button @click="editfreemarket(freemarket.id)" class="btn-edit">수정</button>
                    <button @click="deletefreemarket(freemarket.id)" class="btn-delete">삭제</button>
                </div>
            </div>
        </div>

        <!-- 페이지네이션 버튼 -->
        <div class="pagination">
            <button
                :disabled="currentPage === 1"
                @click="currentPage--"
            >
                이전
            </button>
            <span>{{ currentPage }} / {{ totalPages }}</span>
            <button
                :disabled="currentPage === totalPages"
                @click="currentPage++"
            >
                다음
            </button>
        </div>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    data() {
        return {
            freemarkets: [],
            currentPage: 1,
            itemsPerPage: 5,
        };
    },
    computed: {
        paginatedMyfreemarkets() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = this.currentPage * this.itemsPerPage;
            return this.freemarkets.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.freemarkets.length / this.itemsPerPage);
        },
    },
    methods: {
        async fetchFreemarkets() {
            try {
                const response = await apiClient.get("/freemarkets/?all=false");
                console.log(response.data);
                this.freemarkets = response.data.filter(
                    (freemarket) => freemarket.user.id === this.$store.state.id
                );
            } catch (error) {
                console.error("재료 무료 나눔 조회 실패:", error);
            }
        },
        editfreemarket(freemarketId) {
            this.$router.push({ name: "MyMarketEdit", params: { id: freemarketId } });
        },
        async deletefreemarket(freemarketId) {
            const userConfirmed = confirm("정말 이 재료 무료 나눔을 삭제하시겠습니까?");
            if (userConfirmed) {
                try {
                    await apiClient.delete(`/freemarkets/${freemarketId}/`);
                    this.freemarkets = this.freemarkets.filter((freemarket) => freemarket.id !== freemarketId);
                    alert("재료 무료 나눔이 성공적으로 삭제되었습니다.");
                } catch (error) {
                    console.error("재료 무료 나눔 삭제 중 오류 발생:", error);
                    alert("재료 무료 나눔 삭제 중 오류가 발생했습니다.");
                }
            } else {
                console.log("재료 무료 나눔 삭제 취소됨.");
            }
        },
    },
    mounted() {
        document.title = "My Post - Recipick"
        this.fetchFreemarkets();
    },
};
</script>

<style scoped>
.my-freemarkets-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}
.myfreemarket {
    display: block;
    margin: 0 auto 20px;
    width: 100%;
    max-width: 300px;
    height: auto;
}
.freemarket-item {
    display: flex;
    align-items: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 20px;
    padding: 20px;
}
.freemarket-content {
    flex: 1;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 20px;
}
.freemarket-image {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    margin-right: 20px;
}

.freemarket-info {
    flex: 1;
    color: black;
}
.freemarket-info h3 {
    font-size: 28px;
    font-weight: bold;
}
.freemarket-info span {
    font-size: 16px;
    margin: 10px;
}

.freemarket-actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.btn-edit {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
}

.btn-delete {
    background-color: #f44336;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
}

/* 페이지네이션 */
.pagination {
    margin: 50px;
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
</style>