<template>
  <div v-if="dish" class="dish-detail mb-5">
    <div class="row">
      <div class="col-md-8">
        <figure class="mb-4 dish-image">
          <img v-bind:src="dish.image" class="img-fluid">
        </figure>
      </div>
      <div class="col-md-4">
        <ProfileHeader :user="dish.user" />
        <p class="category">◾ {{ dish.category }}</p>
        <h1 class="title">{{ dish.name }}</h1>

        <h2 class="subtitle">Information</h2>
        <div class="black-bar"></div>

        <div class="serve-time">
          <span>🍽️ {{ dish.serving }}인분</span>
          <span>⏱️ {{ dish.time_minutes }}분</span>
        </div>
        <div class="black-bar"></div>

        <p class="ingredient">
        <p class="ingredient-title">재료</p>
        <p class="ingredients"> : {{ dish.ingredients.map(ing => ing.name).join(', ') }}</p>
        </p>

        <div class="black-bar"></div>
        <div class="url-section">
          <p class="url-title">참고링크</p>
          <p class="url" v-if="dish.link">{{ dish.link }}</p>
          <p class="url" v-else>: 없음</p>
        </div>

        <div class="black-bar"></div>
        <div class="mt-4">
          <button @click="handleLike" class="btn btn-success me-2">
            🧑🏻 지구인 ({{ dish.likes_count }})
          </button>
          <button @click="handleDislike" class="btn btn-danger">
            👽 외계인 ({{ dish.dislikes_count }})
          </button>
        </div>
      </div>

      <div class="description-section">
        <h2 class="subtitle">Description</h2>
        <div class="black-bar"></div>
        <p v-html="formatDescription(dish.description)"></p>
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
import { Toast } from 'bootstrap';

export default {
  name: "RecipeDetailView",
  data() {
    return {
      dish: null,
      toastMessage: '',
      toastClass: '',
      showReportModal: false,
      reportDetail: '',
    }
  },
  methods: {
    showToast(message, type = 'success') {
      this.toastMessage = message;
      this.toastClass = type === 'success' ? 'bg-success' : 'bg-danger';

      const toastElement = this.$refs.toast;
      const toast = new Toast(toastElement, {
        delay: 3000
      });

      toast.show();
    },
    async handleLike() {
      try {
        let response = await apiClient.post('/likengs/', {
          recipe_rated: this.dish.id,
          rate: 1
        });
        await this.fetchDishData();
        console.log(response.status)

        if (response.status == 201 || response.status == 200) {
          this.showToast('지구인을 눌렀습니다! 🧑🏻');
        } else if (response.status == 204) {
          this.showToast('지구인 버튼을 취소했습니다.');
        }
      } catch (error) {
        console.error('좋아요 처리 중 오류가 발생했습니다:', error);
      }
    },
    async handleDislike() {
      try {
        let response = await apiClient.post('/likengs/', {
          recipe_rated: this.dish.id,
          rate: -1
        });
        await this.fetchDishData();
        console.log(response.status)

        if (response.status == 201 || response.status == 200) {
          this.showToast('싫어요를 눌렀습니다! 👎', 'error');
        } else if (response.status == 204) {
          this.showToast('싫어요를 취소했습니다.', 'error');
        }
      } catch (error) {
        console.error('싫어요 처리 중 오류가 발생했습니다:', error);
      }
    },
    async fetchDishData() {
      try {
        const response = await apiClient.get(`/recipes/${this.$route.params.dish_id}/`);
        this.dish = response.data;
        console.log(this.dish);
        document.title = `${this.dish.name} - Recipick`;
      } catch (error) {
        console.error('레시피를 불러오는데 실패했습니다:', error);
      }
    },
    formatDescription(description) {
    // 줄바꿈 문자를 <br> 태그로 변환
    return description.replace(/\n/g, '<br>');
    },
    goBack() {
    this.$router.push("/recipes")
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
          reported_user: this.dish.user.id,
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
    this.fetchDishData();
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
.category {
  margin: 15px;
  font-size: 20px;
  text-align: right;
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
.serve-time {
  margin: 20px;
  gap: 30px;
  display: flex;
  justify-content: center;
  font-size: 20px;
}

/* 재료, url */
.ingredient,
.url-section {
  margin: 20px 0;
  text-align: left;
}
.ingredient-title,
.url-title {
  text-align: left;
  font-size: 21px;
  font-weight: bold;
  color: #505050;
}
.ingredients,
.url {
  text-align: left;
  font-size: 18px;
}

/* 지구인 외계인 버튼 */
.mt-4 {
  display: flex;
  justify-content: center;
  margin: 30px;
  gap: 20px;
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

.toast-container {
  z-index: 1050; /* Toast가 다른 요소 위로 표시되도록 설정 */
}

</style>