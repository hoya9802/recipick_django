<template>
    <div class="category-recipes-container">
        <div class="dish-grid">
            <Dish v-for="dish in dishList" :key="dish.id" :dish="dish" class="dish-item" />
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
        };
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
</style>