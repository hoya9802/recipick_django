<template>
    <div class="title-image">
        <img src='@/assets/upload.png'>
    </div>

    <div class="write-container">
        <form @submit.prevent="submitPost">
            <input class="title" v-model="formData.title" type="text" placeholder="요리 실험 일지 제목" required />
            <textarea class="content" v-model="formData.description" placeholder="내용" required></textarea>

            <!-- 이미지 업로드 -->
            <div class="image-upload-container">
                <input id="image-upload" class="image" type="file" @change="handleFileUpload" accept="image/*" />
                <img v-if="previewImage" :src="previewImage" alt="Image Preview" class="image-preview" />
            </div>

            <div class="ingredients">
                <select id="ingredients" v-model="selectedIngredients" multiple>
                    <option v-for="ingredient in ingredients" :key="ingredient.id" :value="ingredient">
                        {{ ingredient.name }}
                    </option>
                </select>
                <p v-if="selectedIngredients.length === 0">재료를 선택하세요.</p>
            </div>

            <div class="actions">
                <button class="cancel" type="button" @click="$router.back()">취소</button>
                <button class="upload" type="submit">수정</button>
            </div>
        </form>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    name: "MyLabEdit",
    data() {
        return {
            formData: {
                title: "",
                description: "",
            },
            ingredients: [],
            selectedIngredients: [],
            image: null,
            previewImage: null,
            id: null,
        };
    },
    methods: {
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
        async fetchIngredients() {
            try {
                const response = await apiClient.get("/ingredients/");
                this.ingredients = response.data;
            } catch (error) {
                console.error("재료 목록을 불러오는 중 오류 발생:", error);
            }
        },
        async fetchLabDetail() {
            try {
                const response = await apiClient.get(`/labs/${this.id}/`);
                const lab = response.data;

                this.formData.title = lab.title;
                this.formData.description = lab.description;
                this.selectedIngredients = lab.ingredients;
                this.previewImage = lab.image || null;
            } catch (error) {
                console.error("실험일지 불러오기 실패:", error);
                alert("실험일지 정보를 가져오는 중 오류가 발생했습니다.");
            }
        },
        async submitPost() {
            try {
                await apiClient.patch(`/labs/${this.id}/`, {
                    title: this.formData.title,
                    description: this.formData.description,
                    ingredients: this.selectedIngredients.map(ingredient => ({ name: ingredient.name })),
                });

                if (this.image) {
                    await this.uploadImage(this.id);
                }

                alert("수정이 완료되었습니다.");
                this.$router.push("/my-lab");
            } catch (error) {
                console.error("수정 과정에서 오류 발생:", error);
                alert("수정 중 오류가 발생했습니다.");
            }
        },
        async uploadImage(id) {
            try {
                const formData = new FormData();
                formData.append("image", this.image);

                await apiClient.post(`/labs/${id}/upload-image/`, formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });
            } catch (error) {
                console.error("이미지 업로드 실패:", error);
            }
        },
    },
    async mounted() {
        this.id = this.$route.params.id;
        await this.fetchIngredients();
        await this.fetchLabDetail();
    },
};
</script>
<style scoped>
/* 공통 스타일 */
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
.cancel,
.upload {
    padding: 15px 30px;
    background-color: #575757;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.cancel:hover,
.upload:hover {
    background-color: #333333;
}
.cancel:disabled,
.upload:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.ingredients {
    margin: 20px 0;
}
select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 16px;
}

</style>