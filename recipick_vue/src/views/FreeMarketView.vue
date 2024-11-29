<template>
<div class="dish-container">
    <div class="dish-grid">
        <div v-for="market in marketList" :key="market.id" class="post">
            <MarketBox :market="market"/>
        </div>
    </div>
</div>
</template>

<script>
import apiClient from '@/store/api';
import MarketBox from '@/components//MarketBox.vue';

export default {
    name: 'FreeMarketView',
    data() {
        return {
            marketList: [],
        }
    },
    mounted() {
        this.getMarketList()
    },
    methods: {
        async getMarketList() {
            try {
                const response = await apiClient.get('/freemarkets/?all=true')
                this.marketList = response.data;
                document.title = '재료 무료나눔 - Recipick';
            } catch (error) {
                console.log(error);
            }
        }
    },
    components: {
        MarketBox: MarketBox,
    }
}
</script>

<style>
.dish-container {
  padding: 20px;
}

.dish-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2vw;
  padding: 2vw;
  max-width: 1200px;
  margin: 0 auto;
}

.post {
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

@media (max-width: 1024px) {
  .dish-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .dish-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .dish-grid {
    grid-template-columns: 1fr;
  }
}
</style>