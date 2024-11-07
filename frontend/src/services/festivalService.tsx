import axios from "axios"
import { Festival } from "../models/Festival"

const API_URL = "http://localhost:8000/"
const route = "festival"

export const getFestivals = async (): Promise<Festival[]> => {
	const response = await axios.get(`${API_URL}${route}`)
	return response.data
}

export const getFestival = async (id: number): Promise<Festival> => {
	const response = await axios.get(`${API_URL}${route}/${id}`)
	return response.data
}
