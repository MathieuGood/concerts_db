import { api } from './api'
import type { Venue } from '@/models/Venue'

export const venueService = {
  getAll: () => api.get<Venue[]>('/venue/'),
  create: (name: string, city_id: number) =>
    api.post<Venue>('/venue/', { name, city_id }),
}
