<template>
    <div class="top">
        <div class="top-section">
            <a href="">{{ id }} 님</a>
            <button @click="logout">로그아웃</button>
            <a href="">공지사항</a>
        </div>
    </div>
    <div class="header">
        <div class="header-logo">
            <img src="@/assets/recipick1.png">
        </div>
        <div class="header-right">
            <a href="">레시피 업로드</a>
            <img src="@/assets/hearticon.png">
        </div>
    </div>

    <nav class="custom-navbar">
        <div class="container">
            <ul class="nav-menu">
            <li>카테고리</li>
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

export default{
    name : 'App',
    data() {
        return
    },
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
    width: 80%;
    padding: 5px 30px;
    display: flex;
    justify-content: flex-end;
    margin-right: 8%;
    background-color: white;
}
.top-section {
    display: flex;
    align-items: center;
    gap: 1px;
}

.top-section a {
    color: black;
    text-decoration: none;
    font-size: 16px;
    min-width: 80px;
    text-align: center;
}

.top-section a:first-child {
    margin-right: 4px;
    text-align: end;
}

.top-section button {
    background-color: white;
    border: 2px solid black;
    color: #6b6b6b;
    border-radius: 20px;
    cursor: pointer;
    padding: 3px 8px;
    font-size: 16px;
}

.header {
    justify-content: center;
    display: flex;
    align-items: center;
    position: relative;
    margin-bottom: 20px;
}
.header-logo {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}
.header-logo img {
    max-width: 230px;
    max-height: 180px;
    height: auto;
}
.header-right {
    margin-left: auto;
    margin-right: 20%;
    display: flex;
    align-items: center;
    gap: 10px;
}
.header-right a {
    text-decoration: none;
    color: black;
    font-size: 16px;
}
.header-right img {
    max-width: 50px;
    max-height: 50px;
    cursor: pointer;
}

/* nav */
.custom-navbar {
    background-color: black;
    padding: 10px 20px;
    max-width: 100%;
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
    color: white;
    font-weight: bold;
    font-size: clamp(0.8rem, 1vw, 1rem);
}
</style>
