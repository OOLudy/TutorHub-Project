import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Task from '../views/Task.vue'
import Startpage from '../views/Start.vue'
import RealStartpage from '../views/RealStart.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/task',
    name: 'Task',
    component: Task
  },
  {
    path: '/start',
    name: 'Start',
    component: Startpage
  },
  {
    path: '/realstart',
    name: 'RealStart',
    component: RealStartpage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router