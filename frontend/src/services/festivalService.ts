import { api } from './api'
import type { Festival } from '@/models/Festival'

export const festivalService = {
  getAll: () => api.get<Festival[]>('/festival/'),
  create: (name: string) => api.post<Festival>('/festival/', { name }),
  update: (id: number, name: string) => api.put<Festival>(`/festival/${id}`, { name }),
  delete: (id: number) => api.delete(`/festival/${id}`),
}
