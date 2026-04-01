import type { City } from './City'

export interface Venue {
  id: number
  name: string
  city_id: number
  city?: City
}
