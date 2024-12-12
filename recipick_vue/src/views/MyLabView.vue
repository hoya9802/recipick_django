<template>
    <div class="my-labs-container">
        <div>
            <img src="@/assets/mylab.png" class="mylab">
            <div v-for="lab in paginatedMyLabs" :key="lab.id" class="lab-item">
                <router-link :to="`/labs/${lab.id}`" class="lab-content">
                    <img v-if="lab.image" :src="lab.image" alt="Lab Image" class="lab-image" />
                    <div class="lab-info">
                        <h3>{{ lab.title }}</h3>
                        <span>🔎: {{ lab.likes_count }}</span>
                    </div>
                </router-link>
                <div class="lab-actions">
                    <button @click="editLab(lab.id)" class="btn-edit">수정</button>
                    <button @click="deleteLab(lab.id)" class="btn-delete">삭제</button>
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
            labs: [],
            currentPage: 1,
            itemsPerPage: 5,
        };
    },
    computed: {
        paginatedMyLabs() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = this.currentPage * this.itemsPerPage;
            return this.labs.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.labs.length / this.itemsPerPage);
        },
    },
    methods: {
        async fetchLabs() {
            try {
                const response = await apiClient.get("/labs/?all=false");
                console.log(response.data);
                this.labs = response.data.filter(
                    (lab) => lab.user.id === this.$store.state.id
                );
            } catch (error) {
                console.error("실험일지 조회 실패:", error);
            }
        },
        editLab(labId) {
            this.$router.push({ name: "MyLabEdit", params: { id: labId } });
        },
        async deleteLab(labId) {
            const userConfirmed = confirm("정말 이 실험일지를 삭제하시겠습니까?");
            if (userConfirmed) {
                try {
                    await apiClient.delete(`/labs/${labId}/`);
                    this.labs = this.labs.filter((lab) => lab.id !== labId);
                    alert("실험일지가 성공적으로 삭제되었습니다.");
                } catch (error) {
                    console.error("실험일지 삭제 중 오류 발생:", error);
                    alert("실험일지 삭제 중 오류가 발생했습니다.");
                }
            } else {
                console.log("실험일지 삭제 취소됨.");
            }
        },
    },
    mounted() {
        document.title = "My Post - Recipick"
        this.fetchLabs();
    },
};
</script>

<style scoped>
.my-labs-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}
.mylab {
    display: block;
    margin: 0 auto 20px;
    width: 100%;
    max-width: 300px;
    height: auto;
}
.lab-item {
    display: flex;
    align-items: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 20px;
    padding: 20px;
}
.lab-content {
    flex: 1;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 20px;
}
.lab-image {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    margin-right: 20px;
}

.lab-info {
    flex: 1;
    color: black;
}
.lab-info h3 {
    font-size: 28px;
    font-weight: bold;
}
.lab-info span {
    font-size: 16px;
    margin: 10px;
}

.lab-actions {
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