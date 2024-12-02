<template>
    <div class="mypage-container">
        <!-- 프로필 -->
        <div class="profile-section">
            <img :src="user.profile_image || require('@/assets/default-profile.png')" alt="Profile Image"
                class="profile-image" />
            <div class="nick-level-box">
                <p class="nick-level">My Nickname - Level</p>
                <div class="black-bar"></div>
                <h2>{{ user.nick_name }} - {{ user.level }}</h2>
            </div>
        </div>

        <!-- 내가 받은 총 개수 -->
        <div class="recations-counts-section">
            <p class="reactions-title">Reactions to Me</p>
            <div class="black-bar"></div>
            <div class="recations">
                <div class="human">
                    <p>🧑🏻 : {{ user.likes_count }}</p>
                </div>
                <div class="alien">
                    <p>👽 : {{ user.dislikes_count}}</p>
                </div>
                <div class="magnifying glass">
                    <p>🔎 : {{user.lab_likes_count }}</p>
                </div>
            </div>
        </div>

        <!-- 총 개수 -->
        <div class="posts-counts-section">
            <p class="posts-title">My Post</p>
            <div class="black-bar"></div>
            <div class="posts">
                <div class="post-row">
                    <span class="post-label">레시피</span>
                    <span class="post-value">{{ user.recipes_count || 0 }}개</span>
                </div>
                <div class="post-row">
                    <span class="post-label">요리 실험일지</span>
                    <span class="post-value">{{ user.labs_count || 0 }}개</span>
                </div>
                <div class="post-row">
                    <span class="post-label">재료 나눔</span>
                    <span class="post-value">{{ user.freemarkets_count || 0 }}개</span>
                </div>
            </div>
        </div>

        <!-- 회원정보수정 -->
        <div class="update-profile">
            <button @click="goToUpdateProfile">
                회원정보 수정
            </button>
        </div>
    </div>
</template>

<script>
import apiClient from "@/store/api";

export default{
    name: 'Mypage',
    data() {
        return {
            user: {
                profile_image: null,
                nick_name: "",
                level: "",
                recipes_count: 0,
                labs_count: 0,
                freemarkets_count: 0,
                likes_count: 0,
                dislikes_count: 0,
                lab_likes_count: 0,
            },
        };
    },
    methods: {
        async fetchMypageData() {
            try {
                const response = await apiClient.get("/user/mypage/");
                this.user = response.data;
            } catch (err) {
                console.error("마이페이지 데이터를 가져오지 못했습니다.", err);
            }
        },
        goToUpdateProfile() {
            this.$router.push("/mypage/update");
        },

    },
    mounted() {
        document.title = '마이페이지 - Recipick'
        this.fetchMypageData();
    }

}
</script>

<style scoped>
.mypage-container {
    max-width: 600px;
    margin: 17px auto;
    text-align: center;
    padding: 20px;
    border: 1px solid #d6d6d6;
    background-color: white;
}

/* 프로필 */
.profile-section {
    margin-top: 12px;
    margin-bottom: 20px;
}
.profile-image {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    border: 1px solid #d6d6d6;
    object-fit: cover;
    margin-bottom: 10px;
}
.profile-section h2 {
    margin-top: 10px;
    font-size: 23px;
}

/* 블랙바 */
.black-bar {
    width: 100%;
    height: 4px;
    background-color: black;
    margin: 5px 0;
}

/* 리액션 */
.nick-level-box,
.recations-counts-section,
.posts-counts-section {
    justify-content: space-around;
    padding: 15px;
}
.nick-level,
.reactions-title,
.posts-title {
    font-size: 20px;
    font-weight: bold;
    text-align: left;
    margin-bottom: 2px;
}
.recations {
    display: flex;
    justify-content: space-around;
    margin-top: 10px;
    font-size: 18px;
}

/* 포스트 */
.posts {
    margin-top: 10px;
    text-align: left;
    font-size: 18px;
}
.post-row {
    display: flex;
    justify-content: space-between;
    padding: 5px 0;
    font-size: 16px;
    margin-left: 100px;
    margin-right: 150px;
}
.post-label {
    font-weight: bold;
}
.post-value {
    text-align: right;
    color: #555;
}

/* 회원정보 수정 */
.update-profile button {
    margin: 0px auto;
    width: 130px;
    padding: 8px;
    color: white;
    background-color: #5c5c5c;
    border-radius: 10px;
    font-weight: bold;
    font-size: 17px;
}
</style>