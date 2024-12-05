<template>
  <div class="dish-container">
    <img src="@/assets/recipe.png" class="recipeimage">
    <div class="dish-grid">
      <div v-for="dish in paginatedDishList" :key="dish.id" class="post">
        <Dish :dish="dish" />
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
import apiClient from '@/store/api';
import Dish from '@/components/Dish.vue';

export default {
    name: 'RecipeListView',
    data() {
        return {
            dishList: [],
            currentPage: 1,
            itemsPerPage: 12,
        }
    },
    computed: {
      totalPages() {
        return Math.ceil(this.dishList.length / this.itemsPerPage);
      },
      paginatedDishList() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = this.currentPage * this.itemsPerPage;
        return this.dishList.slice(start, end);
      },
    },
    mounted() {
        this.getDishList()
    },
    methods: {
        async getDishList() {
            try {
                const response = await apiClient.get('/recipes/?all=true')
                this.dishList = response.data;
                document.title = '요리보기 - Recipick';
            } catch (error) {
                console.log(error);
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
    },
    components: {
        Dish: Dish,
    }
}
</script>

<style scoped>
.dish-container {
  /* 추가 */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: white;
}

.dish-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  /* gap: 2vw;
  padding: 2vw;
  max-width: 1200px;
  margin: 0 auto; */
  gap: 20px;
  width: 100%;
  max-width: 1200px;
}

.post {
  /* width: 100%;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden; */
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.post:hover {
    transform: scale(1.02);
}
@media (max-width: 1024px) {
  .dish-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .dish-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .dish-grid {
    grid-template-columns: 1fr;
  }
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