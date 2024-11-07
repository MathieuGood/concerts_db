import axios from "axios"
import { Show } from "../models/Show"

const API_URL = "http://localhost:8000/"
const route = "show"

export const getShows = async (): Promise<Show[]> => {
	console.log("getShows")
	const response = await axios.get(`${API_URL}${route}`)
	return response.data
}
