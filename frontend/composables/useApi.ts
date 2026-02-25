/**
 * Base API client using Nuxt's $fetch
 * Provides centralized error handling and base URL configuration
 */
import { useAuth } from '@/store/auth'
import type { ApiError, ApiRequestBody } from '@/types/errors'
import { getErrorMessage } from '@/types/errors'

export const useApi = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBaseUrl || 'http://localhost:8000'

  /**
   * Centralized error handling helper
   */
  const handleError = (error: unknown, endpoint: string) => {
    console.error(`API Error [${endpoint}]:`, error)
    
    // Log detailed error structure for debugging
    if (process.env.NODE_ENV === 'development' && typeof error === 'object' && error !== null) {
      const apiError = error as ApiError
      console.dir({
        data: apiError.data,
        message: apiError.message,
        statusCode: apiError.statusCode,
      }, { depth: null })
    }

    const errorMessage = getErrorMessage(error)
    throw new Error(errorMessage)
  }

  /**
   * Generic API call wrapper
   * Browser automatically handles cookies/headers
   */
  const apiCall = async <T>(
    endpoint: string,
    options: {
      method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
      body?: ApiRequestBody
      headers?: Record<string, string>
      skipAuth?: boolean
    } = {}
  ): Promise<T> => {
    try {
      return await $fetch<T>(`${apiBase}${endpoint}`, {
        ...options,
        credentials: 'include', // Required for cross-origin cookies (localhost:3000 -> localhost:8000)
        // Important: credentials mode is handled by Nuxt/Fetch automatically for same-origin or configured domains
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      })
    } catch (error: unknown) {
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
        credentials: 'include', // Required for cross-origin cookies (same as apiCall)
        // Content-Type is handled automatically by browser for FormData
      })
    } catch (error: unknown) {
      handleError(error, endpoint)
      throw error
    }
  }

  return {
    get: <T>(endpoint: string) => apiCall<T>(endpoint, { method: 'GET' }),
    post: <T>(endpoint: string, body?: ApiRequestBody) => apiCall<T>(endpoint, { method: 'POST', body }),
    put: <T>(endpoint: string, body?: ApiRequestBody) => apiCall<T>(endpoint, { method: 'PUT', body }),
    del: <T>(endpoint: string) => apiCall<T>(endpoint, { method: 'DELETE' }),
    uploadFile,
    apiBase,
  }
}
