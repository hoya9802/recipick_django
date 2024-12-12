<template>
  <div v-if="market" class="dish-detail mb-5">
    <div class="row">
      <div class="col-md-8">
        <figure class="mb-4 dish-image">
          <img v-bind:src="market.image" class="img-fluid">
        </figure>
      </div>
      <div class="col-md-4">
        <ProfileHeader :user="market.user" />
        <h1 class="title">{{ market.name }}</h1>

        <h2 class="subtitle">Information</h2>
        <div class="black-bar"></div>

        <div class="count-share">
          <span>🛒 {{ market.count }}개</span>
          <span v-if="!market.is_shared">🚨 무료나눔중</span>
          <span v-else>상태: 나눔완료</span>
        </div>

        <div class="black-bar"></div>
        <div class="purchase">
          <span class="purchase-title">획득일자</span>
          <span> {{ market.purchase_dt }}</span>
        </div>

        <div class="black-bar"></div>
        <div class="date">
          <span class="date-title">업로드</span>
          <span>{{ market.days_ago }}</span>
        </div>

        <div class="mt-4">
          <button v-if="isAuthor && !market.is_shared" @click="handleComplete"
            class="btn btn-warning me-2">나눔완료</button>
          <button v-if="isAuthor && !market.is_shared" @click="handleEdit" class="btn btn-primary me-2">수정하기</button>
          <button v-if="isAuthor" @click="handleDelete" class="btn btn-danger">삭제하기</button>
          <button v-if="!isAuthor && !market.is_shared" @click="handleContact" class="btn btn-success">채팅하기</button>
        </div>
      </div>
    </div>

    <div class="description-section">
      <h2 class="subtitle">Description</h2>
      <div class="black-bar"></div>
      <p v-html="formatDescription(market.description)"></p>
      <div class="toast-container position-fixed bottom-0 end-0 p-3">
        <div class="toast align-items-center text-white border-0" :class="toastClass" role="alert" aria-live="assertive"
          aria-atomic="true" ref="toast">
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

    <div class="back-section">
      <button class="back-button" @click="goBack">
        목록
      </button>
    </div>
    <div class="report-section">
      <button class="report-button" @click="confirmReport">
        신고하기
      </button>
    </div>

    <!-- 신고하기 모달 -->
    <div v-if="showReportModal" class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title">신고하기</h5>
          </div>

          <div class="modal-body">
            <p>신고 이유를 자세히 작성해주세요.</p>
            <textarea v-model="reportDetail" rows="4" class="form-control"></textarea>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeReportModal">닫기</button>
            <button type="button" class="btn btn-primary" @click="submitReport">제출</button>
          </div>

        </div>
      </div>
    </div>
  </div>
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
      showReportModal: false,
      reportDetail: '',
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
      this.$router.push({
        name: 'ChatRoom',
        query: {
          shop_user_id: this.market.user.id,
          visitor_user_id: this.currentUser.id,
          current_user: this.currentUser.id,
        }
      });
    },
    formatDescription(description) {
    // 줄바꿈 문자를 <br> 태그로 변환
    return description.replace(/\n/g, '<br>');
    },
    goBack() {
    this.$router.push("/freemarket")
    },
    confirmReport() {
      if (confirm("신고하기를 누르면 수정 및 삭제가 불가능합니다. 계속 진행하시겠습니까?")) {
        this.showReportModal = true;
      }
    },
    closeReportModal() {
      this.showReportModal = false;
      this.reportDetail = '';
    },
    async submitReport() {
      try {
        const payload = {
          url: window.location.href,
          detail: this.reportDetail,
          reported_user: this.market.user.id,
        };
        console.log(payload);
        await apiClient.post('/report/report/', payload);
        alert('신고가 접수되었습니다.');
        this.closeReportModal();
      } catch (error) {
        console.error('신고 제출 중 오류:', error);
        alert('신고 제출에 오류가 발생했습니다.');
      }
    },
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
  margin: 40px auto;
  padding: 20px;
}
.dish-image img {
  width: 80%;
  height: auto;
  display: block;
  margin: 0 auto;
  border-radius: 8px;
}
.col-md-4 {
  border: 1px solid #d6d6d6;
  border-radius: 8px;
  margin-bottom: 30px;
  padding: 20px;
  position: relative;
}
.title {
  font-size: 33px;
  text-align: center;
  margin: 40px 0px;
}
.subtitle {
  margin: 10px 0px;
  text-align: left;
  font-weight: bold;
  font-size: 23px;
}
.count-share {
  margin: 20px;
  gap: 30px;
  display: flex;
  justify-content: center;
  font-size: 20px;
}
.purchase,
.date {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 7px;
}
.purchase-title,
.date-title {
  text-align: left;
  font-size: 21px;
  font-weight: bold;
  color: #505050;
}
.purchase span:last-child,
.date span:last-child {
  text-align: right;
  font-size: 18px;
}

/* 나눔여부 버튼 */
.mt-4 {
  display: flex;
  justify-content: center;
  margin: 30px 2px;
  gap: 20px;
}
.mt-4 button {
  font-size: 16px;
}

/* 설명 */
.description-section {
  margin: 20px auto;
  border: 1px solid #d6d6d6;
  border-radius: 8px;
  padding: 20px;
  max-width: 1200px;
  text-align: center;
}
.description-section p{
  padding: 10px;
  text-align: left;
  font-size: 20px;
}

/* 블랙바 */
.black-bar {
  width: 100%;
  height: 2px;
  background-color: #a7a7a7;
  margin: 10px 0;
}
/* 목록, 신고하기 버튼 */
.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}
.back-section {
  flex: 1;
  text-align: center;
}
.back-button {
  display: block;
  margin: auto;
  padding: 10px 20px;
  background-color: #575757;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.report-section {
  text-align: right;
}
.report-button {
  background-color: white;
  color: black;
  border: 1px solid #d6d6d6;
  padding: 10px 15px;
  font-size: 14px;
  border-radius: 7px;
  cursor: pointer;
}

/* 신고하기 모달 */
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1050;
}
.modal-dialog {
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
}
.modal-content {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  padding: 20px;
  border-radius: 10px;
}
.modal-header,
.modal-footer {
  padding: 1rem;
}
.modal-body {
  padding: 1rem;
}
.modal-footer {
  display: flex;
  justify-content: center;
  gap: 20px;
}
.modal-footer .btn-secondary,
.modal-footer .btn-primary {
  color: white;
  border: none;
  width: 60px;
  padding: 5px;
  border-radius: 5px;
  font-size: 16px;
}

.modal-footer .btn-secondary {
  background-color: #868686;
}

.modal-footer .btn-primary {
  background-color: #030303;
}
</style>