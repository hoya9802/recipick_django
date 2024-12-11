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
            return !['loginaccount', 'Signup', 'FindId', 'ResetPassword'].includes(this.$route?.name);
        },
    },


}
</script>


<style lang="scss">
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: black;
}
</style>
