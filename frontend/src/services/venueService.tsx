import axios from "axios"
import { Venue } from "../models/Venue"

const API_URL = "http://localhost:8000/"
const route = "venue"

export const getVenues = async (): Promise<Venue[]> => {
	const response = await axios.get(`${API_URL}${route}`)
	return response.data
}

export const getVenue = async (id: number): Promise<Venue> => {
	const response = await axios.get(`${API_URL}${route}/${id}`)
	return response.data
}
