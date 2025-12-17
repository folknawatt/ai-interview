/**
 * Authentication Service
 * Handles all authentication-related API calls
 */

import type { LoginResponse, User } from '@/types'

export const authService = {
  /**
   * Login with email and password
   */
  async login(email: string, password: string): Promise<LoginResponse> {
    const { post } = useApi()
    return await post<LoginResponse>('/auth/login', { email, password })
  },

  /**
   * Logout current user
   */
  async logout(): Promise<void> {
    const { post } = useApi()
    await post('/auth/logout')
  },

  /**
   * Refresh authentication token
   */
  async refreshToken(token: string): Promise<LoginResponse> {
    const { post } = useApi()
    return await post<LoginResponse>('/auth/refresh-token', {
      refreshToken: token
    })
  },

  /**
   * Get current user information
   */
  async getCurrentUser(): Promise<User> {
    const { get } = useApi()
    return await get<User>('/auth/me')
  }
}
