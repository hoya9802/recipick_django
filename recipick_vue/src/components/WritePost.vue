<template>
    <div class= "image">
        <img src="@/assets/upload.png" class="uploadimage">
    </div>

    <div class="write-container">
        <form @submit.prevent="submitPost">
            <input
                class="title"
                v-model="newPost.name"
                type="text"
                placeholder="제목"
                required
            />
            <input
                type="file"
                @change="handleFileUpload"
            />
            <textarea
                class="description"
                v-model="newPost.description"
                placeholder="내용"
                required>
            </textarea>


        </form>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    name: "FreeMarketWrite",
    data() {
        return {
            newPost: {
                name: "",
                description: "",
                purchase_dt: "",
                count: 1,
                is_shared: false,
                image: null,
            },
        };
    },
    methods: {
        handleFileUpload(event) {
            this.newPost.image = event.target.files[0];
        },
        async submitPost() {
            try {
                const formData = new FormData();
                formData.append("name", this.newPost.name);
                formData.append("description", this.newPost.description);
                formData.append("purchase_dt", this.newPost.purchase_dt);
                formData.append("count", this.newPost.count);
                formData.append("is_shared", this.newPost.is_shared);
                if (this.newPost.image) {
                    formData.append("image", this.newPost.image);
                }

                await apiClient.post("/freemarkets/", formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });

                this.$router.push("/freemarket"); // 글 작성 후 리스트로 이동
            } catch (error) {
                console.log(error);
            }
        },
    },
};
</script>

<style scoped>
.write-container {
    width:100%;
    max-width: 1500px;
    margin: 0 auto;
    padding: 20px;
    background-color: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}
.title {
    width: auto;
    font-size: 25px;
    padding: 10px;
}
.description {
    width: auto;
    height: 500px;
    font-size: 18px;
    padding: 10px;
}


</style>