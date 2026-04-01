import { api } from './api'
import type { Festival } from '@/models/Festival'

export const festivalService = {
  getAll: () => api.get<Festival[]>('/festival/'),
  create: (name: string) => api.post<Festival>('/festival/', { name }),
}
