<template>
    <div class="mypage-container">
        <!-- 프로필 -->
        <div class="profile-section">
            <img :src="user.profile_image || require('@/assets/default-profile.png')" alt="Profile Image"
                class="profile-image" />
            <h2>{{ user.nick_name }} - {{ user.level }}</h2>
        </div>

        <!-- 내가 받은 총 개수 -->
        <div class="recations-counts-section">
            <p class="reactions-title">Reactions to Me</p>
            <div class="black-bar"></div>
            <div class="recations">
                <div class="human">
                    <p>🧑🏻 : {{ }}</p>
                </div>
                <div class="alien">
                    <p>👽 : {{ }}</p>
                </div>
                <div class="magnifying glass">
                    <p>🔎 : {{ }}</p>
                </div>
            </div>
        </div>

        <!-- 총 개수 -->
        <div class="posts-counts-section">
            <p class="posts-title">My Post</p>
            <div class="black-bar"></div>
            <div class="posts">
                <div>
                    <p>레시피 : {{ user.recipes_count }}개</p>
                </div>
                <div>
                    <p>요리 실험일지 : {{ user.labs_count }}개</p>
                </div>
                <div>
                    <p>재료 나눔 : {{ user.freemarkets_count }}개</p>
                </div>
            </div>

        </div>

        <!-- 회원정보수정, 회원탈퇴 -->
        <div class="actions-section">
            <button @click="goToEditProfile" class="btn btn-primary">
                회원정보 수정
            </button>
            <button @click="deleteAccount" class="btn btn-danger">
                회원 탈퇴
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
            },
        };
    },
    methods: {
        async fetchMypageData() {
            try {
                const response = await apiClient.get("/user/mypage/me/");
                this.user = response.data;
            } catch (err) {
                console.error("마이페이지 데이터를 가져오지 못했습니다.", err);
            }
        },
        goToEditProfile() {
            this.$router.push("/mypage/update"); // 프로필 수정 페이지로 이동
        },
        async deleteAccount() {
            if (confirm("정말로 회원 탈퇴를 진행하시겠습니까?")) {
                try {
                    await apiClient.delete("/user/mypage/me/");
                    alert("회원 탈퇴가 완료되었습니다. 회원가입 페이지로 이동합니다.");
                    this.$router.push("/signup"); // 탈퇴 후 회원가입 페이지로 이동
                } catch (err) {
                    console.error("회원 탈퇴 중 문제가 발생했습니다.", err);
                }
            }
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
    margin: 30px auto;
    text-align: center;
    padding: 20px;
    border: 1px solid #d6d6d6;
    border-radius: 10px;
    background-color: white;
}

.profile-section {
    margin-bottom: 20px;
}

.profile-image {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 10px;
}

/* 블랙바 */
.black-bar {
    width: 100%;
    height: 4px;
    background-color: black;
    margin: 5px 0;
}

/* 리액션 */
.recations-counts-section {
    justify-content: space-around;
    flex-direction: column; /* 세로 정렬 */
    align-items: flex-start; /* 텍스트 왼쪽 정렬 */
    margin-bottom: 20px;
    padding: 15px; /* 내부 여백 추가 */
    border: 2px solid #ccc; /* 테두리 색상 및 두께 설정 */
    border-radius: 10px; /* 모서리를 둥글게 처리 (옵션) */
    background-color: #f9f9f9;
}
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
}

/* 포스트 */
.posts-counts-section {
    justify-content: space-around;
    flex-direction: column; /* 세로 정렬 */
    align-items: flex-start; /* 텍스트 왼쪽 정렬 */
    margin-bottom: 20px;
    padding: 15px; /* 내부 여백 추가 */
    border: 2px solid #ccc; /* 테두리 색상 및 두께 설정 */
    border-radius: 10px; /* 모서리를 둥글게 처리 (옵션) */
    background-color: #f9f9f9;
}
.posts {
    margin-top: 10px;
    margin-left: 15px;
    text-align: left;
}

/* 회원정보 수정, 탈퇴 */
.actions-section {
    display: flex;
    justify-content: space-around;
}
</style>