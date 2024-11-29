<template>
    <div class="dish-item">
      <router-link :to="'/freemarket/' + market.id">
        <div class="post-header">
          <div class="profile"></div>
            <span class="profile-name">{{ market.user.nick_name }} - </span>
            <span class="profile-name">{{ market.user.level }}</span>
          </div>
        <div class="post-body" :style="{ backgroundImage: `url(${market.image})` }"></div>
        <div class="post-content">
          <p class="text-center fs-6"><strong>{{ market.name }}</strong></p>
          <p class="text-center"><strong>지역명 / {{ market.days_ago }}</strong></p>
          <div class="text-center fs-5">
            <p v-if="market.is_shared === false"><strong>무료 나눔</strong></p>
            <p v-else><strong>나눔 완료</strong></p>
          </div>
        </div>
      </router-link>
    </div>
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
    height: 45px;
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

  .dish-item a {
    text-decoration: none;
    color: black;
  }
  </style>