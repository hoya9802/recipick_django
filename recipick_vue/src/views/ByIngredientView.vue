<template>
    <div>
        <div class="dish-container">
            <div class="dish-grid">
                <div v-for="dish in dishList" :key="dish.id" class="post">
                    <Dish :dish="dish" />
                </div>
            </div>
        </div>
        <hr>
        <div class="lab-container">
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
        goToLabDetail(lab_id) {
            this.$router.push(`/labs/${lab_id}`);
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
.lab-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}
.lab-list {
    display: flex;
    flex-direction: column;
    gap: 30px;
    align-items: center;
}
.lab-card {
    display: flex;
    width: 900px;
    max-width: 100%;
    justify-content: center;
    align-items: center;
    border: 1px solid #d6d6d6;
    overflow: hidden;
    transition: transform 0.2s ease-in-out;
    cursor: pointer;
}
.lab-image-container {
    flex: 0 0 250px;
    height: 250px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-right: 1px solid #d6d6d6;
}
.lab-image {
    margin-left: 20px;
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.lab-info {
    flex: 1;
    padding: 15px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 20px;
}
.lab-top {
    width: 100%;
    height: 50px;
    margin-top: 10px;
    margin-bottom: 0;
}
.lab-title {
    font-weight: bold;
    margin: 0;
    font-size: 27px;
    color: black;
}
.black-bar {
    width: 100%;
    height: 2px;
    background-color: #a7a7a7;
    margin: 3px 0;
}
.lab-header {
    height: 100px;
    font-size: 17px;
    margin-bottom: 3px 0;
    display: flex;
    justify-content: flex-end;
}
.lab-user {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    font-size: 18px;
}
.lab-likes {
    margin-left: 8px;
    justify-content: flex-start;
}
.lab-details p {
    margin: 5px 0;
    font-size: 16px;
    display: flex;
    justify-content: flex-end;
}
.dish-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: white;
}
</style>