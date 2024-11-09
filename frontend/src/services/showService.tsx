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

export const updateShow = async (id: number, show: Show): Promise<Show> => {
	console.log("Function updateShow")
	console.log("Content of show json sent to API :", show)
	const response = await axios.put(`${API_URL}${route}/${id}`, show)
	return response.data
}
