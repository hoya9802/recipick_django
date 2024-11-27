<template>
  <div class="dish-item">
    <div class="post-header">
      <div class="profile"></div>
        <span class="profile-name">{{ dish.user.nick_name }} - </span>
        <span class="profile-name" v-if="dish.user.level">{{ dish.user.level }}</span>
        <span class="profile-name" v-else>초보 요리사</span>
      </div>
    <div class="post-body" :style="{ backgroundImage: `url(${dish.image})` }"></div>
    <div class="post-content">
      <p><strong>{{ dish.name }}</strong></p>
      <p>{{ dish.likes_count }} Likes {{ dish.dislikes_count }} NGs</p>
    </div>
  </div>
</template>

<script>
export default {
    name: 'DishComponent',
    props: {
        dish: {},
    }
}
</script>

<style scoped>
.profile {
  background-image: url("https://picsum.photos/100?random=0");
  width: 30px;
  height: 30px;
  background-size: 100%;
  border-radius: 50%;
  float: left;
}

.profile-name {
  display: block;
  float: left;
  padding-left: 10px;
  padding-top: 7px;
  font-size: 14px;
}

.post-header {
  height: 30px;
  padding: 10px;
}

.post-body {
  height: 150px;
  background-position: center;
  background-size: cover;
}

.post-content {
  padding-left: 15px;
  padding-right: 15px;
  font-size: 14px;
}
</style>