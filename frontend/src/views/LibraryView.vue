<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const sections = [
  { label: 'Artists', icon: 'pi-star', route: '/artists', description: 'Stats & history for every artist you\'ve seen' },
  { label: 'Venues', icon: 'pi-building', route: '/venues', description: 'Events per venue, first & last visits' },
  { label: 'Cities', icon: 'pi-map-marker', route: '/cities', description: 'Cities explored through concerts' },
  { label: 'Countries', icon: 'pi-globe', route: '/countries', description: 'Countries visited for live music' },
  { label: 'People', icon: 'pi-users', route: '/attendees', description: 'Friends who attended concerts with you' },
  { label: 'Festivals', icon: 'pi-ticket', route: '/festivals', description: 'Festival editions & artists seen' },
]
</script>

<template>
  <div>
    <h2 class="text-xl font-bold mb-8 text-gray-900 dark:text-gray-100">Library</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <button
        v-for="s in sections"
        :key="s.route"
        class="text-left p-5 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-violet-400 dark:hover:border-violet-500 hover:shadow-md transition-all group cursor-pointer"
        @click="router.push(s.route)"
      >
        <i :class="`pi ${s.icon} text-2xl text-violet-500 dark:text-violet-400 mb-3 block group-hover:scale-110 transition-transform`" />
        <p class="font-semibold text-gray-900 dark:text-gray-100">{{ s.label }}</p>
        <p class="text-sm text-gray-400 mt-1">{{ s.description }}</p>
      </button>
    </div>
  </div>
</template>
