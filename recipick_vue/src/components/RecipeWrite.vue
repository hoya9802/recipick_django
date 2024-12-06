<template>
    <div class="title-image">
        <img src='@/assets/upload.png'>
    </div>

    <div class="write-container">
        <form @submit.prevent="submitPost">
            <!-- 이미지 업로드 -->
            <div class="image-upload-container">
                <input id="image-upload" class="image" type="file" @change="handleFileUpload" accept="image/*"/>
                <!-- 미리보기 -->
                <img v-if="previewImage" :src="previewImage" alt="Image Preview" class="image-preview" />
            </div>

            <!-- 제목 -->
            <input class="title" v-model="formData.title" type="text" placeholder="레시피 제목" required />

            <!-- 카테고리 -->
            <select v-model="formData.category" class="category" required>
                <option disabled value="">카테고리 선택</option>
                <option v-for="category in categories" :key="category.id" :value="category.name">
                    {{ category.name }}
                </option>
            </select>

            <!-- 조리 시간 -->
            <input class="time-minutes" v-model.number="formData.time_minutes" type="text" placeholder="조리 시간(분)"
                @input="validateTime" required />

            <!-- 인분 -->
            <input class="serving" v-model.number="formData.serving" type="number" placeholder="몇 인분" min="1"
                @input="validateServing" required />

            <!-- 레시피 링크 -->
            <input class="link" v-model="formData.link" type="url" placeholder="레시피 관련 링크(선택)" />

            <!-- 재료 -->
            <div class="ingredients">
                <select id="ingredients" v-model="selectedIngredients" multiple>
                    <option v-for="ingredient in ingredients" :key="ingredient.id" :value="ingredient">
                        {{ ingredient.name }}
                    </option>
                </select>
                <p v-if="selectedIngredients.length === 0">재료를 선택하세요.</p>
                <p>여러 재료를 선택하려면 ctrl을 누르고 선택해주세요</p>
            </div>

            <!-- 설명 -->
            <textarea class="content" v-model="formData.description" placeholder="내용" required></textarea>

            <!-- 버튼 -->
            <div class="actions">
                <button class="cancel" type="button" @click="$router.back()">취소</button>
                <button class="upload" type="submit">등록</button>
            </div>
        </form>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    name: "RecipeWrite",
    data() {
        return {
            formData: {
                name: "",
                category: "",
                time_minutes: "",
                serving: "",
                link: "",
                description: "",
            },
            ingredients: [],
            selectedIngredients: [],
            categories: [],
            image: null,
            previewImage: null,
        };
    },
    mounted() {
        this.fetchCategories();
        this.fetchIngredients();
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
        async fetchCategories() {
            try {
                const response = await apiClient.get("/categories/");
                this.categories = response.data;
            } catch (error) {
                console.error(error);
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
        validateTime(event) {
            const value = event.target.value.replace(/\D/g, ""); // 숫자가 아닌 문자 제거
            this.formData.time_minutes = value === "" ? "" : Math.max(1, parseInt(value)); // 1 이상으로 제한
        },
        validateServing(event) {
            const value = event.target.value.replace(/\D/g, ""); // 숫자가 아닌 문자 제거
            this.formData.serving = value === "" ? "" : Math.max(1, parseInt(value)); // 1 이상으로 제한
        },
        async submitPost() {
            try {
                if (!this.image) {
                alert("이미지를 선택해주세요.");
                console.warn("이미지가 업로드되지 않았습니다.");
                return;
            }
                const response = await apiClient.post("/recipes/", {
                    name: this.formData.title,
                    description: this.formData.description,
                    category: this.formData.category,
                    time_minutes: this.formData.time_minutes,
                    serving: this.formData.serving,
                    link: this.formData.link,
                    ingredients: this.selectedIngredients.map(ingredient => ({ name: ingredient.name })),
                });

                const id = response.data.id;
                await this.uploadImage(id);

                this.$router.push("/recipes");
            } catch (error) {
                console.error("레시피가 등록되지 않았습니다:", error);
            }
        },
        async uploadImage(id) {
            try {
                const formData = new FormData();
                formData.append("image", this.image);

                await apiClient.post(`/recipes/${id}/upload-image/`, formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });
            } catch (error) {
                console.error("이미지가 업로드 되지 않았습니다.:", error);
            }
        },

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
.image,
.actions {
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
select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 16px;
}

/* 추가 스타일 */
.category,
.time-minutes,
.serving,
.link {
    font-size: 18px;
    border: 1px solid #ccc;
    width: 100%;
    max-width: 960px;
    margin: 0 auto;
    padding: 13px;
    border-radius: 6px;
    box-sizing: border-box;
}

form .ingredient-section {
    margin-top: 15px;
}

form .ingredient-section div {
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>