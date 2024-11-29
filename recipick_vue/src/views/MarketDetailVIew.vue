<template>

  <body>
    <div v-if="market" class="dish-detail mb-5">
      <div class="row">
        <div class="col-md-8">
          <figure class="mb-4 dish-image">
            <img v-bind:src="market.image" class="img-fluid">
          </figure>
        </div>
        <div class="col-md-4">
          <ProfileHeader :user="market.user" />
          <h1 class="title"><strong>{{ market.name }}</strong></h1>

          <h2 class="subtitle">Information</h2>
          <p><strong>{{ market.count }} 개</strong></p>
          <p><strong>획득일자: {{ market.purchase_dt }}</strong></p>
          <p><strong>업로드: {{ market.days_ago }}</strong></p>
          <p v-if="!market.is_shared"><strong>상태: 무료나눔중</strong></p>
          <p v-else><strong>상태: 나눔완료</strong></p>
          <div class="mt-4">
            <button v-if="isAuthor && !market.is_shared" @click="handleComplete"
              class="btn btn-warning me-2">나눔완료</button>
            <button v-if="isAuthor && !market.is_shared" @click="handleEdit" class="btn btn-primary me-2">수정하기</button>
            <button v-if="isAuthor" @click="handleDelete" class="btn btn-danger">삭제하기</button>
            <button v-if="!isAuthor && !market.is_shared" @click="handleContact" class="btn btn-success">연락하기</button>
          </div>
        </div>
      </div>
      <div>
        <h2 class="subtitle">Description</h2>
        {{ market.description }}
        <div class="toast-container position-fixed bottom-0 end-0 p-3">
          <div class="toast align-items-center text-white border-0" :class="toastClass" role="alert"
            aria-live="assertive" aria-atomic="true" ref="toast">
            <div class="d-flex">
              <div class="toast-body">
                {{ toastMessage }}
              </div>
              <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"
                aria-label="Close"></button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
import apiClient from '@/store/api';
import ProfileHeader from '@/components/ProfileHeader.vue';

export default {
  name: "MarketDetailView",
  data() {
    return {
      market: null,
      currentUser: null,
    }
  },
  computed: {
    isAuthor() {
      return this.currentUser && this.market && this.currentUser.nick_name === this.market.user.nick_name;
    }
  },
  methods: {
    async fetchMarketData() {
      try {
        const response = await apiClient.get(`/freemarkets/${this.$route.params.market_id}/`);
        this.market = response.data;
        document.title = `${this.market.name} - Recipick`;
      } catch (error) {
        console.error('데이터를 불러오는데 실패했습니다:', error);
      }
    },
    async getCurrentUser() {
      try {
        const response = await apiClient.get('/user/mypage/me/');
        this.currentUser = response.data;
      } catch (error) {
        console.error('사용자 정보를 불러오는데 실패했습니다:', error);
      }
    },
    async handleComplete() {
      if (confirm('판매완료 처리하시겠습니까? 이후에 수정은 불가합니다.')) {
        try {
          await apiClient.patch(`/freemarkets/${this.market.id}/`, {
            is_shared: true
          });
          this.market.is_shared = true;
        } catch (error) {
          console.error('판매완료 처리에 실패했습니다:', error);
        }
      }
    },
    handleEdit() {
      this.$router.push(`/market/${this.market.id}/edit`);
    },
    async handleDelete() {
      if (confirm('정말로 삭제하시겠습니까?')) {
        try {
          await apiClient.delete(`/freemarkets/${this.market.id}/`);

          this.$router.push('/market');
        } catch (error) {
          this.showToast('삭제에 실패했습니다.', 'error');
        }
      }
    },
    handleContact() {
      window.location.href = `mailto:${this.market.user_email}`;
    }
  },
  created() {
    this.fetchMarketData();
    this.getCurrentUser();
  },
  components: {
    ProfileHeader: ProfileHeader,
  }
}
</script>

<style scoped>
.dish-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.dish-image {
  margin: 0;
}

.dish-image img {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.dish-info {
  margin-top: 20px;
}

h2 {
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 8px;
}

.btn {
  padding: 8px 16px;
  font-size: 14px;
}
</style>