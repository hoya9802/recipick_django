<template>
    <div class="login-box">
        <img src="@/assets/login.png" alt="Login Image" />

        <form @submit.prevent="loginForm">
            <input
                v-model="id"
                type="text"
                placeholder="아이디"
                required
            />
            <input
                v-model="password"
                type="password"
                placeholder="비밀번호"
                required
            />
            <button type="submit">로그인</button>
        </form>

        <a href="">아이디 찾기 / </a>
        <a href="">비밀번호 찾기 / </a>
        <a href="">회원가입</a>
    </div>
</template>

<script>
import apiClient, { setAuthToken } from '@/store/api';

export default {
    name: 'Login',
    data() {
        return {
            id: '',
            password: '',
        };
    },
    mounted() {
        document.title = 'Recipick'
    },
    methods: {
        async loginForm(){
            try {
                const response = await apiClient.post("/user/token/", {
                    id: this.id,
                    password: this.password,
            });

            const token = response.data.token;

            localStorage.setItem("authToken", token);
            setAuthToken(token);
            this.$store.commit("setToken", token);

            const userResponse = await apiClient.get("/user/mypage/me/", {
            headers: { Authorization: `Token ${token}` },
            });

            const userId = userResponse.data.id;
            this.$store.commit("setId", userId);

            this.$router.push("/main");
            } catch (error) {
                console.error("로그인 실패:", error);
                alert("아이디 또는 비밀번호를 확인하세요.");
                this.$store.commit("removeToken");
                localStorage.removeItem("authToken");
            }
        },
    },
};
</script>

<style>
.login-box {
    background: white;
    border: 1px solid #dbdbdb;
    padding: 20px;
    margin-bottom: 20px;
    text-align: center;
    width: 300px;
    height: 400px;
}

.login-box img {
    margin-top: 30px;
    max-width: 160px;
    width: 60%;
    height: auto;
}

input {
    width: 70%;
    margin-bottom: 15px;
    padding: 10px;
    border: 1px solid #dbdbdb;
    border-radius: 5px;
    background: #fafafa;
    font-size: 60%;
}

button {
    width: 77%;
    padding: 8px;
    color: white;
    background-color: #fadba0;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    margin-bottom: 10px;
}

a {
    text-decoration-line: none;
    color: #fdb226;
    font-size: 60%;
}
</style>