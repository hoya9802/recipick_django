import { createRouter, createWebHistory } from 'vue-router'
import LoginAccount from '../views/LoginAccountView.vue';
import Mainpage from '@/views/MainView.vue';
import store from '@/store';
import RecipeList from '@/views/RecipeListView.vue';
import RecipeDetail from '@/views/RecipeDetail.vue';
import Signup from '@/views/SignupView.vue';
import Mypage from '@/views/MypageView.vue';
import Update from '@/views/UpdateView.vue';
import FreeMarket from '@/views/FreeMarketView.vue';
import MarketDetail from '@/views/MarketDetailVIew.vue';
import CategoryView from '@/views/CategoryView.vue';

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
    path: '/recipes',
    name: 'RecipeList',
    component: RecipeList,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/freemarket',
    name: 'FreeMarket',
    component: FreeMarket,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/freemarket/:market_id/',
    name: 'MarketDetail',
    component: MarketDetail,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/recipes/:dish_id/',
    name: 'RecipeDetail',
    component: RecipeDetail,
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
  {
    path: '/category/:category_id',
    name: 'CategoryView',
    component: CategoryView,
    props: true,
    meta: {
      requireLogin: true
    }
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
