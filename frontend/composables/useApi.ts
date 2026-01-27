/**
 * Base API client using Nuxt's $fetch
 * Provides centralized error handling and base URL configuration
 */
import { useAuth } from '@/store/auth'

export const useApi = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBaseUrl || 'http://localhost:8000'
  const authStore = useAuth()

  /**
   * Centralized error handling helper
   */
  const handleError = (error: any, endpoint: string) => {
    console.error(`API Error [${endpoint}]:`, error)
    
    // Log detailed error structure for debugging
    if (process.env.NODE_ENV === 'development') {
      console.dir({
        data: error.data,
        message: error.message,
        statusCode: error.statusCode,
        statusMessage: error.statusMessage,
      }, { depth: null })
    }

    let errorMessage = 'API request failed'

    if (error.data) {
      if (typeof error.data === 'string') {
        errorMessage = error.data
      } else if (error.data.detail) {
        errorMessage = typeof error.data.detail === 'string' 
          ? error.data.detail 
          : JSON.stringify(error.data.detail)
      } else if (error.data.message) {
        errorMessage = typeof error.data.message === 'string'
          ? error.data.message
          : JSON.stringify(error.data.message)
      } else {
        errorMessage = JSON.stringify(error.data)
      }
    } else if (error.message) {
      // Sanitize "Failed to fetch" or weird network errors which might expose URLs
      if (error.message.includes('Failed to fetch') || error.message.includes('<no response>')) {
        errorMessage = 'Unable to connect to server. Please check your internet connection or try again later.'
      } else {
        errorMessage = error.message
      }
    } else if (error.statusMessage) {
      errorMessage = error.statusMessage
    }

    throw new Error(errorMessage)
  }

  /**
   * Get authorization headers if user is logged in
   */
  const getAuthHeaders = (): Record<string, string> => {
    const headers: Record<string, string> = {}
    if (authStore.isLogin && authStore.tokenAuth) {
      headers['Authorization'] = `Bearer ${authStore.tokenAuth}`
    }
    return headers
  }

  /**
   * Generic API call wrapper
   */
  const apiCall = async <T>(
    endpoint: string,
    options: {
      method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
      body?: any
      headers?: Record<string, string>
      skipAuth?: boolean
    } = {}
  ): Promise<T> => {
    try {
      return await $fetch<T>(`${apiBase}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...(options.skipAuth ? {} : getAuthHeaders()),
          ...options.headers,
        },
      })
    } catch (error: any) {
      handleError(error, endpoint)
      throw error // Unreachable due to handleError throwing, but keeps TS happy
    }
  }

  /**
   * Upload file with form data
   */
  const uploadFile = async <T>(endpoint: string, formData: FormData): Promise<T> => {
    try {
      return await $fetch<T>(`${apiBase}${endpoint}`, {
        method: 'POST',
        body: formData,
        // Content-Type is handled automatically by browser for FormData
      })
    } catch (error: any) {
      handleError(error, endpoint)
      throw error
    }
  }

  return {
    get: <T>(endpoint: string) => apiCall<T>(endpoint, { method: 'GET' }),
    post: <T>(endpoint: string, body?: any) => apiCall<T>(endpoint, { method: 'POST', body }),
    put: <T>(endpoint: string, body?: any) => apiCall<T>(endpoint, { method: 'PUT', body }),
    del: <T>(endpoint: string) => apiCall<T>(endpoint, { method: 'DELETE' }),
    uploadFile,
    apiBase,
  }
}
