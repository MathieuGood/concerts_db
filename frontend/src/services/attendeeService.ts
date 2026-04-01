import { api } from './api'
import type { Attendee } from '@/models/Attendee'

export const attendeeService = {
  getAll: () => api.get<Attendee[]>('/attendee/'),
  create: (firstname: string, lastname?: string) =>
    api.post<Attendee>('/attendee/', { firstname, lastname: lastname || null }),
}
