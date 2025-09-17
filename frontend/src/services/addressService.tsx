import axios from "axios"
import { Address } from "../models/Address"

const API_URL = "http://localhost:8000/"
const route = "address"

export const getAddresses = async (): Promise<Address[]> => {
	const response = await axios.get(`${API_URL}${route}`)
	return response.data
}

export const getAddress = async (id: number): Promise<Address> => {
	const response = await axios.get(`${API_URL}${route}/${id}`)
	return response.data
}

export const createAddress = async (address: Address): Promise<Address> => {
	const response = await axios.post(`${API_URL}${route}`, address)
	return response.data
}

export const updateAddress = async (address: Address): Promise<Address> => {
	const response = await axios.put(`${API_URL}${route}/${address.id}`, address)
	return response.data
}

export const deleteAddress = async (id: number): Promise<Address> => {
	const response = await axios.delete(`${API_URL}${route}/${id}`)
	return response.data
}
