import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import reliability from "@/views/Reliability";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'LMT toolkit - Reliability'
    }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
    meta: {
      title: 'LMT toolkit - Reliability'
    }
  },
  {
    path: '/reliability',
    name: 'reliability',
    component: reliability,
    meta: {
      title: 'LMT toolkit - Reliability'
    }
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
