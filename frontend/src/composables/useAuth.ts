import { ref, computed } from 'vue'
import { getStoredUser, clearSession, type User } from '@/services/authService'

const user = ref<User | null>(getStoredUser())

export function useAuth() {
  const isAdmin = computed(() => user.value?.is_admin ?? false)

  function setUser(u: User | null) {
    user.value = u
  }

  function logout() {
    clearSession()
    user.value = null
    window.location.href = '/login'
  }

  return { user, isAdmin, setUser, logout }
}
