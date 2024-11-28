<template>
    <div class="top">
        <div class="top-section">
            <div class="id">
                <span @click="idDropdown">{{ nickname }} 님 <img src="@/assets/icon.png" class="iconimage"></span>
                <ul v-if="iddropdownOpen" class="id-dropdown">
                    <li><router-link to="/mypage" @click.native="closeDropdown">마이페이지</router-link></li>
                    <li><router-link to="/mypage/update" @click.native="closeDropdown">회원정보수정</router-link></li>
                    <li @click="logout">로그아웃</li>
                </ul>
            </div>
            <a href="">공지사항</a>
            <a href="">레시피 업로드</a>
        </div>
            <div class="emo">
                <a class="emo1">🧑🏻</a>
                <a class="emo2">👽</a>
            </div>
    </div>

    <div class="header">
        <div class="header-logo">
            <router-link to="/main">
                <img src="@/assets/recipick1.png">
            </router-link>
        </div>
        <div class="header-right">


        </div>
    </div>

    <nav class="custom-navbar">
        <div class="container">
            <ul class="nav-menu">

                <div class="category">
                    <span @mouseover="toggleDropdown">카테고리</span>
                    <ul v-if="dropdownOpen">
                        <li v-for="category in categories" :key="category.id">
                            ◾ {{ category.name }}
                        </li>
                    </ul>
                </div>
                <li><router-link to="/recipe-list">요리보기</router-link></li>
                <li><a href="#">재료 무료 나눔</a></li>
                <li><a href="#">요리 실험 일지</a></li>
                <li><a href="#">요리 지식인</a></li>
                <li><a href="#">유통기한 알림</a></li>

            </ul>
        </div>
    </nav>
</template>

<script>
import apiClient, { setAuthToken } from '@/store/api';

export default {
    name: 'Header',
    data() {
        return {
            categories: [],
            dropdownOpen: false,
            iddropdownOpen: false,
        }
    },
    computed: {
        nickname() {
            console.log("닉네임 상태:", this.$store.state.nick_name);
            return this.$store.state.nick_name;
        }
    },
    created() {
        if (this.$route.name !== "loginaccount") {
            this.fetchCategories();
        } else {
            console.log("fetchCategories skipped on route:", this.$route.name);
        }
    },

    methods: {
        logout() {
            localStorage.removeItem("authToken");
            setAuthToken(null);
            this.$store.commit("removeToken");
            alert("로그아웃되었습니다.");
            this.$router.push("/");
        },
        async fetchCategories() {
            const token = localStorage.getItem("authToken");
            if (!token) {
                return;
            }

            try {
                const response = await apiClient.get("/categories/", {
                    headers: {
                        Authorization: `Token ${token}`,
                    },
                });
                console.log("Fetched categories:", response.data);
                this.categories = response.data;
            } catch (error) {
                console.error("Error fetching categories:", error);
                alert("카테고리를 가져오지 못했습니다.");
            }
        },
        toggleDropdown() {
            this.dropdownOpen = !this.dropdownOpen;
        },
        idDropdown(){
            this.iddropdownOpen = !this.iddropdownOpen;
        },
        closeDropdown(){
            this.iddropdownOpen = false;
        }
    },

    watch: {
        $route() {
            this.dropdownOpen = false;
        }
    },
};
</script>

<style scoped>
.top {
    width: 88%;
    padding: 5px 30px;
    display: flex;
    justify-content: flex-end;
    margin-right: 8%;
    background-color: white;
}
.top-section {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 10; /* 내부 여백 제거 */
    margin: 10;
}
.top-section span,
.top-section a {
    color: black;
    text-decoration: none;
    font-size: 16px;
    min-width: 80px;
    text-align: center;
    cursor: pointer;
    margin-right: 5px;
}
.emo {
    margin-left: 20px;
    display: flex;
    gap: 25px;
    align-items: center;
    justify-content: flex-start;
    width: auto;
    padding: 0;
}
.emo1, .emo2 {
    font-size: 20px;
    text-decoration: none;
    margin: 0;
    padding: 0;
    display: inline-block;
    width: auto;
}

/* id 드롭다운 */
.id {
    position: relative;
    display: inline-block;
}
.id ul{
    position: absolute;
    top: 110%;
    left: 0;
    background-color: white;
    border: 1px solid #ddd;
    width: 150px;
    padding: 8px 0;
    margin: 0;
    list-style: none;
    z-index: 1000;
}
.id ul.v-enter-active,
.id ul.v-enter-to {
    display: block;
}
.id ul li {
    padding: 8px 16px;
    font-size: 16px;
    color: black;
    cursor: pointer;
    transition: background-color 0.2s ease;
}
.id ul li:hover {
    background-color: #f0f0f0;
}
.iconimage{
    width: 15px;
    height: 18px;
}
.heartimage {
    width: 25px;
    height: 25px;
    cursor: pointer;
}

/* 레시픽 로고 */
.header {
    margin-top: 30px;
    justify-content: center;
    display: flex;
    align-items: center;
    position: relative;
    margin-bottom: 50px;
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
.nav-menu span {
    color: white;
    font-weight: bold;
    font-size: clamp(0.8rem, 1vw, 1rem);
    cursor: pointer;
}
.nav-menu a {
    text-decoration: none;
    color: white;
    font-weight: bold;
    font-size: clamp(0.8rem, 1vw, 1rem);
}

/* 카테고리 드롭다운 */
.category {
    position: relative;
    display: inline-block;
}
.category ul {
    position: absolute;
    top: 140%;
    left: 0;
    background-color: white;
    border: 1px solid #ddd;
    width: 150px;
    padding: 8px 0;
    margin: 0;
    list-style: none;
    z-index: 1000;
}
.category ul.v-enter-active,
.category ul.v-enter-to {
    display: block;
}
.category ul li {
    padding: 8px 16px;
    font-size: 16px;
    color: black;
    cursor: pointer;
    transition: background-color 0.2s ease;
}
.category ul li:hover {
    background-color: #f0f0f0;
}
.nav-menu span {
    color: white;
    font-weight: bold;
    font-size: clamp(0.8rem, 1vw, 1rem);
    cursor: pointer;
    transition: color 0.2s ease;
}

</style>
