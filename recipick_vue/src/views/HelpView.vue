<template>
    <div class="help-container">
        <img src="@/assets/help.png" class="helpimage">

        <!-- 글쓰기 버튼 -->
        <div class="write-post-button">
            <button class="post-button" @click="goToWritePage">업로드 하기</button>
        </div>

        <!-- 요리지식인 -->
        <div class="help-grid">
            <div v-for="help in paginatedHelps" :key="help.id" class="help-card" @click="goToHelpDetail(help.id)">
                <HelpBox :help="help" />
            </div>
        </div>

        <!-- 페이지네이션 -->
        <div class="pagination">
            <button :disabled="currentPage === 1" @click="goToPreviousPage">이전</button>
            <span>{{ currentPage }} / {{ totalPages }}</span>
            <button :disabled="currentPage === totalPages" @click="goToNextPage">다음</button>
        </div>
    </div>
</template>

<script>
import apiClient from "@/store/api";
import HelpBox from "@/components/HelpBox.vue"
import defaultImage from "@/assets/default-image.png";

export default {
    name: "Helps",
    data() {
        return {
            helps: [],
            currentPage: 1,
            itemsPerPage: 12,
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.helps.length / this.itemsPerPage);
        },
        paginatedHelps() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = this.currentPage * this.itemsPerPage;
            return this.helps.slice(start, end);
        },
    },
    created() {
        this.fetchHelps();
    },
    methods: {
        async fetchHelps() {
            try {
                const response = await apiClient.get("/helps/?all=true");
                this.helps = response.data.map((help) => ({
                    ...help,
                    image: help.image || defaultImage,
                }));
                document.title = '요리 지식인 - Recipick';
            } catch (error) {
                console.error("지식인 글을 불러오는 중 오류 발생:", error);
                alert("지식인 글을 불러오지 못했습니다.");
            }
        },
        goToPreviousPage() {
            if (this.currentPage > 1) {
                this.currentPage -= 1;
            }
        },
        goToNextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage += 1;
            }
        },
        goToHelpDetail(id) {
            this.$router.push(`/help/${id}`);
        },
        goToWritePage() {
            this.$router.push("/help/write");
        }
    },
    components: {
        HelpBox: HelpBox,
    }
};
</script>

<style scoped>
.help-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: white;
}

/* 업로드하기 버튼 */
.write-post-button {
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: flex-end;
  margin: 10px 30px;
  position: relative;
}
.post-button {
  margin: 8px;
  padding: 4px;
  width: 120px;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  border: 2px solid #bbbbbb;
  border-radius: 50px;
  background-color: white;
  color: #5a5a5a;
}

/* 요리지식인 */
.help-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    width: 100%;
    max-width: 1200px;
}

.help-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.2s ease;
}
.help-card:hover {
    transform: scale(1.02);
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