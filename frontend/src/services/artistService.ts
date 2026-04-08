import { api } from './api'
import type { Artist } from '@/models/Artist'

export const artistService = {
  getAll: () => api.get<Artist[]>('/artist/'),
  create: (name: string, country_id?: number | null) =>
    api.post<Artist>('/artist/', { name, country_id: country_id ?? null }),
  update: (id: number, name: string, country_id?: number | null) =>
    api.put<Artist>(`/artist/${id}`, { name, country_id: country_id ?? null }),
  delete: (id: number) => api.delete(`/artist/${id}`),
}
