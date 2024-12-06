<template>
    <MarketWrite></MarketWrite>
</template>

<script>
import MarketWrite from '@/components/MarketWrite.vue';

export default {
    name: "MarketWriteView",
    components: {
        MarketWrite : MarketWrite,
    },
    mounted() {
        document.title = '요리 실험일지 업로드 - Recipick'
    },
};
</script>

<style scoped>

</style>