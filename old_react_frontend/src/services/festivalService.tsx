import axios from "axios"
import { Festival } from "../models/Festival"

const API_URL = "http://localhost:8000/"
const route = "festival"

export const getFestivals = async (): Promise<Festival[]> => {
	const response = await axios.get(`${API_URL}${route}`)
	return response.data.data
}

export const getFestival = async (id: number): Promise<Festival> => {
	const response = await axios.get(`${API_URL}${route}/${id}`)
	return response.data.data
}

export const updateFestival = async (festival: Festival): Promise<Festival> => {
	const response = await axios.put(
		`${API_URL}${route}/${festival.id}`,
		{ name: festival.name },
		{
			headers: {
				"Content-Type": "application/json"
			}
		}
	)
	console.log("updateFestival RESPONSE :", response.status, response.statusText)
	return response.data.data
}

export const createFestival = async (festival: Festival): Promise<Festival> => {
	const response = await axios.post(
		`${API_URL}${route}`,
		{ name: festival.name },
		{
			headers: {
				"Content-Type": "application/json"
			}
		}
	)
	console.log("createFestival RESPONSE :", response.status, response.statusText)
	return response.data.data
}

export const deleteFestival = async (festival: Festival): Promise<Festival> => {
	const response = await axios.delete(`${API_URL}${route}/${festival.id}`, {
		headers: {
			"Content-Type": "application/json"
		}
	})
	console.log("deleteFestival RESPONSE :", response.status, response.statusText)
	return response.data.data
}
