<template>
    <div class="title-image">
        <img src='@/assets/upload.png'>
    </div>

    <div class="write-container">
        <form @submit.prevent="submitEdit">
            <input class="title" v-model="formData.title" type="text" placeholder="요리 지식인 제목" required />
            <textarea class="content" v-model="formData.description" placeholder="내용" required></textarea>

            <!-- 이미지 업로드 -->
            <div class="image-upload-container">
                <input id="image-upload" class="image" type="file" @change="handleFileUpload" accept="image/*" />
                <img :src="previewImage" alt="Uploaded or Default" class="image-preview" />
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
import defaultImage from "@/assets/default-image.png";

export default {
    name: "MyHelpEdit",
    data() {
        return {
            formData: {
                title: "",
                description: "",
            },
            image: null,
            previewImage: defaultImage,
            id: null,
        };
    },
    methods: {
        async fetchHelpDetails() {
            try {
                const response = await apiClient.get(`/helps/${this.id}/`);
                const help = response.data;

                this.formData.title = help.title;
                this.formData.description = help.description;
                this.previewImage = help.image || defaultImage;
            } catch (error) {
                console.error("지식인 정보 불러오기 실패:", error);
                alert("지식인 정보를 가져오는 중 오류가 발생했습니다.");
            }
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
            } else {
                this.previewImage = defaultImage;
            }
        },
        async submitEdit() {
            try {
                await apiClient.patch(`/helps/${this.id}/`, {
                    title: this.formData.title,
                    description: this.formData.description,
                });

                if (this.image) {
                    await this.uploadImage();
                }

                alert("수정이 완료되었습니다.");
                this.$router.push("/my-help");
            } catch (error) {
                console.error("수정 과정에서 오류 발생:", error);
                alert("수정 중 오류가 발생했습니다.");
            }
        },
        async uploadImage() {
            try {
                const formData = new FormData();
                formData.append("image", this.image);

                await apiClient.post(`/helps/${this.id}/upload-image/`, formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });
            } catch (error) {
                console.error("이미지 업로드 실패:", error);
            }
        },
    },
    mounted() {
        this.id = this.$route.params.id;
        this.fetchHelpDetails()
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
