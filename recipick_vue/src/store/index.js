import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    id: '',
  },
  getters: {
  },
  mutations: {
    setId(state, id){
      state.id = id;
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
  },
  actions: {
  },
  modules: {
  }
})
