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
