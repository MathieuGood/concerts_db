import { api } from './api'
import type { City } from '@/models/City'

export const cityService = {
  getAll: (country_id?: number) =>
    api.get<City[]>(country_id ? `/city/?country_id=${country_id}` : '/city/'),
  create: (name: string, country_id: number) =>
    api.post<City>('/city/', { name, country_id }),
  update: (id: number, name: string, country_id: number) =>
    api.put<City>(`/city/${id}`, { name, country_id }),
  delete: (id: number) => api.delete(`/city/${id}`),
  async findOrCreate(name: string, country_id: number): Promise<City> {
    const all = await cityService.getAll(country_id)
    const found = all.find((c) => c.name.toLowerCase() === name.toLowerCase())
    return found ?? (await cityService.create(name, country_id))
  },
}
