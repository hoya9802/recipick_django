import { createStore } from 'vuex'
import apiClient from '@/store/api';

export default createStore({
  state: {
    isAuthenticated: '',
    token: '',
    id: '',
    nick_name: '',
    isLoading: false,
    likedRecipes: [],
    dislikedRecipes: [],
  },
  getters: {
  },
  mutations: {
    setId(state, id) {
      state.id = id;
    },
    setNickname(state, nick_name) {
      state.nick_name = nick_name;
    },
    setToken(state, token) {
      state.token = token;
      state.isAuthenticated = true;
    },
    removeToken(state) {
      state.token = null;
      state.isAuthenticated = false;
      state.id = '';
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setLikedRecipes(state, recipes) {
      state.likedRecipes = recipes;
    },
    setDislikedRecipes(state, recipes) {
      state.dislikedRecipes = recipes;
    },
  },
  actions: {
    async fetchLikedRecipes({ commit }) {
      try {
        const response = await apiClient.get('/likengs/user-liked/');
        commit('setLikedRecipes', response.data);
      } catch (error) {
        console.error('좋아요 누른 레시피 가져오기 실패:', error);
      }
    },
    async fetchDislikedRecipes({ commit }) {
      try {
        const response = await apiClient.get('/likengs/user-disliked/');
        commit('setDislikedRecipes', response.data);
      } catch (error) {
        console.error('싫어요 누른 레시피 가져오기 실패:', error);
      }
    },
  },
  modules: {
  }
})
