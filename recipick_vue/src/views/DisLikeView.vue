<template>
    <div class="dislike-container">
        <img src="@/assets/dislike.png" class="dislike">

        <div class="dislike-grid">
            <router-link v-for="recipe in paginatedRecipes" :key="recipe.id" :to="`/recipes/${recipe.id}`" class="recipe-card">
                <!-- 프로필 이미지와 닉네임 -->
                <div class="profile-container">
                    <img v-if="recipe.user.profile_image" :src="`http://127.0.0.1:8000${recipe.user.profile_image}`"
                        alt="profile image" class="profile-image" />
                    <img v-else src="@/assets/default-profile.png"
                        alt="profile image" class="profile-image" />
                    <span class="profile-name">
                        {{ recipe.user.nick_name }} - {{ recipe.user.level }}
                    </span>
                </div>

                <div class="post-link">
                    <!-- 레시피 이미지 -->
                    <div class="post-body">
                        <img :src="`http://127.0.0.1:8000${recipe.image}`" alt="recipe image" class="recipe-image" />
                    </div>
                    <!-- 레시피 정보 -->
                    <div class="post-content">
                        <p class="recipe-name">{{ recipe.name }}</p>
                        <p class="recipe-count">🧑🏻: {{ recipe.likes_count }} 👽: {{ recipe.dislikes_count }}</p>
                    </div>
                </div>
            </router-link>
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
import { mapState, mapActions } from 'vuex';

export default {
    data() {
        return {
            currentPage: 1,
            itemsPerPage: 12,
        };
    },
    computed: {
        ...mapState(['dislikedRecipes']),
        paginatedRecipes() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = this.currentPage * this.itemsPerPage;
            return this.dislikedRecipes.slice(start, end);
        },

        totalPages() {
            return Math.ceil(this.dislikedRecipes.length / this.itemsPerPage);
        },
    },
    methods: {
        ...mapActions(['fetchDislikedRecipes']),
    },
    mounted() {
        this.fetchDislikedRecipes();
        document.title = "내가 누른 👽 - Recipick"
    },
};
</script>

<style scoped>
.dislike-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: white;
}
.recipe-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
    text-decoration: none;
}
.dislike-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 1200px;
}
.dislike {
    margin: 30px;
}
.profile-container {
    display: flex;
    align-items: center;
    padding: 10px;
    width: 100%;
}
.recipe-card:hover {
    transform: scale(1.02);
}
.profile-image{
    background-image: url("@/assets/default-profile.png");
    width: 30px;
    height: 30px;
    background-size: cover;
    background-position: center;
    border-radius: 50%;
    flex-shrink: 0;
}
.profile-name {
    font-size: 14px;
    margin-left: 10px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: black;
}
.recipe-image {
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
.post-link {
    text-decoration: none;
    color: inherit;
    width: 100%;
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