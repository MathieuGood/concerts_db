import axios from "axios"
import { Artist } from "../models/Artist"

const API_URL = "http://localhost:8000/"
const route = "artist"

export const getArtists = async (): Promise<Artist[]> => {
	const response = await axios.get(`${API_URL}${route}`)
	return response.data.data
}

export const getArtist = async (id: number): Promise<Artist> => {
	const response = await axios.get(`${API_URL}${route}/${id}`)
	return response.data.data
}
