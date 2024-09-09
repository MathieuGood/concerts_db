import axios from "axios"

const API_URL = "http://localhost:8000"

export const fetchShows = async () => {
    const response = await axios.get(`${API_URL}/show/`)
    return response.data
}
