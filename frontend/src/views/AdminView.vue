<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Checkbox from 'primevue/checkbox'
import { adminService, type CreateUserPayload } from '@/services/adminService'
import { changePassword } from '@/services/authService'
import type { User } from '@/services/authService'
import { useAuth } from '@/composables/useAuth'

const { user: currentUser } = useAuth()
const users = ref<User[]>([])
const loading = ref(false)
const error = ref('')
const success = ref('')

const form = ref<CreateUserPayload>({ email: '', password: '', name: '', is_admin: false })
const creating = ref(false)

// Reset password state per user
const resetingId = ref<number | null>(null)
const resetPassword = ref('')
const resetError = ref('')
const resetSuccess = ref('')

// Change own password
const changeForm = ref({ current: '', next: '', confirm: '' })
const changing = ref(false)
const changeError = ref('')
const changeSuccess = ref('')

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
    form.value = { email: '', password: '', name: '', is_admin: false }
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

function startReset(id: number) {
  resetingId.value = id
  resetPassword.value = ''
  resetError.value = ''
  resetSuccess.value = ''
}

function cancelReset() {
  resetingId.value = null
  resetPassword.value = ''
}

async function submitReset(id: number) {
  resetError.value = ''
  resetSuccess.value = ''
  if (!resetPassword.value) { resetError.value = 'Password required.'; return }
  try {
    await adminService.resetUserPassword(id, resetPassword.value)
    resetSuccess.value = 'Password updated.'
    resetingId.value = null
    resetPassword.value = ''
  } catch (e: unknown) {
    resetError.value = e instanceof Error ? e.message : 'Failed to reset password'
  }
}

async function submitChangePassword() {
  changeError.value = ''
  changeSuccess.value = ''
  if (changeForm.value.next !== changeForm.value.confirm) {
    changeError.value = 'New passwords do not match.'
    return
  }
  changing.value = true
  try {
    await changePassword(changeForm.value.current, changeForm.value.next)
    changeForm.value = { current: '', next: '', confirm: '' }
    changeSuccess.value = 'Password changed successfully.'
  } catch (e: unknown) {
    changeError.value = e instanceof Error ? e.message : 'Failed to change password'
  } finally {
    changing.value = false
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
        class="px-4 py-3"
      >
        <div class="flex items-center justify-between">
          <div>
            <span class="font-medium text-gray-800 dark:text-gray-200">{{ u.name ?? u.email }}</span>
          <span v-if="u.name" class="ml-2 text-xs text-gray-400">{{ u.email }}</span>
            <span v-if="u.is_admin" class="ml-2 text-xs bg-violet-100 dark:bg-violet-900 text-violet-700 dark:text-violet-300 px-2 py-0.5 rounded-full">admin</span>
            <div class="text-xs text-gray-400">{{ new Date(u.created_at).toLocaleDateString() }}</div>
          </div>
          <div class="flex items-center gap-1">
            <Button
              icon="pi pi-key"
              text
              rounded
              severity="secondary"
              size="small"
              @click="resetingId === u.id ? cancelReset() : startReset(u.id)"
              aria-label="Reset password"
            />
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

        <!-- Inline reset password form -->
        <div v-if="resetingId === u.id" class="mt-3 flex flex-col gap-2">
          <div v-if="resetError" class="text-xs text-red-500">{{ resetError }}</div>
          <div v-if="resetSuccess" class="text-xs text-green-600">{{ resetSuccess }}</div>
          <div class="flex gap-2 items-center">
            <Password v-model="resetPassword" :feedback="false" toggleMask placeholder="New password" class="flex-1" inputClass="w-full" />
            <Button label="Save" size="small" @click="submitReset(u.id)" />
            <Button label="Cancel" size="small" severity="secondary" text @click="cancelReset()" />
          </div>
        </div>
      </div>
    </div>

    <!-- Create user -->
    <div class="bg-white dark:bg-gray-900 rounded-xl shadow p-6 mb-6">
      <h3 class="text-base font-semibold mb-4 text-gray-800 dark:text-gray-200">Invite a user</h3>
      <form @submit.prevent="createUser" class="flex flex-col gap-3">
        <InputText v-model="form.name" placeholder="Name" class="w-full" />
        <InputText v-model="form.email" type="email" placeholder="Email" required class="w-full" />
        <Password v-model="form.password" :feedback="false" toggleMask placeholder="Password" required class="w-full" inputClass="w-full" />
        <div class="flex items-center gap-2">
          <Checkbox v-model="form.is_admin" binary inputId="is_admin" />
          <label for="is_admin" class="text-sm text-gray-700 dark:text-gray-300">Admin</label>
        </div>
        <Button type="submit" label="Create user" :loading="creating" class="mt-2" />
      </form>
    </div>

    <!-- Change my password -->
    <div class="bg-white dark:bg-gray-900 rounded-xl shadow p-6">
      <h3 class="text-base font-semibold mb-4 text-gray-800 dark:text-gray-200">Change my password</h3>
      <div v-if="changeError" class="mb-3 text-sm text-red-500">{{ changeError }}</div>
      <div v-if="changeSuccess" class="mb-3 text-sm text-green-600">{{ changeSuccess }}</div>
      <form @submit.prevent="submitChangePassword" class="flex flex-col gap-3">
        <Password v-model="changeForm.current" :feedback="false" toggleMask placeholder="Current password" required class="w-full" inputClass="w-full" />
        <Password v-model="changeForm.next" :feedback="false" toggleMask placeholder="New password" required class="w-full" inputClass="w-full" />
        <Password v-model="changeForm.confirm" :feedback="false" toggleMask placeholder="Confirm new password" required class="w-full" inputClass="w-full" />
        <Button type="submit" label="Change password" :loading="changing" class="mt-2" />
      </form>
    </div>
  </div>
</template>
