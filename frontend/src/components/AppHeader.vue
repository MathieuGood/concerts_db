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
  { icon: 'pi-star',      path: '/artists',   label: 'Artists',   color: 'pink'    },
  { icon: 'pi-building',  path: '/venues',    label: 'Venues',    color: 'cyan'    },
  { icon: 'pi-map-marker',path: '/cities',    label: 'Cities',    color: 'green'   },
  { icon: 'pi-globe',     path: '/countries', label: 'Countries', color: 'orange'  },
  { icon: 'pi-users',     path: '/attendees', label: 'People',    color: 'yellow'  },
  { icon: 'pi-ticket',    path: '/festivals', label: 'Festivals', color: 'red'     },
  { icon: 'pi-chart-bar', path: '/stats',     label: 'Stats',     color: 'comment' },
]
const { user, isAdmin, logout } = useAuth()

const menuOpen = ref(false)

function navigate(path: string) {
  menuOpen.value = false
  router.push(path)
}

function confirmLogout() {
  menuOpen.value = false
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
        class="text-xl text-violet-600 dark:text-violet-400 cursor-pointer"
        style="font-family: 'DepartureMono', monospace;"
        @click="navigate('/')"
      >
        Concerts
      </button>

      <!-- Desktop nav -->
      <div class="hidden sm:flex items-center gap-2">
        <Button
          label="New Event"
          icon="pi pi-plus"
          size="small"
          @click="navigate('/event/new')"
        />

        <Button
          icon="pi pi-calendar"
          size="small"
          rounded
          :text="route.path !== '/'"
          :severity="route.path === '/' ? undefined : 'secondary'"
          @click="navigate('/')"
          aria-label="Shows"
        />

        <Button
          v-for="link in libraryLinks"
          :key="link.path"
          :icon="`pi ${link.icon}`"
          size="small"
          rounded
          :text="route.path !== link.path"
          :severity="route.path === link.path ? undefined : 'secondary'"
          @click="navigate(link.path)"
          :aria-label="link.label"
        />

        <Button
          v-if="isAdmin"
          icon="pi pi-database"
          size="small"
          rounded
          :text="route.path !== '/import'"
          :severity="route.path === '/import' ? undefined : 'secondary'"
          @click="navigate('/import')"
          aria-label="Import / Export"
        />
        <Button
          v-if="isAdmin"
          icon="pi pi-shield"
          size="small"
          rounded
          :text="route.path !== '/admin'"
          :severity="route.path === '/admin' ? undefined : 'secondary'"
          @click="navigate('/admin')"
          aria-label="Admin panel"
        />

        <span v-if="user?.name" class="text-xs text-gray-500 dark:text-gray-400 max-w-[120px] truncate">
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

      <!-- Mobile: theme + burger -->
      <div class="flex sm:hidden items-center gap-1">
        <Button
          :icon="isDark ? 'pi pi-sun' : 'pi pi-moon'"
          size="small"
          rounded
          text
          @click="toggleTheme"
          :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
        />
        <Button
          :icon="menuOpen ? 'pi pi-times' : 'pi pi-bars'"
          size="small"
          rounded
          text
          severity="secondary"
          @click="menuOpen = !menuOpen"
          aria-label="Menu"
        />
      </div>
    </div>

    <!-- Mobile dropdown menu -->
    <div
      v-if="menuOpen"
      class="sm:hidden border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-4 py-3 flex flex-col gap-1"
    >
      <button
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium w-full text-left transition-colors"
        :class="route.path === '/event/new'
          ? 'badge-d-purple'
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'"
        @click="navigate('/event/new')"
      >
        <i class="pi pi-plus text-d-purple" />
        New Event
      </button>

      <button
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium w-full text-left transition-colors"
        :class="route.path === '/'
          ? 'badge-d-purple'
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'"
        @click="navigate('/')"
      >
        <i class="pi pi-calendar" />
        Shows
      </button>

      <button
        v-for="link in libraryLinks"
        :key="link.path"
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium w-full text-left transition-colors"
        :class="route.path === link.path
          ? `badge-d-${link.color}`
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'"
        @click="navigate(link.path)"
      >
        <i :class="`pi ${link.icon}`" />
        {{ link.label }}
      </button>

      <button
        v-if="isAdmin"
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium w-full text-left transition-colors"
        :class="route.path === '/import'
          ? 'badge-d-comment'
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'"
        @click="navigate('/import')"
      >
        <i class="pi pi-database" />
        Import / Export
      </button>

      <button
        v-if="isAdmin"
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium w-full text-left transition-colors"
        :class="route.path === '/admin'
          ? 'badge-d-comment'
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'"
        @click="navigate('/admin')"
      >
        <i class="pi pi-shield" />
        Admin
      </button>

      <div class="border-t border-gray-200 dark:border-gray-700 mt-1 pt-2 flex items-center justify-between">
        <span v-if="user?.name" class="text-xs text-gray-500 dark:text-gray-400 truncate">
          {{ user.name }}
        </span>
        <button
          class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors ml-auto"
          @click="confirmLogout"
        >
          <i class="pi pi-sign-out" />
          Sign out
        </button>
      </div>
    </div>
  </header>
</template>
