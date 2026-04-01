import type { Country } from './Country'

export interface City {
  id: number
  name: string
  country_id: number
  country: Country
}
