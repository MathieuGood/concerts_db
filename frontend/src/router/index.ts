import { createRouter, createWebHistory } from 'vue-router'
import EventList from '@/views/EventList.vue'
import EventForm from '@/views/EventForm.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: EventList },
    { path: '/event/new', component: EventForm },
    { path: '/event/:id', component: EventForm },
  ],
})

export default router
