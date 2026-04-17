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
    return { top: 0 }
  },
  routes: [
    { path: '/login', component: LoginView, meta: { public: true } },
    { path: '/', component: EventList },
    { path: '/event/new', component: EventForm },
    { path: '/event/:id', component: EventForm },
    { path: '/library', component: LibraryView },
    { path: '/artists', component: ArtistsView },
    { path: '/venues', component: VenuesView },
    { path: '/cities', component: CitiesView },
    { path: '/countries', component: CountriesView },
    { path: '/attendees', component: AttendeesView },
    { path: '/festivals', component: FestivalsView },
    { path: '/stats', component: StatsView },
    { path: '/admin', component: AdminView },
    { path: '/import', component: ImportView },
  ],
})

router.beforeEach((to) => {
  if (to.meta.public) return true
  if (!isLoggedIn()) return '/login'
  if (to.path === '/admin' || to.path === '/import') {
    const user = getStoredUser()
    if (!user?.is_admin) return '/'
  }
  return true
})

export default router
