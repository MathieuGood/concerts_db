import axios from "axios"
import { Concert } from "../models/Concert"

const API_URL = "http://localhost:8000/"
const route = "concert"

export const getConcerts = async (): Promise<Concert[]> => {
	const response = await axios.get(`${API_URL}${route}`)
	return response.data
}

export const getConcert = async (id: number): Promise<Concert> => {
	const response = await axios.get(`${API_URL}${route}/${id}`)
	return response.data
}

export const updateConcert = async (id: number, concert: Concert): Promise<Concert> => {
	const response = await axios.put(`${API_URL}${route}/${id}`, concert, {
		headers: {
			"Content-Type": "application/json"
		}
	})
	console.log("updateConcert RESPONSE :", response.status, response.statusText)
	return response.data
}

export const parseConcertToAPIFormat = (concert: Concert) => {
	console.log("Concert to parse =>", concert)
	const parsedShow = {
		// name: concert.name,
		// event_date: concert.event_date,
		// comments: concert.comments,
		// venue_id: concert.venue.id,
		// festival_id: concert.festival?.id,
		// attendees_ids: concert.attendees?.map(attendee => attendee.id),
		// concerts: concert.concerts.map(concert => {
		// 	return {
		// 		artist_id: concert.artist.id,
		// 		comments: concert.comments,
		// 		setlist: concert.setlist,
		// 		photos: concert.photos.map(photo => photo?.path),
		// 		videos: concert.videos.map(video => video.path)
		// 	}
		// })
	}
	console.log("Parsed show =>", parsedShow)
	return parsedShow
}
