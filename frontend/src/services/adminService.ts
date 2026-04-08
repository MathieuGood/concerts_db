import { api } from './api'
import type { User } from './authService'

export interface CreateUserPayload {
  email: string
  password: string
  is_admin: boolean
}

export const adminService = {
  getUsers: () => api.get<User[]>('/admin/users'),
  createUser: (payload: CreateUserPayload) => api.post<User>('/admin/users', payload),
  deleteUser: (id: number) => api.delete(`/admin/users/${id}`),
  resetUserPassword: (id: number, new_password: string) =>
    api.put<User>(`/admin/users/${id}/password`, { new_password }),
}
