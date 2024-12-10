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
            <router-link to="/notice" class="notice">공지사항</router-link>
            <router-link to="/recipes/write" class="write">레시피 업로드</router-link>
        </div>
        <div class="emo">
            <a class="emo1">🧑🏻</a>
            <a class="emo2">👽</a>
        </div>
    </div>
    <div class="logo header">
        <router-link to="/main">
            <img src="@/assets/recipick1.png" class="logo">
        </router-link>
    </div>

    <nav class="custom-navbar">
        <div class="container">
            <ul class="nav-menu">
                <div class="category">
                    <a @click="toggleDropdown" class="category-title">카테고리</a>
                    <ul v-if="dropdownOpen">
                        <li
                            v-for="category in categories"
                            :key="category.id"
                            @click="fetchRecipes(category.id)"
                            class="category-drop-menu"
                        >
                            ◾ {{ category.name }}
                        </li>
                    </ul>
                </div>
                <li><router-link to="/recipes">요리보기</router-link></li>
                <li><router-link to="/freemarket">재료 무료 나눔</router-link></li>
                <li><router-link to="/labs">요리 실험 일지</router-link></li>
                <li><router-link to="/help">요리 지식인</router-link></li>
                <li><router-link to="/generator">AI 추천 레시피</router-link></li>
                <li><router-link to="/expirations">유통기한 알림</router-link></li>
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
        async fetchRecipes(category_id) {
            try {
                const response = await apiClient.get(`/categories/${category_id}/recipes/`);
                this.$store.commit("setRecipes", response.data);
                this.$router.push(`/category/${category_id}`);
            } catch (error) {
                console.error("Failed to fetch recipes:", error);
            }
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
    width: 100%;
    padding: 5px 30px;
    display: flex;
    justify-content: flex-end;
    margin-top: 10px;
    background-color: white;
}
.top-section {
    display: flex;
    align-items: center;
    gap: 15px;
}
.top-section span,
.top-section a,
.notice {
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
    font-size: 14px;
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
.logo header {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}
.logo {
    margin: 0 auto;
    display: block;
    justify-content: center;
    align-items: center;
    position: relative;
    left: auto;
    transform: none;
    max-width: 230px;
    max-height: 100px;
    width: auto;
    height: auto;
}

/* nav */
.custom-navbar {
    background-color: black;
    padding: 10px 20px;
    max-width: 100%;
    margin-left: auto;
    margin-right: auto;
    display: flex;
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
    gap: clamp(5px, 5vw, 50px);
    margin: 0px 10%;
    padding: 0;
    justify-content: space-around;
    width: 100%;
}
.nav-menu a {
    text-decoration: none;
    color: white;
    font-weight: bold;
    font-size: 16px;
    font-size: clamp(0.8rem, 0.9vw, 1rem);
    padding: 5px 10px; /* 상하좌우 여백 최소화 */
    white-space: nowrap;
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
.category a {
    color: white;
    font-weight: bold;
    font-size: clamp(0.8rem, 1vw, 1rem);
    cursor: pointer;
    transition: color 0.2s ease;
}
.category-drop-menu {
    text-align: left;
}
</style>
