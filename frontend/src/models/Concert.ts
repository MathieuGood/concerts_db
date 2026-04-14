import type { Artist } from './Artist'

export interface Concert {
  id: number
  event_id: number
  artist_id: number
  artist?: Artist
  comments: string
  setlist?: string
  i_played?: boolean
}
