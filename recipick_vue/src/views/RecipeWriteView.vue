<template>
    <RecipeWrite></RecipeWrite>
</template>

<script>
import RecipeWrite from '@/components/RecipeWrite.vue';

export default {
    name: "RecipeWriteView",
    components: {
        RecipeWrite : RecipeWrite,
    },
    mounted() {
        document.title = '레시피 업로드 - Recipick'
    },
};
</script>

<style scoped>

</style>