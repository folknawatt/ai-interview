// Error and API Types
export interface ApiError {
  data?: {
    detail?: string
  }
  message?: string
  statusCode?: number
}

export type ApiRequestBody = Record<string, unknown> | FormData


// Helper function to safely extract error message
export function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }
  
  if (typeof error === 'object' && error !== null) {
    const apiError = error as ApiError
    if (apiError.data?.detail) {
      return apiError.data.detail
    }
    if (apiError.message) {
      return apiError.message
    }
  }
  
  if (typeof error === 'string') {
    return error
  }
  
  return 'An unexpected error occurred'
}
