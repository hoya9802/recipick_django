<template>
    <HelpWrite></HelpWrite>
</template>

<script>
import HelpWrite from '@/components/HelpWrite.vue';

export default {
    name: "HelpWriteView",
    components: {
        HelpWrite : HelpWrite,
    },
    mounted() {
        document.title = '요리 지식인 업로드 - Recipick'
    },
};
</script>

<style scoped>

</style>