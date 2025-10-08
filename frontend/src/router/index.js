import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Task from '../views/Task.vue'
import Startpage from '../views/Start.vue'
import RealStartpage from '../views/RealStart.vue'
import PatchouliKnowledge from '../views/Process.vue'
import SettingsPage from '../views/Settings.vue'  
import CheckAPI from '../views/ApiDocs.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/task',
    name: 'Task',
    component: Task,
    meta:{title:'Task - тμтoяχαv'}
  },
  {
    path: '/start',
    name: 'Start',
    component: Startpage,
    meta:{title:'Start - тμтoяχαv'}
  },
  {
    path: '/realstart',
    name: 'RealStart',
    component: RealStartpage,
    meta:{title:'可删除页面 - тμтoяχαv'}
  },
  {
    path: '/process',
    name: 'PatchouliKnowledge',
    component: PatchouliKnowledge,
    meta:{title:'	パチュリー - тμтoяχαv'}
  },
  {
    path: '/settings',
    name: 'SettingsPage',
    component: SettingsPage,
    meta:{title:'AISettings - тμтoяχαv'} 
  },
  {
    path: '/checkapi',
    name: 'CheckAPI',
    component: CheckAPI,
    meta:{title:'API Docs - тμтoяχαv'}
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Set document title from route meta when navigation completes
const DEFAULT_TITLE = 'тμтoяχαv ряоjест'
router.afterEach((to) => {
  const title = to.meta && to.meta.title ? to.meta.title : DEFAULT_TITLE
  if (title) document.title = title
})

export default router