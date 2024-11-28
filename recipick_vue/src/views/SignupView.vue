<template>
<div class="signup-container">
    <div class="signup-box">
        <img src="@/assets/signup.png" alt="Signup Image" />

        <form @submit.prevent="signupForm">
            <input v-model="profileimage" type="text" placeholder="프로필 이미지" required />
            <input v-model="id" type="text" placeholder="*아이디" required />
            <input v-model="email" type="email" placeholder="*이메일" required />
            <input v-model="nick_name" type="text" placeholder="*닉네임" required />
            <input v-model="password" type="password" placeholder="*비밀번호" required />
            <input v-model="confirmPassword" type="password" placeholder="*비밀번호 확인" required />
            <button type="submit">회원가입</button>
        </form>

        <a class="back-to-login" @click="$router.push('/')">
            이미 계정이 있으신가요? 로그인 페이지로 이동하기
        </a>
    </div>
</div>
</template>

<script>
import apiClient from '@/store/api';

export default {
    name: 'Signup',
    data() {
        return {
            id: '',
            email: '',
            nick_name: '',
            password: '',
            confirmPassword: '',
        };
    },
    mounted() {
        document.title = '회원가입 - Recipick'
    },
    methods: {
        async signupForm() {
            if (this.password !== this.confirmPassword) {
                alert("비밀번호가 일치하지 않습니다.");
                return;
            }

            try {
                await apiClient.post("/user/create/", {
                    id: this.id,
                    email: this.email,
                    nick_name: this.nick_name,
                    password: this.password,
                });

                alert("회원가입이 완료되었습니다.");
                this.$router.push("/");
            } catch (error) {
                console.error("회원가입 실패:", error);
                alert("회원가입에 실패했습니다. 다시 시도해주세요.");
            }
        },
    },
};
</script>

<style scoped>

.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 90vh;
  background-color: white;
  margin: 0;
}
.signup-box {
    background: white;
    border: 1px solid #d6d6d6;
    text-align: center;
    width: 400px;
    padding: 10px;
}
.signup-box img {
    max-width: 330px;
    width: 100%;
    height: auto;
}
.signup-box input {
    width: 70%;
    margin-bottom: 15px;
    padding: 15px;
    border: 1px solid #dbdbdb;
    border-radius: 5px;
    background: #fafafa;
    font-size: 100%;
}
.signup-box button {
    width: 78%;
    padding: 13px;
    color: white;
    background-color: black;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    font-size: 15px;
    cursor: pointer;
    margin-bottom: 10px;
}
.back-to-login {
    text-decoration: none;
    color: black;
    font-size: 85%;
    cursor: pointer;
    margin-top: 20px;
    margin-bottom: 30px;
    display: block;
}
</style>