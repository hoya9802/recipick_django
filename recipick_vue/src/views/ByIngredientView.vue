<template>
  <p>{{ dishList }}</p>
  <p>{{ labList }}</p>
</template>

<script>
import apiClient from '@/store/api';

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
                const dish_response = await apiClient.get(`/ingredients/${ingredientId}/recipes/`);
                const lab_response = await apiClient.get(`/ingredients/${ingredientId}/labs/`);
                this.dishList = dish_response.data;
                this.labList = lab_response.data;
                document.title = '결과 - Recipick';
            } catch (error) {
                console.log(error);
            }
        },
    }
}
</script>

<style>

</style>