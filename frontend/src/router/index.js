/*
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
*/

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Reliability from "@/views/Reliability";
import Results from "@/views/Results";
import VersionHistory from "@/views/VersionHistory";
import Documentation from "@/views/Documentation";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'LMT toolkit - Analysis'
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
      title: 'LMT toolkit'
    }
  },
  {
    path: '/reliability',
    name: 'reliability',
    component: Reliability,
    meta: {
      title: 'LMT toolkit'
    }
  },
  {
    path: '/results',
    name: 'results',
    component: Results,
    meta: {
      title: 'LMT toolkit'
    }
  },
  {
    path: '/versions',
    name: 'versions',
    component: VersionHistory,
    meta: {
      title: 'LMT toolkit'
    }
  },
  {
    path: '/documentation',
    name: 'documentation',
    component: Documentation,
    meta: {
      title: 'LMT toolkit'
    }
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
