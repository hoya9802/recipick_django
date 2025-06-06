<template>
    <div class="category-recipes-container">
        <img src="@/assets/category.png" class="categoryimage">
        <div class="dish-grid">
            <Dish v-for="dish in paginatedDishList" :key="dish.id" :dish="dish" class="dish-item" />
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
import Dish from "@/components/Dish.vue";
import apiClient from "@/store/api";

export default {
    name: "CategoryRecipesView",
    props: {
        category_id: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            dishList: [],
            currentPage: 1,
            itemsPerPage: 12,
        };
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
        document.title= '카테고리 - Recipick'
        this.getDishList(this.category_id);
    },
    methods: {
        async getDishList(category_id) {
            try {
                const response = await apiClient.get(`/categories/${category_id}/recipes/`);
                this.dishList = response.data;
            } catch (error) {
                console.error("Failed to fetch recipes:", error);
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
        Dish,
    },
    watch: {
        category_id: {
            immediate: true,
            handler(newCategoryId) {
                this.getDishList(newCategoryId);
            },
        },
    },

};
</script>

<style scoped>
.category-recipes-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}
.no-recipes {
    text-align: center;
    font-size: 16px;
    color: #999;
}
.dish-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    padding: 20px 0;
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