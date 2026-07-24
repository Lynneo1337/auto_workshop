import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ClientDashboard from '../views/ClientDashboard.vue'
import HomeView from '../views/HomeView.vue'
import ServicesView from '../views/ServicesView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import BookingView from '../views/BookingView.vue'
import MechanicDashboard from '../views/MechanicDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView
  },
  {
    path: '/services',
    name: 'Services',
    component: ServicesView
  },
  {
    path: '/dashboard',
    name: 'ClientDashboard',
    component: ClientDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' } // <-- Новая мета-информация
  },
  {
    path: '/booking',
    name: 'Booking',
    component: BookingView,
    meta: { requiresAuth: true }
  },
  {
    path: '/mechanic',
    name: 'MechanicDashboard',
    component: MechanicDashboard,
    meta: { requiresAuth: true, role: 'mechanic' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.role && role !== to.meta.role) {
    next('/')
  } else {
    next()
  }
})

export default router