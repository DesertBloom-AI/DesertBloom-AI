import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import PathPlanningExample from '@/views/PathPlanningExample.vue'
import Home from '@/views/Home.vue'
import NotFound from '@/views/NotFound.vue'
import Prototype from '@/components/Prototype.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/path-planning',
    name: 'PathPlanning',
    component: () => import('@/components/PathPlanning.vue'),
    meta: {
      title: 'Path Planning',
      requiresAuth: true
    }
  },
  {
    path: '/path-planning/example',
    name: 'PathPlanningExample',
    component: PathPlanningExample,
    meta: {
      title: 'Path Planning Example'
    }
  },
  {
    path: '/prototype',
    name: 'prototype',
    component: Prototype,
    meta: {
      title: 'Prototype'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Update document title
router.beforeEach((to, from, next) => {
  document.title = to.meta.title
    ? `${to.meta.title} - DesertBloom AI`
    : 'DesertBloom AI'
  next()
})

export default router 