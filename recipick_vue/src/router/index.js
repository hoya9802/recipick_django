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
import LabsView from '@/views/LabsView.vue';
import RecipeGenerateView from '@/views/RecipeGenerateView.vue';
import LabsDetail from '@/views/LabsDetailView.vue';
import NoticeView from '@/views/NoticeView.vue';
import NoticeDetailView from '@/views/NoticeDetailView.vue';
import Expirations from '@/views/ExpirationsView.vue';
import ExpirationsDetail from '@/views/ExpirationsDetailView.vue';
import Help from '@/views/HelpView.vue';
import HelpDetail from '@/views/HelpDetail.vue';
import MarketWrite from '@/views/MarketWriteView.vue';
import LabsWrite from '@/views/LabsWriteView.vue';
import RecipeWrite from '@/views/RecipeWriteView.vue';
import HelpWrite from '@/views/HelpWriteView.vue';
import ChatRoom from '@/views/ChatRoomView.vue';
import ChatListView from '@/views/ChatListView.vue'
import FindId from '@/views/FindIdView.vue';
import ResetPassword from '@/views/ResetPasswordView.vue';
import Like from '@/views/LikeView.vue';
import DisLike from '@/views/DisLikeView.vue';

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
    path: '/freemarket/write',
    name: 'MarketWrite',
    component: MarketWrite,
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
    path: '/recipes/write',
    name: 'RecipeWrite',
    component: RecipeWrite,
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
  {
    path: '/labs',
    name: 'LabsView',
    component: LabsView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/labs/:lab_id',
    name: 'LabsDetail',
    component: LabsDetail,
    meta: {
      requireLogin: true
    },
    props: true,
  },
  {
    path: '/labs/write',
    name: 'LabsWrite',
    component: LabsWrite,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/generator',
    name: 'RecipeGenerateView',
    component: RecipeGenerateView,
  },
  {
    path: '/notice',
    name: 'NoticeView',
    component: NoticeView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/notice/:id',
    name: 'NoticeDetailView',
    component: NoticeDetailView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/expirations',
    name: 'Expirations',
    component: Expirations,
    meta: {
      requireLogin: true
    },
  },
  {
    path: '/expirations/:id',
    name: 'ExpirationsDetail',
    component: ExpirationsDetail,
    meta: {
      requireLogin: true
    },
  },
  {
    path: '/help',
    name: 'Help',
    component: Help,
    meta: {
      requireLogin: true
    },
  },
  {
    path: '/help/:id',
    name: 'HelpDetail',
    component: HelpDetail,
    meta: {
      requireLogin: true
    },
  },
  {
    path: '/help/write',
    name: 'HelpWrite',
    component: HelpWrite,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/chat',
    name: 'ChatRoom',
    component: ChatRoom,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/chat/list',
    name: 'ChatList',
    component: ChatListView
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: ResetPassword,
  },
  {
    path: '/find-id',
    name: 'FindId',
    component: FindId,
  },
  {
    path: '/user-dislike',
    name: 'DisLike',
    component: DisLike,
  },
  {
    path: '/user-like',
    name: 'Like',
    component: Like,
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
