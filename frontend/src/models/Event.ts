import type { Concert } from './Concert'
import type { Venue } from './Venue'
import type { Festival } from './Festival'
import type { Attendee } from './Attendee'

export interface Event {
  id: number
  name?: string
  event_date: string
  comments: string
  venue_id: number
  festival_id?: number
  venue?: Venue
  festival?: Festival
  concerts: Concert[]
  attendees?: Attendee[]
}

export interface ConcertFormData {
  id: number | null
  artist_id: number | null
  comments: string
  setlist: string
}

export interface EventFormData {
  name: string
  event_date: Date | null
  comments: string
  venue_id: number | null
  festival_id: number | null
  attendees_ids: number[]
  concerts: ConcertFormData[]
}
