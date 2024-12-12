<template>
    <div class="title-image">
        <img src='@/assets/upload.png'>
    </div>

    <div class="write-container">
        <form @submit.prevent="submitEdit">
            <input class="title" v-model="formData.name" type="text" placeholder="재료 무료 나눔 제목" required />
            <textarea class="content" v-model="formData.description" placeholder="내용" required></textarea>

            <!-- 이미지 업로드 -->
            <div class="image-upload-container">
                <input id="recipe-image" class="image" type="file" @change="handleFileUpload" accept="image/*" />
                <!-- 미리보기 -->
                <img :src="previewImage" alt="Recipe Preview" class="image-preview" />
            </div>

            <div class="date-box">
                <p class="date-title">구입한 날짜</p>
                <div class="black-bar"></div>
                <input
                    class="date"
                    v-model="formData.purchase_dt"
                    type="date"
                    :max="today"
                    required
                />
            </div>

            <div class="count-box">
                <p class="count-title">나눔할 수량</p>
                <div class="black-bar"></div>
                <input
                class="count"
                v-model="formData.count"
                type="number"
                placeholder="나눔할 수량"
                @input="validateCount"
                required
            />
            </div>

            <div class="actions">
                <button type="button" @click="$router.back()">취소</button>
                <button type="submit">수정</button>
            </div>
        </form>
    </div>
</template>

<script>
import apiClient from "@/store/api";
import defaultImage from "@/assets/default-image.png";

export default {
    name: "FreeMarketEdit",
    data() {
        return {
            formData: {
                name: "",
                description: "",
                purchase_dt: "",
                count: 1,
                is_shared: false,
            },
            image: null,
            previewImage: defaultImage,
            today: "",
            id: null,
        };
    },
    mounted() {
        this.setTodayDate();
        this.id = this.$route.params.id;
        this.fetchMarketDetails();
    },
    methods: {
        setTodayDate() {
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            this.today = `${yyyy}-${mm}-${dd}`;
        },
        async fetchMarketDetails() {
            try {
                const response = await apiClient.get(`/freemarkets/${this.id}/`);
                const market = response.data;

                this.formData.name = market.name;
                this.formData.description = market.description;
                this.formData.purchase_dt = market.purchase_dt;
                this.formData.count = market.count;
                this.previewImage = market.image || defaultImage;
            } catch (error) {
                console.error("나눔 정보 불러오기 실패:", error);
                alert("나눔 정보를 가져오는 중 오류가 발생했습니다.");
            }
        },
        validateCount(event) {
            const value = event.target.value.replace(/\D/g, "");
            this.formData.count = value === "" ? "" : Math.max(1, parseInt(value));
        },
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.image = file;
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.previewImage = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        },
        async submitEdit() {
            try {
                await apiClient.patch(`/freemarkets/${this.id}/`, {
                    name: this.formData.name,
                    description: this.formData.description,
                    purchase_dt: this.formData.purchase_dt,
                    count: this.formData.count,
                });

                if (this.image) {
                    await this.uploadImage();
                }

                alert("수정이 완료되었습니다.");
                this.$router.push("/my-market");
            } catch (error) {
                console.error("수정 중 오류 발생:", error);
                alert("수정 중 오류가 발생했습니다.");
            }
        },
        async uploadImage() {
            try {
                const formData = new FormData();
                formData.append("image", this.image);

                await apiClient.post(`/freemarkets/${this.id}/upload-image/`, formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });
            } catch (error) {
                console.error("이미지 업로드 실패:", error);
            }
        },
    },
};
</script>

<style scoped>
.title-image {
    margin: 20px auto;
    text-align: center;
}
.write-container {
    max-width: 1000px;
    margin: 20px auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-family: Arial, sans-serif;
}
form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.title,
.content,
.image {
    width: 100%;
    max-width: 960px;
    margin: 0 auto;
}
.title,
.content,
.image {
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 6px;
    box-sizing: border-box;
    font-size: 20px;
}
.title {
    height: 50px;
}
.content {
    height: 400px;
    resize: vertical;
}
.image {
    font-size: 16px;
}
.image-upload-container {
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 10px;
    margin-bottom: 20px;
}
.image-preview {
    width: 100%;
    max-width: 300px;
    height: auto;
    border-radius: 8px;
    border: 1px solid #ddd;
    object-fit: cover;
}
/* 버튼 */
.actions {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}
button {
    padding: 15px 30px;
    background-color: #575757;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
button:hover {
    background-color: #333333;
}
button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

/* 추가 스타일 */
.date-box,
.count-box {
    width: 100%;
    margin: 10px auto;
    padding: 10px;
}
.date-title,
.count-title {
    margin-bottom: 0px;
    text-align: left;
    font-size: 20px;
    font-weight: bold;
}
.date,
.count {
    margin-top: 15px;
    text-align: center;
    width: 130px;
    height: 40px;
    font-size: 16px;
}

/* 블랙바 */
.black-bar {
    width: 100%;
    height: 2px;
    background-color: #a7a7a7;
    margin: 5px 0;
}
</style>
