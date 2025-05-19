<template>
    <body>
        <div v-if="!recipe" class="container">
            <div  v-if="!isLoading">
                <h1><strong>요리 재료를 하나씩 넣어주세요!</strong></h1>
                <h5>영어로 입력해주세요</h5>
                <div v-for="(input, index) in inputs" :key="index">
                    <input type="text" v-model="inputs[index]" placeholder="재료를 입력하세요" />
                    <button v-if="boxCount !== 1" @click="removeInput(index)">삭제</button>
                </div>
                <button v-if="boxCount<5" @click="addInput">+</button>
                <br>
                <button v-if="!isLoading" class="btn btn-primary" type="button" @click="generateRecipe">레시피 생성하기</button>
            </div>
            <!-- 로딩 상태 표시 -->
            <div v-if="isLoading" class="loading">
                <img src="@/assets/dog-chef.gif" alt="Loading..." />
                <br><br>
                <h3>색다른 요리를 추천해드릴게요. 잠시만 기다려 주세요😊</h3>
            </div>
        </div>

        <div class="container">
            <div v-if="recipe" class="recipe-result">
            <h2>생성된 레시피: <strong>{{ recipe.title }}</strong></h2>
            <hr>
            <p>내가 입력한 재료들: {{ recipe.prompt ? recipe.prompt.join(', ') : inputs.join(', ') }}</p>
            <hr>
            <p v-for="ingre in recipe.ingredients" :key="ingre">
                {{ ingre }}
            </p>
            <hr>
            <p v-for="m in recipe.method" :key="m">
                {{ m }}
            </p>
            </div>
        </div>
    </body>
</template>

<script>
import apiClient from '@/store/api';

export default {
    name: 'RecipeGenerateView',
    data() {
        return {
            inputs: [''],
            isLoading: false,
            recipe: null,
            boxCount: 1,
        };
    },
    methods: {
        addInput() {
            this.inputs.push('');
            this.boxCount ++;
        },
        removeInput(index) {
            this.inputs.splice(index, 1);
            this.boxCount --;
        },
        async generateRecipe() {
            this.isLoading = true;
            this.recipe = null;
            try {
                const response = await apiClient.post('/ai/generate/', {
                    "ingredients": this.inputs
                });
                console.log('API Response:', response.data.output);
                this.recipe = response.data.output;
            } catch (error) {
                console.error('Error generating recipe:', error);
            } finally {
                this.isLoading = false;
            }
        }
    }
}
</script>

<style scoped>
.container {
    padding: 20px;
    display: flex;
    justify-content: center;
}
h1 {
    font-size: 2em;
}
input {
    margin-top: 20px;
    padding: 10px;
    font-size: 1em;
}
button {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 1em;
}
.loading {
    margin-top: 20px;
    font-size: 1.2em;
    color: #007bff;
}
.recipe-result {
    margin-top: 20px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
    width: 100%;
    max-width: 600px;
}
</style>