import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Plants from '../views/Plants.vue'
import Sensors from '../views/Sensors.vue'
import Irrigation from '../views/Irrigation.vue'
import Analytics from '../views/Analytics.vue'
import Robotics from '../views/Robotics.vue'
import PathPlanning from '../components/PathPlanning.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/plants',
    name: 'Plants',
    component: Plants
  },
  {
    path: '/sensors',
    name: 'Sensors',
    component: Sensors
  },
  {
    path: '/irrigation',
    name: 'Irrigation',
    component: Irrigation
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: Analytics
  },
  {
    path: '/robotics',
    name: 'Robotics',
    component: Robotics
  },
  {
    path: '/path-planning',
    name: 'PathPlanning',
    component: PathPlanning
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router 