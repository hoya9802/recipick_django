<template>

    <div class="write-container">
        <WritePost></WritePost>
        <div class="count-box">
            <p class="count-title">판매수량</p>
            <input class="count" v-model="newPost.count" type="number" placeholder="판매 수량" required />
        </div>

        <label>
            <input v-model="newPost.is_shared" type="checkbox" />
            나눔 여부
        </label>
        <input v-model="newPost.purchase_dt" type="date" placeholder="구매한 날짜" required />

        <button type="submit">등록</button>
        <button type="button" @click="$router.back()">취소</button>

    </div>
</template>

<script>
import apiClient from "@/store/api";
import WritePost from '@/components/WritePost.vue';

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
    components: {
        WritePost : WritePost,
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
.count-box {
    margin: 30px 0;
    padding: 10px;
    text-align: left;
}
.count-title {
    font-size: 23px;
    font-weight: bold;

}
.count {

}
button {
    padding: 10px;
    background-color: #575757;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: #333333;
}
</style>