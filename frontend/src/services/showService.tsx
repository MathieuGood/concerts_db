import axios from "axios"
import { Show } from "../models/Show"

const API_URL = "http://localhost:8000/"
const route = "show"

export const getShows = async (): Promise<Show[]> => {
	const response = await axios.get(`${API_URL}${route}`)
	return response.data
}

export const getShow = async (id: number): Promise<Show> => {
	const response = await axios.get(`${API_URL}${route}/${id}`)
	return response.data
}

export const updateShow = async (show: Show): Promise<Show> => {
	const response = await axios.put(`${API_URL}${route}/${show.id}`, parseShowToAPIFormat(show), {
		headers: {
			"Content-Type": "application/json"
		}
	})
	console.log("updateShow RESPONSE :", response.status, response.statusText)
	return response.data
}

export const parseShowToAPIFormat = (show: Show) => {
	const parsedShow = {
		name: show.name,
		event_date: show.event_date,
		comments: show.comments,
		venue_id: show.venue.id,
		festival_id: show.festival?.id,
		attendees_ids: show.attendees?.map(attendee => attendee.id),
		concerts: show.concerts.map(concert => {
			return {
				id: concert.id,
				artist_id: concert.artist.id,
				comments: concert.comments,
				setlist: concert.setlist,
				photos_ids: concert.photos.map(photo => photo?.id),
				videos_ids: concert.videos.map(video => video.id)
			}
		})
	}
	console.log("Parsed show =>", parsedShow)
	return parsedShow
}


