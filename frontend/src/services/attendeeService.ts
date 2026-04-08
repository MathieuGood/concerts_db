import { api } from './api'
import type { Attendee } from '@/models/Attendee'

export const attendeeService = {
  getAll: () => api.get<Attendee[]>('/attendee/'),
  create: (firstname: string, lastname?: string) =>
    api.post<Attendee>('/attendee/', { firstname, lastname: lastname || null }),
  update: (id: number, firstname: string, lastname?: string | null) =>
    api.put<Attendee>(`/attendee/${id}`, { firstname, lastname: lastname || null }),
  delete: (id: number) => api.delete(`/attendee/${id}`),
}
