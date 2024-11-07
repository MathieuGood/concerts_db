import axios from "axios"

const API_URL = "http://localhost:8000"

/**
 * Fetches all the shows.
 * @returns {Promise<any>} A promise that resolves to the fetched shows data.
 */
export const fetchShows = async (): Promise<any> => {
    const response = await axios.get(`${API_URL}/show/`)
    return response.data
}

/**
 * Fetches a show by its ID.
 *
 * @param id - The ID of the show to fetch.
 * @returns {Promise<any>} A Promise that resolves to the data of the fetched show.
 */
export const fetchShow = async (id: number): Promise<any> => {
    const response = await axios.get(`${API_URL}/show/${id}`)
    return response.data
}
