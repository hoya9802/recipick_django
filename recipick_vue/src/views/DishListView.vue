<template>
<div class="dish-container">
    <div class="dish-grid">
        <div v-for="dish in dishList" :key="dish.id" class="post">
            <Dish :dish="dish"/>
        </div>
    </div>
</div>
</template>

<script>
import apiClient from '@/store/api';
import Dish from '@/components/Dish.vue';

export default {
    name: 'DishListView',
    data() {
        return {
            dishList: [],
        }
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
        }
    },
    components: {
        Dish: Dish,
    }
}
</script>

<style>
.dish-container {
  padding: 20px;
}

.dish-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2vw;
  padding: 2vw;
  max-width: 1200px;
  margin: 0 auto;
}

.post {
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
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