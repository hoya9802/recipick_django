<template>
    <div class="find-password">
        <img src="@/assets/reset-password.png" class="title">
        <form @submit.prevent="submitEmail">
            <label class="email-title" for="email">계정의 이메일을 작성해주세요.</label>
            <input class="email-input" type="email" id="email" v-model="email" placeholder="ex) recipick@recipick.com" required />
            <button class="email-button" type="submit">임시 비밀번호 받기</button>
            <p class="back-to-login" @click="$router.push('/')">로그인 페이지로 돌아가기</p>
        </form>
        <p v-if="message" :class="{ success: !isError, error: isError }">{{ message }}</p>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default {
    data() {
        return {
            email: "",
            message: "",
            isError: false,
        };
    },
    methods: {
        async submitEmail() {
            try {
                const response = await apiClient.post("user/reset-password/", {
                    email: this.email,
                });
                this.message = response.data.message;
                this.isError = false;
            } catch (error) {
                this.message = error.response.data.error || "An error occurred.";
                this.isError = true;
            }
        },
    },
    mounted() {
        document.title = '임시 비밀번호 받기 - Recipick'
    },
};
</script>

<style scoped>
.find-password {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: white;
    padding: 20px;
    font-family: 'Arial', sans-serif;
}
form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 400px;
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.email-title {
    font-size: 1rem;
    color: #555;
    margin-bottom: 10px;
    text-align: center;
}
.email-input {
    width: 100%;
    padding: 10px;
    font-size: 1rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 20px;
    box-sizing: border-box;
}
.email-input:focus {
    outline: none;
    border-color: #4e4e4e;
    box-shadow: 0 0 2px #4e4e4e;
}
.email-button {
    width: 100%;
    padding: 10px 15px;
    font-size: 1rem;
    color: #fff;
    background-color: black;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-bottom: 10px;
}
.back-to-login {
    margin-top: 15px;
    font-size: 0.9rem;
    color: black;
    cursor: pointer;
    text-decoration: none;
    text-align: center;
}
p.error {
    color: #d9534f;
    font-size: 0.9rem;
    margin-top: 15px;
    text-align: center;
}
.find-password p.success {
    color: #5cb85c;
    font-size: 0.9rem;
    margin-top: 15px;
    text-align: center;
}
</style>