import type { Country } from './Country'

export interface Artist {
  id: number
  name: string
  country_id?: number | null
  country?: Country | null
}
