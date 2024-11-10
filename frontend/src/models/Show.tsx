// src/models/Show.ts
import { Venue } from "./Venue"
import { Concert } from "./Concert"
import { Attendee } from "./Attendee"
import { Festival } from "./Festival"

export interface Show {
	id: number
	name?: string
	event_date: string
	venue_id: number
	venue: Venue
	concerts: Concert[]
	attendees?: Attendee[]
	comments?: string
	festival_id?: number | null
	festival?: Festival | null
}
