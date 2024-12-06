<template>
    <LabsWrite></LabsWrite>
</template>

<script>
import LabsWrite from '@/components/LabsWrite.vue';
export default {
    name: "LabsWriteView",
    components: {
        LabsWrite : LabsWrite,
    },
    mounted() {
        document.title = '요리 실험일지 업로드 - Recipick'
    },
};
</script>

<style scoped>

</style>