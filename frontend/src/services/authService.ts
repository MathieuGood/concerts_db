const BASE_URL = '/api'

export interface User {
  id: number
  email: string
  name: string | null
  is_admin: boolean
  created_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  const json = await response.json()
  if (!response.ok || !json.success) {
    throw new Error(json.message ?? 'Login failed')
  }
  return json.data as LoginResponse
}

export function saveSession(data: LoginResponse) {
  localStorage.setItem('access_token', data.access_token)
  localStorage.setItem('user', JSON.stringify(data.user))
}

export function clearSession() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
}

export function getStoredUser(): User | null {
  const raw = localStorage.getItem('user')
  return raw ? (JSON.parse(raw) as User) : null
}

export function isLoggedIn(): boolean {
  return !!localStorage.getItem('access_token')
}

export async function changePassword(current_password: string, new_password: string): Promise<void> {
  const token = localStorage.getItem('access_token')
  const response = await fetch(`${BASE_URL}/auth/change-password`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({ current_password, new_password }),
  })
  const json = await response.json()
  if (!response.ok || !json.success) {
    throw new Error(json.message ?? 'Failed to change password')
  }
}
