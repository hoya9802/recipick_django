<template>
    <div class="my-helps-container">
        <div>
            <img src="@/assets/myhelp.png" class="myhelp">
            <div v-for="help in paginatedMyHelps" :key="help.id" class="help-item">
                <router-link :to="`/helps/${help.id}`" class="help-content">
                    <img v-if="help.image" :src="help.image" alt="Help Image" class="help-image" />
                    <img v-else src="@/assets/default-image.png" alt="Default Image" class="help-image" />
                    <div class="help-info">
                        <h3>{{ help.title }}</h3>
                    </div>
                </router-link>
                <div class="help-actions">
                    <button @click="editHelp(help.id)" class="btn-edit">수정</button>
                    <button @click="deleteHelp(help.id)" class="btn-delete">삭제</button>
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
            helps: [],
            currentPage: 1,
            itemsPerPage: 5,
        };
    },
    computed: {
        paginatedMyHelps() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = this.currentPage * this.itemsPerPage;
            return this.helps.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.helps.length / this.itemsPerPage);
        },
    },
    methods: {
        async fetchHelps() {
            try {
                const response = await apiClient.get("/helps/?all=false");
                console.log(response.data);
                this.helps = response.data.filter(
                    (help) => help.user.id === this.$store.state.id
                );
            } catch (error) {
                console.error("요리 지식인 조회 실패:", error);
            }
        },
        editHelp(helpId) {
            this.$router.push({ name: "MyHelpEdit", params: { id: helpId } });
        },
        async deleteHelp(helpId) {
            const userConfirmed = confirm("정말 이 요리 지식인을 삭제하시겠습니까?");
            if (userConfirmed) {
                try {
                    await apiClient.delete(`/helps/${helpId}/`);
                    this.helps = this.helps.filter((help) => help.id !== helpId);
                    alert("요리 지식인이 성공적으로 삭제되었습니다.");
                } catch (error) {
                    console.error("요리 지식인 삭제 중 오류 발생:", error);
                    alert("요리 지식인 삭제 중 오류가 발생했습니다.");
                }
            } else {
                console.log("요리 지식인 삭제 취소됨.");
            }
        },
    },
    mounted() {
        document.title = "My Post - Recipick"
        this.fetchHelps();
    },
};
</script>

<style scoped>
.my-helps-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}
.myhelp {
    display: block;
    margin: 0 auto 20px;
    width: 100%;
    max-width: 300px;
    height: auto;
}
.help-item {
    display: flex;
    align-items: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 20px;
    padding: 20px;
}
.help-content {
    flex: 1;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 20px;
}
.help-image {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    margin-right: 20px;
}

.help-info {
    flex: 1;
    color: black;
}
.help-info h3 {
    font-size: 28px;
    font-weight: bold;
}
.help-info span {
    font-size: 16px;
    margin: 10px;
}

.help-actions {
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