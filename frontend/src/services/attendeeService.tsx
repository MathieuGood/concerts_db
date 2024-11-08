import axios from "axios"
import { Attendee } from "../models/Attendee"

const API_URL = "http://localhost:8000/"
const route = "attendee"

export const getAttendees = async (): Promise<Attendee[]> => {
	const response = await axios.get(`${API_URL}${route}`)
	return response.data
}

export const getAttendee = async (id: number): Promise<Attendee> => {
	const response = await axios.get(`${API_URL}${route}/${id}`)
	return response.data
}
