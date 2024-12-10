import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: '',
    token: '',
    id: '',
    nick_name: '',
    isLoading: false,
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
  },
  actions: {
  },
  modules: {
  }
})
