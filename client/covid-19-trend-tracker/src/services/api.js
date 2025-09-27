import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL

const ApiService = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
})

export const get = async function(url, params) {
    const response = await ApiService.get(url, { params })
    return response.data
}
