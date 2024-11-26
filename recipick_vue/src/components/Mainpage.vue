<template>
<Header></Header>
  <div class="welcom-recipick">
    <img src='@/assets/welcom-recipick.png'>
  </div>

  <h2>📌Recipick의 메뉴 알기</h2>

  <div class="slider-container">
    <div class="slider">
      <div
        class="slide"
        v-for="(image, i) in banners"
        :key="i"
        :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
      >
        <img :src="image" alt="배너 이미지" />
      </div>
    </div>
    <button class="prev" @click="prevSlide">〈</button>
    <button class="next" @click="nextSlide">〉</button>
  </div>

  <div class="bestrecipe-section">
    <h2>🎉어제의 Best 레시피</h2>
    <h4>best레시피 나열</h4>
    <button @click="more">더보기</button>
  </div>

  <div class="recipenote-section">
    <h2>📋요리 실험 일지</h2>
    <h4>요리 실험 일지 나열</h4>
    <button @click="more">더보기</button>
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
      currentIndex: 0,
      intervalId: null,
    };
  },
  components: {
    Header,
  },
  methods: {
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
  },
  beforeDestroy() {
    this.stopAutoSlide();
  },
};
</script>

<style scoped>
.welcom-recipick img{
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

/* 베스트 레시피 */
.bestrecipe-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 15px;
}
.bestrecipe-section h2 {
    font-size: 25px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: left;
    width: 100%;
}
.bestrecipe-section button {
    padding: 10px 20px;
    font-size: 15px;
    color: #fff;
    background-color: black;
    border: none;
    border-radius: 20px;
    cursor: pointer;
}

/* 요리실험일지 */
.recipenote-section{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 15px;
}
.recipenote-section h2 {
    font-size: 25px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: left;
    width: 100%;
}
.recipenote-section button {
    padding: 10px 20px;
    font-size: 15px;
    color: #fff;
    background-color: black;
    border: none;
    border-radius: 20px;
    cursor: pointer;
}
</style>
