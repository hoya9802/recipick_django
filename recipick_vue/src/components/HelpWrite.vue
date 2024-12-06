<template>
    <div class="title-image">
        <img src='@/assets/upload.png'>
    </div>

    <div class="write-container">
        <form @submit.prevent="submitPost">
            <input class="title" v-model="formData.title" type="text" placeholder="요리 지식인 제목" required />
            <textarea class="content" v-model="formData.description" placeholder="내용" required></textarea>

            <!-- 이미지 업로드 -->
            <div class="image-upload-container">
                <input id="image-upload" class="image" type="file" @change="handleFileUpload" accept="image/*" />
                <!-- 미리보기 또는 기본 이미지 -->
                <img :src="previewImage" alt="Uploaded or Default" class="image-preview" />
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
import defaultImage from "@/assets/default-image.png";

export default {
    name: "HelpWrite",
    data() {
        return {
            formData: {
                title: "",
                description: "",
            },
            image: null,
            previewImage: defaultImage,
        };
    },
    methods: {
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.image = file;

                // 미리보기 이미지 생성
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.previewImage = e.target.result;
                };
                reader.readAsDataURL(file);
            } else {
                this.previewImage = defaultImage;
            }
        },
        async submitPost() {
            try {
                const formData = new FormData();
                Object.entries(this.formData).forEach(([key, value]) => {
                    formData.append(key, value);
                });
                if (this.image) formData.append("image", this.image);

                await apiClient.post("/helps/", formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });
                this.$router.push("/help");
            } catch (error) {
                console.error(error);
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
</style>