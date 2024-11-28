<template>
  <div v-if="dish" class="dish-detail mb-5">
    <div class="row">
        <div class="col-md-8">
            <figure class="mb-4 dish-image">
                <img v-bind:src="dish.image" class="img-fluid">
            </figure>
        </div>
        <div class="col-md-4">
            <h1 class="title"><strong>{{ dish.name }}</strong></h1>
            <p><strong>카테고리: </strong>{{ dish.category }}</p>

            <h2 class="subtitle">Information</h2>
            <h4>재료: </h4>
            <p>
                {{ dish.ingredients.map(ing => ing.name).join(', ') }}
            </p>
            <p><strong>{{ dish.serving }} 인분</strong></p>
            <p><strong>요리시간: {{ dish.time_minutes }}</strong></p>
            <p>
                <strong v-if="dish.link">참고링크: {{ dish.link }}</strong>
                <strong v-else>참고링크: 없음</strong>
            </p>

            <div class="mt-4">
                <button @click="handleLike" class="btn btn-success me-2">
                    👍 좋아요 ({{ dish.likes_count }})
                </button>
                <button @click="handleDislike" class="btn btn-danger">
                    👎 싫어요 ({{ dish.dislikes_count }})
                </button>
            </div>
        </div>
    </div>
    <div>
        <h2 class="subtitle">Description</h2>
        {{ dish.description }}
        {{ cur }}
        <div class="toast-container position-fixed bottom-0 end-0 p-3">
            <div
            class="toast align-items-center text-white border-0"
            :class="toastClass"
            role="alert"
            aria-live="assertive"
            aria-atomic="true"
            ref="toast"
            >
            <div class="d-flex">
                <div class="toast-body">
                {{ toastMessage }}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import apiClient from '@/store/api';
import { Toast } from 'bootstrap';

export default {
  name: "DishDetailView",
  data() {
    return {
      dish: null,
      toastMessage: '',
      toastClass: '',
      cur: ''
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
        this.cur = response.status;
        console.log(response.status)

        if (response.status == 201 || response.status == 200) {
          this.showToast('좋아요를 눌렀습니다! 👍');
        } else if (response.status == 204) {
          this.showToast('좋아요를 취소했습니다.');
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
        this.cur = response.status;
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
        document.title = `${this.dish.name} - Recipick`;
      } catch (error) {
        console.error('레시피를 불러오는데 실패했습니다:', error);
      }
    }
  },
  created() {
    this.fetchDishData();
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