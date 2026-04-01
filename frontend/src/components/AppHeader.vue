<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'

const router = useRouter()
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
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  isDark.value = saved ? saved === 'dark' : prefersDark
  if (isDark.value) document.documentElement.classList.add('dark')
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
          class="hidden sm:flex"
        />
        <Button
          icon="pi pi-plus"
          size="small"
          rounded
          @click="router.push('/event/new')"
          class="sm:hidden"
          aria-label="New event"
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
