<template>

<div class="logo-image">
  <img src="./assets/recipick1.png">
</div>

<div class="container">
  <!-- 왼쪽 -->
  <div class="left-section">
    <p>왼쪽</p>
  </div>

  <!-- 오른쪽 -->
  <div class="right-section">
    <Login></Login>
  </div>
</div>

</template>

<script>
import Login from './components/Login.vue'
export default{
  name : 'App',
  data(){
    return {

    }
  },
  components: {
    Login,
  }
}
</script>



<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.logo-image {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}
.logo-image img {
  margin-top: 30px;
  max-width: 250px;
  height: auto;
}
/* 컨테이너 스타일 */
.container {
  display: flex;
  width: 100%;
  max-width: 900px;
  min-width: 300px;
  height: 500px;
  margin: 0 auto;
  margin-bottom: 40px;
  background-color: white;
  padding: 20px;
}
/* 왼쪽 */
.left-section {
  flex: 1;
  max-width: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}
/* 오른쪽 */
.right-section {
  flex: 1;
  max-width: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
