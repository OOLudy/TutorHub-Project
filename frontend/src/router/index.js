import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Task from '../views/Task.vue'
import Startpage from '../views/Start.vue'
import RealStartpage from '../views/RealStart.vue'
import PatchouliKnowledge from '../views/Process.vue'
import SettingsPage from '../views/Settings.vue'  

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
  },
  {
    path: '/process',
    name: 'PatchouliKnowledge',
    component: PatchouliKnowledge
  },
  {
    path: '/settings',
    name: 'SettingsPage',
    component: SettingsPage 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router