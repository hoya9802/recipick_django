import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import apiClient, { setAuthToken } from "@/store/api";

const token = localStorage.getItem("authToken");
if (token) {
  store.commit("setToken", token);
  setAuthToken(token);

  apiClient
    .get("/user/mypage/me/")
    .then((response) => {
      store.commit("setId", response.data.id);
    })
    .catch(() => {
      console.error("사용자 정보를 가져오지 못했습니다.");
    });
}

createApp(App).use(store).use(router).mount('#app')
