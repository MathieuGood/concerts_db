import { api } from './api'
import type { Artist } from '@/models/Artist'

export const artistService = {
  getAll: () => api.get<Artist[]>('/artist/'),
  create: (name: string, country_id?: number | null) =>
    api.post<Artist>('/artist/', { name, country_id: country_id ?? null }),
}
