<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Checkbox from 'primevue/checkbox'
import { adminService, type CreateUserPayload } from '@/services/adminService'
import type { User } from '@/services/authService'
import { useAuth } from '@/composables/useAuth'

const { user: currentUser } = useAuth()
const users = ref<User[]>([])
const loading = ref(false)
const error = ref('')
const success = ref('')

const form = ref<CreateUserPayload>({ email: '', password: '', is_admin: false })
const creating = ref(false)

async function fetchUsers() {
  loading.value = true
  try {
    users.value = await adminService.getUsers()
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : 'Failed to load users'
  } finally {
    loading.value = false
  }
}

async function createUser() {
  error.value = ''
  success.value = ''
  creating.value = true
  try {
    await adminService.createUser(form.value)
    form.value = { email: '', password: '', is_admin: false }
    success.value = 'User created.'
    await fetchUsers()
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : 'Failed to create user'
  } finally {
    creating.value = false
  }
}

async function deleteUser(id: number) {
  if (!confirm('Delete this user?')) return
  error.value = ''
  try {
    await adminService.deleteUser(id)
    await fetchUsers()
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : 'Failed to delete user'
  }
}

onMounted(fetchUsers)
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <h2 class="text-xl font-bold mb-6 text-gray-900 dark:text-gray-100">User Management</h2>

    <div v-if="error" class="mb-4 text-sm text-red-500">{{ error }}</div>
    <div v-if="success" class="mb-4 text-sm text-green-600">{{ success }}</div>

    <!-- User list -->
    <div class="bg-white dark:bg-gray-900 rounded-xl shadow divide-y divide-gray-100 dark:divide-gray-800 mb-8">
      <div v-if="loading" class="p-4 text-gray-500 text-sm">Loading…</div>
      <div
        v-for="u in users"
        :key="u.id"
        class="flex items-center justify-between px-4 py-3"
      >
        <div>
          <span class="font-medium text-gray-800 dark:text-gray-200">{{ u.email }}</span>
          <span v-if="u.is_admin" class="ml-2 text-xs bg-violet-100 dark:bg-violet-900 text-violet-700 dark:text-violet-300 px-2 py-0.5 rounded-full">admin</span>
          <div class="text-xs text-gray-400">{{ new Date(u.created_at).toLocaleDateString() }}</div>
        </div>
        <Button
          icon="pi pi-trash"
          text
          rounded
          severity="danger"
          size="small"
          :disabled="u.id === currentUser?.id"
          @click="deleteUser(u.id)"
          aria-label="Delete user"
        />
      </div>
    </div>

    <!-- Create user -->
    <div class="bg-white dark:bg-gray-900 rounded-xl shadow p-6">
      <h3 class="text-base font-semibold mb-4 text-gray-800 dark:text-gray-200">Invite a user</h3>
      <form @submit.prevent="createUser" class="flex flex-col gap-3">
        <InputText v-model="form.email" type="email" placeholder="Email" required class="w-full" />
        <Password v-model="form.password" :feedback="false" toggleMask placeholder="Password" required class="w-full" inputClass="w-full" />
        <div class="flex items-center gap-2">
          <Checkbox v-model="form.is_admin" binary inputId="is_admin" />
          <label for="is_admin" class="text-sm text-gray-700 dark:text-gray-300">Admin</label>
        </div>
        <Button type="submit" label="Create user" :loading="creating" class="mt-2" />
      </form>
    </div>
  </div>
</template>
