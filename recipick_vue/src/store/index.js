import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    id: '',
    nick_name: '',
    isLoading: false,
    recipes: [],
  },
  getters: {
  },
  mutations: {
    setId(state, id){
      state.id = id;
    },
    setNickname(state, nick_name){
      state.nick_name = nick_name;
    },
    setToken(state, token) {
      state.token = token;
      state.isAuthenticated = true;
    },
    removeToken(state) {
      state.token = '';
      state.isAuthenticated = false;
      state.id = '';
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setRecipes(state, recipes) {
      state.recipes = recipes;
    },
  },
  actions: {
  },
  modules: {
  }
})
