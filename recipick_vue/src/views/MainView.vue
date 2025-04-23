<template>
    <div class="welcome-recipick">
        <img src='@/assets/welcome-recipick.png'>
    </div>

    <div class="menu-notice">
        <p>📌 Recipick의 메뉴 알기</p>
    </div>

    <div class="black-bar"></div>

    <div class="slider-container">
        <div class="slider">
            <div class="slide" v-for="(banner, i) in banners" :key="i"
                :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
                <router-link :to="banner.link">
                    <img :src="banner.image" alt="배너 이미지" />
                </router-link>
            </div>
        </div>
        <button class="prev" @click="prevSlide">〈</button>
        <button class="next" @click="nextSlide">〉</button>
    </div>

    <div class="bestrecipe-section">
        <h2>🎉 Best 레시피</h2>
        <div class="black-bar"></div>
        <div class="bestrecipe-list">
            <div v-for="recipe in bestRecipes" :key="recipe.id" class="bestrecipe-card">
                <router-link :to="'/recipes/' + recipe.id">
                    <img :src="recipe.image || require('@/assets/default-image.png')" alt="Recipe Image"
                        class="bestrecipe-image" />
                    <div class="bestrecipe-info">
                        <h3>{{ recipe.name }}</h3>
                        <p>🧑🏻: {{ recipe.likes_count }} 👽: {{ recipe.dislikes_count }}</p>
                        <p>👩‍🍳 {{ recipe.user.nick_name }} - {{ recipe.user.level }}</p>
                    </div>
                </router-link>
            </div>
        </div>
    </div>

    <div class="ngrecipe-section">
        <h2>👽 지구인은 이해할 수 없는 음식</h2>
        <div class="black-bar"></div>
        <div class="ngrecipe-list">
            <div v-for="recipe in ngRecipes" :key="recipe.id" class="ngrecipe-card">
                <router-link :to="'/recipes/' + recipe.id">
                    <img :src="recipe.image || require('@/assets/default-image.png')" alt="Recipe Image"
                        class="ngrecipe-image" />
                    <div class="ngrecipe-info">
                        <h3>{{ recipe.name }}</h3>
                        <p>👽: {{ recipe.dislikes_count }}</p>
                        <p>👩‍🍳 {{ recipe.user.nick_name }} - {{ recipe.user.level }}</p>
                    </div>
                </router-link>
            </div>
        </div>
    </div>

    <div class="lab-section">
        <h2>💡 요리의 재발견</h2>
        <div class="black-bar"></div>
        <div class="lab-list">
            <div v-for="lab in recipeLabs" :key="lab.id" class="lab-card">
                <router-link :to="'/labs/' + lab.id">
                    <img :src="lab.image || require('@/assets/default-image.png')" alt="Lab Image" class="lab-image" />
                    <div class="lab-info">
                        <h3>{{ lab.title }}</h3>
                        <p> 🔎: {{ lab.likes_count }}</p>
                        <p>👩‍🍳 {{ lab.user.nick_name }} - {{ lab.user.level }}</p>
                    </div>
                </router-link>
            </div>
        </div>
    </div>

</template>

<script>
import Header from '@/components/Header.vue';
import apiClient from '@/store/api';

