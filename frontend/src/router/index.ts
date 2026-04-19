import { createRouter, createWebHistory } from 'vue-router'
import EventList from '@/views/EventList.vue'
import { isLoggedIn, getStoredUser } from '@/services/authService'

// EventList est chargé eagerly (page d'accueil).
// Toutes les autres vues sont lazy-loaded : Vite les split en chunks séparés
// téléchargés uniquement quand l'utilisateur navigue vers elles.
const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.path === from.path) return false
    return { top: 0 }
  },
  routes: [
    { path: '/login',    component: () => import('@/views/LoginView.vue'),    meta: { public: true } },
    { path: '/',         component: EventList,                                 meta: { public: true } },
    { path: '/event/new',component: EventList,                                 meta: { requiresAuth: true } },
    { path: '/event/:id',component: EventList,                                 meta: { public: true } },
    { path: '/library',  component: () => import('@/views/LibraryView.vue'),  meta: { public: true } },
    { path: '/artists',  component: () => import('@/views/ArtistsView.vue'),  meta: { public: true } },
    { path: '/venues',   component: () => import('@/views/VenuesView.vue'),   meta: { public: true } },
    { path: '/cities',   component: () => import('@/views/CitiesView.vue'),   meta: { public: true } },
    { path: '/countries',component: () => import('@/views/CountriesView.vue'),meta: { public: true } },
    { path: '/attendees',component: () => import('@/views/AttendeesView.vue'),meta: { requiresAuth: true } },
    { path: '/festivals',component: () => import('@/views/FestivalsView.vue'),meta: { public: true } },
    { path: '/stats',    component: () => import('@/views/StatsView.vue'),    meta: { public: true } },
    { path: '/admin',    component: () => import('@/views/AdminView.vue'),    meta: { requiresAuth: true, adminOnly: true } },
    { path: '/import',   component: () => import('@/views/ImportView.vue'),   meta: { requiresAuth: true, adminOnly: true } },
  ],
})

router.beforeEach((to) => {
  if (to.meta.public) return true
  if (!isLoggedIn()) return '/login'
  if (to.meta.adminOnly && !getStoredUser()?.is_admin) return '/'
  return true
})

export default router
