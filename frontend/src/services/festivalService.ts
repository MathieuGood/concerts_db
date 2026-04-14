import { api } from './api'
import type { Festival } from '@/models/Festival'

export const festivalService = {
  getAll: () => api.get<Festival[]>('/festival/'),
  create: (name: string, year?: number | null) => api.post<Festival>('/festival/', { name, year: year ?? null }),
  update: (id: number, name: string, year?: number | null) => api.put<Festival>(`/festival/${id}`, { name, year: year ?? null }),
  delete: (id: number) => api.delete(`/festival/${id}`),
}
