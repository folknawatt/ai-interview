/**
 * Authentication Store
 * Manages user authentication state and tokens using Cookies for SSR support
 */

import { defineStore } from 'pinia'
import type { User } from '@/types'

export const useAuth = defineStore('auth', () => {
  // State - using useCookie for SSR support
  const tokenAuth = useCookie<string | null>('auth_token', {
    maxAge: 60 * 60 * 24 * 7, // 7 days
    sameSite: 'lax'
  })
  
  const refreshTokenAuth = useCookie<string | null>('auth_refresh_token', {
    maxAge: 60 * 60 * 24 * 30, // 30 days
    sameSite: 'lax'
  })
  
  const userData = useCookie<User | null>('auth_user', {
    maxAge: 60 * 60 * 24 * 7,
    sameSite: 'lax'
  })

  // Getters
  const isLogin = computed(() => !!tokenAuth.value)
  
  const bearerToken = computed(() => {
    return tokenAuth.value ? `Bearer ${tokenAuth.value}` : ''
  })

  const currentUser = computed(() => userData.value)
  const userRole = computed(() => userData.value?.role)

  const hasRole = (role: string) => {
    return userData.value?.role === role
  }

  // Actions
  const signInAuth = (token: string, refreshToken: string, user?: User) => {
    tokenAuth.value = token
    refreshTokenAuth.value = refreshToken
    if (user) {
      userData.value = user
    }
  }

  const setUser = (user: User) => {
    userData.value = user
  }

  const clearToken = () => {
    tokenAuth.value = null
    refreshTokenAuth.value = null
    userData.value = null
  }

  return {
    // State
    tokenAuth,
    refreshTokenAuth,
    currentUser,
    userRole,
    
    // Getters
    isLogin,
    bearerToken,
    hasRole,
    
    // Actions
    signInAuth,
    setUser,
    clearToken
  }
})
