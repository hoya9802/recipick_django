<template>
    <div class="welcom-recipick">
        <img src='@/assets/welcom-recipick.png'>
    </div>

    <h2>📌Recipick의 메뉴 알기</h2>

    <div class="slider-container">
        <div class="slider">
            <div class="slide" v-for="(image, i) in banners" :key="i"
                :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
                <img :src="image" alt="배너 이미지" />
            </div>
        </div>
        <button class="prev" @click="prevSlide">〈</button>
        <button class="next" @click="nextSlide">〉</button>
    </div>

    <div class="bestrecipe-section">
        <h2>🎉어제의 Best 레시피</h2>
        <div v-if="topRecipes.length > 0" class="recipe-list">
            <div v-for="recipe in topRecipes" :key="recipe.id" class="recipe-card">
                <img :src="recipe.image" alt="Recipe Image" class="recipe-image" />
                <div class="recipe-info">
                    <h3>{{ recipe.name }}</h3>
                    <p>👍 좋아요: {{ recipe.likes_count }}</p>
                    <p>👩‍🍳 작성자: {{ recipe.user.nick_name }} (Level: {{ recipe.user.level }})</p>
                </div>
            </div>
        </div>
        <div v-else>
            <p>데이터를 불러오는 중입니다.</p>
        </div>
    </div>

    <div class="ngrecipe-section">
        <h2>💥어제의 NG 요리</h2>
        <h4>어제의 NG 요리</h4>
    </div>

    <div class="recipenote-section">
        <h2>📋요리 실험 일지</h2>
        <h4>요리 실험 일지 나열</h4>
    </div>
</template>

<script>
import Header from '@/components/Header.vue';

export default {
    data() {
        return {
            banners: [
                require('@/assets/banner1.png'),
                require('@/assets/banner2.png'),
                require('@/assets/banner3.png'),
                require('@/assets/banner4.png'),
                require('@/assets/banner5.png'),
            ],
            topRecipes: [],
            currentIndex: 0,
            intervalId: null,
        };
    },
    components: {
        Header,
    },
    methods: {
        async fetchTopRecipes() {
            try {
                const response = await axios.get('/api/recipes/top-liked/');
                this.topRecipes = response.data;
            } catch (error) {
                console.error('Best 레시피 데이터를 가져오는 중 오류 발생:', error);
            }
        },
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
    },
    mounted() {
        this.startAutoSlide();
        this.fetchTopRecipes();
    },
    beforeDestroy() {
        this.stopAutoSlide();
    },
};
</script>

<style scoped>
.welcom-recipick img {
    width: 100%;
    height: auto;
    margin-bottom: 40px;
    display: block;
}
.slider-container {
    position: relative;
    width: 100%;
    max-width: 1520px;
    margin: 0 auto;
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
.recipenote-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 15px;
}

.bestrecipe-section h2,
.ngrecipe-section h2,
.recipenote-section h2 {
    font-size: 25px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: left;
    width: 100%;
}

/* 스타일을 최적화 */
.recipe-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    margin-top: 20px;
}

.recipe-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    width: 300px;
    text-align: center;
}

.recipe-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 10px;
}

.recipe-info h3 {
    font-size: 20px;
    margin-bottom: 5px;
}

.recipe-info p {
    margin: 5px 0;
}
</style>
