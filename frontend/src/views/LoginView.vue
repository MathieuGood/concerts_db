<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import { login, saveSession } from '@/services/authService'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { setUser } = useAuth()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const data = await login(email.value, password.value)
    saveSession(data)
    setUser(data.user)
    router.push('/')
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 px-4">
    <div class="w-full max-w-sm bg-white dark:bg-gray-900 rounded-2xl shadow p-8">
      <h1 class="text-2xl font-bold text-violet-600 dark:text-violet-400 mb-6 text-center">🎸 Concerts</h1>

      <form @submit.prevent="submit" class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
          <InputText v-model="email" type="email" placeholder="you@example.com" class="w-full" autocomplete="email" required />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
          <Password v-model="password" :feedback="false" toggleMask class="w-full" inputClass="w-full" placeholder="••••••••" required />
        </div>

        <p v-if="error" class="text-sm text-red-500">{{ error }}</p>

        <Button type="submit" label="Sign in" :loading="loading" class="w-full mt-2" />
      </form>
    </div>
  </div>
</template>
