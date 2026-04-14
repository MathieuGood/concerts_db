import { api } from './api'
import type { Event, ConcertFormData } from '@/models/Event'

export interface EventPayload {
  name?: string
  event_date: string
  comments: string
  venue_id: number
  festival_id?: number
  attendees_ids: number[]
  concerts: {
    id?: number
    artist_id: number
    comments: string
    setlist: string
    photos_ids: number[]
    videos_ids: number[]
  }[]
}

function formatDate(date: Date): string {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

export function buildPayload(
  formData: {
    name: string
    event_date: Date
    comments: string
    venue_id: number
    festival_id: number | null
    attendees_ids: number[]
    concerts: ConcertFormData[]
  }
): EventPayload {
  return {
    name: formData.name || undefined,
    event_date: formatDate(formData.event_date),
    comments: formData.comments,
    venue_id: formData.venue_id,
    festival_id: formData.festival_id ?? undefined,
    attendees_ids: formData.attendees_ids,
    concerts: formData.concerts.map((c) => ({
      id: c.id ?? undefined,
      artist_id: c.artist_id!,
      comments: c.comments,
      setlist: c.setlist,
      i_played: c.i_played,
      photos_ids: [],
      videos_ids: [],
    })),
  }
}

export const eventService = {
  getAll: () => api.get<Event[]>('/event/'),
  getOne: (id: number) => api.get<Event>(`/event/${id}`),
  create: (payload: EventPayload) => api.post<Event>('/event/', payload),
  update: (id: number, payload: EventPayload) => api.put<Event>(`/event/${id}`, payload),
  delete: (id: number) => api.delete(`/event/${id}`),
}
