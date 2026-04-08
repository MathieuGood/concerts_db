<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Button from 'primevue/button'
import { useConfirm } from 'primevue/useconfirm'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const route = useRoute()
const confirm = useConfirm()

const libraryLinks = [
  { icon: 'pi-star', path: '/artists', label: 'Artists' },
  { icon: 'pi-building', path: '/venues', label: 'Venues' },
  { icon: 'pi-map-marker', path: '/cities', label: 'Cities' },
  { icon: 'pi-globe', path: '/countries', label: 'Countries' },
  { icon: 'pi-users', path: '/attendees', label: 'People' },
  { icon: 'pi-ticket', path: '/festivals', label: 'Festivals' },
]
const { user, isAdmin, logout } = useAuth()

function confirmLogout() {
  confirm.require({
    message: 'Are you sure you want to sign out?',
    header: 'Sign out',
    icon: 'pi pi-sign-out',
    rejectLabel: 'Cancel',
    acceptLabel: 'Sign out',
    accept: logout,
  })
}
const isDark = ref(false)

function toggleTheme() {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

onMounted(() => {
  const saved = localStorage.getItem('theme')
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  isDark.value = saved ? saved === 'dark' : mediaQuery.matches
  if (isDark.value) document.documentElement.classList.add('dark')
  mediaQuery.addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      isDark.value = e.matches
      document.documentElement.classList.toggle('dark', e.matches)
    }
  })
})
</script>

<template>
  <header class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-50">
    <div class="max-w-4xl mx-auto px-4 h-14 flex items-center justify-between">
      <button
        class="text-lg font-bold text-violet-600 dark:text-violet-400 tracking-tight cursor-pointer"
        @click="router.push('/')"
      >
        🎸 Concerts
      </button>

      <div class="flex items-center gap-2">
        <Button
          label="New Event"
          icon="pi pi-plus"
          size="small"
          @click="router.push('/event/new')"
        />

        <Button
          v-for="link in libraryLinks"
          :key="link.path"
          :icon="`pi ${link.icon}`"
          size="small"
          rounded
          :text="route.path !== link.path"
          :severity="route.path === link.path ? undefined : 'secondary'"
          @click="router.push(link.path)"
          :aria-label="link.label"
        />

        <Button
          v-if="isAdmin"
          icon="pi pi-users"
          size="small"
          rounded
          text
          @click="router.push('/admin')"
          aria-label="Admin panel"
        />

        <span v-if="user?.name" class="hidden sm:block text-xs text-gray-500 dark:text-gray-400 max-w-[120px] truncate">
          {{ user.name }}
        </span>

        <Button
          icon="pi pi-sign-out"
          size="small"
          rounded
          text
          severity="secondary"
          @click="confirmLogout"
          aria-label="Sign out"
        />

        <Button
          :icon="isDark ? 'pi pi-sun' : 'pi pi-moon'"
          size="small"
          rounded
          text
          @click="toggleTheme"
          :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
        />
      </div>
    </div>
  </header>
</template>
