import { createRouter, createWebHistory } from 'vue-router'
import EventList from '@/views/EventList.vue'
import EventForm from '@/views/EventForm.vue'
import LoginView from '@/views/LoginView.vue'
import AdminView from '@/views/AdminView.vue'
import { isLoggedIn, getStoredUser } from '@/services/authService'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: LoginView, meta: { public: true } },
    { path: '/', component: EventList },
    { path: '/event/new', component: EventForm },
    { path: '/event/:id', component: EventForm },
    { path: '/admin', component: AdminView },
  ],
})

router.beforeEach((to) => {
  if (to.meta.public) return true
  if (!isLoggedIn()) return '/login'
  if (to.path === '/admin') {
    const user = getStoredUser()
    if (!user?.is_admin) return '/'
  }
  return true
})

export default router
