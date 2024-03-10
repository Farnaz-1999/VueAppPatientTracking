import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import HomePage from '../views/HomePage.vue'
import login from '../views/login.vue'
import patients from '../views/patients.vue'  
import patientA from '../views/patientA.vue'
import location from '../views/location.vue'
import register from '../views/register.vue'
import setting from '../views/setting.vue'
import notifs from '../views/notifs.vue'
import data from '../views/data.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/home',
    name: 'Home',
    component: HomePage
  },
  { 
    path: '/login',
    component: login 
  },
  { 
    path: '/dashboard', 
    component: patients 
  },
  { 
    path: '/person',
    component: patientA 
  },
  { 
    path: '/location', 
    component: location 
  },
  { 
    path: '/register', 
    component: register 
  }
  ,
  { 
    path: '/setting', 
    component: setting 
  },
  { 
    path: '/notifications', 
    component: notifs 
  },
  { 
    path: '/data', 
    component: data 
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
