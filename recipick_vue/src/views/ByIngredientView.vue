<template>
    <div>
        <div class="dish-grid">
            <div v-for="dish in dishList" :key="dish.id" class="post">
                <Dish :dish="dish" />
            </div>
        </div>
        <hr>
        <div v-if="labList.length > 0" class="lab-list">
            <div v-for="lab in labList" :key="lab.id" class="lab-card" @click="goToLabDetail(lab.id)">
                <div class="lab-image-container">
                    <img v-if="lab.image" :src="lab.image" alt="Lab" class="lab-image" />
                </div>
                <div class="lab-info">
                    <div class="lab-top">
                        <p class="lab-title">{{ lab.title }}</p>
                        <div class="black-bar"></div>
                    </div>
                    <div class="lab-header">
                        <div class="lab-user">
                            <span class="lab-likes">🔎 : {{ lab.likes_count }}</span>
                            <span>{{ lab.user.nick_name }} - {{ lab.user.level }}</span>
                        </div>
                    </div>
                    <div class="lab-details">
                        <p>사용 재료 : {{ lab.ingredients.map(ingredient => ingredient.name).join(", ") || "재료 없음" }}</p>
                        <p>Update : {{ lab.modify_dt }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import apiClient from '@/store/api';
import Dish from '@/components/Dish.vue';

export default {
    name: 'ByIngredientView',
    data() {
        return {
            dishList: [],
            labList: [],
            ingredientId: null
        }
    },
    mounted() {
        this.ingredientId = this.$route.params.ingredient_id;
        this.getByIngredient(this.ingredientId);
    },
    methods: {
        async getByIngredient(ingredientId) {
            try {
                const dish_response = await apiClient.get(`ingredients/${ingredientId}/recipes/`);
                console.log(dish_response)
                const lab_response = await apiClient.get(`ingredients/${ingredientId}/labs/`);
                console.log(lab_response)
                this.dishList = dish_response.data;
                this.labList = lab_response.data;
                document.title = '결과 - Recipick';
            } catch (error) {
                console.log(error);
            }
        },
    },
    components: {
        Dish: Dish,
    }
}
</script>

<style>
/* 레시피 리스트 */
.dish-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 1200px;
}

.post {
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

</style>