export default {
    data() {
        return {
            banners: [
                {
                    image: require('@/assets/banner1.png'),
                    link: '/freemarket'
                },
                {
                    image: require('@/assets/banner2.png'),
                    link: '/labs'
                },
                {
                    image: require('@/assets/banner3.png'),
                    link: '/help'
                },
                {
                    image: require('@/assets/banner4.png'),
                    link: '/expirations'
                },
                {
                    image: require('@/assets/banner5.png'),
                    link: '/generator'
                },
            ],
            currentIndex: 0,
            intervalId: null,

            // 베스트 레시피
            topRecipes: [],
            ng5Recipes: [],
            recipe3Labs: [],
        };
    },
    components: {
        Header,
    },
    computed: {
        bestRecipes() {
            return this.topRecipes.slice(0, 5);
        },
        ngRecipes() {
            return this.ng5Recipes.slice(0, 5);
        },
        recipeLabs() {
            return this.recipe3Labs.slice(0, 3);
        }
    },
    methods: {
        // Recipick의 메뉴 알기
        nextSlide() {
            this.currentIndex = (this.currentIndex + 1) % this.banners.length;
        },
        prevSlide() {
            this.currentIndex =
                (this.currentIndex - 1 + this.banners.length) % this.banners.length;
        },
        startAutoSlide() {
            this.intervalId = setInterval(() => {
                this.nextSlide();
            }, 5000);
        },
        stopAutoSlide() {
            if (this.intervalId) {
                clearInterval(this.intervalId);
                this.intervalId = null;
            }
        },

        // 베스트 레시피
        async fetchBestRecipes() {
            try {
                const response = await apiClient.get("/recipes/top-ranked/");
                this.topRecipes = response.data.map((recipe) => ({
                    ...recipe,
                    image: recipe.image ? `${process.env.VUE_APP_API_BASE_URL.replace('/api', '')}${recipe.image}` : null,
                }));
            } catch (error) {
                console.error("레시피 데이터를 가져오는 중 오류 발생:", error);
            }
        },
        // ng 레시피
        async fetchNgRecipes() {
            try {
                const response = await apiClient.get("/recipes/top-nglisted/");
                this.ng5Recipes = response.data.map((recipe) => ({
                    ...recipe,
                    image: recipe.image ? `${process.env.VUE_APP_API_BASE_URL.replace('/api', '')}${recipe.image}` : null,
                }));
            } catch (error) {
                console.error("지구인은 이해할 수 없는 음식 데이터를 가져오는 중 오류 발생:", error);
            }
        },
        // 요리 실험 일지
        async fetchRecipeLab() {
            try {
                const response = await apiClient.get("/labs/top-lablisted/");
                this.recipe3Labs = response.data.map((lab) => ({
                    ...lab,
                    image: lab.image ? `${process.env.VUE_APP_API_BASE_URL.replace('/api', '')}${lab.image}` : null,
                }));
            } catch (error) {
                console.error("요리 실험 일지 데이터를 가져오는 중 오류 발생:", error);
            }
        },
    },
    mounted() {
        document.title = 'Recipick'
        this.startAutoSlide();
        this.fetchBestRecipes();
        this.fetchNgRecipes();
        this.fetchRecipeLab();
    },
    beforeDestroy() {
        this.stopAutoSlide();
    },
};
</script>

<style scoped>
.welcome-recipick img {
    width: 100%;
    height: auto;
    margin-bottom: 40px;
    display: block;
}

.slider-container {
    position: relative;
    width: 100%;
    max-width: 1520px;
    margin: 40px auto;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

.slider {
    display: flex;
    transition: transform 0.5s ease-in-out;
    width: 100%;
    height: 100%;
}

.slide {
    min-width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

.slide img {
    width: 100%;
    height: auto;
    object-fit: contain;
    display: block;
}

.prev,
.next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background-color: rgba(175, 175, 175, 0.5);
    color: white;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    cursor: pointer;
    font-size: 20px;
    z-index: 10;
    opacity: 0;
    visibility: hidden;
}

.prev {
    left: 10px;
}

.next {
    right: 10px;
}

.slider-container:hover .prev,
.slider-container:hover .next {
    opacity: 1;
    visibility: visible;
}

/* 베스트 레시피, ng 레시피, 실험일지 */
.bestrecipe-section,
.ngrecipe-section,
.lab-section {
    margin-top: 150px;
    margin-bottom: 150px;
    text-align: left;
    width: 100%;
}

.lab-section {
    margin-bottom: 200px;
}

.menu-notice,
.bestrecipe-section h2,
.ngrecipe-section h2,
.lab-section h2 {
    font-size: 28px;
    font-weight: bold;
    margin-left: 20px;
    margin-bottom: 20px;
    text-align: left;
}

.bestrecipe-list,
.ngrecipe-list,
.lab-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: left;
    margin: 10px;
}

.bestrecipe-card,
.ngrecipe-card {
    flex: 1 1 calc(20% - 10px);
    /* 5개의 카드가 한 줄에 고르게 배치 */
    max-width: calc(20% - 10px);
    box-sizing: border-box;
    border: 1px solid #ddd;
    padding: 20px;
    text-align: center;
}

.lab-card {
    flex: 1 1 calc(33% - 10px);
    /* 3개의 카드가 한 줄에 고르게 배치 */
    max-width: calc(33% - 10px);
    box-sizing: border-box;
    border: 1px solid #ddd;
    padding: 20px;
    text-align: center;
}

.bestrecipe-image,
.ngrecipe-image {
    width: 100%;
    height: 350px;
    object-fit: cover;
    margin-bottom: 5px;
}

.lab-image {
    width: 100%;
    height: 300px;
    object-fit: cover;
    margin-bottom: 5px;
}

.bestrecipe-info h3,
.ngrecipe-info h3,
.lab-info h3 {
    font-size: 25px;
    font-weight: bold;
    margin: 15px;
}

.bestrecipe-info p,
.ngrecipe-info p,
.lab-info p {
    font-size: 20px;
    margin: 5px 0;
    color: #555;
}

/* 블랙바 */
.black-bar {
    width: 100%;
    height: 4px;
    background-color: black;
    margin: 5px 0;
}

.bestrecipe-card a,
.ngrecipe-card a,
.lab-card a {
    text-decoration: none;
    color: black;
}
</style>
