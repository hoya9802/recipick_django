<template>
    <div class="top">
        <div class="top-box">
            <a href="">{{ id }} 님</a>
            <button @click="logout">로그아웃</button>
            <a href="">공지사항</a>
        </div>
    </div>
    <div class="header">
        <img src="@/assets/recipick1.png">
    </div>

    <nav class="custom-navbar">
        <div class="container">
            <ul class="nav-menu">
                <li><a href="#">카테고리</a></li>
                <li><a href="#">요리보기</a></li>
                <li><a href="#">재료 무료 나눔</a></li>
                <li><a href="#">요리 실험 일지</a></li>
                <li><a href="#">요리 지식인</a></li>
                <li><a href="#">유통기한 알림</a></li>
            </ul>
        </div>
    </nav>

</template>

<script>
import { setAuthToken } from '@/store/api';

export default {
    name: 'Mainpage',
    computed: {
        id(){
            return this.$store.state.id;
        }
    },

    methods: {
        logout() {
            localStorage.removeItem("authToken");
            setAuthToken(null);
            this.$store.commit("removeToken");
            alert("로그아웃되었습니다.");
            this.$router.push("/");
        }
    }
};
</script>

<style scoped>
.top {
    padding: 5px 30px;
    display: flex;
    justify-content: flex-end;
    margin-right: 8%;
}
.top-box {
    display: flex;
    align-items: center;
    gap: 1px;
}

.top-box a {
    color: #333;
    text-decoration: none;
    font-size: 14px;
    min-width: 80px;
    text-align: center;
}

.top-box a:first-child {
    margin-right: 0px;
}

.top-box button {
    background-color: white;
    border: 2px solid #fce4b9;
    color: #6b6b6b;
    border-radius: 3px;
    margin-top: 12px;
    padding: 3px 8px;
    font-size: 13px;
}

.header {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}
.header img {
    max-width: 190px;
    height: auto;
}

/* nav */
.custom-navbar {
    background-color: white;
    border: 3px solid #fce4b9;
    border-radius: 20px;
    padding: 10px 20px;
    max-width: 1500px;
    margin-left: auto;
    margin-right: auto;
}

.container {
    max-width: 100%;
    margin: 0 auto;
    display: flex;
    justify-content: center;
    align-items: center;
}

.nav-menu {
    list-style: none;
    display: flex;
    gap: clamp(10px, 12vw, 150px);
    margin: 0;
    padding: 0;
    justify-content: center;
    width: 100%;
}

.nav-menu a {
    text-decoration: none;
    color: rgb(88, 88, 88);
    font-weight: bold;
    font-size: clamp(0.8rem, 1vw, 1rem);
}
</style>