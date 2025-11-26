import axios from 'axios'

export default defineNuxtPlugin(() => {
  // Create axios instance with default config
  const api = axios.create({
    baseURL: 'http://localhost:8000', // Your backend API
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  // Create external API instance (for third-party APIs like Pokemon)
  const externalApi = axios.create({
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  // Request interceptor
  api.interceptors.request.use(
    (config) => {
      // You can add auth tokens here if needed
      // const token = localStorage.getItem('token')
      // if (token) {
      //   config.headers.Authorization = `Bearer ${token}`
      // }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  // Response interceptor
  api.interceptors.response.use(
    (response) => {
      return response
    },
    (error) => {
      // Handle errors globally
      console.error('API Error:', error.response?.data || error.message)
      return Promise.reject(error)
    }
  )

  // Make it available throughout the app
  return {
    provide: {
      api,
      externalApi,
    },
  }
})
