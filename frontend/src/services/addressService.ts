import { api } from './api'
import type { Address } from '@/models/Address'

export const addressService = {
  getAll: () => api.get<Address[]>('/address/'),
  findOrCreate: async (city: string, country: string): Promise<Address> => {
    const addresses = await api.get<Address[]>('/address/')
    const existing = addresses.find(
      (a) =>
        a.city.trim().toLowerCase() === city.trim().toLowerCase() &&
        a.country.trim().toLowerCase() === country.trim().toLowerCase()
    )
    if (existing) return existing
    return api.post<Address>('/address/', { city: city.trim(), country: country.trim() })
  },
}
