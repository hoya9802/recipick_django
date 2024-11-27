<template>
    <Header v-if="showHeader"></Header>
    <router-view />

</template>

<script>
import Header from '@/components/Header.vue';

export default {
    name: 'App',
    components: {
        Header: Header,
    },
    computed: {
        showHeader() {
            return !['loginaccount', 'Signup'].includes(this.$route?.name);
        },
    },


}
</script>


<style scoped lang="scss">
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}
</style>
