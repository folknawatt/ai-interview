/**
 * Authentication Store
 * Manages user authentication state and tokens using Cookies for SSR support
 */

import { defineStore } from 'pinia'
import type { User } from '@/types'

export const useAuth = defineStore('auth', () => {
  // State - User data only (Tokens handled by HttpOnly cookies)
  const userData = useState<User | null>('auth_user', () => null)
  const loading = useState<boolean>('auth_loading', () => false)

  // Getters
  const isLogin = computed(() => !!userData.value)

  const currentUser = computed(() => userData.value)
  const userRole = computed(() => userData.value?.role)

  const hasRole = (role: string) => {
    return userData.value?.role === role
  }

  // Actions
  const fetchUser = async () => {
    try {
      loading.value = true
      const { get } = useApi()
      const user = await get<User>('/auth/me')
      userData.value = user
      return user
    } catch (error) {
      userData.value = null
      throw error
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      loading.value = true
      const { post } = useApi()
      await post('/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      userData.value = null
      loading.value = false
      const router = useRouter()
      router.push('/login')
    }
  }

  const setUser = (user: User) => {
    userData.value = user
  }

  return {
    // State
    currentUser,
    userRole,
    loading,
    
    // Getters
    isLogin,
    hasRole,
    
    // Actions
    fetchUser,
    logout,
    setUser
  }
})
