<template>
    <div class="my-recipes-container">
        <div>
            <img src="@/assets/myrecipe.png" class="myrecipe">
            <div v-for="recipe in paginatedMyRecipes" :key="recipe.id" class="recipe-item">
                <router-link :to="`/recipes/${recipe.id}`" class="recipe-content">
                    <img v-if="recipe.image" :src="recipe.image" alt="Recipe Image" class="recipe-image" />
                    <div class="recipe-info">
                        <h3>{{ recipe.name }}</h3>
                        <span>🧑🏻: {{ recipe.likes_count }}</span>
                        <span>👽: {{ recipe.dislikes_count }}</span>
                    </div>
                </router-link>

                <div class="recipe-actions">
                    <button @click="editRecipe(recipe.id)" class="btn-edit">수정</button>
                    <button @click="deleteRecipe(recipe.id)" class="btn-delete">삭제</button>
                </div>
            </div>
        </div>

        <!-- 페이지네이션 버튼 -->
        <div class="pagination">
            <button :disabled="currentPage === 1" @click="currentPage--">
                이전
            </button>
            <span>{{ currentPage }} / {{ totalPages }}</span>
            <button :disabled="currentPage === totalPages" @click="currentPage++">
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
            recipes: [],
            currentPage: 1,
            itemsPerPage: 5,
        };
    },
    computed: {
        paginatedMyRecipes() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = this.currentPage * this.itemsPerPage;
            return this.recipes.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.recipes.length / this.itemsPerPage);
        },
    },
    methods: {
        async fetchRecipes() {
            try {
                const response = await apiClient.get("/recipes/?all=false");
                console.log(response.data);
                this.recipes = response.data.filter(
                    (recipe) => recipe.user.id === this.$store.state.id
                );
            } catch (error) {
                console.error("레시피 조회 실패:", error);
            }
        },
        editRecipe(recipeId) {
            this.$router.push({ name: "MyRecipeEdit", params: { id: recipeId } });
        },
        async deleteRecipe(recipeId) {
            const userConfirmed = confirm("정말 이 레시피를 삭제하시겠습니까?");
            if (userConfirmed) {
                try {
                    await apiClient.delete(`/recipes/${recipeId}/`);
                    this.recipes = this.recipes.filter((recipe) => recipe.id !== recipeId);
                    alert("레시피가 성공적으로 삭제되었습니다.");
                } catch (error) {
                    console.error("레시피 삭제 중 오류 발생:", error);
                    alert("레시피 삭제 중 오류가 발생했습니다.");
                }
            } else {
                console.log("레시피 삭제 취소됨.");
            }
        },
    },
    mounted() {
        document.title = "My Post - Recipick"
        this.fetchRecipes();
    },
};
</script>

<style scoped>
.my-recipes-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}
.myrecipe {
    display: block;
    margin: 0 auto 20px;
    width: 100%;
    max-width: 330px;
    height: auto;
}
.recipe-item {
    display: flex;
    align-items: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 20px;
    padding: 20px;
}
.recipe-image {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    margin-right: 20px;
}
.recipe-content {
    flex: 1;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 20px;
}
.recipe-info {
    flex: 1;
    color: black;
}
.recipe-info h3 {
    font-size: 28px;
    font-weight: bold;
}
.recipe-info span {
    font-size: 16px;
    margin: 10px;
}

.recipe-actions {
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