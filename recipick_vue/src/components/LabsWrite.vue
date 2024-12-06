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
                <input id="recipe-image" class="image" type="file" @change="handleFileUpload" accept="image/*" />
                <!-- 미리보기 -->
                <img v-if="previewImage" :src="previewImage" alt="Recipe Preview" class="image-preview" />
            </div>

            <!-- <div class="ingredients">
                <div class="ingredient-grid">
                    <div v-for="(ingredient, index) in ingredients" :key="index" class="ingredient-item">
                        <input v-model="ingredients[index].name" placeholder="재료 이름" required
                            class="ingredient-input" />
                        <button type="button" @click="removeIngredient(index)" class="remove-ingredient">X</button>
                    </div>
                </div>
                <button type="button" @click="addIngredient" :disabled="ingredients.length >= 30"
                    class="add-ingredient">
                    + 재료 추가
                </button>
            </div> -->

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
                <button class="upload" type="submit">등록</button>
            </div>
        </form>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    name: "LabWrite",
    data() {
        return {
            formData: {
                title: "",
                description: "",
            },
            ingredients: [], // 재료 목록
            selectedIngredients: [], // 선택된 재료
            image: null,
            previewImage: null,
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
        async submitPost() {
            try {
                const formData = new FormData();
                Object.entries(this.formData).forEach(([key, value]) => {
                    formData.append(key, value);
                });
                formData.append("ingredients", JSON.stringify(this.selectedIngredients.map(ingredient => ({ name: ingredient.name })))
            );
                if (this.image) formData.append("image", this.image);

                await apiClient.post("/labs/", formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });
                this.$router.push("/labs");
            } catch (error) {
                console.error(error);
            }
        },
    },
        mounted() {
        this.fetchIngredients();
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

/* 재료 추가 버튼 및 제거 버튼 */
/* .ingredients {
    margin-top: 15px;
}
.ingredient-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}
.ingredient-item {
    display: flex;
    align-items: center;
    gap: 10px;
}
.ingredient-input {
    flex: 1;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 16px;
}
.add-ingredient {
    display: block;
    margin: 10px auto;
    background-color: #658aee;
    color: white;
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.add-ingredient:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.remove-ingredient {
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.remove-ingredient:hover {
    background-color: #d63333;
} */
</style>