import { createRouter, createWebHistory } from 'vue-router'
import LoginAccount from '../views/LoginAccountView.vue';
import Mainpage from '@/views/MainView.vue';
import store from '@/store';
import DishList from '@/views/DishListView.vue';
import Signup from '@/views/SignupView.vue';
import Mypage from '@/views/MypageView.vue';
import Update from '@/views/UpdateView.vue';

const routes = [
  {
    path: '/',
    name: 'loginaccount',
    component: LoginAccount,
    beforeEnter: (to, from, next) => {
      if (store.state.isAuthenticated == true) {
        next({name: 'main'});
      } else {
        next();
      }
    }
  },
  {
    path: '/main',
    name: 'main',
    component: Mainpage,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dish-list',
    name: 'DishList',
    component: DishList,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
    beforeEnter: (to, from, next) => {
      if (store.state.isAuthenticated) {
        alert('회원가입 페이지는 로그아웃 후에 접근할 수 있습니다.');
        next({ name: 'main' });
      } else {
        next();
      }
    },
  },
  {
    path: '/mypage',
    name: 'Mypage',
    component: Mypage,
    meta: {
      requireLogin: true
    },
  },
  {
    path: '/mypage/update',
    name: 'Update',
    component: Update,
    meta: {
      requireLogin: true
    },
  },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = store.state.isAuthenticated;

    if (to.meta.requireLogin && !isAuthenticated) {
        alert('로그인 후에 접근할 수 있습니다.')
        next({ name: 'loginaccount' });
    } else if (to.name === 'loginaccount' && isAuthenticated) {
        alert('로그아웃 후에 접근할 수 있습니다.')
        next({ name: 'main' });
    } else {
        next();
    }
});
export default router
