import { api } from './api'
import type { Country } from '@/models/Country'

export const countryService = {
  getAll: () => api.get<Country[]>('/country/'),
  create: (name: string) => api.post<Country>('/country/', { name }),
  update: (id: number, name: string) => api.put<Country>(`/country/${id}`, { name }),
  delete: (id: number) => api.delete(`/country/${id}`),
  async findOrCreate(name: string): Promise<Country> {
    const all = await countryService.getAll()
    const found = all.find((c) => c.name.toLowerCase() === name.toLowerCase())
    return found ?? (await countryService.create(name))
  },
}
