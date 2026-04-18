import { createRouter, createWebHistory } from 'vue-router'
import EventList from '@/views/EventList.vue'
import EventForm from '@/views/EventForm.vue'
import LoginView from '@/views/LoginView.vue'
import AdminView from '@/views/AdminView.vue'
import LibraryView from '@/views/LibraryView.vue'
import ArtistsView from '@/views/ArtistsView.vue'
import VenuesView from '@/views/VenuesView.vue'
import CitiesView from '@/views/CitiesView.vue'
import CountriesView from '@/views/CountriesView.vue'
import AttendeesView from '@/views/AttendeesView.vue'
import FestivalsView from '@/views/FestivalsView.vue'
import StatsView from '@/views/StatsView.vue'
import ImportView from '@/views/ImportView.vue'
import { isLoggedIn, getStoredUser } from '@/services/authService'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    // Same path, only query changed (list state sync on expand/search) — keep scroll
    if (to.path === from.path) return false
    return { top: 0 }
  },
  routes: [
    { path: '/login', component: LoginView, meta: { public: true } },
    { path: '/', component: EventList, meta: { public: true } },
    { path: '/event/new', component: EventForm, meta: { requiresAuth: true } },
    { path: '/event/:id', component: EventForm, meta: { public: true } },
    { path: '/library', component: LibraryView, meta: { public: true } },
    { path: '/artists', component: ArtistsView, meta: { public: true } },
    { path: '/venues', component: VenuesView, meta: { public: true } },
    { path: '/cities', component: CitiesView, meta: { public: true } },
    { path: '/countries', component: CountriesView, meta: { public: true } },
    { path: '/attendees', component: AttendeesView, meta: { requiresAuth: true } },
    { path: '/festivals', component: FestivalsView, meta: { public: true } },
    { path: '/stats', component: StatsView, meta: { public: true } },
    { path: '/admin', component: AdminView, meta: { requiresAuth: true, adminOnly: true } },
    { path: '/import', component: ImportView, meta: { requiresAuth: true, adminOnly: true } },
  ],
})

router.beforeEach((to) => {
  if (to.meta.public) return true
  if (!isLoggedIn()) return '/login'
  if (to.meta.adminOnly && !getStoredUser()?.is_admin) return '/'
  return true
})

export default router
