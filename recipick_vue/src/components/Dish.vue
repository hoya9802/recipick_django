<template>
  <div class="dish-item">
    <div class="post-header">
      <div v-if="dish.user.profile_image" class="profile" :style="{ backgroundImage: `url(${dish.user.profile_image})` }"></div>
      <div v-else class="profile"></div>
      <span class="profile-name">{{ dish.user.nick_name }} - {{ dish.user.level }}</span>
    </div>
    <router-link :to="'/recipes/' + dish.id" class="post-link">
      <div class="post-body" :style="{ backgroundImage: `url(${dish.image})` }"></div>
      <div class="post-content">
        <p>{{ dish.name }}</p>
        <p>🧑🏻: {{ dish.likes_count }} 👽: {{ dish.dislikes_count }}</p>
      </div>
    </router-link>
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
.dish-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
}
.post-header {
    display: flex;
    align-items: center;
    padding: 10px;
    width: 100%;
}
.profile {
    background-image: url("@/assets/default-profile.png");
    width: 30px;
    height: 30px;
    background-size: cover;
    background-position: center;
    border-radius: 50%;
    flex-shrink: 0;
}
.profile-name {
    font-size: 14px;
    margin-left: 10px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: black;
}
.post-body {
    width: 100%;
    aspect-ratio: 4 / 3;
    background-size: cover;
    background-position: center;
    border-top: 1px solid #ddd;
}
.post-content {
    padding: 10px;
    text-align: center;
    margin: 10px;
}
.post-content p{
    color: black;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: bold;
    font-size: 17px !important;
    margin: 0;
}
.post-link {
    text-decoration: none;
    color: inherit;
    width: 100%;
}
</style>