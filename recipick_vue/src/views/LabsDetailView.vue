<template>
    <div class="lab-detail-container">
        <div v-if="lab" class="lab-detail">
            <div class="lab-header">
                <h1 class="help-title">{{ lab.title }}</h1>
                <div class="black-bar"></div>
                <div class="lab-meta">
                    <span class="user">{{ lab.user?.nick_name || "Unknown" }} - {{ lab.user?.level || "Unknown Level"
                        }}</span>
                    <span @click="handleLikeToggle" style="cursor: pointer">🔎 : {{ lab.likes_count || 0 }}</span>
                    <span class="date">Update: {{ lab.modify_dt }}</span>
                </div>
            </div>

            <!-- 이미지 섹션 -->
            <div class="lab-image-container">
                <img v-if="lab.image" :src="lab.image" alt="Lab" class="lab-image" />
            </div>

            <!-- 재료 및 설명 섹션 -->
            <div class="lab-ingredients">
                <p class="lab-ingredients-title">Ingredients</p>
                <div class="black-bar"></div>
                <span v-for="ing in lab.ingredients" :key="ing.id">
                    <router-link :to="'/ingredients/' + ing.id" class="ingredient-link ingredients">
                        {{ ing.name }}
                    </router-link>{{ index < lab.ingredients.length - 1 ? ', ' : '' }}
                </span>
            </div>

            <div class="lab-description">
                <p class="lab-description-title">Description</p>
                <div class="black-bar"></div>
                <p class="description" v-html="formatDescription(lab.description) || 'No description available.'"></p>
            </div>

            <button @click="goBack" class="back-btn">목록</button>
            <div class="report-section">
                <button class="report-button" @click="confirmReport">
                    신고하기
                </button>
            </div>
        </div>
        <div v-else>
            <p>데이터를 불러오는 중입니다...</p>
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
import apiClient from "@/store/api";

export default {
    name: "LabsDetailView",
    data() {
        return {
            lab: null,
            showReportModal: false,
            reportDetail: '',
        };
    },
    async created() {
        const lab_id = this.$route.params.lab_id;
        await this.fetchLabDetail(lab_id);
    },
    methods: {
        async fetchLabDetail(lab_id) {
            try {
                const response = await apiClient.get(`/labs/${lab_id}/`);
                this.lab = response.data;
                document.title = `${this.lab.title} - Recipick`;
            } catch (error) {
                console.error("실험일지 상세 정보를 가져오는 중 오류 발생:", error);
                alert("실험일지 상세 정보를 불러오지 못했습니다.");
            }
        },
        async handleLikeToggle() {
            try {
                if (this.userLiked) {
                    // 좋아요 취소
                    await apiClient.post(`/likes/`, { exlog: this.lab.id });
                    this.lab.likes_count--;
                    this.userLiked = false;
                } else {
                    // 좋아요 추가
                    await apiClient.post(`/likes/`, { exlog: this.lab.id });
                    this.lab.likes_count++;
                    this.userLiked = true;
                }
            } catch (error) {
                console.error("좋아요 토글 중 오류 발생:", error);
                alert("좋아요 처리 중 오류가 발생했습니다.");
            }
        },
        goBack() {
            this.$router.push("/labs");
        },
        formatDescription(description) {
            // 줄바꿈 문자를 <br> 태그로 변환
            return description.replace(/\n/g, '<br>');
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
                    reported_user: this.lab.user.id,
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
};
</script>
<style scoped>
.lab-detail-container {
    padding: 20px;
    background-color: white
}
.lab-detail {
    max-width: 800px;
    margin: auto;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
}
.lab-header {
    margin-bottom: 30px;
}
.lab-title {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
}
.lab-meta {
    display: flex;
    justify-content: space-between;
    margin: 20px;
}
.user {
    color: #777;
    text-align: start;
    font-size: 17px;
}
.date {
    color: #777;
    font-size: 17px;
    text-align: end;
}
.lab-image-container {
    margin: 20px 0;
    text-align: center;
}
.lab-image {
    max-width: 100%;
    border-radius: 8px;
}
.lab-ingredients,
.lab-description {
    margin: 0 auto 50px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}
.lab-ingredients-title,
.lab-description-title {
    font-weight: bold;
    font-size: 25px;
    text-align: left;
}
.ingredients,
.description {
    font-size: 18px;
    line-height: 1.6;
    text-align: left;
    max-height: 400px;
    overflow-y: auto;
    padding: 2px 10px;
}
/* 블랙바 */
.black-bar {
    width: 100%;
    height: 2px;
    background-color: #a7a7a7;
    margin: 10px 0;
}
.back-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #575757;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

/* 신고하기 버튼 */
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
