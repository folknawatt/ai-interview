/**
 * Base API client using Nuxt's $fetch
 * Provides centralized error handling and base URL configuration
 */

export const useApi = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase || 'http://localhost:8000'

  /**
   * Generic API call wrapper
   */
  const apiCall = async <T>(
    endpoint: string,
    options: {
      method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
      body?: any
      headers?: Record<string, string>
    } = {}
  ): Promise<T> => {
    try {
      const url = `${apiBase}${endpoint}`

      const response = (await $fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      })) as T

      return response
    } catch (error: any) {
      console.error(`API Error [${endpoint}]:`, error)
      console.error('Error details:', {
        data: error.data,
        message: error.message,
        statusCode: error.statusCode,
        statusMessage: error.statusMessage,
      })

      // Handle different error types and ensure we always get a string message
      let errorMessage = 'API request failed'

      if (error.data) {
        // Extract message from various possible formats
        if (typeof error.data === 'string') {
          errorMessage = error.data
        } else if (error.data.detail) {
          errorMessage =
            typeof error.data.detail === 'string'
              ? error.data.detail
              : JSON.stringify(error.data.detail)
        } else if (error.data.message) {
          errorMessage =
            typeof error.data.message === 'string'
              ? error.data.message
              : JSON.stringify(error.data.message)
        } else {
          errorMessage = JSON.stringify(error.data)
        }
      } else if (error.message && typeof error.message === 'string') {
        errorMessage = error.message
      } else if (error.statusMessage) {
        errorMessage = error.statusMessage
      }

      throw new Error(errorMessage)
    }
  }

  /**
   * GET request
   */
  const get = <T>(endpoint: string) => {
    return apiCall<T>(endpoint, { method: 'GET' as const })
  }

  /**
   * POST request
   */
  const post = <T>(endpoint: string, body?: any) => {
    return apiCall<T>(endpoint, {
      method: 'POST' as const,
      body,
    })
  }

  /**
   * PUT request
   */
  const put = <T>(endpoint: string, body?: any) => {
    return apiCall<T>(endpoint, {
      method: 'PUT' as const,
      body,
    })
  }

  /**
   * DELETE request
   */
  const del = <T>(endpoint: string) => {
    return apiCall<T>(endpoint, {
      method: 'DELETE' as const,
    })
  }

  /**
   * Upload file with form data
   */
  const uploadFile = async <T>(endpoint: string, formData: FormData): Promise<T> => {
    try {
      const url = `${apiBase}${endpoint}`

      // Don't set Content-Type header for file uploads - browser will set it with boundary
      const response = (await $fetch(url, {
        method: 'POST',
        body: formData,
      })) as T

      return response
    } catch (error: any) {
      console.error(`Upload Error [${endpoint}]:`, error)
      throw new Error(error.data?.detail || error.message || 'Upload failed')
    }
  }

  return {
    get,
    post,
    put,
    del,
    uploadFile,
    apiBase,
  }
}
