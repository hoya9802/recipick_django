<template>
  <div class="market-item">
    <div class="post-header">
      <div v-if="market.user.profile_image" class="profile" :style="{ backgroundImage: `url(${market.user.profile_image})` }"></div>
      <div v-else class="profile"></div>
      <span class="profile-name">{{ market.user.nick_name }} - {{ market.user.level }} </span>
    </div>
  </div>
  <router-link :to="'/freemarket/' + market.id" class="post-link">
    <div class="post-body" :style="{ backgroundImage: `url(${market.image})` }"></div>
    <div class="post-content">
      <p class="text-center fs-6">{{ market.name }}</p>
      <p class="text-center">지역명 / {{ market.days_ago }}</p>
      <div class="text-center fs-5">
        <p v-if="market.is_shared === false">무료 나눔</p>
        <p v-else>나눔 완료</p>
      </div>
    </div>
  </router-link>
</template>

<script>
export default {
  name: 'MarketComponent',
  props: {
    market: {},
  }
}
</script>

<style scoped>
.market-item {
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

.post-content p {
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