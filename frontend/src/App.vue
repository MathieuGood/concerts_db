<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
import Toast from 'primevue/toast'
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 transition-colors duration-200">
    <AppHeader />
    <main class="max-w-4xl mx-auto px-4 py-6">
      <router-view />
    </main>
    <Toast position="bottom-right" />
  </div>
</template>
